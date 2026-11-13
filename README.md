# enron-memory-replay

**A personal memory that lived through a real mailbox.** One Enron employee's email (the
`kaminski-v` mailbox of the public CMU Enron corpus, 11,523 messages from November 1999 to
February 2002) is replayed in the order it arrived into an
[eleman](https://github.com/akadal/eleman) memory core: an AI assistant's long-term memory kept as
plain markdown in git. Every week of mail is captured into short notes, then distilled by an
unattended consolidation run. The repository keeps every layer, from each raw message to the
distilled memory after every week, with the links between them.

> **Status: pilot, under construction.** Not frozen, no DOI yet. Layout and numbers below can
> still change. See `dataset/DESIGN.md` for the plan and `dataset/runs/` for what has run.

## What you can study with it

- **Question answering against memory at a date:** every weekly snapshot is a git tag.
- **Fact updates over time:** distilled facts are dated and move to `## History` when they change.
- **Consolidation loss:** every distilled fact links to the message it came from, and a ledger per
  week says, for every message, whether it was kept, dropped with a reason, or not durable.
- **Retrieval:** distilled memory (L1) against the verbatim archive (L2) over the same messages.
- **Re-consolidation with other models:** the capture notes are frozen, so the weekly runs can be
  repeated with another model on identical input.
- **Growth and compression** of a long-lived memory, and **person/alias resolution**.

## The layers

| Layer | Where | What |
|---|---|---|
| Stream | `dataset/manifest.csv` | One row per message: order, id (`m00001`...), source path, checksum, dates, direction, bulk class, quoted messages, thread (approximate). |
| L2, raw | `memory/archive/mail/YYYY/m<seq>.md` | Every message verbatim, uncapped. |
| Capture | `dataset/capture/s<slice>.jsonl`, `memory/archive/inbox/` | Per message: a model's durable/not-durable verdict and up to five notes, with the full response and usage. |
| L1, distilled | `memory/domains/`, `memory/people/`, `memory/state.md` | The memory after each weekly consolidation; facts end in `←[[m<seq>]]`. Tags `sleep-001`, `sleep-002`, ... |
| Ledger and runs | `dataset/ledger/`, `dataset/runs/` | Per week: where each message ended up; tokens, cost, gates, the full consolidation transcript. |

## How it was built

`dataset/DESIGN.md` describes every stage and every deviation from eleman as shipped; the short
version: a checksummed source tarball, a deterministic Python stream (de-duplication, owner
addresses, quote pointers, no model), one stateless capture call per message and one
consolidation per ISO week, both by Claude Opus 5.5 (eleman's own prompt plus a replay preamble),
each checked from outside before the next week is fed. `dataset/audit/` holds the reviews the
design went through, before it ran and after its pilots.

Four pilots are kept as branches and tagged: `pilot-raw` (raw mail straight into the inbox),
`pilot-v2` (the capture pipeline before the review's fixes, Sonnet 5.5), `control-opus` (the
same feed consolidated by Opus 5.5) and `pilot-v3` (ten weeks on the corrected pipeline, Haiku
capture). `dataset/DESIGN.md` says what each one is.

## Models

One model for every model call, fixed for the whole run, so every result can be read against a
known setup: **Claude Opus 5.5** (`claude-opus-5-5`), effort `high`, through Claude Code 2.1.323
(`claude -p`, a pinned copy, auto-update off) on a Claude subscription.

| Role | Call |
|---|---|
| Capture, one call per message | Claude Code's system prompt replaced by the capture prompt (`capture-v3`), no tools, one turn |
| Consolidation, weekly | eleman's sleep prompt plus the replay preamble, Claude Code's own tools |
| Coverage repair turn (when needed) | same as consolidation |
| Everything else (stream, description, slicing, gates, ledger) | deterministic Python, no model |

Token counts and the list-price equivalent of every call are in `dataset/capture/` and
`dataset/runs/`. Cheaper models were measured against Opus before this choice, and the results
are kept for anyone who wants to rebuild the dataset more cheaply: Claude Haiku 5.5 and Opus each
miss about a third of what the other captures, DeepSeek V4 Pro reaches 41% of Opus's facts
(`dataset/validation/`), and Opus consolidates with fewer losses and less bloat than Sonnet 5.5
on the same feed (`dataset/audit/2026-11-13-4-pilot-review.md`).

## The data is used as it is

The Enron mail has been public since 2003-2004 and is used here exactly as the CMU release
holds it: nothing is anonymised, redacted, corrected or filtered out. Each message is kept
byte-for-byte in content (only line endings are normalised; the checksum of the original bytes
sits beside it). The only messages not replayed are 26 whose Date header cannot be placed on a
timeline (a 1979 placeholder date, and one dated 2005); they are kept verbatim in
`memory/archive/mail/unplaced/`. Duplicate copies of a message across folders are replayed once
and listed in the manifest.

## Licence and citation

Code: MIT (`LICENSE`). Our own data (capture notes, distilled memory, ledger, run records):
CC BY 4.0. Message text comes from the CMU release; no further rights are claimed over it.

Until the frozen release has its own DOI, cite the source corpus and the mechanism:
Klimt & Yang (2004), https://doi.org/10.1007/978-3-540-30115-8_22, and eleman,
https://doi.org/10.5281/zenodo.23975338. The rest of this repository is the eleman template
(`AGENTS.md`, `docs/`, `memory/rules`, `memory/tools`); eleman's own README is
`docs/eleman-README.md`.
