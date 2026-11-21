"""Integration contracts for original reader fixtures, not reader-app tests."""

from __future__ import annotations

from contextlib import closing
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
import zipfile

import pikepdf
import pymupdf
import pypdf
import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_raw


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "fixtures"
GENERATOR = ROOT / "scripts" / "generate_fixtures.py"
CHECKER = ROOT / "scripts" / "check_fixtures.py"
PDF_NAMES = {
    "plain-text",
    "two-columns",
    "long-document",
    "mixed-geometry",
    "navigation",
    "annotations",
    "acroform",
    "password-protected",
    "scanned-image-only",
    "unicode",
}
TEMP_ROOT = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
if os.name == "nt":
    TEMP_ROOT = TEMP_ROOT / "Temp" / "opencode"


def run_script(script: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-B", str(script), *arguments],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env={**os.environ, "PYTHONUTF8": "1"},
        timeout=120,
        check=False,
    )


def pdfium_text(path: Path, page_index: int = 0, password: str | None = None) -> str:
    with pdfium.PdfDocument(path, password=password) as document:
        with closing(document[page_index]) as page, closing(page.get_textpage()) as textpage:
            return textpage.get_text_bounded()


class FixtureContracts(unittest.TestCase):
    def document(self, name: str, extension: str = "pdf") -> Path:
        path = FIXTURES / "documents" / f"{name}.{extension}"
        self.assertTrue(path.is_file(), f"Missing synthetic fixture: {path.name}")
        return path

    def manifest(self) -> dict:
        path = FIXTURES / "manifest.json"
        self.assertTrue(path.is_file(), "The corpus needs an expected-properties manifest")
        return json.loads(path.read_text(encoding="utf-8"))

    def test_manifest_covers_every_artifact_with_hash_size_and_expectations(self):
        manifest = self.manifest()
        self.assertEqual(manifest["schema_version"], 1)
        self.assertEqual(manifest["origin"]["license"], "MIT")
        entries = manifest["fixtures"]
        self.assertEqual({entry["id"] for entry in entries}, PDF_NAMES | {"tiny-original"})
        self.assertEqual(len(entries), 11)
        total_bytes = 0
        for entry in entries:
            with self.subTest(fixture=entry["id"]):
                path = FIXTURES / entry["path"]
                self.assertTrue(path.is_file())
                self.assertTrue(path.resolve().is_relative_to(FIXTURES.resolve()))
                content = path.read_bytes()
                self.assertEqual(hashlib.sha256(content).hexdigest(), entry["sha256"])
                self.assertEqual(len(content), entry["size_bytes"])
                self.assertTrue(entry["expected"])
                self.assertTrue(entry["purpose"])
                total_bytes += len(content)
        self.assertEqual(total_bytes, manifest["total_document_bytes"])
        self.assertLess(total_bytes, 5_000_000)
        for library in ("reportlab", "PyMuPDF", "Pillow"):
            self.assertTrue(manifest["generator_versions"][library])

    def test_plain_text_is_searchable_in_three_independent_parsers(self):
        path = self.document("plain-text")
        reader = pypdf.PdfReader(path)
        with pymupdf.open(path) as document:
            texts = [reader.pages[0].extract_text(), document[0].get_text(), pdfium_text(path)]
            self.assertEqual(len(reader.pages), 1)
            self.assertTrue(document[0].search_for("lighthouse-427"))
        for text in texts:
            self.assertIn("PLAIN-TEXT-ALPHA", text)
            self.assertIn("lighthouse-427", text)

    def test_two_columns_have_distinct_regions_and_column_major_content(self):
        path = self.document("two-columns")
        with pymupdf.open(path) as document:
            left = document[0].search_for("LEFT-01")
            right = document[0].search_for("RIGHT-01")
            self.assertEqual(len(left), 1)
            self.assertEqual(len(right), 1)
            self.assertLess(left[0].x1, 290)
            self.assertGreater(right[0].x0, 320)
            self.assertAlmostEqual(left[0].y0, right[0].y0, delta=1)
        for text in (pypdf.PdfReader(path).pages[0].extract_text(), pdfium_text(path)):
            markers = ["LEFT-01", "LEFT-02", "LEFT-03", "RIGHT-01", "RIGHT-02", "RIGHT-03"]
            positions = [text.index(marker) for marker in markers]
            self.assertEqual(positions, sorted(positions))

    def test_long_document_keeps_all_hundred_pages_and_distant_search_anchors(self):
        path = self.document("long-document")
        reader = pypdf.PdfReader(path)
        with pymupdf.open(path) as mupdf, pikepdf.open(path) as qpdf:
            with pdfium.PdfDocument(path) as pdfium_document:
                self.assertEqual(len(reader.pages), 100)
                self.assertEqual(len(mupdf), 100)
                self.assertEqual(len(qpdf.pages), 100)
                self.assertEqual(len(pdfium_document), 100)
            for index, marker in [(0, "LONG-DOC-PAGE-001"), (49, "LONG-DOC-PAGE-050"), (99, "LONG-DOC-PAGE-100")]:
                with self.subTest(page=index + 1):
                    self.assertIn(marker, reader.pages[index].extract_text())
                    self.assertIn(marker, mupdf[index].get_text())
                    self.assertIn(marker, pdfium_text(path, index))

    def test_mixed_geometry_preserves_media_boxes_and_rotations(self):
        path = self.document("mixed-geometry")
        reader = pypdf.PdfReader(path)
        media_sizes = [(612, 792), (420, 595), (792, 612), (300, 450)]
        displayed_sizes = [(612, 792), (595, 420), (792, 612), (450, 300)]
        with pymupdf.open(path) as mupdf, pdfium.PdfDocument(path) as pdfium_document:
            self.assertEqual(len(reader.pages), 4)
            for index, rotation in enumerate([0, 90, 180, 270]):
                with self.subTest(page=index + 1):
                    page = reader.pages[index]
                    self.assertEqual((float(page.mediabox.width), float(page.mediabox.height)), media_sizes[index])
                    self.assertEqual(page.rotation, rotation)
                    self.assertEqual(mupdf[index].rotation, rotation)
                    self.assertEqual((mupdf[index].rect.width, mupdf[index].rect.height), displayed_sizes[index])
                    with closing(pdfium_document[index]) as pdfium_page:
                        self.assertEqual(pdfium_page.get_rotation(), rotation)
                        self.assertEqual(pdfium_page.get_size(), displayed_sizes[index])

    def test_internal_links_and_outlines_resolve_to_real_pages(self):
        path = self.document("navigation")
        reader = pypdf.PdfReader(path)
        outline = [(item.title, reader.get_destination_page_number(item)) for item in reader.outline]
        self.assertEqual(outline, [("Start", 0), ("Middle", 1), ("End", 2)])
        for source, target in [(0, 2), (2, 0)]:
            links = [ref.get_object() for ref in reader.pages[source]["/Annots"]]
            self.assertEqual(len(links), 1)
            self.assertEqual(links[0]["/Subtype"], "/Link")
            self.assertEqual(links[0]["/Dest"][0], reader.pages[target].indirect_reference)
        with pymupdf.open(path) as document:
            self.assertEqual(document.get_toc(), [[1, "Start", 1], [1, "Middle", 2], [1, "End", 3]])
            for source, target in [(0, 2), (2, 0)]:
                page = document[source]
                link = page.first_link
                self.assertIsNotNone(link)
                self.assertTrue(link.uri.startswith("#"))
                self.assertEqual(document.resolve_link(link.uri)[0], target)
                self.assertIsNone(link.next)
        with pdfium.PdfDocument(path) as document:
            actual = [(bookmark.get_title(), bookmark.get_dest().get_index()) for bookmark in document.get_toc()]
            self.assertEqual(actual, [("Start", 0), ("Middle", 1), ("End", 2)])

    def test_annotations_are_standard_objects_with_a_portable_note(self):
        path = self.document("annotations")
        expected = {"/Text", "/Highlight", "/Underline", "/StrikeOut", "/Ink", "/Square"}
        objects = [ref.get_object() for ref in pypdf.PdfReader(path).pages[0]["/Annots"]]
        self.assertEqual({obj["/Subtype"] for obj in objects} - {"/Popup"}, expected)
        self.assertIn("SYNTHETIC-NOTE-001", [obj.get("/Contents") for obj in objects])
        with pymupdf.open(path) as document:
            page = document[0]
            annotations = list(page.annots())
            self.assertEqual({"/" + annotation.type[1] for annotation in annotations}, expected)
            self.assertTrue(all(annotation.rect.width > 0 for annotation in annotations))

    def test_acroform_fields_remain_editable_widgets_with_initial_values(self):
        path = self.document("acroform")
        fields = pypdf.PdfReader(path).get_fields()
        self.assertEqual(set(fields), {"reader_name", "subscribe", "color"})
        self.assertEqual(fields["reader_name"]["/FT"], "/Tx")
        self.assertEqual(fields["reader_name"]["/V"], "Test Reader")
        self.assertEqual(fields["subscribe"]["/FT"], "/Btn")
        self.assertEqual(fields["subscribe"]["/V"], "/Yes")
        self.assertEqual(fields["color"]["/FT"], "/Ch")
        self.assertEqual(fields["color"]["/V"], "Blue")
        with pymupdf.open(path) as document:
            page = document[0]
            widgets = {widget.field_name: widget for widget in page.widgets()}
            self.assertEqual(set(widgets), set(fields))
            self.assertEqual(widgets["reader_name"].field_value, "Test Reader")
            self.assertEqual(widgets["subscribe"].field_value, "Yes")
            self.assertEqual(widgets["color"].field_value, "Blue")
        with pikepdf.open(path) as document:
            self.assertEqual(len(document.Root.AcroForm.Fields), 3)
            self.assertTrue(all("/AP" in field for field in document.Root.AcroForm.Fields))

    def test_password_is_required_and_public_test_password_unlocks_content(self):
        path = self.document("password-protected")
        reader = pypdf.PdfReader(path)
        self.assertTrue(reader.is_encrypted)
        self.assertEqual(reader.decrypt(""), 0)
        self.assertEqual(reader.decrypt("incorrect"), 0)
        self.assertNotEqual(reader.decrypt("reader-lab"), 0)
        self.assertIn("PASSWORD-OPEN-271", reader.pages[0].extract_text())
        with pymupdf.open(path) as document:
            self.assertTrue(document.needs_pass)
            self.assertEqual(document.authenticate("incorrect"), 0)
            self.assertGreater(document.authenticate("reader-lab"), 0)
            self.assertIn("PASSWORD-OPEN-271", document[0].get_text())
        for password in (None, "incorrect"):
            with self.subTest(engine="PDFium", password=password):
                with self.assertRaises(pdfium.PdfiumError):
                    pdfium.PdfDocument(path, password=password)
            with self.subTest(engine="qpdf", password=password):
                with self.assertRaises(pikepdf.PasswordError):
                    pikepdf.open(path, password=password or "")
        with pikepdf.open(path, password="reader-lab") as document:
            self.assertEqual(len(document.pages), 1)
            self.assertTrue(document.is_encrypted)
        self.assertIn("PASSWORD-OPEN-271", pdfium_text(path, password="reader-lab"))

    def test_scan_has_an_image_but_no_selectable_text_layer(self):
        path = self.document("scanned-image-only")
        reader = pypdf.PdfReader(path)
        self.assertEqual(reader.pages[0].extract_text().strip(), "")
        self.assertGreaterEqual(len(reader.pages[0].images), 1)
        with pymupdf.open(path) as document:
            self.assertEqual(document[0].get_text().strip(), "")
            self.assertEqual(len(document[0].get_images()), 1)
        self.assertEqual(pdfium_text(path).strip(), "")
        with pdfium.PdfDocument(path) as document, closing(document[0]) as page:
            self.assertEqual(len(list(page.get_objects(filter=[pdfium_raw.FPDF_PAGEOBJ_IMAGE]))), 1)
            self.assertEqual(len(list(page.get_objects(filter=[pdfium_raw.FPDF_PAGEOBJ_TEXT]))), 0)

    def test_unicode_preserves_accents_and_includes_font_permission_notice(self):
        path = self.document("unicode")
        expected = "café naïve façade Straße Ångström €"
        reader = pypdf.PdfReader(path)
        with pymupdf.open(path) as document:
            for text in [reader.pages[0].extract_text(), document[0].get_text(), pdfium_text(path)]:
                self.assertIn(expected, text)
            embedded_fonts = [font for font in document[0].get_fonts() if font[1] == "ttf"]
            self.assertTrue(embedded_fonts, "Unicode must not rely on an OS font")
            self.assertIn("font-license.txt", document.embfile_names())
            self.assertIn(b"Copyright (c) 2003 by Bitstream", document.embfile_get("font-license.txt"))
        font = self.manifest()["unicode_font"]
        self.assertEqual(font["sha256"], "c4c45690b345435b2cba52ecabe275f05e49b389b39fe68ad03afbb551288d3d")
        license_path = FIXTURES / font["license_path"]
        self.assertIn("Permission is hereby granted", license_path.read_text(encoding="utf-8"))

    def test_epub_has_a_valid_container_two_spine_chapters_and_working_toc(self):
        path = self.document("tiny-original", "epub")
        ns = {"opf": "http://www.idpf.org/2007/opf", "c": "urn:oasis:names:tc:opendocument:xmlns:container", "x": "http://www.w3.org/1999/xhtml"}
        with zipfile.ZipFile(path) as archive:
            first = archive.infolist()[0]
            self.assertEqual(first.filename, "mimetype")
            self.assertEqual(first.compress_type, zipfile.ZIP_STORED)
            self.assertEqual(archive.read("mimetype"), b"application/epub+zip")
            self.assertIsNone(archive.testzip())
            container = ET.fromstring(archive.read("META-INF/container.xml"))
            package_path = container.find("c:rootfiles/c:rootfile", ns).attrib["full-path"]
            package = ET.fromstring(archive.read(package_path))
            items = {item.attrib["id"]: item.attrib for item in package.findall("opf:manifest/opf:item", ns)}
            spine = [item.attrib["idref"] for item in package.findall("opf:spine/opf:itemref", ns)]
            self.assertEqual(spine, ["chapter-one", "chapter-two"])
            nav_item = next(item for item in items.values() if item.get("properties") == "nav")
            nav = ET.fromstring(archive.read("OEBPS/" + nav_item["href"]))
            links = [link.attrib["href"] for link in nav.findall(".//x:nav/x:ol/x:li/x:a", ns)]
            self.assertEqual(links, ["chapter-one.xhtml#one", "chapter-two.xhtml#two"])
            for link in links:
                filename, anchor = link.split("#")
                chapter = ET.fromstring(archive.read("OEBPS/" + filename))
                self.assertTrue(any(node.attrib.get("id") == anchor for node in chapter.iter()))
        with pymupdf.open(path) as document:
            text = "\n".join(page.get_text() for page in document)
            self.assertIn("EPUB-CHAPTER-ONE", text)
            self.assertIn("EPUB-CHAPTER-TWO", text)

    def test_selected_pages_render_nonblank_in_mupdf_and_pdfium(self):
        for name in sorted(PDF_NAMES):
            path = self.document(name)
            password = "reader-lab" if name == "password-protected" else None
            with pymupdf.open(path) as mupdf, pdfium.PdfDocument(path, password=password) as pdfium_document:
                if password:
                    self.assertGreater(mupdf.authenticate(password), 0)
                pdfium_document.init_forms()
                indices = [0, 49, 99] if name == "long-document" else list(range(len(mupdf)))
                for index in indices:
                    with self.subTest(fixture=name, page=index + 1):
                        pixels = mupdf[index].get_pixmap(matrix=pymupdf.Matrix(0.5, 0.5), colorspace=pymupdf.csGRAY)
                        self.assertLess(min(pixels.samples), 200)
                        self.assertGreater(max(pixels.samples), 240)
                        with closing(pdfium_document[index]) as page, closing(page.render(scale=0.5, grayscale=True, draw_annots=True)) as bitmap:
                            low, high = bitmap.to_pil().getextrema()
                            self.assertLess(low, 200)
                            self.assertGreater(high, 240)

    def test_generation_is_byte_repeatable_across_two_output_directories(self):
        self.assertTrue(GENERATOR.is_file(), "Fixture generator has not been implemented")
        with tempfile.TemporaryDirectory(prefix="reader-fixtures-", dir=TEMP_ROOT) as temporary:
            first, second = Path(temporary) / "first", Path(temporary) / "second"
            for destination in (first, second):
                result = run_script(GENERATOR, "--output", str(destination))
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual((first / "manifest.json").read_bytes(), (second / "manifest.json").read_bytes())
            manifest = json.loads((first / "manifest.json").read_text(encoding="utf-8"))
            for entry in manifest["fixtures"]:
                with self.subTest(fixture=entry["id"]):
                    self.assertEqual((first / entry["path"]).read_bytes(), (second / entry["path"]).read_bytes())

    def test_reference_checker_records_real_host_engines_without_app_claims(self):
        self.assertTrue(CHECKER.is_file(), "Reference checker has not been implemented")
        with tempfile.TemporaryDirectory(prefix="reader-check-", dir=TEMP_ROOT) as temporary:
            output = Path(temporary) / "results.json"
            result = run_script(CHECKER, "--fixtures", str(FIXTURES), "--output", str(output))
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            report = json.loads(output.read_text(encoding="utf-8"))
            self.assertFalse(report["moon_reader_tested"])
            self.assertEqual(report["evidence_type"], "reference-engine-check")
            self.assertEqual(report["summary"]["fixtures_passed"], 11)
            self.assertEqual(report["summary"]["fixtures_failed"], 0)
            for entry in report["results"]:
                self.assertEqual(entry["status"], "pass")
                if entry["fixture_id"] != "tiny-original":
                    self.assertEqual(set(entry["engines"]), {"pypdf", "PyMuPDF", "pikepdf", "pypdfium2"})
                    self.assertTrue(all(engine["observed"]["page_count"] > 0 for engine in entry["engines"].values()))

    def test_reference_checker_rejects_an_altered_document_hash(self):
        self.assertTrue(CHECKER.is_file(), "Reference checker has not been implemented")
        self.manifest()
        with tempfile.TemporaryDirectory(prefix="reader-tamper-", dir=TEMP_ROOT) as temporary:
            copied = Path(temporary) / "fixtures"
            shutil.copytree(FIXTURES, copied)
            with (copied / "documents" / "plain-text.pdf").open("ab") as stream:
                stream.write(b"\n% deliberately changed test bytes\n")
            output = Path(temporary) / "results.json"
            result = run_script(CHECKER, "--fixtures", str(copied), "--output", str(output))
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            report = json.loads(output.read_text(encoding="utf-8"))
            plain = next(entry for entry in report["results"] if entry["fixture_id"] == "plain-text")
            self.assertFalse(plain["sha256_matches"])
            self.assertEqual(plain["status"], "fail")

    def test_reference_checker_rejects_wrong_expected_page_count(self):
        self.assertTrue(CHECKER.is_file(), "Reference checker has not been implemented")
        self.manifest()
        with tempfile.TemporaryDirectory(prefix="reader-expectation-", dir=TEMP_ROOT) as temporary:
            copied = Path(temporary) / "fixtures"
            shutil.copytree(FIXTURES, copied)
            manifest_path = copied / "manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            plain = next(entry for entry in manifest["fixtures"] if entry["id"] == "plain-text")
            plain["expected"]["page_count"] = 2
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            output = Path(temporary) / "results.json"
            result = run_script(CHECKER, "--fixtures", str(copied), "--output", str(output))
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            report = json.loads(output.read_text(encoding="utf-8"))
            plain_result = next(entry for entry in report["results"] if entry["fixture_id"] == "plain-text")
            for engine in plain_result["engines"].values():
                check = next(check for check in engine["checks"] if check["property"] == "page_count")
                self.assertEqual(check["actual"], 1)
                self.assertEqual(check["expected"], 2)
                self.assertFalse(check["passed"])


if __name__ == "__main__":
    unittest.main()
