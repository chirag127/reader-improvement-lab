---
type: Research
title: Desktop and web reader alternatives
description: Ten bounded reader dossiers, four pinned implementation reviews, and thirteen draft contribution candidates with explicit evidence limits.
tags: [readers, desktop, web, pdf, accessibility, annotations, open-source, research]
timestamp: 2026-11-21T14:46:56Z
---

# Desktop and web reader alternatives

## Scope and evidence contract

This lane covers **PDF.js, Okular, Sioyek, Zotero Reader, SumatraPDF, GNOME Papers, Evince, calibre, Foliate, and Thorium Reader**. It includes **10 application/library dossiers**, **4 targeted implementation reviews**, and **13 alternative-specific proposals**. It is a bounded, extensible catalog, not exhaustive market coverage. PDF.js is an embeddable PDF implementation with a viewer; calibre is also a library/conversion system; these are adjacent workflow comparators rather than interchangeable Android applications.

- [Structured inventory](../data/alternatives-desktop-web.json): identities, licenses, sourced capabilities, and exact review boundaries.
- [Structured proposals](../data/alternative-proposals-desktop-web.json): `ALT-DW-001` through `ALT-DW-013`, all **draft**.
- [Investigation design](design.md): repository-wide evidence contract.
- [Android alternatives](alternatives-android.md): the separate Android lane.

**Observed date: 2026-11-21.** Public HTTP research was collected between approximately **13:50 and 14:47 UTC**. Dates below distinguish release dates, feed update dates, source versions, and repository push metadata. Code was retrieved at full 40-character commit IDs, using public raw files and public repository tree pages. No reader application, screen reader, build, or upstream test suite was run in this lane. One small JavaScript comparator expression was evaluated independently; its narrow result is recorded below and is not a Zotero runtime result.

Evidence labels:

| Label | Meaning |
|---|---|
| **D — documented** | First-party documentation describes a capability; application behavior is untested here. |
| **C — static-observation** | A declaration or implementation path was read at the cited source revision. |
| **T — upstream-report** | An issue/PR reports a problem or proposed fix; its author's measurements are not our measurements. |
| **P — proposal** | An improvement or investigation to evaluate, with prospective acceptance checks. |
| **U — unknown/blocked** | The bounded evidence does not establish a conclusion. |

For comparison with Moon+, use the parent's baseline. Its [official feature page](https://moondownload.com/) already documents PDF, annotations, dictionaries, TTS, themes, OPDS, and synchronization. Those capabilities must not be proposed as wholly absent merely because another reader also has them. The supplied APK's provenance and failed signature verification are handled by the parent; this report makes no finding about that artifact or an official Play build.

## 1. Canonical identities, licenses, and release evidence

GitHub metadata was observed through `https://api.github.com/repos/<owner>/<repo>` at approximately 13:50 UTC; source refs through `https://github.com/<owner>/<repo>/info/refs?service=git-upload-pack` at approximately 13:51 UTC. All ten GitHub repositories/mirrors returned `archived:false` at that observation. A GitHub mirror's state does not independently establish the canonical GitLab project's state. Push dates below are repository metadata, **not timestamps of the pinned commit**.

| ID / canonical repository | Examined source revision | Verified license evidence | Release/status evidence at observation |
|---|---|---|---|
| `pdfjs` — <https://github.com/mozilla/pdf.js> | `57dead10694ead8fb21b97f7812fc95311a38ea1`, `master` | **Apache-2.0**, [LICENSE][pdf-license] and package declaration | [v6.5.438][pdf-release], published **2026-11-01**; release commit `0a4153349dc473ba950fc17941c5ca7eda43c1de`. Repository pushed 2026-11-21. Reviewed master is later than the release. |
| `okular` — <https://invent.kde.org/graphics/okular> | GitHub mirror `KDE/okular`: `110d017ab20368a449a21fcc2566f4ef7baaf3ae`, `master` | **GPL-2.0-or-later**, [official site][okular-site] and SPDX headers in reviewed core/backend files | **26.08.3**, [KDE Gear announcement, 2026-11-05][okular-release], with [Okular source tarball in that release][okular-tarballs]. Tag `v26.08.3` peels to `24f5e83a1aa26e450362b74b50304d7684111f0e`. Reviewed CMake version is **27.03.70 development**, not the stable release. Mirror pushed 2026-11-21. |
| `sioyek` — <https://github.com/ahrm/sioyek> | `1e2f8037353724a83ccb10a697e28e295383e017`, `development` | **GPL v3**, [LICENSE][sioyek-license]; only/or-later qualifier not established. Bundled dependency terms require separate review. | [v2.0.0][sioyek-release], published **2022-12-16**, commit `7cb948face57b56ee55224b62d841c316e85294c`. [Release feed][sioyek-feed] also has `sioyek3-alpha0`, entry updated **2024-09-12**, warning of database incompatibility. Development pushed 2026-11-04. A build-file `VERSION=2.0.0` does not identify the development build as the old stable binary. |
| `zotero-reader` — <https://github.com/zotero/reader> | `09af7187f0b219cec3e32f5fec56f77269a44b67`, `master` | **AGPL v3**, explicit grant in [COPYING][zotero-license]; preserve third-party notices | Host application [Zotero 10.0.9, 2026-11-10][zotero-changelog] is a Mac-only release; 10.0.8 is dated 2026-11-06. Reader `package.json` says `2.0.0`, **not** the host version. No reader tags appeared in the observed ref advertisement. Reader pushed 2026-11-17. |
| `sumatrapdf` — <https://github.com/sumatrapdfreader/sumatrapdf> | `e6519ebc6b239330d9d0c4d9778e0e68762d3e78`, `master` | [AUTHORS][sumatra-authors]: most source **GPL v3**, BSD portions, and **AGPL v3 section 13 applies via MuPDF**. A simple GPL-only label omits an explicit upstream qualification. | [3.6.1][sumatra-release], published **2026-04-06**, commit `16c59fde8b824ab54c56f23aef910a6fdd874ad0`. Current documentation mixes stable capabilities with **3.7/pre-release** additions. Repository pushed 2026-11-21. No application implementation review here. |
| `papers` — <https://gitlab.gnome.org/GNOME/papers> | GitHub mirror `GNOME/papers`: `fe4bc08d1a5427a33abc9bead467150e3531c4c8`, `main` | **GPL-2.0-or-later**, [AppStream project license][papers-meta] and COPYING | [GNOME app page][papers-app] identifies **51.1, 2026-10-09**. [Source server][papers-releases] has 51.1 uploaded 2026-10-12. Reviewed main AppStream release list ends at 51.0; it is not an authoritative latest-maintenance-release list. Mirror pushed 2026-11-21. |
| `evince` — <https://gitlab.gnome.org/GNOME/evince> | GitHub mirror `GNOME/evince`: `e822030005f22231052667d51398a84327004924`, `main` | **GPL-2.0-or-later**, [AppStream project license][evince-meta]; README/COPYING identify GPL v2 | [Source server][evince-releases] identifies **48.5**, uploaded **2026-11-16**, with [48.5 release notes][evince-news]. Main AppStream/NEWS describe **49.alpha.1**, not the latest stable branch. Mirror pushed 2026-11-20. Do not describe Evince as abandoned or Papers as an in-place rename of this repository. |
| `calibre` — <https://github.com/kovidgoyal/calibre> | `d69ad111794cf2032264d2b02b3f9b9adfb139a2`, `master`; also peeled `v9.19.0` | **GPL v3**, [LICENSE][calibre-license], with per-file exceptions in [COPYRIGHT][calibre-copyright] | [9.19, 2026-11-21][calibre-news]. Tag `v9.19.0` peels to the examined revision. Repository pushed 2026-11-21. Documentation/license review, not converter implementation review. |
| `foliate` — <https://github.com/johnfactotum/foliate> | `67b6676d3f936c5edea91d4d903385ef39dd25c0`, `gtk4` | **GPL-3.0-or-later**, [README][foliate-readme] and [AppStream][foliate-meta]. Bundled foliate-js is MIT, PDF.js Apache-2.0; other bundled libraries retain their terms. | [3.3.0, 2025-04-01][foliate-release], commit `6846cf62ef3ff4f0162f1b288f44d6dcce5f1a19`. Repository pushed 2026-04-08. Release age is not evidence of abandonment. |
| `thorium` — <https://github.com/edrlab/thorium-reader> | `f603ca2848eb567b1d32cdfd6728362d73f8f557`, `develop` | **BSD-3-Clause**, [LICENSE][thorium-license]. Production LCP component is **not included** in the public source; [README][thorium-readme] explains the boundary. | [Desktop 3.5.1, 2026-09-02][thorium-release], peeled commit `137e8901196bc47173580856105fe78b40473570`. Examined package version **3.6.0-beta.1**; automated test-build tags are not stable releases. Repository pushed 2026-11-21. |

