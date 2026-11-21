"""Generate small, original reader inputs with deterministic metadata and bytes."""

from __future__ import annotations

import argparse
import hashlib
from importlib.metadata import version
from io import BytesIO
import json
from pathlib import Path
import platform
import zipfile

from PIL import Image, ImageDraw, ImageFont
import pymupdf
import reportlab
from reportlab.lib.pdfencrypt import StandardEncryption
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen.canvas import Canvas


ROOT = Path(__file__).resolve().parents[1]
PDF_DATE = "D:20000101000000Z"
FONT_SHA256 = "c4c45690b345435b2cba52ecabe275f05e49b389b39fe68ad03afbb551288d3d"
USER_PASSWORD = "reader-lab"
OWNER_PASSWORD = "reader-owner-lab"
UNICODE_TEXT = "café naïve façade Straße Ångström €"


def canvas_for(buffer: BytesIO, title: str, **options) -> Canvas:
    canvas = Canvas(
        buffer, pagesize=(612, 792), invariant=1, pageCompression=1, **options
    )
    canvas.setTitle(title)
    canvas.setAuthor("Reader Improvement Lab — original synthetic corpus")
    canvas.setCreator("scripts/generate_fixtures.py")
    canvas.setSubject("Original MIT-licensed test input; no reader-app result implied")
    return canvas


def heading(canvas: Canvas, text: str, height: float = 792) -> None:
    canvas.setFont("Helvetica-Bold", 16)
    canvas.drawString(36, height - 48, text)
    canvas.setFont("Helvetica", 11)


def plain_text() -> bytes:
    buffer = BytesIO()
    canvas = canvas_for(buffer, "Plain selectable text")
    heading(canvas, "PLAIN-TEXT-ALPHA")
    for index, line in enumerate(
        [
            "A small brass lighthouse marks the edge of a fictional paper sea.",
            "Search anchor: lighthouse-427. Select this sentence and copy it.",
            "Every sentence on this page was written for this test corpus.",
            "Digits: 0123456789. Punctuation: comma, period. Question? Yes!",
            "The final line is a stable reading-position anchor: PLAIN-END-903.",
        ]
    ):
        canvas.drawString(36, 700 - index * 24, line)
    canvas.showPage()
    canvas.save()
    return buffer.getvalue()


def two_columns() -> bytes:
    buffer = BytesIO()
    canvas = canvas_for(buffer, "Two columns with column-major content")
    heading(canvas, "TWO-COLUMN-READING-ORDER")
    canvas.setFont("Helvetica", 10)
    for side, x, sentences in [
        ("LEFT", 36, ["A paper boat leaves the dock.", "It carries a tiny green flag.", "The left column ends here."]),
        ("RIGHT", 330, ["A second boat follows slowly.", "It carries a tiny blue flag.", "The right column ends here."]),
    ]:
        for index, sentence in enumerate(sentences, start=1):
            canvas.drawString(x, 700 - (index - 1) * 30, f"{side}-{index:02d} {sentence}")
    canvas.showPage()
    canvas.save()
    return buffer.getvalue()


def long_document() -> bytes:
    buffer = BytesIO()
    canvas = canvas_for(buffer, "One hundred original synthetic pages")
    for number in range(1, 101):
        heading(canvas, f"LONG-DOC-PAGE-{number:03d}")
        canvas.drawString(36, 704, f"This is page {number} of 100 in a fictional field notebook.")
        for row in range(1, 13):
            canvas.drawString(
                36,
                668 - row * 24,
                f"Entry {number:03d}.{row:02d}: The clockwork garden has {number + row} paper leaves.",
            )
        canvas.drawString(36, 72, f"Stable bookmark anchor: NOTEBOOK-{number:03d}-END")
        canvas.showPage()
    canvas.save()
    return buffer.getvalue()


