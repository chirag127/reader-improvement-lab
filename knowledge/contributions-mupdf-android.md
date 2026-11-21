---
type: Report
title: MuPDF Android contribution — follow links to the first page
description: A three-line sentinel correction, retained 15-case Robolectric red/green evidence, local debug artifacts, and verified fork publication.
tags: [mupdf, android, contributions, navigation, regression-tests]
timestamp: 2026-11-21T00:00:00Z
---

# MuPDF Android: follow internal links to page one

**Implemented, host-tested, and published to the fork.** The simplified MuPDF Android viewer used `0` both for a valid first-page destination and for no internal destination, while tap handling accepted only `page > 0`. The contribution reserves `-1` for no internal destination and accepts `page >= 0`. The retained regression run changed from **10 passes / 5 failures** to **15 passes / 0 failures**. Debug APKs were also assembled for a separate application-runtime investigation.

These are executable Java host-test and build observations, not an Android device result. Recovery reused the completed runs and verified the committed source against their recorded hashes.

## Identity and publication

Observed **2026-11-21**.

| Field | Value |
|---|---|
| Upstream | [ArtifexSoftware/mupdf-android-viewer](https://github.com/ArtifexSoftware/mupdf-android-viewer), simplified viewer **1.28.5a** |
| Base | `f2f75636fb9d5508f7d366bc55bac7fbdf5a38a0` |
| Fork | <https://github.com/chirag127/mupdf-android-viewer> |
| Branch | `fix/internal-links-first-page` |
| Contribution | [`523ad7cb3083fc4af91c4d00e89e0c1f20859d93`](https://github.com/chirag127/mupdf-android-viewer/commit/523ad7cb3083fc4af91c4d00e89e0c1f20859d93) |
| Structured record | [`data/contributions/mupdf-android.json`](../data/contributions/mupdf-android.json) |

At **15:51:06 UTC**, `git ls-remote origin refs/heads/fix/internal-links-first-page` returned that exact commit with exit `0`; the fork's porcelain status was empty. [Publication evidence](../evidence/contributions/mupdf-android-publication.json) preserves both interrupted push receipts: the first succeeded, and an overlapping duplicate was rejected because the branch already existed. The subsequent remote readback establishes the published state. No upstream issue, PR, or message was submitted.

## Defect and focused correction

The following are **static observations** of the pinned base, inspected on 2026-11-21:

1. [`MuPDFCore.resolveLink`](https://github.com/ArtifexSoftware/mupdf-android-viewer/blob/f2f75636fb9d5508f7d366bc55bac7fbdf5a38a0/lib/src/main/java/com/artifex/mupdf/viewer/MuPDFCore.java#L190-L192) returns the fitz document's page number for the resolved location. The first page has index `0`.
2. [`PageView.hitLink`](https://github.com/ArtifexSoftware/mupdf-android-viewer/blob/f2f75636fb9d5508f7d366bc55bac7fbdf5a38a0/lib/src/main/java/com/artifex/mupdf/viewer/PageView.java#L565-L598) returned `0` after attempting an external intent and when no link rectangle matched. Internal destinations were returned directly from `MuPDFCore`.
3. [`ReaderView.onSingleTapUp`](https://github.com/ArtifexSoftware/mupdf-android-viewer/blob/f2f75636fb9d5508f7d366bc55bac7fbdf5a38a0/lib/src/main/java/com/artifex/mupdf/viewer/ReaderView.java#L917-L942) pushed history and navigated only when the result was `> 0`. A link to index `0` instead invoked the main-document-area tap callback.

**Three production lines change:** the external-link return and no-hit return become `-1`, and the navigation check becomes `>= 0`. Both producer and consumer must change together: accepting `0` without correcting the sentinel would turn a missed or external link into first-page navigation.

The other changes add JUnit **4.13.2**, Robolectric **4.13**, Android-resource support for host tests, and one 15-case test file. Existing AGP, Gradle, application configuration, and fitz versions were used. The public `hitLink` methods now return `-1` for no internal destination; downstream library callers beyond the inspected viewer source were not inventoried.

## Executed evidence

| Check | Retained result | Evidence |
|---|---|---|
| Base production with new tests | **15 tests: 10 passed, 5 failed, 0 errors, 0 skipped; exit 1** | [Red record](../evidence/contributions/mupdf-android-red-tests.json) |
| Corrected production, identical tests | **15 passed, 0 failures, 0 errors, 0 skipped**, 25.097 seconds | [Green record](../evidence/contributions/mupdf-android-green-tests.json) |
| Base debug assembly | `BUILD SUCCESSFUL in 3m 7s`; 51 tasks, 36 executed | [Build record](../evidence/contributions/mupdf-android-build.json) |
| Green tests and debug assembly | `BUILD SUCCESSFUL in 1m 58s`; 65 tasks, 7 executed | [Build record](../evidence/contributions/mupdf-android-build.json) |
| Committed-source identity, whitespace, licensing | All four source hashes match; diff check and `COPYING`/`README` preservation checks exit `0` | [Publication/source record](../evidence/contributions/mupdf-android-publication.json) |

The **observable navigation regression** starts on zero-based page `2`, taps a link to page `0`, expects page `0`, and checks that history returns to page `2`. Before the fix, the first navigation assertion reports `expected:<0> but was:<2>`. The other four red failures require the new negative sentinel for absent link information, an empty link array, a missed rectangle, and an external link. They are contract checks supporting the fix, not four additional independently reproduced application defects.

The [canonical test source](https://github.com/chirag127/mupdf-android-viewer/blob/523ad7cb3083fc4af91c4d00e89e0c1f20859d93/lib/src/test/java/com/artifex/mupdf/viewer/LinkNavigationTest.java) has LF SHA-256:

```text
7f2e971a31751b888761f19d0d3a5e943baab2656ecada9308bc8a755f962603
```

Both red and green used those exact test bytes. Coverage includes:

- First-page resolution and navigation/history; later-page navigation/history.
- Null/empty link arrays, missed hit rectangles, and unresolved destinations.
- External intent action, URI, and flags; failed external launch; no internal navigation/history for those paths.
- Disabled-link main-area and margin behavior; suppression of internal/external taps while scaling.

### What actually runs

Robolectric simulates **Android API 33** on **Windows 11 amd64**, using **Temurin 17.0.21.1+2**, **Gradle 8.7**, and **AGP 8.5.2**. Production `MuPDFCore`, `PageView`, `ReaderView`, and fitz Java link classification/location conversion execute. The fixture has one chapter, three pages, a 600×800 page, a synthetic link rectangle, and `#page=1` / `#page=2` internal URIs. `https://example.org/` is an intent target, not a network request performed by the tests.

Native initialization and JNI document/link operations are substituted. A test `PageAdapter` supplies laid-out pages without invoking the renderer, and tap/margin callbacks are observation spies. The suite does not parse `fixtures/documents/navigation.pdf`, render a document, launch `DocumentActivity`, or open an external app.

The green JUnit timestamp is `2026-11-21T15:15:45` **without a recorded timezone offset**. Its filesystem modification time is `15:16:11 UTC`; the combined Gradle log was last modified at `15:16:44 UTC`. The raw XML stays local because it contains a host name. Its hash, counts, and all test names are published in the green record.

The recovered build logs omit their full shell invocations and process exit codes. Their `BUILD SUCCESSFUL` summaries and the JUnit results are directly observed. The following command is a **normalized reproduction command**, not a claimed verbatim transcript of the interrupted green invocation.

## Reproduce in an existing checkout

Use the contribution revision, JDK 17, and an Android SDK with platform 33 and the build tools required by AGP 8.5.2. The build declares `com.artifex.mupdf:fitz:1.28.5` when a local JNI build is unavailable. From the fork, with local environment paths substituted:

```powershell
$env:JAVA_HOME = '<path-to-Temurin-17>'
$env:ANDROID_HOME = '<path-to-Android-SDK>'
.\gradlew.bat :lib:testDebugUnitTest --tests com.artifex.mupdf.viewer.LinkNavigationTest :app:assembleDebug --console=plain --no-daemon --max-workers=4
```

For a red reproduction, use base production revision `f2f75636fb9d5508f7d366bc55bac7fbdf5a38a0` with only `lib/build.gradle` and the new test source from the contribution. Preserve any existing work before changing revisions. The recorded red command selected only `:lib:testDebugUnitTest` with the same class filter and console/daemon/worker options. Recovery did not repeat either run.

## Debug artifacts and remaining device verification

The [artifact record](../evidence/contributions/mupdf-android-build.json) identifies four retained local APKs by full SHA-256 and size. Fixed outputs also remain at `app/build/outputs/apk/debug/` in the fork. Metadata reports package `com.artifex.mupdf.viewer.app`, version **1.28.5a**, code **270**, debug variant.

| Local retained artifact | SHA-256 |
|---|---|
| `baseline-app-x86_64-debug.apk` | `27b7930e66e334e90a02a70203d7ba554cfb48809eff42b5f0e2aae3a791ea9b` |
| `fixed-app-x86_64-debug.apk` | `c0866838dcf88cc7d1d637b9a5b5c2083a3d77a4e108b650066660639d3aa198` |
| `baseline-app-universal-debug.apk` | `88b458db93f24d9a55e8f94e51c8c203d28cedd53fbea4f3bb1fe017bab01481` |
| `fixed-app-universal-debug.apk` | `de13402c7133d1ff2a661bc15b4a3a1ae3df23230c5bfd0e5c83a6edfe76220f` |

**Baseline and fixed debug APKs were assembled, but application/device A/B was not run**, as recorded in the [runtime closeout](runtime-results.md#complete-canonical-coverage). The 15 passing Java/Robolectric tests substitute native document operations. A remaining device check would open a synthetic document containing a link back to the first page, enable links, tap from a later page, verify the displayed page and history return, and retain missed/external-link controls. Each future run needs its APK hash, fixture hash, explicit device/environment, steps, observations, and evidence.

Build warnings included SDK XML version skew, unstripped native code in the baseline, unavailable native libraries for four generated ABI splits, and Java/Gradle deprecations. No full CI/lint, Android instrumentation, native rebuild, complete ABI audit, or official-build reproduction is claimed. Upstream's dynamic appcompat dependency and local debug signing also prevent a claim of byte-identical rebuilds. APKs and raw local configuration remain outside this public repository.

## Licensing and future upstream submission

The pinned [README](https://github.com/ArtifexSoftware/mupdf-android-viewer/blob/f2f75636fb9d5508f7d366bc55bac7fbdf5a38a0/README) states **AGPL-3.0-or-later**; [COPYING](https://github.com/ArtifexSoftware/mupdf-android-viewer/blob/f2f75636fb9d5508f7d366bc55bac7fbdf5a38a0/COPYING) contains AGPL v3. Both were preserved. Contribution code/tests live in the upstream-licensed fork; this lab links to the canonical patch. The README also requires a different application package name for a custom release; these retained audit artifacts are local debug builds.

A bounded tracked-guidance search and the [GitHub community profile](https://api.github.com/repos/ArtifexSoftware/mupdf-android-viewer/community/profile), read on 2026-11-21, returned no dedicated `CONTRIBUTING` file or PR template. That profile reports an old `updated_at` value, so this does not establish the absence of other or newer policies. Before any later submission, review current upstream guidance and [the reporting guide](reporting.md), check for duplicate first-page/internal-link reports, and attach the pinned three-line patch plus red/green evidence. State the JNI and application-runtime limits; link any separately completed device evidence rather than inferring it from these tests. Sending an upstream report or PR requires a separate instruction.

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
