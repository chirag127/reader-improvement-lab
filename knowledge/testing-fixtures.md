---
type: Reference
title: Synthetic reader fixtures and host verification
description: Original redistributable PDF and EPUB inputs, reproducible generation, and the limits of independent host-engine checks.
tags: [readers, fixtures, pdf, epub, testing]
timestamp: 2026-11-21T00:00:00Z
---

# Synthetic reader fixtures

This corpus supplies small, original inputs for repeatable reader investigations.
Its manifest specifies expected document properties. Host-library results establish
those properties only; they do not establish that Moon+ Reader or another reader
application passed a workflow.

- [Expected properties and SHA-256 hashes](../fixtures/manifest.json)
- [Generator](../scripts/generate_fixtures.py)
- [Independent reference checker](../scripts/check_fixtures.py)
- [Integration tests](../tests/test_fixtures.py)
- [Pinned direct dependencies](../fixtures/requirements.txt)
- [Per-engine observations and comparisons](../fixtures/reference-results.json)
- [Execution evidence](../evidence/fixture-verification.json)

Observed on 2026-11-21: **17 integration tests passed**, and all **11 fixtures**
passed their listed checks across **42 fixture/engine pairs**. The execution record
identifies the exact manifest and scripts, command outputs, and corrected host-tool
integration issues. These counts describe fixture tooling, not application tests.

## Origin and redistribution

All prose, vector geometry, and the synthetic scanned page were created for this
repository by `scripts/generate_fixtures.py`. The original content inherits the
repository's [MIT license](../LICENSE). No APK sample documents, personal documents,
or third-party books are included.

The Unicode PDF embeds the full, unmodified Bitstream Vera Sans font bundled with
ReportLab. Its reviewed SHA-256 is
`c4c45690b345435b2cba52ecabe275f05e49b389b39fe68ad03afbb551288d3d`.
The [font permission notice](../fixtures/licenses/bitstream-vera-license.txt) is
preserved beside the corpus and attached as `font-license.txt` inside `unicode.pdf`.
The font's license remains separate from the MIT-licensed original content. The
generator fails explicitly if the bundled font or notice is missing, or if the font
differs from the reviewed hash. The image-only page uses rasterized Vera text; it
has no OCR text layer.

## Expected inputs

The 11 generated documents occupy **168,613 bytes** in recipe revision 1. There are
114 PDF pages in total. Paths below are relative to `fixtures/documents/`.

| Fixture | Pages | Purpose and expected properties |
|---|---:|---|
| `plain-text.pdf` | 1 | Selectable prose, `lighthouse-427` search anchor and a final reading-position anchor |
| `two-columns.pdf` | 1 | Separate left/right regions; `LEFT-01` through `LEFT-03` precede the right column in content-stream order |
| `long-document.pdf` | 100 | Distinct page-number text and stable anchors at pages 1, 50 and 100 |
| `mixed-geometry.pdf` | 4 | Media sizes 612×792, 420×595, 792×612, 300×450 points; rotations 0°, 90°, 180°, 270° |
| `navigation.pdf` | 3 | Start/Middle/End outlines and internal links from page 1 to 3 and from 3 to 1 |
| `annotations.pdf` | 1 | Text note, highlight, underline, strikeout, ink and square; a note popup is an additional PDF object |
| `acroform.pdf` | 1 | Unflattened text, checked checkbox and choice widgets with initial values and appearances |
| `password-protected.pdf` | 1 | Requires public test password `reader-lab`; rejects missing/wrong passwords; legacy RC4-128 revision 3 |
| `scanned-image-only.pdf` | 1 | One visible image, zero extracted text; printed OCR target `SCAN-ANCHOR-846` |
| `unicode.pdf` | 1 | Precomposed Latin accents and selected symbols, full embedded font and embedded font-license notice |
| `tiny-original.epub` | 2 spine chapters | Original story, ordered spine, EPUB 3 navigation, NCX fallback and chapter links |

The password fixture's owner password, `reader-owner-lab`, is public test data too.
It is a deterministic compatibility input, not an example for protecting secrets.
The scanned page's visible OCR target is supplied for future application tests;
the host checker does not perform OCR.

## Reproduce

Use Python 3.13 and the pinned dependencies. The observed environment was Python
3.13.14 on Windows AMD64; all six packages imported successfully before generation.
No additional packages were installed for this lane.

| Python package | Verified version | Underlying engine, where applicable |
|---|---|---|
| ReportLab | 5.0.0 | PDF canvas and AcroForm generation |
| PyMuPDF | 1.28.0 | MuPDF 1.29.0 |
| pypdf | 6.15.0 | Independent Python PDF parser |
| pikepdf | 10.11.0 | qpdf 12.3.2 |
| pypdfium2 | 5.12.1 | PDFium 152.0.7947.0 |
| Pillow | 12.3.0 | Synthetic raster generation and bitmap inspection |

