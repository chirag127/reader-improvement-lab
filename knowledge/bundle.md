---
type: Bundle
title: Reader Improvement Lab
description: A self-contained open-knowledge research bundle connecting reader capabilities, source observations, test evidence, and actionable proposals.
resource: https://github.com/chirag127/reader-improvement-lab
tags: [readers, open-knowledge, pdf, epub, reproducibility]
timestamp: 2026-11-21T00:00:00Z
---

# Reader Improvement Lab knowledge bundle

This bundle is the canonical public record of the investigation. Start at the
[knowledge index](index.md) or [repository overview](../README.md). Its Markdown
notes carry YAML metadata; JSON records and openly licensed synthetic inputs make
the evidence reusable outside this repository.

## Layout

| Location | Role |
|---|---|
| `knowledge/` | Human-readable findings, interpretation, comparison, test specifications, and reporting instructions |
| `data/` | Structured product identities, source revisions, proposals, and contribution records |
| `evidence/` | Curated diagnostic excerpts and execution receipts with their limitations |
| `fixtures/` | Original PDF, EPUB, and scenario inputs, expected properties, hashes, and dependency/license records |
| `scripts/` and `tests/` | Reproducible generation and verification tooling |

## Stable references

- `MF-*` identifies the [official Moon baseline](../data/moon-baseline.json).
- `APK-*` identifies [supplied-artifact static observations](../evidence/static/observations.json).
- `REA-*` identifies [focused follow-up observations](../evidence/static/rea-followup.json); the [developer digest](rea-followup.md) explains their static and runtime boundaries.
- `MOON-001`–`MOON-064` identifies the [original proposals](moon-improvements.md), whose detailed requirements are canonical in [the original JSON backlog](../data/moon-improvements.json). `MOON-065`–`MOON-074` identifies [ten additional workflows](moon-followup-proposals.md), with requirements in [the supplement](../data/moon-followup-proposals.json). Together they contain 74 drafts and 220 prospective criteria.
- `ALT-*` identifies alternative-reader proposals. Each record names its target
  application and supporting sources; proposed acceptance checks are future work.
- `RT-*` identifies [application test specifications](testing-plan.md). The
  [runtime report](runtime-results.md) and [case records](../data/runtime-results.json)
  identify which portions actually ran and their outcomes.
- `RUNTIME-PDF-PREV-001` identifies the [repeated saved-form interoperability
  failure](runtime-results.md#repeated-saved-form-interoperability-failure).
  `AUX-*` observations have separate scope and do not add canonical case passes.
- Fixture IDs resolve through the [core manifest](../fixtures/manifest.json) or
  [scenario manifest](../data/scenario-fixtures.json). SHA-256 identifies the exact
  input bytes; modified outputs need their own identity.

The [methodology](methodology.md) defines evidence strength. The [coverage
ledger](coverage.md) records remaining work. Original observations cite exact
upstream commits or artifact hashes and an observation date; external documentation
retains its publication/version qualifications where known.

## Reuse and attribution

Original analysis, fixtures, and investigation tooling use the repository's
[MIT license](../LICENSE). Third-party font notices and contribution licenses
remain with their materials. Product names identify the examined software and
do not imply developer endorsement. Public-source permalinks identify examined
code; a repository link does not certify that a store binary matches it.

Private raw analysis is represented by digest receipts where appropriate. Such a
receipt is an identity reference, not a publicly downloadable source file or an
independent verification of the withheld content. The [supplied APK identity](../data/artifact.json)
also retains its unresolved distribution provenance.

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
