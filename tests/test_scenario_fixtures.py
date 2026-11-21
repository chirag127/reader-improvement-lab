"""Contracts for RT-12/29/36 inputs; optional evidence records host checks only."""

from __future__ import annotations

import argparse
from contextlib import closing, redirect_stderr, redirect_stdout
from datetime import datetime, timezone
import hashlib
from importlib.metadata import version
from io import BytesIO, StringIO
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import tempfile
import unittest

import pikepdf
import pymupdf
import pypdf
import pypdfium2 as pdfium
import reportlab


ROOT = Path(__file__).resolve().parents[1]
SCENARIOS = ROOT / "fixtures" / "scenarios"
MANIFEST = ROOT / "data" / "scenario-fixtures.json"
GENERATOR = ROOT / "scripts" / "generate_scenario_fixtures.py"
FILENAMES = {
    "rt12-literal-search.txt",
    "rt12-literal-search.pdf",
    "rt29-long-paragraph.txt",
    "rt36-healthy-control.pdf",
    "rt36-empty.pdf",
    "rt36-truncated.pdf",
    "rt36-invalid-header.pdf",
}
SEARCH_ROWS = {
    "S01": "a.b",
    "S02": "a+b",
    "S03": "[x]",
    "S04": "axb",
    "S05": "aaab",
    "S06": "x",
    "S07": "ab",
    "S08": "a-b",
}
PDF_ENGINES = ("pypdf", "PyMuPDF", "pikepdf", "pypdfium2")
HOST_OBSERVATIONS: dict[str, dict] = {}
TEMP_ROOT = (
    Path(os.environ["LOCALAPPDATA"]) / "Temp" / "opencode"
    if os.name == "nt" and "LOCALAPPDATA" in os.environ
    else Path(tempfile.gettempdir())
)


