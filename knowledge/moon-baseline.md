---
type: Research
title: Moon+ Reader Pro official baseline and Android comparators
description: Dated publisher evidence for existing Moon capabilities, release notes, product identities, and comparator limitations.
tags: [moon-reader, android, readers, official-sources, evidence]
timestamp: 2026-11-21T13:56:54Z
---

# Moon+ Reader Pro: official-source baseline

**Observation date: 2026-11-21.** This note records publisher documentation, not application test results. Its 21 baseline entries include a documented DRM limitation. The [structured Moon records](../data/moon-baseline.json) preserve `MF-01` through `MF-21`; the [commercial inventory](../data/commercial-alternatives.json) supplies reusable comparator records. Contact details and submission drafts live in [Reporting](reporting.md).

Use the [evidence contract](design.md#evidence-contract) and [methodology](methodology.md) when interpreting these claims. Public package names and release notes do not authenticate an APK. The [examined artifact record](../data/artifact.json) has separate provenance limitations; its observations must not be silently attributed to an official Play release.

## Product identity and distribution

| Item | Official evidence | Qualification |
|---|---|---|
| Paid Android product | **Moon+ Reader Pro**, Play publisher **Moon+**, package `com.flyersoft.moonreaderp`; the official download page links the same package. [M02] [M04] | Listing identity, not binary authentication. |
| Free Android product | **Moon+ Reader**, package `com.flyersoft.moonreader`. [M04] | Keep free and Pro behavior/policies distinct. |
| Website | The Pro listing links `moondownload.com`. [M01] [M02] | Website and listing cross-identify the product. |
| Purchase model | Download page states one payment and lifetime free upgrades; Pro is advertised as ad-free. [M04] [M02] | Published promise, not a support-response or feature-delivery SLA. |
| PDF engine attribution | Download page credits **PDFViewer SDK from Radaee Studio** for PDF rendering/management. [M04] | Exact SDK version and linkage in an APK were not established here. |
| Regional distribution | Site describes special downloads for Russian and Belarusian paid users unable to obtain Pro through Play, with observed notice expiry **2027-10-10**. [M01] [M04] | Not a claim that all Pro builds expire or match Play packages byte-for-byte. No package was downloaded for this review. |

## Observed v10.8 release notes

The Pro Play listing retrieved on **2026-11-21** displayed **Updated on Oct 16, 2026** and these five **v10.8** changes. [M02]

1. **“Double-Tap To Zoom”** option for PDF, DjVu, and comic books.
2. **“Show my rating on book cover”** option.
3. Improved CSS rendering for embedded font styles.
4. Mini status bar text customization using only color or font.
5. Bookmarks-tab management can associate a missing book file with a new file.

These are observed listing notes and a listing update date, not a first-release timestamp, version code, complete rollout history, or certification of every package labeled 10.8. Missing-file relinking and double-tap zoom are already advertised capabilities. [M02]

No complete official version-history archive was recovered in this bounded review. The press collection contains older third-party coverage and its retrieved output was truncated; it does not establish a complete v10.8 history. [M08]

## Existing capability baseline

**Evidence type: `documented` for every row.** Website and FAQ pages are not separately versioned to v10.8. Each citation resolves to the exact primary URL and retrieval date below. None of these rows is an application-test pass.

| ID | Documented capability or limitation | Evidence and boundary |
|---|---|---|
| MF-01 | Broad ebook/document formats | Play lists EPUB, PDF, DjVu, AZW3, MOBI, FB2, PRC, CHM, CBZ, CBR, UMD, DOCX, ODT, RTF, TXT, HTML, MHT/MHTML, Markdown, WEBP, RAR, ZIP, and OPDS. OPDS is catalog access; the list does not establish identical speech/selection/annotation behavior across formats. [M02] |
| MF-02 | Pro text-to-speech | Shake-to-speak and TTS engine support are advertised. Engine availability and document text extraction are separate dependencies; scan OCR is not established. [M02] [M03] |
| MF-03 | Background speech | FAQ addresses TTS stopping with the screen off and battery restrictions for **both** reader and TTS engine. This is an existing workflow, with app/engine/OS diagnosis needed for interruptions. [M03] |
| MF-04 | Gestures, hardware keys, hands-free controls | Headset/Bluetooth, tilt actions, customizable taps/swipes/keys, five auto-scroll modes, brightness gesture, and page animations are documented. Exact audio-focus/accessibility interactions were not tested. [M01] [M02] |
| MF-05 | PDF forms, annotations, handwriting | Pro list includes form filling, highlighting, annotations, and handwriting. Individual form types and cross-viewer persistence require fixture tests. [M02] |
| MF-06 | PDF reading controls | Speech, auto-scroll, smart scroll lock, night mode, six additional PDF themes, landscape dual-page mode, statistics, sync, and flip animation are advertised. Official documentation does not settle PDF text reflow; see the separate [artifact evidence](#related-artifact-evidence). [M02] |
| MF-07 | Ebook annotations, lookup, and sharing | Highlights, notes/bookmarks, offline/online dictionary integration, translation, and sharing are documented. Integration does not establish a complete bundled offline dictionary. [M01] [M02] |
| MF-08 | Themes and typography | Ten-plus themes, day/night switching, line spacing, font scaling/styles, colors, justification, hyphenation, and paragraph/whitespace controls. Eye-care wording is a publisher claim, not a measured health outcome. [M01] [M02] |
| MF-09 | Custom fonts/backgrounds | FAQ names `.ttf`, `.otf`, `.ttc` and **Visual Options → Font Name/Background Images**. Its folder guidance uses older Android conventions; current storage/picker behavior is untested. [M03] |
| MF-10 | Publisher-formatting preview | For tables, FAQ recommends **“Preview mode with publisher formattings”** in Misc Options. Record the active mode before reporting a table problem; a fallback already exists in documentation. [M03] |
| MF-11 | EPUB3 media and footnotes | Audio/video and popup footnotes are advertised. This is not a complete EPUB3-conformance or media-overlay guarantee. [M02] |
| MF-12 | Reading-state/annotation sync | Dropbox/WebDAV position sync and backup; FAQ says highlights/notes/bookmarks continue syncing after position. Conflict resolution, retries, and completion visibility remain unverified. [M01] [M02] [M03] |
| MF-13 | Google Drive and cloud shelf/files | Pro policy explicitly includes Drive, Dropbox, and WebDAV and describes reading-state, annotation, and shelf-file sync. Drive's omission from shorter lists is not evidence of absence; authorization success was not tested. [M05] |
| MF-14 | Backup, restore, annotation export | FAQ documents **Options → Backup** for all books/settings and **Bookmarks dialog → Export → Export to file** for the current book; Free-to-Pro migration uses Backup/Restore. Completeness, merging, and cross-reader portability need separate checks. [M03] |
| MF-15 | Library/file management | Shelves, favorites, downloads, authors/tags, custom covers, import/search, file management, widgets, and book shortcuts. Automatic deduplication or content-based identity is not established. [M01] [M02] |
| MF-16 | Cover-cache repair | FAQ provides **My Shelf → Rebuild book covers** and discusses cleaning tools removing caches. Current cache/repair behavior was not tested. [M03] |
| MF-17 | OPDS/calibre | Play advertises online libraries/personal calibre servers; FAQ explains **Online Library → Add new catalog...**. Authentication, pagination, and protocol variants are separate test questions. [M02] [M03] |
| MF-18 | Statistics and focus aids | Per-book reading time/speed, six-style ruler, and blue-light filter up to 95% are advertised. These describe options, not measured health, cognitive, or performance benefits. [M01] [M02] |
| MF-19 | Orientation, dual-page layout, startup lock | Four orientations, landscape dual-page reading, and startup password/fingerprint protection. Two pages of one book do not establish two-document reading; app locking does not establish file/cloud encryption. [M02] |
| MF-20 | Localization | English homepage/download page say 46 languages; older Chinese page says 40. Preserve page-specific statements rather than claiming a build-specific translation-quality audit. [M01] [M04] [M07] |
| MF-21 | DRM compatibility limitation | FAQ explicitly says DRM-protected books are unsupported. Such a file failing to open is not by itself a malfunction of a documented supported format. No DRM-removal procedure was used here. [M03] |

### Sync sequencing matters

FAQ describes uploading position on **Pause**, checking for a newer remote position on **Resume**, then continuing highlights/notes/bookmarks sync in the background. A position arriving does not establish annotation sync completion. [M03]

Pro policy describes state/annotation caches under the user's cloud path `/Apps/Books/.Moon+` and shelf files under `/Apps/Books`. These are documented cloud locations, not an inspected account or an encryption guarantee. [M05]

FAQ includes broad reinstall/cloud-cache-reset advice and separate backup/export instructions. Preserving evidence and backups before a reset is this project's reporting recommendation, not a claimed publisher-mandated diagnostic sequence. [M03]

## Nonfunctional claims and unknowns

| Topic | Official evidence | Not established by this review |
|---|---|---|
| Performance | Smooth scrolling and faster/smoother Pro behavior. [M01] [M02] | Measured latency, memory, battery, or large-library advantage. |
| Storage access | Play explains All Files Access for file management, downloads, and PDF annotation saving; policy distinguishes older storage permission from `MANAGE_EXTERNAL_STORAGE` on Android 11+. [M02] [M05] | Actual grants/accesses, permission-denied behavior, or availability of folder-scoped access. |
| Cloud data | Policy describes local tokens/file information and user-selected clouds. [M05] | Actual retention, encryption, backup exclusions, traffic, or SDK behavior. |
| Accessibility | TTS, scaling, themes, ruler, and input controls. [M02] | Comprehensive TalkBack semantics, focus order, keyboard coverage, or formal conformance. |
| Native PDF reflow | **Unknown in this official-documentation review.** Reviewed Play/FAQ pages do not explicitly settle its interface or combinations. [M02] [M03] | Official-build runtime behavior and mode combinations remain unverified. Separate supplied-artifact evidence establishes a text-reflow code path; a documentation search miss is not absence. |

### Related artifact evidence

The separate [focused APK analysis](apk-analysis.md#implementation-map), observed on **2026-11-21**, records **APK-PDF-001**: `PDFReader.getPageText(int)` and `ActivityTxt.pdfCreateReflowText(long)` establish text extraction/reflow code in the supplied artifact. It also records **APK-SEARCH-002**: `misc.FuncSearch.getSearchResults(...)` searches settings/dialog titles, and **APK-NOTE-003**: `Readwise.addHighlights(...)` implements a token-authenticated highlight-upload path. The primary [static observation ledger](../evidence/static/observations.json) retains those findings and their evidence receipts; successful Readwise delivery was not observed in that analysis.

These are **`static-observation`** findings for SHA-256 `e2c0ef649413b2f6671598ac8b027d582ba220e38738f2e253694289ea20e1fc`, whose [artifact record](../data/artifact.json) retains unverified official provenance and the signature-verification failure. They establish existing code paths in those bytes, not an authenticated official-build runtime result. The official-source gap above remains a documentation limit; requests should investigate a specific reflow, settings-search, or Readwise-upload refinement rather than assume the capability is absent. This note links the original analysis without reproducing proprietary implementation.

### Policy wording inquiry

**MD-01 — documented wording discrepancy, not a verified telemetry defect.** Pro Play declares no data collected/shared. Later Pro-policy disclosure sections likewise deny collection/sharing, while earlier **Information Collection and Use** and **Log Data** sections describe third-party collection and error information that may include IP address, device/OS details, configuration, and usage time. Clarification is warranted about which clauses and optional flows apply to Pro. These statements do not establish undisclosed transmission, malicious behavior, or a legal violation. [M02] [M05]

Homepage's combined policy lists Google Play Services and AdMob; Pro Play links a Pro-specific policy whose third-party list names Google Play Services without AdMob. The combined policy is not evidence that Pro contains AdMob. [M01] [M02] [M05] [M06]

The [privacy clarification draft](reporting.md#privacy-policy-clarification-draft) asks about this wording using the policy's published contact.

## Resolving the name Reader Pro

**Identity remains unresolved.** Obtain a store URL, package name, About screenshot, or exact repository before choosing a product or tracker. These are distinct plausible candidates.

| Candidate | Official identity | Source status and qualification |
|---|---|---|
| Moon+ Reader Pro | `com.flyersoft.moonreaderp`, publisher Moon+. [M02] [M04] | Could mean the target itself. Full current source not established in reviewed official material. |
| ReadEra Premium | `org.readera.premium`; free `org.readera`; READERA LLC. [R01] [R03] [R04] | Proprietary app plus separate GPL OpenReadEra renderers; renderer source is offered by email, not full-app source. [R05] |
| PDF Reader Pro by PDF Technologies | Official Android page links `com.pdftechnologies.pdfreaderpro`. [P01] [P03] | Distinct PDF editor with Android viewing, annotation, editing, conversion, and forms. Full current app source unavailable here; SDK links do not establish its publication. [P02] |
| Readest | Site links `com.bilingify.readest` and `readest/readest`. [D01] | Public repository, AGPL-3.0-or-later statement. No evidence selects it as the intended ambiguous name. [D02] [D03] |
| Librera PRO | `com.foobnix.pro.pdf.reader`; Play explicitly lists **PDF Reader PRO** and Lirbi Reader as former names. [L01] | Public `foobnix/LibreraReader`, GPL-3.0-or-later text. Particularly plausible historical-name match, still unresolved. [L02] [L03] |

### Pinned repository evidence

| Repository | Exact commit and commit time | Files actually inspected |
|---|---|---|
| `readest/readest` | `0882c8074215edc24e2ee5ac25e99cdccddb7e34`, 2026-11-21T13:36:52Z | README features/planned features/license statement and LICENSE; retrieved 2026-11-21T14:06:42Z. No executable implementation review. [D02] [D03] |
| `foobnix/LibreraReader` | `b7378bbde373bbf8b80842f3e47ea444fa9fd542`, 2026-11-21T09:38:02Z | README package/release/license tables and LICENSE.txt; retrieved 2026-11-21T14:06:42Z. No executable implementation review. [L02] [L03] |

Readest's README advertises parallel two-document reading, library-shelf search, TTS, sync, keyboard/screen-reader support, and focus aids. **Handwriting annotations are planned**, not established as shipping by that evidence. [D02]

Librera's README contains both a development/support-freeze notice and a release table including **9.5.7 dated 2026-09-02**. These facts and the newer commit do not justify an unqualified abandonment claim. Play advertises PDF reflow, annotations, TTS, themes, and sync. [L01] [L02]

## Commercial and legacy Android comparators

This bounded seven-product inventory is a technical reference, not a ranking. **Source unavailable** means full current Android app source was not established from reviewed official material; dependencies may have different licenses. No comparator was installed, executed, or decompiled for this documentation review. The [structured inventory](../data/commercial-alternatives.json) records the same seven product families; free and paid editions are kept together with their entitlement differences.

| Product / package | Documented comparison points | Payment and source boundary |
|---|---|---|
| **Adobe Acrobat Reader** — `com.adobe.reader` | Reading, highlights/comments, forms/signing, cloud access, Liquid Mode, read-aloud. [A01] [A02] [A03] | Basic reading/comments/forms/signing described as free; Premium includes editing, conversion, OCR, page operations, higher-quality voices. Full current Android source unavailable. Desktop/mobile capabilities are not interchangeable. [A01] |
| **Xodo** — `com.xodo.pdf.reader` | Annotations, forms/signing, scanning/OCR, conversion, page tools, cloud access; official help documents Reading Mode/Reflow. [X01] [X02] [X03] | Exact Android entitlements unverified per tool. Full current Android source unavailable. Website terms distinguish mobile-app terms. [X04] |
| **Foxit PDF Editor** — `com.foxit.mobile.pdf.lite` | Reflow, read-aloud, annotations, forms, clouds, tablet-only document tabs; manual **2026.4.0** documents copying and annotating text inside reflow. [F01] [F02] | Advanced OCR, editing/conversion, redaction, certificate signing and other marked tools require subscription. Proprietary product licensing; full current Android source not obtained. [F02] [F03] |
| **ReadEra / Premium** — `org.readera` / `org.readera.premium` | Broad-format library, collections, notes, PDF cropping, duplicate detection, persistent state, Android multi-window. Premium: Drive sync, background TTS, cross-book notes/dictionary, fonts, thumbnails/layouts. [R01] [R02] [R03] | Free app advertised without ads/registration; Premium page states one payment. Proprietary app plus separate GPL EraPDF/EraEPUB/EraDjVu/EraComic/EraMOBI programs, with source offered by email. Not a full-app open-source release. [R04] [R05] |
| **FBReader Free / Premium** — `org.geometerplus.zlibrary.ui.android` / `com.fbreader` | Text formats; Readium LCP EPUB since 3.7; Premium TTS/translation and embedded PDF; Free PDF plugin; separate DjVu plugin for both. [B01] | One-time Premium purchase. PDF/DjVu excluded from read-aloud. Current source explicitly **closed**; GPL **2.6.15** source is historical. Page identifies stable **3.8.32**, **2026-08-03**, and experimental 4.0 branch. [B01] |
| **EBookDroid** — historical `org.ebookdroid` | Archived project lists PDF, DjVu, XPS, EPUB, RTF, FB2, comics. [E02] | Legacy freeware: up to **1.6.x GPLv3**, since **2.0.0 proprietary/closed-source**, with separate helpers. Play returned 404 in this fetch context; current distribution/maintenance unresolved. [E02] [E03] |
| **PDF Reader Pro** — `com.pdftechnologies.pdfreaderpro` | Android-specific pages document PDF reading modes, annotations, text/image editing, page organization, conversion, forms/signing, file access, and Wi-Fi transfer. [P01] [P02] | Terms describe a limited free license and paid plans; exact Android entitlement per tool was not verified. Full current Android app source unavailable in reviewed material. ComPDF developer links do not establish publication of this product's source. [P01] [P03] |

### Comparator qualifications

- **Adobe:** detailed Liquid Mode help, visibly last updated **2025-08-07 12:37**, describes server processing and deletion after generating the experience. It lists possible limits for over 200 pages/10 MB, scans, encryption, languages, and complex layouts; says TalkBack is supported and Dark Mode is not. These are dated documentation conditions, not verified current-app restrictions. The observed Play listing still advertises Liquid Mode. [A04] [A01]
- **Xodo:** older Reading Mode help explains that pages without extractable text, including scans, can show a no-reflowable-text message. This documents failure explanation, not current UI or entitlement. [X02]
- **Foxit:** the versioned manual documents annotations within reflow and an images on/off option: a specific mode combination, not just separate feature checkboxes. [F01]
- **ReadEra:** the claimed test against more than 500,000 books/documents is the developer's statement; no device, latency, memory, or fixture result was independently measured. [R01]
- **EBookDroid:** landing page returned a JavaScript shell; official archive JSON supplied project/license facts. Its `hasSource` flag and old mirrors do not establish post-2.0 app-source availability. One Play 404 does not prove permanent worldwide delisting. [E01] [E02] [E03]
- **PDF Reader Pro:** use its Android-specific pages for feature claims; a desktop or cross-platform product page is not proof of identical Android tools, licensing, or behavior. Its Android page identifies the package; the shared terms do not establish which current Android plan unlocks each tool. [P01] [P02] [P03]

## Coverage limits

- Native Moon PDF reflow is not settled by the reviewed official pages; [separate static evidence](#related-artifact-evidence) establishes a text-reflow code path in the supplied artifact. Complete release history, mandatory report format, official public tracker, and response SLA were not established in the reviewed pages. Unknown does not mean absent. [M01] [M02] [M03] [M08]
- Policy findings concern wording; no network or token-storage inspection was performed. [M05] [M06]
- Initial cleaned extraction omitted FAQ sections; fuller reads supplied the sync/export details used here. Press output remained truncated. [M03] [M08]
- Some discovery engines timed out or returned off-domain hits. Search snippets and APK mirrors were not used as feature or Pro-history evidence.
- Adobe locale-specific help returned 404 and one direct product-page fetch returned 403; successful official English help, product, and Play reads support the stated claims. [A01] [A02] [A04]
- Retrieval and publication dates differ. Automatically inferred review dates and copyright footers were not used as release chronology.

## Dated source ledger

All sources were retrieved on **2026-11-21**. Times are UTC where recorded; **date only** means no precise retrieval time was recorded for the full read. Source IDs link to exact primary URLs.

| ID | Source / role | Retrieval time | Source date/version qualification |
|---|---|---|---|
| [M01] | Moon homepage, features/contact | 13:56:54Z | Unversioned |
| [M02] | Pro Play, identity/features/support/privacy/notes | 13:58:02Z; full read also | Updated **2026-10-16**, **v10.8** notes |
| [M03] | FAQ, sync/TTS/fonts/backup/export | 13:58:32Z; full read also | Older Android examples; unversioned |
| [M04] | Download, packages/payment/SDK | 13:58:33Z | Regional expiry **2027-10-10** |
| [M05] | Pro privacy policy | Date only | No explicit policy version established |
| [M06] | Combined free/Pro policy | 13:58:32Z | Distinct third-party list |
| [M07] | Chinese Moon page | 14:02:31Z | Older page-specific language count |
| [M08] | Moon press collection | 14:05:35Z | Historical excerpts; truncated |
| [R01] | ReadEra homepage | 13:59:58Z; full read also | Unversioned; scale is publisher claim |
| [R02] | ReadEra Premium page | 13:59:57Z | Premium features/purchase model |
| [R03] | ReadEra Premium Play | 14:01:05Z | Updated **2026-11-07**; Markdown/backup notes |
| [R04] | ReadEra terms | 14:01:06Z | App/helper license distinction |
| [R05] | OpenReadEra | 14:01:06Z | Five GPL helpers; source-request channel |
| [P01] | PDF Reader Pro Android | Date only | Official package link |
| [P02] | PDF Reader Pro Android features | 13:59:57Z | Android-specific description |
| [P03] | PDF Reader Pro terms | 14:04:32Z | Effective **2026-03-18** |
| [D01] | Readest site | 14:03:56Z | Official Play/repository cross-links |
| [D02] | Readest pinned README | 14:06:42Z | Commit `0882c8074215edc24e2ee5ac25e99cdccddb7e34` |
| [D03] | Readest pinned LICENSE | 14:06:42Z | Same commit; AGPL v3 |
| [L01] | Librera PRO Play | 14:03:56Z | Former names/features |
| [L02] | Librera pinned README | 14:06:42Z | Commit `b7378bbde373bbf8b80842f3e47ea444fa9fd542` |
| [L03] | Librera pinned LICENSE.txt | 14:06:42Z | Same commit; GPL v3-or-later |
| [A01] | Adobe Android Play | 14:04:51Z | Package/free/Premium distinction |
| [A02] | Adobe mobile page | 13:59:57Z | Successful parsed fetch |
| [A03] | Adobe mobile overview | 14:02:32Z | Overview, not older detailed help |
| [A04] | Adobe Android Liquid Mode | 14:08:25Z; full read also | Visible update **2025-08-07 12:37** |
| [X01] | Xodo mobile page | 14:01:12Z | iOS/Android combined; platform scope preserved |
| [X02] | Xodo reflow help | 14:01:06Z | Tool reports **2022-07-07**; older guidance |
| [X03] | Xodo Android Play | 14:02:31Z | Tools advertised; entitlements untested |
| [X04] | Xodo web terms | 14:04:51Z | Last Modified **2025-07-17**; mobile terms distinguished |
| [F01] | Foxit mobile views manual | 14:01:06Z | URL version **2026.4.0** |
| [F02] | Foxit Android Play | 14:01:06Z | Features/subscription/support link |
| [F03] | Foxit app-store license | 14:04:32Z | Proprietary licensing |
| [B01] | FBReader Android | 13:59:58Z | **3.8.32**, **2026-08-03**; source status |
| [E01] | EBookDroid archive landing | 14:01:06Z | JavaScript shell |
| [E02] | Official archived project JSON | 14:03:56Z | Historical identity/license transition |
| [E03] | EBookDroid Play URL | 14:04:32Z | **404 observed**, bounded result |

[M01]: https://www.moondownload.com/
[M02]: https://play.google.com/store/apps/details?id=com.flyersoft.moonreaderp&hl=en
[M03]: https://www.moondownload.com/faq.html
[M04]: https://www.moondownload.com/download.html
[M05]: https://www.moondownload.com/privacymrp.html
[M06]: https://www.moondownload.com/privacy.html
[M07]: https://www.moondownload.com/chinese.html
[M08]: https://www.moondownload.com/press.html
[R01]: https://readera.org/
[R02]: https://readera.org/premium
[R03]: https://play.google.com/store/apps/details?id=org.readera.premium&hl=en
[R04]: https://readera.org/terms
[R05]: https://readera.org/open-readera
[P01]: https://www.pdfreaderpro.com/android
[P02]: https://www.pdfreaderpro.com/android/features
[P03]: https://www.pdfreaderpro.com/terms_of_service
[D01]: https://readest.com/
[D02]: https://github.com/readest/readest/blob/0882c8074215edc24e2ee5ac25e99cdccddb7e34/README.md
[D03]: https://github.com/readest/readest/blob/0882c8074215edc24e2ee5ac25e99cdccddb7e34/LICENSE
[L01]: https://play.google.com/store/apps/details/?hl=en-US&id=com.foobnix.pro.pdf.reader
[L02]: https://github.com/foobnix/LibreraReader/blob/b7378bbde373bbf8b80842f3e47ea444fa9fd542/README.md
[L03]: https://github.com/foobnix/LibreraReader/blob/b7378bbde373bbf8b80842f3e47ea444fa9fd542/LICENSE.txt
[A01]: https://play.google.com/store/apps/details?feature=nav_result&id=com.adobe.reader
[A02]: https://www.adobe.com/acrobat/mobile/acrobat-reader.html
[A03]: https://helpx.adobe.com/ee/acrobat/mobile/get-started/overview.html
[A04]: https://www.adobe.com/devnet-docs/acrobat/android/en/lmode.html
[X01]: https://xodo.com/mobile-apps
[X02]: https://feedback.xodo.com/support/solutions/articles/35000202857-reading-mode-reflow-
[X03]: https://play.google.com/store/apps/details?hl=en_US&id=com.xodo.pdf.reader
[X04]: https://xodo.com/legal
[F01]: https://help.foxit.com/manuals/pdf-editor/mobile/en_us/2026.4.0/Adjust_PDF_Views.html
[F02]: https://play.google.com/store/apps/details?id=com.foxit.mobile.pdf.lite&hl=en
[F03]: https://appstore.foxitsoftware.com/appstore/license
[B01]: https://fbreader.org/en/android
[E01]: https://code.google.com/archive/p/ebookdroid
[E02]: https://storage.googleapis.com/google-code-archive/v2/code.google.com/ebookdroid/project.json
[E03]: https://play.google.com/store/apps/details?id=org.ebookdroid&hl=en

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