The GPL/AGPL version-only descriptions deliberately avoid inventing an `-only` or `-or-later` grant where the reviewed declaration did not settle it. This is identification of upstream license evidence, not a complete dependency-license audit or permission to copy copyleft code into a proprietary reader.

## 2. Confirmed existing capabilities and functional comparison

The following are **D/C capability observations**, not tested performance or accessibility rankings. Numbered items provide 6–12 documented/code-observed capabilities per entry. Desktop, browser, mobile-source, and released-product support are distinguished.

### PDF.js — browser viewing and reusable PDF layers

**Platforms/formats:** modern and legacy browser builds, built into Firefox, official Chrome extension; PDF input. Node-facing display APIs are a library surface, not a desktop reader product. [README][pdf-readme], [getting started][pdf-start].

1. **D:** PDF parsing and rendering based on web standards.
2. **C:** worker-backed loading/parsing and custom range transport/chunk sizing. [Display API][pdf-api].
3. **C:** in-document search with case, diacritic and whole-word options, normalized text and original-text position mapping. [Find controller][pdf-find].
4. **C:** progressive match counts and a polite live region for search messages. [Viewer markup][pdf-viewer].
5. **C:** highlight editing, serialization and associated comment data. [Highlight editor][pdf-highlight].
6. **C:** free-text, ink and image-stamp controls in the viewer. [Viewer markup][pdf-viewer].
7. **C:** key/value annotation/form storage with modified-state callbacks. [Annotation storage][pdf-storage].
8. **C:** tagged-PDF structure mapping for headings, lists, tables, language, alternative text and MathML. [Structure builder][pdf-struct]. These DOM structures do not prove assistive-technology interoperability.
9. **C:** printing uses a frozen copy of serializable annotation data. [Annotation storage][pdf-storage].
10. **C:** save/download, presentation mode and a current-view bookmark link appear in the viewer. [Viewer markup][pdf-viewer].

**P — comparison value:** the strongest browser embedding and accessible-structure implementation reference here. **U/limits:** generic viewer vs Firefox integration can expose different features; browser behavior and memory limits need their own tests. It does not by itself establish an Android library/catalog/sync workflow equivalent to Moon+.

### Okular — native multi-format document work

**Platforms/formats:** Linux and Windows packages; macOS nightly builds explicitly described as untested on the [download page][okular-download]. PDF, EPUB, DjVu, Markdown, images and comics, with format-specific plugins. A Kirigami mobile/Android build target exists in source; no mobile distribution or parity test was performed. [README][okular-readme], [CMake][okular-cmake].

1. **D:** read multiple document/image/comic formats. [Official site][okular-site].
2. **D:** native PDF annotations, including inline/pop-up notes, highlights, underlines and added text. [README][okular-readme], [site][okular-site].
3. **D:** text, area and table selection/copy tools. [Site][okular-site].
4. **D:** magnifier mode. [Site][okular-site].
5. **D:** page thumbnails and contents navigation. [Site][okular-site].
6. **D:** inspect and verify digital signatures and sign PDFs. [Site][okular-site]. This is distinct from drawing a signature image.
7. **C:** optional Qt TextToSpeech integration in the desktop build. [CMake][okular-cmake]. Availability depends on build dependencies.
8. **C:** asynchronous generator capabilities for rendering and text extraction. [Generator interface][okular-generator].
9. **C:** undo/redo command objects for adding, removing, modifying and translating annotations. [Document commands][okular-commands].
10. **C:** touchscreen page swiping, pinch zoom and drag scrolling in the mobile component. [DocumentView.qml][okular-mobile].

**P — comparison value:** native PDF review, signatures, document plugins and robust annotation command separation. **Limits:** desktop features must not be projected onto the mobile shell; format plugins/build options affect support. No measured rendering or energy comparison with Moon+ is made.

### Sioyek — research navigation and linked reading locations

**Platforms/formats:** official README lists Windows, macOS and Linux installers; PDF-focused. Development contains touch/Android-related code, but this lane does not claim a shipped Android counterpart. [README][sioyek-readme].

1. **D:** quick-open search over previously opened files.
2. **D:** searchable table of contents.
3. **D:** smart jumps to referenced figures/bibliography entries, including some PDFs without explicit links.
4. **D:** temporary overview of figures, tables or references.
5. **D:** local lowercase and global uppercase named marks.
6. **D:** global text-named bookmarks.
7. **D:** multiple highlight types and search over highlights.
8. **D:** portals linking a reading location to a second location, displayed in a helper window.
9. **D:** configurable key bindings and preferences. Items 1–9 are documented in the [pinned README][sioyek-readme]; heuristic smart jumps are not a guarantee for arbitrary documents.
10. **C:** the development search worker supports page ranges, case/smart-case selection, and literal/regex search. [Renderer search loop][sioyek-search].

**P — comparison value:** reference previews, return-to-context marks and persistent portal relationships are useful research-workflow patterns to evaluate on smaller screens. **Limits:** multi-monitor and keyboard-centric workflows do not automatically fit a phone; stable 2.0, the alpha and current development have important dependency/database differences.

### Zotero Reader — annotations connected to research notes

**Platforms/formats:** the host desktop application supports Windows, macOS and Linux per [system requirements][zotero-platforms]. This reader repository builds desktop/web and mobile integrations; those are distinct adapters, not proof of equal feature support. PDF, EPUB and HTML snapshots are named in the [README][zotero-readme].

1. **D:** PDF, EPUB and HTML reading/annotation. [README][zotero-readme].
2. **D:** unlocked selection pop-up and locked repeated highlighting/underlining modes. [PDF reader guide][zotero-guide].
3. **D:** add annotations to notes with page backlinks and citations. [Guide][zotero-guide].
4. **D:** build notes from annotations in one PDF or across multiple library items. [Guide][zotero-guide].
5. **D:** return from a note to the source annotation using “Show on Page”, and customize annotation note templates. [Guide][zotero-guide].
6. **D:** annotations are stored in Zotero's database; export a PDF with embedded annotations for external-reader visibility. [Guide][zotero-guide]. Database storage is an existing design choice, not a claim of absent export.
7. **D:** Zotero 10 Reading Mode presents PDFs as reflowable text while retaining rendered figures/tables and sharing positions/annotations with the fixed-layout view. [Changelog][zotero-changelog].
8. **D:** smarter Read Aloud skips selected non-prose structures and reads paragraphs across columns/pages, with sentence/word/paragraph highlighting options. [Changelog][zotero-changelog].
9. **C:** annotation filters combine query, color, author, tag and enabled type criteria. [Annotation manager][zotero-annotations].
10. **C:** annotation undo/redo history is exposed to the host, with remapping of IDs when restoring deleted annotations. [Annotation manager][zotero-annotations].
11. **C:** PDF search owns generation-scoped native or semantic-text sessions and contains cancellation/fallback paths. [Search controller][zotero-search].

**P — comparison value:** the clearest end-to-end research-note workflow comparator, including a current PDF reflow mode. **Limits:** host database/sync behavior and the semantic-text producer were not audited; viewing annotations in another application requires the documented export. This is not a neutral proof that Moon+ lacks citations, reflow, export or synchronization.

### SumatraPDF — Windows reading and command-driven navigation

**Platforms/formats:** Windows. Pinned README names PDF, EPUB, MOBI, FB2, comics, CHM, XPS and DjVu. [Format documentation][sumatra-formats] lists additional types, some explicitly **3.7+**. Treat that page as rolling documentation, not a 3.6.1 feature manifest.

