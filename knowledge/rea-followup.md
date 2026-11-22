---
type: Investigation
title: Moon REA follow-up and prioritized developer findings
description: Focused search, speech and PDF-save findings from the same supplied APK, linked to reproducible developer packets and a ten-feature supplement.
tags: [moon-reader, reverse-engineering, rea, bugs, evidence]
timestamp: 2026-11-22T00:00:00Z
---

# REA follow-up: findings for the Moon developer

**The strongest observed defect remains saved-form interoperability.** Two outputs from the supplied sample contain `/Prev -1`; one independent parser rejects them and another repairs them while preserving the edits. New REA inspections clarify search-error recovery, the speech availability check, and the Java-to-native save boundary. They add static evidence, not new application-test passes.

For feature requests, the [ten additional proposals](moon-followup-proposals.md) extend the [original 64](moon-improvements.md). Each additional proposal has three prospective acceptance checks and an explanation of its difference from the existing backlog.

## Scope and identity

| Item | Evidence boundary |
|---|---|
| Inspected build | Supplied artifact declares `com.flyersoft.moonreaderp`, version `10.8`, code `1008000` |
| APK SHA-256 | `e2c0ef649413b2f6671598ac8b027d582ba220e38738f2e253694289ea20e1fc` |
| Observation dates | New static inspection: 22 November 2026; reused application observations: 21 November 2026 |
| Authenticity | Unknown; the sample failed the retained default signature verification and displayed a mod-store promotion. See [provenance](../data/artifact.json) and [runtime context](runtime-results.md#installation-promotion-and-storage-onboarding). |
| New REA scope | Eight distinct method selections, two class inventories and one JNI inventory restricted to `com.radaee.pdf.Document` and `lib/x86_64/librdpdf.so` |
| Supporting records | [Follow-up evidence and exact selectors](../evidence/static/rea-followup.json); [original static observations](../evidence/static/observations.json) |
| Application execution | No new Android runs in this follow-up. The retained [36-case ledger](../data/runtime-results.json) remains 3 pass, 6 partial, 1 fail, 7 blocked and 19 not-run. |

**Verified** below means the specified static representation or retained observation supports the fact. **Inferred** identifies a conditional explanation. **Unknown** marks the further evidence required. Neither a recovered method nor a package name authenticates the official Play build. The APK and full proprietary evidence remain private; published receipts identify their bytes without redistributing them.

## Priorities

Priority is a suggested investigation order, not a measured severity assigned to an official release.

| Order | Finding | Evidence today | Next useful action |
|---|---|---|---|
| 1 | Saved form outputs contain a negative previous-xref offset | Repeated sample-specific runtime/host-readback observation, `RUNTIME-PDF-PREV-001` | Reproduce on an authenticated build using the same synthetic form; inspect incremental-writer state |
| 2 | Export and PDF-save success propagation | Existing static candidates `APK-NOTE-002` and `APK-PDF-002`; new `Document.Save()` bridge evidence | Induce a controlled destination failure and compare visible success/pending state with durable output |
| 3 | Invalid regex exit skips normal search finalization | New static chain for `APK-SEARCH-001`; progress-control recovery exists | Test a simple invalid expression followed by valid search; capture feedback and control state |
| 4 | Backward-only PDF search excludes the current page | Retained worker bytecode and new option-listener context | Check the intended scope contract and first-/middle-page boundaries |
| 5 | Speech availability helper has no upper-length bound | New smali narrows `APK-TTS-002`; complete pipeline reachability remains unknown | Record actual document-to-engine submissions for a long synthetic segment |

## 1. Saved-form interoperability packet

**Suggested subject:** `[PDF forms / supplied 10.8 sample] Close-triggered save writes /Prev -1; independent readback needs repair`

**Verified observation:** canonical case `RT-16`, environment `aosp-api36-x86_64-audit`, used an account-free Android API 36 x86-64 audit emulator. The first run changed three fields; a fresh-copy second run changed only the name. Both were saved by closing with Android Back. Both outputs retained the intended values, but each appended `/Prev -1`. This is an interoperability failure, not demonstrated loss of those values.

| Input/output | SHA-256 |
|---|---|
| [Original `acroform.pdf`](../fixtures/documents/acroform.pdf) | `3a7b514b4a6c01640bd27436857826bc258cf10b6f7ac4e58ce1c3f7af842402` |
| [First saved output](../evidence/runtime/outputs/acroform.pdf) | `af860b1720c51d4f2ebaca787c80e9230d201ababbc9599f41c1b12e2de0067a` |
| [Text-only repeat output](../evidence/runtime/outputs/acroform-repeat.pdf) | `4f189a85b395615b8ae6726f333bb7e4805ae52b4d7cb5621e7f6d718425d9d9` |

### Recorded steps and actual result

1. Open a writable copy of the original synthetic form. Set the name to `LAB_FORM_20261121`, clear Subscribe, and select Green.
2. Close with Android Back and retain the saved bytes.
3. Inspect with pypdf **6.15.0** and PyMuPDF **1.28.0**; force-stop/reopen the reader and inspect the values.
4. On a fresh original copy, change only the name to `LAB_FORM_REPEAT_20261121`, close with Back, and repeat the independent readback and reader reopening.

**Expected:** edited values survive and the resulting PDF can be independently read without repairing its cross-reference chain.

**Actual:** pypdf raised `ValueError('negative seek value -1')` for both outputs. PyMuPDF opened with `repaired=True` and recovered the edits. The original opened without repair; its recorded initial `startxref` was 7523 and it had no `/Prev` entry. The first output retained the original prefix and added another `startxref` at 11743.

Evidence: [first output inspection](../evidence/runtime/form-preserved-output-inspection.json), [repeat inspection](../evidence/runtime/form-repeat-text-only-inspection.json), [first reopen](../evidence/runtime/60-form-output-reopened.png), [repeat reopen](../evidence/runtime/67-form-repeat-text-only-reopened.png), and [full execution record](../data/runtime-results.json).

### What REA adds

`PDFReader.save()` was already observed to ignore `Document.Save()`'s boolean. The new `Document.Save()Z` body returns the native `save(hand_val)` result, or returns false after catching an `Exception`. The JNI inspection associates `save(J)Z` with an exported candidate named `Java_com_radaee_pdf_Document_save` at ELF virtual address `0x15fb40`. It also identifies `saveAs(JLjava/lang/String;Z)Z` at `0x15fbc0` in the selected native member, SHA-256 `31bdb8e9516801d87008846bcd20b5d2376c2b90da4a475af25856cd521108a7`.

**Inferred:** the incremental-writer boundary is the appropriate next diagnostic for the negative previous-xref value. **Unknown:** the internal writer instruction responsible, the native return value during either recorded save, and the exact SDK version. The discarded return value and malformed successful-looking output are distinct concerns; this investigation has not proved that one caused the other. A matched JNI export is not observed library loading or invocation, and partial relocation/table coverage does not establish unique registration.

### Supporting native disassembly

Four bounded captures using the existing Ubuntu WSL **GNU objdump 2.46** examined the two named JNI wrappers and two direct-callee windows. These are ordinary static observations, separate from REA Evidence. Exact selections and private output digests are in the [follow-up record](../evidence/static/rea-followup.json).

- **Verified:** the `save` wrapper at `0x15fb40` calls `0x291730` and preserves its result register through cleanup. The selected worker window, `[0x291730, 0x291b30)`, in turn preserves the selected result of calls to `0x4ae550` or `0x4afeb0`. Those downstream bodies were not inspected.
- **Verified:** on the inspected file-open-success route, `saveAs` calls `0x15fe70`, performs cleanup and sets its eventual JNI boolean low byte to `1`, without testing the helper's return register. **Unknown:** whether that helper returns any meaningful status; its selected `[0x15fe70, 0x160070)` window covers setup only. This is not evidence of a discarded boolean failure.
- **Boundary:** internal nearest-symbol labels are not recovered function names. Indirect calls, field meanings and the runtime route taken by either saved-form experiment remain unknown. The captures narrow the next investigation but do not identify the trailer-writing instruction or establish that save-as was used in the form experiment.

### Requested developer investigation and acceptance checks

- Repeat on an authenticated official build, retaining the original, output and exact close/save route. Compare incremental save with a new-file save where supported.
- Trace how the existing previous-xref offset is initialized, updated and serialized, including unavailable/sentinel states. A valid output must not encode a negative previous-xref location.
- Require all edited field values to round-trip through the reader and independent readback. Check failure feedback and preservation of pending edits separately from PDF structural validity.

Related requests already exist as **MOON-001**, **MOON-011** and **MOON-032**. This packet strengthens those requests rather than counting them as new features.

## 2. Invalid-pattern search finalization packet

**Suggested subject:** `[Search / static candidate] Invalid pattern exits without normal completion; verify automatic recovery`

**Verified static chain:**

1. The retained `PrefSearch.startSearch()` sets `inSearching` before starting its worker. The worker compiles the entered key as a regular expression.
2. Retained worker smali places compilation inside a catch-all range. Its exception exit calls `A.error(Throwable)` and returns without the worker's normal completion message or flag clearing.
3. The new constructor body installs a search handler whose message `2` calls `showSearchButton(true)` and renders the result count. `showSearchButton(true)` restores options and the text field and hides progress; it does not itself clear `inSearching`.
4. The new `A.error` overloads show error logging, stack-trace recording and conditional beta-log persistence; they contain no explicit search completion dispatch.
5. The new `initView()` registers the progress control's click listener. `onClick()` handles that control by calling `showSearchButton(true)` and the already-inspected `stopSearch()`.

**Inferred candidate:** after a normal search-button launch with invalid regex syntax, the inspected exception route can miss the automatic return to idle controls. **Important counterevidence:** an explicit manual recovery route exists. Calling this a permanent freeze, a crash, or an unrecoverable search would overstate the evidence. Unexamined global callbacks and actual UI timing remain unknown.

### Prospective reproduction — not executed

1. Record the exact build, search mode and case/word options. The retained sample UI explicitly advertises regular expressions; regex support is intentional, not the defect.
2. Open [the synthetic search text](../fixtures/scenarios/rt12-literal-search.txt), SHA-256 `8b28e45b31d7b992a6242c27eb5942404d511ff0c49e7d06828af534f58a4373`, and successfully search for `S01` as a control.
3. Search for the simple invalid expression `[`. Record any syntax message, the edit field's enabled state, progress state and whether automatic completion occurs. This is a syntax check, not an expensive-pattern stress test.
4. Tap the progress control if still active, record whether controls recover, and run the valid control again. Distinguish automatic recovery from successful manual recovery.

**Expected proposed contract:** syntax errors produce useful feedback, end the busy state, retain the query for correction and permit a subsequent valid search. **Unknown:** the actual outcome of this sequence; `RT-12` remains unexecuted. Existing **MOON-018** is the appropriate improvement request.

## 3. Directional-search boundary question

**Verified static observation:** the inspected PDF worker starts at the current page only for forward-only searches; otherwise it starts at zero. For backward-only searches its exclusive upper bound is the current-page index; otherwise it is the document page count. The new option listeners make the two direction checkboxes mutually exclusive through that UI.

Consequently, the backward-only branch excludes the current page and covers no pages when the current-page index is zero. Forward-only includes the current page. This is a static asymmetry, not yet a contradiction of the intended product contract.

**Prospective check:** use a one-page PDF with a known text match; compare unrestricted, forward-only and backward-only searches. Repeat from a middle page in a numbered multi-page fixture, recording which pages are included and the exact scope wording. If the product promises "previous pages only", exclusion can be intentional; if it promises searching backward from the current reading position, the result needs clarification. Acceptance should name current-page inclusion, ordering and boundary behavior explicitly. Related request: **MOON-020**.

## 4. Speech-length boundary clarification

**Verified new evidence:** `A.TtsLine.isAvialable()Z` was recovered as smali. With `end > start`, it accepts strings longer than one character; a one-character string must also avoid the object-replacement character and listed punctuation. The inspected predicate imposes no upper string-length bound.

**Already known:** the queue truncates an over-limit string to a prefix ending ten characters below its configured input limit and advances to another line. The line adder appends a valid line object without splitting it. Earlier segmentation/constructor reconstructions carry warnings and interruption limitations.

**Updated conclusion:** the availability helper does not supply the previously unresolved maximum-length guard. This removes one possible guard from the hypothesis; it still does not prove a real document produces an over-limit queue entry. Upstream segmentation and text transformations remain the decisive uncertainty. No speech omission was heard or measured in this follow-up.

**Next check:** follow the existing [RT-29 protocol](bug-candidates.md#6-an-over-limit-speech-segment-may-lose-its-suffix) using the [long-speech fixture and sentinels](testing-scenarios.md). Record actual engine submissions and source offsets, then check complete token coverage and pause/resume across any split. Keep **MOON-005** conditional on reachability; intentional narration exclusions in **MOON-066** are a separate workflow.

## Other high-value packets already available

- [Export success after a failed write](bug-candidates.md#1-export-reports-success-after-an-unsuccessful-write): a static helper/wrapper error-propagation concern; an actual destination failure remains required.
- [Pending PDF state before save success](bug-candidates.md#3-pending-pdf-changes-may-be-cleared-before-durable-save-success): use the new `Document.Save()` bridge evidence above, while preserving the distinction from malformed-output interoperability.
- [Same-length cover updates](bug-candidates.md#2-equal-length-cover-revisions-may-not-be-considered-newer) and [annotation-upload retry](bug-candidates.md#4-failed-annotation-upload-may-lose-its-pending-flag): retain their specific workflow boundaries; the findings do not cover every synchronization operation.
- [One-off `101/1` indicator](../data/runtime-results.json): `AUX-STATUS-001` was observed once while the correct one-page text was displayed. **MOON-065** specifies document-scoped status consistency and printed-label navigation; its proposed document-switch test is not a claimed root cause.

## Submission and remaining coverage

Use the [verified reporting guide](reporting.md). Send a focused packet with its synthetic input and evidence links, identifying the unknown-origin sample up front. An official-release allegation requires its own authenticated-build reproduction. These packets and the ten feature proposals are prepared drafts; publishing them does not send email or create an upstream issue.

The follow-up does not replace the [historical static analysis](apk-analysis.md) or [runtime ledger](runtime-results.md). It resolves the availability-helper question, narrows the search recovery hypothesis and identifies the native save boundary. Complete native writer causality, official-build behavior, actual invalid-pattern recovery, end-to-end long speech, cloud retry, accessibility and physical-device coverage remain open with the next diagnostics stated above.

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
