---
type: TestPlan
title: Reader application test matrix
description: Reproducible functional and quality-attribute workflows, required inputs, and explicit criteria for recording application results.
tags: [readers, android, testing, reliability, accessibility]
timestamp: 2026-11-21T00:00:00Z
---

# Application test matrix

**This is a test specification, not a test result.** Each case below is an execution target. A completed run must identify the cases it actually exercised; creating this matrix does not increase the application-pass count. See [coverage](coverage.md) for the current evidence and [fixture verification](testing-fixtures.md) for the separately tested input corpus.

## Run contract

Record the application/package, version, artifact SHA-256 or source commit, acquisition channel, Android/API/ABI, emulator or physical device, viewport, font/display scale, locale, reading mode, relevant permissions, and test timestamp. Use the explicitly selected disposable audit AVD and an explicit ADB serial. Cloud and TTS cases additionally need the backend or engine/voice identity.

For each executed case retain:

1. Initial state and exact input hash. A modified output gets a new hash; retain the original input.
2. Numbered actions, expected result, actual result, and observed repetitions.
3. A relevant screenshot, structured state readback, saved output, or minimal diagnostic excerpt.
4. **Pass**, **fail**, **blocked**, or **not run**. A blocked setup is not an application failure. A screenshot of a control is not proof that the control's operation succeeded.
5. The limitation: what the observation does and does not establish. A result on this [supplied APK](../data/artifact.json) is not an official-release finding.

Core fixture names refer to [the committed manifest](../fixtures/manifest.json). Literal-search, long-speech, and malformed-input cases use the separate [scenario manifest](../data/scenario-fixtures.json) and [scenario guide](testing-scenarios.md). **Additional input required** means neither corpus supplies the necessary case. Such a row stays unexecuted until that input is supplied and identified. Acceptance conditions are proposed test expectations, not unverified claims that a product promises every capability.

## Opening, rendering, and navigation

| ID | Input / setup | Actions and observable acceptance condition |
|---|---|---|
| RT-01 | Exact supplied APK; fresh audit AVD | Attempt installation through the platform package manager; record its actual response. If accepted, read back the installed package/version and launch the declared main activity. Preserve installation rejection as a platform result without modifying/re-signing the input. |
| RT-02 | `plain-text` | Open the document from the app, return to the library, and reopen. The known title/content appears and controls remain usable. Record the chosen permission flow. |
| RT-03 | `plain-text`; document-provider URI | Use Android Open With with a temporary read grant, background/resume, then reopen. Distinguish a transient URI's lifetime from persistence of an imported copy; record which workflow the app offers. |
| RT-04 | `navigation` | Follow the page-1 link to page 3 and the page-3 link to page 1; use the outline and available back/history action. Check the destination text, not just the numeric indicator. |
| RT-05 | `mixed-geometry` | Visit all four pages and rotate the device. Inspect page orientation, crop, navigation, and fit mode for each media box; record screenshots for all geometries. |
| RT-06 | `plain-text`, `scanned-image-only` | Toggle the documented double-tap zoom option; double-tap at a known point, pan, and toggle off. Verify the actual zoom/pan behavior and distinguish document gestures from system accessibility gestures. |
| RT-07 | `long-document` | Jump to pages 1, 50, and 100, close, and reopen. Compare the page markers with the displayed positions and record the restored location. |
| RT-08 | `two-columns` | Open every available PDF reading/reflow mode. Inspect column order, selection order, mode switching, and location preservation. A content-stream-order result does not establish arbitrary layout reconstruction. |
| RT-09 | `scanned-image-only` | Open the page and try selection, search, and speech/reflow if available. The absence of a text layer should be understandable; failure to extract text is not itself an OCR defect where OCR is unsupported. |
| RT-10 | `tiny-original` | Open both spine chapters, use forward/back chapter links and the contents list, then change font size and reopen. Check content and position retention separately from laid-out page count. |

## Search, annotations, export, and persistence

| ID | Input / setup | Actions and observable acceptance condition |
|---|---|---|
| RT-11 | `plain-text`, `long-document` | Search `lighthouse-427` and `LONG-DOC-PAGE-100`; activate results and confirm the target text. Record case/whole-word/direction settings. |
| RT-12 | `rt12-literal-search-text`, `rt12-literal-search-pdf` from the scenario manifest | Search `a.b`, `a+b`, and `[x]`, then an invalid regex only if the UI offers regex or accepts that syntax. Compare the labeled positive and negative rows; record intended search mode, visible error, recovery, and the next successful search. Motivated by APK-SEARCH-001. |
| RT-13 | `long-document`; larger input if needed | Start a search, cancel, and immediately perform another action/search. Measure cancellation and UI response separately. Do not infer interruptibility of every regex/extraction operation from this one input. |
| RT-14 | `annotations` copied to a writable test folder | Open the six standard annotations, inspect the note, create/edit/delete a new mark, save, close, and reopen. Compare durable objects and geometry in an independent reader/parser. |
| RT-15 | `annotations`, `mixed-geometry` writable copies | Add markup to a rotated page, change mode/zoom, save, and reopen elsewhere. Verify its location against the original text/page; screenshots alone do not establish portable PDF objects. |
| RT-16 | `acroform` writable copy | Change the text, checkbox, and choice values; explicitly save and reopen in the app and an independent viewer/parser. Distinguish appearance changes from durable field values. |
| RT-17 | `password-protected` | Try empty and incorrect passwords, cancel, then enter public test password `reader-lab`. The wrong attempts must not reveal the content; the correct attempt should show `PASSWORD-OPEN-271`. This tests RC4-128 revision 3 only. |
| RT-18 | Writable PDF plus a controlled unwritable destination | First prove a normal save. Make only the disposable destination unavailable, save a new mark, and inspect dirty state, feedback, and durable bytes. Restore access and retry. Motivated by APK-PDF-002; setting up a real write failure is required. |
| RT-19 | `tiny-original` with synthetic highlights/notes | Export using the existing reader-specific format, inspect the output, and import into a separate test copy. Compare count, text, color/style, and anchors; repeated import should have a recorded duplicate policy. |
| RT-20 | Synthetic notes; controlled failing export destination | First verify a normal export, then cause the destination write to fail and compare the reported outcome with file existence/content. Motivated by APK-NOTE-002; a dialog opening is not an export-success test. |
| RT-21 | One synthetic quote | Share as an image to a controlled receiver. Compare actual encoded bytes, filename extension, declared MIME, and receiver display. Motivated by APK-NOTE-003; a `.jpg` name alone does not reveal encoding. |
| RT-22 | Additional synthetic export exceeding 80,000 characters | Invoke text sharing and test the offered file/clipboard alternative. Compare complete text length and beginning/end markers. The existing fallback's presence is not proof of lossless output. |

