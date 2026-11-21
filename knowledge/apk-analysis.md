---
type: Analysis
title: Supplied Moon+ Reader APK — focused static analysis
description: Manifest, package structure and bounded PDF, notes, search, sync and TTS observations from one supplied APK.
tags: [android, apk, static-analysis, readers, evidence]
timestamp: 2026-11-21T00:00:00Z
---

# Supplied APK: focused static analysis

**The inspected bytes contain established PDF, annotation/export, search, synchronization and TTS implementations.** This pass maps those paths and identifies focused verification candidates. It does not reproduce application defects or authenticate an official release.

| Identity | Value |
|---|---|
| Artifact | `moonreader-supplied-10.8` — [identity and signature record](../data/artifact.json) |
| SHA-256 | `e2c0ef649413b2f6671598ac8b027d582ba220e38738f2e253694289ea20e1fc` |
| Size | 57,787,496 bytes |
| Package/version declarations | `com.flyersoft.moonreaderp`, `10.8`, code `1008000` |
| SDK declarations | Minimum 21; target and compile 36 |
| Observation date | 2026-11-21 |
| Authenticity | Unknown. The recorded Android `apksigner` invocation failed v1 digests for `classes3.dex` and `classes5.dex`. |

Findings apply to this exact artifact. The signature result and unusual decompiled instructions are not a basis for attributing these observations to the official Play build, or for declaring the artifact malicious.

## Evidence and coverage

- [Package structure](../data/apk-structure.json): namespace counts, selected class summaries, manifest component declarations, DEX/native member inventory and coverage boundaries.
- [Original observations](../evidence/static/observations.json): stable finding IDs, observed facts, inferences, unknowns and private-evidence digest receipts.
- [Tool and run provenance](../evidence/static/provenance.json): versions, source identities, commands, response counts, diagnostics and shutdown limits.
- [Follow-up consistency verification](../evidence/static/bounded-followup-verification.json): saved-record checks, including recovery from interrupted run E; **not an app test or certification of decompiler correctness**. The [original verification](../evidence/static/verification.json) remains an unchanged historical snapshot of the initial pass.

REA's isolated CLI produced complete manifest/component declarations with Evidence ID:

`ev_2197257034924089fcc7e23e8721f63b439afeae495f011eaad051297f1c3679`

The standalone headless JAR supplied ordinary local static evidence for the focused code pass. Those records were not inserted into a shared REA ledger. The public evidence contains original analysis and hash receipts; APKs, raw responses, proprietary method bodies and local machine paths remain outside this repository.

### What was examined

| Surface | Recorded coverage |
|---|---|
| Manifest | Complete root XML and 25 component declarations; 12 requested permissions |
| Class inventory | 12,959 of 12,959 top-level JADX display names, one exhausted page |
| Engine load diagnostic | 27,211 classes, 191,473 methods and 5,008,727 instructions reported by JADX's root loader; this is a different scope from the top-level list |
| Focused class summaries | 21 selected classes, including nested note and helper types |
| Method bodies | 52 evidenced requests: 51 returned bodies and one unresolved selector; 49 bodies have finalized run receipts, two are recovered from interrupted run E |
| Smali corroboration | Six selected method requests, including the search worker, export wrapper, two freshness checks and TTS queue |
| References | Five incoming-reference queries: the original serializer query plus four freshness/cover queries; bounded JADX using-node relationships |
| Bounded follow-up support queries | Three signature queries and two inner-class/resolution queries; the numeric nested sync worker remains unresolved |
| Archive members | Five root DEX files and 24 native-library members across four ABIs |
| Application execution | None in this lane |

The loader's larger class count includes a different internal scope; neither the API's misleading `raw_class_count` label nor the top-level list is treated as a complete raw-DEX-definition inventory. Namespace counts group the first three package segments and include bundled dependencies. Package names alone do not establish that a library executes, its exact version, or any telemetry behavior.

The follow-up reused the original inventories and retained all 13 finding IDs and earlier assessments. It adds eight distinct method selections within the original eight-selection budget: five bodies from finalized runs A/C, one unresolved selection in finalized run B, and two bodies recovered from interrupted run E. Across A–E, 33 planned call slots account for 22 calls in finalized receipts, three surviving E response exchanges, seven unexecuted B slots and one E unload slot whose execution is unknown. Cumulatively there are 108 retained response exchanges: 107 successful tool responses and one selector error. Successful responses do not certify source reconstruction or run completion.

