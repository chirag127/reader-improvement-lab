---
type: Index
title: Reader Improvement Lab knowledge index
description: Entry points into source-backed reader research, reproducible evidence, and developer reporting.
tags: [readers, index, open-knowledge, evidence]
timestamp: 2026-11-21T00:00:00Z
---

# Knowledge index

This is the canonical navigation for the public investigation. Markdown notes explain the findings; JSON records preserve identities, evidence, and reusable proposals. The [bundle description](bundle.md) defines the layout and stable references. See [the repository overview](../README.md) for the current delivery state.

## Research and interpretation

| Note | Purpose | Companion records |
|---|---|---|
| [Methodology](methodology.md) | Claim types, defect threshold, scope, quality attributes | [Investigation design](design.md) |
| [Coverage and remaining evidence](coverage.md) | Question-by-question boundaries and evidence still needed | [Execution plan](plan.md) |
| [Moon official baseline](moon-baseline.md) | Existing features, v10.8 notes, commercial/legacy comparisons, name disambiguation | [Moon baseline](../data/moon-baseline.json) |
| [64 Moon improvement proposals](moon-improvements.md) | Prioritized extensions, conditional reliability candidates and new-workflow ideas | [Detailed backlog and acceptance criteria](../data/moon-improvements.json) |
| [Supplied APK analysis](apk-analysis.md) | Package structure, focused implementation paths, conditional defect candidates | [Artifact identity](../data/artifact.json), [structure](../data/apk-structure.json), [observations](../evidence/static/observations.json) |
| [Bug-report candidates](bug-candidates.md) | Six concrete reproduction protocols and evidence required before official-build attribution | References the static finding ledger and application test IDs |
| [Android and cross-platform alternatives](alternatives-android.md) | Eight public repositories, feature dossiers, six targeted application-code reviews | [Inventory](../data/alternatives-android.json), [21 proposals](../data/alternative-proposals-android.json) |
| [Desktop and web alternatives](alternatives-desktop-web.md) | Ten adjacent readers/libraries and four targeted implementation reviews | [Inventory](../data/alternatives-desktop-web.json), [13 proposals](../data/alternative-proposals-desktop-web.json) |
| [Feature comparison](feature-matrix.md) | Workflow-level comparison, code boundaries, and limits on parity claims | Uses the pinned sources in the baseline and alternative dossiers |
| [Fixture guide](testing-fixtures.md) | Original PDF/EPUB corpus, expected properties, host verification | [Manifest](../fixtures/manifest.json), [reference results](../fixtures/reference-results.json), [execution record](../evidence/fixture-verification.json) |
| [Additional scenario inputs](testing-scenarios.md) | Literal-search controls, long speech text and simple malformed PDFs | [Scenario manifest](../data/scenario-fixtures.json), [host verification](../evidence/scenario-fixture-verification.json) |
| [Application test matrix](testing-plan.md) | 36 specified workflows and the evidence needed to record an application result | Specifications; actual execution is recorded in [runtime results](runtime-results.md) |
| [Android runtime results](runtime-results.md) | 3 pass, 6 partial, 1 fail, 7 blocked, 19 not-run; sample-specific saved-form failure | [Case records](../data/runtime-results.json), [evidence manifest](../evidence/runtime/manifest.json), [cleanup](../evidence/runtime/cleanup.json) |
| [Reporting guide](reporting.md) | Verified contacts, duplicate checks, and unsent templates | [Repository issue forms](../.github/ISSUE_TEMPLATE/) |
| [Corpus validation](validation.md) | Offline record, citation, hash and publication checks | [Validator](../scripts/validate_repository.py), [regression tests](../tests/test_repository_validation.py) |

## Implemented contributions

| Contribution | Delivered evidence | Remaining boundary |
|---|---|---|
| [KOReader CBR MIME aliases](contributions-koreader.md) | [Fork commit and execution record](../data/contributions/koreader.json): four expected failures before the fix, then 42 passing host-module tests | Eight internet-tagged cases and device download/rendering tests are outside this run; upstream submission remains separate |
| [MuPDF first-page internal links](contributions-mupdf-android.md) | [Fork commit and execution record](../data/contributions/mupdf-android.json): 15 host tests, five failures before the fix and zero afterward; debug APKs assembled and source pushed to fork | JNI is substituted; application/device A/B not run and contribution not submitted upstream |

## Verification receipts

- [Android signature verification](../evidence/apk-signature-verification.txt) and [manifest excerpt](../evidence/apk-badging-excerpt.txt).
- [Static-analysis tool provenance](../evidence/static/provenance.json), [initial saved-evidence checks](../evidence/static/verification.json), and [bounded follow-up verification](../evidence/static/bounded-followup-verification.json). The initial verification describes its historical inputs; the follow-up records the updated evidence and interrupted-run limits.
- [Fixture integration tests](../tests/test_fixtures.py), [generator](../scripts/generate_fixtures.py), and [reference checker](../scripts/check_fixtures.py).
- [Final combined host-suite receipt](../evidence/host-suite-verification.json): 68 passing tests, with input identities and the retained execution outcome.
- [Independent validator review and resolutions](../evidence/reviews/repository-validator.json): malformed records, filesystem boundaries, contribution references, and runtime evidence binding.
- [Runtime delivery verification](../evidence/runtime/verification.json) and [independent runtime-claim review](../evidence/reviews/runtime-claims.json). These verify retained evidence; they add no application executions.
- [Execution plan](plan.md): the work ledger distinguishes completed deliverables from remaining validation and publication steps.

## Knowledge conventions

Every material conclusion needs a source, observation date, evidence type, and limitation. Source-code claims name the inspected commit; local APK claims name its SHA-256. Runtime claims additionally require the environment, fixture, actions, and actual result. Recommendation priority describes expected user benefit, not the severity of a proven defect.

This repository is an independent corpus. Public-source links and product names identify evidence; they do not imply endorsement, issue submission, or completion of every planned test.

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
