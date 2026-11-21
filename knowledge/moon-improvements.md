---
type: Research
title: Moon+ Reader improvement backlog
description: Overview and navigable catalog of 64 actionable draft proposals grounded in existing capabilities and dated evidence.
tags: [moon-reader, proposals, reliability, interoperability, accessibility, research]
timestamp: 2026-11-21T00:00:00Z
---

# Moon+ Reader: 64 improvement proposals

**Exactly 64 distinct proposals, MOON-001 through MOON-064, all `proposal` / `draft`.** The [JSON backlog](../data/moon-improvements.json) is the canonical detailed record: existing capability, baseline relationship, rationale, requested change, measurable acceptance criteria, sources and limitations. This page is its overview and compact navigation catalog.

**Evidence snapshot: 2026-11-21.** The corpus preserves and reviews the original 33 entries and adds 31. It spans 12 categories, with **30 high**, **31 medium** and **3 low** suggested priorities. Priority indicates investigation or product value, not confirmed defect severity. Acceptance scenarios and numerical budgets are proposed checks; catalog validation does not execute them.

## Read the evidence correctly

- The [official baseline](moon-baseline.md#existing-capability-baseline) already documents **TTS, background speech, PDF annotations and forms, export/backup, cloud sync, typography and publisher-formatting preview**. Its [v10.8 notes](moon-baseline.md#observed-v108-release-notes) already advertise double-tap zoom and missing-file relinking.
- The [supplied-artifact analysis](apk-analysis.md#implementation-map) additionally establishes existing **PDF text reflow, settings/function search and Readwise-upload paths**. Every APK claim in this backlog applies only to the unknown-provenance artifact with SHA-256 **`e2c0ef649413b2f6671598ac8b027d582ba220e38738f2e253694289ea20e1fc`**. Its [identity record](../data/artifact.json) records failed signature verification; an authenticated public download URL was not established. These observations do not authenticate or demonstrate defects in the official Play build.
- Comparator ideas reuse the completed [Android research](alternatives-android.md) and [desktop/web research](alternatives-desktop-web.md), with their [Android](../data/alternatives-android.json) and [desktop/web](../data/alternatives-desktop-web.json) structured inventories. Documentation and pinned source observations retain their original boundaries; they are not comparative runtime measurements.
- Each JSON proposal inherits the snapshot's `observed_at`. Its `baseline_refs` resolve to `MF-*` entries in the [official records](../data/moon-baseline.json) or `APK-*` findings in the [static ledger](../evidence/static/observations.json). Primary URLs and comparator commit pins remain in the detailed sources. Relative source paths there are repository-root-relative.

**Unknown does not mean absent.** Check the current official workflow before submitting a refinement. The [evidence contract](design.md#evidence-contract) distinguishes a desired outcome, a static concern and a reproduced application defect.

## Recommended first submissions

Use the [reporting guide and verified channels](reporting.md#verified-official-channels) to prepare one focused packet at a time. These recommendations are **unsent drafts**:

1. **[MOON-056](#moon-056): Pro policy wording.** The existing [clarification draft](reporting.md#privacy-policy-clarification-draft) can ask about the dated wording discrepancy without alleging undisclosed traffic.
2. **[MOON-002](#moon-002): truthful annotation-export completion.** Prioritize a real failed-destination reproduction. The recorded helper follow-up strengthens the static error-propagation concern; durable bytes and official-build feedback still need comparison before a bug claim.
3. **[MOON-004](#moon-004): same-size cover updates.** The [focused follow-up](apk-analysis.md#focused-verification-candidates) supports a narrow cover-transfer experiment. Keep the request cover-scoped; the unresolved shared worker does not establish equivalent behavior for notes, positions or book files.
4. **[MOON-025](#moon-025): an export compatibility contract.** Existing `.mrexpt` export and Readest import make a versioned, identity-aware format discussion useful. Present it as an interoperability refinement and check existing specifications first.
5. **[MOON-041](#moon-041): sync completion by data type.** The documented position-first, annotation-later sequence supplies a concrete status-design question after checking the current status UI.

Native PDF save outcomes ([MOON-001](#moon-001)) and over-limit TTS reachability ([MOON-005](#moon-005)) are further focused reproduction priorities. The catalog itself supplies prospective outcomes, not the missing execution evidence.

## Catalog

**Kind:** **E** = extension (**53**); **R** = reliability candidate (**7**); **N** = new-capability candidate (**4**, availability unverified). These correspond exactly to the JSON `relationship_to_baseline` values. An R entry is a conditional concern, not a reproduced defect; an N entry is not an absence claim.

Jump by category:

[Reliability (6)](#moon-001) · [PDF (10)](#moon-007) · [Search (8)](#moon-017) · [Export/migration (10)](#moon-025)  
[EPUB/typesetting (6)](#moon-035) · [Sync (4)](#moon-041) · [Library (4)](#moon-045) · [Accessibility (4)](#moon-049)  
[TTS (3)](#moon-053) · [Privacy (3)](#moon-056) · [Performance (3)](#moon-059) · [Support (3)](#moon-062)

Each ID opens its detailed JSON record at the corresponding source line. The stable `MOON-*` value is the record identifier if later edits move those lines.

| ID / detail | Area | Priority | Kind | Proposal |
|---|---|---|---|---|
| <a id="moon-001"></a>[MOON-001](../data/moon-improvements.json#L8) | Reliability | High | R | Retain PDF dirty state until a save succeeds |
| <a id="moon-002"></a>[MOON-002](../data/moon-improvements.json#L32) | Reliability | High | R | Report annotation export success only after a durable write |
| <a id="moon-003"></a>[MOON-003](../data/moon-improvements.json#L56) | Reliability | High | R | Persist a retryable outbox for failed note uploads |
| <a id="moon-004"></a>[MOON-004](../data/moon-improvements.json#L80) | Reliability | High | R | Detect same-size cover revisions during synchronization |
| <a id="moon-005"></a>[MOON-005](../data/moon-improvements.json#L104) | Reliability | High | R | Chunk over-limit TTS text without dropping the remainder |
| <a id="moon-006"></a>[MOON-006](../data/moon-improvements.json#L128) | Reliability | High | E | Recover unfinished note edits after lifecycle interruption |
| <a id="moon-007"></a>[MOON-007](../data/moon-improvements.json#L149) | PDF | High | E | Preserve multi-column reading order in PDF text reflow |
| <a id="moon-008"></a>[MOON-008](../data/moon-improvements.json#L172) | PDF | High | E | Keep reflow selection and annotations anchored to PDF pages |
| <a id="moon-009"></a>[MOON-009](../data/moon-improvements.json#L196) | PDF | Medium | E | Explain per-page PDF text availability and reflow fallback |
| <a id="moon-010"></a>[MOON-010](../data/moon-improvements.json#L220) | PDF | High | E | Preserve annotation geometry through crop and rotation |
| <a id="moon-011"></a>[MOON-011](../data/moon-improvements.json#L241) | PDF | High | E | Round-trip supported PDF form values across viewers |
| <a id="moon-012"></a>[MOON-012](../data/moon-improvements.json#L262) | PDF | Medium | E | Make PDF handwriting and annotation undo transactional |
| <a id="moon-013"></a>[MOON-013](../data/moon-improvements.json#L283) | PDF | High | E | Keep glyph and transparency output consistent across PDF backends |
| <a id="moon-014"></a>[MOON-014](../data/moon-improvements.json#L307) | PDF | Medium | E | Preserve figures when applying PDF night themes |
| <a id="moon-015"></a>[MOON-015](../data/moon-improvements.json#L327) | PDF | Medium | E | Persist page-group crop and zoom profiles |
| <a id="moon-016"></a>[MOON-016](../data/moon-improvements.json#L348) | PDF | Low | N | Offer an independently navigable two-document workspace |
| <a id="moon-017"></a>[MOON-017](../data/moon-improvements.json#L372) | Search | High | E | Make literal and regular-expression search explicit modes |
| <a id="moon-018"></a>[MOON-018](../data/moon-improvements.json#L396) | Search | High | R | Recover from invalid patterns and cancel expensive searches |
| <a id="moon-019"></a>[MOON-019](../data/moon-improvements.json#L420) | Search | Medium | E | Normalize search text while preserving exact highlight offsets |
| <a id="moon-020"></a>[MOON-020](../data/moon-improvements.json#L444) | Search | Medium | E | Scope searches to chapters or page ranges with stable return context |
| <a id="moon-021"></a>[MOON-021](../data/moon-improvements.json#L468) | Search | Medium | E | Stream capped search results with honest completion counts |
| <a id="moon-022"></a>[MOON-022](../data/moon-improvements.json#L492) | Search | Medium | N | Offer an opt-in offline full-text index for selected shelves |
| <a id="moon-023"></a>[MOON-023](../data/moon-improvements.json#L516) | Search | Medium | E | Combine annotation text and metadata filters in a review view |
| <a id="moon-024"></a>[MOON-024](../data/moon-improvements.json#L540) | Search | Medium | E | Deep-link settings search results with aliases and context |
| <a id="moon-025"></a>[MOON-025](../data/moon-improvements.json#L564) | Export/migration | High | E | Version the annotation export schema and stable identities |
| <a id="moon-026"></a>[MOON-026](../data/moon-improvements.json#L588) | Export/migration | High | E | Reconcile migration anchors with exact and fallback outcomes |
| <a id="moon-027"></a>[MOON-027](../data/moon-improvements.json#L612) | Export/migration | Medium | E | Export selected books as configurable study documents |
| <a id="moon-028"></a>[MOON-028](../data/moon-improvements.json#L636) | Export/migration | High | E | Preserve Unicode and delimiter-like text through annotation round trips |
| <a id="moon-029"></a>[MOON-029](../data/moon-improvements.json#L660) | Export/migration | Medium | E | Make Readwise delivery resumable and duplication-aware |
| <a id="moon-030"></a>[MOON-030](../data/moon-improvements.json#L684) | Export/migration | Medium | R | Align quote-image encoding, filename and share MIME type |
| <a id="moon-031"></a>[MOON-031](../data/moon-improvements.json#L708) | Export/migration | Medium | E | Deliver large text shares as complete readable attachments |
| <a id="moon-032"></a>[MOON-032](../data/moon-improvements.json#L732) | Export/migration | Medium | E | Distinguish editable PDF exports from flattened copies and sidecars |
| <a id="moon-033"></a>[MOON-033](../data/moon-improvements.json#L756) | Export/migration | Medium | N | Export citation-ready notes with source-passage backlinks |
| <a id="moon-034"></a>[MOON-034](../data/moon-improvements.json#L780) | Export/migration | High | E | Preview and verify whole-library backup restoration |
| <a id="moon-035"></a>[MOON-035](../data/moon-improvements.json#L801) | EPUB/typesetting | High | E | Make publisher-style and reader-style precedence inspectable |
| <a id="moon-036"></a>[MOON-036](../data/moon-improvements.json#L822) | EPUB/typesetting | Medium | E | Map embedded and custom font faces without synthetic-style surprises |
| <a id="moon-037"></a>[MOON-037](../data/moon-improvements.json#L843) | EPUB/typesetting | High | E | Keep EPUB tables and code blocks readable at large type |
| <a id="moon-038"></a>[MOON-038](../data/moon-improvements.json#L864) | EPUB/typesetting | High | E | Honor language-specific shaping, direction and hyphenation |
| <a id="moon-039"></a>[MOON-039](../data/moon-improvements.json#L885) | EPUB/typesetting | High | E | Restore exact EPUB passages after repagination |
| <a id="moon-040"></a>[MOON-040](../data/moon-improvements.json#L906) | EPUB/typesetting | Medium | E | Retain popup-footnote context and nested return navigation |
| <a id="moon-041"></a>[MOON-041](../data/moon-improvements.json#L927) | Sync | High | E | Expose sync completion per data type and destination |
| <a id="moon-042"></a>[MOON-042](../data/moon-improvements.json#L948) | Sync | High | E | Resolve concurrent annotation edits and deletions explicitly |
| <a id="moon-043"></a>[MOON-043](../data/moon-improvements.json#L969) | Sync | Medium | E | Keep reading-position history before applying remote jumps |
| <a id="moon-044"></a>[MOON-044](../data/moon-improvements.json#L990) | Sync | High | E | Resume cloud book downloads without exposing partial files |
| <a id="moon-045"></a>[MOON-045](../data/moon-improvements.json#L1011) | Library | High | E | Distinguish duplicate books from changed editions before merging |
| <a id="moon-046"></a>[MOON-046](../data/moon-improvements.json#L1032) | Library | Medium | E | Make bulk library organization reversible and previewable |
| <a id="moon-047"></a>[MOON-047](../data/moon-improvements.json#L1053) | Library | Medium | E | Make OPDS navigation and acquisition compatibility explicit |
| <a id="moon-048"></a>[MOON-048](../data/moon-improvements.json#L1074) | Library | High | E | Recover unavailable library locations without discarding reading state |
| <a id="moon-049"></a>[MOON-049](../data/moon-improvements.json#L1095) | Accessibility | High | E | Expose document structure to assistive navigation |
| <a id="moon-050"></a>[MOON-050](../data/moon-improvements.json#L1116) | Accessibility | High | E | Make annotation editing and status feedback usable with TalkBack |
| <a id="moon-051"></a>[MOON-051](../data/moon-improvements.json#L1137) | Accessibility | High | E | Keep reading controls operable at large system text sizes |
| <a id="moon-052"></a>[MOON-052](../data/moon-improvements.json#L1158) | Accessibility | Medium | E | Provide complete remappable keyboard and switch navigation |
| <a id="moon-053"></a>[MOON-053](../data/moon-improvements.json#L1179) | TTS | High | E | Make background TTS interruption and media-control policy predictable |
| <a id="moon-054"></a>[MOON-054](../data/moon-improvements.json#L1200) | TTS | Medium | E | Resolve TTS language and offline voice availability explicitly |
| <a id="moon-055"></a>[MOON-055](../data/moon-improvements.json#L1221) | TTS | Medium | E | Keep narration position and sentence navigation synchronized |
| <a id="moon-056"></a>[MOON-056](../data/moon-improvements.json#L1242) | Privacy | Medium | E | Reconcile Pro privacy disclosures by actual data flow |
| <a id="moon-057"></a>[MOON-057](../data/moon-improvements.json#L1263) | Privacy | Medium | E | Support selected-file and folder access for core reading tasks |
| <a id="moon-058"></a>[MOON-058](../data/moon-improvements.json#L1284) | Privacy | Medium | N | Protect backup and sync packages independently of startup lock |
| <a id="moon-059"></a>[MOON-059](../data/moon-improvements.json#L1305) | Performance | Medium | E | Reduce cold-open time to the first usable reading passage |
| <a id="moon-060"></a>[MOON-060](../data/moon-improvements.json#L1326) | Performance | Medium | E | Bound retained document resources across repeated reading sessions |
| <a id="moon-061"></a>[MOON-061](../data/moon-improvements.json#L1347) | Performance | Low | E | Offer a measured low-refresh reading profile for e-ink screens |
| <a id="moon-062"></a>[MOON-062](../data/moon-improvements.json#L1368) | Support | Medium | E | Prepare minimal redacted diagnostics for a chosen support problem |
| <a id="moon-063"></a>[MOON-063](../data/moon-improvements.json#L1389) | Support | Medium | E | Publish a versioned format-by-mode capability and fallback matrix |
| <a id="moon-064"></a>[MOON-064](../data/moon-improvements.json#L1410) | Support | Low | E | Publish build-specific changes with traceable resolution status |

## Scope and follow-through

Distinctness is by requested outcome, not just title: PDF persistence, local annotation export, Moon note sync, Readwise delivery and cloud book downloads have separate success boundaries. Likewise, local repagination, remote-position decisions and cross-reader migration have different identity and recovery contracts. Document semantics, editor focus, large-text layout and keyboard/switch access are independently checkable accessibility tasks. A shared implementation may satisfy several records; consolidate overlapping submissions when that is demonstrated.

The original findings and acceptance detail remain in the JSON and linked evidence. Current official-build availability, exhaustive duplicate searches, provider behavior, assistive-technology interoperability and performance budgets require focused verification. Follow [the submission and follow-up process](reporting.md#submission-and-follow-up) when an individual report is requested, keeping proposed, reproduced, submitted and retested states distinct.

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