def mixed_geometry() -> bytes:
    buffer = BytesIO()
    canvas = canvas_for(buffer, "Mixed media boxes and rotations")
    for number, (width, height) in enumerate([(612, 792), (420, 595), (792, 612), (300, 450)], start=1):
        canvas.setPageSize((width, height))
        heading(canvas, f"GEOMETRY-PAGE-{number}", height)
        canvas.drawString(36, height - 84, f"Media box: {width} x {height} points")
        canvas.drawString(36, height - 108, f"Page rotation: {(number - 1) * 90} degrees")
        canvas.rect(24, 24, width - 48, height - 48)
        canvas.showPage()
    canvas.save()
    with pymupdf.open(stream=buffer.getvalue(), filetype="pdf") as document:
        for page, rotation in zip(document, [0, 90, 180, 270]):
            page.set_rotation(rotation)
        return document.tobytes(garbage=4, deflate=True, no_new_id=True)


def navigation() -> bytes:
    buffer = BytesIO()
    canvas = canvas_for(buffer, "Internal links and outlines")
    for number, name in enumerate(["Start", "Middle", "End"], start=1):
        canvas.bookmarkPage(name.lower())
        canvas.addOutlineEntry(name, name.lower(), level=0)
        heading(canvas, f"NAVIGATION-{name.upper()}")
        canvas.drawString(36, 700, f"Section {number} of 3. Use the outline to move between sections.")
        if name == "Start":
            canvas.drawString(36, 660, "Jump to End (page 3)")
            canvas.linkRect("Jump to End", "end", (32, 654, 220, 676), relative=0, thickness=1)
        elif name == "End":
            canvas.drawString(36, 660, "Return to Start (page 1)")
            canvas.linkRect("Return to Start", "start", (32, 654, 220, 676), relative=0, thickness=1)
        canvas.showPage()
    canvas.save()
    return buffer.getvalue()


def annotations() -> bytes:
    buffer = BytesIO()
    canvas = canvas_for(buffer, "Standard portable annotation objects")
    heading(canvas, "STANDARD-ANNOTATIONS")
    phrases = ["Highlight this synthetic phrase", "Underline this synthetic phrase", "Strike out this synthetic phrase"]
    for index, phrase in enumerate(phrases):
        canvas.drawString(36, 700 - index * 42, phrase)
    canvas.drawString(36, 490, "A square and an ink stroke are stored as annotations below.")
    canvas.showPage()
    canvas.save()
    with pymupdf.open(stream=buffer.getvalue(), filetype="pdf") as document:
        page = document[0]
        objects = [
            page.add_text_annot((540, 60), "SYNTHETIC-NOTE-001"),
            page.add_highlight_annot(page.search_for(phrases[0])),
            page.add_underline_annot(page.search_for(phrases[1])),
            page.add_strikeout_annot(page.search_for(phrases[2])),
            page.add_ink_annot([[(48, 350), (90, 365), (135, 340), (180, 365)]]),
            page.add_rect_annot(pymupdf.Rect(250, 330, 400, 405)),
        ]
        for number, annotation in enumerate(objects):
            annotation.set_info(
                content="SYNTHETIC-NOTE-001" if number == 0 else f"SYNTHETIC-MARK-{number:03d}",
                title="Synthetic author",
                creationDate=PDF_DATE,
                modDate=PDF_DATE,
            )
            annotation.update()
        return document.tobytes(garbage=4, deflate=True, no_new_id=True)


def acroform() -> bytes:
    buffer = BytesIO()
    canvas = canvas_for(buffer, "Three editable AcroForm controls")
    heading(canvas, "ACROFORM-INITIAL-VALUES")
    canvas.drawString(36, 704, "Name (editable text):")
    canvas.acroForm.textfield(name="reader_name", tooltip="Reader name", value="Test Reader", x=200, y=690, width=240, height=26)
    canvas.drawString(36, 644, "Subscribe (checked):")
    canvas.acroForm.checkbox(name="subscribe", tooltip="Subscribe", checked=True, x=200, y=638, size=18, buttonStyle="check")
    canvas.drawString(36, 586, "Favorite color (choice):")
    canvas.acroForm.choice(name="color", tooltip="Favorite color", options=["Red", "Blue", "Green"], value="Blue", x=200, y=572, width=140, height=26)
    canvas.drawString(36, 520, "This synthetic form contains no submission action or JavaScript.")
    canvas.showPage()
    canvas.save()
    return buffer.getvalue()


