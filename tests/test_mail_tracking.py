"""Synthetic SQLite/SMTP-boundary tests; never authenticate or contact a server."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from contextlib import closing
from datetime import datetime, timezone
from email import policy
from email.parser import BytesParser
import hashlib
import importlib.util
import json
from pathlib import Path
import smtplib
import sqlite3
import subprocess
import sys
import tempfile
import threading
import unittest
from uuid import UUID

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "mail_tracking.py"
spec = importlib.util.spec_from_file_location("mail_tracking", SCRIPT)
mail = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mail)


class FakeSMTP:
    """Only the authenticated client's sendmail boundary is substituted."""

    debuglevel = 0

    def __init__(self, action=None):
        self.action = action
        self.calls = []

    def sendmail(self, sender, recipients, wire):
        self.calls.append((sender, recipients, wire))
        if self.action:
            return self.action(sender, recipients, wire)
        return {}


def raising(error):
    def fail(*_):
        raise error
    return fail


class MailTrackingTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="reader-mail-test-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.db = self.root / "private" / "tracking.sqlite3"

    def prepare(self, report_id="REPORT-001", **changes):
        fields = dict(sender="sender@example.invalid", recipient="reader@example.invalid",
                      subject="Synthetic report", body="Private synthetic body.\n.second line\n")
        fields.update(changes)
        return mail.prepare_report(report_id, db_path=self.db, **fields)

    def row(self):
        with closing(sqlite3.connect(self.db)) as connection:
            connection.row_factory = sqlite3.Row
            return dict(connection.execute("SELECT * FROM reports").fetchone())

    def execute(self, statement, parameters=()):
        with closing(sqlite3.connect(self.db)) as connection, connection:
            connection.execute(statement, parameters)

    def cli(self, *arguments):
        return subprocess.run([sys.executable, "-X", "utf8", "-B", str(SCRIPT),
                               "--db", str(self.db), *arguments], cwd=self.root,
                              capture_output=True, text=True, encoding="utf-8", timeout=15)

    def test_init_creates_a_durable_sqlite_ledger(self):
        mail.init_db(self.db)
        self.assertTrue(self.db.is_file(), "init must persist a ledger, not just return success")
        with closing(sqlite3.connect(self.db)) as connection:
            self.assertEqual(connection.execute("PRAGMA integrity_check").fetchone()[0], "ok")
        self.assertEqual(mail.list_reports(db_path=self.db), [])

    def test_prepare_persists_identity_content_and_utc_before_return(self):
        before = datetime.now(timezone.utc)
        draft = self.prepare(body="Café\n")
        self.assertEqual(draft["status"], "draft")
        self.assertEqual(draft["report_id"], "REPORT-001")
        self.assertEqual(UUID(draft["attempt_id"]).version, 4)
        self.assertTrue(draft["prepared_at"].endswith("Z"))
        self.assertGreaterEqual(datetime.fromisoformat(draft["prepared_at"]), before)
        self.assertEqual(draft["content_sha256"], hashlib.sha256("Café\n".encode()).hexdigest())
        row = self.row()
        self.assertEqual(row["attempt_id"], draft["attempt_id"])
        self.assertEqual(hashlib.sha256(row["wire_bytes"]).hexdigest(), draft["wire_sha256"])
        message = BytesParser(policy=policy.default).parsebytes(row["wire_bytes"])
        self.assertEqual(str(message["From"]), "sender@example.invalid")
        self.assertEqual(str(message["To"]), "reader@example.invalid")
        self.assertEqual(str(message["Subject"]), "Synthetic report")
        self.assertEqual(str(message["Message-ID"]), draft["message_id"])
        self.assertRegex(draft["message_id"], r"^<[0-9a-f]{32}@report\.invalid>$")
        self.assertEqual(message.get_content().replace("\r\n", "\n"), "Café\n")
        self.assertIsNone(message["Cc"])
        self.assertIsNone(message["Bcc"])
        self.assertIsNone(draft["attempted_at"])
        self.assertIsNone(draft["outcome_at"])

    def test_duplicate_prepare_reuses_every_original_identity_and_wire_byte(self):
        first = self.prepare()
        original = self.row()
        self.assertEqual(self.prepare(), first)
        self.assertEqual(self.row(), original)
        self.assertEqual(len(mail.list_reports(db_path=self.db)), 1)
        mail.init_db(self.db)
        self.assertEqual(self.row(), original)

    def test_same_report_id_cannot_change_any_envelope_or_content_field(self):
        self.prepare()
        original = self.row()
        for field, replacement in (("sender", "other@example.invalid"),
                                   ("recipient", "other@example.invalid"),
                                   ("subject", "Changed subject"), ("body", "Changed body")):
            with self.subTest(field=field):
                with self.assertRaises(mail.ReportConflict):
                    self.prepare(**{field: replacement})
                self.assertEqual(self.row(), original)

    def test_separate_reports_get_separate_attempts_and_message_ids(self):
        first = self.prepare()
        second = self.prepare("REPORT-002")
        self.assertNotEqual(first["attempt_id"], second["attempt_id"])
        self.assertNotEqual(first["message_id"], second["message_id"])
        self.assertEqual(first["content_sha256"], second["content_sha256"])

    def test_unsafe_addresses_are_rejected_without_creating_a_ledger(self):
        bad = ["", "a@example.invalid,b@example.invalid", "Name <a@example.invalid>",
               "a@example.invalid\r\nBcc: b@example.invalid", "a@example.invalid\x00",
               " a@example.invalid", "a@example.invalid ", "a..b@example.invalid",
               ".a@example.invalid", "a.@example.invalid", "a@-example.invalid",
               "a@example-.invalid", "a@example..invalid", "a@[127.0.0.1]",
               "a@localhost", '"quoted"@example.invalid', "a(comment)@example.invalid",
               "a;@example.invalid", "ü@example.invalid", "a@exam​ple.invalid",
               "a" * 65 + "@example.invalid", "a@" + "b" * 64 + ".invalid"]
        for field in ("sender", "recipient"):
            for address in bad:
                with self.subTest(field=field, address=repr(address)):
                    with self.assertRaises(ValueError):
                        self.prepare(**{field: address})
                    self.assertFalse(self.db.exists())

    def test_header_and_id_controls_are_rejected_before_storage(self):
        for subject in ("", " ", "Hello\r\nBcc: b@example.invalid", "nul\x00", "tab\t",
                        "del\x7f", "bidi‮", "x" * 999):
            with self.subTest(subject=repr(subject)):
                with self.assertRaises(ValueError):
                    self.prepare(subject=subject)
        for report_id in ("", "space id", "r\n", "r\x00", "x" * 129):
            with self.subTest(report_id=repr(report_id)):
                with self.assertRaises(ValueError):
                    self.prepare(report_id)
        self.assertFalse(self.db.exists())

    def test_valid_unicode_subject_and_sql_like_text_remain_data(self):
        draft = self.prepare(subject="Café: '); DROP TABLE reports; --",
                             sender="writer+reports@example.invalid")
        self.assertEqual(mail.list_reports(db_path=self.db)[0], draft)
        message = BytesParser(policy=policy.default).parsebytes(self.row()["wire_bytes"])
        self.assertEqual(str(message["Subject"]), "Café: '); DROP TABLE reports; --")

    def test_acceptance_uses_exact_persisted_bytes_after_durable_attempt_claim(self):
        draft = self.prepare()
        wire = self.row()["wire_bytes"]

        def accept(sender, recipients, payload):
            active = self.row()
            self.assertEqual(active["status"], "attempting")
            self.assertIsNotNone(active["attempted_at"])
            self.assertEqual(sender, "sender@example.invalid")
            self.assertEqual(recipients, ["reader@example.invalid"])
            self.assertIsInstance(payload, bytes)
            self.assertEqual(payload, wire)
            return {}

        smtp = FakeSMTP(accept)
        result = mail.submit_report(draft["attempt_id"], smtp, db_path=self.db)
        self.assertEqual(result["status"], "accepted")
        self.assertEqual(result["smtp_code"], 250)
        self.assertIsNotNone(result["outcome_at"])
        self.assertEqual(self.row()["status"], "accepted")
        self.assertEqual(len(smtp.calls), 1)
        self.assertEqual(self.prepare()["status"], "accepted")
        with self.assertRaises(mail.SubmissionBlocked):
            mail.submit_report(draft["attempt_id"], smtp, db_path=self.db)
        self.assertEqual(len(smtp.calls), 1)

    def test_explicit_smtp_rejections_are_not_acceptance(self):
        errors = [smtplib.SMTPSenderRefused(550, b"PRIVATE RESPONSE", "sender@example.invalid"),
                  smtplib.SMTPRecipientsRefused({"reader@example.invalid": (450, b"PRIVATE RESPONSE")}),
                  smtplib.SMTPDataError(554, b"PRIVATE RESPONSE"),
                  smtplib.SMTPHeloError(500, b"PRIVATE RESPONSE")]
        for index, error in enumerate(errors):
            with self.subTest(error=type(error).__name__):
                draft = self.prepare(f"REJECT-{index}")
                smtp = FakeSMTP(raising(error))
                result = mail.submit_report(draft["attempt_id"], smtp, db_path=self.db)
                self.assertEqual(result["status"], "rejected")
                self.assertTrue(400 <= result["smtp_code"] <= 599)
                with self.assertRaises(mail.SubmissionBlocked):
                    mail.submit_report(draft["attempt_id"], smtp, db_path=self.db)
                self.assertEqual(len(smtp.calls), 1)
        self.assertNotIn(b"PRIVATE RESPONSE", self.db.read_bytes())

    def test_disconnect_and_unexpected_protocol_results_are_unknown_never_retried(self):
        actions = [raising(smtplib.SMTPServerDisconnected("PRIVATE RESPONSE")),
                   raising(TimeoutError("PRIVATE RESPONSE")), raising(OSError("PRIVATE RESPONSE")),
                   raising(smtplib.SMTPDataError(354, b"PRIVATE RESPONSE")),
                   raising(smtplib.SMTPResponseException(250, b"PRIVATE RESPONSE")),
                   lambda *_: None, lambda *_: [],
                   lambda *_: {"reader@example.invalid": (550, b"PRIVATE RESPONSE")}]
        for index, action in enumerate(actions):
            with self.subTest(index=index):
                draft = self.prepare(f"UNKNOWN-{index}")
                smtp = FakeSMTP(action)
                result = mail.submit_report(draft["attempt_id"], smtp, db_path=self.db)
                self.assertEqual(result["status"], "unknown")
                self.assertIsNone(result["smtp_code"])
                with self.assertRaises(mail.SubmissionBlocked):
                    mail.submit_report(draft["attempt_id"], smtp, db_path=self.db)
                self.assertEqual(len(smtp.calls), 1)
        self.assertNotIn(b"PRIVATE RESPONSE", self.db.read_bytes())

    def test_crash_during_network_leaves_attempting_and_blocks_replay(self):
        draft = self.prepare()
        smtp = FakeSMTP(raising(KeyboardInterrupt()))
        with self.assertRaises(KeyboardInterrupt):
            mail.submit_report(draft["attempt_id"], smtp, db_path=self.db)
        self.assertEqual(self.row()["status"], "attempting")
        mail.init_db(self.db)
        with self.assertRaises(mail.SubmissionBlocked):
            mail.submit_report(draft["attempt_id"], smtp, db_path=self.db)
        self.assertEqual(len(smtp.calls), 1)

    def test_concurrent_submissions_call_smtp_once_without_holding_db_lock(self):
        draft = self.prepare()
        entered = threading.Event()
        release = threading.Event()

        def accept(*_):
            entered.set()
            if not release.wait(10):
                raise TimeoutError("test synchronization")
            return {}

        smtp = FakeSMTP(accept)
        with ThreadPoolExecutor(max_workers=2) as pool:
            first = pool.submit(mail.submit_report, draft["attempt_id"], smtp, db_path=self.db)
            try:
                self.assertTrue(entered.wait(5))
                second = pool.submit(mail.submit_report, draft["attempt_id"], smtp, db_path=self.db)
                with self.assertRaises(mail.SubmissionBlocked):
                    second.result(timeout=5)
                self.assertEqual(self.row()["status"], "attempting")
                self.prepare("UNRELATED-REPORT")
            finally:
                release.set()
            self.assertEqual(first.result(timeout=5)["status"], "accepted")
        self.assertEqual(len(smtp.calls), 1)

    def test_concurrent_prepare_creates_only_one_immutable_draft(self):
        with ThreadPoolExecutor(max_workers=6) as pool:
            results = list(pool.map(lambda _: self.prepare(), range(6)))
        self.assertTrue(all(result == results[0] for result in results))
        self.assertEqual(len(mail.list_reports(db_path=self.db)), 1)

    def test_claim_write_failure_sends_nothing_and_preserves_draft(self):
        draft = self.prepare()
        self.execute("""CREATE TRIGGER fail_claim BEFORE UPDATE OF status ON reports
                        WHEN NEW.status = 'attempting'
                        BEGIN SELECT RAISE(ABORT, 'synthetic storage failure'); END""")
        smtp = FakeSMTP()
        with self.assertRaises(sqlite3.Error):
            mail.submit_report(draft["attempt_id"], smtp, db_path=self.db)
        self.assertEqual(smtp.calls, [])
        self.assertEqual(self.row()["status"], "draft")

    def test_failed_acceptance_write_leaves_nonretryable_attempt_and_explicit_warning(self):
        draft = self.prepare()
        self.execute("""CREATE TRIGGER fail_outcome BEFORE UPDATE OF status ON reports
                        WHEN NEW.status = 'accepted'
                        BEGIN SELECT RAISE(ABORT, 'synthetic storage failure'); END""")
        smtp = FakeSMTP()
        with self.assertRaises(mail.OutcomeNotRecorded) as raised:
            mail.submit_report(draft["attempt_id"], smtp, db_path=self.db)
        self.assertEqual(raised.exception.outcome, "accepted")
        self.assertIn("Do not resubmit", str(raised.exception))
        self.assertEqual(self.row()["status"], "attempting")
        with self.assertRaises(mail.SubmissionBlocked):
            mail.submit_report(draft["attempt_id"], smtp, db_path=self.db)
        self.assertEqual(len(smtp.calls), 1)

    def test_failed_rejection_or_unknown_write_also_blocks_replay(self):
        mail.init_db(self.db)
        self.execute("""CREATE TRIGGER fail_other_outcomes BEFORE UPDATE OF status ON reports
                        WHEN NEW.status IN ('rejected', 'unknown')
                        BEGIN SELECT RAISE(ABORT, 'synthetic storage failure'); END""")
        cases = [("rejected", smtplib.SMTPDataError(550, b"PRIVATE RESPONSE")),
                 ("unknown", smtplib.SMTPServerDisconnected("PRIVATE RESPONSE"))]
        for status, error in cases:
            with self.subTest(status=status):
                draft = self.prepare(f"OUTCOME-{status}")
                smtp = FakeSMTP(raising(error))
                with self.assertRaises(mail.OutcomeNotRecorded) as raised:
                    mail.submit_report(draft["attempt_id"], smtp, db_path=self.db)
                self.assertEqual(raised.exception.outcome, status)
                record = next(row for row in mail.list_reports(db_path=self.db)
                              if row["attempt_id"] == draft["attempt_id"])
                self.assertEqual(record["status"], "attempting")
                self.assertIsNone(record["outcome_at"])
                with self.assertRaises(mail.SubmissionBlocked):
                    mail.submit_report(draft["attempt_id"], smtp, db_path=self.db)
                self.assertEqual(len(smtp.calls), 1)
        self.assertNotIn(b"PRIVATE RESPONSE", self.db.read_bytes())

    def test_claim_commit_failure_cannot_cross_the_smtp_boundary(self):
        draft = self.prepare()
        smtp = FakeSMTP()
        with closing(sqlite3.connect(self.db)) as reader:
            reader.execute("BEGIN")
            reader.execute("SELECT * FROM reports").fetchall()
            with self.assertRaises(sqlite3.OperationalError):
                mail.submit_report(draft["attempt_id"], smtp, db_path=self.db)
        self.assertEqual(smtp.calls, [])
        self.assertEqual(self.row()["status"], "draft")
        self.assertIsNone(self.row()["attempted_at"])

    def test_outcome_commit_failure_preserves_nonretryable_attempt_after_acceptance(self):
        draft = self.prepare()
        with closing(sqlite3.connect(self.db)) as reader:
            def accept(*_):
                # A real reader lock permits UPDATE but prevents its final commit.
                reader.execute("BEGIN")
                reader.execute("SELECT * FROM reports").fetchall()
                return {}

            smtp = FakeSMTP(accept)
            with self.assertRaises(mail.OutcomeNotRecorded) as raised:
                mail.submit_report(draft["attempt_id"], smtp, db_path=self.db)
        self.assertEqual(raised.exception.outcome, "accepted")
        self.assertEqual(self.row()["status"], "attempting")
        self.assertIsNone(self.row()["outcome_at"])
        with self.assertRaises(mail.SubmissionBlocked):
            mail.submit_report(draft["attempt_id"], smtp, db_path=self.db)
        self.assertEqual(len(smtp.calls), 1)

    def test_prepared_identity_and_terminal_status_cannot_be_overwritten(self):
        draft = self.prepare()
        with self.assertRaises(sqlite3.IntegrityError):
            self.execute("UPDATE reports SET recipient = ?", ("other@example.invalid",))
        self.assertEqual(self.row()["recipient"], "reader@example.invalid")
        mail.submit_report(draft["attempt_id"], FakeSMTP(), db_path=self.db)
        with self.assertRaises(sqlite3.IntegrityError):
            self.execute("UPDATE reports SET status = 'draft'")
        self.assertEqual(self.row()["status"], "accepted")

    def test_failed_prepare_inserts_no_incomplete_draft(self):
        mail.init_db(self.db)
        self.execute("""CREATE TRIGGER fail_prepare AFTER INSERT ON reports
                        BEGIN SELECT RAISE(ABORT, 'synthetic storage failure'); END""")
        with self.assertRaises(sqlite3.Error):
            self.prepare()
        self.assertEqual(mail.list_reports(db_path=self.db), [])

    def test_missing_ledger_or_attempt_never_invokes_smtp(self):
        smtp = FakeSMTP()
        with self.assertRaises(sqlite3.Error):
            mail.submit_report("missing", smtp, db_path=self.db)
        self.assertFalse(self.db.exists())
        mail.init_db(self.db)
        with self.assertRaises(KeyError):
            mail.submit_report("missing", smtp, db_path=self.db)
        self.assertEqual(smtp.calls, [])

    def test_smtp_debug_mode_is_refused_before_claim_or_network(self):
        draft = self.prepare()
        smtp = FakeSMTP()
        smtp.debuglevel = 1
        with self.assertRaises(ValueError):
            mail.submit_report(draft["attempt_id"], smtp, db_path=self.db)
        self.assertEqual(self.row()["status"], "draft")
        self.assertEqual(smtp.calls, [])

    def test_metadata_has_no_body_wire_or_delivery_read_claim(self):
        draft = self.prepare(body="BODY-MUST-STAY-PRIVATE")
        mail.submit_report(draft["attempt_id"], FakeSMTP(), db_path=self.db)
        listed = mail.list_reports(db_path=self.db)
        self.assertEqual(len(listed), 1)
        self.assertEqual(listed[0]["status"], "accepted")
        serialized = json.dumps(listed)
        for forbidden in ("BODY-MUST-STAY-PRIVATE", "wire_bytes", "password", "credential",
                          "delivered", "read_at"):
            self.assertNotIn(forbidden, serialized)
        self.assertNotIn("wire_bytes", draft)

    def test_cli_init_prepare_list_are_offline_and_do_not_print_body(self):
        result = self.cli("init")
        self.assertEqual(result.returncode, 0, result.stderr)
        body = self.root / "synthetic.txt"
        body.write_text("CLI-BODY-MUST-STAY-PRIVATE", encoding="utf-8")
        result = self.cli("prepare", "REPORT-CLI", "--sender", "sender@example.invalid",
                          "--recipient", "reader@example.invalid", "--subject", "Synthetic CLI report",
                          "--body-file", str(body))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["status"], "draft")
        result = self.cli("list")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)[0]["report_id"], "REPORT-CLI")
        self.assertNotIn("CLI-BODY-MUST-STAY-PRIVATE", result.stdout + result.stderr)
        for command in ("send", "scan", "import", "auth"):
            self.assertNotEqual(self.cli(command).returncode, 0)
        self.assertEqual(self.row()["status"], "draft")


if __name__ == "__main__":
    unittest.main()
