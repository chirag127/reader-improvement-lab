---
type: Report
title: KOReader contribution — CBR MIME aliases in OPDS
description: A focused alias correction with real registry and OPDS red/green regression evidence, fork provenance, and explicit host-runtime limits.
tags: [koreader, contributions, opds, mime, comics, regression-tests]
timestamp: 2026-11-21T00:00:00Z
---

# KOReader: recognize two additional CBR MIME aliases

**Implemented and host-tested.** Adding `application/vnd.comicbook+rar` and `application/x-cbr` to the existing MuPDF CBR registration makes suffixless OPDS acquisition links resolve to `cbr` and produce a download-button model. The real registry and OPDS suites produced **38 passes / 4 expected failures before the correction**, then **42 passes / 0 failures afterward**. This is executable Lua-module evidence, not a device/UI or archive-rendering result.

## Identity and attribution

Observed **2026-11-21**. The original research pin was `07d7b22098ef1693f090a881abf27ca5a25fa50a`. The existing workspace fork was clean on `master` at the newer `107b6ddaa7d671d10a82aee395f270608ce02720` when this contribution began. The implementation and test claims below refer to that newer base.

| Field | Value |
|---|---|
| Upstream | <https://github.com/koreader/koreader> |
| Fork | <https://github.com/chirag127/koreader> |
| Branch | `fix/cbr-opds-mime-aliases` |
| Commit | [`ac9a701eb6d3e1ab5ab3e9e6681018d5a36df3da`](https://github.com/chirag127/koreader/commit/ac9a701eb6d3e1ab5ab3e9e6681018d5a36df3da) |
| Existing report | [KOReader issue #15844](https://github.com/koreader/koreader/issues/15844) |
| Structured record | [`data/contributions/koreader.json`](../data/contributions/koreader.json) |

The branch is **pushed to the user's fork**. A remote readback with `git ls-remote origin refs/heads/fix/cbr-opds-mime-aliases` returned the full contribution commit above; the local checkout was clean after the push. [Publication evidence](../evidence/contributions/koreader-publication.txt).

The issue reporter already proposed these exact aliases and reported a local fix on a Kobo using KOReader 2026.07.2. That is **upstream-report** evidence, not our device reproduction. This work contributes independent executable reproduction, the focused fork patch, and regression coverage. The fork uses the existing registered workspace checkout; no second source clone was created. Existing upstream licensing in `COPYING` was preserved.

## Why this fixes the tested path

The following are **static observations** at base `107b6ddaa7d671d10a82aee395f270608ce02720`, inspected on 2026-11-21:

1. [`PdfDocument:register`](https://github.com/koreader/koreader/blob/107b6ddaa7d671d10a82aee395f270608ce02720/frontend/document/pdfdocument.lua#L370-L394) registered CBR under `application/vnd.comicbook-rar` and `application/vnd.rar`, but not the two requested aliases. CBZ already used `application/vnd.comicbook+zip` and `application/x-cbz`.
2. [`DocumentRegistry:addProvider`](https://github.com/koreader/koreader/blob/107b6ddaa7d671d10a82aee395f270608ce02720/frontend/document/documentregistry.lua#L31-L47) records MIME-to-extension mappings. [`hasProvider(nil, mime)`](https://github.com/koreader/koreader/blob/107b6ddaa7d671d10a82aee395f270608ce02720/frontend/document/documentregistry.lua#L63-L85) and [`mimeToExt`](https://github.com/koreader/koreader/blob/107b6ddaa7d671d10a82aee395f270608ce02720/frontend/document/documentregistry.lua#L224-L226) expose them. [`getProviders`](https://github.com/koreader/koreader/blob/107b6ddaa7d671d10a82aee395f270608ce02720/frontend/document/documentregistry.lua#L109-L140) deduplicates registrations for the same renderer. The registry [loads and registers real document providers](https://github.com/koreader/koreader/blob/107b6ddaa7d671d10a82aee395f270608ce02720/frontend/document/documentregistry.lua#L287-L297).
3. [`genItemTableFromCatalog`](https://github.com/koreader/koreader/blob/107b6ddaa7d671d10a82aee395f270608ce02720/plugins/opds.koplugin/opdsbrowser.lua#L957-L1049) accepts explicit acquisition relations before its generic MIME-recognition fallback. An entry being listed therefore does **not** prove its download action is supported.
4. [`getFiletype`](https://github.com/koreader/koreader/blob/107b6ddaa7d671d10a82aee395f270608ce02720/plugins/opds.koplugin/opdsbrowser.lua#L1455-L1464) first checks the URL suffix, then consults registry MIME recognition and extension mapping. A suffixless URL exposes the missing-alias behavior; a URL already ending in `.cbr` can mask it.
5. [`getDownloadButtons`](https://github.com/koreader/koreader/blob/107b6ddaa7d671d10a82aee395f270608ce02720/plugins/opds.koplugin/opdsbrowser.lua#L1234-L1332) calls `getFiletype` and adds a normal download button only when it gets a supported type. This is why the regression exercises the actual OPDS consumer as well as the registry.

No OPDS production code changed. Two registrations use the same `cbr` extension, MuPDF provider, and weight `100` as the existing entries.

### Standards versus compatibility

The [IANA registration](https://www.iana.org/assignments/media-types/application/vnd.comicbook-rar), retrieved 2026-11-21, names **`application/vnd.comicbook-rar`** and explicitly lists **`application/x-cbr`** as a deprecated alias. `application/vnd.comicbook+rar` is treated as a non-standard compatibility alias, consistent with the [maintainer comment on #15844](https://github.com/koreader/koreader/issues/15844#issuecomment-5232097418). The patch keeps the existing canonical registration first and documents the non-standard spelling inline. It does not claim a new IANA registration.

## Executed regression evidence

The tests were added before changing the implementation. Both runs used the same test content and host harness; the production change between red and green was only the two registrations.

| Verification | Result | Evidence |
|---|---|---|
| Before implementation | **38 successes, 4 failures, 0 errors; exit 1**, expected | [Red diagnostic excerpts](../evidence/contributions/koreader-red-tests.txt) |
| After implementation | **42 successes, 0 failures, 0 errors, 0 pending; exit 0** | [Green diagnostic excerpts](../evidence/contributions/koreader-green-tests.txt) |
| Focused Luacheck 1.2.0 | **0 warnings, 0 errors in 3 files; exit 0** | [Lint output](../evidence/contributions/koreader-lint.txt) |

The **13 new cases** are:

- Six registry cases calling `hasProvider(nil, mime)` and `mimeToExt(mime)` for all four CBR aliases and both CBZ aliases.
- One registry case confirming `.cbr` and `.cbz` each still resolve to one MuPDF provider at weight 100.
- Six OPDS cases parsing a synthetic Atom feed through the real `OPDSParser`, generating items through the real `OPDSBrowser`, resolving a suffixless acquisition URL, and obtaining exactly one correctly labeled download button.

The run also includes **29 existing cases** from those two files. **Eight `#internet` OPDS cases were excluded**, along with the harness's `notest` tag exclusion. Zero pending tests in Busted's summary does not mean there were no exclusions.

The synthetic acquisition link is `/opds/download/42/`, with `rel="http://opds-spec.org/acquisition"`, and its MIME type is varied across the six cases. `https://example.test/opds/` is a synthetic base URL; these tests do not contact that server. The changed [registry tests](https://github.com/chirag127/koreader/blob/ac9a701eb6d3e1ab5ab3e9e6681018d5a36df3da/spec/unit/document_registry_spec.lua) and [OPDS tests](https://github.com/chirag127/koreader/blob/ac9a701eb6d3e1ab5ab3e9e6681018d5a36df3da/spec/unit/opds_spec.lua) are the canonical fixtures and assertions.

In the red run, the requested aliases returned `false` from registry recognition and `nil` from OPDS type resolution. Those OPDS assertions fail before button generation is reached. In the green run, button generation is executed and passes for every tested alias. The harness does not mock the registry, copy its implementation, or inspect changed text as a substitute for execution.

## Host environment and reproduction

Verification ran under **Ubuntu 26.04 LTS x86_64 / WSL2**, kernel `6.18.33.2-microsoft-standard-WSL2`, on a Windows host. The initial environment lacked Lua/Busted. The following installation completed with **0 existing packages upgraded**:

```sh
apt-get install --no-install-recommends -y luajit lua-busted lua-check libsdl3-0
```

The eventual test run used **LuaJIT 2.1.1783773675 and bundled native libraries from KOReader's Linux v2026.07.1 archive**, with **Ubuntu Busted 2.3.0**. Luacheck was **1.2.0**. The packaged LuaJIT and SDL3 were used rather than the newly installed system counterparts. No host profile, personal reader settings, or device configuration was edited.

- Asset: [`koreader-linux-x86_64-v2026.07.1.tar.xz`](https://github.com/koreader/koreader/releases/download/v2026.07.1/koreader-linux-x86_64-v2026.07.1.tar.xz).
- Verified SHA-256: `299aadb28147a25e9432ced1214ea444a4184393b5ae97cf42402c8a61b1a1b0`.
- The current source expects `koreader-base` gitlink `6839b1fa580c777f9ec609a24ef55cb1a0f3bec8`; those native dependencies were **not rebuilt from that revision**.

The [published harness](../evidence/contributions/koreader-host-tests.sh) links frontend/plugin source from the existing checkout and native/common dependencies from the extracted release into a fresh scratch run directory. `KO_HOME` is private to that run. Stock `commonrequire` uses a dummy framebuffer; display/audio drivers are dummy. Native dependencies, Lua framework modules, and all actual registry/OPDS implementation modules load normally. This is a bounded adaptation of the upstream [Busted runner](https://github.com/koreader/koreader-base/blob/6839b1fa580c777f9ec609a24ef55cb1a0f3bec8/test-runner/runtests), not a full revision-matched `kodev` build.

To reproduce the green result in Ubuntu/WSL, use the existing checkout at the contribution commit and the verified, extracted release archive. Set these variables to absolute **Linux** paths:

```sh
SOURCE_DIR=/mnt/c/ws/repos/fork/koreader
RUNTIME_DIR=/path/to/extracted-release/lib/koreader
SCRATCH_DIR=/path/to/existing/disposable-scratch

# From Reader Improvement Lab:
bash evidence/contributions/koreader-host-tests.sh \
  "$SOURCE_DIR" "$RUNTIME_DIR" "$SCRATCH_DIR"

# From the KOReader checkout:
luacheck --no-color frontend/document/pdfdocument.lua \
  spec/unit/document_registry_spec.lua spec/unit/opds_spec.lua
```

The harness prints the fresh run directory and retains it for inspection. Tests that use relative sidecar paths stay within that scratch tree. For a red reproduction, use the parent implementation revision with only the two changed spec files from the contribution commit; run the same harness before applying the two production registration lines. Save any existing work before changing revisions. No source re-clone is needed.

### Checks not run

- Fully revision-matched native build; `./kodev test front document_registry opds`; complete frontend/base suites; full project CI.
- Eight internet-tagged cases in `opds_spec.lua`; live OPDS server integration and actual acquisition downloads.
- Actual CBR/CBZ archive parsing/rendering, application display, Android/Kobo behavior, and other device classes.
- Comprehensive MIME parameter/case handling, generic link relations, or OPDS 2.0 coverage.

These boundaries prevent upgrading the host result into a claim that an official release or the reporter's exact environment was reproduced.

## Remaining device verification

**Device-level OPDS acquisition, download and rendering A/B was not run.** A useful follow-up is an A/B test of the base and patched builds against a local synthetic OPDS feed with the six MIME cases and suffixless URLs, using a legally redistributable synthetic comic archive. Record the exact build/APK SHA-256, fixture hash, explicitly selected disposable AVD/ADB serial, steps, visible download action, actual download, and opening/rendering result. The Lua fixture tests above establish bounded type/button behavior; this device follow-up remains unperformed.

## Upstream submission instructions

No upstream issue, PR, comment, release, or developer message was sent. A bounded GitHub PR search for `repo:koreader/koreader is:pr CBR` on 2026-11-21 returned 11 closed matches and no open result; this is not an exhaustive duplicate check. Issue #15844 was open at retrieval.

Before any later submission:

1. Review current [upstream contribution guidance](https://github.com/koreader/koreader/blob/107b6ddaa7d671d10a82aee395f270608ce02720/doc/Collaborating_with_Git.md#L126-L138) and search again for related PRs, including #15844, `application/x-cbr`, and `application/vnd.comicbook+rar`.
2. Have the human contributor review the patch and **write their own commit message and PR explanation**, as upstream explicitly requires, and personally handle review discussion. This generated research note is evidence, not a ready-to-post human-authored submission.
3. Build using the project's current [build instructions](https://github.com/koreader/koreader/blob/107b6ddaa7d671d10a82aee395f270608ce02720/doc/Building.md), then run `./kodev test front document_registry opds` with matching native dependencies, plus the applicable CI checks. Keep this report's host-dependency mismatch and excluded tests visible until those checks are actually completed.
4. Reference #15844, explain suffixless URL fallback, credit the reporter's original alias proposal, preserve the canonical IANA spelling, and attach the focused red/green evidence. Submit only after a separate instruction authorizes that action.

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
