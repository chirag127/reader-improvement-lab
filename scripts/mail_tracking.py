"""Private, offline report preparation and one-shot SMTP submission tracking.

Only submit_report performs transport, using a caller-owned, already authenticated
smtplib client. It does not authorize a send. Review the prepared recipient, subject
and content before separately authorizing that call. 'accepted' means final SMTP
DATA acceptance, never delivery or reading. Every non-draft state blocks replay;
uncertain attempts need manual reconciliation, not a new report ID to bypass them.

The default ledger is Git-ignored, not encrypted. New POSIX files are owner-only;
on Windows use a directory with private inherited ACLs. Never publish the database.
No credentials, transcripts, mailbox scanning, or historical receipt imports belong
here. Historical observations are not transport receipts.
"""

from __future__ import annotations

import argparse
from contextlib import closing, contextmanager
from datetime import datetime, timezone
from email import policy
from email.message import EmailMessage
from email.utils import format_datetime
import hashlib
import json
import os
from pathlib import Path
import re
import smtplib
import sqlite3
import sys
import unicodedata
from uuid import uuid4

DEFAULT_DB = Path(__file__).resolve().parents[1] / ".local" / "mail" / "tracking.sqlite3"
_METADATA = ("report_id", "attempt_id", "prepared_at", "sender", "recipient", "subject",
             "content_sha256", "message_id", "wire_sha256", "status", "attempted_at",
             "outcome_at", "smtp_code")
_ADDRESS = re.compile(
    r"[A-Za-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[A-Za-z0-9!#$%&'*+/=?^_`{|}~-]+)*@"
    r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?"
    r"(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?)+"
)


class ReportConflict(ValueError):
    """A report ID is already bound to different content or envelope fields."""


class SubmissionBlocked(RuntimeError):
    """This attempt has already left draft state and cannot be submitted again."""


class OutcomeNotRecorded(RuntimeError):
    """The transport outcome could not be durably recorded; replay is unsafe."""

    def __init__(self, outcome):
        self.outcome = outcome
        super().__init__(f"SMTP outcome {outcome}; ledger update failed. Do not resubmit. "
                         "Reconcile the existing attempt manually.")


def _utc_now():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


@contextmanager
def _connection(db_path):
    # mode=rw prevents a typo in a lookup/submission from creating an empty ledger.
    uri = Path(db_path).resolve().as_uri() + "?mode=rw"
    with closing(sqlite3.connect(uri, uri=True, timeout=5)) as connection:
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA synchronous = FULL")
        with connection:
            yield connection


def init_db(db_path=DEFAULT_DB):
    """Create the ledger offline; preserve all existing rows on repeated calls."""
    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    try:
        descriptor = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError:
        pass
    else:
        os.close(descriptor)
    with _connection(path) as connection:
        connection.execute("BEGIN IMMEDIATE")
        connection.execute("""CREATE TABLE IF NOT EXISTS reports (
            report_id TEXT PRIMARY KEY NOT NULL,
            attempt_id TEXT UNIQUE NOT NULL,
            prepared_at TEXT NOT NULL,
            sender TEXT NOT NULL,
            recipient TEXT NOT NULL,
            subject TEXT NOT NULL,
            content_sha256 TEXT NOT NULL,
            payload_sha256 TEXT NOT NULL,
            message_id TEXT UNIQUE NOT NULL,
            wire_sha256 TEXT NOT NULL,
            wire_bytes BLOB NOT NULL,
            status TEXT NOT NULL CHECK(status IN ('draft','attempting','accepted','rejected','unknown')),
            attempted_at TEXT,
            outcome_at TEXT,
            smtp_code INTEGER
        )""")
        connection.execute("""CREATE TRIGGER IF NOT EXISTS immutable_report
            BEFORE UPDATE OF report_id, attempt_id, prepared_at, sender, recipient,
                subject, content_sha256, payload_sha256, message_id, wire_sha256, wire_bytes
            ON reports BEGIN SELECT RAISE(ABORT, 'prepared reports are immutable'); END""")
        connection.execute("""CREATE TRIGGER IF NOT EXISTS forward_only_status
            BEFORE UPDATE OF status ON reports
            WHEN NOT ((OLD.status = 'draft' AND NEW.status = 'attempting') OR
                      (OLD.status = 'attempting' AND NEW.status IN ('accepted','rejected','unknown')))
            BEGIN SELECT RAISE(ABORT, 'submission state cannot be replayed'); END""")


