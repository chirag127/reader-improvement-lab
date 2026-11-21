"""Mutation-based checks of the public research validator, using original tiny records."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import runpy
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


VALIDATOR = Path(__file__).resolve().parents[1] / "scripts" / "validate_repository.py"
TEMP_ROOT = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
if os.name == "nt":
    TEMP_ROOT = TEMP_ROOT / "Temp" / "opencode"


class RepositoryValidation(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="reader-validator-", dir=TEMP_ROOT)
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.write("README.md", "# Research\n\n[Start](knowledge/index.md)\n")
        self.write("AGENTS.md", "# Instructions\n\n[Workspace](../../AGENTS.md)\n")
        self.write("CLAUDE.md", "@AGENTS.md\n")
        self.write("LICENSE", "Original synthetic validator test data.\n")
        note = "---\ntype: Research\ntitle: Test\ndescription: Test input\ntags: [test]\ntimestamp: 2026-11-21T00:00:00Z\n---\n\n# Test\n"
        for name in ("index", "bundle", "design", "methodology", "coverage", "reporting", "feature-matrix", "moon-improvements", "testing-plan"):
            self.write(f"knowledge/{name}.md", note)
        self.write("knowledge/index.md", note + "\n[Details](moon-improvements.md#test)\n")
        self.write_json("data/artifact.json", {"id": "supplied", "observed_at": "2026-11-21", "evidence_type": "static-observation", "sha256": "a" * 64, "provenance": "Unknown origin", "limitations": ["No official-build attribution"]})
        self.write_json("data/moon-baseline.json", {"observed_at": "2026-11-21", "features": [{"id": "MF-01", "title": "Reading", "evidence_type": "documented", "sources": ["https://example.org/reader"], "limitations": ["Not executed"]}]})
        self.write_json("evidence/static/observations.json", {"observed_at": "2026-11-21", "artifact_id": "supplied", "artifact_sha256": "a" * 64, "evidence_type": "static-observation", "findings": [{"id": "APK-ONE", "title": "A declaration", "observed": ["A declaration"], "unknown": ["Runtime"], "evidence": [{"private_evidence_ref": "private/withheld.txt", "sha256": "c" * 64}]}]})
        self.write_json("data/apk-structure.json", {"observed_at": "2026-11-21", "artifact_id": "supplied", "artifact_sha256": "a" * 64, "evidence_type": "static-observation"})
        for filename, identifier in (("alternatives-android", "reader-a"), ("alternatives-desktop-web", "reader-b"), ("commercial-alternatives", "reader-c")):
            self.write_json(f"data/{filename}.json", {"observed_at": "2026-11-21", "scope": "Synthetic", "alternatives": [{"id": identifier, "name": identifier, "repository": "https://example.org/source" if identifier != "reader-c" else None, "commit": "b" * 40 if identifier != "reader-c" else None, "license": "Test", "platforms": ["Test"], "formats": ["TXT"], "evidence_type": "documented", "features": [{"name": "Read", "evidence_type": "documented", "source_url": "https://example.org/reader"}], "sources": [{"url": "https://example.org/reader", "observed_at": "2026-11-21", "evidence_type": "documented"}], "limitations": ["Not executed"]}]})
        for filename, identifier in (("alternative-proposals-android", "reader-a"), ("alternative-proposals-desktop-web", "reader-b")):
            self.write_json(f"data/{filename}.json", {"observed_at": "2026-11-21", "proposals": [{"id": f"ALT-{identifier}", "title": "An extension", "application_id": identifier, "priority": "medium", "evidence_type": "proposal", "status": "draft", "basis": "Documented reading", "acceptance_criteria": ["Open the intended file"], "sources": ["https://example.org/reader"], "limitations": ["Not executed"]}]})
        self.write_json("data/moon-improvements.json", {"observed_at": "2026-11-21", "application_id": "moonreader", "proposals": [{"id": f"MOON-{i:03}", "title": f"Outcome {i}", "application_id": "moonreader", "category": "reading", "priority": "medium", "evidence_type": "proposal", "status": "draft", "relationship_to_baseline": "extension", "existing_capability": "Reading", "baseline_refs": ["MF-01"], "rationale": "A specific improvement", "requested_change": f"Refine workflow {i}", "acceptance_criteria": [f"Observe outcome {i}"], "sources": ["knowledge/moon-improvements.md#test"], "limitations": ["Not executed"]} for i in range(1, 51)]})
        content = b"Original test fixture\n"
        self.write("fixtures/documents/example.txt", content)
        self.write_json("fixtures/manifest.json", {"fixtures": [{"id": "example", "path": "documents/example.txt", "sha256": hashlib.sha256(content).hexdigest(), "size_bytes": len(content), "expected": {"text": "Original test fixture"}}]})
        self.write_json("data/scenario-fixtures.json", {"fixtures": []})

    def write(self, path, content):
        destination = self.root / path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(content.encode("utf-8") if isinstance(content, str) else content)

    def write_json(self, path, value):
        self.write(path, json.dumps(value, ensure_ascii=False) + "\n")

    def document(self, path):
        return json.loads((self.root / path).read_text(encoding="utf-8"))

    def validate(self, *arguments):
        self.assertTrue(VALIDATOR.is_file(), "Repository validator has not been implemented")
        result = subprocess.run([sys.executable, "-X", "utf8", "-B", str(VALIDATOR), "--root", str(self.root), *arguments], capture_output=True, text=True, encoding="utf-8", timeout=30)
        self.assertIn(result.returncode, (0, 1), result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(result.returncode, 1 if report["errors"] else 0)
        return report

    def assert_error(self, code):
        report = self.validate()
        self.assertEqual(report["status"], "fail")
        self.assertIn(code, {error["code"] for error in report["errors"]}, report)

    def test_complete_bounded_corpus_passes_without_claiming_application_tests(self):
        report = self.validate()
        self.assertEqual(report["errors"], [])
        self.assertFalse(report["application_tests_executed"])
        self.assertEqual(report["summary"]["moon_proposals"], 50)
        self.assertEqual(report["summary"]["alternatives"], 3)
        self.assertEqual(report["status"], "pending")
        self.assertIn("data/runtime-results.json", {item["path"] for item in report["pending"]})

    def test_fifty_proposal_boundary_and_duplicate_identity_are_enforced(self):
        path = "data/moon-improvements.json"
        original = self.document(path)
        short = self.document(path)
        short["proposals"].pop()
        self.write_json(path, short)
        self.assert_error("proposal-count")
        original["proposals"][-1]["id"] = original["proposals"][0]["id"]
        self.write_json(path, original)
        self.assert_error("duplicate-id")

    def test_repeated_requested_outcome_is_not_counted_as_distinct(self):
        path = "data/moon-improvements.json"
        value = self.document(path)
        value["proposals"][-1]["requested_change"] = "  REFINE   workflow 1  "
        self.write_json(path, value)
        self.assert_error("duplicate-outcome")

    def test_unknown_baseline_and_target_references_are_rejected(self):
        path = "data/moon-improvements.json"
        value = self.document(path)
        value["proposals"][0]["baseline_refs"] = ["MF-404"]
        value["proposals"][1]["application_id"] = "unlisted-reader"
        self.write_json(path, value)
        self.assert_error("unknown-baseline")
        self.assert_error("unknown-application")

    def test_missing_source_and_proposal_misclassified_as_pass_are_rejected(self):
        path = "data/moon-improvements.json"
        value = self.document(path)
        value["proposals"][0]["sources"] = []
        value["proposals"][1]["status"] = "pass"
        self.write_json(path, value)
        self.assert_error("missing-source")
        self.assert_error("proposal-status")

    def test_missing_file_anchor_and_reference_definition_are_rejected(self):
        self.write("README.md", "# Test\n\n[Missing](knowledge/absent.md) [Wrong](knowledge/index.md#absent) [Citation][not-defined]\n")
        report = self.validate()
        codes = {error["code"] for error in report["errors"]}
        self.assertTrue({"missing-link", "missing-anchor", "unresolved-reference"}.issubset(codes), report)

    def test_heading_suffixes_explicit_anchors_and_code_examples_are_handled(self):
        self.write("README.md", '# Title\n## Repeat\n## Repeat\n<a id="chosen"></a>\n[Second](#repeat-1) [Named](#chosen)\n```text\n[example](not-a-real-file.md)\n```\n')
        self.assertEqual(self.validate()["errors"], [])

    def test_duplicate_reference_definitions_and_invalid_line_anchors_fail(self):
        self.write("README.md", "# Test\n\n[Source][REF]\n[REF]: https://example.org/a\n[ref]: https://example.org/b\n\n[Record](data/artifact.json#L999)\n")
        report = self.validate()
        codes = {error["code"] for error in report["errors"]}
        self.assertTrue({"duplicate-reference", "invalid-line-anchor"}.issubset(codes), report)

    def test_changed_fixture_bytes_and_traversal_are_rejected(self):
        self.write("fixtures/documents/example.txt", b"Different bytes\n")
        self.assert_error("fixture-hash")
        value = self.document("fixtures/manifest.json")
        value["fixtures"][0]["path"] = "../../outside.txt"
        self.write_json("fixtures/manifest.json", value)
        self.assert_error("fixture-path")

    def test_proprietary_binary_is_rejected_even_in_an_evidence_folder(self):
        self.write("evidence/sample.apk", b"Not a redistributable fixture")
        self.assert_error("forbidden-file")

    def test_ignored_local_evidence_is_excluded_but_public_credentials_fail(self):
        self.write(".local/private.apk", b"Local input")
        self.assertEqual(self.validate()["errors"], [])
        self.write("evidence/unsafe.txt", "-----BEGIN " + "PRIVATE KEY-----\n")
        self.assert_error("sensitive-content")

    def test_duplicate_json_members_and_mismatched_artifact_identity_fail(self):
        self.write("data/invalid.json", '{"id":"one","id":"two"}\n')
        self.assert_error("invalid-json")
        value = self.document("data/apk-structure.json")
        value["artifact_sha256"] = "c" * 64
        self.write_json("data/apk-structure.json", value)
        self.assert_error("artifact-identity")

    def test_latest_review_hash_is_bound_to_current_inputs(self):
        self.write_json("evidence/reviews/current.json", {"id": "review", "inputs": [{"path": "data/moon-improvements.json", "sha256": "d" * 64}]})
        self.assert_error("evidence-hash")

    def test_invalid_and_missing_proposal_ids_fail(self):
        path = "data/moon-improvements.json"
        value = self.document(path)
        value["proposals"][0]["id"] = "not-a-moon-id"
        del value["proposals"][1]["id"]
        self.write_json(path, value)
        report = self.validate("--json")
        self.assertTrue({"invalid-id", "required-field"}.issubset({error["code"] for error in report["errors"]}), report)

    def test_unknown_evidence_and_invalid_dates_are_rejected(self):
        path = "data/moon-baseline.json"
        value = self.document(path)
        value["features"][0]["evidence_type"] = "verified-by-assumption"
        value["observed_at"] = "2026-11-21garbage"
        self.write_json(path, value)
        report = self.validate()
        self.assertTrue({"evidence-type", "observation-date"}.issubset({error["code"] for error in report["errors"]}), report)

    def test_wrong_field_types_produce_errors_instead_of_a_traceback(self):
        path = "data/moon-improvements.json"
        value = self.document(path)
        value["proposals"][0].update(application_id={}, priority=[], evidence_type=[], status={}, baseline_refs=[{}])
        self.write_json(path, value)
        self.assert_error("required-field")

    def test_json_report_links_and_finding_references_are_checked(self):
        path = "data/moon-baseline.json"
        value = self.document(path)
        value["report_path"] = "knowledge/index.md#absent"
        value["related_evidence"] = [{"finding_ids": ["APK-NOT-DECLARED"], "evidence_path": "evidence/missing.json"}]
        self.write_json(path, value)
        report = self.validate()
        codes = {error["code"] for error in report["errors"]}
        self.assertTrue({"missing-anchor", "missing-link", "unknown-reference"}.issubset(codes), report)

    def test_sources_are_root_relative_and_cannot_escape_the_public_corpus(self):
        path = "data/moon-improvements.json"
        value = self.document(path)
        value["proposals"][0]["sources"] = ["../knowledge/index.md"]
        value["proposals"][1]["sources"] = [".local/private-notes.txt"]
        self.write(".local/private-notes.txt", "Not a public source")
        self.write_json(path, value)
        self.assert_error("link-path")

    def test_only_known_workspace_policy_links_are_external_exceptions(self):
        self.write("AGENTS.md", "# Instructions\n[Workspace](../../AGENTS.md)\n[Other](../../unrelated.txt)\n")
        self.assert_error("link-path")

    def test_host_evidence_cannot_claim_an_application_execution(self):
        self.write_json("evidence/host.json", {"observed_at": "2026-11-21", "evidence_type": "host-unit-test", "application_executed": True, "limitations": ["Synthetic host test"]})
        self.assert_error("evidence-boundary")

    def test_historical_static_hashes_and_withheld_receipts_remain_historical(self):
        target = "data/apk-structure.json"
        old = {"observed_at": "2026-11-21T01:00:00Z", "evidence_type": "static-observation", "checked_public_files": [{"file": target, "sha256": "d" * 64}]}
        current = {"observed_at": "2026-11-21T02:00:00Z", "evidence_type": "static-observation", "checked_public_files": [{"file": target, "sha256": hashlib.sha256((self.root / target).read_bytes()).hexdigest()}]}
        self.write_json("evidence/static/verification.json", old)
        self.write_json("evidence/static/bounded-followup-verification.json", current)
        self.assertEqual(self.validate()["errors"], [])
        self.write_json(target, {**self.document(target), "new_observation": True})
        self.assert_error("evidence-hash")

    def test_zero_byte_fixture_is_valid_but_fixture_ids_are_global(self):
        self.write("fixtures/scenarios/empty.pdf", b"")
        entry = {"id": "empty", "path": "fixtures/scenarios/empty.pdf", "sha256": hashlib.sha256(b"").hexdigest(), "size_bytes": 0, "expected": {"application_result": "not-run"}}
        self.write_json("data/scenario-fixtures.json", {"fixtures": [entry]})
        self.assertEqual(self.validate()["errors"], [])
        entry["id"] = "example"
        self.write_json("data/scenario-fixtures.json", {"fixtures": [entry]})
        self.assert_error("duplicate-id")

    def test_contributions_have_independent_ids_targets_and_published_commits(self):
        contribution = {"id": "reader-fix", "app_id": "reader-a", "observed_at": "2026-11-21", "evidence_type": "runtime-observation", "evidence_scope": "Host module checks only", "upstream_url": "https://example.org/source", "upstream_revision": "b" * 40, "commit": "c" * 40, "summary": "Focused change", "status": "implemented-tested", "source_urls": ["https://example.org/source"], "limitations": ["No app test"], "verification": [{"name": "host", "exit_code": 0, "evidence_path": "evidence/host.txt"}], "publication": {"status": "pushed-to-fork", "verified_commit": "c" * 40}}
        self.write("evidence/host.txt", "Synthetic test setup; not real contribution evidence.\n")
        self.write_json("data/contributions/one.json", contribution)
        report = self.validate()
        self.assertEqual(report["errors"], [])
        self.assertEqual(report["summary"]["contributions"], 1)
        self.assertFalse(report["application_tests_executed"])
        contribution["app_id"] = "missing-reader"
        contribution["publication"]["verified_commit"] = "d" * 40
        self.write_json("data/contributions/two.json", contribution)
        report = self.validate()
        self.assertTrue({"duplicate-id", "unknown-application", "source-revision"}.issubset({error["code"] for error in report["errors"]}), report)

    def test_invalid_hash_and_commit_syntax_are_rejected_even_for_private_receipts(self):
        value = self.document("evidence/static/observations.json")
        value["findings"][0]["evidence"][0]["sha256"] = "not-a-digest"
        self.write_json("evidence/static/observations.json", value)
        value = self.document("data/alternatives-desktop-web.json")
        value["alternatives"][0]["commit"] = "main"
        self.write_json("data/alternatives-desktop-web.json", value)
        report = self.validate()
        self.assertTrue({"hash-format", "source-revision"}.issubset({error["code"] for error in report["errors"]}), report)

    def test_duplicate_html_ids_fail_and_setext_headings_resolve(self):
        self.write("README.md", '# Title\nCafé — example\n----------------\n[Heading](#café--example)\n<a id="chosen"></a><span id="chosen"></span>\n')
        report = self.validate()
        self.assertIn("duplicate-anchor", {error["code"] for error in report["errors"]})
        self.assertNotIn("missing-anchor", {error["code"] for error in report["errors"]})

    def test_public_raw_configuration_and_bulk_dump_paths_are_rejected(self):
        self.write("evidence/local.properties", "sdk.dir=not-public\n")
        self.write("evidence/decompiled/Example.java", "class Example {}\n")
        self.assert_error("forbidden-file")

    def test_missing_fixture_path_is_a_structured_failure(self):
        value = self.document("fixtures/manifest.json")
        del value["fixtures"][0]["path"]
        self.write_json("fixtures/manifest.json", value)
        self.assert_error("required-field")

    def test_malformed_current_receipts_cannot_silently_skip_checks(self):
        mutations = [
            ("evidence/fixture-verification.json", {"artifacts": []}),
            ("evidence/reviews/current.json", {"inputs": [None]}),
            ("evidence/reviews/current.json", {"inputs": [{"path": 42, "sha256": "bad"}]}),
            ("evidence/reviews/current.json", {"inputs": []}),
            ("evidence/static/bounded-followup-verification.json", {}),
            ("evidence/static/bounded-followup-verification.json", {"checked_public_files": [None]}),
        ]
        for path, value in mutations:
            with self.subTest(path=path, value=value):
                self.write_json(path, value)
                report = self.validate()
                self.assertEqual(report["status"], "fail", report)
                self.assertTrue(any(error["path"] == path for error in report["errors"]), report)
                (self.root / path).unlink()

    def test_output_preserves_public_inputs_on_valid_and_invalid_corpora(self):
        source = self.root / "README.md"
        original = source.read_bytes()
        for corrupt in (False, True):
            with self.subTest(invalid_corpus=corrupt):
                if corrupt:
                    self.write("data/broken.json", "{not-json}")
                report = self.validate("--output", str(source))
                self.assertIn("output-path", {error["code"] for error in report["errors"]})
                self.assertEqual(source.read_bytes(), original)

    def test_local_and_external_receipts_match_stdout_and_replace_atomically(self):
        with tempfile.TemporaryDirectory(prefix="reader-receipt-", dir=TEMP_ROOT) as directory:
            for output in (self.root / ".local" / "result.json", Path(directory) / "result.json"):
                with self.subTest(output=output.name):
                    output.parent.mkdir(parents=True, exist_ok=True)
                    output.write_text("Previous receipt\n", encoding="utf-8")
                    report = self.validate("--output", str(output))
                    self.assertEqual(report["errors"], [])
                    self.assertEqual(json.loads(output.read_text(encoding="utf-8")), report)
                    self.assertEqual(list(output.parent.glob(".reader-validation-*.tmp")), [])

    def test_receipt_hardlink_cannot_overwrite_an_examined_input(self):
        source = self.root / "README.md"
        original = source.read_bytes()
        with tempfile.TemporaryDirectory(prefix="reader-hardlink-", dir=TEMP_ROOT) as directory:
            output = Path(directory) / "receipt.json"
            os.link(source, output)
            report = self.validate("--output", str(output))
            self.assertIn("output-path", {error["code"] for error in report["errors"]})
            self.assertEqual(source.read_bytes(), original)
            self.assertEqual(output.read_bytes(), original)

    @unittest.skipUnless(os.name == "nt", "NTFS junction boundary")
    def test_windows_junction_is_neither_scanned_nor_used_for_output(self):
        with tempfile.TemporaryDirectory(prefix="reader-junction-", dir=TEMP_ROOT) as directory:
            outside = Path(directory)
            canary = outside / "private-canary.txt"
            canary.write_text("-----BEGIN " + "PRIVATE KEY-----\n", encoding="utf-8")
            junction = self.root / "linked"
            result = subprocess.run(["cmd", "/d", "/c", "mklink", "/J", str(junction), str(outside)], capture_output=True, text=True, timeout=15)
            self.assertEqual(result.returncode, 0, result.stderr)
            try:
                report = self.validate("--output", str(junction / "receipt.json"))
                codes = {error["code"] for error in report["errors"]}
                self.assertTrue({"public-symlink", "output-path"}.issubset(codes), report)
                self.assertNotIn("sensitive-content", codes, "The outside canary must never be read")
                self.assertFalse((outside / "receipt.json").exists())
                self.assertTrue(canary.is_file())
            finally:
                junction.rmdir()

    def runtime_ledger(self):
        """A complete record of unexecuted cases; no fabricated application passes."""
        path = "data/runtime-results.json"
        plan = self.root / "knowledge/testing-plan.md"
        fixture = self.document("fixtures/manifest.json")["fixtures"][0]
        self.write_json("evidence/runtime/manifest.json", {"files": [{"path": "fixtures/documents/example.txt", "sha256": fixture["sha256"], "size_bytes": fixture["size_bytes"]}], "file_count": 1})
        self.write_json("evidence/runtime/cleanup.json", {"status": "not-started"})
        value = {
            "id": "synthetic-runtime-ledger", "observed_at": "2026-11-21", "evidence_type": "runtime-observation",
            "artifact_id": "supplied", "artifact_sha256": "a" * 64, "test_plan": "knowledge/testing-plan.md",
            "test_plan_sha256_at_curation": hashlib.sha256(plan.read_bytes()).hexdigest(),
            "evidence_manifest": "evidence/runtime/manifest.json", "report_path": "knowledge/coverage.md",
            "environment": {"id": "synthetic-unexecuted"}, "limitations": ["Validator fixture only; no app was launched"],
            "cleanup": {"status": "not-started", "receipt": "evidence/runtime/cleanup.json"},
            "cases": [{"id": f"RT-{i:02}", "title": f"Unexecuted workflow {i}", "status": "not-run", "evidence_type": "unknown", "artifact_sha256": "a" * 64, "environment_id": "synthetic-unexecuted", "observed_at": "2026-11-21", "source_url": "https://example.org/test-plan", "expected": "Complete the real workflow", "actual": "Not run", "steps": [], "inputs": [], "evidence": [], "subchecks": [], "limitations": ["Not run"]} for i in range(1, 37)],
            "summary": {"pass": 0, "partial": 0, "fail": 0, "blocked": 0, "not-run": 36, "total": 36, "executed_at_least_in_part": 0},
        }
        self.write_json(path, value)
        return value

    def test_complete_runtime_ledger_is_record_validation_not_an_app_pass(self):
        self.runtime_ledger()
        report = self.validate()
        self.assertEqual(report["errors"], [])
        self.assertEqual(report["pending"], [])
        self.assertEqual(report["status"], "pass")
        self.assertEqual(report["summary"]["runtime_not-run"], 36)
        self.assertFalse(report["application_tests_executed"])

    def test_runtime_counts_and_missing_case_are_rejected(self):
        value = self.runtime_ledger()
        value["cases"].pop()
        self.write_json("data/runtime-results.json", value)
        report = self.validate()
        self.assertTrue({"runtime-count", "runtime-coverage"}.issubset({error["code"] for error in report["errors"]}), report)

    def test_runtime_pass_requires_consistent_subchecks_and_retained_evidence(self):
        value = self.runtime_ledger()
        case = value["cases"][0]
        case.update(status="pass", evidence_type="runtime-observation", steps=[{"number": 1, "action": "Synthetic record mutation"}], evidence=["evidence/runtime/missing.txt"], subchecks=[{"id": "unfinished", "status": "not-run", "actual": "Unexecuted", "evidence": []}])
        value["summary"].update({"pass": 1, "not-run": 35, "executed_at_least_in_part": 1})
        self.write_json("data/runtime-results.json", value)
        report = self.validate()
        self.assertTrue({"runtime-status", "missing-link"}.issubset({error["code"] for error in report["errors"]}), report)

    def test_runtime_fixture_and_auxiliary_output_hashes_are_bound(self):
        value = self.runtime_ledger()
        value["cases"][0]["inputs"] = [{"id": "example", "path": "fixtures/documents/example.txt", "sha256": "b" * 64}]
        value["auxiliary_observations"] = [{"outputs": [{"path": "fixtures/documents/example.txt", "sha256": "c" * 64}]}]
        self.write_json("data/runtime-results.json", value)
        report = self.validate()
        self.assertTrue({"fixture-identity", "evidence-hash"}.issubset({error["code"] for error in report["errors"]}), report)

    def test_runtime_changed_manifest_file_fails_without_replaying_app_steps(self):
        self.runtime_ledger()
        self.write("fixtures/documents/example.txt", "Altered bytes\n")
        self.assert_error("evidence-hash")

    def test_runtime_citations_require_manifest_membership_before_and_after_mutation(self):
        reference = "evidence/runtime/step.txt"
        for location in ("case", "subcheck", "auxiliary"):
            with self.subTest(location=location):
                value = self.runtime_ledger()
                case = value["cases"][0]
                case.update(status="pass", evidence_type="runtime-observation", steps=[{"number": 1, "action": "Synthetic record mutation"}], evidence=["fixtures/documents/example.txt"], subchecks=[{"id": "synthetic", "status": "pass", "actual": "Synthetic record only", "evidence": []}])
                value["summary"].update({"pass": 1, "not-run": 35, "executed_at_least_in_part": 1})
                if location == "case":
                    case["evidence"].append(reference)
                elif location == "subcheck":
                    case["subchecks"][0]["evidence"] = [reference]
                else:
                    value["auxiliary_observations"] = [{"evidence": [reference]}]
                self.write_json("data/runtime-results.json", value)
                for content in (b"Original synthetic evidence\n", b"Changed synthetic evidence\n"):
                    self.write(reference, content)
                    self.assert_error("unbound-evidence")
                manifest = self.document("evidence/runtime/manifest.json")
                manifest["files"].append({"path": reference, "sha256": hashlib.sha256(content).hexdigest(), "size_bytes": len(content)})
                manifest["file_count"] += 1
                self.write_json("evidence/runtime/manifest.json", manifest)
                self.assertEqual(self.validate()["errors"], [])
                self.write(reference, b"Changed after digest binding\n")
                self.assert_error("evidence-hash")

    def test_runtime_evidence_aliases_resolve_to_the_same_hashed_file(self):
        value = self.runtime_ledger()
        value["auxiliary_observations"] = [{"evidence": ["fixtures/documents/%65xample.txt#L1"]}]
        self.write_json("data/runtime-results.json", value)
        self.assertEqual(self.validate()["errors"], [])
        manifest = self.document("evidence/runtime/manifest.json")
        manifest["files"].append({**manifest["files"][0], "path": "fixtures/documents/../documents/example.txt"})
        manifest["file_count"] += 1
        self.write_json("evidence/runtime/manifest.json", manifest)
        self.assert_error("duplicate-reference")

    def test_external_source_url_is_not_a_retained_runtime_evidence_file(self):
        value = self.runtime_ledger()
        value["auxiliary_observations"] = [{"source_url": "https://example.org/source", "evidence": ["https://example.org/step.txt"]}]
        self.write_json("data/runtime-results.json", value)
        self.assert_error("unbound-evidence")

    def test_required_provenance_fields_cannot_be_removed(self):
        artifact = self.document("data/artifact.json")
        del artifact["observed_at"]
        self.write_json("data/artifact.json", artifact)
        baseline = self.document("data/moon-baseline.json")
        del baseline["features"][0]["limitations"]
        self.write_json("data/moon-baseline.json", baseline)
        inventory = self.document("data/alternatives-android.json")
        del inventory["alternatives"][0]["platforms"]
        del inventory["alternatives"][0]["sources"][0]["evidence_type"]
        self.write_json("data/alternatives-android.json", inventory)
        report = self.validate()
        self.assertTrue({"observation-date", "record-shape", "required-field"}.issubset({error["code"] for error in report["errors"]}), report)

    def test_markdown_emphasis_and_reference_headings_use_rendered_text(self):
        self.write("README.md", '# Title\n## **Strong** _em_ and `code_name`\n## [Named][ref]\n[ref]: https://example.org\n[One](#strong-em-and-code_name) [Two](#named)\n<!-- [not rendered](absent.md) -->\n')
        self.assertEqual(self.validate()["errors"], [])

    def test_git_publication_candidates_include_tracked_private_and_untracked_files(self):
        self.write(".local/tracked.apk", b"Tracked private input")
        self.write(".local/ignored.apk", b"Ignored local input")
        self.write("evidence/untracked.dex", b"Unignored publication candidate")
        self.write("evidence/ignored.json", "{invalid, but excluded by Git}")
        self.write("README.md", "# Test\n[Ignored](evidence/ignored.json)\n")
        candidates = [path.relative_to(self.root).as_posix() for path in self.root.rglob("*") if path.is_file()]
        candidates.remove(".local/ignored.apk")
        candidates.remove("evidence/ignored.json")
        (self.root / ".git").mkdir()
        namespace = runpy.run_path(str(VALIDATOR))
        result = subprocess.CompletedProcess(["git"], 0, ("\0".join(candidates) + "\0").encode("utf-8"), b"")
        with patch.object(namespace["subprocess"], "run", return_value=result):
            report = namespace["Validator"](self.root).run()
        forbidden = {error["path"] for error in report["errors"] if error["code"] == "forbidden-file"}
        self.assertTrue({".local/tracked.apk", "evidence/untracked.dex"}.issubset(forbidden), report)
        self.assertNotIn(".local/ignored.apk", forbidden)
        self.assertNotIn("invalid-json", {error["code"] for error in report["errors"]})
        self.assertIn("unpublished-link", {error["code"] for error in report["errors"]})


if __name__ == "__main__":
    unittest.main()
