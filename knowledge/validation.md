---
type: Guide
title: Validate and maintain the research corpus
description: Offline checks for reader identities, proposal records, citations, fixture hashes, and publication boundaries.
tags: [readers, validation, evidence, maintenance]
timestamp: 2026-11-21T00:00:00Z
---

# Corpus validation

The [repository validator](../scripts/validate_repository.py) checks the public
research files without installing or running a reader. Its JSON result reports
the exact errors and counts it inspected; `application_tests_executed` is always
`false`. A successful corpus check is distinct from the application results in
the [coverage ledger](coverage.md).

## Run the checks

From the repository root, the corpus validator uses Python's standard library and Git to inventory tracked files and unignored additions. A source archive without `.git` uses the documented filesystem exclusions:

```sh
python -X utf8 -B scripts/validate_repository.py --output .local/repository-validation.json
```

Exit `0` means no implemented validation check failed; exit `1` means a recorded
validation error. Inspect `status`: **pending** specifically means the runtime
ledger is absent, while **pass** means the present records satisfy the implemented
contracts. Even a complete ledger of unexecuted cases is only a record-validation
pass. `--root` selects another corpus directory; `--json` explicitly selects the
already-default JSON format.

In-repository output is restricted to `.local/`; an explicitly selected external
receipt path is also supported. Public-input collisions, hardlink aliases, and
symlink/junction output paths are rejected. Receipt replacement uses a temporary
file and atomic rename. The `.local/` receipt is excluded from the next public-file
inventory.

The [validator regression tests](../tests/test_repository_validation.py) exercise
small original records and deliberate corruptions. Run the entire host suite with
the [fixture dependencies](../fixtures/requirements.txt) installed:

```sh
python -X utf8 -B -m unittest discover -s tests -v
```

The fixture tests use independent PDF libraries; the validator tests inspect
validation outcomes. Neither command starts an Android emulator or submits a
developer report. Refer to [fixture verification](testing-fixtures.md) and
[scenario inputs](testing-scenarios.md) for their separate evidence boundaries.

The [retained final suite](../evidence/host-suite-verification.json) passed **68
tests**: 17 core-fixture, eight scenario, and 43 validator cases. It includes
malformed current receipts, NTFS-junction read/output boundaries, input-preserving
output handling, contribution identities, publication inventory, provenance fields,
and runtime-record consistency. The [independent review](../evidence/reviews/repository-validator.json)
records the original findings and their scoped resolutions.

## Contracts checked

- Required entry documents and the one-line `CLAUDE.md` adapter.
- JSON syntax, duplicate member names, and required record fields.
- Full source revisions for open-source alternatives and consistent supplied-APK
  identity across artifact records.
- Unique application/proposal/contribution IDs, known targets and baseline references, source
  references, nonempty acceptance criteria, and draft-proposal classifications.
- At least fifty Moon proposals, with normalized duplicate titles/outcomes rejected.
  Semantic distinctness still needs content review.
- Local Markdown inline/reference links, named anchors, ATX/setext heading anchors,
  duplicate HTML IDs/reference definitions, and source-line ranges. Fenced examples are
  excluded from rendered-link checks.
- Fixture file hashes/sizes and selected current evidence-input hashes. The
  original static verification remains a historical snapshot when the bounded
  follow-up receipt supplies current input hashes.
- Recognized public JSON references, declared dates/classifications/digest syntax,
  contribution publication-commit agreement, and host/application evidence boundaries.
- Runtime case IDs, status/subcheck consistency, summary arithmetic, canonical
  fixture identities, evidence-file hashes, and cleanup-summary/receipt agreement.
  Every retained case, subcheck and auxiliary evidence citation must resolve to a
  successfully hashed manifest file. External citations belong in `source_url`.
- Public-file extensions, raw-configuration/bulk-decompilation paths, symlink and
  junction boundaries, and bounded credential/local-user-path markers.

## Interpretation and maintenance

An external URL's syntax is checked, not its current availability or truth. The
Markdown reader covers this corpus's conventions, not every CommonMark extension.
Hash agreement establishes byte identity, not the accuracy of private analysis or
the correctness of a reader. In a Git checkout, the scanner checks current working
bytes for tracked files and unignored additions; it rejects private/build files
that are publication candidates and links to excluded files. It does not read
staged blobs, so the actual staged inventory and bytes still need a publication check.
Existing filesystem aliases are rejected; protection against concurrent malicious
filesystem mutation is outside this offline tool's scope. The historical runtime
test specification is hash-bound; its original four-name outcome list is clarified
by the five-state [runtime result contract](runtime-results.md#evidence-and-counting),
which explicitly defines partial execution.

When a finding changes, retain its earlier assessment where material, update its
source/limitations, and rerun affected checks. Keep source documentation,
static observations, host regression results, application workflows, and draft
acceptance criteria distinguishable. See [methodology](methodology.md).

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