def password_protected() -> bytes:
    buffer = BytesIO()
    encryption = StandardEncryption(USER_PASSWORD, ownerPassword=OWNER_PASSWORD, strength=128)
    canvas = canvas_for(buffer, "Public test-password document", encrypt=encryption)
    heading(canvas, "PASSWORD-OPEN-271")
    canvas.drawString(36, 704, "The public test password unlocked this original synthetic page.")
    canvas.drawString(36, 680, "Legacy RC4-128 / revision 3 compatibility fixture; all permissions enabled.")
    canvas.showPage()
    canvas.save()
    return buffer.getvalue()


def scanned_image_only(font_path: Path) -> bytes:
    image = Image.new("L", (612, 792), color=255)
    draw = ImageDraw.Draw(image)
    title_font = ImageFont.truetype(str(font_path), 24)
    body_font = ImageFont.truetype(str(font_path), 16)
    draw.text((36, 48), "SYNTHETIC SCANNED PAGE", fill=0, font=title_font)
    for index, line in enumerate(
        [
            "This page was drawn directly into an image.",
            "It has no selectable or hidden OCR text layer.",
            "Visible OCR target: SCAN-ANCHOR-846",
            "A small square has four equal paper sides.",
            "All prose and geometry are original test material.",
        ]
    ):
        draw.text((36, 118 + index * 42), line, fill=0, font=body_font)
    draw.rectangle((80, 400, 250, 570), outline=0, width=5)
    draw.line((340, 540, 430, 400, 520, 540, 340, 540), fill=0, width=5)
    buffer = BytesIO()
    canvas = canvas_for(buffer, "Synthetic image-only scan")
    canvas.drawImage(ImageReader(image), 0, 0, width=612, height=792)
    canvas.showPage()
    canvas.save()
    return buffer.getvalue()


def unicode_document(font_path: Path, license_bytes: bytes) -> bytes:
    buffer = BytesIO()
    canvas = canvas_for(buffer, "Embedded-font Unicode text")
    heading(canvas, "UNICODE-SELECTABLE")
    canvas.showPage()
    canvas.save()
    with pymupdf.open(stream=buffer.getvalue(), filetype="pdf") as document:
        page = document[0]
        # Embed the unmodified font in full: no subset/derivative naming ambiguity.
        page.insert_font(fontname="FixtureVera", fontfile=str(font_path))
        page.insert_text((36, 104), UNICODE_TEXT, fontname="FixtureVera", fontsize=17)
        page.insert_text((36, 145), "Symbols: Ω ∑ — €", fontname="FixtureVera", fontsize=17)
        page.insert_text((36, 186), "Precomposed Latin accents and symbols only.", fontname="FixtureVera", fontsize=12)
        attachment = document.embfile_add("font-license.txt", license_bytes, desc="Bitstream Vera permission and copyright notice")
        # embfile_add otherwise injects wall-clock dates into the stream parameters.
        document.xref_set_key(attachment, "Params/CreationDate", pymupdf.get_pdf_str(PDF_DATE))
        document.xref_set_key(attachment, "Params/ModDate", pymupdf.get_pdf_str(PDF_DATE))
        return document.tobytes(garbage=4, deflate=True, no_new_id=True)


