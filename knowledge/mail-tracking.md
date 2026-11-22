---
type: Guide
title: Private outgoing report tracking
description: Durable report identities, exact message hashes, and one-shot SMTP outcomes without confusing submission with delivery.
tags: [reporting, email, tracking, evidence]
timestamp: 2026-11-22T00:00:00Z
---

# Private outgoing report tracking

The [mail tracker](../scripts/mail_tracking.py) keeps each prepared report and its
submission state in a local SQLite database. Use it with the [reporting
guide](reporting.md) to connect a specific message to an observed submission
outcome. Preparing a report does not submit it.

## Local record

The default database is `.local/mail/tracking.sqlite3`, excluded from Git. It
contains the frozen message as well as metadata, so keep it within the existing
private local access boundary. Git exclusion is not encryption. On Windows,
directory permissions are inherited; the tracker does not change Windows ACLs.

Each record includes:

- A caller-selected report ID, unique attempt ID, and RFC Message-ID.
- The sender, one recipient, subject, and preparation time in UTC.
- `content_sha256`: the exact input body's UTF-8 hash before MIME encoding.
- `wire_sha256`: the hash of the frozen RFC 5322 message passed to SMTP, including
  headers and CRLF encoding. SMTP framing and dot-stuffing are handled by the client.
- Submission-start and outcome times, status, and a numeric SMTP code when known.

The public repository contains the reusable tracker and synthetic tests. Actual
addresses, message records, and submission history stay in the local database.
SMTP credentials are handled separately from report tracking.

## Offline commands

Use Python 3.13 from the repository root. These commands initialize, prepare, or
inspect records; the command-line interface has no sending command.

```sh
python -X utf8 -B scripts/mail_tracking.py init
python -X utf8 -B scripts/mail_tracking.py prepare REPORT-001 --sender sender@example.invalid --recipient reader@example.invalid --subject "Synthetic report" --body-file .local/mail/report.txt
python -X utf8 -B scripts/mail_tracking.py list
```

The addresses above are synthetic. A body file must already exist. To select an
existing private database elsewhere, put `--db <path>` before the subcommand.
`list` returns message-identifying metadata and status without printing the body
or raw message bytes.

Within the same database, re-preparing the same ID with identical sender, recipient, subject, and body
returns its existing record and identities. Changing those fields under an
existing ID is rejected. A new report ID denotes a genuinely separate report;
it must not be used to evade an unresolved or completed send attempt.

## Submission and outcome meaning

An authorized caller uses
`submit_report(attempt_id, authenticated_smtp, db_path=...)` with an already
authenticated, debug-disabled `smtplib` client. The caller owns the selected
account, verified TLS connection, permission to send that particular message,
and connection lifecycle. Route each report submission through this function
so that its attempt is recorded before transport.

| Status | Supported conclusion | Replay behavior |
|---|---|---|
| `draft` | A message is prepared; no transport attempt has been claimed. | Can be submitted once. |
| `attempting` | The attempt claim was committed before calling SMTP. It may still be running or may have been interrupted. | Blocked pending reconciliation. |
| `accepted` | The single-recipient `smtplib.sendmail` call returned successful final DATA acceptance. | Blocked. |
| `rejected` | A recognized SMTP rejection was returned. | Blocked; retain this failed attempt. |
| `unknown` | The transport result did not establish acceptance or a recognized rejection. | Blocked pending reconciliation. |

**SMTP acceptance does not establish recipient delivery, opening, or reading.**
Those facts need separate evidence. This tool does not inspect a mailbox or
discover messages sent outside this workflow.

The claim and final result are separate durable transactions. Concurrent callers
using the same database cannot both claim one draft. A crash after claiming, a disconnect, or a failed
outcome write must not cause an automatic resend. If storing an observed result
fails, `OutcomeNotRecorded` reports the observed outcome while the retained
`attempting` state continues to block replay. Preserve that exception's outcome
as evidence and reconcile the existing attempt before further action.

This is conservative duplicate-send protection, not a guarantee of exactly-once
delivery across SQLite, SMTP, and the recipient's mailbox. There is no automated
retry or state-reset command. Raw SMTP responses and authentication transcripts
are not copied into the tracking record.

## Verification

The [focused tests](../tests/test_mail_tracking.py) use synthetic reports and real
temporary SQLite databases, substituting the SMTP submission boundary. Run:

```sh
python -X utf8 -B -m unittest discover -s tests -p test_mail_tracking.py -v
```

They exercise persistence, message identity, rejected and ambiguous outcomes,
concurrent claims, interrupted attempts, and storage failures. Passing these
tests is evidence about the tracker; it does not establish Gmail authentication,
email submission, recipient delivery, or reader application behavior. The
[repository validation guide](validation.md) covers the separate public-corpus
checks.

The [retained focused run](../evidence/mail-tracker-verification.json) passed all
25 tests on 22 November 2026 in 15.343 seconds, with exit code 0 and unchanged
source/test hashes. The receipt distinguishes that inspectable result from the
earlier reported-only full-host run.

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