## Implementation map

### PDF — existing rendering, extraction, reflow and annotations

`ActivityTxt.pdfOpen2(String)` creates `com.radaee.pdf.Document`, handles open-result codes, and hands the document to `PDFReader.open(ActivityTxt, Document, String)`. That method selects the GL or ordinary PDF layout. `PDFReader.setView(int)` also has separate comic and DjVu branches.

`PDFReader.getPageText(int)` reads page-object text through `ObjsGetString`; `ActivityTxt.pdfCreateReflowText(long)` applies format-specific formatting. The package also contains `com.radaee.*` wrappers and `librdpdf.so` for each ABI. Native function bindings, SDK version, OCR, reading-order quality and render speed were not established. See **APK-PDF-001**.

Annotation methods bridge the local note model and PDF markup/popup text. `pdfUpdateNotesToFile(boolean)` reaches the save path, while `ActivityTxt.pdfSaveChanges()` updates dirty/sync state. Complex PDF-import/update Java reconstructions contain warnings; only selected relationships are corroborated in smali. See **APK-PDF-002**.

### Notes/export — a local model and several distinct outputs

`BookDb` queries a SQLite `notes` table. Its `NoteInfo` model includes document/file identity, chapter/split/position, original and note text, time, highlight range/color and markup flags.

`PrefChapters.doShare(...)` exposes `.mrexpt` import/export. `BookDb.exportNotesToText(...)` serializes non-PDF rows with file-length/formatting metadata; the PDF path uses a separate page-count/tagged representation. `BookDb.importNotesFromText(...)` dispatches back to the appropriate importer. This establishes an existing reader-specific format, not verified lossless interchange. See **APK-NOTE-001**.

Other paths already support:

- Checked highlights/notes assembled with optional chapter headings.
- `text/plain` sharing, optionally with a cover attachment.
- Clipboard/text-file fallback for constructed share strings of at least 80,000 characters.
- Rendered quote/image sharing in `PrefShareText`.
- Token-authenticated highlight upload in `Readwise.addHighlights(...)`.

Sharing and serialization are separate functions. Readwise service success and image encoding were not tested. The image-share path uses a `.jpg` filename with an `image/png` intent; compatibility remains a verification question. See **APK-NOTE-003**.

### Search — content and settings have different paths

`PrefSearch.startSearch()` launches a worker that constructs `java.util.regex.Pattern` from the entered key plus case and whole-word options. The saved worker smali confirms this construction. Reconstructed branches scan plain text, HTML/splits, ebook chapters and PDF text, building snippets and delivering results through handlers.

`stopSearch()` clears an `inSearching` flag checked by examined loops. This does not establish cancellation of an ongoing regex operation or extraction call. Result-count checks occur in some branches; uniform limits and busy-state recovery were not demonstrated. See **APK-SEARCH-001**.

Separately, `misc.FuncSearch.getSearchResults(...)` searches settings/dialog titles and delegates searches through their views. Settings discovery is therefore an existing capability. See **APK-SEARCH-002**.

### Sync — provider dispatch and shared note serialization

`Cloud.instance(int)` dispatches to Dropbox, Google Drive, FTP or WebDAV. `Sync.uploadCloudPositionFile(...)` exchanges saved position data with a device identifier; `notifyNewCloudPosition(...)` applies the received data to preferences and signals the reader.

Note upload uses the same `BookDb.exportNotesToText(...)` serializer as local export, adds deletion records and compresses the payload. Download decompresses and selects the PDF or ordinary note importer. The original serializer xref query returned `Sync.uploadCloudNoteFile` and `BookDb.exportNotesToFile` as users. Dynamic and reflective relationships remain outside that result. See **APK-SYNC-001**.

The bounded follow-up identifies a concrete use of the equal-size freshness gates: `verifyDownloadBookCovers(...)` and `verifyUploadBookCovers(...)` remove corresponding entries from the cover-transfer lists when their predicates return false, before calling the final cover-transfer functions. Each predicate's xref query also reports a shared worker as `Sync.7.1.run`; its supplied class selector did not resolve, so that worker's enclosing workflow remains unknown. These findings support a cover-refresh test, not a claim about all book-file, note or reading-position synchronization (**APK-SYNC-002**).

