# Reader Improvement Lab

An independent, evidence-backed investigation of **Moon+ Reader Pro 10.8** and alternative PDF/ebook readers. It connects existing features, inspected code, synthetic test inputs, and actionable developer feedback.

**Research snapshot: 21 November 2026.** Source research, static analysis, synthetic checks, and bounded Android observations are recorded below. This repository distinguishes publisher documentation, executed tests, and proposals. It is an independent investigation, not an official support tracker.

## Start here

| Question | Read |
|---|---|
| Which open-source readers are relevant? | [Eight Android/cross-platform projects](knowledge/alternatives-android.md) · [ten desktop/web projects](knowledge/alternatives-desktop-web.md) |
| What does Moon already offer? | [Official feature baseline](knowledge/moon-baseline.md) |
| Which improvements should I request? | [64 prioritized Moon proposals](knowledge/moon-improvements.md) · [detailed acceptance criteria](data/moon-improvements.json) |
| What is inside the supplied APK? | [Implementation map and static candidates](knowledge/apk-analysis.md) · [artifact identity](data/artifact.json) |
| Which possible defects deserve reproduction? | [Six source-grounded bug-report candidates](knowledge/bug-candidates.md) |
| How do their capabilities compare? | [Feature comparison](knowledge/feature-matrix.md) |
| What improvements could help other readers? | [21 Android proposals](data/alternative-proposals-android.json) · [13 desktop/web proposals](data/alternative-proposals-desktop-web.json) |
| Has any reader been improved? | [KOReader CBR/OPDS fix](knowledge/contributions-koreader.md) · [MuPDF first-page link fix](knowledge/contributions-mupdf-android.md) — both host-tested and pushed to forks; neither submitted upstream |
| What can I reproduce locally? | [Synthetic fixture guide](knowledge/testing-fixtures.md) · [expected properties and hashes](fixtures/manifest.json) |
| Which application checks are specified? | [36-workflow test matrix](knowledge/testing-plan.md) · [additional search, speech and malformed-file inputs](knowledge/testing-scenarios.md) |
| What actually happened in the Android app? | [Runtime findings and coverage](knowledge/runtime-results.md) · [36 case records](data/runtime-results.json) · [hashed evidence](evidence/runtime/manifest.json) |
| How do I report a finding? | [Verified contacts, reporting steps, and draft templates](knowledge/reporting.md) |
| How should I interpret the evidence? | [Methodology](knowledge/methodology.md) · [complete knowledge index](knowledge/index.md) |
| What remains unverified? | [Question-by-question coverage](knowledge/coverage.md) |

## Important findings

- Moon already advertises TTS, PDF annotations/forms, backup/export, cloud synchronization, and extensive reading controls. The supplied APK also contains PDF text-reflow, settings-search, and Readwise-upload implementations. Suggestions should refine a specific workflow rather than re-request an existing feature.
- Readest already has a UI-connected Moon+ `.mrexpt` importer. More useful migration requests concern anchor accuracy, color fidelity, and understandable partial-import results.
- Current Librera source includes PDFium and foliate/WebView paths. MJ PDF's canonical GitLab source is newer than its GitHub mirror. Old descriptions can produce misleading feature comparisons.
- The Moon backlog contains 64 distinct proposals across 12 categories, each acknowledging existing capabilities and carrying acceptance criteria, sources and limitations. All remain drafts.
- Eighteen original inputs are available: the eleven-document core corpus and seven additional search, speech and malformed-file scenarios. Their host checks are separately recorded; they do not certify any reader application.
- The source/documentation inventory covers 18 public-source projects and seven commercial or legacy product families. Ten alternative projects received targeted implementation review; each dossier identifies the exact files examined.
- The KOReader contribution adds two CBR MIME aliases for suffixless OPDS downloads. Its real registry/OPDS tests changed from four expected failures to 42 passes; the tested commit is published to the fork. Device downloads and rendering were not part of that host run.
- The MuPDF contribution corrects first-page internal-link handling. Its 15 Java/Robolectric tests changed from five failures to zero; the tested source is published to the fork. The host tests substitute the native document boundary.
- The supplied-APK runtime matrix records **3 pass, 6 partial, 1 fail, 7 blocked, and 19 not-run cases**. Successful subsets include rendering, internal navigation, search, password handling, and a persisted note. [Each result names its exact scope](knowledge/runtime-results.md#complete-canonical-coverage).
- **Two edited form PDFs contain an incremental trailer with `/Prev -1`.** pypdf rejects both; PyMuPDF opens with repair and recovers the edits. The second repetition was text-only. This [saved-form interoperability failure](knowledge/runtime-results.md#repeated-saved-form-interoperability-failure) is specific to the supplied sample and environment.
- Cloud, speech, TalkBack, physical-device coverage, comparative performance, and the two contribution fixes' application/device A/B remain unverified. The disposable emulator and its private ADB server were [stopped after preserving evidence](evidence/runtime/cleanup.json).

### Supplied APK provenance

The examined file declares `com.flyersoft.moonreaderp`, version `10.8`, code `1008000`. Its SHA-256 is:

```text
e2c0ef649413b2f6671598ac8b027d582ba220e38738f2e253694289ea20e1fc
```

Android `apksigner verify --verbose --print-certs` returned **DOES NOT VERIFY**, reporting v1 digest mismatches in two DEX members. The user is unsure of the file's origin. This establishes a provenance limitation for the sample, not a defect or malicious behavior in the official product. [Exact verification evidence](evidence/apk-signature-verification.txt).

The audit emulator accepted the unchanged APK, whose initial screen displayed a **LITEAPKS mod-store promotion**. Installation acceptance does not authenticate the publisher. The [retained screenshot and explanation](knowledge/runtime-results.md#installation-promotion-and-storage-onboarding) belong to this sample; official Play-build behavior was not established.

## Validate the research and reproduce fixture checks

The offline repository validator needs only Python's standard library:

```sh
python -X utf8 -B scripts/validate_repository.py --output .local/repository-validation.json
```

It checks records, local links, references, fixture identities and selected evidence
hashes. See [validation scope and maintenance](knowledge/validation.md).

Use Python 3.13 with the [recorded direct dependencies](fixtures/requirements.txt):

```sh
python -m pip install -r fixtures/requirements.txt
python -X utf8 -B -m unittest discover -s tests -v
python -X utf8 -B scripts/check_fixtures.py --fixtures fixtures --output .local/reference-results.json
```

The checker reads the committed corpus and writes a new result. Generate into a new directory when experimenting, so existing test inputs keep their recorded hashes:

```sh
python -X utf8 -B scripts/generate_fixtures.py --output .local/rebuilt-fixtures
```

The [final combined host run](evidence/host-suite-verification.json) passed **68 tests**: 17 core-fixture, eight scenario, and 43 repository-validator tests. The retained [core reference run](evidence/fixture-verification.json) also passed 42 fixture/engine pairs and 590 property comparisons. These are host-tool results; [Android application results](knowledge/runtime-results.md) have their own execution evidence. See the guides for exact tool versions and reproducibility limits.

## Contribute evidence

Use the repository's bug-candidate or improvement issue form. Include an exact application build or source commit, observation date, source URL, synthetic input/hash, and clear expected/actual behavior. Label an idea as a proposal and an unperformed test as not run. “Not found in the inspected files” does not establish absence from an entire product.

The canonical public research lives in `knowledge/` and `data/`; supporting observations live in `evidence/`. Original fixtures and investigation tooling are reusable under [MIT](LICENSE). Third-party fonts and contribution patches retain their own licenses. APKs, bulk proprietary decompilation, credentials, and personal documents remain outside the public corpus.

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