def digest(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def inspect_pdf(content: bytes, engine: str) -> dict:
    """Return observations; let unexpected exceptions fail the test."""
    if engine == "pypdf":
        with pypdf.PdfReader(BytesIO(content), strict=True) as document:
            return {
                "page_count": len(document.pages),
                "encrypted": document.is_encrypted,
                "text": document.pages[0].extract_text(),
            }
    if engine == "PyMuPDF":
        with pymupdf.open(stream=content, filetype="pdf") as document:
            pixels = document[0].get_pixmap(
                matrix=pymupdf.Matrix(0.5, 0.5),
                colorspace=pymupdf.csGRAY,
                alpha=False,
            )
            return {
                "page_count": len(document),
                "encrypted": bool(document.needs_pass),
                "text": document[0].get_text(),
                "render_grayscale_extrema": [min(pixels.samples), max(pixels.samples)],
                "render_size": [pixels.width, pixels.height],
            }
    if engine == "pikepdf":
        with pikepdf.open(BytesIO(content)) as document:
            return {
                "page_count": len(document.pages),
                "encrypted": document.is_encrypted,
                "syntax_issues": document.check_pdf_syntax(),
            }
    if engine == "pypdfium2":
        with pdfium.PdfDocument(content) as document:
            with closing(document[0]) as page, closing(page.get_textpage()) as textpage:
                with closing(page.render(scale=0.5, grayscale=True)) as bitmap:
                    image = bitmap.to_pil()
                    return {
                        "page_count": len(document),
                        "text": textpage.get_text_bounded(),
                        "render_grayscale_extrema": list(image.getextrema()),
                        "render_size": [image.width, image.height],
                    }
    raise ValueError(f"Unknown reference engine: {engine}")


def observe_pdf(path: Path, engine: str) -> dict:
    diagnostics = StringIO()
    rejection_errors = (
        pypdf.errors.PdfReadError,
        pymupdf.EmptyFileError,
        pymupdf.FileDataError,
        pikepdf.PdfError,
        pdfium.PdfiumError,
    )
    with redirect_stderr(diagnostics), redirect_stdout(diagnostics):
        try:
            result = {"load_status": "opened", **inspect_pdf(path.read_bytes(), engine)}
        except rejection_errors as error:
            result = {
                "load_status": "rejected",
                "exception_type": type(error).__name__,
                "exception_message": str(error),
            }
    result["diagnostics"] = diagnostics.getvalue()
    HOST_OBSERVATIONS.setdefault(path.name, {})[engine] = result
    return result


class ScenarioFixtureContracts(unittest.TestCase):
    def document(self, name: str) -> Path:
        path = SCENARIOS / name
        self.assertTrue(path.is_file(), f"Missing scenario input: {name}")
        return path

    def manifest(self) -> dict:
        self.assertTrue(MANIFEST.is_file(), "Scenario manifest has not been generated")
        return json.loads(MANIFEST.read_text(encoding="utf-8"))

    def test_manifest_identifies_seven_bounded_original_inputs(self):
        manifest = self.manifest()
        self.assertEqual(manifest["schema_version"], 1)
        self.assertEqual(manifest["origin"]["license"], "MIT")
        self.assertFalse(manifest["moon_reader_tested"])
        self.assertEqual(set(manifest["test_plan_ids"]), {"RT-12", "RT-29", "RT-36"})
        entries = manifest["fixtures"]
        self.assertEqual({Path(entry["path"]).name for entry in entries}, FILENAMES)
        self.assertEqual(len(entries), 7)
        total = 0
        for entry in entries:
            with self.subTest(fixture=entry["id"]):
                path = ROOT / entry["path"]
                self.assertTrue(path.resolve().is_relative_to(SCENARIOS.resolve()))
                content = path.read_bytes()
                self.assertEqual(digest(content), entry["sha256"])
                self.assertEqual(len(content), entry["size_bytes"])
                self.assertTrue(entry["expected"])
                self.assertTrue(entry["purpose"])
                total += len(content)
        self.assertEqual(total, manifest["total_document_bytes"])
        self.assertLess(total, 100_000)

    def test_search_text_has_exact_literals_and_distinct_negative_rows(self):
        content = self.document("rt12-literal-search.txt").read_bytes()
        self.assertFalse(content.startswith(b"\xef\xbb\xbf"))
        text = content.decode("utf-8", errors="strict")
        self.assertIn("café", text)
        self.assertNotIn("\r", text)
        for marker, token in SEARCH_ROWS.items():
            with self.subTest(row=marker):
                self.assertIn(f"{marker} | {token} |", text)
                self.assertEqual(text.count(marker), 1)
        for literal in ("a.b", "a+b", "[x]"):
            self.assertEqual(text.count(literal), 1)

    def test_search_pdf_preserves_literals_in_three_independent_text_extractors(self):
        path = self.document("rt12-literal-search.pdf")
        for engine in ("pypdf", "PyMuPDF", "pypdfium2"):
            with self.subTest(engine=engine):
                observed = observe_pdf(path, engine)
                self.assertEqual(observed["load_status"], "opened")
                self.assertEqual(observed["page_count"], 1)
                for marker, token in SEARCH_ROWS.items():
                    self.assertIn(f"{marker} | {token} |", observed["text"])
                for literal in ("a.b", "a+b", "[x]"):
                    self.assertEqual(observed["text"].count(literal), 1)

    def test_long_paragraph_has_single_begin_middle_and_far_suffix_markers(self):
        content = self.document("rt29-long-paragraph.txt").read_bytes()
        text = content.decode("utf-8", errors="strict")
        self.assertTrue(text.startswith("RT29-BEGIN-173 "))
        self.assertTrue(text.endswith(" RT29-SUFFIX-947"))
        for marker in ("RT29-BEGIN-173", "RT29-MIDDLE-509", "RT29-SUFFIX-947"):
            self.assertEqual(text.count(marker), 1)
        self.assertFalse(any(separator in text for separator in ("\n", "\r", "\u2028", "\u2029")))
        self.assertGreater(len(text), 12_000)
        self.assertLess(len(text), 20_000)
        self.assertGreater(text.index("RT29-MIDDLE-509"), 6_000)
        self.assertLess(abs(text.index("RT29-MIDDLE-509") - len(text) / 2), 100)
        self.assertGreater(text.index("RT29-SUFFIX-947"), 12_000)
        self.assertFalse(any(punctuation in text for punctuation in ".!?"))
        entry = next(item for item in self.manifest()["fixtures"] if item["id"] == "rt29-long-paragraph")
        expected = entry["expected"]
        self.assertEqual(expected["unicode_codepoints"], len(text))
        self.assertEqual(expected["utf16_code_units"], len(text.encode("utf-16-le")) // 2)
        self.assertIsNone(expected["actual_tts_engine_limit"])
        self.assertEqual(expected["actual_tts_engine_limit_status"], "unknown")
        for marker in expected["markers"]:
            self.assertEqual(text.find(marker["text"]), marker["codepoint_offset"])

    def test_malformed_inputs_are_exact_benign_bytes_derived_from_a_healthy_control(self):
        healthy = self.document("rt36-healthy-control.pdf").read_bytes()
        self.assertTrue(healthy.startswith(b"%PDF-"))
        self.assertTrue(healthy.rstrip().endswith(b"%%EOF"))
        self.assertEqual(self.document("rt36-empty.pdf").read_bytes(), b"")
        truncated = self.document("rt36-truncated.pdf").read_bytes()
        self.assertEqual(truncated, healthy[:64])
        self.assertEqual(len(truncated), 64)
        self.assertNotIn(b"%%EOF", truncated)
        self.assertEqual(
            self.document("rt36-invalid-header.pdf").read_bytes(),
            b"This is original plain text, not a PDF document.\nRT36-INVALID-HEADER-284\n",
        )

    def test_healthy_pdfs_have_one_nonblank_page_and_valid_qpdf_syntax(self):
        for filename, marker in (
            ("rt12-literal-search.pdf", "RT12-LITERAL-SEARCH-681"),
            ("rt36-healthy-control.pdf", "RT36-HEALTHY-621"),
        ):
            path = self.document(filename)
            for engine in PDF_ENGINES:
                with self.subTest(fixture=filename, engine=engine):
                    observed = observe_pdf(path, engine)
                    self.assertEqual(observed["load_status"], "opened")
                    self.assertEqual(observed["page_count"], 1)
                    if engine == "pikepdf":
                        self.assertEqual(observed["syntax_issues"], [])
                    else:
                        self.assertIn(marker, observed["text"])
                    if engine in ("PyMuPDF", "pypdfium2"):
                        low, high = observed["render_grayscale_extrema"]
                        self.assertLess(low, 200)
                        self.assertGreater(high, 240)

    def test_each_host_parser_rejects_malformed_input_then_opens_healthy_control(self):
        healthy = self.document("rt36-healthy-control.pdf")
        for filename in ("rt36-empty.pdf", "rt36-truncated.pdf", "rt36-invalid-header.pdf"):
            path = self.document(filename)
            for engine in PDF_ENGINES:
                with self.subTest(fixture=filename, engine=engine):
                    rejected = observe_pdf(path, engine)
                    self.assertEqual(rejected["load_status"], "rejected")
                    recovery = observe_pdf(healthy, engine)
                    self.assertEqual(recovery["load_status"], "opened")
                    self.assertEqual(recovery["page_count"], 1)
                    if "text" in recovery:
                        self.assertIn("RT36-HEALTHY-621", recovery["text"])
                    rejected["healthy_reopen"] = {
                        "path": "fixtures/scenarios/rt36-healthy-control.pdf",
                        "sha256": digest(healthy.read_bytes()),
                        "page_count": recovery["page_count"],
                        "load_status": recovery["load_status"],
                    }

    def test_regeneration_is_repeatable_and_preserves_other_corpus_files(self):
        self.assertTrue(GENERATOR.is_file(), "Scenario generator has not been implemented")
        original_paths = [ROOT / "fixtures" / "manifest.json"]
        original_paths.extend((ROOT / "fixtures" / "documents").glob("*"))
        before = {path: digest(path.read_bytes()) for path in original_paths}
        with tempfile.TemporaryDirectory(prefix="reader-scenarios-", dir=TEMP_ROOT) as temporary:
            destinations = [Path(temporary) / "first", Path(temporary) / "second"]
            for destination in destinations:
                sentinel = destination / "fixtures" / "documents" / "existing.pdf"
                sentinel.parent.mkdir(parents=True)
                sentinel.write_bytes(b"Existing corpus sentinel; must not be changed.")
                process = subprocess.run(
                    [sys.executable, "-X", "utf8", "-B", str(GENERATOR), "--output-root", str(destination)],
                    cwd=ROOT, capture_output=True, text=True, encoding="utf-8", timeout=60,
                    check=False,
                )
                self.assertEqual(process.returncode, 0, process.stdout + process.stderr)
                self.assertEqual(sentinel.read_bytes(), b"Existing corpus sentinel; must not be changed.")
            first, second = destinations
            relative_paths = [Path("data/scenario-fixtures.json")]
            relative_paths += [Path("fixtures/scenarios") / filename for filename in sorted(FILENAMES)]
            for relative in relative_paths:
                with self.subTest(path=str(relative)):
                    generated = (first / relative).read_bytes()
                    self.assertEqual(generated, (second / relative).read_bytes())
                    self.assertEqual(generated, (ROOT / relative).read_bytes())
        self.assertEqual(before, {path: digest(path.read_bytes()) for path in original_paths})


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence", type=Path, help="Write the observed test run and host readbacks as JSON")
    arguments = parser.parse_args()
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(ScenarioFixtureContracts)
    output = StringIO()
    result = unittest.TextTestRunner(stream=output, verbosity=2).run(suite)
    print(output.getvalue(), end="")
    if arguments.evidence:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8")) if MANIFEST.is_file() else None
        evidence = {
            "schema_version": 1,
            "evidence_type": "scenario-fixture-verification",
            "observed_at_utc": datetime.now(timezone.utc).isoformat(),
            "source_url": "https://github.com/chirag127/reader-improvement-lab",
            "status": "pass" if result.wasSuccessful() else "fail",
            "moon_reader_tested": False,
            "test_plan_ids": ["RT-12", "RT-29", "RT-36"],
            "command": "python -X utf8 -B tests/test_scenario_fixtures.py --evidence evidence/scenario-fixture-verification.json",
            "command_note": "Executed with the selected Python interpreter; local executable path is normalized to python.",
            "exit_code": 0 if result.wasSuccessful() else 1,
            "test_run": {"tests_run": result.testsRun, "failures": len(result.failures), "errors": len(result.errors), "skipped": len(result.skipped), "output": output.getvalue()},
            "environment": {
                "python": platform.python_version(), "system": platform.system(), "machine": platform.machine(),
                "imported_libraries": {name: version(name) for name in ("reportlab", "pypdf", "PyMuPDF", "pikepdf", "pypdfium2")},
                "MuPDF": ".".join(map(str, pymupdf.mupdf_version_tuple)),
                "PDFium": str(pdfium.PDFIUM_INFO), "qpdf": pikepdf.__libqpdf_version__,
                "packages_installed": [],
            },
            "artifact_hashes": {
                str(path.relative_to(ROOT)).replace("\\", "/"): digest(path.read_bytes())
                for path in (GENERATOR, MANIFEST, Path(__file__)) if path.is_file()
            },
            "input_hashes": [{"path": item["path"], "sha256": item["sha256"], "size_bytes": item["size_bytes"]} for item in manifest["fixtures"]] if manifest else [],
            "host_observations": HOST_OBSERVATIONS,
            "limitations": [
                "Host parser rejection and subsequent healthy opens are not application error handling or UI recovery tests.",
                "Search checks verify literal input identity/extraction, not application matching or regex handling.",
                "The actual Android TTS engine limit, segmentation, selected ranges and audible suffix remain unknown; no speech was run.",
                "36 dpi nonblank renders do not establish visual fidelity or accessibility.",
                "Malformed inputs are zero bytes, a 64-byte prefix of the new healthy PDF, and plain text with a .pdf extension; no exploit payloads.",
                "Byte repeatability covers the recorded generator and toolchain, not arbitrary platforms or dependency versions.",
                "Test runner duration in output is not a reader performance measurement.",
            ],
        }
        arguments.evidence.parent.mkdir(parents=True, exist_ok=True)
        arguments.evidence.write_text(json.dumps(evidence, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
