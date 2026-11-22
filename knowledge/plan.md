---
type: Plan
title: Reader investigation execution plan
description: Checkable delivery steps and evidence boundaries for the reader audit.
tags: [readers, research, plan]
timestamp: 2026-11-21T00:00:00Z
---

# Reader investigation implementation plan

> **For agentic workers:** Execute the assigned task against this plan and the design. Preserve existing completed evidence and use isolated write surfaces. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish a source-backed reader comparison, at least fifty actionable Moon+ Reader improvements, reproducible tests, and verified open-source contribution work.

**Architecture:** Parallel research, static-analysis, fixture, and Android-environment lanes produce source records. One integration lane curates the public knowledge bundle and verifies claims against those records.

**Tech Stack:** Markdown/YAML frontmatter, JSON, Python PDF tools, Android SDK, REA/JADX, Git/GitHub CLI.

**Spec:** [Investigation design](design.md).

## Global constraints

- Label evidence types and exact artifact/upstream identities.
- Keep official-app claims separate from this unknown-origin APK.
- Use synthetic documents and a disposable explicitly targeted AVD.
- Keep each public finding canonical within this repository.
- Preserve existing workspace changes and restrict commits to this investigation.

## Review focus

- Existing advertised features mistakenly presented as missing: compare every proposal to the baseline and mark it as an extension when appropriate.
- An upstream issue, static branch, or fixture check mistaken for a reproduced app defect: verify result provenance.
- Unpinned or stale sources: name the observed revision/date and retained coverage limits.
- Corrupted, encrypted, rotated, and image-only PDFs: include explicit expectations and avoid treating parser tolerance as universal conformance.
- Private paths, proprietary bodies, or user content entering publication: review the tracked-file inventory and actual diff.

## Task 1: Establish artifact and alternatives

**Files:** `knowledge/`, `data/`, curated `evidence/`.

**Interface:** Source records feed the baseline, comparison, proposals, and test matrix.

- [x] Identify the supplied file and record its SHA-256 and signature-verification result.
- [x] Create the requested public repository and register its workspace submodule.
- [x] Complete the primary-source alternative inventory and record discovery boundaries.
- [x] Record package structure and focused code observations with limitations.
- [x] Verify every material claim has a source or explicit unknown status.

## Task 2: Produce comparison and proposals

**Files:** comparison and backlog records under `data/`; interpretation under `knowledge/`.

**Interface:** Each proposal references existing feature or comparison evidence and carries a unique ID, priority, rationale, and acceptance criterion.

- [x] Assemble the documented/static feature comparison.
- [x] Produce at least fifty non-duplicate Moon+ Reader proposals.
- [x] Add issue and enhancement candidates for source-reviewed alternatives.
- [x] Check that suggestions do not masquerade as confirmed defects or feature absences.

## Task 3: Execute reproducible testing

**Files:** synthetic fixture generator/tests and public test records.

**Interface:** Fixture IDs and hashes connect test cases to exact inputs; result records identify the application and environment.

- [x] Validate existing host PDF tools and generate synthetic fixtures.
- [x] Verify fixture properties with independent assertions.
- [x] Provision and verify a disposable Android AVD.
- [x] Exercise the selected APK and representative workflows; retain screenshots/log excerpts where useful.
- [x] Record pass, partial, fail, blocked, and not-run separately; state measurement scope. Partial results identify successful subchecks and specified actions not executed.

## Task 4: Improve an open-source reader

**Files:** focused changes in a registered contribution fork; evidence and links here.

**Interface:** A contribution record identifies upstream revision, change, regression check, patch/commit, and submission state.

- [x] Choose a source-backed bounded improvement.
- [x] Reproduce the behavior with a meaningful failing check.
- [x] Implement the focused correction or enhancement.
- [x] Run the relevant upstream verification and record limits.
- [x] Publish the contribution artifact and document its exact status.

## Task 5: Review and publish

