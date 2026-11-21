---
type: Research
title: Android and cross-platform reader alternatives
description: Source-backed comparison of eight open-source readers, six targeted implementation reviews, and twenty-one contribution proposals.
tags: [readers, android, open-source, comparison, interoperability, research]
timestamp: 2026-11-21T14:20:22Z
---

# Android and cross-platform reader alternatives

## Scope and evidence contract

This alternatives-first comparison covers **KOReader, Librera Reader, MJ PDF, Orion Viewer, MuPDF Android Viewer, Book's Story, Readest, and Anx Reader**. It contains eight application dossiers, six targeted application-code inspections, **21 improvement proposals**, and four submission drafts. The [machine-readable inventory](../data/alternatives-android.json) indexes identities, sourced features, and reviewed code. The [proposal records](../data/alternative-proposals-android.json) provide acceptance criteria and source links for reuse; this report retains the detailed reasoning, qualifications, and duplicate-search boundaries.

**Retrieval date: 2026-11-21.** GitHub, GitLab, and raw-source responses returned HTTP `Date` headers from **13:50:12 through 14:20:22 UTC**; later requests also recorded retrieval timestamps. Dates below come from those responses, commit metadata, or explicitly identified documentation. A build-file version is **not** a verified latest store release. This is a dated snapshot, not a claim of exhaustive market coverage.

**Evidence labels:**

- **D — documented:** an official README, project website, or maintainer document describes the feature (`documented`).
- **C — code-observed:** the cited implementation/configuration exists at the pinned commit (`static-observation`). This is not an on-device correctness result.
- **T — tracker evidence:** an existing issue contains the report/request and had the recorded open/closed state (`upstream-report`). Its reporter's diagnosis is not independently proven here.
- **P — proposal/inference:** a suggested improvement or reasoned consequence of inspected code (`proposal`), requiring focused verification.
- **U — unknown:** not established by the bounded inspection (`unknown`). **All application runtime behavior in this report remains untested.**

The evidence comes from public HTTP GETs, repository metadata, pinned raw files, and bounded issue searches. Tests were read or located, not executed. This report does not establish the behavior or provenance of an official Moon+ Reader build. Readest's interpretation of `.mrexpt` is third-party implementation evidence, not a format specification verified against Moon+ Reader v10.8.

## 1. Alternatives first: shortlist and trade-offs

These are **P: evaluation priorities** based on the capabilities below, not a runtime ranking.

| Reading need | Alternatives to evaluate first | Why they belong | Important boundary |
|---|---|---|---|
| Broad Android ebook reading and extensive controls | KOReader; Librera Reader | Broad formats, typesetting, dictionaries, catalogs; KOReader has plugin seams and an e-ink focus; Librera has TTS, PDF tools, and multiple rendering engines | Device support and Librera build flavors require specific checks |
| Cross-platform library and migration from Moon+ | Readest; Anx Reader | Both document Android/desktop/iOS support and synchronization; Readest already exposes a Moon+ `.mrexpt` import flow | Readest entitlements are separate from its open-source license; Anx OPDS is documented as in progress |
| Android PDF reading and annotation | MJ PDF | Canonical source documents embedded PDF highlights, notes, forms, signatures, text mode, and several reading modes | Source is on GitLab; GitHub is an issue-facing mirror and is behind canonical source |
| PDF/DjVu/comic navigation, including older Android devices | Orion Viewer | Crop, zoom, tap zones, hardware key bindings, dictionary handoff, and DjVu support | Compatibility is a build/documentation claim; analytics differ by build |
| Small embeddable viewer / engine reference | MuPDF Android Viewer | Separate pure-Java viewer library and chooser app backed by MuPDF fitz | This repository deliberately omits annotation editing and form filling |
| Native Compose reading UX and parser comparison | Book's Story | Material You, SAF, categories, chapters, and continuous/paged reading | Maintainer declines code contributions; suggestions, reproducers, and translations are appropriate routes |

## 2. Canonical repositories, licenses, versions, and activity

GitHub metadata was read from `https://api.github.com/repos/<owner>/<repo>` at 13:50 UTC; default-branch commits from `/commits/<branch>` at 13:50:52 UTC. GitLab metadata and commit endpoints are separately linked for MJ PDF.

| Application and canonical public repository | Source license observed | Pinned source identity and observed version | Activity/status at retrieval |
|---|---|---|---|
| **KOReader** — <https://github.com/koreader/koreader> | AGPL v3, actual `COPYING` and README; GitHub identifies `AGPL-3.0` | `07d7b22098ef1693f090a881abf27ca5a25fa50a` (`master`); commit **2026-11-20T22:07:45Z**; no release-version claim made | `archived:false`, `disabled:false`; pushed **2026-11-21T07:25:48Z** |
| **Librera Reader** — <https://github.com/foobnix/LibreraReader> | **GPL-3.0-or-later** in `LICENSE.txt`, despite GitHub returning `NOASSERTION`; bundled components retain their own licenses | `b7378bbde373bbf8b80842f3e47ea444fa9fd542`; commit **2026-11-21T09:38:02Z**, title `10.1.14`; F-Droid version constant **10.1.14**, code **7671** | `archived:false`, `disabled:false`; pushed **2026-11-21T09:41:02Z**. README still says development/support is frozen due to war; recent commits preclude treating that notice as proof of abandonment |
| **MJ PDF** — <https://gitlab.com/mudlej_android/mj_pdf_reader>; GitHub issue-facing mirror <https://github.com/mudlej/mj_pdf> | GPL v3 in actual `LICENSE` and source headers; a more specific `-only`/`-or-later` qualifier was not established | GitLab `aef93faaa4c7fa7df373d415e1c874412cba2db5`; committed **2026-11-20T23:46:44Z**, merge `feat/gh126` / MR !75; app **3.1.0**, base code **58**, with ABI-specific code transformation | GitLab public; `last_activity_at:2026-11-20T23:07:11.547Z`; `archived` field not returned. Official site says active/maintained and v3.0 released July 2026. GitHub mirror unarchived, last push **2026-08-25T06:37:01Z**; it is not an authoritative freshness proxy |
| **Orion Viewer** — <https://github.com/max-kammerer/orion-viewer> | **GPL-3.0-or-later** in `LICENSE`; GitHub returns `NOASSERTION` | `1adfe2da0791d1e563fd8966fc3107e9ad79fc74`; commit **2026-11-14T06:45:13Z**; `orion-viewer/version.properties`: **0.97.6**, code **2514** | `archived:false`, `disabled:false`; pushed **2026-11-14T06:45:14Z** |
| **MuPDF Android Viewer** — <https://github.com/ArtifexSoftware/mupdf-android-viewer> | **AGPL-3.0-or-later**, actual `COPYING` and README grant | `f2f75636fb9d5508f7d366bc55bac7fbdf5a38a0`; commit **2026-09-25T02:23:26Z**, `Update to MuPDF 1.28.5.`; library **1.28.5a**, fitz **1.28.5**; `jni` submodule `2f0328165b08fd9c91720d95702cbef3a3d35706` | `archived:false`, `disabled:false`; pushed **2026-09-25T11:00:33Z** |
| **Book's Story** — <https://github.com/Acclorite/book-story> | **GPL-3.0-only**, README grant/badge and implementation SPDX headers | `6ffefb974ae8eac542e36eb659f77e4802735fd9`; commit **2026-11-05T22:33:22Z**; build **1.8.0**, code **14** | `archived:false`, `disabled:false`; pushed **2026-11-05T22:33:39Z**. README declines code PRs and makes an Android developer-verification installation warning; that platform-policy claim was not independently verified |
| **Readest** — <https://github.com/readest/readest> | **AGPL-3.0-or-later**, actual `LICENSE` and README grant | `0882c8074215edc24e2ee5ac25e99cdccddb7e34`; commit **2026-11-21T13:36:52Z**, sign-out/relaunch fix #7743; package **0.12.20** | `archived:false`, `disabled:false`; pushed **2026-11-21T13:36:55Z** |
| **Anx Reader** — <https://github.com/Anxcye/anx-reader> | **MIT** in pinned `LICENSE`. README records MIT → GPLv3 → MIT changes; the current grant does not automatically apply to old versions | `0c7fc1ad4551f7dbbeba6a6468f69d830957fa2a` (`develop`, resolved from GitHub HTML); patch author date **2026-10-17T12:54:44Z**, subject `release: v1.15.0-alpha.35`; `pubspec.yaml` **1.15.0+6358** | `archived:false`, `disabled:false`; pushed **2026-10-17T12:57:09Z**. This is a development/prerelease pin, not a verified latest stable release |

All eight expose public source. APK/source correspondence and build reproducibility were not checked. Librera's and Orion's actual license grants resolve GitHub's `NOASSERTION`; that detector result does not mean closed source. Librera's README lists MuPDF as AGPL and other third-party licenses, including an undeclared component. Dependency-level redistribution review remains separate from the app's declared grant.

### Identity, version, and license sources

