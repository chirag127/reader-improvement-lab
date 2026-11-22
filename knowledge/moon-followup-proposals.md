---
type: Research
title: Moon+ Reader follow-up proposals
description: Ten additional draft reading workflows with explicit distinctions from the original 64 proposals and dated source boundaries.
tags: [moon-reader, proposals, reading, narration, study, interoperability]
timestamp: 2026-11-22T00:00:00Z
---

# Moon+ Reader: ten follow-up proposals

**MOON-065 through MOON-074 are ten desired outcomes, all `proposal` / `draft`, with medium suggested priority and three prospective acceptance criteria each.** The [detailed JSON](../data/moon-followup-proposals.json) is the canonical record of their requested changes, **30 criteria**, sources and limitations. This catalog summarizes the workflows and their distinctions from the [original 64 proposals](moon-improvements.md).

Prepared **2026-11-22**, using retained sources **observed 2026-11-21**. No fresh source retrieval or application execution is represented. Priority describes proposed workflow value, not defect severity. Current availability remains unknown: an extension acknowledges an existing capability, and a new-capability candidate identifies a baseline gap rather than proving product absence.

## Catalog

Categories identify the specific workflows in this supplement. **E** = extension; **N** = new-capability candidate with availability unverified. There are **six E** and **four N** records; all ten have **medium** suggested priority. Full requested changes and criteria live in the [JSON records](../data/moon-followup-proposals.json), keyed by the IDs below.

