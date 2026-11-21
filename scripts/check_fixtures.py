"""Check synthetic inputs with host libraries; this does not exercise reader apps."""

from __future__ import annotations

import argparse
from contextlib import closing
from datetime import datetime, timezone
import hashlib
from importlib.metadata import version
import json
from pathlib import Path, PurePosixPath
import platform
import sys
import xml.etree.ElementTree as ET
import zipfile

import pikepdf
import pymupdf
import pypdf
import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_raw


ROOT = Path(__file__).resolve().parents[1]
RENDER_SCALE = 0.5


def sha256(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def text_observations(texts: dict[int, str], expected: dict) -> dict:
    observed = {
        "text_pages": list(texts),
        "text_characters_by_page": {str(page): len(text) for page, text in texts.items()},
        "text_layer_by_page": {str(page): bool(text.strip()) for page, text in texts.items()},
        "text_markers": [
            {"page": int(page), "text": marker, "found": marker in texts.get(int(page), "")}
            for page, markers in expected.get("text_by_page", {}).items()
            for marker in markers
        ],
    }
    if "text_order" in expected:
        text = texts.get(1, "")
        observed["text_order"] = sorted(
            [marker for marker in expected["text_order"] if marker in text],
            key=text.index,
        )
    return observed


def render_observation(page: int, width: int, height: int, pixels: bytes) -> dict:
    low, high = min(pixels), max(pixels)
    return {
        "page": page,
        "width_pixels": width,
        "height_pixels": height,
        "grayscale_min": low,
        "grayscale_max": high,
        "pixel_sha256": sha256(pixels),
        "nonblank": low < 200 and high > 240,
    }


def pypdf_observations(path: Path, expected: dict) -> dict:
    with pypdf.PdfReader(path) as document:
        observed = {"encrypted": document.is_encrypted}
        if document.is_encrypted:
            observed["empty_password_rejected"] = document.decrypt("") == 0
            observed["wrong_password_rejected"] = document.decrypt("incorrect") == 0
            observed["user_password_accepted"] = document.decrypt(expected.get("user_password", "")) != 0
            encryption = document.trailer["/Encrypt"]
            observed["encryption_dictionary"] = {
                "revision": encryption.get("/R"),
                "version": encryption.get("/V"),
                "length_bits": encryption.get("/Length"),
            }
        observed["page_count"] = len(document.pages)
        observed["page_geometry"] = []
        texts = {}
        annotation_objects = []
        images = {}
        fonts = set()
        links = []
        for number, page in enumerate(document.pages, start=1):
            width, height = float(page.mediabox.width), float(page.mediabox.height)
            observed["page_geometry"].append({
                "media_size": [width, height], "rotation": page.rotation,
                "displayed_size": [height, width] if page.rotation in (90, 270) else [width, height],
            })
            texts[number] = page.extract_text()
            annotations = [ref.get_object() for ref in page.get("/Annots", [])]
            annotation_objects.extend(annotations)
            for annotation in annotations:
                if annotation.get("/Subtype") == "/Link" and "/Dest" in annotation:
                    target = annotation["/Dest"][0]
                    page_number = next(
                        (index for index, item in enumerate(document.pages, start=1)
                         if item.indirect_reference == target),
                        None,
                    )
                    links.append({"source_page": number, "target_page": page_number})
            if "image_count_by_page" in expected:
                images[str(number)] = len(page.images)
            if "embedded_font_sha256" in expected:
                for ref in page["/Resources"].get("/Font", {}).values():
                    font = ref.get_object()
                    for candidate in font.get("/DescendantFonts", [font]):
                        descriptor = candidate.get_object().get("/FontDescriptor")
                        if descriptor:
                            stream = descriptor.get_object().get("/FontFile2")
                            if stream:
                                fonts.add(sha256(stream.get_object().get_data()))
        observed.update(text_observations(texts, expected))
        observed["annotation_types"] = sorted({
            str(item["/Subtype"]).removeprefix("/") for item in annotation_objects
            if item["/Subtype"] not in ("/Popup", "/Widget", "/Link")
        })
        observed["popup_count"] = sum(item["/Subtype"] == "/Popup" for item in annotation_objects)
        observed["note_contents"] = [str(item["/Contents"]) for item in annotation_objects if "/Contents" in item]
        observed["internal_links"] = links
        observed["fields"] = {
            name: {"type": str(field.get("/FT", "")).removeprefix("/"),
                   "value": str(field.get("/V", "")).removeprefix("/")}
            for name, field in (document.get_fields() or {}).items()
        }
        if "outlines" in expected:
            observed["outlines"] = [
                {"level": 1, "title": item.title, "page": document.get_destination_page_number(item) + 1}
                for item in document.outline
            ]
        if images:
            observed["image_count_by_page"] = images
        if "embedded_font_sha256" in expected:
            observed["embedded_font_sha256s"] = sorted(fonts)
        if "font_license_attachment" in expected:
            observed["attachment_sha256s"] = {
                name: [sha256(content) for content in contents]
                for name, contents in document.attachments.items()
            }
        return observed


def mupdf_observations(path: Path, expected: dict) -> dict:
    with pymupdf.open(path) as document:
        observed = {"encrypted": bool(document.needs_pass)}
        if document.needs_pass:
            observed["empty_password_rejected"] = document.authenticate("") == 0
            observed["wrong_password_rejected"] = document.authenticate("incorrect") == 0
            observed["user_password_accepted"] = document.authenticate(expected.get("user_password", "")) > 0
        observed["page_count"] = len(document)
        observed["page_geometry"] = []
        observed["renders"] = []
        texts = {}
        annotation_types, contents, links = set(), [], []
        fields, images, fonts = {}, {}, set()
        field_types = {pymupdf.PDF_WIDGET_TYPE_TEXT: "Tx", pymupdf.PDF_WIDGET_TYPE_CHECKBOX: "Btn", pymupdf.PDF_WIDGET_TYPE_COMBOBOX: "Ch"}
        for number, page in enumerate(document, start=1):
            observed["page_geometry"].append({
                "media_size": [page.mediabox.width, page.mediabox.height],
                "rotation": page.rotation,
                "displayed_size": [page.rect.width, page.rect.height],
            })
            texts[number] = page.get_text()
            for annotation in page.annots() or []:
                annotation_types.add(annotation.type[1])
                contents.append(annotation.info.get("content", ""))
            for widget in page.widgets() or []:
                fields[widget.field_name] = {
                    "type": field_types.get(widget.field_type, widget.field_type_string),
                    "value": widget.field_value,
                }
            # Fit destinations can surface as LINK_NAMED; resolve the actual URI.
            link = page.first_link
            while link is not None:
                if link.uri.startswith("#"):
                    target, _, _ = document.resolve_link(link.uri)
                    links.append({"source_page": number, "target_page": target + 1 if target >= 0 else None})
                link = link.next
            if "image_count_by_page" in expected:
                images[str(number)] = len(page.get_images())
            if "embedded_font_sha256" in expected:
                for font in page.get_fonts():
                    if font[1] == "ttf":
                        fonts.add(sha256(document.extract_font(font[0])[3]))
            if number in expected["render_pages"]:
                pixmap = page.get_pixmap(matrix=pymupdf.Matrix(RENDER_SCALE, RENDER_SCALE), colorspace=pymupdf.csGRAY, alpha=False, annots=True)
                observed["renders"].append(render_observation(number, pixmap.width, pixmap.height, pixmap.samples))
        observed.update(text_observations(texts, expected))
        observed.update({"annotation_types": sorted(annotation_types), "note_contents": contents,
                         "fields": fields, "internal_links": links})
        if "outlines" in expected:
            observed["outlines"] = [{"level": level, "title": title, "page": page} for level, title, page in document.get_toc()]
        if "column_regions" in expected:
            regions = expected["column_regions"]
            page = document[0]
            left, right = page.search_for(regions["left_marker"]), page.search_for(regions["right_marker"])
            observed["column_marker_boxes"] = {"left": [list(rect) for rect in left], "right": [list(rect) for rect in right]}
            observed["columns_separated"] = (
                len(left) == len(right) == 1
                and left[0].x1 < regions["left_max_x"]
                and right[0].x0 > regions["right_min_x"]
                and abs(left[0].y0 - right[0].y0) < 1
            )
        if images:
            observed["image_count_by_page"] = images
        if "embedded_font_sha256" in expected:
            observed["embedded_font_sha256s"] = sorted(fonts)
        if "font_license_attachment" in expected:
            observed["attachment_sha256s"] = {name: [sha256(document.embfile_get(name))] for name in document.embfile_names()}
        return observed


def qpdf_observations(path: Path, expected: dict) -> dict:
    observed = {}
    if expected["encrypted"]:
        for label, password in [("empty", ""), ("wrong", "incorrect")]:
            try:
                with pikepdf.open(path, password=password):
                    observed[f"{label}_password_rejected"] = False
            except pikepdf.PasswordError:
                observed[f"{label}_password_rejected"] = True
    with pikepdf.open(path, password=expected.get("user_password", "")) as document:
        observed.update({"page_count": len(document.pages), "encrypted": document.is_encrypted,
                         "syntax_issues": document.check_pdf_syntax(), "page_geometry": []})
        if expected["encrypted"]:
            observed["user_password_accepted"] = True
        annotations, images = [], {}
        for number, page in enumerate(document.pages, start=1):
            box = [float(value) for value in page.obj["/MediaBox"]]
            width, height = box[2] - box[0], box[3] - box[1]
            rotation = int(page.obj.get("/Rotate", 0))
            observed["page_geometry"].append({
                "media_size": [width, height], "rotation": rotation,
                "displayed_size": [height, width] if rotation in (90, 270) else [width, height],
            })
            annotations.extend(page.obj.get("/Annots", []))
            if "image_count_by_page" in expected:
                images[str(number)] = len(page.get_images())
        observed["annotation_types"] = sorted({
            str(item["/Subtype"]).removeprefix("/") for item in annotations
            if str(item["/Subtype"]) not in ("/Popup", "/Widget", "/Link")
        })
        observed["note_contents"] = [str(item["/Contents"]) for item in annotations if "/Contents" in item]
        if "/AcroForm" in document.Root:
            observed["fields"] = {
                str(field["/T"]): {"type": str(field["/FT"]).removeprefix("/"), "value": str(field["/V"]).removeprefix("/")}
                for field in document.Root.AcroForm.Fields
            }
            observed["field_appearances_present"] = all("/AP" in field for field in document.Root.AcroForm.Fields)
        else:
            observed["fields"] = {}
        if images:
            observed["image_count_by_page"] = images
        return observed


def pdfium_observations(path: Path, expected: dict) -> dict:
    observed = {}
    if expected["encrypted"]:
        for label, password in [("empty", None), ("wrong", "incorrect")]:
            try:
                with pdfium.PdfDocument(path, password=password):
                    observed[f"{label}_password_rejected"] = False
            except pdfium.PdfiumError as error:
                observed[f"{label}_password_rejected"] = error.err_code == pdfium_raw.FPDF_ERR_PASSWORD
    with pdfium.PdfDocument(path, password=expected.get("user_password")) as document:
        document.init_forms()
        observed.update({"page_count": len(document), "page_geometry": [], "renders": []})
        if expected["encrypted"]:
            observed["user_password_accepted"] = True
        texts, images, text_objects = {}, {}, {}
        for index in range(len(document)):
            number = index + 1
            with closing(document[index]) as page:
                box = page.get_mediabox()
                observed["page_geometry"].append({
                    "media_size": [box[2] - box[0], box[3] - box[1]],
                    "rotation": page.get_rotation(), "displayed_size": list(page.get_size()),
                })
                with closing(page.get_textpage()) as textpage:
                    texts[number] = textpage.get_text_bounded()
                    if "column_regions" in expected and number == 1:
                        regions = expected["column_regions"]
                        left = textpage.get_text_bounded(left=0, right=regions["left_max_x"])
                        right = textpage.get_text_bounded(left=regions["right_min_x"], right=page.get_width())
                        observed["column_region_text"] = {"left": left, "right": right}
                        observed["columns_separated"] = (
                            regions["left_marker"] in left and regions["right_marker"] not in left
                            and regions["right_marker"] in right and regions["left_marker"] not in right
                        )
                if "image_count_by_page" in expected:
                    images[str(number)] = len(list(page.get_objects(filter=[pdfium_raw.FPDF_PAGEOBJ_IMAGE])))
                    text_objects[str(number)] = len(list(page.get_objects(filter=[pdfium_raw.FPDF_PAGEOBJ_TEXT])))
                if number in expected["render_pages"]:
                    with closing(page.render(scale=RENDER_SCALE, grayscale=True, draw_annots=True)) as bitmap:
                        image = bitmap.to_pil()
                        observed["renders"].append(render_observation(number, image.width, image.height, image.tobytes()))
        observed.update(text_observations(texts, expected))
        if images:
            observed["image_count_by_page"] = images
            observed["text_object_count_by_page"] = text_objects
        if "outlines" in expected:
            observed["outlines"] = []
            for bookmark in document.get_toc():
                destination = bookmark.get_dest()
                index = destination.get_index() if destination else None
                observed["outlines"].append({"level": bookmark.level + 1, "title": bookmark.get_title(), "page": index + 1 if index is not None else None})
        return observed


def pdf_checks(observed: dict, expected: dict) -> tuple[list[dict], list[str]]:
    checks, covered = [], set()

    def equal(name: str, actual, wanted, key: str | None = None) -> None:
        checks.append({"property": name, "expected": wanted, "actual": actual, "passed": actual == wanted})
        covered.add(key or name)

    for name in ("page_count", "encrypted", "page_geometry", "outlines", "internal_links", "annotation_types", "fields", "image_count_by_page", "text_order"):
        if name in expected and name in observed:
            equal(name, observed[name], expected[name])
    if "syntax_issues" in observed:
        equal("syntax_issues", observed["syntax_issues"], [])
    if "text_layer_by_page" in observed:
        for page, present in observed["text_layer_by_page"].items():
            equal(f"text_layer:page={page}", present, expected["text_layer"], "text_layer")
        for marker in observed["text_markers"]:
            equal(f"text_marker:page={marker['page']}:{marker['text']}", marker["found"], True, "text_by_page")
    if "columns_separated" in observed:
        equal("column_regions", observed["columns_separated"], True)
    if "renders" in observed:
        equal("render_pages", [item["page"] for item in observed["renders"]], expected["render_pages"])
        for render in observed["renders"]:
            equal(f"nonblank_render:page={render['page']}", render["nonblank"], True, "render_pages")
    if "note_contents" in expected and "note_contents" in observed:
        equal("note_contents", expected["note_contents"] in observed["note_contents"], True)
    if "fields" in expected and "field_appearances_present" in observed:
        equal("field_appearances_present", observed["field_appearances_present"], True, "fields")
    if expected["encrypted"]:
        for name in ("empty_password_rejected", "wrong_password_rejected", "user_password_accepted"):
            if name in observed:
                equal(name, observed[name], True, "user_password")
    if "embedded_font_sha256s" in observed:
        equal("embedded_font_sha256", expected["embedded_font_sha256"] in observed["embedded_font_sha256s"], True)
    if "attachment_sha256s" in observed:
        attachment = expected["font_license_attachment"]
        equal("font_license_attachment", observed["attachment_sha256s"].get(attachment["name"]), [attachment["sha256"]])
    if expected["text_layer"] is False and "text_object_count_by_page" in observed:
        equal("text_objects_absent", all(value == 0 for value in observed["text_object_count_by_page"].values()), True, "text_layer")
    return checks, sorted(set(expected) - covered)


def epub_container_observations(path: Path, expected: dict) -> dict:
    ns = {"opf": "http://www.idpf.org/2007/opf", "c": "urn:oasis:names:tc:opendocument:xmlns:container", "x": "http://www.w3.org/1999/xhtml"}
    with zipfile.ZipFile(path) as archive:
        first = archive.infolist()[0]
        container = ET.fromstring(archive.read("META-INF/container.xml"))
        package_path = container.find("c:rootfiles/c:rootfile", ns).attrib["full-path"]
        prefix = PurePosixPath(package_path).parent
        package = ET.fromstring(archive.read(package_path))
        items = {item.attrib["id"]: item.attrib for item in package.findall("opf:manifest/opf:item", ns)}
        spine = [item.attrib["idref"] for item in package.findall("opf:spine/opf:itemref", ns)]
        nav_item = next(item for item in items.values() if "nav" in item.get("properties", "").split())
        nav = ET.fromstring(archive.read(str(prefix / nav_item["href"])))
        links = [link.attrib["href"] for link in nav.findall(".//x:nav/x:ol/x:li/x:a", ns)]
        targets = []
        for link in links:
            filename, anchor = link.split("#", 1)
            chapter = ET.fromstring(archive.read(str(prefix / filename)))
            targets.append(any(node.attrib.get("id") == anchor for node in chapter.iter()))
        chapters = [ET.fromstring(archive.read(str(prefix / items[item]["href"]))) for item in spine]
        text = "\n".join(" ".join(chapter.itertext()) for chapter in chapters)
        return {
            "mimetype_first": first.filename == "mimetype",
            "mimetype_uncompressed": first.compress_type == zipfile.ZIP_STORED,
            "mimetype": archive.read("mimetype").decode("ascii"),
            "crc_error_member": archive.testzip(), "spine_ids": spine, "nav_links": links,
            "nav_targets_resolve": all(targets),
            "text_markers": {marker: marker in text for marker in expected["text_markers"]},
        }


def epub_mupdf_observations(path: Path, expected: dict) -> dict:
    with pymupdf.open(path) as document:
        text = "\n".join(page.get_text() for page in document)
        return {"page_count_at_default_layout": len(document),
                "text_markers": {marker: marker in text for marker in expected["text_markers"]},
                "outlines_at_default_layout": document.get_toc()}


def epub_checks(observed: dict, expected: dict) -> tuple[list[dict], list[str]]:
    checks = []
    wanted = {"mimetype_first": True, "mimetype_uncompressed": True,
              "mimetype": "application/epub+zip", "crc_error_member": None,
              "nav_targets_resolve": True, "spine_ids": expected["spine_ids"],
              "nav_links": expected["nav_links"],
              "text_markers": {marker: True for marker in expected["text_markers"]}}
    for name, value in wanted.items():
        if name in observed:
            checks.append({"property": name, "expected": value, "actual": observed[name], "passed": observed[name] == value})
    covered = {check["property"] for check in checks}
    return checks, sorted(set(expected) - covered)


def check_corpus(fixtures: Path) -> dict:
    manifest_bytes = (fixtures / "manifest.json").read_bytes()
    manifest = json.loads(manifest_bytes)
    if manifest["schema_version"] != 1:
        raise ValueError("Unsupported fixture manifest schema")
    versions = {name: version(name) for name in ("pypdf", "PyMuPDF", "pikepdf", "pypdfium2")}
    versions["stdlib"] = platform.python_version()
    results = []
    for entry in manifest["fixtures"]:
        result = {"fixture_id": entry["id"], "path": entry["path"], "expected_sha256": entry["sha256"], "engines": {}}
        path = fixtures / entry["path"]
        if not path.resolve().is_relative_to(fixtures.resolve()):
            result.update({"status": "fail", "error": "Fixture path is outside the corpus"})
            results.append(result)
            continue
        try:
            content = path.read_bytes()
        except OSError as error:
            result.update({"status": "fail", "error": type(error).__name__})
            results.append(result)
            continue
        result.update({"observed_sha256": sha256(content), "sha256_matches": sha256(content) == entry["sha256"],
                       "size_bytes": len(content), "size_matches": len(content) == entry["size_bytes"]})
        if entry["media_type"] == "application/pdf":
            inspectors = {"pypdf": pypdf_observations, "PyMuPDF": mupdf_observations, "pikepdf": qpdf_observations, "pypdfium2": pdfium_observations}
            compare = pdf_checks
        elif entry["media_type"] == "application/epub+zip":
            inspectors = {"stdlib": epub_container_observations, "PyMuPDF": epub_mupdf_observations}
            compare = epub_checks
        else:
            result.update({"status": "fail", "error": "Unsupported media type"})
            results.append(result)
            continue
        for name, inspect in inspectors.items():
            engine = {"version": versions[name]}
            try:
                observed = inspect(path, entry["expected"])
                checks, unchecked = compare(observed, entry["expected"])
                engine.update({"observed": observed, "checks": checks, "unchecked_expectations": unchecked,
                               "status": "pass" if checks and all(check["passed"] for check in checks) else "fail"})
            except Exception as error:
                engine.update({"status": "fail", "error": {"type": type(error).__name__, "message": str(error).replace(str(path), entry["path"])}})
            result["engines"][name] = engine
        passed = result["sha256_matches"] and result["size_matches"] and all(engine["status"] == "pass" for engine in result["engines"].values())
        result["status"] = "pass" if passed else "fail"
        results.append(result)
    return {
        "schema_version": 1,
        "evidence_type": "reference-engine-check",
        "moon_reader_tested": False,
        "observed_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_url": "https://github.com/chirag127/reader-improvement-lab",
        "manifest_sha256": sha256(manifest_bytes),
        "checker_sha256": sha256(Path(__file__).read_bytes()),
        "environment": {"python": platform.python_version(), "system": platform.system(), "machine": platform.machine(),
                        "libraries": versions, "MuPDF": ".".join(map(str, pymupdf.mupdf_version_tuple)),
                        "PDFium": str(pdfium.PDFIUM_INFO), "qpdf": pikepdf.__libqpdf_version__},
        "method": {"text": "All PDF pages extracted by pypdf, MuPDF and PDFium; counts and literal anchor matches retained.",
                   "render": "MuPDF and PDFium grayscale at 36 dpi; listed pages only; annotations and forms enabled; nonblank extrema check.",
                   "syntax": "pikepdf check_pdf_syntax, not a full PDF conformance validator.",
                   "epub": "ZIP CRC, XML container/spine/nav targets, plus independent MuPDF chapter text extraction."},
        "limitations": [
            "No Android or proprietary reader application was tested by this command.",
            "Engine pass covers only its listed checks; unchecked_expectations names the remaining manifest keys.",
            "Nonblank rasters do not establish visual fidelity or cross-engine pixel equivalence.",
            "Long-document rendering samples pages 1, 50 and 100; all 100 pages are counted and text-extracted.",
            "No timing, memory, OCR, form-edit persistence, annotation round-trip, accessibility, PDF/A, PDF/UA or full EPUB conformance evaluation.",
            "The public owner password and encryption algorithm description are not separate assertions; authentication uses the public user password.",
        ],
        "summary": {"fixtures_passed": sum(result["status"] == "pass" for result in results),
                    "fixtures_failed": sum(result["status"] == "fail" for result in results),
                    "engine_checks_passed": sum(engine["status"] == "pass" for result in results for engine in result["engines"].values()),
                    "engine_checks_failed": sum(engine["status"] == "fail" for result in results for engine in result["engines"].values())},
        "results": results,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixtures", type=Path, default=ROOT / "fixtures")
    parser.add_argument("--output", type=Path, help="Save structured observations; stdout is always a compact summary.")
    arguments = parser.parse_args()
    report = check_corpus(arguments.fixtures)
    if arguments.output:
        arguments.output.parent.mkdir(parents=True, exist_ok=True)
        arguments.output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"evidence_type": report["evidence_type"], "moon_reader_tested": False, **report["summary"]}, indent=2))
    for result in report["results"]:
        if result["status"] == "fail":
            print(json.dumps(result, ensure_ascii=False), file=sys.stderr)
    return 1 if report["summary"]["fixtures_failed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
