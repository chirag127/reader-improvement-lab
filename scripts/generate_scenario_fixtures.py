"""Generate original, byte-repeatable RT-12, RT-29, and RT-36 scenario inputs."""

from __future__ import annotations

import argparse
import hashlib
from importlib.metadata import version
from io import BytesIO
import json
from pathlib import Path
import platform

from reportlab.pdfgen.canvas import Canvas


ROOT = Path(__file__).resolve().parents[1]
SEARCH_ROWS = [
    ("S01", "a.b", "literal dot"),
    ("S02", "a+b", "literal plus"),
    ("S03", "[x]", "literal brackets"),
    ("S04", "axb", "negative control one"),
    ("S05", "aaab", "negative control two"),
    ("S06", "x", "negative control three"),
    ("S07", "ab", "negative control four"),
    ("S08", "a-b", "negative control five"),
]
BEGIN_MARKER = "RT29-BEGIN-173"
MIDDLE_MARKER = "RT29-MIDDLE-509"
SUFFIX_MARKER = "RT29-SUFFIX-947"


def digest(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def healthy_pdf(title: str, lines: list[str]) -> bytes:
    buffer = BytesIO()
    canvas = Canvas(buffer, pagesize=(612, 792), invariant=1, pageCompression=1)
    canvas.setTitle(title)
    canvas.setAuthor("Reader Improvement Lab")
    canvas.setCreator("scripts/generate_scenario_fixtures.py")
    canvas.setSubject("Original MIT-licensed synthetic input; no application result")
    canvas.setFont("Helvetica-Bold", 16)
    canvas.drawString(36, 744, title)
    canvas.setFont("Helvetica", 12)
    for index, line in enumerate(lines):
        canvas.drawString(36, 704 - index * 28, line)
    canvas.showPage()
    canvas.save()
    return buffer.getvalue()


def long_paragraph() -> str:
    phrase = "a paper boat crosses the quiet harbor while the keeper counts the waves"
    half = " ".join([phrase] * 100)
    return f"{BEGIN_MARKER} {half} {MIDDLE_MARKER} {half} {SUFFIX_MARKER}"


def generate(output_root: Path) -> dict:
    search_lines = ["Original UTF-8 café note", "Each labeled row is separate"]
    search_lines.extend(f"{row} | {token} | {label}" for row, token, label in SEARCH_ROWS)
    search_text = "\n".join(["RT12-LITERAL-SEARCH-681", *search_lines]) + "\n"
    search_pdf = healthy_pdf("RT12-LITERAL-SEARCH-681", search_lines)
    paragraph = long_paragraph()
    control = healthy_pdf(
        "RT36-HEALTHY-621",
        [
            "A paper kite rests beside an original clockwork harbor.",
            "Open this healthy page before and after each malformed input.",
            "Recovery anchor: RT36-RECOVERY-358",
            "This page contains ordinary selectable text and no actions.",
        ],
    )
    search_expectations = {
        "rows": [{"id": row, "token": token} for row, token, _ in SEARCH_ROWS],
        "literal_queries": [
            {
                "query": token,
                "occurrences": 1,
                "positive_row_ids": [row],
                "negative_row_ids": [other for other, _, _ in SEARCH_ROWS if other != row],
            }
            for row, token, _ in SEARCH_ROWS[:3]
        ],
        "title_marker": "RT12-LITERAL-SEARCH-681",
        "application_search_mode": "Record at runtime; literal-mode expectations only",
    }
    recipes = [
        (
            "rt12-literal-search-text", "rt12-literal-search.txt", "RT-12",
            "text/plain; charset=utf-8", search_text.encode("utf-8"),
            "Literal search metacharacters with distinct labeled negative controls.",
            {"encoding": "utf-8", "bom": False, "line_endings": "LF", **search_expectations},
        ),
        (
            "rt12-literal-search-pdf", "rt12-literal-search.pdf", "RT-12",
            "application/pdf", search_pdf,
            "A selectable one-page PDF with the same literal search rows.",
            {"page_count": 1, "text_layer": True, "encrypted": False, **search_expectations},
        ),
        (
            "rt29-long-paragraph", "rt29-long-paragraph.txt", "RT-29",
            "text/plain; charset=utf-8", paragraph.encode("utf-8"),
            "One paragraph with far-apart speech markers for runtime segmentation checks.",
            {
                "encoding": "utf-8", "ascii_only": True, "paragraph_count": 1,
                "newline_count": 0, "sentence_terminators": [],
                "unicode_codepoints": len(paragraph),
                "utf16_code_units": len(paragraph.encode("utf-16-le")) // 2,
                "markers": [
                    {"text": marker, "occurrences": 1, "codepoint_offset": paragraph.index(marker)}
                    for marker in (BEGIN_MARKER, MIDDLE_MARKER, SUFFIX_MARKER)
                ],
                "sizing_reference_utf16_code_units": 4000,
                "sizing_reference_scope": "Synthetic sizing reference only, not a measured platform or engine limit",
                "actual_tts_engine_limit": None,
                "actual_tts_engine_limit_status": "unknown",
                "runtime_requirement": "Measure the selected platform/engine limit and utterance segmentation before making truncation claims",
            },
        ),
        (
            "rt36-healthy-control", "rt36-healthy-control.pdf", "RT-36",
            "application/pdf", control,
            "Healthy control for opening before and after each malformed input.",
            {"page_count": 1, "text_layer": True, "encrypted": False,
             "text_markers": ["RT36-HEALTHY-621", "RT36-RECOVERY-358"]},
        ),
        (
            "rt36-empty", "rt36-empty.pdf", "RT-36", "application/pdf", b"",
            "Benign zero-byte input for graceful rejection and subsequent healthy opening.",
            {"byte_length": 0, "construction": "Empty byte string",
             "intended_host_result": "rejected", "application_result": "not-run"},
        ),
        (
            "rt36-truncated", "rt36-truncated.pdf", "RT-36", "application/pdf", control[:64],
            "Benign header-only prefix of the new healthy PDF, without a complete page or trailer.",
            {"byte_length": 64, "construction": "First 64 bytes of rt36-healthy-control.pdf",
             "source_path": "fixtures/scenarios/rt36-healthy-control.pdf",
             "source_sha256": digest(control), "contains_eof_marker": False,
             "intended_host_result": "rejected", "application_result": "not-run"},
        ),
        (
            "rt36-invalid-header", "rt36-invalid-header.pdf", "RT-36", "application/pdf",
            b"This is original plain text, not a PDF document.\nRT36-INVALID-HEADER-284\n",
            "Benign original plain text carrying a .pdf extension, without any PDF structure.",
            {"construction": "Original plain text with LF endings and a .pdf extension",
             "actual_content_type": "text/plain; charset=utf-8", "pdf_header_present": False,
             "intended_host_result": "rejected", "application_result": "not-run"},
        ),
    ]
    destination = output_root / "fixtures" / "scenarios"
    destination.mkdir(parents=True, exist_ok=True)
    entries = []
    for identifier, filename, test_id, media_type, content, purpose, expected in recipes:
        (destination / filename).write_bytes(content)
        entries.append({
            "id": identifier, "test_plan_id": test_id,
            "path": f"fixtures/scenarios/{filename}", "media_type": media_type,
            "sha256": digest(content), "size_bytes": len(content),
            "purpose": purpose, "expected": expected,
        })
    manifest = {
        "schema_version": 1,
        "evidence_type": "synthetic-scenario-inputs",
        "moon_reader_tested": False,
        "test_plan_ids": ["RT-12", "RT-29", "RT-36"],
        "test_plan_path": "knowledge/testing-plan.md",
        "origin": {
            "kind": "original-synthetic", "license": "MIT",
            "copyright": "Copyright (c) 2026 Chirag Singhal",
            "source": "scripts/generate_scenario_fixtures.py",
            "source_url": "https://github.com/chirag127/reader-improvement-lab",
            "note": "Original prose and standard-font PDFs; no proprietary samples, personal documents, or exploit payloads",
        },
        "generator_sha256": digest(Path(__file__).read_bytes()),
        "generator_versions": {"python": platform.python_version(), "reportlab": version("reportlab")},
        "reproducibility": {
            "recipe_revision": 1,
            "metadata_epoch": "2000-01-01T00:00:00Z",
            "method": "Fixed text, UTF-8 with LF endings, ReportLab invariant metadata and deterministic PDF IDs",
            "boundary": "Same generator and recorded toolchain; cross-platform byte identity is not claimed",
        },
        "limitations": [
            "The fixture tooling does not run Moon+ Reader or any Android application.",
            "Literal data and extraction checks do not establish application search mode or matching behavior.",
            "Actual TTS engine input limit and segmentation are unknown; no speech is submitted.",
            "Malformed parser rejection does not establish application crash handling or UI recovery.",
            "Only seven named scenario files and this manifest are generated; the original corpus is separate.",
        ],
        "total_document_bytes": sum(entry["size_bytes"] for entry in entries),
        "fixtures": entries,
    }
    manifest_path = output_root / "data" / "scenario-fixtures.json"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8", newline="\n",
    )
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", type=Path, default=ROOT)
    arguments = parser.parse_args()
    manifest = generate(arguments.output_root)
    print(json.dumps({
        "fixtures_generated": len(manifest["fixtures"]),
        "test_plan_ids": manifest["test_plan_ids"],
        "total_document_bytes": manifest["total_document_bytes"],
        "generator_versions": manifest["generator_versions"],
        "moon_reader_tested": False,
    }, indent=2))


if __name__ == "__main__":
    main()
