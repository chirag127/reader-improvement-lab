---
type: Guide
title: Reporting reader findings and feature refinements
description: Verified Moon contacts, duplicate-search and evidence guidance, and unsent bug, feature, and policy drafts.
tags: [moon-reader, support, reporting, evidence, drafts]
timestamp: 2026-11-21T13:58:02Z
---

# Reporting findings and feature refinements

**Submission status: UNSENT — no emails or upstream issues submitted.** These are preparation instructions and drafts. The [Moon baseline](moon-baseline.md) owns feature, release, comparator, and policy analysis; this guide turns supported findings into focused reports.

The [22 November REA developer digest](rea-followup.md) provides the prioritized saved-form packet, search-error reproduction protocol and native/speech evidence limits. The [ten-workflow supplement](moon-followup-proposals.md) brings the Moon backlog to 74 proposals. These linked packets retain their own observation dates and submission status.

## Verified official channels

All sources were retrieved on **2026-11-21**; the [baseline ledger](moon-baseline.md#dated-source-ledger) retains their dates and scope.

| Purpose | Published channel | Primary evidence / retrieval |
|---|---|---|
| Product support, bugs, feature suggestions | **[seanyword@gmail.com](mailto:seanyword@gmail.com)** | Homepage **Contact**, 13:56:54Z; Pro Play **App support**, 13:58:02Z and full read. Pro advertises customer email support; homepage welcomes suggestions/comments. [M01] [M02] [M03] |
| Privacy-policy questions | **[moonplusreader@gmail.com](mailto:moonplusreader@gmail.com)** | **Contact Us** in Pro policy, date-only full read, and combined policy, 13:58:32Z. [M05] [M06] |
| Self-service guidance | **[Official FAQ][M03]** | Linked from official site and Pro Play; 13:58:32Z and full read. [M01] [M02] [M03] |

Email is an explicitly advertised support route. Reviewed sources do not establish a mandatory bug/feature template, verified in-app reporting menu, official public tracker, or response SLA. The following workflow is this project's recommendation, not an invented developer requirement. [M01] [M02] [M03]

## Other entry points and feedback routes

These routes were checked against the publisher sources above and Google Play Help on **2026-11-21**. Several are different ways to reach the same contact, rather than separate support queues.

| Route | How to use it | Audience and limitation |
|---|---|---|
| Direct developer email | Send a concise bug report or feature request to **seanyword@gmail.com**. Include the exact build, steps, expected/actual result, and a small shareable example. | Direct Moon support; the recommended route for technical reports and a prioritized request digest. [M01] [M02] |
| Google Play **App support** | Open the [Moon+ Reader Pro listing][M02] in Play, tap **App support**, then its email link. | Another entry point to the same developer email, not a separate Google bug-ticket system. [G01] |
| Official website **Contact** | Open [moondownload.com][M01] and use its published contact email. Consult the [FAQ][M03] for existing settings and troubleshooting first. | The same developer contact. The reviewed site did not establish a separate ticket form; the FAQ itself is not a submission channel. |
| Privacy-policy contact | Email **moonplusreader@gmail.com** using the [Pro policy][M05] contact. | Published route for privacy-policy questions; use the product-support address for ordinary feature requests. |
| Public Google Play review | On the app listing, choose **Write a review**; an existing review can be edited with follow-up information. | Public feedback visible to users and the developer. Google links reviews to the reviewing account. Email is better for attachments and detailed reproduction. Review eligibility requires a previously downloaded/installed app and an eligible account. [G02] |
| Private Play beta feedback, **if available** | If enrolled in a Moon beta, open Play → profile → **Manage apps & devices** → **Beta** → the app → **Private feedback to developer** → **Write feedback**. | Google documents this private developer-feedback mechanism. This investigation has **not verified an available Moon beta**, so it is conditional rather than a confirmed Moon-specific channel. [G03] |
| Google Play app/developer report | Use Play's **More → Flag as inappropriate**, or the reporting links in [Google's guide][G04]. | Reports policy or illegal-content concerns to **Google**, not ordinary Moon bugs or feature requests. It is not an escalation mechanism for a declined enhancement. |

An official Moon GitHub/GitLab issue tracker, public feature-voting board, support phone/chat, social-media support account, and an exact in-app feedback path were **not established in the reviewed sources**. This is a bounded verification result, not proof that none exists. A community forum or this independent repository can help organize evidence, but developer receipt must be established through a verified channel.