**Files:** `README.md`, knowledge navigation, reporting instructions, validation tooling.

**Interface:** A standalone reader can navigate claims, reproduce checks, and prepare a focused report.

- [x] Add sourced developer contact instructions and issue templates.
- [x] Validate structured records, links, counts, evidence status, and publication candidates; staged-byte verification is part of publication.
- [x] Obtain an independent claim/coverage review and address material findings.
- [x] Commit and push the initial investigation; verify the public remote content at `060fc174671c7e82072db905e4f9f1f1e15e5d60`.
- [x] Publish the workspace registration and documentation pointer on an isolated task branch, preserving the active workspace branch and normal index. This operational workspace is private; the public research is self-contained here.

## Task 6: Focused REA follow-up — 22 November

- [x] Match the relocated APK to the original digest and reuse completed evidence.
- [x] Inspect unresolved search, speech and Java/native save boundaries; record bounded coverage and unknowns in the [follow-up](rea-followup.md).
- [x] Add [ten distinct proposals](moon-followup-proposals.md), with 30 prospective criteria and an [independent semantic review](../evidence/reviews/moon-followup-proposals.json).
- [x] Extend optional-supplement validation and retain the [50-test focused result](../evidence/validator-supplement-verification.json).
- [x] Complete follow-up evidence review, validate the integrated corpus and publish [the changed deliverables](https://github.com/chirag127/reader-improvement-lab/commit/5d64d04c95950f71d5d491bd0632e656b64d6ced) with anonymous remote readback.

## Execution notes

2026-11-21: The user asked to install whatever is needed and proceed. The public repository is the requested deliverable, not a replacement for the broader investigation. Shell background completion notifications are authoritative; do not poll pending jobs or repeat uncertain operations.

2026-11-21: Static analysis delivered 13 original findings with complete package declarations and focused method/smali evidence. The fixture lane delivered 11 synthetic documents, 17 passing tests, and 42 passing fixture/engine pairs. These are separate evidence classes; neither establishes application runtime success. See [coverage](coverage.md), [static verification](../evidence/static/verification.json), and [fixture verification](../evidence/fixture-verification.json).

2026-11-21: Completed research covers 25 alternatives and ten targeted implementation reviews. The Moon backlog contains 64 draft proposals; the alternative backlogs contain 34. Eighteen synthetic inputs are retained. Bounded static follow-up is integrated; both contribution branches are host-tested and pushed to forks. The [runtime ledger](runtime-results.md) records 3 pass, 6 partial, 1 fail, 7 blocked and 19 not-run cases, with owned-resource cleanup completed. The [combined host suite](../evidence/host-suite-verification.json) passed 68 tests, including 43 validator tests after evidence-integrity fixes. Final publication validation passed across 203 candidates, 947 local links and 234 hashes. Initial research commit `060fc174671c7e82072db905e4f9f1f1e15e5d60` was published and anonymously read back: 203 blobs and 18 directories matched, plus six byte-identical selected raw files. Task-only workspace integration remained outstanding.

2026-11-22: The [REA follow-up](rea-followup.md) and [ten additional proposals](moon-followup-proposals.md) were published at `5d64d04c95950f71d5d491bd0632e656b64d6ced`. Anonymous readback matched all 210 public blobs and 18 directories, plus the bytes of all 17 changed files. The corpus contains 74 Moon proposals with 220 prospective criteria. Its validation passed 1,152 local links and 241 hashes with zero errors; the separate focused validator suite passed 50 tests. Eight distinct method selections and four bounded native disassembly captures add static evidence only. The Android execution counts and official-build limitations remain as recorded in [coverage](coverage.md). Workspace registration was published on a separate task branch without merging into or changing the unrelated active branch.

The dated [test matrix](testing-plan.md) is preserved at the exact hash used during runtime curation. Its original outcome list predates the **partial** classification explained in the [runtime result contract](runtime-results.md#evidence-and-counting); no case criteria were changed to improve a result.

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
