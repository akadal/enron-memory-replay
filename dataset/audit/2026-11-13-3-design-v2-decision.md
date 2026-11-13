# Design v2: a replayed-mailbox memory dataset

Decision record, 2026-11-13. Supersedes `dataset/PLAN.md` v2. Numbers are measured on
`kaminski-v.jsonl` unless marked "estimate".

## 1. Scope and identity

- **One mailbox in v1.0: `kaminski-v`**, full length (11,523 messages, 1999-11-30 to 2002-02-03).
  The selection rule in `SOURCE.md` stays as written. A second mailbox is v1.1 with the same
  pipeline (the rule's next pick is `jones-t`, 10,656 messages); it is not promised in v1.0.
- **Name: `enron-memory-replay`** (repository `akadal/enron-memory-replay`, renamed from
  `eleman-demo`). The name states source and method, not a paper and not a demo.
- **The citable object** is the frozen release, made of five layers that can each be used alone:
  1. the stream: `dataset/manifest.csv` (order, checksums, direction, thread, class, quote pointers);
  2. L2: every message verbatim in `memory/archive/mail/`;
  3. the capture layer: one model-written note record per message, with the full request and response;
  4. L1 snapshots: the distilled memory after each of about 122 weekly sleeps (git tags);
  5. the ledger and run records: which message ended in which L1 fact, tokens, cost, gates.
- **Tasks it supports:** question answering against memory at a given date; tracking of updated
  facts; measuring consolidation loss (layer 3 against layer 4); retrieval over L1 against L2;
  rerunning the sleeps with another model from the frozen capture layer; growth and compression
  over time; person and alias resolution.
- **Generic by construction:** nothing in the repository refers to a paper, and evaluation
  assets live in `eval/`, never in `memory/`.

Layout:

```
enron-memory-replay/
├── AGENTS.md, docs/, memory/rules, memory/tools    eleman, pinned
├── memory/                                         L1 + inbox + archive/mail (L2) + archive/inbox
├── dataset/  README, DATASHEET, SOURCE, DESIGN, manifest.csv
│   ├── tools/     build_stream, preprocess, capture, feed, run, ledger, summary
│   ├── capture/   <ISO-week>.jsonl, committed with that week's feed
│   ├── ledger/    sleep-kkk.tsv
│   ├── runs/      sleep-kkk.json + full stream-json transcript
│   └── audit/
└── eval/     recall-probe/, questions/, enronqa-join.csv
```

## 2. Pipeline

**S0. Stream (`build_stream.py`, exists).** Two fixes:
- Owner addresses: `vkaminski@aol.com` (251 messages) and `kaminski@enron.com` (250) are
  labelled "received" today. Verify by reading 20 of each, then add them to an explicit owner
  list in `SOURCE.md`. The 5% rule missed them.
- Drop the 6,000-character cap. It hides 2.70M of 20.66M characters (13%) in 560 messages.

**S1. Preprocess (Python, no model, adds manifest columns only).**
- `quoted_from`: line-level match against earlier messages in the stream (normalised lines of
  30+ characters). 32.8% of all characters are such repeats. Matching by marker is rejected:
  51.9% of characters sit below a reply or forward marker, and the difference is forwarded
  material never seen as its own message.
- `same_body_as`: 404 messages repeat another message's body.
- `class: bulk`: automated sender pattern (571 messages) or a received message with more than
  20 recipients (249).
- `thread_id`: normalised subject, participants and quote pointers (5,944 subject keys).
- All lossless: L2 keeps the verbatim message, these columns only describe it.

**S2. Capture (Haiku 5.5, OpenRouter, temperature 0, pinned model ID, 15 workers).**
- One call per message. Input: headers, the novel text in full (chunked when long), and the
  text behind its quote pointers as context only. The call sees no other message and no
  memory, so the whole mailbox can be captured upfront without leaking the future.
- Output (JSON): `durable: true|false`, a reason class when false, and up to five notes of
  about 600 characters in total. A note that states what the owner said carries a verbatim
  quote. Python checks that each quote is a substring of the message and drops the line if not.
- This mirrors real eleman capture in three ways I checked in the private deployment. The
  real mail tap writes only sender and subject with a `(from mail)` trace and no raw dump.
  Real inbox blocks are short (median about 680 characters, 90th percentile about 1,400, over
  161 recent blocks). The automatic session summary is written by a cheap model, tagged as
  automatic, ranked as model inference, and its owner quotes must exist verbatim in the source.
- Why OpenRouter: 11,523 small calls through `claude -p` would spend quota on start-up
  overhead. Why Haiku: the task is extraction from one message, and the recall probe (section 4)
  measures whether that was enough.

**S3. Feed (Python), one slice at a time.**
- Raw message, uncapped and verbatim, to `memory/archive/mail/YYYY/m<seq>.md` with path and
  SHA-256 in frontmatter. The file id `m<seq>` is the provenance target.
- Inbox: one file per day, one block per message, every message present:
  `(mail · sent|received · m<seq> · automatic capture)`, sender, subject, then the notes; a
  message with `durable: false` gets the header line and its reason class only.
- That slice's capture records are committed with the feed, so no tag contains the future.

**S4. Sleep (Sonnet 5.5, `claude -p`, subscription).**
- Cadence: ISO week, simulated today = the slice's last day, at most 200 messages per sleep.
  114 weeks become 122 sleeps (a 150 cap would give 134).
- Prompt: `sleep-run.sh` verbatim plus the replay preamble, with two added sentences: every
  L1 fact ends with `←[[m<seq>]]` (format.md already defines this link), and the run's log
  block lists each durable note it chose not to keep, with a reason class.
- Output saved as `stream-json`, so the tool trace of every sleep is part of the dataset.

**S5. Gates, from outside, after every sleep.**
- Existing: at least one commit, inbox empty, tree clean, `lint.py`, `sleep-audit.py --last`,
  `date_leaks.py`.
- New, coverage: every message of the slice with `durable: true` is either cited by an L1
  fact or listed as dropped. `ledger.py` derives the ledger from the links; the model does not
  write it. One automatic repair turn naming the missing ids is allowed and recorded; a second
  failure stops the run.
- New, provenance: every `m<seq>` cited exists and is not later than simulated today.

**S6. Record.** `runs/sleep-kkk.json` as now, plus kept-rate by position decile within the
slice and by slice size. A kept-rate that falls toward the end of a slice is skimming; the
dataset reports the curve, whatever it shows.

## 3. The current repository

- `main` and `pilot-raw` are the same three raw sleeps. Keep `pilot-raw`, rename its tags to
  `pilot-raw-01..03`, and say in the README that it is the raw-inbox baseline over messages 1-300.
- Restart `main` from the setup commit (`40b3da3`) with a force-push, then re-pin eleman to
  `66bd1af`, which fixes the `questions.md` cap the pilot patched by hand. The repository is
  one day old and nothing depends on it. If the owner refuses a force-push, the fallback is one
  commit that restores the setup tree; it works but leaves pilot commits in the memory's history.
- Rename the repository at the same moment (GitHub redirects the old URL).

## 4. Evaluation assets in v1.0

- **Recall probe.** 500 messages, stratified by direction, bulk class, length and quarter.
  Sonnet reads the raw message and lists its durable facts; a judge checks each against L1 at
  the tag of the sleep that consumed it. Shipped: sample, facts, judgments, recall with a
  confidence interval, and 50 judgments checked by hand. This is the evidence for the
  "no silent loss" claim, with the coverage gate.
- **EnronQA join.** `eval/enronqa-join.csv` maps our `seq` to the CMU `path`, plus a loader
  that downloads EnronQA from Hugging Face. The questions are not redistributed: the licence
  is undeclared. How many EnronQA records `kaminski-v` has is not verified yet.
- **Temporal and update questions.** 120 in total: 60 "what was true on date D" and 60 "what
  changed between D1 and D2". Written from L2 by a model that never saw L1, each with its
  supporting `m<seq>` ids and validity dates; a script checks ids and dates; 30 are checked by hand.
- **Time split.** Questions with D before 2001-07-01 are development, the rest are test.
  24.8% of messages (2,862) fall in the test period. The memory itself is built over the whole
  stream; the split applies to questions only, and is fixed before anyone reads L1.

## 5. Freezing

- Tag `v1.0.0`, then a manual Zenodo deposit. The GitHub integration alone archives a source
  zip without history, which would lose the per-sleep snapshots. Deposit three files: the
  source zip, a `git bundle` with all tags, and `l1-snapshots.tar.gz` (L1 at every sleep).
- Concept DOI plus version DOI. `CITATION.cff` cites the dataset; references are Klimt & Yang
  (2004) and the eleman software DOI (10.5281/zenodo.23975338).
- Licence: code MIT; capture notes, L1, ledger, run records and `eval/` CC BY 4.0; message
  text keeps the status of the CMU release, no rights claimed.
- `DATASHEET.md` (Gebru et al.) states: real named people; model-written notes can be wrong
  about them (quotes are verified, paraphrase is not); private matters appear in the mailbox;
  the unattended mode (nobody answers `questions.md`).
- Removal requests: an issue or an email address; a removal makes a new version, because the
  layers are append-only and DOI versions are immutable.
- Versioning: 1.0.x for documentation and evaluation fixes; 1.1 for a second mailbox; 2.0 if
  the memory itself is rebuilt.

## 6. Cost, time, order of work

| Part | Where | Cost | Wall time |
|---|---|---|---|
| Capture, 11,523 calls | OpenRouter, Haiku 5.5 | $2-3 (estimate) | under 30 min |
| 122 sleeps | subscription, Sonnet 5.5 | $1-2.5 each, $150-300 list-equivalent (estimate) | 10-17 machine hours |
| Recall probe | OpenRouter, Sonnet 5.5 | $5-10 (estimate) | under 1 hour |
| 120 questions | OpenRouter, Sonnet 5.5 | $5-10 (estimate) | under 1 hour |

OpenRouter total: under $30 (estimate). Quota: the pilot moved the weekly meter 0-1 point per
sleep, so 122 sleeps need 60-120 points, two to three quota weeks (estimate). Milestone M4
replaces these estimates with a measured slope. Sleeps are sequential; everything else can
run in parallel.

Milestones, each verifiable alone:

- **M0** Owner decisions (section 7). Rename, reset `main`, re-pin eleman.
- **M1** S0 and S1: owner list fixed, cap gone, four manifest columns. Check: the stream
  builds byte-identical twice; sent share rises from 45.0% to about 49%; the measured numbers
  above reproduce. Also confirm lint accepts `archive/mail/YYYY/` and the `←[[m<seq>]]` link.
- **M2** Capture on messages 1-300. Check: 300 of 300 records, zero unverified quotes kept,
  20 notes read by hand against their messages.
- **M3** Full capture into the local cache. Check: 11,523 of 11,523; cost recorded.
- **M4** Ten sleeps with all gates. Check: ten green, coverage gate exercised at least once,
  cost slope fitted, L1 budgets hold with provenance links. Go or no-go for the full run.
- **M5** Full run in quota-sized stretches, resumable at any sleep.
- **M6** Recall probe and the 120 questions; EnronQA join.
- **M7** Datasheet, README, `CITATION.cff`; an adversarial review of the frozen candidate.
- **M8** Tag, bundle, Zenodo deposit.

## 7. Decisions only the owner can make

1. Rename to `enron-memory-replay` and force-push `main` back to the setup commit.
2. Budget: an OpenRouter ceiling of $40, and how much of each week's quota the sleeps may take.
3. One mailbox for v1.0, the second deferred to v1.1.
4. Publishing model-written notes and private-life content about named real people under CC BY 4.0.
5. About two hours of his own reading for the hand checks (50 probe judgments, 30 questions),
   or delegating them and saying so in the datasheet.
6. Title, author list and affiliation on the Zenodo record, and the moment of the deposit:
   a DOI version cannot be withdrawn quietly.