1. **D:** multi-format PDF/ebook/comic/document viewing. [Pinned README][sumatra-readme].
2. **D:** portable operation and configurable application-data location. Packaging changes in 3.7 are explicitly distinguished in the [portable guide][sumatra-portable].
3. **D:** PDF highlights, notes, text and shape annotations with saving into the PDF. [Annotation guide][sumatra-annotations].
4. **D:** annotation copy/cut/paste and gesture-grouped undo/redo in current documentation; exact stable-version availability of all current controls is unverified. [Annotation guide][sumatra-annotations].
5. **D:** text search, find-selection and next/previous matches. [Search guide][sumatra-find].
6. **D:** current docs describe a floating results list, snippets and page-range restrictions. [Search guide][sumatra-find]. No claim that all were in 3.6.1.
7. **D:** searchable command palette, with commands, files, tabs, contents, favorites, annotations and settings in current docs. [Palette guide][sumatra-palette]. The palette itself dates to 3.4; modes have evolved.
8. **D:** themes and document color inversion; [3.5 release notes][sumatra-feed] explicitly qualify image quality under inversion.
9. **D:** tabs, drag-out windows and reopen-last-closed actions. [Release notes][sumatra-feed].
10. **D:** command-line/DDE search integration. [Search guide][sumatra-find]. Installer components additionally provide Explorer previews and search filters. [Portable guide][sumatra-portable].

**P — comparison value:** fast-to-invoke reading commands, portable settings, keyboard discovery and external desktop integration. **Limits:** “small/fast” is an upstream positioning claim, not this investigation's benchmark. No Sumatra implementation paths were audited; new 3.7 TTS, forms, tool commands and format features should not be retroactively assigned to 3.6.1.

### GNOME Papers — adaptive document UI with evolving accessibility

**Platforms/formats:** GNOME/Linux, with adaptive mobile-friendly UI; PDF, DjVu, TIFF, CBR/CBT/CBZ/CB7. [App page][papers-app], [AppStream][papers-meta]. “Mobile-friendly” does not establish Android support.

1. **D:** view the listed fixed-layout/document/comic formats.
2. **D:** full-text search contained in a sidebar.
3. **D:** colored annotation list and sidebar editing actions.
4. **D:** ink and free-text annotation tools, documented for 50.0.
5. **D:** underline, strikethrough and wavy markup, documented for 48.0.
6. **D:** digital signing and signature verification, described in 48.0 release notes.
7. **D:** visual signature insertion, added in the documented 51.0 release.
8. **D:** night mode preserving hue and propagating across documents/windows, described for 48.0.
9. **D:** large thumbnail navigation and adaptive layout with keyboard/pointing/touch controls.
10. **D:** search-result announcements to screen readers (50.0), building on “preliminary screen reader support” in 49.0. These are upstream claims, not a WCAG or AT certification.

Items 1–3 and 9: [app page][papers-app]. Version-specific items: [AppStream lines 100–208][papers-meta]. **P — comparison value:** compact/adaptive navigation and visible annotation state. **Limits:** only metadata/documentation were reviewed; forms, signing trust stores, rendering and assistive technologies remain untested. Papers joined GNOME's recommended core set in 49.0; Evince remains separately maintained.

### Evince — established GNOME document and print workflow

**Platforms/formats:** GNOME/Linux in the checked distribution/documentation; PDF, PS/EPS, XPS, DjVu, TIFF, DVI/SyncTeX and comic archives, dependent on optional backends. [README][evince-readme], [AppStream][evince-meta]. Historical ports are outside this verified platform claim.

1. **D:** broad fixed-layout/document backends including PS, XPS and DVI.
2. **D:** document text search. [Help index][evince-help].
3. **D:** thumbnails/outline navigation, direct page jumps and keyboard navigation. [Moving around][evince-navigation].
4. **D:** zoom with fit-page and fit-width modes. [Moving around][evince-navigation].
5. **D:** dual-page, continuous and full-screen viewing. [Moving around][evince-navigation].
6. **D:** pointer-position autoscroll and drag panning. [Moving around][evince-navigation].
7. **D:** annotations, annotation navigation and saving an annotated PDF copy. [Help index][evince-help].
8. **D:** interactive forms and form saving. [Help index][evince-help].
9. **D:** printing, including booklet workflows. [Help index][evince-help].
10. **D:** SyncTeX workflows and inverted page colors. [Help index][evince-help].

**P — comparison value:** predictable document navigation, printing and TeX-oriented integration. **Limits:** release notes report fixes in 48.5, not fresh defects discovered here. Main-branch NEWS/metadata lag stable maintenance releases. Neither shared ancestry nor similar UI makes Evince and Papers the same application.

### calibre — library, conversion and configurable ebook reading

**Platforms/formats:** Windows, macOS and Linux; major ebook formats. PDF is a conversion input/output as well as library material; conversion support must not be equated with full-fidelity native PDF annotation. [README][calibre-readme], [format FAQ][calibre-formats].

1. **D:** library cataloging, metadata fetching, format conversion/editing, device transfer and news-to-ebook workflows. [README][calibre-readme].
2. **D:** paged/flow layouts with mouse, keyboard and touch navigation.
3. **D:** last-read position and bookmarks, optionally saved inside EPUB files.
4. **D:** contents navigation and copyable precise-location URLs.
5. **D:** paragraph-number reference mode.
6. **D:** highlights with notes, chapter lists and library-wide annotation browsing.
7. **D:** annotation synchronization with the Content server's browser viewer.
8. **D:** Read Aloud with word/sentence highlighting, using documented TTS backends.
9. **D:** contains, whole-word, nearby-word and regex searches, including current-chapter scope.
10. **D:** dictionary lookup with custom language-scoped URL sources, including a local HTTP dictionary.
11. **D:** text/image copy and enlarged image viewing.
12. **D:** configurable fonts, margins, headers/footers, colors and custom CSS. Items 2–12: [E-book viewer manual][calibre-viewer].

**P — comparison value:** library-wide annotation discovery, powerful search, stable reference links and desktop/browser reading continuity. **Limits/correction:** the [conversion manual][calibre-conversion] warns about PDF fidelity and says complex/multi-column inputs are unsupported, while the **9.19 changelog specifically claims improved column, paragraph and heading detection**. These sources are not fully reconciled. Do not infer either universal multi-column failure or solved conversion fidelity from this review; the converter was not inspected or tested.

### Foliate — GNOME ebook ergonomics

**Platforms/formats:** GNOME/Linux, GTK4/libadwaita/WebKitGTK; EPUB, Mobipocket/Kindle, FB2, CBZ and **PDF**. PDF support is explicitly present in the [AppStream description][foliate-meta]; describing Foliate as EPUB-only would be incorrect.

1. **D:** open the listed ebook/comic/PDF formats.
2. **D:** paginated and scrolled modes.
3. **D:** font and line-spacing customization.
4. **D:** light, sepia, dark and invert modes.
5. **D:** reading-progress slider with chapter marks.
6. **D:** bookmarks and annotations.
7. **D:** find in book.
8. **D:** quick dictionary lookup.
9. **D:** optional speech-dispatcher-based TTS. [README][foliate-readme].
10. **D:** OPDS catalogs, including OPDS 2.0 since the documented 3.1.0 release. Items 1–8 and 10: [AppStream][foliate-meta].

**P — comparison value:** reading-centered layout, typography and catalog integration on GNOME. **Limits:** per-format annotation/TTS behavior was not verified; bundled PDF.js presence does not confer every generic PDF.js viewer feature. The 2025 stable release and 2026 source activity are separate observations.

### Thorium Reader — accessible publishing and library access

**Platforms/formats:** the inspected repository is the **desktop** application for Windows, macOS and Linux. EDRLab documents EPUB 2/3 and fixed-layout EPUB, PDF, DAISY 2.02/3, Readium/W3C audiobooks and Divina; the current product website also lists CBZ and a separate iOS/iPadOS product. [EDRLab feature list][thorium-features], [product site][thorium-site]. Do not assign that mobile product to this desktop source pin.

1. **D:** the listed ebook, PDF, accessible-book and audio/visual publication formats.
2. **D:** typography, spacing, columns, brightness and color schemes.
3. **D:** keyboard navigation and screen-reader support claims for NVDA, JAWS, Narrator and VoiceOver.
4. **D:** OPDS 1/2 browsing and catalog authentication.
5. **D:** bookmarks, EPUB page lists and position lists.
6. **D:** persistent reading position.
7. **D:** full-text search within a publication.
8. **D:** media overlays.
9. **D:** Read Aloud.
10. **D:** shareable annotations.
11. **D:** accessibility metadata support.
12. **D:** LCP-protected publication access in the distributed product. The public-source build only supports the **Basic Encryption Profile** without the additional production-grade component. [README][thorium-readme]. Items 1–11: [EDRLab feature list][thorium-features] and [product site][thorium-site].