### TTS — platform speech with document-aware progression

`ActivityTxt.initTTS()` constructs Android `TextToSpeech`. `setSpeakQueue(int)` applies rate/pitch, submits identified utterances and optionally inserts silence. PDF text passes through `pdfGetTtsLines()`; progress callbacks coordinate selection and page/chapter progression. The non-exported `BookTtsService` declares `mediaPlayback` and starts a foreground notification.

This is static evidence of integration. Voices, audio focus, engine limits, lifecycle survival and actual speech were not exercised. See **APK-TTS-001**.

The follow-up located upstream segmentation in `A.getTtsLines(...)` and recovered `A.addTtsLine(...)` and the `A.TtsLine` constructor. The adder checks `isAvialable()` and appends the same object; its own body has no length-based splitting. The availability helper was not selected. Segmentation contains explicit duplication warnings and inconsistent reconstructed branches; the constructor shows ruby/filter substitutions and whitespace processing but also malformed reconstructed literals and exception-flow variables. These stages do not establish a reliable length bound or prove that an over-limit line reaches the queue. The two E bodies have valid saved response pairs, with interruption limits below (**APK-TTS-002**).

## Focused verification candidates

These are conditional implementation concerns, **not reproduced official-app bugs**. The observation ledger preserves the exact class/method selectors and evidence hashes.

| Finding | Direct observation | Check needed before reporting a defect |
|---|---|---|
| **APK-NOTE-002** | `T.saveFileText(String, String)` tries ordinary output and, where applicable, an SD document-provider fallback; handled exceptions or unsuccessful paths return false. `BookDb.exportNotesToFile(...)` discards that result and returns true for nonempty serialized content, which its UI callback uses for success feedback. | A non-throwing helper failure is now supported by the examined code path. Induce a real destination failure and compare feedback with durable bytes; storage grants, picker acceptance and logging side effects remain untested. |
| **APK-SYNC-002** | Both freshness predicates reject equal-size files before comparing dates. The inspected cover-download/upload verifiers remove those candidates from their transfer lists. | Exercise same-length, different-content cover revisions in both directions. The shared nested worker remains unresolved; other sync workflows are not established by this result. |
| **APK-TTS-002** | The queue method shortens a string longer than `maxSpeechInputLength` to a prefix ending ten characters below the limit, then advances to the next line. Smali confirms it. Upstream stages are now located, but their reconstructions and the interrupted E receipt limit inference. | Over-limit reachability remains unresolved. Check long unbroken text and filter effects, then compare complete input with spoken output on an authenticated build. |
| **APK-PDF-002** | The PDF wrapper ignores `Document.Save()`'s boolean and its caller clears dirty state before saving. | Simulate save failure and inspect durable bytes, user feedback and pending sync state. Native semantics and other handlers are unknown. |
| **APK-SYNC-003** | Note upload clears `hasNewNoteForUpload` before the transfer and supplies a null callback at this call site. | Fail a transfer, reconnect and verify that pending notes retry; other code may restore the flag. |
| **APK-SEARCH-001** | Entered text becomes regex syntax; cancellation uses a flag. | Check metacharacters, invalid patterns, cancellation and result limits on representative documents. Intended regex semantics are unknown. |

`ActivityTxt`'s summary reports 1,018 methods and 586 fields, including synthetic members. This identifies a broad cross-feature navigation/test surface, not a measured architecture or performance defect (**APK-STRUCT-001**).

## Tooling recovery and provenance

| Tool | Recorded version / identity |
|---|---|
| REA CLI | `rea-agents` 6.10.1, installed package source inspected locally |
| Headless producer | `jadx-headless-mcp` 0.7.1; REA-pinned source revision `5844800a486d2248fa949b74c9896285f5b54de2` |
| Producer JAR SHA-256 | `6e5eacf500b64292bfb73c49797c1958f6ee44646e43e868039ae7feb573ff75` |
| REA bridge | Protocol 11; source SHA-256 `08de17c12c68adf077aaccba84c6d53b6c9ac86ff2d2e581e35b9b03618003f2` |
| Java | Temurin OpenJDK `27.0.1.0.2+1`, full JDK |
| Node | `v26.13.0` on Windows x64 |
| Android declaration/signature tools | SDK Build Tools 36.0.0 `aapt` / `apksigner`, as recorded in the parent artifact evidence |

