---
type: Status
title: Investigation coverage and remaining evidence
description: Which reader questions are answered by documentation, static analysis, fixture verification, and application testing.
tags: [readers, coverage, verification, limitations]
timestamp: 2026-11-21T00:00:00Z
---

# Investigation coverage

This page distinguishes completed evidence from the broader work requested. The corpus is a dated investigation of a named set of products; it is not an exhaustive census of PDF readers or a certification of every feature.

## Questions and evidence

| Requested question | Evidence obtained | Status and boundary |
|---|---|---|
| Which alternative repositories are relevant? | Eight [Android/cross-platform projects](../data/alternatives-android.json), ten [desktop/web projects](../data/alternatives-desktop-web.json), and seven [commercial/legacy families](../data/commercial-alternatives.json): 25 named alternatives. | Answered for the named inventory. The phrase “Reader Pro” remains ambiguous; candidates are [identified](moon-baseline.md#resolving-the-name-reader-pro). |
| What does Moon already offer? | Twenty-one [official baseline entries](moon-baseline.md#existing-capability-baseline), including the documented DRM limitation, plus the observed v10.8 release notes. | Documentation-backed. Advertisement is not a runtime pass. |
| What is the supplied APK's structure? | Five DEX files, 24 native-library members across four ABIs, 25 manifest components, and a 12,959-row top-level class-name inventory; 21 focused class summaries and 52 evidenced method requests yielding 51 bodies and one unresolved selector. | [Static analysis and bounded follow-up integrated](apk-analysis.md). Of the returned bodies, 49 have finalized run receipts and two were recovered from interrupted run E. Native internals and a complete call graph remain unexamined; loader/class-list totals have different scopes. |
| Are there potentially non-working features? | Six focused candidates in the [static analysis](apk-analysis.md#focused-verification-candidates), plus two retained form outputs with `/Prev -1` in the [runtime report](runtime-results.md#repeated-saved-form-interoperability-failure). | The static candidates need their stated execution checks. The saved-form interoperability failure was observed twice on the unknown-origin sample; official-build attribution and the precise implementation cause remain unverified. |
| How does the alternative code compare? | Six [Android/cross-platform application-code reviews](alternatives-android.md#4-reviewed-code-and-extension-seams) and four [desktop/web implementation reviews](alternatives-desktop-web.md#3-four-pinned-implementation-reviews-and-contribution-candidates), with exact files and revisions. | Ten targeted implementation reviews. The other eight public-source projects received documentation/license/build inspection, not whole-codebase review. |
| What can be tested reproducibly? | Eleven [core inputs](testing-fixtures.md) plus seven [scenario inputs](testing-scenarios.md), with hashes and expectations, four PDF libraries, two rendering engines, and EPUB packaging checks. | The core run passed 17 tests, 42 fixture/engine pairs, and 590 property comparisons. The combined run passed 25 tests, including eight scenario tests. These are host checks, not application-test counts. |
| What should developers improve? | [64 Moon proposals](moon-improvements.md), twenty-one [Android alternative proposals](../data/alternative-proposals-android.json), and thirteen [desktop/web proposals](../data/alternative-proposals-desktop-web.json), with acceptance criteria and sources. | 98 draft proposals in total, including 64 specifically for Moon. Current availability, actual failure and upstream submission are separate questions. |
| Has the Android app been thoroughly exercised? | [Bounded runtime evidence](runtime-results.md): 3 pass, 6 partial, 1 fail, 7 blocked, and 19 not-run among 36 specified cases. Nine canonical PDFs were opened; the independent legacy-core note observation uses a different input. | Ten cases were exercised at least in part, not a full application certification. Scenario application tests, EPUB/reflow, many lifecycle/export workflows, and comparative performance remain unexecuted. The selected emulator and private ADB were stopped. |
| Have alternative applications been improved? | The [KOReader CBR-MIME fix](contributions-koreader.md) and [MuPDF first-page-link fix](contributions-mupdf-android.md) are implemented, host-tested and published to their forks. | KOReader: 42 selected tests passed after four baseline failures. MuPDF: 15 host tests passed after five baseline failures. Application/device A/B, full CI and upstream submission were not performed. |
| How can reports reach the Moon developer? | Official support and privacy contacts, duplicate-search guidance, and unsent templates. | [Reporting guide completed](reporting.md). No particular response time or feature-delivery commitment is established. |

## Evidence needed for stronger claims

- **Official-build attribution:** reproduce on an APK acquired from the user's official installation and record that acquisition and its signature. Matching package/version text does not authenticate a binary. The [supplied sample](../data/artifact.json) fails the recorded default signature-verification command.
- **Application reliability:** exercise open, modify, save, close, and reopen; inspect the durable output. A success toast, source branch, or host-parser success alone is insufficient.
- **Complete the retained matrix:** the [per-case ledger](runtime-results.md#complete-canonical-coverage) identifies unfinished actions, including the remaining steps in partial cases. The historical test specification lists four outcome names; the final result contract additionally defines **partial** for successful subsets with explicitly unexecuted steps. Its case acceptance criteria remain unchanged.
- **Cloud correctness:** use two explicitly selected test installations and disposable cloud documents. Verify position, annotations, deletions, conflicts, and retries separately. No account credentials are needed for the offline work completed so far.
- **Performance:** measure first-readable-page latency, memory, and long-session behavior on comparable hardware, settings, documents, and sample counts. No cross-app speed or battery ranking is claimed.
- **Accessibility:** test task completion with TalkBack, keyboard, large system text, and appropriate assistive settings. TTS support and marketing claims do not establish screen-reader accessibility.
- **Broader compatibility:** AES-encrypted, damaged, tagged PDF/UA, RTL/CJK, complex shaping, very large scans, other Android API levels, physical devices, and e-ink devices need additional inputs and runs. The first fixture corpus deliberately records its narrower scope.

The evidence contract in [Methodology](methodology.md) applies to each later result. A newly completed run changes only the questions it actually tested.

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