def _validate_address(value, field):
    if (not isinstance(value, str) or len(value) > 254 or not _ADDRESS.fullmatch(value)
            or len(value.split('@')[0]) > 64):
        raise ValueError(f"{field} must be one bare ASCII email address; no names, lists or headers")


def _metadata(row):
    return {key: row[key] for key in _METADATA}


def list_reports(*, db_path=DEFAULT_DB):
    """Return envelope/status metadata only; never return body or raw wire bytes."""
    with _connection(db_path) as connection:
        rows = connection.execute("SELECT " + ", ".join(_METADATA) +
                                  " FROM reports ORDER BY prepared_at, report_id")
        return [_metadata(row) for row in rows]


def prepare_report(report_id, *, sender, recipient, subject, body, db_path=DEFAULT_DB):
    """Freeze a single plain-text report; identical ID/payload returns its saved state.

    content_sha256 hashes the exact UTF-8 input body, before MIME/CRLF encoding;
    wire_sha256 hashes the complete frozen RFC 5322 message passed to sendmail.
    SMTP dot-stuffing and framing remain the transport client's responsibility.
    """
    if not isinstance(report_id, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,127}", report_id):
        raise ValueError("report_id must be 1-128 ASCII letters, digits or . _ : -")
    _validate_address(sender, "sender")
    _validate_address(recipient, "recipient")
    if (not isinstance(subject, str) or not subject.strip() or len(subject) > 998
            or any(unicodedata.category(char)[0] == "C" or
                   unicodedata.category(char) in ("Zl", "Zp") for char in subject)):
        raise ValueError("subject must be a nonblank single header without control characters")
    if not isinstance(body, str):
        raise ValueError("body must be plain text")
    content_sha256 = hashlib.sha256(body.encode("utf-8")).hexdigest()
    payload = json.dumps([sender, recipient, subject, body], ensure_ascii=True, separators=(",", ":"))
    payload_sha256 = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    init_db(db_path)
    with _connection(db_path) as connection:
        connection.execute("BEGIN IMMEDIATE")
        existing = connection.execute("SELECT * FROM reports WHERE report_id = ?", (report_id,)).fetchone()
        if existing is not None:
            if existing["payload_sha256"] != payload_sha256:
                raise ReportConflict("report_id already identifies a different payload; original preserved")
            return _metadata(existing)
        prepared_at = _utc_now()
        attempt_id = str(uuid4())
        message_id = f"<{uuid4().hex}@report.invalid>"
        message = EmailMessage(policy=policy.SMTP)
        message["From"] = sender
        message["To"] = recipient
        message["Subject"] = subject
        message["Date"] = format_datetime(datetime.fromisoformat(prepared_at), usegmt=True)
        message["Message-ID"] = message_id
        message.set_content(body, charset="utf-8", cte="quoted-printable")
        wire = message.as_bytes()
        connection.execute("""INSERT INTO reports
            (report_id, attempt_id, prepared_at, sender, recipient, subject, content_sha256,
             payload_sha256, message_id, wire_sha256, wire_bytes, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'draft')""",
            (report_id, attempt_id, prepared_at, sender, recipient, subject, content_sha256,
             payload_sha256, message_id, hashlib.sha256(wire).hexdigest(), wire))
        row = connection.execute("SELECT * FROM reports WHERE attempt_id = ?", (attempt_id,)).fetchone()
        result = _metadata(row)
    return result


