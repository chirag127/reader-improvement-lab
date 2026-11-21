---
type: Methodology
title: Evidence and comparison methodology
description: How to interpret the reader inventory, proposals, code review, and tests.
tags: [evidence, reproducibility, comparison]
timestamp: 2026-11-21T00:00:00Z
---

# Evidence and comparison methodology

## The unit of comparison

A product, a source repository, and a rendering engine are different units. An Android application using MuPDF is not equivalent to every capability in MuPDF. Desktop capabilities are design references, not proof of Android implementation feasibility. A product called “Pro” is not necessarily open source.

The inventory records direct Android alternatives and adjacent desktop/web examples. It is a bounded discovery set, not a claim to enumerate every PDF reader. Source-review depth and runtime-test coverage are reported separately for each examined application.

## Reading a claim

| Evidence type | What it supports | What it does not support |
|---|---|---|
| Official documentation | The developer advertises a feature | That the feature works in every build or scenario |
| Repository source | The examined revision contains a particular implementation | That a distributed application contains it or successfully executes it |
| APK static inspection | This exact artifact contains declarations, resources, or code | Official provenance, runtime success, or complete call coverage |
| Runtime observation | The recorded build produced the recorded result for the stated input | Universal correctness or results on untested devices |
| Upstream issue | A reporter described a behavior | Independent reproduction by this investigation |
| Proposal | A desired outcome and acceptance criterion | Evidence that the current app lacks the capability |

“Not found in the reviewed files” is a search result. “Absent from the app” requires broader evidence. A disabled control can be contextual, permission-dependent, subscription-dependent, or genuinely defective; the reason must be investigated.

## Defect threshold

A report-ready runtime defect needs an exact build, environment, synthetic input, reproduction steps, expected behavior, observed behavior, and repeatability evidence. A static code defect can be supported by a focused executable regression check, with its runtime/application limits stated. Suspicions remain candidates.

For the supplied Moon+ Reader APK, even a reproducible defect is artifact-specific until reproduced on an official build. A cryptographic verification failure is an input-provenance finding, not evidence of a vulnerability in the official product.

## Quality attributes

Non-functional requirements include response time, memory, stability, recoverability, accessibility, privacy, offline reliability, and interoperability. They are not synonyms for “features that do not work.” Report timing with device/API, cold or warm state, input, sample count, and units. A single launch does not establish battery usage or long-session stability.

## Source and test identity

- Cite commit-pinned code links, exact issue URLs, and official product pages.
- Record retrieval dates independently of publication dates.
- Bind local static observations to the APK SHA-256 and tool version.
- Bind tests to fixture IDs/hashes and explicit application/environment identity.
- Preserve meaningful failures and blocked steps rather than silently substituting another test.
- Report test counts by kind: fixture validation, host renderer checks, application runtime tests, and upstream regression tests.

## Reporting discipline

Start with a small number of high-value, well-supported reports. Search the developer's existing issues and documentation before submission. Use one problem per bug report. Group related feature ideas in a digest when the developer prefers email. Describe an improvement to an existing capability as an extension, with a concrete user workflow and observable success criterion.

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
