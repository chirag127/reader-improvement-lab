---
type: Investigation
title: Moon bug-report candidates and reproduction criteria
description: Six source-grounded investigation candidates, with concrete reproduction steps and explicit official-build attribution limits.
tags: [moon-reader, bugs, reproduction, persistence, evidence]
timestamp: 2026-11-21T00:00:00Z
---

# Bug-report candidates

**Six implementation candidates were identified by static inspection. They are not six confirmed bugs in the official app.** This page specifies the evidence needed to turn each into a useful report. The canonical observations, selectors, smali corroboration, and evidence receipts are in the [static finding ledger](../evidence/static/observations.json); the [implementation map](apk-analysis.md) explains their context.

All six candidates concern the [supplied APK](../data/artifact.json), SHA-256 `e2c0ef649413b2f6671598ac8b027d582ba220e38738f2e253694289ea20e1fc`, inspected on **2026-11-21**. Its distribution origin is unknown and the recorded default signature verification failed. Reproduction on that sample remains sample-specific. An official-release report requires an independently identified official installation and its own result.

The steps below are **proposed experiments**, not actions claimed to have been executed. Consult the [coverage ledger](coverage.md) and any linked runtime results for executed cases. Priority here describes potential user impact if the hypothesis is confirmed, rather than a measured defect severity.

## 1. Export reports success after an unsuccessful write

- **Evidence:** `APK-NOTE-002`; the examined `.mrexpt` wrapper discards the write helper's boolean result, and the UI uses the wrapper's result. The bounded follow-up establishes non-throwing false-return paths in `T.saveFileText`, after ordinary output and any applicable SD document-provider fallback fail.
- **Potential impact:** a reader may rely on an export that was not durably saved. Investigate early because exports are often used before migration or device replacement.
- **Test:** `RT-20` in the [application matrix](testing-plan.md).

Proposed reproduction:

1. Create a note in the original synthetic EPUB and successfully export it to a disposable destination. Record the output hash and note content.
2. Establish a controlled destination failure while keeping the note and original book intact. Record why the write fails; a cancelled picker is not necessarily the same code path.
3. Repeat the export. Compare the displayed outcome with actual destination existence, length, and contents.
4. Restore a writable destination and verify a successful retry.

**Expected:** a failed write is reported as failed, the note remains available, and retry produces the complete export. **Needed to confirm:** induce that failed write through the actual app workflow and compare the visible feedback with durable output. The helper-to-wrapper error-propagation chain is supported statically; storage grants, picker acceptance and real user-visible behavior remain untested.

Suggested report subject after confirmation: **[Export] Success message shown when the destination write fails**.

## 2. Equal-length cover revisions may not be considered newer

- **Evidence:** `APK-SYNC-002`; two inspected freshness predicates return false for equal-size, nonempty local and remote files before date comparison. The bounded follow-up traces both predicates to cover-upload/download list filtering. A second shared nested worker remains unresolved.
- **Potential impact:** a same-length changed cover can be removed from the examined transfer lists. Visible cover-refresh behavior still needs reproduction.
- **Test:** `RT-26`; use a controlled backend and disposable namespace.

Proposed reproduction:

1. Successfully synchronize a book with an original synthetic cover and record both local and remote cover hashes, lengths, and modification times.
2. Replace the cover with a visibly different valid image of exactly the same byte length. Verify that the image decodes and has a newer modification time and different hash.
3. Exercise cover download, retaining server metadata, transferred bytes and the displayed cover after the documented refresh operation.
4. Reset the disposable fixture and test cover upload independently. Use a different-length cover revision as a control.

**Expected:** the documented cover-update policy handles changed cover content consistently, regardless of accidental byte-length equality. **Needed to confirm:** establish the real cover-list construction and demonstrate stale transferred/displayed content under that policy. The unresolved shared worker does not justify extending this finding to book files, reading positions or annotation synchronization.

Suggested subject: **[Cover sync] Same-length newer cover is not transferred in <direction/backend>**.

## 3. Pending PDF changes may be cleared before durable save success

- **Evidence:** `APK-PDF-002`; the observed save caller clears dirty state before saving, while the wrapper does not consume the native save result. Native semantics and other error handlers remain unexamined.
- **Potential impact:** misleading saved state or missed retry after a genuine save failure.
- **Test:** `RT-18`, with successful `RT-14` as a prerequisite.

Proposed reproduction:

1. Work on a writable copy of `annotations.pdf`, add a distinctive note, save, and verify it after reopening.
2. Establish a controlled write failure on another disposable copy after making a new annotation.
3. Attempt save; record the message, dirty/pending state, and output bytes. Preserve the original before closing anything.
4. Restore access, retry, and inspect durable annotation objects with a second reader or parser.