- KOReader: [README][ko-readme], [COPYING][ko-license], [commit][ko-commit].
- Librera: [README][li-readme], [LICENSE.txt][li-license], [app/build.gradle L9–12, L121–187, L300–327, L399–403][li-build], [official overview][li-site].
- MJ PDF: [project metadata][mj-meta], [commit metadata][mj-commit-api], [pinned README][mj-readme], [LICENSE][mj-license], [app/build.gradle L51–62 and L170–173][mj-build], [official page][mj-site].
- Orion: [README][or-readme], [LICENSE][or-license], [version.properties][or-version], [root build.gradle L26–35][or-build].
- MuPDF: [README][mu-readme], [COPYING][mu-license], [lib/build.gradle L1–24][mu-build], [root tree showing JNI submodule][mu-tree].
- Book's Story: [README][bs-readme], [app/build.gradle.kts L15–25][bs-build], [parser SPDX header][bs-dispatch].
- Readest: [README][re-readme], [LICENSE][re-license], [package.json L1–9, L137–146, L194–201][re-package].
- Anx: [README][an-readme], [LICENSE][an-license], [pubspec.yaml L1–8][an-build], [commit patch with author date][an-commit].

## 3. Functional feature evidence

### 3.1 KOReader — broad reading and e-ink reference

**Platforms/formats (D):** Android, Linux, and embedded Cervantes/Kindle/Kobo/PocketBook/reMarkable; Linux/macOS developer emulator. README lists PDF, DjVu, CBT, CBZ, EPUB, FB2, Mobi, DOC, RTF, HTML, CHM, and TXT, plus some ZIP-wrapped formats. The developer emulator is not evidence of general macOS distribution support. **C:** the current PDF provider additionally registers CBR and other formats; registration is not a rendering-conformance result.

| Functional feature | Evidence |
|---|---|
| Fixed-page PDF/DjVu/comic viewing | D: [README][ko-readme]; C: [PDF provider registrations L370–394][ko-pdf] |
| Reflowable ebook reading across the listed formats | D: [README][ko-readme] |
| Reflow of scanned PDF/DjVu using K2pdfopt | D: [README][ko-readme]; not an OCR accuracy claim |
| Arbitrary margins, line spacing, external fonts/styles, and hyphenation dictionaries | D: [README][ko-readme] |
| E-ink-oriented animation-free UI, contrast, and page/content-fit zoom | D: [README][ko-readme] |
| StarDict dictionary and Wikipedia lookup | D: [README][ko-readme]; C: [reader module wiring L218–231][ko-ui] |
| Calibre metadata search, wireless book receipt, and OPDS catalogs | D: [README][ko-readme] |
| Wallabag integration and RSS feeds | D: [README][ko-readme] |
| Highlights, bookmarks, chapters, and full-text search | C: [ReaderUI module registration L153–245, L409–414][ko-ui] |
| Current-book, selected-file, and history-wide annotation export | C: [exporter main L181–206][ko-export-main] |
| Markdown/JSON/text/HTML and remote-service exports; style/color filtering | C: [target registry L77–87 and filters L343–394][ko-export-main], [JSON writer][ko-json] |
| Plugin extensibility | D: [README][ko-readme]; C: reader imports `PluginLoader`; exporter registers its menu [L97–104][ko-export-main] |

### 3.2 Librera Reader — Android all-in-one reference

**Platforms/formats (D):** Android; README lists PDF, EPUB/EPUB3, MOBI, DjVu, FB2, TXT, RTF, AZW/AZW3, HTML, CBZ/CBR, DOC/DOCX. Official overview additionally lists ODT, XPS, TIFF, PDB, MHT, and FB2.ZIP. These lists are documented claims, not identical capabilities proven in every flavor. OPDS is a catalog protocol. README documents recent builds as Android 7/API24 minimum; exact variant compatibility was not executed.

| Functional feature | Evidence |
|---|---|
| Folder-configured automatic discovery and in-app file browsing | D: [official overview][li-site] |
| List/grid covers, title/author/series/genre filtering and sorting | D: [official overview][li-site] |
| Configurable TTS using installed/custom engines and a media player | D: [overview][li-site]; C: [FoliateDocument read-ahead integration L64–114][li-foliate] |
| PDF text reflow, page splitting, and whitespace crop | D: [official overview][li-site] |
| Musician mode with adjustable automatic sheet scrolling | D: [official overview][li-site] |
| Bookmarks, annotations, comments, and PDF drawing | D: [overview][li-site]; C: [CodecDocument annotation methods L59–70][li-codec] |
| Offline/online dictionaries and selection translation/share/copy | D: [official overview][li-site] |
| Themes, layout, custom CSS, tap zones/volume keys, and LTR/RTL direction | D: [overview][li-site]; C: [FoliateCss conversion][li-css] |
| OPDS browsing and offline Calibre metadata/covers | D: [official overview][li-site] |
| Reading progress/bookmark synchronization via Google Drive | D: [official overview][li-site]; flavor applicability remains U |
| Settings import/export and automatic session backup | D: [official overview][li-site] |
| EPUB3 audio/video | D: [official overview][li-site]; untested for the foliate/JS flavors |

**C:** Librera is no longer accurately described as only MuPDF-based. The inspected build includes PDFium as the default PDF engine, foliate-js/WebView for reflowable reading, and `fdroidJS`/`proJS` variants without MuPDF. [Build L141–186, L312–326, L399–403][li-build] and the [FoliateDocument adapter][li-foliate] establish these paths. LibreraX, advertised on the website, is not this Android Java repository.

### 3.3 MJ PDF — PDF-focused alternative

**Platforms/formats:** Android **API23+** (C: [build][mj-build]); **PDF** (D: [canonical README][mj-readme]). Non-PDF formats are a roadmap item. Current source supersedes older descriptions of MJ PDF as just a simple PDFium viewer.

| Functional feature | Evidence |
|---|---|
| Recent, Library, and Folders tabs with file manager/SD-card browsing | D: [README L57–64][mj-readme] |
| Reading-status filters, cover grid/list, sorting, and device PDF discovery | D: [README L57–64][mj-readme]; C: [filter-chip layout][mj-chips] |
| Last-position/history persistence surviving moves/renames | D: [README L59–64][mj-readme]; database entities C: [AppDatabase L23–47][mj-db] |
| Continuous/horizontal/single-page/dual-page modes and page-fit policies | D: [README L43–45, L71–72][mj-readme] |
| App/PDF dark mode, full-screen controls, rotation, brightness, autoscroll, zoom lock | D: [README L66–77][mj-readme] |
| Margin hiding, RTL autodetection, password PDFs, and online PDF links | D: [README L73–75][mj-readme] |
| PDF-embedded highlights, editing existing highlights, notes, and annotation lists | D: [README L79–82][mj-readme]; C: [highlight list/export wiring][mj-highlights] |
| Reusable vector signatures and supported PDF form filling | D: [README L83–84][mj-readme] |
| Inline selection/copy/share/translation/dictionary actions and quote images | D: [README L85–86][mj-readme] |
| Streaming search, TOC search, link list, named bookmarks, and navigation history | D: [README L88–94][mj-readme]; C: [folded-text search][mj-search] |
| PDF text-mode reflow, fonts/themes/line length; incremental extraction | D: [README L96–98][mj-readme]; C: [TextModeContentLoader L29–168][mj-text-loader] |
| Share/print, multiple instances, incognito mode, and shared-file copy choices | D: [README L76, L100–109][mj-readme] |

**Freshness correction:** canonical pinned README L104 already offers **Ask / Always / Never keep a copy**. The GitHub mirror says only Ask/Always, and open GitLab issue #85 requests a “Just read it” default. Neither mirror text nor an open issue proves absence in current canonical source. Plain-text note/highlight export also exists: [UserHighlightsActivity L277–316][mj-highlights], [UserNotesActivity L223–261][mj-notes]. The study-export proposal below extends those paths.

### 3.4 Orion Viewer — fixed-page and navigation specialist

**Platforms/formats:** Android; D: PDF, DjVu, XPS, TIFF, CB7/CBR/CBZ/CBT in [README][or-readme]. C: normal `minSdk=16`, special Android-4.0 build `minSdk=14`, `targetSdk=36`. A `desktop` source directory does not establish released desktop support.

| Functional feature | Evidence |
|---|---|
| Outline navigation | D: [README, Application features][or-readme] |
| Internal PDF and DjVu links | D: [README][or-readme] |
| Bookmarks | D: [README][or-readme] |
| Screen-tap page navigation | D: [README][or-readme] |
| Configurable tap zones and hardware key bindings | D: [README][or-readme] |
| Text selection | D: [README][or-readme] |
| Double-tap word selection with external dictionary translation | D: [README][or-readme] |
| Custom zoom and border crop | D: [README][or-readme] |
| Portrait/landscape and LTR/RTL within-page navigation patterns | D: [README][or-readme] |
| Built-in file manager and recently opened files | D: [README][or-readme] |

**Telemetry:** README says automatic crash/usage collection from 0.91.0. C: [root build L34][or-build] enables analytics only for non-Android-4.0 builds when `orion-viewer/google-services.json` exists; [app build L4–7, L37–40, L93–94][or-app-build] conditionally adds Firebase and selects the analytics implementation. This establishes a build distinction, not distributed-APK network behavior. Orion received documentation/license/build review, not an application implementation or issue-tracker deep dive.

### 3.5 MuPDF Android Viewer — simplified library and app

**Platforms/formats:** Android **API21+** (C: [library build L15–21][mu-build]). C: [manifest L10–25][mu-manifest] and [LibraryActivity L28–43][mu-library] advertise PDF, XPS/OXPS, CBZ, EPUB, FictionBook, and Mobipocket MIME types. Handler registration does not establish format-edge-case conformance.