## Library, backup, synchronization, and speech

| ID | Input / setup | Actions and observable acceptance condition |
|---|---|---|
| RT-23 | `tiny-original` with saved state | Rename/move the fixture, use the v10.8 relink workflow, and verify progress, highlights, notes, and bookmarks. Test a second file with the same name but different content separately. |
| RT-24 | Small synthetic library | Back up, record archive/output hash, restore to a clean test installation, and compare book metadata, settings, notes, and missing-file handling. A created archive is not a successful restore. |
| RT-25 | Two test installations and a disposable cloud namespace | Make different offline notes on each, reconnect in both orders, and compare final note sets, position, deletion state, and visible conflicts. Record position-sync and annotation-sync completion separately. |
| RT-26 | Controlled cloud backend and equal-length valid cover images | Replace a disposable cover with a visibly different, decodable image of the same byte length and a newer modification time; test cover upload and download independently. Compare server/client bytes, transfer-list selection and displayed cover. Motivated by the cover-scoped follow-up to APK-SYNC-002; other sync workflows remain unestablished. |
| RT-27 | Controlled backend with transfer-failure injection | Create a note, fail the upload, restart/resume, restore connectivity, and confirm eventual durable delivery without losing the pending change. Motivated by APK-SYNC-003; do not use a personal cloud account for fault injection. |
| RT-28 | Installed TTS engine; `plain-text`, `two-columns` | Start, pause, resume, and stop speech. Check sentence/page progression and visible selection against audible output or a controlled test engine's utterance log. Record engine and voice. |
| RT-29 | `rt29-long-paragraph` from the scenario manifest; controlled TTS engine | Measure the speech-input limit and confirm the fixture exceeds it before testing. Verify every segment and the beginning/middle/suffix markers are submitted/spoken and selected correctly. Trace segmentation before concluding truncation is reachable. Motivated by APK-TTS-002. |
| RT-30 | Working TTS baseline | Turn screen off/on, background/resume, and introduce/release audio focus. Record reader and engine settings and exact interruption behavior; absence of speech-engine provisioning is a blocked case. |

## Accessibility, quality attributes, and robustness

| ID | Input / setup | Actions and observable acceptance condition |
|---|---|---|
| RT-31 | `plain-text`; TalkBack installed/enabled in audit AVD | Open a book, navigate controls, search, and reach a result using TalkBack. Record inaccessible controls, labels, focus order, and task completion. TTS playback is not a substitute. |
| RT-32 | Same document; large font/display scaling | Exercise library, settings, dialogs, search, and export at baseline and enlarged scale. Record clipped labels, unreachable actions, scrolling, and focus, with viewport/density/fontScale. |
| RT-33 | Keyboard input in audit AVD | Open, navigate, search, dismiss dialogs, and return to the library without touch. Record key mappings and focus visibility; do not generalize to unsupported input devices. |
| RT-34 | `plain-text`, `long-document`, `scanned-image-only` | Measure five cold and five warm open-to-first-readable-page samples under a defined reset/cache policy. Record raw values, median/range, device load, and failures. A launcher timing alone is not first-readable-page latency. |
| RT-35 | Fixed open/page/close workload and sample schedule | Measure process memory before, during, and after repeated reads. Record workload, OS counters, duration, and whether memory settles; a single high reading is not a demonstrated leak. |
| RT-36 | `rt36-empty`, `rt36-truncated`, `rt36-invalid-header`, and `rt36-healthy-control` from the scenario manifest | Attempt each malformed input independently, retain exact hashes and platform/app diagnostics, and verify recovery by opening the healthy control afterwards. Record file-picker rejection separately from reader-parser rejection. A parser's intentional rejection is not a crash. |

## Comparison discipline

Run the same case only where the comparator's declared product scope supports it. Mark exclusions explicitly: the simplified MuPDF Android Viewer intentionally omits form filling and annotation editing; Book's Story's inspected PDF path is text extraction rather than original-page rendering. A desktop feature can motivate a request without supplying an Android pass result. The [feature matrix](feature-matrix.md) and pinned dossiers establish those boundaries.

For a confirmed bug report, repeat the smallest failing case on an authenticated official build and attach its actual evidence. For a feature request, describe the desired workflow and acceptance condition even when the current behavior remains unknown. These are different submission types.

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