def _claim(attempt_id, db_path):
    with _connection(db_path) as connection:
        connection.execute("BEGIN IMMEDIATE")
        row = connection.execute("SELECT * FROM reports WHERE attempt_id = ?", (attempt_id,)).fetchone()
        if row is None:
            raise KeyError("Prepared attempt not found")
        if row["status"] != "draft":
            raise SubmissionBlocked(f"Attempt is {row['status']}; do not resubmit")
        if hashlib.sha256(row["wire_bytes"]).hexdigest() != row["wire_sha256"]:
            raise ValueError("Stored message integrity check failed; no submission attempted")
        claimed = connection.execute("""UPDATE reports SET status = 'attempting', attempted_at = ?
                                        WHERE attempt_id = ? AND status = 'draft'""", (_utc_now(), attempt_id))
        if claimed.rowcount != 1:
            raise SubmissionBlocked("Attempt is no longer a draft; do not resubmit")
        payload = (row["sender"], [row["recipient"]], row["wire_bytes"])
    # The commit and close finish before the SMTP boundary, even after a crash/restart.
    return payload


def _rejection_code(error, recipient):
    if isinstance(error, smtplib.SMTPRecipientsRefused):
        refused = error.recipients
        if not isinstance(refused, dict) or set(refused) != {recipient}:
            return None
        response = refused[recipient]
        if not isinstance(response, tuple) or len(response) != 2:
            return None
        code = response[0]
    elif isinstance(error, (smtplib.SMTPSenderRefused, smtplib.SMTPDataError, smtplib.SMTPHeloError)):
        code = error.smtp_code
    else:
        return None
    return code if type(code) is int and 400 <= code <= 599 else None


def submit_report(attempt_id, smtp, *, db_path=DEFAULT_DB):
    """Submit once through an already authenticated, debug-disabled smtplib client.

    Caller owns authorization, TLS/authentication and client lifecycle. This wrapper
    never retries, reconnects, quits, or loads credentials. Outcome storage failures
    raise OutcomeNotRecorded: the durable attempting state still blocks resubmission.
    """
    if getattr(smtp, "debuglevel", 0):
        raise ValueError("SMTP debug output must be disabled before submitting private reports")
    if not callable(getattr(smtp, "sendmail", None)):
        raise ValueError("An authenticated SMTP client with sendmail is required")
    sender, recipients, wire = _claim(attempt_id, db_path)
    smtp_code = None
    status = "unknown"
    try:
        refused = smtp.sendmail(sender, recipients, wire)
        # With exactly one recipient, smtplib returns {} only after final DATA 250.
        if type(refused) is dict and not refused:
            status, smtp_code = "accepted", 250
    except Exception as error:
        smtp_code = _rejection_code(error, recipients[0])
        if smtp_code is not None:
            status = "rejected"
    try:
        with _connection(db_path) as connection:
            updated = connection.execute("""UPDATE reports SET status = ?, smtp_code = ?, outcome_at = ?
                                            WHERE attempt_id = ? AND status = 'attempting'""",
                                         (status, smtp_code, _utc_now(), attempt_id))
            if updated.rowcount != 1:
                raise sqlite3.IntegrityError("Attempt state changed before outcome recording")
            result = _metadata(connection.execute("SELECT * FROM reports WHERE attempt_id = ?",
                                                   (attempt_id,)).fetchone())
    except (sqlite3.Error, OSError):
        raise OutcomeNotRecorded(status) from None
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description="Offline private report ledger; this CLI cannot send mail.")
    parser.add_argument("--db", type=Path, default=DEFAULT_DB)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("init", help="initialize a private local ledger")
    commands.add_parser("list", help="list envelope and status metadata, excluding bodies")
    prepare = commands.add_parser("prepare", help="freeze one unsent report from a UTF-8 text file")
    prepare.add_argument("report_id")
    for field in ("sender", "recipient", "subject"):
        prepare.add_argument(f"--{field}", required=True)
    prepare.add_argument("--body-file", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "init":
            init_db(args.db)
            result = {"status": "initialized"}
        elif args.command == "list":
            result = list_reports(db_path=args.db)
        else:
            result = prepare_report(args.report_id, sender=args.sender, recipient=args.recipient,
                                    subject=args.subject, body=args.body_file.read_text(encoding="utf-8"),
                                    db_path=args.db)
    except (OSError, sqlite3.Error, ValueError):
        print("Offline operation failed; check inputs and private ledger access. No mail was sent.", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