| Functional feature | Evidence |
|---|---|
| System Storage Access Framework document picker | C: [LibraryActivity L24–46][mu-library]; corrects README's older external-storage chooser description |
| Android Open With / `ACTION_VIEW` integration | C: [manifest L10–25][mu-manifest], [DocumentActivity L233–299][mu-activity] |
| Rendering through fitz with reflowable layout support | C: [MuPDFCore L48–94, L144–196][mu-core] |
| Password prompt/authentication | C: [DocumentActivity L295–298, L327–351][mu-activity] |
| Previous/next text-search navigation | C: [DocumentActivity L517–526, L854–859][mu-activity], [MuPDFCore L194–196][mu-core] |
| Outline navigation | C: [MuPDFCore L27–28, L199–227][mu-core], [DocumentActivity L575–583][mu-activity]; capped at 1,000 entries/depth 4 |
| Page slider/readout and position persistence on pause/save | C: [DocumentActivity L385–387, L435–457, L645–682][mu-activity] |
| Pinch zoom, scrolling/fling, and screen-edge navigation | C: [ReaderView L396–400, L475–534, L917–940][mu-reader] |
| Font-size relayout preserving a document bookmark | C: [DocumentActivity L535–564][mu-activity], [MuPDFCore L77–95][mu-core] |
| Link highlighting, external-link dispatch, and navigation history | C: [DocumentActivity L529–532, L708–711][mu-activity], [PageView L565–598][mu-page], [ReaderView L120–132][mu-reader]; page-zero caveat below |

**D:** [README][mu-readme] explicitly excludes annotation editing and form filling. Capabilities of MuPDF Core, the full Android editor, commercial products, or other wrappers must not be credited to this simplified viewer. Long-press selection is an existing upstream request; `ReaderView.onLongPress` is empty at this pin.

### 3.6 Book's Story — native Compose reader

**Platforms/formats:** Android **8/API26+**, target/compile API36 (C: [build][bs-build]). D: README claims seven extensions including `.md`. C: [ExtensionsData L11–19][bs-extensions], [FileParserImpl L30–59][bs-file-dispatch], and [ContentParserImpl L47–75][bs-dispatch] enumerate **six**: EPUB, PDF, FB2, TXT, HTML, HTM, with no Markdown branch. This is a documentation/implementation mismatch, not seven verified formats.

| Functional feature | Evidence |
|---|---|
| SAF access and storage-folder discovery | D: [README][bs-readme]; C: [CachedFile L78–148][bs-cached-file], [FileSystemRepositoryImpl L34–89][bs-filesystem] |
| Ebook library with custom categories | D: [README][bs-readme] |
| Chapters/TOC in the reader | D: [README][bs-readme]; C: [BookRepositoryImpl L87–92][bs-repository] |
| Material You themes and color presets | D: [README][bs-readme] |
| Custom fonts/layout, margins, colors, and progress readout | C: [ReaderContent L33–94][bs-reader-content] passes settings to the reader |
| Continuous and paged layouts | C: [ReaderScaffold L169–232][bs-scaffold] selects separate implementations |
| Selection with copy, share, and web-search actions | C: [ReaderLayoutPaged L168–177][bs-paged] |
| Translation/dictionary selection actions and paragraph double-tap translation | C: [ReaderLayoutPaged L174–177][bs-paged], [ReaderLayoutContentParagraph L40–58][bs-paragraph] |
| Images with captions, width/alignment, and color-effect controls | C: [ReaderLayoutContent L82–118][bs-layout-content] |
| Reading ruler/horizontal limiter and perception-expander overlays | C: [ReaderScaffold L219–227, L283–287][bs-scaffold] |
| PDF-to-text reflow | C: [PdfContentParser L52–80, L102–153][bs-pdf]; PDFBox text extraction into nodes, not original-page rendering or OCR |

**Contribution boundary (D):** README says “I do not accept code contributions”; PRs will likely be closed. It invites suggestions, detailed reports, and Weblate translations. The GPL permits independent modifications, but that does not imply upstream acceptance. The README's Android-registration warning is a maintainer statement, not a verified global installation ban or archive declaration.

### 3.7 Readest — cross-platform reader with an observed Moon import path

**Platforms/formats (D):** macOS, Windows, Linux, Android, iOS, Web; EPUB, PDF, MOBI, KF8/AZW3, FB2, CBZ, TXT, HTML, Markdown. C: package declares Next **16.4.6**, React **19.2.9**, Tauri API **2.11.1**. Platform performance/accessibility and distribution parity remain U.

| Functional feature | Evidence |
|---|---|
| Scroll and paginated reading | D: [README Features][re-readme] |
| Full-text search inside a book or across the current library shelf | D: [README][re-readme] |
| Highlights, notes, bookmarks, and instant annotation interactions | D: [README][re-readme]; C: [Annotator import/merge wiring][re-annotator] |
| Dictionary/Wikipedia lookup and local Yomitan ZIP/RDICT dictionaries | D: [README][re-readme] |
| Two-document split-screen “Parallel Read” | D: [README][re-readme] |
| Fonts/layout/themes and code syntax highlighting | D: [README][re-readme]; C: [style assembly L1265–1330][re-style] |
| Library organization and OPDS/Calibre integration | D: [README][re-readme] |
| Web clipping and selected web-novel chapter/image import | D: [README][re-readme] |
| Sentence/book translation and multilingual TTS | D: [README][re-readme] |
| EPUB3 Media Overlays and local DRM-free audiobook pairing/read-along | D: [README][re-readme], [code-layout L308–330][re-layout-doc] |
| Cross-device files/progress/notes/bookmarks and KOReader interoperability | D: [README][re-readme]; C: [KOSyncClient][re-kosync], [file-provider registry][re-sync-registry] |
| **Moon+ `.mrexpt`, ReadEra `.bak`, and Readest `.json` annotation-import UI** | C: [ImportAnnotationsDialog L43–57][re-import-dialog]; Moon parser/converter invoked at [Annotator L2260–2369][re-annotator] |

Additional **D:** README claims full keyboard/screen-reader support, reading ruler, paragraph mode, and speed-reading aids. These were not accessibility-tested. **C:** [cloudSyncProvider L116–149][re-sync-gate] can pause third-party file sync based on plan/customization entitlement; its comments distinguish library data from signed-in account-level sync. The open-source license does not promise every hosted/distributed feature is free or entirely local.

### 3.8 Anx Reader — additional cross-platform alternative

**Platforms/formats (D):** Android/iOS/macOS/Windows; EPUB/MOBI/AZW3/FB2/TXT/PDF. Linux/Web/OHOS directories do not establish supported releases. The development pin is labeled `v1.15.0-alpha.35`; [pubspec][an-build] declares Flutter, Riverpod, and a vendored WebDAV client. No application-code deep inspection was performed.

| Functional feature | Evidence |
|---|---|
| Multi-format ebook/PDF reading | D: [README feature matrix][an-readme] |
| WebDAV synchronization of books, notes, and position | D: [README][an-readme] |
| Letter/line/paragraph/margin spacing and font size/style/weight controls | D: [README][an-readme] |
| Themes, backgrounds, and alignment customization | D: [README][an-readme] |
| Color/style note presets, chapter/time sorting, and color filtering | D: [README][an-readme] |
| TXT/Markdown/CSV note export and shareable cards | D: [README][an-readme] |
| Reading-time statistics by day/week/month/year and heatmap | D: [README][an-readme] |
| TTS voice/speed/tone controls and sleep timer | D: [README][an-readme] |
| Full-book side-by-side translation and simplified/traditional Chinese conversion | D: [README][an-readme] |
| Cloud book storage with on-demand download | D: [README][an-readme] |
| AI dictionary, summaries, perspective analysis, and mind maps | D: [README][an-readme]; provider behavior/cost/privacy uninspected |

**OPDS is marked “In progress” in the pinned README**, not verified implemented. Community Calibre plugin/library-manager links are explicitly labeled unofficial there.

## 4. Reviewed code and extension seams

These are the **six application-code representatives**. Linked ranges were inspected; large files were examined through selected excerpts. This is not a whole-repository audit. Orion and Anx received documentation/license/build inspection only.

### KOReader

- **C — document providers:** [frontend/document/documentregistry.lua L31–56, L63–140, L154–225][ko-registry] registers extension/MIME/weight, resolves document/type preferences, and maps MIME to extensions. [frontend/document/pdfdocument.lua L370–416][ko-pdf] is a concrete registration site. New aliases belong there; a renderer implements a document provider.
- **C — reader composition:** [frontend/apps/reader/readerui.lua L94–101, L153–245, L287–424][ko-ui] composes view/link/highlight/menu/TOC/bookmark/dictionary/search modules and distinct fixed-page/reflowable controllers.
- **C — annotation exporters:** [plugins/exporter.koplugin/base.lua L23–125][ko-export-base] supplies settings, identity, readiness, and `export`; [main.lua L77–104, L181–206, L343–394][ko-export-main] registers targets/actions/filters. [target/json.lua L26–73][ko-json] serializes booknotes with optional checksum; [template/md.lua L39–65][ko-md] constructs Markdown; [target/markdown.lua L36–103, L106–126][ko-markdown] exposes custom formatter strings and writes/shares output.
- **Tests located, not read/run:** `spec/unit/document_registry_spec.lua`, `spec/unit/exporter_plugin_main_spec.lua` in the pinned tree. No coverage claim follows from their existence.