**P — comparison value:** accessible publishing formats and institution/library acquisition, beyond ordinary local-file reading. **Limits:** support descriptions span formats; PDF-specific TTS/annotation/AT parity is not established. Production LCP functionality is not fully reproducible from the BSD repository alone. The help service returned 403 and was not bypassed.

## 3. Four pinned implementation reviews and contribution candidates

**Review depth:** targeted source excerpts, not whole-project audits. The ranges below identify the sections actually used as evidence. Retrieval of a larger file does not mean all of it was semantically reviewed. Test names and files described as *located* or *scanned* were not executed. All acceptance checks are prospective.

### 3.1 PDF.js

**Pin:** `mozilla/pdf.js@57dead10694ead8fb21b97f7812fc95311a38ea1`.

| Reviewed source/range | C — observation and transferable seam |
|---|---|
| [src/display/api.js, selected lines 120–170 and 230–275][pdf-api] | Public loading options separate document access, worker selection, range transport and image/canvas capability choices. Useful boundary for portable rendering integration. |
| [web/pdf_find_controller.js, 635–677, 710–946, 1195–1235][pdf-find] | Query invalidation, normalization-to-original offsets, match counts, serial page-text extraction and close/search-state handling are separate concerns. `match()` is a documented override seam within the viewer component. |
| [web/pdf_find_bar.js, 99–152][pdf-findbar] | UI handles found/pending/not-found/wrapped and result counts. |
| [web/struct_tree_layer_builder.js, 25–118, 330–460, 540–674][pdf-struct] | Builds semantic/ARIA relationships, table header references and MathML; these relationships depend on browser accessibility behavior. |
| [web/text_layer_builder.css, 59–74][pdf-textcss] | `.markedContent` uses `display: contents` at this pin. |
| [src/display/editor/highlight.js, selected 509–623][pdf-highlight] | Highlight deserialization/serialization includes geometry and comments; copying a highlight returns null by design. |
| [src/display/annotation_storage.js, selected 29–54, 110–158, 174–180, 323–342][pdf-storage] | Modified-state hooks and a separately frozen print representation avoid exposing mutable live state during printing. |
| [web/viewer.html, selected 343–385, 588–668, 678–734][pdf-viewer] | Search live region and editor/print/save/presentation controls. |
| [test/integration/accessibility_spec.mjs, selected 23–99 and 121–139][pdf-a11y-test]; [test/unit/struct_tree_layer_builder_spec.js][pdf-struct-test] | The inspected integration assertions follow DOM `aria-owns` and text content. Unit test names cover role/name/table semantics. This is not proof of the browser's actual accessibility tree or of missing AT coverage throughout the repository. |

The [official layered architecture][pdf-start] is core parser/interpreter → display API → viewer. It offers reusable rendering/search/accessibility mechanisms rather than an Android application shell.

#### ALT-DW-001 — Extend verification of the existing marked-content accessibility fix