From the repository root, with the intended interpreter selected:

```sh
python -m pip install -r fixtures/requirements.txt
python -X utf8 -B scripts/check_fixtures.py --fixtures fixtures --output fixtures/reference-results.json
python -X utf8 -B -m unittest discover -s tests -v
```

`check_fixtures.py` checks the existing documents without changing them. It emits a
nonzero exit status on a hash, size, engine, or supported-property mismatch. Its
JSON output records observations, literal comparisons, engine versions, and
unchecked expectations per engine.

For regeneration, use a new output directory before replacing any input already
used in a runtime investigation:

```sh
python -X utf8 -B scripts/generate_fixtures.py --output rebuilt-fixtures
```

The generator writes only its named documents, font notice, and manifest. The
repeatability test runs it in two temporary directories and compares every generated
document and the manifests byte for byte. ReportLab invariant metadata, fixed
annotation/attachment/ZIP dates, preserved PDF IDs, and uncompressed EPUB entries
remove wall-clock and directory-path variation. The manifest records the generator
hash and tool versions. The metadata date `2000-01-01` is an artificial fixed epoch,
not a claim about when the corpus was authored or tested.

Byte identity is expected with the recorded generator, font and toolchain; it is
not promised across library, Python, compression, font-rendering, or platform changes.
The requirements file pins direct packages rather than pretending to lock the whole
operating environment. Use manifest hashes to identify existing test inputs.

## What the checks establish

- **pypdf, MuPDF and PDFium:** extract text from every PDF page and check literal
  anchors, text-layer presence and column order where specified.
- **All four PDF libraries:** count pages and inspect geometry. Password handling
  uses the public user password, with empty/wrong-password rejection checks.
- **pypdf and MuPDF:** resolve internal destinations and inspect the font bytes and
  embedded license. PDFium independently inspects outlines.
- **pypdf, MuPDF and qpdf:** inspect standard annotations and initial AcroForm values.
  qpdf also checks initial field appearances and PDF syntax.
- **MuPDF and PDFium:** render 17 selected PDF pages each at 36 dpi and assert nonblank
  grayscale extrema. The long input samples pages 1, 50 and 100; the other inputs
  render all their pages. Pixel hashes are observations, not cross-engine equality
  assertions.
- **Python ZIP/XML and MuPDF:** check EPUB packaging, spine/navigation targets and
  independently extract both chapter markers. This is not an EPUBCheck conformance
  certificate.
- **Integration tests:** reject changed document bytes and deliberately incorrect
  expected page counts, in addition to the document-specific assertions.

The checker reports `unchecked_expectations` so an engine's pass cannot silently
stand in for capabilities it did not inspect. The generator itself uses MuPDF for
some PDFs; pypdf, PDFium and qpdf provide independent readback where relevant.

## Coverage limits

No application UI, Android lifecycle, device storage, performance, memory,
accessibility, PDF/A or PDF/UA conformance is evaluated here. Nonblank rendering
does not establish visual fidelity. Form editing/saving, annotation round trips,
OCR quality, AES encryption, damaged documents, RTL/CJK shaping, emoji and Unicode
normalization are outside this corpus revision. An EPUB's laid-out page count is
renderer-dependent; its two spine chapters are the stable expectation.

During checker development, installed API behavior required explicit closing of
PDFium page/text/bitmap resources and retaining a MuPDF page while using its
annotations. MuPDF exposed `/Fit` links as named-link dictionaries with string page
values; resolving the actual link URI recovered their correct destinations. These
were host-tool integration corrections, not reader-app findings. The generated
document bytes were preserved while correcting the checks.

<footer class="hire-me">
  <h3>Hire me</h3>
  <p>Chirag Singhal: building free, open APIs and tools.</p>
  <p>
    <a href="mailto:chirag@oriz.in">chirag@oriz.in</a> ·
    <a href="https://github.com/chirag127">GitHub</a> ·
    <a href="https://www.linkedin.com/in/chirag127/">LinkedIn</a> ·
    <a href="https://x.com/singhal127">X</a> ·
    <a href="https://www.youtube.com/@ChiragSinghal127">YouTube</a> ·
    <a href="https://www.instagram.com/chiragsinghal127/">Instagram</a> ·
    <a href="https://www.reddit.com/user/Far_Macaron_9910/">Reddit</a> ·
    <a href="https://buymeacoffee.com/chirag127">Buy me a coffee</a>
  </p>
</footer>
