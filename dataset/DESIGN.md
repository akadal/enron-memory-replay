# Design

How the dataset is built, stage by stage, and every way it departs from eleman as shipped. The
reasoning behind the choices is in `dataset/audit/` (a plan review, a design consultation and the
decision record); this file is the description of what actually runs.

## Pipeline

| Stage | Tool | Model | Output |
|---|---|---|---|
| S0 stream | `build_stream.py` | none | one mailbox from the checksummed tarball, de-duplicated across folders, impossible dates dropped, ordered by UTC instant; owner addresses from a hand-checked list |
| S1 describe | `preprocess.py` | none | `dataset/manifest.csv`: id, direction, bulk class, quote pointers, same-body links, thread; for each message its new text, with repeated runs replaced by `[quoted from m<seq>, k lines]` |
| S2 capture | `capture.py` | Claude Haiku 5.5 (OpenRouter) | one stateless call per message: durable or not (with a reason class), up to five notes; owner quotes verified as verbatim substrings |
| S3 slice | `slices.py` | none | `dataset/slices.csv`: one slice per ISO week, weeks above 200 messages split; simulated today = last message's date |
| S4 feed | `feed.py` | none | per slice: L2 files, inbox notes, capture records, one commit |
| S5 consolidate | `run.sh` | Claude Sonnet 5.5 (`claude -p`) | eleman's own sleep prompt plus the replay preamble; one commit per slice |
| S6 check | `run.sh`, `ledger.py`, `date_leaks.py` | none | gates from outside; ledger; record; tag `sleep-<kkk>` |

Steps S0-S3 are deterministic: run twice, byte-identical output. S2 and S5 are model calls and
are not; their every response is stored, so the dataset is reproducible from the repository even
though a rerun of the models would differ.

## Capture (S2)

Real eleman inboxes hold short notes written as things happen; long raw material goes to the
archive. The capture step reproduces that: one call per message, seeing the message's new text,
its headers, and up to three of the earlier messages it quotes as context, and nothing else (no
memory, no later mail), so capturing the whole mailbox upfront cannot leak the future into any
snapshot. Health, family and personal contact details are excluded at this step. Requests are
reproducible from `capture.py`, its `PROMPT_VERSION` and the manifest (their SHA-256 is stored);
responses are stored verbatim with token usage and cost.

## Consolidation (S5)

The prompt is `memory/tools/sleep-run.sh`'s, read at run time, with a preamble (the exact text
is in `run.sh`) that adds: the simulated date; that notes are model inference and quoted owner
words are the owner's own statement; that every fact line ends with `←[[m<seq>]]` and is dated by
its source message; that the run lists in `dataset/drops/sleep-<kkk>.tsv` every message with notes
it chose not to keep; that health, family and contact details are not distilled; and that it
commits but does not push.

## Gates (S6), checked from outside after every slice

1. The harness exited 0 and committed at least once.
2. Every inbox file the feed wrote was consumed; the tree is clean.
3. `lint.py` green; `sleep-audit.py --last <the run's commit>` green.
4. `date_leaks.py`: no date more than a year outside [first message, simulated today].
5. `ledger.py`: every message the capture step marked durable is either cited by an L1 fact or
   listed as dropped (no silent loss), and no fact cites a later message. One repair turn is
   allowed and recorded; a second failure stops the run.
6. The weekly subscription quota is below 80% before a slice starts.

`sleep-audit.py`'s FABRICATION check exempts lines carrying `←[[...]]`, which here is every
fact; gate 5 and the ledger's date-match metric (bracket date equals the cited message's date)
take its place.

## Deviations from eleman as shipped

eleman is pinned at `66bd1af`. Everything below differs on purpose, and nothing else does.

- Root `README.md` and `CITATION.cff` describe the dataset; eleman's are in `docs/`.
- `people_index` budget raised from [2300, 2900] to [5000, 6500] characters.
- Raw mail lives in `memory/archive/mail/YYYY/`, a source segment like `archive/inbox/`, not a
  domain segment.
- The replay preamble above; the `pre-sleep` checkpoint is set by the runner; the lock commit of
  `sleep-run.sh` is skipped (one machine); the runner, not the model, pushes.
- Nobody answers `questions.md`: approval items pile up and close by status quo when due.
- `python3` is a shim to `python` on the Windows machine that runs it.

## Pilot and go/no-go

The pilot feeds slices until at least three consolidations and at least 300 messages have run
(slices 1-7, 349 messages), then an independent review decides: continue, revise, or restart. The
full run proceeds in quota-sized stretches and is resumable at any slice.
