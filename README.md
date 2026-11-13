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
| Stream | `dataset/manifest.csv` | One row per message: order, id (`m00001`...), source path, checksum, dates, direction, bulk class, quoted messages, thread. |
| L2, raw | `memory/archive/mail/YYYY/m<seq>.md` | Every message verbatim, uncapped. |
| Capture | `dataset/capture/s<slice>.jsonl`, `memory/archive/inbox/` | Per message: a model's durable/not-durable verdict and up to five notes, with the full response and usage. |
| L1, distilled | `memory/domains/`, `memory/people/`, `memory/state.md` | The memory after each weekly consolidation; facts end in `←[[m<seq>]]`. Tags `sleep-001`, `sleep-002`, ... |
| Ledger and runs | `dataset/ledger/`, `dataset/runs/` | Per week: where each message ended up; tokens, cost, gates, the full consolidation transcript. |

## How it was built

`dataset/DESIGN.md` describes every stage and every deviation from eleman as shipped; the short
version: a checksummed source tarball, a deterministic Python stream (de-duplication, owner
addresses, quote pointers, no model), one stateless capture call per message (Claude Haiku 5.5),
and one consolidation per ISO week (Claude Sonnet 5.5, eleman's own prompt plus a replay
preamble), each checked from outside before the next week is fed. `dataset/audit/` holds the
reviews the design went through before it ran.

Branch `pilot-raw` keeps an earlier variant that fed raw mail straight into the inbox (three
consolidations over messages 1-300); it is the baseline for the capture step.

## Licence, ethics, citation

Code: MIT (`LICENSE`). Our own data (capture notes, distilled memory, ledger, run records):
CC BY 4.0. Message text comes from the CMU release, public since 2004; no further rights are
claimed over it. The people in it are real: health, family and personal contact details are
kept out of the distilled memory, and anyone who appears in the data can ask for a removal by
opening an issue.

Until the frozen release has its own DOI, cite the source corpus and the mechanism:
Klimt & Yang (2004), https://doi.org/10.1007/978-3-540-30115-8_22, and eleman,
https://doi.org/10.5281/zenodo.23975338. The rest of this repository is the eleman template
(`AGENTS.md`, `docs/`, `memory/rules`, `memory/tools`); eleman's own README is
`docs/eleman-README.md`.