### Librera Reader

- **C — renderer contract:** [app/src/main/java/org/ebookdroid/core/codec/CodecDocument.java L11–120][li-codec] abstracts pages, search, outlines, notes/media, annotations, metadata, and locations. Fixed-page and reflowable adapters share it.
- **C — foliate adapter:** [app/src/main/java/org/ebookdroid/droids/foliate/codec/FoliateDocument.java L31–180, L378–453, L482–503][li-foliate] integrates a WebView-backed document, read-ahead cache, page index, CFI location, and text fallback. Location methods return a miss on the main thread rather than block; this does not prove all save/restore callers lose anchors.
- **C — thread boundary:** [FoliateRenderer.java L36–82, L123–173, L343–374, L459–509, L594–651, L683–718][li-renderer] posts WebView work to the main thread and uses a lock/latch protocol for workers, with 20s call and 180s indexing budgets. Existing timing/profile entrypoints support measurement before optimization.
- **C — CSS adaptation:** [FoliateCss.java L20–38, L50–67, L111–165, L182–194, L202–229][li-css] translates MuPDF-oriented CSS, rewrites local font URLs, supplies generic fallbacks, and maps margins into paginator settings.
- **C — build variants:** [app/build.gradle L121–187, L300–327, L399–403][li-build] separates F-Droid/Pro and MuPDF-free JS variants. Capability documentation should identify these explicitly.

### Book's Story

- **C — ingestion/parser separation:** [data/repository/FileSystemRepositoryImpl.kt L34–89][bs-filesystem] discovers files and obtains metadata/covers. [data/parser/file/FileParserImpl.kt L16–62][bs-file-dispatch] dispatches metadata parsing; [data/parser/content/ContentParserImpl.kt L27–78][bs-dispatch] dispatches parsers returning progress/error/success through `Flow` on `Dispatchers.IO`.
- **C — typed reader data:** [data/repository/BookRepositoryImpl.kt L39–61, L79–145, L167–215][bs-repository] maps app/per-book Room databases to chapters/nodes/metadata. [presentation/reader/ReaderState.kt L20–65][bs-state] models loading/parsing/saving/showing/error and node-based scroll targets.
- **C — rendering:** [ui/reader/ReaderLayoutContent.kt L26–129][bs-layout-content] dispatches headers, paragraphs, images, and separators. [ReaderScaffold.kt L169–287][bs-scaffold] separates continuous/paged layouts; [ReaderLayoutPaged.kt L149–177][bs-paged] loads a node window and wires selection actions. New elements require parsing, typed content, and rendering changes.
- **C — parser versioning:** [core/data/ParsersData.kt L9–44][bs-parser-versions] supplies versions for content/cache compatibility. Parser extensions must account for invalidation.
- **C — PDF boundary:** [PdfContentParser.kt L52–80, L102–153][bs-pdf] extracts text using PDFBox and emits paragraphs/separators; its `cacheImage` callback is unused. Original layout/image/OCR equivalence cannot be claimed.
- **Tests read in excerpts, not run:** [ContentParserRegressionTest.kt L93–178][bs-tests] includes HTML/CSS, FB2, UTF BOM, EPUB spine/navigation/resources, and NCX fixtures. This single file does not establish the repository's total PDF test coverage.

### Readest

- **D + C — platform services:** [code-layout.md][re-layout-doc] and [architecture.md][re-architecture] describe React/Next UI, Tauri host, and server routes. [src/services/appService.ts L47–131][re-app-service] defines filesystem/path/database/dialog/save abstractions and capability flags, providing platform-specific extension points.
- **C — file sync:** [src/services/sync/file/provider.ts L19–99][re-sync-provider] defines normalized errors and read/head/list/write/directory/optional streaming operations. [providerRegistry.ts L17–33, L51–140][re-sync-registry] constructs/caches WebDAV, Drive, S3, OneDrive, and iCloud. New providers must preserve missing-file/error semantics. A shared conformance suite is mentioned, not inspected/run.
- **C — wired import UI:** [ImportAnnotationsDialog.tsx L43–57][re-import-dialog] exposes Moon+/ReadEra/Readest. [Annotator.tsx L2260–2369, L3087–3094][re-annotator] selects `.mrexpt`, parses, converts, merges, saves, and updates views. [annotation/providers/index.ts L16–21][re-import-registry] lists only Foliate, but the dedicated Moon flow bypasses that registry.
- **C — Moon location conversion:** [src/utils/mrexpt.ts L1–55, L74–161][re-mrexpt-parser] reads `b4`, `b5`, `b6`, length, timestamp, and entry ID. [annotation/providers/mrexpt.ts L89–257, L261–395][re-mrexpt] maps NCX to spine, matches the first occurrence in one DOM text node, builds a CFI, and falls back to section CFI/global scanning. `b6` participates in deduplication, not repeated-occurrence selection in this loop.
- **C — existing merge behavior:** [converter L35–86][re-mrexpt] handles duplicate IDs, newer notes, and resurrected deletions; [mrexpt-import.test.ts L20–118][re-mrexpt-tests] covers merge/import-time scenarios in source. Basic duplicate/no-op reimport is already implemented. Source modification time versus import time and anchor fidelity merit further fixtures.
- **C — publisher-style boundary:** [src/utils/style.ts L577–585, L632–640, L806–808, L1265–1286, L1320–1330][re-style] always includes page-layout CSS while `useBookLayout` skips paragraph CSS only. [FoliateViewer.tsx L1131, L1387–1402][re-viewer] applies it. This is the extension point for the existing “Force Book Layout” request.

### MJ PDF

- **C — modules:** [settings.gradle L1–4][mj-settings] includes app, `AndroidPdfViewer:android-pdf-viewer`, `PdfiumAndroid`, and macrobenchmark. Kotlin app, Java viewer, and Java/C++ bindings are distinct surfaces; README documents a native build pipeline.
- **C — persistence:** [data/AppDatabase.kt L23–68][mj-db] uses Room version 15 with PDF records, save destinations, scanned entries, bookmarks, and explicit migrations.
- **C — extraction:** [pdf/PdfExtractor.kt L16–99, L101–167][mj-extractor] wraps PDFium page/text/metrics/thumbnail/link/note access and page close lifecycle. Character-metrics work is capped at 20,000 characters per page. This is not an OCR implementation claim.
- **C — text mode:** [ui/text_mode/TextModeContentLoader.kt L29–168][mj-text-loader] has an extraction mutex, jobs, page cache, nearby prefetch, and cancellation outside the target window. TTS should coordinate this ownership instead of adding unmanaged native handles.
- **C — export:** [ui/usernotes/AnnotationListLogic.kt L13–24, L27–68][mj-annotation-logic] centralizes filters and formatted export with TOC/color/date callbacks. [UserHighlightsActivity.kt L65–69, L277–316][mj-highlights] and [UserNotesActivity.kt L57–61, L223–261][mj-notes] already offer SAF text export.
- **C — responsive layout:** [app/src/main/res/layout/item_home_chip_row.xml][mj-chips] uses equal `0dp`/weight=1 chip slots and fixed horizontal margins, including Completed/Abandoned. Issue #90 supplies the scaling reproduction; it was not rendered for this report.

### MuPDF Android Viewer

- **C — app/library separation:** [app/.../LibraryActivity.java L24–66][mu-library] obtains a SAF document and launches `ACTION_VIEW` with multiple-document/task flags. [lib/build.gradle L1–24][mu-build] packages a library with local-or-Maven fitz.
- **C — engine facade:** [lib/.../MuPDFCore.java L48–129, L144–227][mu-core] owns `Document`, `Page`, `DisplayList`, layout/bookmarks, search, links, and outline flattening. `gotoPage` uses zero-based indices; UI display adds one.
- **C — UI:** [lib/.../DocumentActivity.java, ranges in the feature table][mu-activity] connects intents, passwords, search, relayout, slider, and persistence. [ReaderView.java L120–132, L473, L917–940][mu-reader] handles gestures/history; [PageView.java L565–598][mu-page] resolves internal links or dispatches external URLs.
- **P — first-page-link candidate:** `MuPDFCore.resolveLink` returns a document page number; `PageView.hitLink` returns it for internal links but also uses `0` for external/no-link results; `ReaderView.onSingleTapUp` follows only `page > 0`. An internal destination at index zero is indistinguishable in this path. This is a strong source-level reproduction target, not an on-device confirmed defect.

## 5. Contribution candidates — 21 scoped proposals

Each entry is **P**, supported by the indicated **C/T/D** evidence. “Open” means returned open at retrieval, not confirmed broken at pinned HEAD. Acceptance checks describe proposed work, not executed tests.

Machine-readable proposal IDs prefix the short IDs below with `ALT-` (for example, K01 is `ALT-K01`). Record priorities are suggested investigation order, **not defect severity**: `high` prioritizes narrow reproduction or migration/position integrity, `medium` identifies focused product improvements, and `low` marks broader roadmap or documentation work. Every proposal record has status `draft`; none represents an implemented or submitted change.

### KOReader (3)

