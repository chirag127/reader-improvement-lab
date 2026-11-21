---
type: Design
title: Reader Improvement Lab investigation design
description: Evidence contract and delivery scope for a public reader comparison and improvement project.
tags: [readers, research, evidence, design]
timestamp: 2026-11-21T00:00:00Z
---

# Investigation design

## Intent

A paying Moon+ Reader user wants actionable developer feedback, a source-backed comparison with alternatives, reproducible tests, and useful improvements to open-source readers. The deliverable is a public, independently usable knowledge repository.

## Approach

| Approach | Strength | Limitation |
|---|---|---|
| Documentation-only comparison | Broad discovery at low setup cost | Cannot establish implementation behavior or reproduce defects |
| APK-only reverse engineering | Identifies shipped declarations and implementation paths | Cannot establish official provenance, usability, or runtime correctness |
| Combined source, artifact, and runtime investigation | Connects recommendations to existing features and reproducible evidence | Runtime and contribution coverage must be explicitly bounded |

Selected by the investigator: the combined approach, consistent with the user's request to proceed and install needed tools. Independent research and environment work run in parallel; integration and publication use a single owner.

## Evidence contract

- `documented`: a primary source describes the feature; it was not necessarily tested.
- `static-observation`: source or package inspection establishes a declaration or code path.
- `runtime-observation`: the selected application was actually exercised, with recorded steps and results.
- `upstream-report`: an existing issue describes a problem; this investigation has not necessarily reproduced it.
- `proposal`: a suggested outcome, not a claim that a feature is missing or broken.
- `unknown` / `blocked`: evidence needed for a conclusion is unavailable.

Each finding identifies its source and observation date. Code references are pinned to a commit where possible. APK observations identify the exact SHA-256. A bounded negative search remains bounded. A planned test never receives a passing result.

## Parts

1. **Alternative inventory:** direct Android readers, adjacent desktop/web readers, and rendering engines. Resolve ambiguous product names such as “Reader Pro” rather than guessing a repository.
2. **Moon+ Reader baseline:** official feature documentation alongside the supplied APK's identity, manifest, package structure, and focused implementation observations.
3. **Feature matrix:** formats, rendering, search, annotations, library management, text-to-speech, synchronization, accessibility, offline use, and portability.
4. **Quality investigation:** reliability, performance, memory, accessibility, privacy, interoperability, and Android lifecycle/storage behavior. Track suspected non-working features separately from these non-functional requirements.
5. **Improvement backlog:** at least fifty distinct proposals, each with rationale, evidence or comparison basis, priority, and a checkable acceptance criterion. Extensions to an existing feature are labeled as extensions.
6. **Reproducible tests:** synthetic documents, fixture checks, an explicit Android test matrix, and observed results. Host renderer results do not stand in for reader results.
7. **Open-source contributions:** identify issue candidates from examined code, reproduce a bounded defect or missing behavior, implement a focused improvement, and preserve the upstream verification evidence.
8. **Reporting:** developer contact sources, duplicate-search instructions, bug/feature templates, and a staged submission guide.

## Constraints and decisions

- “All alternatives” is an open-ended universe. Publish the searched inventory, inclusion criteria, exact reviewed set, and coverage gaps; make no exhaustive-market claim.
- The supplied APK's origin is unknown. Its v1 signature verification fails. Results from this artifact are not automatically findings about the official app.
- The public repository contains original findings and synthetic inputs. APKs and bulk decompilation remain local research inputs.
- Use existing Java, Android SDK, Python, and GitHub authentication where verified. Add only tools required by a concrete analysis or test.
- Android runtime work uses a disposable, account-free AVD with explicit serial targeting.
- The user's direct request makes this repository the canonical home of its public research. Workspace documentation links here; it does not mirror these notes.
- Publish the repository as requested. Developer emails and upstream issue submissions remain prepared drafts unless the user explicitly requests sending a particular report.

## Completion criteria

- The public repository has usable navigation, sources, artifact limitations, a feature comparison, and at least fifty distinct proposals.
- Every claimed test has execution evidence; unperformed tests and unavailable capabilities are visible.
- Code-comparison coverage names the upstream revisions and files actually examined.
- Contribution status distinguishes proposed, implemented, tested, submitted, and merged.
- Repository validation passes and publication is verified by a remote readback.
- Remaining work, including any official-build reproduction and untested device classes, is explicit.

## Builder-owned choices

Markdown with YAML frontmatter is the human-readable knowledge format. JSON records support validation and reuse. Source citations use stable upstream links. The investigator selects representative platforms and prioritizes high-value, reproducible contributions rather than issuing a large unverified bug dump.

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