Producer sources: [pinned headless source](https://github.com/1013503897/jadx-headless-mcp/tree/5844800a486d2248fa949b74c9896285f5b54de2), [release JAR](https://github.com/1013503897/jadx-headless-mcp/releases/download/v0.7.1/jadx-headless-mcp-0.7.1-all.jar), [REA 6.10.1 package](https://www.npmjs.com/package/rea-agents/v/6.10.1). These establish tool provenance, not the APK's publisher.

An earlier shared-session REA attempt reported changed JAR bytes during admission. One bounded diagnostic using the unmodified installed snapshot/hash helpers passed: byte extent, descriptor/path metadata, digest, snapshot and readback all matched. A subsequent isolated CLI invocation succeeded with exit 0 and empty stderr.

**The historical cause remains unknown.** The error message can represent size, metadata/identity or digest changes. A Windows ChangeTime transition is only a hypothesis. Recovery was verified for the isolated CLI, not for the parent's long-lived provider. No installed package, integrity guard or shared configuration was changed, and no shared service or ledger was reset.

The package command used shell-scoped JAR/JDK settings, a 3,072 MiB heap and a 300,000 ms operation budget:

```powershell
# APK, JAR, JAVA_HOME and OUT select the local files and a new private output directory.
$env:REA_JADX_MCP_JAR = $JAR
$env:JAVA_HOME = $JAVA_HOME
$env:TEMP = $OUT
$env:TMP = $OUT
$env:REA_JADX_HEAP_MIB = '3072'
$env:REA_JADX_OPERATION_TIMEOUT_MS = '300000'
rea inspect-android-package $APK --detail summary --evidence_output "$OUT/rea-package-bundle.json" --json
```

The focused pass used the verified JAR directly over local stdio with a 3 GiB heap, four active processors/workers and a 90-second decompile budget. Exact sanitized request selectors, run outcomes and private evidence receipts are in the provenance record. The original finalized runs checked the JAR/APK SHA-256 before and after. Their standalone server acknowledged unload but did not exit within a 15-second EOF allowance; the client terminated only its owned JVM and recorded that disposition.

Follow-up A, C and D completed their planned calls; B finalized after its unresolved method selector and did not reach unload. All four retained matching before/after hashes and owned-JVM termination records. **E was interrupted and has no final receipt:** its original `run.json` still records zero calls and only pre-run hashes. Saved initialization, catalog, load and two method exchanges survive; matching request/response IDs, selectors and decoded sidecars support response recovery. They do not supply per-call timing, post-run identity, unload acknowledgment, child exit or cleanup. No saved unload exchange establishes whether that request was sent. A later hash check measures current bytes only; an earlier narrow process-name/path search cannot reconstruct E's missing lifecycle events.

## Decompiler and remaining limits

- All 51 returned body responses reported Java mode with no automatic smali fallback, including the two recovered E bodies. One additional method selector returned an error and no body. Output mode is not proof of correct source recovery.
- The two focused body runs each logged 100 error lines, with 763 and 762 warning lines respectively. These include bundled dependencies and repeated diagnostics; they are not counts of 100 distinct application defects or 100 failed selected methods.
- `pdfUpdateNotesToFile`, `pdfCreateNotesFromText`, `PrefSearch.startSearch` and the new `A.getTtsLines` response contain explicit decompiler warnings. `BookDb.importNotesFromText`, `T.saveNormalFileText` and the recovered TTS constructor also have imperfect reconstruction despite empty provider markers. Smali corroboration supports only the originally selected claims stated above; the follow-up added no smali requests.
- This pass is not a full call graph, native/JNI analysis, security audit, OCR assessment, all-format test or performance benchmark. Reflection, dynamic loading and unexamined callers remain unknown.
- Authentic official-build reproduction, real storage failures, sync conflicts/retries, long-utterance reachability, accessibility and lifecycle behavior remain open. A missing observation is not an absent feature.

<footer class="hire-me">
  <h3>Hire me</h3>
  <p>Chirag Singhal — building free, open APIs and tools.</p>
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