**Expected:** pending edits remain recoverable until a successful durable save, and failure is visible. **Needed to confirm:** an actual native save failure and its user-visible state consequences. A screenshot of a new annotation is not proof that it was saved.

Suggested subject: **[PDF saving] Pending edits are marked saved after <specific write failure>**.

## 4. Failed annotation upload may lose its pending flag

- **Evidence:** `APK-SYNC-003`; the inspected upload call clears a flag before transfer and passes no callback at that call site. A provider or another caller may retry or restore state.
- **Potential impact:** a note may require another user action before being delivered after a failed transfer.
- **Test:** `RT-27`; first prove normal annotation delivery.

Proposed reproduction:

1. Synchronize a synthetic note successfully and establish how both reading-position and annotation completion are observed.
2. Create a second distinct note. Have the test backend reject its upload with a recorded failure response.
3. Restore backend service, background/resume the reader, and test a restart separately.
4. Compare local note content, server data, pending indicators, and delivery after retry. Keep a successful retry control with a newly created note.

**Expected:** an undelivered local note remains pending or is retried according to the documented workflow. **Needed to confirm:** failure across the complete retry lifecycle. Early flag clearing does not by itself prove note loss.

Suggested subject: **[Annotation sync] Failed upload is not retried after <recovery sequence>**.

## 5. Search syntax and cancellation need explicit behavior checks

- **Evidence:** `APK-SEARCH-001`; entered text is compiled as a regular expression in an examined worker, and cancellation clears a flag. The supplied sample's [runtime UI advertises regular-expression search](runtime-results.md#rendering-navigation-and-search). Literal/metacharacter matching, invalid-pattern recovery, and cancellation behavior remain untested.
- **Potential impact:** punctuation may be interpreted unexpectedly, or a search may be difficult to cancel. These are independent hypotheses and should become separate reports only if independently reproduced.
- **Tests:** `RT-12` for syntax/recovery and `RT-13` for cancellation.

Proposed reproduction:

1. Record the active search mode, case/word options, and any regex guidance in the actual UI.
2. Use a synthetic document containing literal `a.b`, `a+b`, and `[x]`; compare exact-match expectations with actual results under the documented mode.
3. If regex input is accepted, enter a simple invalid pattern, record the error, then run a valid search. Avoid expensive adversarial expressions.
4. On a separately identified longer input, cancel an ordinary search and immediately use another control. Record measured cancellation and UI response separately.

**Expected:** syntax is understandable; invalid input recovers cleanly; cancellation has a clear outcome. **Needed to confirm:** a contradiction with the actual search-mode contract or an observed usability failure. Regex support itself is not a defect, and a flag does not establish worst-case latency.

Suggested subjects: **[Search] <literal query> behaves contrary to the selected mode** or **[Search] Cancelling <ordinary workload> leaves <observed state>**.

## 6. An over-limit speech segment may lose its suffix

- **Evidence:** `APK-TTS-002`; the queue method truncates an over-limit string and advances to the next entry. Segmentation, the line adder and constructor have now been inspected, but imperfect reconstruction and the unexamined availability helper leave over-limit reachability unresolved. Two follow-up bodies were recovered from an interrupted run whose final lifecycle receipt is missing.
- **Potential impact:** omitted speech if the boundary condition is reachable.
- **Test:** `RT-29`, after the normal speech baseline in `RT-28`.

Proposed reproduction:

1. Record the active TTS engine, voice, and measured input-length limit.
2. Use original text above that limit with identifiable markers near the beginning, boundary, and suffix. Include an ordinary paragraph as a control.
3. Capture actual engine submissions using a controlled test engine, or retain an auditable speech observation. Trace the segmentation result rather than assuming one paragraph becomes one utterance.
4. Compare submitted/spoken text and highlight progression with the complete source text.

**Expected:** supported content is segmented without silently dropping its suffix. **Needed to confirm:** an over-limit segment reaches this queue in a real document workflow. A branch that is unreachable after segmentation is not a reproduced speech-loss defect.

Suggested subject: **[TTS] Text after <boundary> is skipped with <engine/build>**.

## A documentation question that can be asked now

**MD-01** is a sourced inconsistency/ambiguity in Pro privacy wording, independent of APK behavior. The [prepared clarification message](reporting.md#privacy-policy-clarification-draft) asks which clauses apply. It does not allege undisclosed traffic. It is suitable as a documentation inquiry without first proving a runtime data flow.

## Promotion and submission

Use the [reporting guide](reporting.md) and [bug form](../.github/ISSUE_TEMPLATE/bug-report.yml). Add the build, exact input hash, steps, expected/actual outcome, repetitions, relevant evidence, and remaining limitation. Retain an unconfirmed candidate as such when its experiment is blocked or disproved; do not relabel it to meet a report-count target. No email or issue is sent by creating this page.

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