| ID | Desired outcome | Category | Kind | Nearest original proposals |
|---|---|---|---|---|
| [MOON-065](#moon-065) | Separate PDF page labels from physical navigation positions | PDF | E | [020](moon-improvements.md#moon-020), [033](moon-improvements.md#moon-033) |
| [MOON-066](#moon-066) | Inspect and reverse per-book narration exclusions | TTS | E | [005](moon-improvements.md#moon-005), [055](moon-improvements.md#moon-055) |
| [MOON-067](#moon-067) | Navigate authored EPUB3 audio through its text mapping | EPUB media | N | [055](moon-improvements.md#moon-055) |
| [MOON-068](#moon-068) | Preserve comic cover, spread and within-image reading order | Comics | E | [015](moon-improvements.md#moon-015), [038](moon-improvements.md#moon-038) |
| [MOON-069](#moon-069) | Route dictionary lookups with recoverable local fallback | Lookup | E | [054](moon-improvements.md#moon-054), [056](moon-improvements.md#moon-056) |
| [MOON-070](#moon-070) | Keep translations aligned with their original passages | Translation | E | [016](moon-improvements.md#moon-016) |
| [MOON-071](#moon-071) | Review chosen word meanings with independent recall state | Study | N | [023](moon-improvements.md#moon-023), [027](moon-improvements.md#moon-027), [033](moon-improvements.md#moon-033) |
| [MOON-072](#moon-072) | Explain reading-time totals and reversible session exclusions | Reading statistics | E | [043](moon-improvements.md#moon-043), [059](moon-improvements.md#moon-059) |
| [MOON-073](#moon-073) | Read temporarily with an explicit history-retention boundary | Privacy | N | [058](moon-improvements.md#moon-058), [056](moon-improvements.md#moon-056) |
| [MOON-074](#moon-074) | Print selected pages from one identifiable edit revision | Printing | N | [032](moon-improvements.md#moon-032) |

## Baselines and distinct outcomes

<a id="moon-065"></a>
### MOON-065 — Page labels and physical positions

**Existing baseline:** MF-06 covers PDF reading controls; retained runtime evidence also shows navigation and search-result activation. **Refinement:** make publication labels, physical indices and the active document agree throughout ordinary navigation, with an explicit choice for duplicate labels. MOON-020 specifies numbering for search scopes; MOON-033 specifies it for exported citations. This request covers the main navigator, slider and readout.

**Evidence boundary:** [AUX-STATUS-001](runtime-results.md#rendering-navigation-and-search) records `101/1` once while the correct text was shown in a one-page document. It concerns only supplied SHA-256 **`e2c0ef649413b2f6671598ac8b027d582ba220e38738f2e253694289ea20e1fc`**, whose [official provenance is unverified](../data/artifact.json). The JSON's 100-page-to-one-page switch is a **proposed check**, not the recorded reproduction or proven cause. [Official PDF baseline](moon-baseline.md#existing-capability-baseline) · [Primary listing](https://play.google.com/store/apps/details?id=com.flyersoft.moonreaderp&hl=en).

<a id="moon-066"></a>
### MOON-066 — Intentional narration exclusions

**Existing baseline:** MF-02/MF-06 already cover ebook and PDF speech. **Refinement:** preview included/skipped headers, footnotes or selected regions, with per-book policy and a Read everything override. Intentional pre-speech selection is distinct from retaining an accidentally truncated remainder (MOON-005) or following the spoken cursor (MOON-055). Search, copy and source text retain the excluded material.

**Source basis:** [Moon baseline](moon-baseline.md#existing-capability-baseline), [Moon FAQ](https://www.moondownload.com/faq.html), and the retained [Zotero Read Aloud description](alternatives-desktop-web.md#zotero-reader--annotations-connected-to-research-notes) from its [changelog](https://www.zotero.org/support/changelog). Zotero's documentation supplies a workflow reference; no narration scenario was executed.

<a id="moon-067"></a>
### MOON-067 — Authored EPUB audio

**Existing baseline:** MF-11 already advertises EPUB3 audio/video; it does not settle media-overlay availability. **Refinement:** navigate publication-authored clip intervals from their mapped text, restore playback through relayout and explain a missing clip locally. Authored recordings and timings have a different contract from the generated TTS cursor in MOON-055.

**Source basis:** [Moon baseline](moon-baseline.md#existing-capability-baseline), [primary listing](https://play.google.com/store/apps/details?id=com.flyersoft.moonreaderp&hl=en), [Readest's retained media-overlay claim](alternatives-android.md#37-readest--cross-platform-reader-with-an-observed-moon-import-path) in its [pinned README](https://github.com/readest/readest/blob/0882c8074215edc24e2ee5ac25e99cdccddb7e34/README.md), and [Thorium's retained description](alternatives-desktop-web.md#thorium-reader--accessible-publishing-and-library-access) from [EDRLab](https://www.edrlab.org/software/thorium-reader/). These are documentation references. The proposed 250 ms restoration tolerance is unmeasured; arbitrary audiobook alignment and DRM handling are outside scope.

<a id="moon-068"></a>
### MOON-068 — Comic spread order

**Existing baseline:** MF-01/MF-19 and the [v10.8 notes](moon-baseline.md#observed-v108-release-notes) already cover comics, dual-page layout and comic zoom. **Refinement:** coordinate a cover-alone policy, LTR/RTL spread placement and traversal of a wide image's halves, retaining image/half position after reopening. This concerns comic-image sequence and pairing rather than PDF crop/zoom profiles (MOON-015) or paragraph text direction (MOON-038).

**Source basis:** [Primary listing](https://play.google.com/store/apps/details?id=com.flyersoft.moonreaderp&hl=en) and [Orion's documented directional navigation](alternatives-android.md#34-orion-viewer--fixed-page-and-navigation-specialist), preserved in its [pinned README](https://github.com/max-kammerer/orion-viewer/blob/1adfe2da0791d1e563fd8966fc3107e9ad79fc74/README.md). No claim is made that Orion implements the proposed cover/split policy, and automatic panel detection is outside scope.

<a id="moon-069"></a>
### MOON-069 — Dictionary routing

**Existing baseline:** MF-07 establishes offline/online dictionary and translation integration. **Refinement:** route lookups by passage language or a per-book provider override, retain an edited multiword query when switching providers, and recover with an installed local dictionary. Dictionary invocation and return-to-selection are distinct from voice selection (MOON-054) and disclosure wording (MOON-056).

**Source basis:** [Moon baseline](moon-baseline.md#existing-capability-baseline), [official homepage](https://www.moondownload.com/), and the retained [calibre lookup comparison](alternatives-desktop-web.md#calibre--library-conversion-and-configurable-ebook-reading) from its [viewer manual](https://manual.calibre-ebook.com/viewer.html). Current Moon routing, publication language metadata and external result reporting remain untested; dictionary integration does not imply bundled dictionaries.

<a id="moon-070"></a>
### MOON-070 — Aligned translations

**Existing baseline:** MF-07 already covers translation. **Refinement:** pair each translated passage with its stable source anchor through out-of-order provider replies and relayout, with localized failure/retry state. This is one source and its derived text; MOON-016 concerns two independently navigated documents.

**Source basis:** [Moon baseline](moon-baseline.md#existing-capability-baseline), [official homepage](https://www.moondownload.com/), [Anx's retained side-by-side translation description](alternatives-android.md#38-anx-reader--additional-cross-platform-alternative) in its [pinned README](https://github.com/Anxcye/anx-reader/blob/0c7fc1ad4551f7dbbeba6a6468f69d830957fa2a/README.md), and [Readest's pinned translation description](https://github.com/readest/readest/blob/0882c8074215edc24e2ee5ac25e99cdccddb7e34/README.md). These sources do not establish translation quality, cost, privacy or offline availability.

<a id="moon-071"></a>
### MOON-071 — Vocabulary recall

**Existing baseline:** MF-07 already covers dictionary lookup and notes. **Refinement:** explicitly save a chosen meaning and source sentence into a hide/reveal review queue, with Remembered/Revisit actions and independent resumable recall state. This adds an interactive review task beyond annotation filtering (MOON-023), study export (MOON-027) and citation backlinks (MOON-033).

**Source basis:** [Moon baseline](moon-baseline.md#existing-capability-baseline), [official homepage](https://www.moondownload.com/), and the retained [Readest dictionary/annotation foundations](alternatives-android.md#37-readest--cross-platform-reader-with-an-observed-moon-import-path) in its [pinned README](https://github.com/readest/readest/blob/0882c8074215edc24e2ee5ac25e99cdccddb7e34/README.md). These sources establish foundations, not a recall queue's presence or absence. No learning-effectiveness or scheduling-algorithm claim is made.

<a id="moon-072"></a>
### MOON-072 — Session accounting

**Existing baseline:** MF-18 already covers per-book time/speed. **Refinement:** explain eligible and excluded session intervals, count simultaneous visual/TTS time once and make session exclusion reversible. This concerns reader duration rather than remote position history (MOON-043) or application-open latency (MOON-059).

**Source basis:** [Moon baseline](moon-baseline.md#existing-capability-baseline), [official homepage](https://www.moondownload.com/), [FAQ](https://www.moondownload.com/faq.html), and [Anx's retained statistics description](alternatives-android.md#38-anx-reader--additional-cross-platform-alternative) in its [pinned README](https://github.com/Anxcye/anx-reader/blob/0c7fc1ad4551f7dbbeba6a6468f69d830957fa2a/README.md). Neither source proves a current accounting error. The proposed timeline checks arithmetic, not human attention or comprehension.

<a id="moon-073"></a>
### MOON-073 — Temporary reading

**Existing baseline:** MF-15/MF-18/MF-12/MF-19 already cover library state, statistics, sync and startup locking. **Refinement:** visibly suppress named history, position, statistics and position-sync updates during temporary reading, while separately explaining explicitly saved notes. Normal recording resumes without retroactively recording temporary activity. This changes session-recording behavior rather than encrypting retained packages (MOON-058) or revising disclosure wording (MOON-056).

**Source basis:** [Moon baseline](moon-baseline.md#existing-capability-baseline), [primary listing](https://play.google.com/store/apps/details?id=com.flyersoft.moonreaderp&hl=en), [FAQ](https://www.moondownload.com/faq.html), and the retained [MJ PDF inventory](../data/alternatives-android.json) citing its [pinned README](https://gitlab.com/mudlej_android/mj_pdf_reader/-/blob/aef93faaa4c7fa7df373d415e1c874412cba2db5/README.md) for incognito/shared-file choices. Availability remains unknown. The boundary names Moon-managed records and does not promise zero operating-system, provider or filesystem traces.

<a id="moon-074"></a>
### MOON-074 — Snapshot-based printing

**Existing baseline:** MF-05/MF-14 already cover PDF forms, annotations and export. **Refinement:** align selected physical pages, markup inclusion and fit/actual-size choices between preview and output from one identified edit revision. Later edits either leave that snapshot identified or require preview regeneration. This print-job range/revision contract is distinct from editable, flattened or sidecar export products (MOON-032).

**Source basis:** [Moon baseline](moon-baseline.md#existing-capability-baseline), [primary listing](https://play.google.com/store/apps/details?id=com.flyersoft.moonreaderp&hl=en), [FAQ](https://www.moondownload.com/faq.html), and the retained [PDF.js review](alternatives-desktop-web.md#pdfjs--browser-viewing-and-reusable-pdf-layers) of [frozen print annotation data](https://github.com/mozilla/pdf.js/blob/57dead10694ead8fb21b97f7812fc95311a38ea1/src/display/annotation_storage.js#L323-L342). Moon's printing route is unknown. The pinned source is a design reference, not Android printing verification or a physical-output guarantee.

## Deduplication and evidence limits

Each record's `related_proposal_ids` and `distinction` identify its nearest original outcomes. The follow-up retains the ten agreed workflows; it adds no second proposal for PDF save success, form round trips, annotation outboxes, literal/regex modes, whole-library restoration, or generic privacy/support diagnostics. Those remain in the [original detailed backlog](../data/moon-improvements.json).

The ten outcomes also have separate boundaries from one another: choosing narration content differs from playing authored audio; selecting a dictionary differs from retaining a vocabulary card; translation alignment differs from two-document viewing; session accounting differs from deciding not to retain a session. Shared implementation may support several outcomes, but does not by itself make them the same user task.

The [official baseline](../data/moon-baseline.json), retained [Android](alternatives-android.md) and [desktop/web](alternatives-desktop-web.md) comparisons, and [runtime report](runtime-results.md) retain their own evidence types. `source_observed_at` is the date of those prior observations, not a new retrieval. Baseline references use original `MF-*`/`APK-*` identifiers; the incidental runtime ID is separate in `supporting_observation_ids`. All full criteria and individual caveats live in the [JSON records](../data/moon-followup-proposals.json). A syntax or record check is not execution of these workflows.

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