**P; high evaluation priority.** **T:** [issue #20790][pdf-20790] describes empty/unusable tagged structures in Chromium and differing AT behavior. **An open fix already exists: [PR #22558][pdf-22558]**, observed open on 2026-11-21. Its author reports a real Chromium accessibility-tree test, geometry/copy checks and NVDA testing; a later comment adds manual selection checks in Safari. Those are author-reported results, not this lane's tests. The original PR text leaves Safari/VoiceOver and older Chromium selection-workaround behavior untested; the later Safari selection check does not prove VoiceOver behavior.

**Seam:** CSS plus structure builder and browser integration tests. Contribute additional compatibility evidence or tests to the existing work, rather than filing a duplicate or proposing that the same CSS fix is new.

**Acceptance checks:** headings, table cells/headers and lists expose their text in the actual accessibility tree; VoiceOver/Safari and the older Chromium workaround receive explicitly versioned checks; selected/copied text and span geometry remain equivalent; NVDA browse-mode line grouping is assessed separately from restored heading navigation.

#### ALT-DW-002 — Expose incomplete search coverage after text-extraction errors

**P; medium.** **C:** find-controller lines 917–925 log a page extraction error and replace its searchable text with an empty string. The inspected find-bar switch has no incomplete-coverage state. This establishes a local information-loss seam, not a reproduced false “no matches” application result.

**Seam:** extraction result metadata → find-controller event → accessible find-bar status. Related [#21557][pdf-21557] is closed as a duplicate of #20973 and concerned a Safari extraction failure; it is not proof that the proposed partial-result UI already exists or is absent.

**Acceptance checks:** inject a failing middle page in a three-page fixture; retain matches on healthy pages; distinguish incomplete coverage from a completed zero-result search; announce the condition accessibly; clear/retry state correctly on document change. Do not rewrite parser error recovery to implement a UI distinction.

#### ALT-DW-003 — Benchmark a current-page-first, cancellable search-extraction strategy

**P; medium.** **C:** lines 880–930 construct a serial extraction chain starting at page zero, retain normalized page text, and guard against document replacement. Close-find handling prevents late UI navigation but does not by itself describe a resource cancellation strategy for the extraction chain.

**Seam:** text extraction scheduling and caching, with existing normalization/match semantics retained. Related slow-search issues exist; no performance defect was reproduced at this pin.

**Acceptance checks:** compare baseline and candidate on fixed long, scanned and mixed-text PDFs; record time to first match near the current page, final result count, peak memory and warm repeat-search latency; rapid query replacement/close must not produce stale navigation; preserve diacritic, punctuation and whole-word results. Promote only a measured improvement with acceptable caching trade-offs.

### 3.2 Okular

**Pin:** mirror `KDE/okular@110d017ab20368a449a21fcc2566f4ef7baaf3ae`; canonical contribution target is KDE Invent.

| Reviewed source/range | C — observation and transferable seam |
|---|---|
| [README.md][okular-readme] and [CMakeLists.txt][okular-cmake], selected build/dependency sections | Desktop shell, KParts plugin, Kirigami mobile application and format generators share `okularcore`. PDF uses Poppler Qt6. Optional dependencies gate speech, scripting and formats. |
| [core/generator.h, selected 184–206, 331–339, 534–575][okular-generator] | Explicit asynchronous rendering/text-extraction capability boundary. |
| [core/document.cpp, selected 1623–1662, 1717–1735, 1827–1835][okular-document] | Observer pixmap requests and document-level search dispatch. |
| [core/textpage.cpp, 549–553][okular-textpage] | Text search entry point rejects empty text/query/invalid areas; deeper normalization was not reviewed. |
| [generators/poppler/generator_pdf.cpp, 171–204][okular-dest] | Link destinations set page and normalized position; this function retains TODOs for other destination attributes/zoom. |
| [core/document.h, selected 464–470, 1398–1462][okular-viewport] | Viewport/observer state includes position and auto-fit flags; zoom also has an explicit document method. |
| [core/documentcommands.cpp, selected 56–178, 193–280][okular-commands] | Undoable annotation commands restore relevant view position and use stable annotation names during reload reference refresh. |
| [mobile/components/DocumentView.qml, 1–260][okular-mobile] | Custom pinch/pan/page transitions, page delegates, height-based zoom constraints and fixed 250 ms transitions. |
| [mobile/components/pageitem.h, 28–153][okular-pageitem] | QQuickItem view adapter with bookmark, viewport and paint boundaries. |

`autotests/searchtest.cpp`, annotation command tests and `mobile/components/testDocumentView.qml` were **located in tree listings**, not read in full or run. Do not infer absence of coverage from this subset.

#### ALT-DW-004 — Re-evaluate mobile fit-page zoom against the existing report

**P; high.** **T:** [Bug 463787][okular-463787] reports inability to zoom back to a whole-page view on a PinePhone, Okular 22.12/Qt 5.15. **C:** the reviewed mobile QML uses strict height constraints during pinch and clamps resized content to viewport dimensions. That is a relevant seam, not a current-build reproduction of the 2023 report.

**Acceptance checks:** portrait, landscape and mixed-aspect documents can return to a documented fit-page state after pinch; rotation/resizing preserves the intended reading anchor; page-swipe and pan gestures remain distinguishable; capture results on a versioned current Kirigami build before claiming the old report still reproduces.

#### ALT-DW-005 — Make mobile page-transition motion explicitly configurable

**P; medium.** **C:** lines 228–247 hardcode two 250 ms animations and explain the component cannot depend on Kirigami units. **T/correction:** desktop animated-scroll setting [Bug 420755][okular-420755] is **resolved fixed**; [421039][okular-421039] is its duplicate. This proposal targets the inspected mobile component, not a supposedly missing desktop setting.

**Acceptance checks:** expose a shell-supplied duration/reduced-motion policy without adding an unnecessary component dependency; reduced-motion operation changes pages immediately with the same final viewport; ordinary motion retains the existing interaction contract; keyboard, touch, canceled drags and document changes remain correct. Inspect existing shell preference wiring before adding a new setting.

#### ALT-DW-006 — Trace and extend link-destination fit/zoom policy

**P; medium.** **C:** `fillViewportFromLinkDestination()` handles page and position while leaving zoom/destination-kind TODOs. Other call paths or user settings could affect final behavior; no app-wide absence is claimed.

**Acceptance checks:** synthetic `/XYZ`, `/Fit`, `/FitH` and `/FitV` links demonstrate the chosen behavior; null destination coordinates preserve specified state; rotated pages land correctly; the user's preserve-zoom policy wins when enabled; back/forward restores position/zoom. Start with tracing caller/consumer behavior, then add focused generator/view tests.

### 3.3 Sioyek

**Pin:** `ahrm/sioyek@1e2f8037353724a83ccb10a697e28e295383e017` (`development`).

| Reviewed source/range | C — observation and transferable seam |
|---|---|
| [pdf_viewer_build_config.pro][sioyek-build-config], initial build/module sections; [.gitmodules, 1–8][sioyek-modules] | C++20/Qt application with OpenGL and a MuPDF submodule. The dependency submodule's exact code/license was not deeply reviewed here. |
| [pdf_viewer/pdf_renderer.cpp, 342–449][sioyek-search] and worker construction at 48–55 | Separate rendering/search workers; page range/case/regex selection, progress signaling and latest-request interruption. |
| [pdf_viewer/database.cpp, 502–534 and 833–889][sioyek-database] | Local/shared SQLite handles; highlight coordinate writes use escaped text plus streamed SQL numeric values. |
| [pdf_viewer/document.cpp, selected 158–184, 322–390][sioyek-document] | Annotations and portals are associated with document checksums; reload and insertion paths connect document state to storage. |
| [pdf_viewer/document_view.h, selected 29–33, 89–110][sioyek-view] | Navigation state and closest-portal/bookmark operations are separate from document content. |
| [README.md][sioyek-readme], development FAQ/build sections; [build_windows.bat, 1–34][sioyek-windows] | FAQ requires Qt 6.7/6.8 but Linux/Windows instructions still say Qt5; Windows recipe mentions VS2019 and the batch script mixes build and external file-tool commands. |

#### ALT-DW-007 — Reconcile development build documentation and toolchain preflight

**P; medium.** **C:** README's Qt guidance conflicts within the same pinned file. **T:** [#1371][sioyek-1371] records wrong MinGW-vs-MSVC Qt selection, maintainer-tested VS2022/Qt6.8 and subsequent build troubleshooting. This is a concrete documentation/toolchain seam; not every historic failure in that discussion is current.

**Acceptance checks:** separate stable/development prerequisites; identify matching Qt/MSVC architecture and shell/file-tool requirements; give a preflight that reports qmake/toolchain identity before compilation; validate a clean, documented Windows build and one Linux build with the declared dependency revisions. No build was attempted here.

#### ALT-DW-008 — Verify and simplify search-worker MuPDF resource ownership

**P; high investigation priority.** **C:** lines 394–396 load an `fz_page*` and then create structured text by page number. The local `page` is unused in the inspected loop, which drops the structured-text page at 426 but contains no corresponding `fz_drop_page`. Context lifetime also requires tracing outside this function. This is an **untested ownership suspicion**, not a measured memory leak or crash.

**Acceptance checks:** trace MuPDF ownership and worker shutdown; remove a redundant load or pair each retained reference with its correct release; repeated whole-document searches show bounded retained memory after cleanup; cancellation and malformed-page paths release resources; range/regex/empty-result behavior stays equivalent. Compare bundled MuPDF with any supported system-library configurations explicitly.

**T/correction:** [#1401][sioyek-1401] concerns Sioyek **2.0.0 with system MuPDF**. The maintainer raises packaging/version mismatch and the thread includes a report of success after rebuilding. It must not be repackaged as proof of this development-loop suspicion.

#### ALT-DW-009 — Use locale-independent typed SQLite writes for annotation geometry

**P; medium.** **C:** inspected highlight insertions stream floating-point values into SQL; strings use `esc()`. Consider typed prepared bindings to make geometry round-trips independent of formatting locale and to reduce ad hoc query assembly. This review does **not** establish SQL injection.

**T/correction:** [#1616][sioyek-1616] reports coordinate-based deletion failures in stable 2.0.0. The maintainer states development uses UUID deletion and the problem is fixed there. Do not file the old deletion report again against this pin.

**Acceptance checks:** save/reload/edit/delete highlights and portals under C, German and Brazilian-Portuguese numeric locales; include negative/fractional coordinates, apostrophes and non-ASCII notes; compare semantic stored values; migration and UUID deletion remain compatible. Confirm the application's actual C++ locale before asserting an existing insertion failure.

### 3.4 Zotero Reader

**Pin:** `zotero/reader@09af7187f0b219cec3e32f5fec56f77269a44b67`.

| Reviewed source/range | C — observation and transferable seam |
|---|---|
| [src/common/reader.js, 1–38, 100–132, 352–368][zotero-reader-code] | React UI coordinates PDF/EPUB/snapshot/semantic views, annotation manager, keyboard/focus managers and host callbacks. |
| [src/common/annotation-manager.js, 80–118, 243–453, 459–478, 598–722][zotero-annotations] | Typed annotation operations, filters, debounced host saves, merging and host-visible undo/redo are centralized. |
| [src/pdf/selection.js, 403–414][zotero-sortindex] | A sort index is a padded, pipe-separated **string**, not a number. |
| [src/pdf/pdf-search-controller.mjs, selected 1–37, 219–242, 307–355, 393–445][zotero-search] | Native/semantic search sessions use generation/revision checks, abort and fallback paths. |
| [src/common/view.js, 80–100][zotero-mobile-view] | Mobile view forces immediate first delivery of a new annotation so host callbacks can resolve its ID. |
| [src/index.android.js, selected 1–22, 59–93][zotero-android-entry]; [src/index.ios.js, selected 1–26, 53–54][zotero-ios-entry]; [src/index.view-dev.js, 1–140][zotero-dev-entry] | Distinct platform message transports wrap similar initialization/callback structures. The development adapter also renders page-region images for semantic reading. This is bridge-source inspection, not Android application/runtime work. |
| [test/common/annotation-manager.test.mjs][zotero-annotation-tests], test names at 38, 51, 66, 85, 99, 114; [test/pdf/search-session.test.mjs][zotero-search-tests], selected 1–19, 65–72 | Existing tests address immediate/debounced saves, undo identity behavior and session fallback. Their presence is retained when proposing additional cases; they were not run. |

`structured-document-text` was observed as a submodule at `7963c11faac4595be3bbe86b7574704a22c67bed` in the repository tree, **not reviewed internally**. A source dependency is not evidence of complete semantic-PDF correctness.

#### ALT-DW-010 — Correct ink-merge ordering for string metadata

**P; high.** **C:** annotation-manager lines 282–284 use numeric subtraction to select the smallest `sortIndex` and oldest `dateCreated`. `formatSortIndex()` produces strings such as `00001|000100|00010`; `addAnnotation()` produces ISO timestamps. Subtracting either form yields `NaN`.

**Narrow executed check:** at **2026-11-21T14:27:06.471Z**, the two exact comparator expressions were evaluated in a JavaScript runtime with the following synthetic input. Both comparator results were `NaN`, and both sorts selected the first (`later`) record rather than the earlier metadata. This check did **not** invoke `mergeAnnotations()`, build Zotero, or exercise its UI.

```js
const annotations = [
  { id: 'later', sortIndex: '00001|000200|00020', dateCreated: '2026-11-20T10:00:00.000Z' },
  { id: 'earlier', sortIndex: '00001|000100|00010', dateCreated: '2026-11-19T10:00:00.000Z' },
];
Number.isNaN(annotations[0].sortIndex - annotations[1].sortIndex); // true
Number.isNaN(annotations[0].dateCreated - annotations[1].dateCreated); // true
[...annotations].sort((a, b) => a.sortIndex - b.sortIndex)[0].id; // 'later'
[...annotations].sort((a, b) => a.dateCreated - b.dateCreated)[0].id; // 'later'
```

**Acceptance checks:** invoke the actual manager on same-page, same-color ink annotations in both selection orders; merged `sortIndex` and creation date must be the intended minima, independent of order; preserve tags, paths, width selection, undo and save callbacks; explicitly define treatment of invalid/legacy metadata. Compare strings or parse timestamps according to the existing schema rather than relying on numeric coercion.

**Duplicate-search boundary:** exact `sortIndex`/`dateCreated` issue searches returned insufficient result metadata, not a verified zero. A `merge ink` PR search returned three summaries, including open [#264](https://github.com/zotero/reader/pull/264); its full implementation was not examined. Originality is unresolved.

#### ALT-DW-011 — Consolidate shared mobile initialization with explicit transport adapters

**P; medium.** **T:** open [#234][zotero-234] specifically requests merging `index.{ios,android,view-dev}.js` because feature/callback behavior drifts. **C:** the inspected entries share the `View` surface while Android uses a message port and iOS uses WebKit message handlers.

**Acceptance checks:** a shared initialization contract drives all three adapters; transport-specific serialization remains explicit; callback names/payloads remain backward compatible; annotation-save-before-selection ordering and history metadata survive; a table-driven adapter test detects capabilities added on one platform but not considered on others. Coordinate against #234, not a new duplicate issue.

#### ALT-DW-012 — Define and test the annotation-save rejection contract

**P; high investigation priority.** **C:** lines 425–452 mark saving in progress, clear pending entries, call delete, await the host save callback, then clear the flag. There is no local rejection handler in that inspected method. Host adapters may intentionally own error handling, retries or fail-stop UI; those boundaries were not fully reviewed.

**T/correction:** closed [#52][zotero-52] documents a previous save-error UI change. Do not claim Zotero has never reported save failures. This proposal is a callback-contract and failure-injection exercise, not a reproduced annotation-loss report.

**Acceptance checks:** reject a save while subsequent edits/deletes arrive; the documented policy must either retain/retry the unsaved batch safely or expose an explicit blocked/error state with recoverable content; no silent successful-save indication; undo/remapped IDs must not resurrect deleted data; recovery and document close are covered at the host adapter as well as the manager.

#### ALT-DW-013 — Add controller-level native/semantic search transition checks

**P; medium.** **C:** the controller already contains generation guards and semantic-to-native fallback. Existing `search-session.test.mjs` covers a current-session-only fallback at the state-owner layer. Additional integration checks should exercise delayed page/mapping callbacks and visible results, rather than reimplement those existing guards.

**Acceptance checks:** query A's delayed semantic results cannot overwrite query B; a failure only falls back for the current query; destroyed/closed views publish no late navigation; result geometry/page labels remain coherent across Reading Mode and standard PDF view; native and semantic fixture text produce explicitly documented equivalence or differences. Real semantic-text producer and UI integration remain to be exercised.

## 4. Existing-issue search ledger and report drafts

Searches were public, unauthenticated, bounded GETs on **2026-11-21**. GitHub REST tree requests encountered a shared **403 rate limit** after initial metadata collection; subsequent raw files and public HTML payloads were used. Search-result counts are the server's reported counts, not proof that all relevant issues are indexed. No issue, PR or email was submitted.

| Project | Exact search boundary | Material result / limit |
|---|---|---|
| PDF.js | [is:issue "table" accessibility](https://github.com/mozilla/pdf.js/issues?q=is%3Aissue%20%22table%22%20accessibility): first 12 summaries of 22 reported results; #20790 body read. [is:pr 20790](https://github.com/mozilla/pdf.js/issues?q=is%3Apr%2020790): one result; #22558 body/comments read. | Existing open fix identified. Additional compatibility checks must account for the author's later Safari selection testing. |
| PDF.js | [is:issue "text extraction" error](https://github.com/mozilla/pdf.js/issues?q=is%3Aissue%20%22text%20extraction%22%20error): 12 summaries; #21557 body/comments read. | #21557 is closed duplicate of #20973. No claim that these searches settle the incomplete-search-status proposal. |
| PDF.js | [is:issue "search" "slow"](https://github.com/mozilla/pdf.js/issues?q=is%3Aissue%20%22search%22%20%22slow%22): first 15 summaries of 43 reported results over two pages. | Related #13962/#11208 appeared in searches; closed historical reports are not current performance measurements. No full issue/PR history audit. |
| Okular | Bugzilla REST `product=okular`, `summary=zoom`, `limit=30`; another with `component=PDF backend`, limit 30. `summary=destination`: 3 returned. `summary=mobile`: 5 returned. | Oldest/limited pages can omit newer or differently worded reports. #463787 body read. Destination behavior originality remains unresolved. |
| Okular | Bugzilla REST `summary=animation`, limit 30: 8 returned; `summary=accessibility`: 16 returned. #421039 and its duplicate target #420755 read. | Desktop disable-animation request is fixed. Mobile scope remains separately untested. Invent merge requests were not exhaustively searched. |
| Sioyek | [is:issue search memory](https://github.com/ahrm/sioyek/issues?q=is%3Aissue%20search%20memory): first 12 summaries of 22; #1401 body/comments read. | Stable/system-MuPDF packaging issue is distinct from the inspected development resource-ownership suspicion. |
| Sioyek | [is:issue sqlite](https://github.com/ahrm/sioyek/issues?q=is%3Aissue%20sqlite): 11 summaries; #1616 body and maintainer reply read. [is:issue Qt6 README](https://github.com/ahrm/sioyek/issues?q=is%3Aissue%20Qt6%20README): 5 summaries; #1371 discussion read. | Preserve maintainer's development UUID-deletion correction. No complete PR search. |
| Zotero Reader | [is:issue "annotation" save](https://github.com/zotero/reader/issues?q=is%3Aissue%20%22annotation%22%20save): 4 summaries, #52 body read. [is:issue "merge"](https://github.com/zotero/reader/issues?q=is%3Aissue%20%22merge%22): 2 summaries, #234 body read. [is:issue "search"](https://github.com/zotero/reader/issues?q=is%3Aissue%20%22search%22): 10 summaries. | Known save-error and bridge-maintenance work exists. Main Zotero issue tracker/forums were not exhaustively searched. |
| Zotero Reader | [is:issue "sortIndex"](https://github.com/zotero/reader/issues?q=is%3Aissue%20%22sortIndex%22) and [is:issue "dateCreated"](https://github.com/zotero/reader/issues?q=is%3Aissue%20%22dateCreated%22) yielded page metadata without a reliable result list. [is:pr merge ink](https://github.com/zotero/reader/issues?q=is%3Apr%20merge%20ink): 3 summaries. | **Not a confirmed negative search.** #264 open; #138/#128 merged. No guarantee of a new, unreported merge-order problem. |
| Other six dossiers | Official docs, metadata, license and release sources only. | No systematic issue/PR search or application-code audit for Sumatra, Papers, Evince, calibre, Foliate or Thorium. |

KDE REST search base: <https://bugs.kde.org/rest/bug?product=okular&summary=mobile&include_fields=id,summary,status,resolution,component&limit=30>. Substitute the recorded summary/component to reproduce the bounded queries; do not infer absence from the limit.

### Four draft contribution/report briefs — not submitted

1. **PDF.js / follow-up to #20790 and PR #22558.** “Extend AT/selection compatibility evidence for tagged marked content.” Cite the exact master pin, existing PR, CSS and actual-AX-vs-DOM distinction. Proposed steps: run tagged heading/list/table fixtures before/after the existing branch with versioned browser/AT pairs; record geometry/copy output separately from semantic navigation. **Current result:** upstream-reported defect and open patch; no local browser/AT reproduction. Offer missing matrix evidence instead of another implementation of the same patch.
2. **Okular / re-evaluation of Bug 463787.** “Current Kirigami fit-page zoom behavior on mixed-aspect pages.” Cite the 2023 report and current QML pin; propose pinch-in/out and orientation changes on a versioned mobile build. Expected outcome: recover a documented whole-page fit without unwanted page changes. **Current result:** relevant constraints read; current application reproduction pending. Do not state the old report is still reproducible.
3. **Sioyek / search resource ownership review.** “Verify page/context ownership in development search worker.” Cite `pdf_renderer.cpp:342–449`, unused page load and structured-text cleanup; propose repeated-search/exception/cancellation memory checks. **Current result:** static ownership suspicion; no measured leak. Explicitly distinguish stable/system-MuPDF #1401 and its packaging discussion.
4. **Zotero Reader / ink merge metadata ordering.** “Selection-order-independent oldest date and earliest sort index for ink merge.” Cite annotation-manager 282–284 and selection 408–414; attach the tiny synthetic comparator input above. Expected metadata are the minima in either input order. **Current result:** exact comparator expressions evaluated, full manager/UI reproduction pending; duplicate status unresolved. Next step is a focused actual-manager regression before describing it as a reproduced Zotero defect.

## 5. Transferable workflows and remaining coverage

**P — evaluation priorities, not measured winners:**

| Need | First comparators to evaluate | Transferable pattern / boundary |
|---|---|---|
| Embedded browser PDF and semantic accessibility | PDF.js | Separate parser/render API, text/search layer, editable annotations and semantic tree; verify actual AT output rather than counting ARIA attributes. |
| Native PDF review and signatures | Okular; Papers; Sumatra | Distinguish visual signatures from cryptographic signatures, document edits from reading-state changes, and stable releases from development features. |
| Dense academic reading | Sioyek; Zotero | Reference previews/portals, return-to-context navigation, citations and annotation-to-note backlinks; phone ergonomics need independent design/testing. |
| Ebook typography and personal library | calibre; Foliate | Chapter-scoped search, precise reference locations, library-wide annotations, OPDS and CSS/typography controls. These extend a reading workflow that Moon+ already partly documents. |
| Accessible publishing and institutional acquisition | Thorium | DAISY/media overlays/accessibility metadata and authenticated OPDS; verify per-format behavior and public-source LCP limits. |
| Legacy formats and TeX/printing | Evince; Okular | Backend capability matrices, SyncTeX and print workflows; not direct substitutes for phone-specific controls. |

**Extension contract:** add a candidate when it has an identifiable canonical public repository and a relevant reading workflow. Record platform/build/release, license evidence, retrieval date, 6–12 sourced capabilities and review depth. Promote from metadata-only to targeted-code only after reading pinned implementation paths. Add an improvement candidate only with a concrete seam, bounded duplicate search, prospective acceptance checks and honest status. Keep separate products and forks separate; do not equate library dependencies with exposed application features.

**Remaining limits:**

- No Android/iOS, desktop reader, AT, performance, battery, synchronization, PDF-conformance or export/import round-trip tests were run. The small comparator check is not an application test.
- Four targeted implementation reviews satisfy the deep-comparison boundary; the other six entries have documentation/metadata/license depth. Sumatra is **not** counted as a fifth deep review.
- Most reviewed heads are development snapshots, not released binaries. No source-to-binary reproducibility or store-package audit was performed.
- Repository/mirror push dates and release feeds can differ from publication dates and stable maintenance versions; those differences are retained above.
- Browser compatibility, proprietary/optional production LCP components, package backends and external TTS engines affect feature availability.
- Initial API rate limiting, incomplete search payloads and Thorium help 403 remain coverage limits. Raw-source 404s for initially guessed README/license paths were corrected using directory evidence, not interpreted as missing licenses or projects.
- Exact issue novelty is not established. Existing open work and resolved historical reports are identified to prevent duplicate contributions.
- Upstream capability descriptions do not prove universal accessibility or safe interoperability. No blanket “all alternatives” or “Moon+ lacks this” conclusion is supported.

## Sources

All URLs below were read on **2026-11-21**. Source-code links use the examined commit; unpinned official pages/releases are dated observations. Detailed line boundaries are listed above and in the inventory.

[pdf-license]: https://github.com/mozilla/pdf.js/blob/57dead10694ead8fb21b97f7812fc95311a38ea1/LICENSE
[pdf-readme]: https://github.com/mozilla/pdf.js/blob/57dead10694ead8fb21b97f7812fc95311a38ea1/README.md
[pdf-start]: https://mozilla.github.io/pdf.js/getting_started/
[pdf-release]: https://github.com/mozilla/pdf.js/releases/tag/v6.5.438
[pdf-api]: https://github.com/mozilla/pdf.js/blob/57dead10694ead8fb21b97f7812fc95311a38ea1/src/display/api.js#L120-L275
[pdf-find]: https://github.com/mozilla/pdf.js/blob/57dead10694ead8fb21b97f7812fc95311a38ea1/web/pdf_find_controller.js#L635-L946
[pdf-findbar]: https://github.com/mozilla/pdf.js/blob/57dead10694ead8fb21b97f7812fc95311a38ea1/web/pdf_find_bar.js#L99-L152
[pdf-struct]: https://github.com/mozilla/pdf.js/blob/57dead10694ead8fb21b97f7812fc95311a38ea1/web/struct_tree_layer_builder.js#L330-L674
[pdf-textcss]: https://github.com/mozilla/pdf.js/blob/57dead10694ead8fb21b97f7812fc95311a38ea1/web/text_layer_builder.css#L59-L74
[pdf-highlight]: https://github.com/mozilla/pdf.js/blob/57dead10694ead8fb21b97f7812fc95311a38ea1/src/display/editor/highlight.js#L509-L623
[pdf-storage]: https://github.com/mozilla/pdf.js/blob/57dead10694ead8fb21b97f7812fc95311a38ea1/src/display/annotation_storage.js#L323-L342
[pdf-viewer]: https://github.com/mozilla/pdf.js/blob/57dead10694ead8fb21b97f7812fc95311a38ea1/web/viewer.html#L343-L734
[pdf-a11y-test]: https://github.com/mozilla/pdf.js/blob/57dead10694ead8fb21b97f7812fc95311a38ea1/test/integration/accessibility_spec.mjs#L23-L139
[pdf-struct-test]: https://github.com/mozilla/pdf.js/blob/57dead10694ead8fb21b97f7812fc95311a38ea1/test/unit/struct_tree_layer_builder_spec.js
[pdf-20790]: https://github.com/mozilla/pdf.js/issues/20790
[pdf-22558]: https://github.com/mozilla/pdf.js/pull/22558
[pdf-21557]: https://github.com/mozilla/pdf.js/issues/21557
[okular-site]: https://okular.kde.org/
[okular-download]: https://okular.kde.org/download/
[okular-readme]: https://github.com/KDE/okular/blob/110d017ab20368a449a21fcc2566f4ef7baaf3ae/README.md
[okular-cmake]: https://github.com/KDE/okular/blob/110d017ab20368a449a21fcc2566f4ef7baaf3ae/CMakeLists.txt
[okular-release]: https://kde.org/announcements/gear/26.08.3/
[okular-tarballs]: https://download.kde.org/stable/release-service/26.08.3/src/
[okular-generator]: https://github.com/KDE/okular/blob/110d017ab20368a449a21fcc2566f4ef7baaf3ae/core/generator.h#L184-L206
[okular-document]: https://github.com/KDE/okular/blob/110d017ab20368a449a21fcc2566f4ef7baaf3ae/core/document.cpp#L1623-L1835
[okular-textpage]: https://github.com/KDE/okular/blob/110d017ab20368a449a21fcc2566f4ef7baaf3ae/core/textpage.cpp#L549-L553
[okular-dest]: https://github.com/KDE/okular/blob/110d017ab20368a449a21fcc2566f4ef7baaf3ae/generators/poppler/generator_pdf.cpp#L171-L204
[okular-viewport]: https://github.com/KDE/okular/blob/110d017ab20368a449a21fcc2566f4ef7baaf3ae/core/document.h#L1398-L1462
[okular-commands]: https://github.com/KDE/okular/blob/110d017ab20368a449a21fcc2566f4ef7baaf3ae/core/documentcommands.cpp#L56-L280
[okular-mobile]: https://github.com/KDE/okular/blob/110d017ab20368a449a21fcc2566f4ef7baaf3ae/mobile/components/DocumentView.qml#L1-L260
[okular-pageitem]: https://github.com/KDE/okular/blob/110d017ab20368a449a21fcc2566f4ef7baaf3ae/mobile/components/pageitem.h#L28-L153
[okular-463787]: https://bugs.kde.org/show_bug.cgi?id=463787
[okular-421039]: https://bugs.kde.org/rest/bug/421039
[okular-420755]: https://bugs.kde.org/rest/bug/420755
[sioyek-license]: https://github.com/ahrm/sioyek/blob/1e2f8037353724a83ccb10a697e28e295383e017/LICENSE
[sioyek-readme]: https://github.com/ahrm/sioyek/blob/1e2f8037353724a83ccb10a697e28e295383e017/README.md
[sioyek-release]: https://github.com/ahrm/sioyek/releases/tag/v2.0.0
[sioyek-feed]: https://github.com/ahrm/sioyek/releases.atom
[sioyek-build-config]: https://github.com/ahrm/sioyek/blob/1e2f8037353724a83ccb10a697e28e295383e017/pdf_viewer_build_config.pro
[sioyek-modules]: https://github.com/ahrm/sioyek/blob/1e2f8037353724a83ccb10a697e28e295383e017/.gitmodules#L1-L8
[sioyek-search]: https://github.com/ahrm/sioyek/blob/1e2f8037353724a83ccb10a697e28e295383e017/pdf_viewer/pdf_renderer.cpp#L342-L449
[sioyek-database]: https://github.com/ahrm/sioyek/blob/1e2f8037353724a83ccb10a697e28e295383e017/pdf_viewer/database.cpp#L833-L889
[sioyek-document]: https://github.com/ahrm/sioyek/blob/1e2f8037353724a83ccb10a697e28e295383e017/pdf_viewer/document.cpp#L158-L390
[sioyek-view]: https://github.com/ahrm/sioyek/blob/1e2f8037353724a83ccb10a697e28e295383e017/pdf_viewer/document_view.h#L29-L110
[sioyek-windows]: https://github.com/ahrm/sioyek/blob/1e2f8037353724a83ccb10a697e28e295383e017/build_windows.bat#L1-L34
[sioyek-1371]: https://github.com/ahrm/sioyek/issues/1371
[sioyek-1401]: https://github.com/ahrm/sioyek/issues/1401
[sioyek-1616]: https://github.com/ahrm/sioyek/issues/1616
[zotero-license]: https://github.com/zotero/reader/blob/09af7187f0b219cec3e32f5fec56f77269a44b67/COPYING#L1-L11
[zotero-readme]: https://github.com/zotero/reader/blob/09af7187f0b219cec3e32f5fec56f77269a44b67/README.md
[zotero-platforms]: https://www.zotero.org/support/system_requirements
[zotero-guide]: https://www.zotero.org/support/pdf_reader
[zotero-changelog]: https://www.zotero.org/support/changelog
[zotero-reader-code]: https://github.com/zotero/reader/blob/09af7187f0b219cec3e32f5fec56f77269a44b67/src/common/reader.js#L1-L38
[zotero-annotations]: https://github.com/zotero/reader/blob/09af7187f0b219cec3e32f5fec56f77269a44b67/src/common/annotation-manager.js#L243-L478
[zotero-sortindex]: https://github.com/zotero/reader/blob/09af7187f0b219cec3e32f5fec56f77269a44b67/src/pdf/selection.js#L403-L414
[zotero-search]: https://github.com/zotero/reader/blob/09af7187f0b219cec3e32f5fec56f77269a44b67/src/pdf/pdf-search-controller.mjs#L219-L445
[zotero-mobile-view]: https://github.com/zotero/reader/blob/09af7187f0b219cec3e32f5fec56f77269a44b67/src/common/view.js#L80-L100
[zotero-android-entry]: https://github.com/zotero/reader/blob/09af7187f0b219cec3e32f5fec56f77269a44b67/src/index.android.js#L1-L93
[zotero-ios-entry]: https://github.com/zotero/reader/blob/09af7187f0b219cec3e32f5fec56f77269a44b67/src/index.ios.js#L1-L54
[zotero-dev-entry]: https://github.com/zotero/reader/blob/09af7187f0b219cec3e32f5fec56f77269a44b67/src/index.view-dev.js#L1-L140
[zotero-annotation-tests]: https://github.com/zotero/reader/blob/09af7187f0b219cec3e32f5fec56f77269a44b67/test/common/annotation-manager.test.mjs
[zotero-search-tests]: https://github.com/zotero/reader/blob/09af7187f0b219cec3e32f5fec56f77269a44b67/test/pdf/search-session.test.mjs#L1-L77
[zotero-234]: https://github.com/zotero/reader/issues/234
[zotero-52]: https://github.com/zotero/reader/issues/52
[sumatra-authors]: https://github.com/sumatrapdfreader/sumatrapdf/blob/e6519ebc6b239330d9d0c4d9778e0e68762d3e78/AUTHORS#L23-L26
[sumatra-readme]: https://github.com/sumatrapdfreader/sumatrapdf/blob/e6519ebc6b239330d9d0c4d9778e0e68762d3e78/readme.md
[sumatra-release]: https://github.com/sumatrapdfreader/sumatrapdf/releases/tag/3.6.1rel
[sumatra-feed]: https://github.com/sumatrapdfreader/sumatrapdf/releases.atom
[sumatra-formats]: https://www.sumatrapdfreader.org/docs/Supported-document-formats.md
[sumatra-portable]: https://www.sumatrapdfreader.org/docs/SumatraPDF-portable.md
[sumatra-annotations]: https://www.sumatrapdfreader.org/docs/Editing-annotations.md
[sumatra-find]: https://www.sumatrapdfreader.org/docs/Finding-text.md
[sumatra-palette]: https://www.sumatrapdfreader.org/docs/Command-Palette.md
[papers-app]: https://apps.gnome.org/Papers/
[papers-meta]: https://github.com/GNOME/papers/blob/fe4bc08d1a5427a33abc9bead467150e3531c4c8/data/org.gnome.Papers.metainfo.xml.in.in#L100-L208
[papers-releases]: https://download.gnome.org/sources/papers/51/
[evince-readme]: https://github.com/GNOME/evince/blob/e822030005f22231052667d51398a84327004924/README.md
[evince-meta]: https://github.com/GNOME/evince/blob/e822030005f22231052667d51398a84327004924/data/org.gnome.Evince.metainfo.xml.in.in
[evince-releases]: https://download.gnome.org/sources/evince/48/
[evince-news]: https://download.gnome.org/sources/evince/48/evince-48.5.news
[evince-help]: https://help.gnome.org/users/evince/stable/
[evince-navigation]: https://help.gnome.org/evince/movingaround.html
[calibre-readme]: https://github.com/kovidgoyal/calibre/blob/d69ad111794cf2032264d2b02b3f9b9adfb139a2/README.md
[calibre-license]: https://github.com/kovidgoyal/calibre/blob/d69ad111794cf2032264d2b02b3f9b9adfb139a2/LICENSE
[calibre-copyright]: https://github.com/kovidgoyal/calibre/blob/d69ad111794cf2032264d2b02b3f9b9adfb139a2/COPYRIGHT
[calibre-news]: https://calibre-ebook.com/whats-new
[calibre-formats]: https://manual.calibre-ebook.com/faq.html#what-formats-does-calibre-support-conversion-to-from
[calibre-viewer]: https://manual.calibre-ebook.com/viewer.html
[calibre-conversion]: https://manual.calibre-ebook.com/conversion.html#convert-pdf-documents
[foliate-readme]: https://github.com/johnfactotum/foliate/blob/67b6676d3f936c5edea91d4d903385ef39dd25c0/README.md
[foliate-meta]: https://github.com/johnfactotum/foliate/blob/67b6676d3f936c5edea91d4d903385ef39dd25c0/data/com.github.johnfactotum.Foliate.metainfo.xml.in
[foliate-release]: https://github.com/johnfactotum/foliate/releases/tag/3.3.0
[thorium-readme]: https://github.com/edrlab/thorium-reader/blob/f603ca2848eb567b1d32cdfd6728362d73f8f557/README.md
[thorium-license]: https://github.com/edrlab/thorium-reader/blob/f603ca2848eb567b1d32cdfd6728362d73f8f557/LICENSE
[thorium-release]: https://github.com/edrlab/thorium-reader/releases/tag/v3.5.1
[thorium-features]: https://www.edrlab.org/software/thorium-reader/
[thorium-site]: https://www.thoriumreader.com/en/

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
