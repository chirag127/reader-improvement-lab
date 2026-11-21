---
type: Reference
title: Synthetic inputs for literal search, long speech, and malformed-document recovery
description: Original scenario inputs for RT-12, RT-29, and RT-36 with exact bytes, host readback, and explicit application-test boundaries.
tags: [readers, fixtures, scenarios, search, tts, robustness]
timestamp: 2026-11-21T00:00:00Z
---

# RT-12, RT-29, and RT-36 scenario inputs

These seven small, original inputs supplement the [runtime test plan](testing-plan.md).
Use the [scenario manifest](../data/scenario-fixtures.json) to identify the exact
bytes and expected document properties. The [verification record](../evidence/scenario-fixture-verification.json)
contains host-library observations and executable test output. Neither file is a
Moon+ Reader test result.

Observed on 2026-11-21: all **eight scenario integration tests passed**. All four
host PDF libraries opened both healthy PDFs, rejected all three malformed inputs,
and opened the healthy control after each rejection. Those are eight healthy
file/engine pairs and twelve rejection/reopen pairs. Two fresh generations also
matched the retained inputs and manifest byte for byte.

The combined discovery run passed **25 tests**: the 17 retained corpus tests and
these eight scenario tests. Its exact output is retained in the verification record.

## Inputs and runtime handoff

All paths in the table are relative to `fixtures/scenarios/`. Recipe revision 1
contains seven files totaling 18,603 bytes.

| Scenario | Input | What to exercise |
|---|---|---|
| RT-12 | `rt12-literal-search.txt` | UTF-8, LF-only text with literal queries and separately labeled negative controls |
| RT-12 | `rt12-literal-search.pdf` | A one-page selectable-text version of the same search rows |
| RT-29 | `rt29-long-paragraph.txt` | One long paragraph without newline or sentence-ending punctuation, with unique beginning/middle/suffix markers |
| RT-36 | `rt36-healthy-control.pdf` | A one-page healthy control to open before and after each malformed input |
| RT-36 | `rt36-empty.pdf` | Exactly zero bytes |
| RT-36 | `rt36-truncated.pdf` | Exactly the first 64 bytes of the new healthy control |
| RT-36 | `rt36-invalid-header.pdf` | Original plain text saved with a `.pdf` extension; no PDF header |

### RT-12: literal search

In **literal** mode, query `a.b` should identify only row `S01`, `a+b` only `S02`,
and `[x]` only `S03`. Each literal occurs once in each input. Negative control rows
contain `axb`, `aaab`, `x`, `ab`, and `a-b`; these make accidental regular-expression
interpretation distinguishable from literal matching. The manifest records the
query/row mapping. Record the app's case, whole-word, and search-mode settings.

An invalid regex is a separate runtime action, appropriate only if the application
offers regex mode or interprets that syntax. The fixture supplies data; host text
extraction does not establish application search behavior or error recovery.

### RT-29: long speech input

The unique markers are `RT29-BEGIN-173`, `RT29-MIDDLE-509`, and `RT29-SUFFIX-947`.
The paragraph is 14,446 Unicode code points / UTF-16 code units, with markers at
zero-based offsets 0, 7,215, and 14,431. The manifest records those lengths and
offsets. The text uses ASCII so offsets do not depend on surrogate pairs.
It has no newline and no `.`, `!`, or `?` sentence terminator; there is no hidden
paragraph boundary at the middle marker.

The **actual Android speech-input limit is unknown**. A 4,000-code-unit value is
only a sizing reference for this synthetic input, not a measured engine limit.
The runtime owner must record the platform limit, selected engine/version/voice,
and accepted utterance lengths. Capture submitted segments and audible or logged
marker progression before deciding whether any suffix is lost. No speech engine
is invoked by this fixture tooling.

### RT-36: malformed documents and healthy recovery

Open the healthy control first, then each malformed input independently. Record
the application's actual diagnostics, exit/crash behavior, and ability to reopen
the healthy control (`RT36-HEALTHY-621`). The empty file may be rejected by a file
picker or document provider before the reader opens it; record that layer rather
than treating it as a reader-parser result.

These are simple malformed bytes, with no scripts, exploit structures, embedded
files, or external actions. Intentional parser rejection is an expected host
observation, not an application defect. The host tests instantiate a fresh parser
for the subsequent healthy open in the same Python process; this does not prove
application UI recovery or reuse of a failed native document handle.

## Origin, dependencies, and reproduction

All prose and document geometry were authored for this repository and inherit its
[MIT license](../LICENSE). ReportLab creates the two healthy PDFs using its built-in
standard PDF fonts. No proprietary sample, user document, downloaded book, or new
font asset is included. The malformed inputs are derived only from the new healthy
control or original plain text.

The generator and tests reuse Python 3.13 and the
[already recorded toolchain](../fixtures/requirements.txt). No dependencies were
installed for this scenario task. The generator needs ReportLab; independent
readback uses pypdf, PyMuPDF/MuPDF, pikepdf/qpdf, and pypdfium2/PDFium.

Run from the repository root with the intended Python interpreter selected:

```sh
python -X utf8 -B tests/test_scenario_fixtures.py --evidence evidence/scenario-fixture-verification.json
python -X utf8 -B -m unittest discover -s tests -v
```

To regenerate in a separate root:

```sh
python -X utf8 -B scripts/generate_scenario_fixtures.py --output-root .local/rebuilt-scenarios
```

The generator writes its seven named files beneath `fixtures/scenarios/` and
`data/scenario-fixtures.json` in that root. Fixed text, ReportLab invariant metadata,
and a recorded generator hash support byte comparisons. The tests compare two
fresh generations and the retained inputs, and check preservation of an existing
corpus sentinel. The artificial PDF metadata epoch is not an observation date.

Byte identity is scoped to the recorded generator and toolchain. The manifest's
hashes identify inputs used by the runtime lane; coordinate a new revision before
replacing any input already exercised. Host readback checks literal content,
nonblank PDF rendering, malformed byte identity, and healthy reopening. It
does not measure reader performance, speech delivery, search results, application
crashes, accessibility, or general PDF conformance.

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