**For a large backlog:** email one short introduction with the public report link and three to five priority requests. Offer individual reproducible bug packets and ask how the developer prefers the remaining ideas. Keep later evidence in the same thread; sending the same backlog through every entry point does not create independent reports.

Google's contact guide states an expectation of a response within three business days for **purchase-related problems**. It does not promise a three-day answer or implementation for general bug reports and feature requests. [G01]

## Check for an existing answer or duplicate

1. **Resolve the product.** Match package/store/repository URL; consult [Reader Pro candidates](moon-baseline.md#resolving-the-name-reader-pro) for ambiguity. Do not select a similarly named project's tracker.
2. **Check existing support and release notes.** Match the report to `MF-01`–`MF-21`. TTS, export, sync, themes, publisher-formatting preview, and v10.8 relinking are already documented; identify the remaining interaction or failure. Also consult the [separate artifact evidence](moon-baseline.md#related-artifact-evidence) for existing reflow, settings-search, and Readwise-upload paths, preserving its build/provenance qualification. [M02] [M03]
3. **Search narrowly.** Suggested queries: `site:moondownload.com "<exact option or symptom>"` and `"Moon+ Reader Pro" "<distinctive error>"`. Read the pages, not snippets. Record query, date, examined URLs, version context, and whether a match actually covers the same behavior. Use “no match in the pages reviewed,” not “no duplicates exist.”
4. **Use a verified tracker when available.** For another reader, follow its official repository/support link and search open/closed issues, releases, and contribution guidance. Do not invent a Moon GitHub tracker. Third-party forums and this repository are not official Moon support channels.
5. **Preserve report identity.** Add new measured evidence to a matching issue or known email thread rather than creating another report. Keep private thread details in an appropriate private record.

These are future preparation steps, not a claim that every proposal already received an exhaustive duplicate search. An older report remains `upstream-report` evidence until reproduced under the [evidence contract](design.md#evidence-contract).

## Build an evidence packet

Use one concrete problem per bug report. A small related feature digest may suit email; the full proposal corpus is not a replacement for reproducible examples.

| Field | Include | Do not infer |
|---|---|---|
| Product/build | App/package, version/build, acquisition channel, relevant artifact hash | Authenticity from matching package/version |
| Environment | Device/emulator, Android/API, engine/backend versions, connectivity, orientation, reading mode | Results on untested devices/accounts |
| Input | Small redistributable/synthetic fixture, format, ID/hash, text-layer status when relevant | That a scan necessarily supports text extraction |
| Steps | Starting state, numbered actions, settings, lifecycle transitions, expected outcome | Unperformed resets/checks or last-working releases |
| Observation | Actual result, measured repetitions, relevant screenshot/log | Universal failure or performance ranking from one run |
| Existing capability | MF ID, precise primary URL, retrieval date, remaining gap | “Add TTS/sync/export” for an existing capability |
| Duplicate search | Date, scope, queries, examined URLs, match rationale | Exhaustiveness from a bounded search |

The [methodology](methodology.md#defect-threshold) distinguishes documentation, static observations, runtime results, and proposals. The [artifact record](../data/artifact.json) retains supplied-APK provenance/verification limits; results from that artifact remain artifact-specific until an official-build reproduction supports a release-level claim.

- **Sync:** record position and annotation completion separately: FAQ documents position-first, annotation-later synchronization around Pause/Resume. [M03]
- **TTS:** record the engine and battery/background settings of both apps, as the FAQ discusses both. [M03]
- **Backup/export:** preserve fixture/evidence and relevant backups before reset or migration experiments. Whole-library backup and current-book export already exist in FAQ guidance. The backup-first order is this project's recommendation. [M03]

Public evidence should contain original analysis, minimal diagnostics, and shareable fixtures. Omit credentials/tokens, personal device paths, private books, receipts, unrelated library data, APKs, and extracted proprietary code, following [project policy](../AGENTS.md). State paid-user status only if true; ordinary reproduction does not require publishing a receipt.

## Bug report email draft

**UNSENT — template, not a confirmed defect.** Fill placeholders from observations; the address is the published support channel. [M01] [M02]

```text
To: seanyword@gmail.com
Subject: [Bug][Moon+ Reader Pro <build>][component] <specific symptom>

Hello Moon+ Reader team,

I am a paid Pro user [retain only if accurate]. On <device/Android>, using
<exact build and acquisition channel>, I observed <one symptom>.
I know <existing capability> is supported; the issue is <specific case>.

Input: <shareable fixture, format, ID/hash>
Mode/settings: <values>
Engine/backend, if relevant: <details>
Artifact provenance: <verified acquisition or explicit uncertainty>

Steps:
1. <Starting state and action>
2. <Action>
3. <Action>

Expected: <specific outcome>
Actual: <observation>
Repeatability: <measured count, or not yet measured>
Last working build: <tested build, or unknown>

FAQ checks actually performed: <details or none>
Duplicate search: <date, scope, known matching report if any>
Evidence: <small fixture and relevant screenshot/log link>
Official feature reference: <URL and retrieval date>

Is this known, or have I missed an existing setting?
I can provide a targeted reproduction if useful.

Thank you,
<Name>
```

## Feature refinement email draft

**UNSENT — proposal template.** Acknowledge existing support, then describe the desired outcome. The baseline does not prove a refinement is absent. [M02] [M03]

```text
To: seanyword@gmail.com
Subject: [Feature refinement][workflow] <specific desired outcome>

Hello Moon+ Reader team,

I use Pro <build> for <reading task>. I already use <existing feature>
and checked <option/FAQ section, URL, retrieval date>.

Current workflow: <steps actually observed>
Remaining friction: <specific cost or interaction>

Would you consider <one focused refinement>?
It would help if:
- <observable acceptance condition>
- <observable acceptance condition>

Duplicate search: <date and scope; known related request if any>
Optional comparison: <product/version and precise interaction,
primary URL/date; say whether documented only or actually tested>

If Moon already offers this through another setting, please point me to it.

Thank you,
<Name>
```

For example, sync refinements may concern visible completion/errors or recovery from an observed conflict, acknowledging `MF-12`/`MF-13`. The official pages do not settle PDF reflow, but [separate supplied-artifact evidence](moon-baseline.md#related-artifact-evidence) records text-reflow, settings-search, and Readwise-upload code paths. Inspect the relevant official-build workflow before describing a refinement as missing. [M03] [M05] [M02]

## Privacy-policy clarification draft

**UNSENT — evidence-backed wording inquiry.** Analysis lives once in [MD-01](moon-baseline.md#policy-wording-inquiry); the message uses the policy contact. [M05] [M06]

```text
To: moonplusreader@gmail.com
Subject: Clarification of Moon+ Reader Pro privacy-policy wording

Hello Moon+ Reader team,

When reading the Pro documentation on 2026-11-21, I noticed that Play
Data safety and later Pro-policy disclosure sections say the app does
not collect or share data. Earlier sections describe third-party
services and error Log Data that may include IP/device details.

Could you clarify which clauses apply to Pro 10.8, whether any crash
reporting is present or optional, and which flows belong to user-selected
cloud providers rather than the developer?

This is a documentation question; this review has not established
undisclosed network transmission.

Sources read on 2026-11-21:
https://play.google.com/store/apps/details?id=com.flyersoft.moonreaderp&hl=en
https://www.moondownload.com/privacymrp.html

Thank you,
<Name>
```

## Submission and follow-up

1. Keep **draft**, **submitted**, **acknowledged**, **fixed**, and **independently retested** distinct. Unfilled observation placeholders remain templates.
2. Review the exact recipient, subject, evidence, and build qualification before a requested submission. Publishing this corpus sends nothing to a developer.
3. If a particular report is later sent, record date/channel and the confirmed result; keep new evidence in the same thread. Reviewed Moon sources promise no particular response time. [M01] [M02] [M03]
4. An acknowledgement or release-note change is not independent retesting on a named build and fixture.

**For this documented work: no emails, upstream issues, or upstream pull requests submitted.**

[M01]: https://www.moondownload.com/
[M02]: https://play.google.com/store/apps/details?id=com.flyersoft.moonreaderp&hl=en
[M03]: https://www.moondownload.com/faq.html
[M05]: https://www.moondownload.com/privacymrp.html
[M06]: https://www.moondownload.com/privacy.html
[G01]: https://support.google.com/googleplay/answer/113418?hl=en
[G02]: https://support.google.com/googleplay/answer/4346705?hl=en
[G03]: https://support.google.com/googleplay/answer/7003180?hl=en
[G04]: https://support.google.com/googleplay/answer/2853570?hl=en

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