def tiny_epub() -> bytes:
    files = {
        "mimetype": "application/epub+zip",
        "META-INF/container.xml": '<?xml version="1.0" encoding="utf-8"?>\n<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container"><rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/></rootfiles></container>',
        "OEBPS/content.opf": '''<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="book-id" xml:lang="en">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="book-id">urn:uuid:a5b14a2d-ef45-4e41-8c86-76917e6af491</dc:identifier>
    <dc:title>The Paper Harbor</dc:title><dc:language>en</dc:language>
    <dc:creator>Reader Improvement Lab</dc:creator>
    <dc:rights>Original synthetic text. MIT License; Copyright (c) 2026 Chirag Singhal.</dc:rights>
    <meta property="dcterms:modified">2000-01-01T00:00:00Z</meta>
  </metadata>
  <manifest>
    <item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>
    <item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>
    <item id="chapter-one" href="chapter-one.xhtml" media-type="application/xhtml+xml"/>
    <item id="chapter-two" href="chapter-two.xhtml" media-type="application/xhtml+xml"/>
  </manifest>
  <spine toc="ncx"><itemref idref="chapter-one"/><itemref idref="chapter-two"/></spine>
</package>''',
        "OEBPS/nav.xhtml": '''<?xml version="1.0" encoding="utf-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="en"><head><title>Contents</title></head><body>
<nav epub:type="toc" id="toc"><h1>Contents</h1><ol><li><a href="chapter-one.xhtml#one">A Paper Harbor</a></li><li><a href="chapter-two.xhtml#two">The Quiet Return</a></li></ol></nav>
</body></html>''',
        "OEBPS/toc.ncx": '''<?xml version="1.0" encoding="utf-8"?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1"><head><meta name="dtb:uid" content="urn:uuid:a5b14a2d-ef45-4e41-8c86-76917e6af491"/></head><docTitle><text>The Paper Harbor</text></docTitle><navMap><navPoint id="one" playOrder="1"><navLabel><text>A Paper Harbor</text></navLabel><content src="chapter-one.xhtml#one"/></navPoint><navPoint id="two" playOrder="2"><navLabel><text>The Quiet Return</text></navLabel><content src="chapter-two.xhtml#two"/></navPoint></navMap></ncx>''',
        "OEBPS/chapter-one.xhtml": '''<?xml version="1.0" encoding="utf-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en"><head><title>A Paper Harbor</title></head><body><h1 id="one">A Paper Harbor</h1><p>EPUB-CHAPTER-ONE</p><p>A paper boat rested beside a folded lighthouse. Each evening, a patient clockwork keeper counted the painted waves. On the seventh evening, a new blue flag appeared on the boat.</p><p><a href="chapter-two.xhtml#two">Continue to the quiet return.</a></p></body></html>''',
        "OEBPS/chapter-two.xhtml": '''<?xml version="1.0" encoding="utf-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en"><head><title>The Quiet Return</title></head><body><h1 id="two">The Quiet Return</h1><p>EPUB-CHAPTER-TWO</p><p>The boat crossed the paper sea and returned before the ink had dried. The keeper folded the flag into a bookmark, then placed it between two empty pages. Tomorrow would bring another original story.</p><p><a href="chapter-one.xhtml#one">Return to the paper harbor.</a></p></body></html>''',
    }
    buffer = BytesIO()
    with zipfile.ZipFile(buffer, "w") as archive:
        for name, text in files.items():
            info = zipfile.ZipInfo(name, date_time=(2000, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_STORED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, text.encode("utf-8"))
    return buffer.getvalue()


def generate(output: Path) -> dict:
    font_path = Path(reportlab.__file__).parent / "fonts" / "Vera.ttf"
    license_path = font_path.with_name("bitstream-vera-license.txt")
    if not font_path.is_file() or not license_path.is_file():
        raise RuntimeError("Unicode fixture blocked: ReportLab's bundled Vera font/license is missing")
    if hashlib.sha256(font_path.read_bytes()).hexdigest() != FONT_SHA256:
        raise RuntimeError("Unicode fixture blocked: bundled font differs from the reviewed SHA-256")
    license_bytes = license_path.read_bytes()
    license_hash = hashlib.sha256(license_bytes).hexdigest()
    documents = output / "documents"
    documents.mkdir(parents=True, exist_ok=True)
    (output / "licenses").mkdir(parents=True, exist_ok=True)
    (output / "licenses" / "bitstream-vera-license.txt").write_bytes(license_bytes)

    recipes = [
        ("plain-text", plain_text, "Selection, search, copy and reading-position baseline.", {"text_by_page": {"1": ["PLAIN-TEXT-ALPHA", "lighthouse-427", "PLAIN-END-903"]}}),
        ("two-columns", two_columns, "Column geometry and content-stream reading order.", {"text_by_page": {"1": ["LEFT-01", "RIGHT-01"]}, "text_order": ["LEFT-01", "LEFT-02", "LEFT-03", "RIGHT-01", "RIGHT-02", "RIGHT-03"], "column_regions": {"left_marker": "LEFT-01", "left_max_x": 290, "right_marker": "RIGHT-01", "right_min_x": 320}}),
        ("long-document", long_document, "One hundred pages for distant search and navigation; no speed claim.", {"page_count": 100, "render_pages": [1, 50, 100], "text_by_page": {"1": ["LONG-DOC-PAGE-001"], "50": ["LONG-DOC-PAGE-050"], "100": ["LONG-DOC-PAGE-100"]}}),
        ("mixed-geometry", mixed_geometry, "Four exact media boxes and all quarter-turn rotations.", {"page_count": 4, "render_pages": [1, 2, 3, 4], "page_geometry": [{"media_size": [612, 792], "rotation": 0, "displayed_size": [612, 792]}, {"media_size": [420, 595], "rotation": 90, "displayed_size": [595, 420]}, {"media_size": [792, 612], "rotation": 180, "displayed_size": [792, 612]}, {"media_size": [300, 450], "rotation": 270, "displayed_size": [450, 300]}], "text_by_page": {str(number): [f"GEOMETRY-PAGE-{number}"] for number in range(1, 5)}}),
        ("navigation", navigation, "Internal links with actual destinations and three outline entries.", {"page_count": 3, "render_pages": [1, 2, 3], "text_by_page": {"1": ["NAVIGATION-START"], "2": ["NAVIGATION-MIDDLE"], "3": ["NAVIGATION-END"]}, "outlines": [{"level": 1, "title": name, "page": number} for number, name in enumerate(["Start", "Middle", "End"], start=1)], "internal_links": [{"source_page": 1, "target_page": 3}, {"source_page": 3, "target_page": 1}]}),
        ("annotations", annotations, "Six standard annotation types and a portable note, plus the note popup.", {"text_by_page": {"1": ["STANDARD-ANNOTATIONS"]}, "annotation_types": ["Highlight", "Ink", "Square", "StrikeOut", "Text", "Underline"], "note_contents": "SYNTHETIC-NOTE-001"}),
        ("acroform", acroform, "Unflattened text, checkbox and choice controls with initial appearances.", {"text_by_page": {"1": ["ACROFORM-INITIAL-VALUES"]}, "fields": {"reader_name": {"type": "Tx", "value": "Test Reader"}, "subscribe": {"type": "Btn", "value": "Yes"}, "color": {"type": "Ch", "value": "Blue"}}}),
        ("password-protected", password_protected, "Reject missing/wrong passwords; open using the public test password.", {"encrypted": True, "user_password": USER_PASSWORD, "owner_password": OWNER_PASSWORD, "encryption": "RC4-128, standard security handler revision 3", "text_by_page": {"1": ["PASSWORD-OPEN-271"]}}),
        ("scanned-image-only", lambda: scanned_image_only(font_path), "A visible image with no OCR or selectable text layer.", {"text_layer": False, "image_count_by_page": {"1": 1}, "visible_ocr_target": "SCAN-ANCHOR-846"}),
        ("unicode", lambda: unicode_document(font_path, license_bytes), "Precomposed Latin accents and symbols with an unmodified embedded font.", {"text_by_page": {"1": [UNICODE_TEXT, "Symbols: Ω ∑ — €"]}, "embedded_font_sha256": FONT_SHA256, "font_license_attachment": {"name": "font-license.txt", "sha256": license_hash}}),
    ]
    entries = []
    for identifier, build, purpose, properties in recipes:
        content = build()
        filename = f"documents/{identifier}.pdf"
        (output / filename).write_bytes(content)
        entries.append({
            "id": identifier, "path": filename, "media_type": "application/pdf",
            "sha256": hashlib.sha256(content).hexdigest(), "size_bytes": len(content),
            "purpose": purpose,
            "expected": {"page_count": 1, "encrypted": False, "text_layer": True, "render_pages": [1], **properties},
        })
    epub = tiny_epub()
    (documents / "tiny-original.epub").write_bytes(epub)
    entries.append({
        "id": "tiny-original", "path": "documents/tiny-original.epub",
        "media_type": "application/epub+zip", "sha256": hashlib.sha256(epub).hexdigest(),
        "size_bytes": len(epub), "purpose": "Two original reflowable chapters, spine order and navigable anchors.",
        "expected": {"spine_ids": ["chapter-one", "chapter-two"], "nav_links": ["chapter-one.xhtml#one", "chapter-two.xhtml#two"], "text_markers": ["EPUB-CHAPTER-ONE", "EPUB-CHAPTER-TWO"]},
    })
    manifest = {
        "schema_version": 1,
        "origin": {"kind": "original-synthetic", "license": "MIT", "copyright": "Copyright (c) 2026 Chirag Singhal", "source": "scripts/generate_fixtures.py", "source_url": "https://github.com/chirag127/reader-improvement-lab", "note": "Original prose, vector geometry and synthetic raster page; no APK samples or personal documents."},
        "generator_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "generator_versions": {"python": platform.python_version(), **{name: version(name) for name in ["reportlab", "PyMuPDF", "Pillow"]}},
        "reproducibility": {"recipe_revision": 1, "metadata_epoch": "2000-01-01T00:00:00Z", "method": "ReportLab invariant metadata, fixed attachment/annotation/ZIP dates, preserved PDF IDs, uncompressed EPUB entries; compare bytes using the declared toolchain."},
        "unicode_font": {"name": "Bitstream Vera Sans", "source": "reportlab/fonts/Vera.ttf", "source_url": f"https://pypi.org/project/reportlab/{version('reportlab')}/", "sha256": FONT_SHA256, "license_path": "licenses/bitstream-vera-license.txt", "license_sha256": license_hash, "embedding": "Full unmodified font; license also attached inside unicode.pdf"},
        "coordinate_convention": "Page numbers are 1-based. PDF dimensions are points. Column x coordinates are measured from the left page edge.",
        "limitations": ["Reference engine checks do not test Moon+ Reader or any Android application.", "Long-document rendering samples pages 1, 50 and 100; page counts cover all pages.", "Unicode coverage is precomposed Latin accents and a few symbols, not RTL, CJK, shaping, normalization or emoji.", "The password case is legacy RC4-128 R3 only, not AES or a security-strength assessment.", "Image-only input has no OCR layer; OCR accuracy is not checked.", "No timing, memory, accessibility, PDF/A, PDF/UA or complete EPUB-conformance claim is made."],
        "total_document_bytes": sum(entry["size_bytes"] for entry in entries),
        "fixtures": entries,
    }
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "fixtures")
    arguments = parser.parse_args()
    manifest = generate(arguments.output)
    print(json.dumps({"fixtures_generated": len(manifest["fixtures"]), "total_document_bytes": manifest["total_document_bytes"], "generator_versions": manifest["generator_versions"]}, indent=2))


if __name__ == "__main__":
    main()
