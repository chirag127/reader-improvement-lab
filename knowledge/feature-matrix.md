---
type: Comparison
title: Reader feature and implementation comparison
description: Workflow-level comparison of documented and source-observed reader capabilities, with explicit platform and test boundaries.
tags: [readers, pdf, epub, comparison, architecture]
timestamp: 2026-11-21T00:00:00Z
---

# Feature and implementation comparison

**Observation date: 2026-11-21.** This is a comparison of capabilities supported by the linked documentation and inspected source. It is not a performance ranking or a claim that every feature was exercised. Each source dossier records the exact revision and inspected files.

**D** = publisher/project documentation; **C** = inspected implementation; **U** = unresolved in this review; **Excluded** = explicitly outside that product's documented scope. An omitted feature is **U**, not an absent feature. Source evidence for the supplied Moon APK remains bound to its [unknown-provenance artifact](../data/artifact.json).

## Android and cross-platform reading workflows

| Reader | PDF and reflow | Annotation/export | Library and synchronization | Speech and input | Evidence |
|---|---|---|---|---|---|
| Moon+ Reader Pro | D: PDF controls and dual-page layout. C: Radaee document wrapper, page-text extraction and PDF text-reflow path. OCR/reading-order quality U. | D: PDF forms, handwriting, highlights, notes, backup. C: `.mrexpt`, text/image sharing and Readwise upload; durable success U. | D: shelves, tags, OPDS/calibre, cloud state/annotation sync. C: Dropbox/Drive/FTP/WebDAV dispatch. Conflict convergence U. | D/C: Android TTS and document progression; D: headset/gesture/key controls. TalkBack completeness U. | [Official baseline](moon-baseline.md#existing-capability-baseline), [APK map](apk-analysis.md#implementation-map) |
| KOReader | D: PDF/DjVu/comics, reflowable ebooks, K2pdfopt scanned-page reflow. Bitmap rearrangement is not OCR accuracy. | C: highlights/bookmarks and Markdown/JSON/text/HTML exporters with style/color filters. | D: OPDS, calibre, Wallabag/RSS. C: provider/plugin and export seams. Universal sync parity U. | D: e-ink-oriented controls, dictionaries, typesetting. Full speech/accessibility parity U. | [KOReader dossier](alternatives-android.md#31-koreader--broad-reading-and-e-ink-reference) |
| Librera Reader | D: PDF reflow, page splitting/crop. C: PDFium, foliate/WebView and variant-specific MuPDF paths. | D/C: notes, PDF markup and save contracts. D: settings export and session backup. | D: folder discovery, metadata filters, OPDS, calibre and Drive synchronization; flavor applicability U. | D: TTS, configurable tap/volume controls, musician autoscroll; C: read-ahead integration. | [Librera dossier](alternatives-android.md#32-librera-reader--android-all-in-one-reference) |
| MJ PDF | D/C: PDF page modes and incremental text-mode reflow; no claimed non-PDF support. | D/C: embedded highlights/notes, signatures/forms, annotation lists and plain-text export. | D: recent/library/folder views, relocation-aware history, shared-file copy choices. Cloud-sync parity U. | D: autoscroll, zoom lock; TTS is a roadmap enhancement at the inspected pin. | [MJ PDF dossier](alternatives-android.md#33-mj-pdf--pdf-focused-alternative) |
| Orion Viewer | D: PDF/DjVu/XPS/TIFF/comic page viewing, crop/zoom, LTR/RTL navigation. Reflow U. | D: bookmarks and selection; broad annotation editing/export U. | D: file manager and recent documents. Cross-device synchronization U. | D: configurable tap zones/hardware keys, dictionary handoff. TTS U. | [Orion dossier](alternatives-android.md#34-orion-viewer--fixed-page-and-navigation-specialist) |
| MuPDF Android Viewer | C: fitz rendering and reflowable-document relayout. These do not establish PDF text-reflow parity. | Excluded: annotation editing and form filling in this simplified viewer. C: links, outline and search. | C: SAF picker, Open With, saved position and navigation history. Full library/cloud U. | C: pinch/scroll/edge taps; empty long-press handler. TTS U. | [Viewer dossier](alternatives-android.md#35-mupdf-android-viewer--simplified-library-and-app) |
| Book's Story | C: PDFBox text-to-paragraph conversion. Original PDF page layout and scan OCR are not established. | C: selection/copy/share/search/translation. Broad PDF markup U. | D/C: categories, SAF discovery, Room-backed book/content storage. Cloud U. | D/C: Compose layouts, typography, ruler and reading overlays. TTS U. | [Book's Story dossier](alternatives-android.md#36-books-story--native-compose-reader) |
| Readest | D: PDF and numerous ebook formats; two-document Parallel Read. PDF reflow details U. | D/C: highlights/notes/bookmarks; UI-connected Moon/ReadEra import. Standard PDF writeback is an existing request with incomplete absence search. | D/C: library/shelf search, OPDS/calibre, provider-based file/state sync and KOReader interoperability; entitlements vary. | D: multilingual TTS, keyboard/screen-reader support and media-overlay read-along; accessibility not measured. | [Readest dossier](alternatives-android.md#37-readest--cross-platform-reader-with-an-observed-moon-import-path) |
| Anx Reader | D: PDF and ebook formats, configurable text layout. Exact PDF mode semantics U. | D: notes/color filters and TXT/Markdown/CSV exports. | D: WebDAV books/notes/position and on-demand cloud files. OPDS explicitly in progress. | D: TTS voice/speed/tone/sleep timer, translation, reading statistics. | [Anx dossier](alternatives-android.md#38-anx-reader--additional-cross-platform-alternative) |

## Desktop and web workflow references

These ten entries are adjacent references for browser embedding, academic reading, accessibility, and document review. The [desktop/web dossier](alternatives-desktop-web.md) records release-versus-development distinctions and pins; its [inventory](../data/alternatives-desktop-web.json) retains per-feature sources. These are documented or source-observed capabilities, not installed-application test results.

| Reader / library | Relevant reading workflow | Annotation, search, or accessibility reference | Important boundary |
|---|---|---|---|
| PDF.js | C: worker-backed PDF loading and rendering, text and structure layers | C: normalized search, editable highlights/ink/text, form storage, semantic table/heading relationships | A browser library/viewer, not a complete Android library or cloud service. DOM semantics require actual assistive-technology checks. |
| Okular | D/C: format generators, desktop shell, separate mobile component | D: native PDF annotations, table selection and cryptographic signatures. C: annotation undo commands and asynchronous generation | Optional backends and desktop/mobile builds differ. The reviewed development pin is not the stable binary. |
| Sioyek | D: academic reference previews, smart jumps, marks and cross-location portals | D/C: highlight search, page-range and literal/regex search, checksum-associated reading state | Keyboard/multi-window desktop workflows need adaptation for phones. Stable and development database/toolchain behavior differs. |
| Zotero Reader | D: PDF/EPUB/HTML reading; host documentation describes Reading Mode and read-aloud | D/C: annotations linked to research notes/citations, PDF annotation export, filters and undo. C: native/semantic search sessions | Reader component version differs from the host application version. Host sync/database and semantic-text production were not fully reviewed. |
| SumatraPDF | D: Windows multi-format and portable reading, tabs and command palette | D: annotation saving, search snippets and navigation commands in rolling documentation | Some documented capabilities are 3.7/pre-release additions, not established in stable 3.6.1. Documentation-level review here. |
| GNOME Papers | D: adaptive fixed-layout reader with sidebar search and thumbnails | D: ink/free-text markup, signature tools and evolving screen-reader announcements | GNOME/mobile-friendly does not mean Android. Accessibility is documented, not certified by this investigation. |
| Evince | D: fixed-layout backends, fit modes, dual-page view and printing | D: annotations/forms, keyboard navigation, SyncTeX and booklet workflows | Backend availability varies. Evince and Papers are separately maintained projects, not interchangeable names. |
| calibre | D: library/conversion plus configurable ebook viewer and Content server | D: library-wide annotations, precise location links, rich search and read-aloud | PDF conversion is not native PDF annotation parity. The conversion manual and newer column-detection release claim require empirical reconciliation. |
| Foliate | D: GNOME ebook/PDF reading, typography and OPDS 2.0 | D: annotations, in-book search, dictionaries and optional speech-dispatcher TTS | Per-format capabilities are untested; bundled PDF.js does not expose every generic PDF.js feature automatically. |
| Thorium Reader | D: desktop EPUB/PDF, accessible-book/audio formats and authenticated OPDS | D: accessibility metadata, keyboard/screen-reader support, media overlays and shareable annotations | Production LCP support needs an additional component outside the public source. PDF-specific parity and the separate iOS product are not established by this desktop pin. |

## Commercial and historical comparison points

The [commercial/legacy source dossier](moon-baseline.md#commercial-and-legacy-android-comparators) owns the source dates, package identities and entitlement qualifications.

| Product | Most relevant comparison workflow | Boundary |
|---|---|---|
| Adobe Acrobat Reader | Liquid Mode, TalkBack guidance, annotations/forms and paid OCR/editing | The detailed Liquid Mode help is dated 2025 and describes server processing and input limits. Current runtime behavior remains untested. |
| Xodo | Reflow help explains when a PDF has no extractable text | Older help establishes a documented explanation pattern, not unchanged current UI or pricing. |
| Foxit PDF Editor | Versioned 2026.4.0 manual documents copying and annotating text inside reflow | This demonstrates a documented mode combination; mobile/desktop and paid/free scope remain distinct. |
| ReadEra / Premium | Library duplicate handling, moved-file state and cross-book notes; Premium sync/background speech | Proprietary full app with separate GPL renderer helpers. The advertised large-library test is not this investigation's benchmark. |
| FBReader / Premium | Text-format reading/TTS and embedded-versus-plugin PDF handling | Current Android source is closed; old GPL source is not the current app. Official documentation excludes PDF/DjVu read-aloud. |
| EBookDroid | Historical fixed-page reader and format support | Source transition after 1.6.x and uncertain current distribution prevent current-app source equivalence claims. |
| PDF Reader Pro | Android PDF office/editor feature reference and name-disambiguation candidate | Separate PDF Technologies product. Full current Android source was not established; it is not automatically the user's intended “Reader Pro.” |

## Compare the code at the correct boundary

| Inspected product | Actual implementation boundary | Useful improvement location |
|---|---|---|
| Supplied Moon APK | Activity-centric reading flows; SQLite note model; Radaee PDF wrapper; provider dispatch; Android TTS | Follow each operation through durable save and retry state, then reproduce failures on an official build. A large class alone is not a user-visible defect. |
| KOReader | Lua reader modules, document registry and exporter plugins | MIME registration and OPDS acquisition; export metadata/templates. |
| Librera | `CodecDocument` interface and renderer adapters with WebView/native thread coordination | Per-flavor compatibility, CFI persistence and measured cold-open/indexing work. |
| MJ PDF | Kotlin application/Room data, Java viewer, C++ PDFium, shared annotation-list logic | Text extraction ownership, native-resource cleanup, export formats and responsive library UI. |
| MuPDF Android Viewer | Java chooser/activity/view and fitz core facade | Link sentinel semantics, navigation history and content-URI sharing. |
| Book's Story | SAF ingestion → parser `Flow` → typed nodes/Room → Compose reader | Parser/rendering parity and accurate format claims; maintainers request reports/translations rather than code PRs. |
| Readest | React/Next frontend, Tauri platform services, sync-provider contracts, annotation import/conversion | Migration reconciliation and anchoring, provider conformance and publisher-style handling. |
| PDF.js | Core parser/interpreter → display API → viewer; separate text, search, editable-annotation and structure layers | Search coverage/error status and actual browser accessibility-tree verification. |
| Okular | Shared document/generator contracts, Poppler PDF backend, annotation commands and mobile QML | Destination fit/zoom propagation, mobile fit-page behavior and shell-supplied motion policy. |
| Sioyek | C++/Qt viewer, rendering/search workers, checksum-associated SQLite state and portals | Native search-resource ownership and locale-independent geometry persistence. |
| Zotero Reader | Shared annotation manager, native/semantic search sessions and platform-specific host bridges | Ink-merge ordering, save rejection contracts and generation-safe search transitions. |

The [Android source-review sections](alternatives-android.md#4-reviewed-code-and-extension-seams), [four desktop/web implementation reviews](alternatives-desktop-web.md#3-four-pinned-implementation-reviews-and-contribution-candidates), and [APK analysis](apk-analysis.md#implementation-map) cite the exact paths. Ten alternative projects received targeted implementation review. Orion, Anx, SumatraPDF, Papers, Evince, calibre, Foliate, and Thorium received documentation/license/build review rather than application-code deep inspection. No line-for-line architectural equivalence across these products is implied.

## Quality attributes need comparable measurements

| Attribute | Test that would support a comparison | Current evidence boundary |
|---|---|---|
| Reliability | Repeat open/edit/save/reopen and interrupted-write workflows on the same fixtures | Static save/retry candidates are not confirmed failures. Fixture parsing is not app persistence. |
| Performance | Same hardware, documents/settings, cold/warm definition, repeat count and first-readable-page timing | No cross-application latency ranking has been established. |
| Memory and battery | Comparable workload duration, foreground/background state and OS measurements | Code size, package size and one launch do not establish memory/battery efficiency. |
| Accessibility | Task completion using TalkBack, keyboard and large text, with exact blocked controls | TTS and a README accessibility claim do not certify the UI. |
| Interoperability | Save or export in one app, reopen in two independent readers, compare anchors/notes/forms | Host fixtures establish known input properties; application round trips require their own results. |
| Sync correctness | Two-device edits, conflict resolution, offline queue, reconnection and deletion propagation | Cloud-provider declarations and an upstream issue do not establish convergence. |
| Offline/privacy | Exercise named operations offline and inspect scoped network/storage behavior | Permission and policy wording are declarations, not observations of actual transmission. |

## Highest-value directions

**Recommendations:** prioritize data-preserving save/export/sync behavior, reliable migration anchors, discoverable PDF mode combinations and accessibility task completion. Check current options first; several apparently missing capabilities already exist. Use a small, evidence-backed report rather than a broad claim that an application is inferior.

An application can have both reflow and annotations without supporting annotations *in reflow*. Likewise, a startup lock is not encrypted storage, scan reflow is not OCR, two-page layout is not two-document reading, and overlay annotations are not standard PDF writeback. These distinctions make requests useful to developers.

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