1. **K01 — OPDS CBR MIME aliases and a feed regression fixture.** T: [#15844](https://github.com/koreader/koreader/issues/15844), open, updated 2026-08-09. C: [pdfdocument.lua L372–373][ko-pdf] registers `application/vnd.comicbook-rar` and `application/vnd.rar`, but not the reported `application/vnd.comicbook+rar` / `application/x-cbr`; [MIME mapping][ko-registry] is the extension seam. **Acceptance:** all four aliases resolve to CBR; local OPDS fixtures expose download actions; CBZ remains correct. Trace feed logic before attributing the full UI failure to this block.
2. **K02 — configurable Markdown metadata/header presentation.** T: [#14885](https://github.com/koreader/koreader/issues/14885) and [#13321](https://github.com/koreader/koreader/issues/13321), open. C: [template/md.lua L42–59][ko-md] hardcodes author/header/page/date/separator presentation; [target/markdown.lua][ko-markdown] already supports style/custom formatter strings. **Acceptance:** independent page/date visibility and a blockquote preset; multiline/no-note/Unicode fixtures; existing output remains the default. This extends Markdown export.
3. **K03 — hierarchical chapter context in annotation exports.** T: [#12480](https://github.com/koreader/koreader/issues/12480), open. C: [template/md.lua L41–50][ko-md] emits one `entry.chapter` at one heading level. **Acceptance:** a three-level TOC retains ancestor context with fallback for old annotations; inspect parser/metadata before selecting storage changes. **Color filtering already exists** at [main.lua L369–393][ko-export-main] despite open #14334.

### Librera Reader (4)

4. **L01 — profile and reduce cold-open/indexing cost.** T: [#1692](https://github.com/foobnix/LibreraReader/issues/1692), open, reports 10.0.35 Pro foliate loading regressions. C: [FoliateRenderer open/index/profile methods][li-renderer], [FoliateDocument indexing/read-ahead][li-foliate]. **Acceptance:** compare cold/warm open-to-first-readable-page and index latency on identical device/corpus/settings while preserving layout and anchors. The alleged regression is unmeasured here.
5. **L02 — font discovery, weight, and justification conformance.** T: #1692; #1691 concerns **LibreraX**, not necessarily this implementation. C: [FoliateCss font rewriting/fallback][li-css]. **Acceptance:** regular-only, genuine bold, variable-font, Turkish-justification, and large-heading fixtures; retain authored `<strong>` without globally bolding body text. Trace discovery before adopting the reporter's unverified filtering diagnosis.
6. **L03 — exact-position persistence across layout and lifecycle changes.** T: old open [#672](https://github.com/foobnix/LibreraReader/issues/672) describes percentage drift across screen sizes. C: current [location contract][li-codec] and [FoliateDocument L388–448][li-foliate] support CFIs but skip blocking location calls on the UI thread. **Acceptance:** restore the same words after rotation/font changes, backgrounding, and device-size migration; establish which callers fall back and retain a nonblocking last-known CFI if needed. The old report is not proof of current failure.
7. **L04 — current flavor/engine capability documentation.** C/D: [README notice/build instructions][li-readme] versus [10.1.14 and JS variants][li-build], GPL grant, dependency table. **Acceptance:** maintainer-approved dated status and matrix of MuPDF/PDFium/foliate, F-Droid/Pro/JS, network/GMS-dependent features, and minimum API. This is an onboarding contribution, not a demand to remove the war notice or a license-violation allegation.

### Book's Story (3; suggestions/reproducers/translations)

8. **B01 — page-preserving PDF mode or explicit PDF capability messaging.** T: [#117](https://github.com/Acclorite/book-story/issues/117), open, updated 2026-11-05, requests display without parsing. C: [PdfContentParser][bs-pdf] emits extracted paragraphs. **Acceptance:** original-page handling for scanned/layout-sensitive PDFs, or clear text-only messaging; two-column, image-only, table, and mixed-script fixtures. Keep page rendering distinct from ebook text layout.
9. **B02 — Android Open With/share import.** T: [#310](https://github.com/Acclorite/book-story/issues/310), open, updated 2026-11-08. C: [AndroidManifest.xml L38–49][bs-manifest] has only MAIN/LAUNCHER for MainActivity; [file repository][bs-filesystem] provides ingestion. **Acceptance:** supported `content://` files from file-manager/mail share use the same import flow, including transient grants, duplicates, and cancellation. Source manifest is not a merged-APK manifest audit.
10. **B03 — reconcile Markdown claims with dispatch.** C: README `.md` claim versus [ExtensionsData][bs-extensions], [FileParserImpl][bs-file-dispatch], [ContentParserImpl][bs-dispatch]. T: [#93](https://github.com/Acclorite/book-story/issues/93) is **closed**. **Acceptance:** a `.md` fixture is discoverable/importable/rendered if intended; otherwise docs list six current extensions. Clarify whether a rewrite intentionally removed support; a closed old request does not prove current implementation.

### Readest (4)

11. **R01 — occurrence-aware Moon anchors, including split text nodes.** C: [parser fields][re-mrexpt-parser], [converter L202–257, L333–365][re-mrexpt] perform first-match searches rather than offset-based occurrence selection; matches are per text node. **Acceptance:** repeated phrases in one/multiple chapters, inline-element splits, CJK, and whitespace changes resolve correctly or expose ambiguity. Verify v10.8 export semantics first; offsets are not certified portable across editions.
12. **R02 — import fidelity and reconciliation outcomes.** C: [parser][re-mrexpt-parser] does not retain the raw marker/color value; [converter L289–395][re-mrexpt] applies one chosen style/color and returns `unmatched`; [Annotator L2331–2366][re-annotator] reports added/updated totals without using unmatched/total. **Acceptance:** supported color/style mappings and exact/chapter-fallback/skipped/ambiguous counts with a reviewable partial-import result. Preserve duplicate/resurrection behavior covered by [existing tests][re-mrexpt-tests].
13. **R03 — stronger author-CSS/layout preservation.** T: [#7417](https://github.com/readest/readest/issues/7417), open, updated 2026-11-19. C: [style.ts L632–636, L1265–1286, L1330][re-style] includes image/page CSS even with paragraph overrides off; [FoliateViewer][re-viewer] applies it. **Acceptance:** a synthetic EPUB with author `img { width: 50%; }` keeps that width in publisher-first mode while links/footnotes/overflow work. Check Chromium, Android WebView, and WebKit; existing reporter measurements are not independent results here.
14. **R04 — interoperable annotated-PDF export.** T: [#7572](https://github.com/readest/readest/issues/7572), open, updated 2026-11-18, requests embedded standard PDF annotations. C: annotation UI/data flow and [BaseAppService.saveFile L95–104][re-app-service] provide input/output seams. **Acceptance:** a new annotated PDF reopens correctly in two independent readers, preserving crop/rotation geometry; flattening is a separate choice. **U:** no complete PDF-writeback absence search was made; check implementation/PRs before coding. JSON/Markdown export and overlays are not PDF writeback.

### MJ PDF (4)

15. **M01 — readable Library chips at large text/display scaling.** T: [GitLab #90](https://gitlab.com/mudlej_android/mj_pdf_reader/-/work_items/90), open, updated 2026-11-20, supplies Android 9 emulator 1080×1920 comparisons at 540 dpi/fontScale 1.3 and 420/1.0. C: [item_home_chip_row.xml][mj-chips] retains equal-weight widths. **Acceptance:** Completed/Abandoned and long translations remain readable at large scale/narrow width, with clear selection and usable accessibility focus. Reproduce, then consider measured-width wrapping/scrolling.
16. **M02 — text-mode TTS with synchronized highlighting.** D: [roadmap v3.7][mj-roadmap]. C: [TextModeContentLoader][mj-text-loader], [PdfExtractor][mj-extractor]. **Acceptance:** start/pause/resume, sentence highlight, jumps, and close without leaked handles or conflicting extraction; narration begins without loading every page. This is a roadmap enhancement.
17. **M03 — structured study exports beyond plain text.** D: [roadmap v3.8][mj-roadmap] names Markdown/Anki/Obsidian/flashcards. C: [AnnotationListLogic][mj-annotation-logic], [highlight export][mj-highlights], [note export][mj-notes]. **Acceptance:** stable document/page/annotation identities, quote/note separation, color/TOC context, deterministic repeated export, and multiline/Unicode/third-party-highlight fixtures. Plain-text export already exists.
18. **M04 — large-screen multi-document tabs with isolated lifecycle.** T: [#88](https://gitlab.com/mudlej_android/mj_pdf_reader/-/work_items/88), open; D: [roadmap v3.3][mj-roadmap]. C: loader/extractor ownership above. **Acceptance:** independent page/zoom/unsaved-annotation state across tabs, close-time native cleanup, process restoration, and bounded large-file memory. Multiple Android instances already exist; in-window tabs are distinct.

### MuPDF Android Viewer (3)

19. **U01 — separate no-link from page index zero.** C: [PageView L565–598][mu-page], [MuPDFCore L190–191][mu-core], [ReaderView L917–928][mu-reader]. **Acceptance:** a three-page PDF links from page 3 to page 1/index 0 and page 2/index 1; both navigate and history returns correctly; external URLs/no-link taps remain distinct. **T:** bounded `link` search returned #33 (external links), #26, #1, not an exact page-zero report. This is not an exhaustive novelty claim.
20. **U02 — basic selection/copy within viewer scope.** T: [#29](https://github.com/ArtifexSoftware/mupdf-android-viewer/issues/29), [#36](https://github.com/ArtifexSoftware/mupdf-android-viewer/issues/36), open. C: [ReaderView L473][mu-reader] has an empty long-press handler. **Acceptance:** handles, clipboard, and cancellation at different zoom/rotation, with clear image-only-PDF behavior. This does not require adding form/annotation editing.
21. **U03 — share the currently open document.** T: [#25](https://github.com/ArtifexSoftware/mupdf-android-viewer/issues/25), open, updated 2026-11-15. C: [DocumentActivity intents][mu-activity], [LibraryActivity SAF][mu-library] expose the URI. **Acceptance:** sharing passes a readable content URI with transient grant to a receiver, works with document providers, and avoids dependence on raw `file://` paths. Verify receiver readability and source lifetime.

### Additional routes at lighter inspection depth

- **Orion (D/P):** README welcomes PRs, suggestions, and translations. Translation completeness and a fixture matrix for tap-zone/key-binding/crop/rotation behavior are useful starting points. A dedicated source/issue pass is needed before alleging a defect.
- **Anx (D/P):** coordinate with documented in-progress OPDS work rather than re-request it as a newly discovered gap. Export interoperability and WebDAV cross-device fixtures are promising; application-code inspection and issue deduplication were not performed. The vendored redirect-fix comment in `pubspec.yaml` is not evidence of a current defect.

## 6. Ready-to-submit drafts

These drafts have **not been submitted**. Use existing threads where identified and add independently collected runtime evidence when available.

### Draft A — comment on KOReader #15844

**Context: CBR MIME aliases and regression-fixture scope**

At `07d7b22098ef1693f090a881abf27ca5a25fa50a`, `frontend/document/pdfdocument.lua` L372–373 registers CBR for `application/vnd.comicbook-rar` and `application/vnd.rar`. The reported `application/vnd.comicbook+rar` and `application/x-cbr` aliases are not in that block. `DocumentRegistry:addProvider` records MIME-to-extension mappings, providing a concrete test seam.

I have not reproduced the OPDS UI on-device. A regression fixture could expose the same public-domain CBR acquisition under all four MIME values and check each download action, while preserving CBZ behavior. Would a small alias patch with registry/OPDS fixture coverage be welcome?

Sources: [provider registrations][ko-pdf], [registry][ko-registry].

### Draft B — MuPDF Android Viewer source-level candidate

**Title: Internal links to page index zero share the no-link sentinel**

**Source checked:** `ArtifexSoftware/mupdf-android-viewer@f2f75636fb9d5508f7d366bc55bac7fbdf5a38a0`, library 1.28.5a.

`MuPDFCore.resolveLink()` returns a document page number. `PageView.hitLink()` returns it for internal links but returns `0` for external/no-link results too. `ReaderView.onSingleTapUp()` follows only `page > 0`. Surrounding navigation code uses zero-based indices.

Page 0 should be a valid destination, distinguished from “no internal destination” by a separate sentinel or result type.

**Proposed reproduction:** a three-page PDF with page-3 links to page 1, page 2, and HTTPS. Enable link handling; activate each; exercise history. Both internal links should navigate and external/no-link interactions should retain their behavior.

**Coverage:** source-level analysis, not an on-device reproduction. A bounded issue search found #33 about external links, not an exact page-zero duplicate. Complete duplicate/reproduction checks before submitting.

Sources: [ReaderView][mu-reader], [PageView][mu-page], [MuPDFCore][mu-core].

### Draft C — Readest Moon import reconciliation

**Title: Show matched, chapter-fallback, and skipped counts for Moon+ imports**

Readest already has a wired Moon+ import path: selection in `Annotator`, `parseMrexpt`, CFI conversion, and merge/save. At `0882c8074215edc24e2ee5ac25e99cdccddb7e34`, conversion returns `unmatched` and `total`, but `Annotator.tsx` L2356–2366 reports only added/updated counts. A chapter-start CFI can be emitted when exact matching fails, so “Imported N annotations” does not communicate anchor quality.

Could the result distinguish exact matches, chapter fallbacks, skipped entries, and ambiguity? A details panel or exportable reconciliation record would help verify migrations. Existing duplicate/no-op and deletion-resurrection behavior should remain intact.

Suggested fixtures: repeated words within a chapter, the same phrase in two chapters, a phrase split by inline elements, and an unmatched phrase. This is a source-grounded enhancement; v10.8 export behavior has not been tested here. Verify offset/color semantics with actual lawful exports before broad compatibility claims.

Sources: [converter][re-mrexpt], [Annotator][re-annotator], [merge tests][re-mrexpt-tests].

### Draft D — comment on MJ PDF GitLab #90

**Context: Current-source confirmation and large-font layout coverage**

At canonical commit `aef93faaa4c7fa7df373d415e1c874412cba2db5`, `app/src/main/res/layout/item_home_chip_row.xml` still gives Completed/Abandoned `layout_width="0dp"`, equal `layout_weight="1"`, and fixed horizontal margins, consistent with the width-allocation concern.

I have not independently rendered the reported combination. Could a change cover 540 dpi/fontScale 1.3, the 420/1.0 baseline, a narrow window, and a long translation? Content-sized wrapping/scrolling could retain full labels without shrinking text; selection and accessibility focus need checking too.

Source: [pinned XML][mj-chips].

## 7. Search boundaries and contradictions

### Bounded duplicate searches

GitHub searches used `https://api.github.com/search/issues`, scoped to the repository and sorted by `updated` descending. Responses included state, URL, update time, and body excerpts. **Only the returned first page was examined.**

| Repository | Queries and examined-page bounds |
|---|---|
| KOReader | `is:issue exporter`: 6/156; `is:issue is:open "export" in:title`: 12/13; `is:issue mime`: 6/47 |
| Librera | `is:issue foliate`: 6/6, including a LibreraX report; no all-issue sweep |
| Book's Story | `is:issue PDF`: 6/27; `is:issue markdown`: 2/2 |
| Readest | `is:issue KOSync`: 6/43; `is:issue is:open sync`: 10/22; `is:issue "syncBooks"`: 3/3; `is:issue mrexpt`: 0; `is:issue "Moon"`: 10/38 |
| MuPDF Android Viewer | `is:issue is:open`: 6/31; `is:issue link`: 3/3 |
| MJ PDF | GitLab `/api/v4/projects/38392439/issues?state=opened&per_page=12&order_by=updated_at&sort=desc`: newest returned page, eleven entries |
| Orion / Anx | No issue sweep; novelty/absence not established |

Readest's literal `mrexpt` search returning zero does **not** establish absence of related issues/PRs. “Moon” returned many reports; PRs and all comments were not exhausted. Closed issues do not prove a working fix, and open issues do not prove continuing absence.

### Corrections that materially affect comparison

1. **Readest Moon import exists and is UI-wired.** Precision, fidelity, and reconciliation are stronger proposals than implementing a new importer.
2. **KOReader export color filtering exists.** #14334 remains open; color labeling and hierarchy are separate concerns.
3. **Librera has foliate/CFI/PDFium paths.** Old percentage-sync reports and its frozen README notice cannot override current source/activity.
4. **MJ PDF v3 has substantial annotation/form/text features.** Canonical GitLab is fresher than GitHub; Never-keep-copy is documented and text exports are implemented.
5. **Book's Story's Markdown claim conflicts with inspected dispatch.** Six extension gates were observed; seven documented extensions are not seven verified implementations.
6. **MuPDF's simplified viewer is not its full editor.** Its README excludes editing/forms; the chooser description lags SAF code.
7. **Anx OPDS is in progress in documentation.** Directories and historical licenses do not establish present-release capabilities.
8. **Readest roadmap text can lag source.** Handwriting-related files exist although README calls handwriting planned; usable support was not established. An open E2EE request likewise does not prove absence when architecture describes encryption-related components.

### Coverage limits

- No runtime, latency, battery, accessibility, rendering-fidelity, or sync-convergence comparison was executed. “Fast,” “accurate,” and “privacy-focused” remain documentation claims rather than measurements.
- No APK/source reproducibility, release signatures, full dependency-license audit, store entitlements, or binary provenance validation was performed for alternatives.
- The unauthenticated GitHub core API quota was exhausted after metadata/commit/tree calls. Remaining work used public raw files, HTML tree data, and the separate issue-search resource. Failed requests supply no absence evidence.
- `https://mupdf.com/docs/android.html` returned 404 and was excluded as product evidence; the official repository supplied viewer-specific sources.
- Selected files/ranges were inspected. Referenced tests were read or located, **not run**. No new defect is labeled runtime-confirmed.
- Orion and Anx have lighter documentation/license/build review; their preliminary contribution routes are not counted among the 21 scoped proposals.
- The 21 proposals concern specific alternatives and existing extension points. They are not 21 confirmed bugs or missing features in every reader.

## 8. Contribution priorities and project policies

1. **Narrow reproduction targets:** K01 CBR MIME handling and U01 page-zero links, using small synthetic/public-domain fixtures.
2. **Moon migration value:** R01/R02 using lawful `.mrexpt` exports and shared compatibility fixtures. Existing import support makes this extension work.
3. **Existing-report follow-ups:** MJ chip scaling #90 and Readest publisher-CSS #7417, keeping reporter measurements separate from independent results.
4. **Contribution routing:** Book's Story accepts suggestions/reproducers/translations but declines code PRs. Recheck each project's policy and related work before implementation/submission.

Readest [CONTRIBUTING.md L7–14, L172–187][re-contributing] requests an issue before opinion-driven changes, issue-linked PRs, manual functional testing, and agent/model attribution for assisted commits. KOReader invites fixes/features/translations/docs; Orion invites PRs/translations; MJ PDF directs code/issues to GitLab and translations to resource files. All drafts above remain unsubmitted.

## Source ledger

All sources below were retrieved **2026-11-21**. Code links preserve the reviewed revision. Line ranges in the report describe the inspected excerpts; unanchored file links intentionally permit inspection of surrounding context.

[ko-readme]: https://github.com/koreader/koreader/blob/07d7b22098ef1693f090a881abf27ca5a25fa50a/README.md
[ko-license]: https://github.com/koreader/koreader/blob/07d7b22098ef1693f090a881abf27ca5a25fa50a/COPYING
[ko-commit]: https://github.com/koreader/koreader/commit/07d7b22098ef1693f090a881abf27ca5a25fa50a
[ko-registry]: https://github.com/koreader/koreader/blob/07d7b22098ef1693f090a881abf27ca5a25fa50a/frontend/document/documentregistry.lua#L31-L225
[ko-pdf]: https://github.com/koreader/koreader/blob/07d7b22098ef1693f090a881abf27ca5a25fa50a/frontend/document/pdfdocument.lua#L370-L416
[ko-ui]: https://github.com/koreader/koreader/blob/07d7b22098ef1693f090a881abf27ca5a25fa50a/frontend/apps/reader/readerui.lua
[ko-export-base]: https://github.com/koreader/koreader/blob/07d7b22098ef1693f090a881abf27ca5a25fa50a/plugins/exporter.koplugin/base.lua#L23-L125
[ko-export-main]: https://github.com/koreader/koreader/blob/07d7b22098ef1693f090a881abf27ca5a25fa50a/plugins/exporter.koplugin/main.lua
[ko-json]: https://github.com/koreader/koreader/blob/07d7b22098ef1693f090a881abf27ca5a25fa50a/plugins/exporter.koplugin/target/json.lua#L26-L73
[ko-md]: https://github.com/koreader/koreader/blob/07d7b22098ef1693f090a881abf27ca5a25fa50a/plugins/exporter.koplugin/template/md.lua#L39-L65
[ko-markdown]: https://github.com/koreader/koreader/blob/07d7b22098ef1693f090a881abf27ca5a25fa50a/plugins/exporter.koplugin/target/markdown.lua

[li-readme]: https://github.com/foobnix/LibreraReader/blob/b7378bbde373bbf8b80842f3e47ea444fa9fd542/README.md
[li-license]: https://github.com/foobnix/LibreraReader/blob/b7378bbde373bbf8b80842f3e47ea444fa9fd542/LICENSE.txt
[li-site]: https://librera.app/librera-reader/
[li-build]: https://github.com/foobnix/LibreraReader/blob/b7378bbde373bbf8b80842f3e47ea444fa9fd542/app/build.gradle
[li-codec]: https://github.com/foobnix/LibreraReader/blob/b7378bbde373bbf8b80842f3e47ea444fa9fd542/app/src/main/java/org/ebookdroid/core/codec/CodecDocument.java#L11-L120
[li-foliate]: https://github.com/foobnix/LibreraReader/blob/b7378bbde373bbf8b80842f3e47ea444fa9fd542/app/src/main/java/org/ebookdroid/droids/foliate/codec/FoliateDocument.java
[li-renderer]: https://github.com/foobnix/LibreraReader/blob/b7378bbde373bbf8b80842f3e47ea444fa9fd542/app/src/main/java/org/ebookdroid/droids/foliate/codec/FoliateRenderer.java
[li-css]: https://github.com/foobnix/LibreraReader/blob/b7378bbde373bbf8b80842f3e47ea444fa9fd542/app/src/main/java/org/ebookdroid/droids/foliate/codec/FoliateCss.java

[mj-meta]: https://gitlab.com/api/v4/projects/38392439
[mj-commit-api]: https://gitlab.com/api/v4/projects/38392439/repository/commits/aef93faaa4c7fa7df373d415e1c874412cba2db5
[mj-site]: https://mudlej.com/projects/mj-pdf
[mj-readme]: https://gitlab.com/mudlej_android/mj_pdf_reader/-/blob/aef93faaa4c7fa7df373d415e1c874412cba2db5/README.md
[mj-license]: https://gitlab.com/mudlej_android/mj_pdf_reader/-/blob/aef93faaa4c7fa7df373d415e1c874412cba2db5/LICENSE
[mj-build]: https://gitlab.com/mudlej_android/mj_pdf_reader/-/blob/aef93faaa4c7fa7df373d415e1c874412cba2db5/app/build.gradle#L51
[mj-settings]: https://gitlab.com/mudlej_android/mj_pdf_reader/-/blob/aef93faaa4c7fa7df373d415e1c874412cba2db5/settings.gradle
[mj-db]: https://gitlab.com/mudlej_android/mj_pdf_reader/-/blob/aef93faaa4c7fa7df373d415e1c874412cba2db5/app/src/main/java/com/gitlab/mudlej/MjPdfReader/data/AppDatabase.kt
[mj-search]: https://gitlab.com/mudlej_android/mj_pdf_reader/-/blob/aef93faaa4c7fa7df373d415e1c874412cba2db5/app/src/main/java/com/gitlab/mudlej/MjPdfReader/core/text/TextSearch.kt
[mj-chips]: https://gitlab.com/mudlej_android/mj_pdf_reader/-/blob/aef93faaa4c7fa7df373d415e1c874412cba2db5/app/src/main/res/layout/item_home_chip_row.xml
[mj-extractor]: https://gitlab.com/mudlej_android/mj_pdf_reader/-/blob/aef93faaa4c7fa7df373d415e1c874412cba2db5/app/src/main/java/com/gitlab/mudlej/MjPdfReader/pdf/PdfExtractor.kt
[mj-text-loader]: https://gitlab.com/mudlej_android/mj_pdf_reader/-/blob/aef93faaa4c7fa7df373d415e1c874412cba2db5/app/src/main/java/com/gitlab/mudlej/MjPdfReader/ui/text_mode/TextModeContentLoader.kt
[mj-highlights]: https://gitlab.com/mudlej_android/mj_pdf_reader/-/blob/aef93faaa4c7fa7df373d415e1c874412cba2db5/app/src/main/java/com/gitlab/mudlej/MjPdfReader/ui/userhighlights/UserHighlightsActivity.kt
[mj-notes]: https://gitlab.com/mudlej_android/mj_pdf_reader/-/blob/aef93faaa4c7fa7df373d415e1c874412cba2db5/app/src/main/java/com/gitlab/mudlej/MjPdfReader/ui/usernotes/UserNotesActivity.kt
[mj-annotation-logic]: https://gitlab.com/mudlej_android/mj_pdf_reader/-/blob/aef93faaa4c7fa7df373d415e1c874412cba2db5/app/src/main/java/com/gitlab/mudlej/MjPdfReader/ui/usernotes/AnnotationListLogic.kt
[mj-roadmap]: https://gitlab.com/mudlej_android/mj_pdf_reader/-/blob/aef93faaa4c7fa7df373d415e1c874412cba2db5/roadmap.md

[or-readme]: https://github.com/max-kammerer/orion-viewer/blob/1adfe2da0791d1e563fd8966fc3107e9ad79fc74/README.md
[or-license]: https://github.com/max-kammerer/orion-viewer/blob/1adfe2da0791d1e563fd8966fc3107e9ad79fc74/LICENSE
[or-version]: https://github.com/max-kammerer/orion-viewer/blob/1adfe2da0791d1e563fd8966fc3107e9ad79fc74/orion-viewer/version.properties
[or-build]: https://github.com/max-kammerer/orion-viewer/blob/1adfe2da0791d1e563fd8966fc3107e9ad79fc74/build.gradle#L26-L37
[or-app-build]: https://github.com/max-kammerer/orion-viewer/blob/1adfe2da0791d1e563fd8966fc3107e9ad79fc74/orion-viewer/build.gradle

[mu-readme]: https://github.com/ArtifexSoftware/mupdf-android-viewer/blob/f2f75636fb9d5508f7d366bc55bac7fbdf5a38a0/README
[mu-license]: https://github.com/ArtifexSoftware/mupdf-android-viewer/blob/f2f75636fb9d5508f7d366bc55bac7fbdf5a38a0/COPYING
[mu-tree]: https://github.com/ArtifexSoftware/mupdf-android-viewer/tree/f2f75636fb9d5508f7d366bc55bac7fbdf5a38a0
[mu-build]: https://github.com/ArtifexSoftware/mupdf-android-viewer/blob/f2f75636fb9d5508f7d366bc55bac7fbdf5a38a0/lib/build.gradle#L1-L24
[mu-manifest]: https://github.com/ArtifexSoftware/mupdf-android-viewer/blob/f2f75636fb9d5508f7d366bc55bac7fbdf5a38a0/lib/src/main/AndroidManifest.xml#L10-L25
[mu-library]: https://github.com/ArtifexSoftware/mupdf-android-viewer/blob/f2f75636fb9d5508f7d366bc55bac7fbdf5a38a0/app/src/main/java/com/artifex/mupdf/viewer/app/LibraryActivity.java#L24-L66
[mu-core]: https://github.com/ArtifexSoftware/mupdf-android-viewer/blob/f2f75636fb9d5508f7d366bc55bac7fbdf5a38a0/lib/src/main/java/com/artifex/mupdf/viewer/MuPDFCore.java
[mu-activity]: https://github.com/ArtifexSoftware/mupdf-android-viewer/blob/f2f75636fb9d5508f7d366bc55bac7fbdf5a38a0/lib/src/main/java/com/artifex/mupdf/viewer/DocumentActivity.java
[mu-reader]: https://github.com/ArtifexSoftware/mupdf-android-viewer/blob/f2f75636fb9d5508f7d366bc55bac7fbdf5a38a0/lib/src/main/java/com/artifex/mupdf/viewer/ReaderView.java
[mu-page]: https://github.com/ArtifexSoftware/mupdf-android-viewer/blob/f2f75636fb9d5508f7d366bc55bac7fbdf5a38a0/lib/src/main/java/com/artifex/mupdf/viewer/PageView.java#L565-L598

[bs-readme]: https://github.com/Acclorite/book-story/blob/6ffefb974ae8eac542e36eb659f77e4802735fd9/README.md
[bs-build]: https://github.com/Acclorite/book-story/blob/6ffefb974ae8eac542e36eb659f77e4802735fd9/app/build.gradle.kts#L15-L25
[bs-manifest]: https://github.com/Acclorite/book-story/blob/6ffefb974ae8eac542e36eb659f77e4802735fd9/app/src/main/AndroidManifest.xml#L38-L49
[bs-extensions]: https://github.com/Acclorite/book-story/blob/6ffefb974ae8eac542e36eb659f77e4802735fd9/app/src/main/java/ua/acclorite/book_story/core/data/ExtensionsData.kt#L11-L19
[bs-file-dispatch]: https://github.com/Acclorite/book-story/blob/6ffefb974ae8eac542e36eb659f77e4802735fd9/app/src/main/java/ua/acclorite/book_story/data/parser/file/FileParserImpl.kt
[bs-dispatch]: https://github.com/Acclorite/book-story/blob/6ffefb974ae8eac542e36eb659f77e4802735fd9/app/src/main/java/ua/acclorite/book_story/data/parser/content/ContentParserImpl.kt
[bs-pdf]: https://github.com/Acclorite/book-story/blob/6ffefb974ae8eac542e36eb659f77e4802735fd9/app/src/main/java/ua/acclorite/book_story/data/parser/content/PdfContentParser.kt
[bs-parser-versions]: https://github.com/Acclorite/book-story/blob/6ffefb974ae8eac542e36eb659f77e4802735fd9/app/src/main/java/ua/acclorite/book_story/core/data/ParsersData.kt
[bs-filesystem]: https://github.com/Acclorite/book-story/blob/6ffefb974ae8eac542e36eb659f77e4802735fd9/app/src/main/java/ua/acclorite/book_story/data/repository/FileSystemRepositoryImpl.kt
[bs-cached-file]: https://github.com/Acclorite/book-story/blob/6ffefb974ae8eac542e36eb659f77e4802735fd9/app/src/main/java/ua/acclorite/book_story/data/storage/file/CachedFile.kt
[bs-repository]: https://github.com/Acclorite/book-story/blob/6ffefb974ae8eac542e36eb659f77e4802735fd9/app/src/main/java/ua/acclorite/book_story/data/repository/BookRepositoryImpl.kt
[bs-state]: https://github.com/Acclorite/book-story/blob/6ffefb974ae8eac542e36eb659f77e4802735fd9/app/src/main/java/ua/acclorite/book_story/presentation/reader/ReaderState.kt
[bs-reader-content]: https://github.com/Acclorite/book-story/blob/6ffefb974ae8eac542e36eb659f77e4802735fd9/app/src/main/java/ua/acclorite/book_story/ui/reader/ReaderContent.kt
[bs-layout-content]: https://github.com/Acclorite/book-story/blob/6ffefb974ae8eac542e36eb659f77e4802735fd9/app/src/main/java/ua/acclorite/book_story/ui/reader/ReaderLayoutContent.kt
[bs-paragraph]: https://github.com/Acclorite/book-story/blob/6ffefb974ae8eac542e36eb659f77e4802735fd9/app/src/main/java/ua/acclorite/book_story/ui/reader/ReaderLayoutContentParagraph.kt
[bs-scaffold]: https://github.com/Acclorite/book-story/blob/6ffefb974ae8eac542e36eb659f77e4802735fd9/app/src/main/java/ua/acclorite/book_story/ui/reader/ReaderScaffold.kt
[bs-paged]: https://github.com/Acclorite/book-story/blob/6ffefb974ae8eac542e36eb659f77e4802735fd9/app/src/main/java/ua/acclorite/book_story/ui/reader/ReaderLayoutPaged.kt
[bs-tests]: https://github.com/Acclorite/book-story/blob/6ffefb974ae8eac542e36eb659f77e4802735fd9/app/src/test/java/ua/acclorite/book_story/data/parser/content/ContentParserRegressionTest.kt

[re-readme]: https://github.com/readest/readest/blob/0882c8074215edc24e2ee5ac25e99cdccddb7e34/README.md
[re-license]: https://github.com/readest/readest/blob/0882c8074215edc24e2ee5ac25e99cdccddb7e34/LICENSE
[re-package]: https://github.com/readest/readest/blob/0882c8074215edc24e2ee5ac25e99cdccddb7e34/apps/readest-app/package.json
[re-layout-doc]: https://github.com/readest/readest/blob/0882c8074215edc24e2ee5ac25e99cdccddb7e34/apps/readest-app/docs/code-layout.md
[re-architecture]: https://github.com/readest/readest/blob/0882c8074215edc24e2ee5ac25e99cdccddb7e34/apps/readest-app/docs/architecture.md
[re-app-service]: https://github.com/readest/readest/blob/0882c8074215edc24e2ee5ac25e99cdccddb7e34/apps/readest-app/src/services/appService.ts#L47-L131
[re-kosync]: https://github.com/readest/readest/blob/0882c8074215edc24e2ee5ac25e99cdccddb7e34/apps/readest-app/src/services/sync/KOSyncClient.ts
[re-sync-provider]: https://github.com/readest/readest/blob/0882c8074215edc24e2ee5ac25e99cdccddb7e34/apps/readest-app/src/services/sync/file/provider.ts
[re-sync-registry]: https://github.com/readest/readest/blob/0882c8074215edc24e2ee5ac25e99cdccddb7e34/apps/readest-app/src/services/sync/file/providerRegistry.ts
[re-sync-gate]: https://github.com/readest/readest/blob/0882c8074215edc24e2ee5ac25e99cdccddb7e34/apps/readest-app/src/services/sync/cloudSyncProvider.ts
[re-import-registry]: https://github.com/readest/readest/blob/0882c8074215edc24e2ee5ac25e99cdccddb7e34/apps/readest-app/src/services/annotation/providers/index.ts
[re-import-dialog]: https://github.com/readest/readest/blob/0882c8074215edc24e2ee5ac25e99cdccddb7e34/apps/readest-app/src/app/reader/components/annotator/ImportAnnotationsDialog.tsx
[re-annotator]: https://github.com/readest/readest/blob/0882c8074215edc24e2ee5ac25e99cdccddb7e34/apps/readest-app/src/app/reader/components/annotator/Annotator.tsx
[re-mrexpt-parser]: https://github.com/readest/readest/blob/0882c8074215edc24e2ee5ac25e99cdccddb7e34/apps/readest-app/src/utils/mrexpt.ts
[re-mrexpt]: https://github.com/readest/readest/blob/0882c8074215edc24e2ee5ac25e99cdccddb7e34/apps/readest-app/src/services/annotation/providers/mrexpt.ts
[re-mrexpt-tests]: https://github.com/readest/readest/blob/0882c8074215edc24e2ee5ac25e99cdccddb7e34/apps/readest-app/src/__tests__/services/mrexpt-import.test.ts
[re-style]: https://github.com/readest/readest/blob/0882c8074215edc24e2ee5ac25e99cdccddb7e34/apps/readest-app/src/utils/style.ts
[re-viewer]: https://github.com/readest/readest/blob/0882c8074215edc24e2ee5ac25e99cdccddb7e34/apps/readest-app/src/app/reader/components/FoliateViewer.tsx
[re-contributing]: https://github.com/readest/readest/blob/0882c8074215edc24e2ee5ac25e99cdccddb7e34/CONTRIBUTING.md

[an-readme]: https://github.com/Anxcye/anx-reader/blob/0c7fc1ad4551f7dbbeba6a6468f69d830957fa2a/README.md
[an-license]: https://github.com/Anxcye/anx-reader/blob/0c7fc1ad4551f7dbbeba6a6468f69d830957fa2a/LICENSE
[an-build]: https://github.com/Anxcye/anx-reader/blob/0c7fc1ad4551f7dbbeba6a6468f69d830957fa2a/pubspec.yaml
[an-commit]: https://github.com/Anxcye/anx-reader/commit/0c7fc1ad4551f7dbbeba6a6468f69d830957fa2a.patch

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
