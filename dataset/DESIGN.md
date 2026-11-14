# Design

How the dataset is built, stage by stage, and every way it departs from eleman as shipped. The
reasoning behind the choices is in `dataset/audit/` (a plan review, a design consultation and the
decision record); this file is the description of what actually runs.

## Pipeline

| Stage | Tool | Model | Output |
|---|---|---|---|
| S0 stream | `build_stream.py` | none | one mailbox from the checksummed tarball, de-duplicated across folders, ordered by UTC instant, messages without a placeable date set aside; owner addresses from a hand-checked list |
| S1 describe | `preprocess.py` | none | `dataset/manifest.csv`: id, direction, bulk class, quote pointers, same-body links, thread; for each message its new text, with repeated runs replaced by `[quoted from m<seq>, k lines]` |
| S2 capture | `capture.py` | Claude Opus 5.5, effort high (`claude -p`, Claude Code 2.1.323, capture prompt as system prompt, no tools), prompt `capture-v3` | one stateless call per message: durable or not (with a reason class), up to five notes; owner quotes verified as verbatim substrings; one recorded retry for a "quote_only" or "empty" verdict on more than 500 new characters |
| S3 slice | `slices.py` | none | `dataset/slices.csv`: one slice per ISO week, weeks above 200 messages split; simulated today = last message's date |
| S4 feed | `feed.py` | none | per slice: L2 files, inbox notes, capture records, one commit |
| S5 consolidate | `run.sh` | Claude Opus 5.5, effort high (`claude -p`, Claude Code 2.1.323 pinned, auto-update off) | eleman's own sleep prompt plus the replay preamble; one commit per slice |
| S6 check | `run.sh`, `ledger.py`, `date_leaks.py` | none | gates from outside; ledger; record; tag `sleep-<kkk>` |

Steps S0-S3 are deterministic: run twice, byte-identical output. S2 and S5 are model calls and
are not; their every response is stored, so the dataset is reproducible from the repository even
though a rerun of the models would differ.

## Describing the stream (S1)

A line counts as quoted when its normalised form has at least 30 characters, at least 15 letters
or digits, is not a header line (To:, Cc:, From:, Subject:, Date:, Sent: ...), and was first seen
in an earlier message; an earlier message counts as quoted only when at least three of its lines
recur. Threads join two messages on a shared subject only when they also share a participant
other than the owner, and on quote pointers only between non-bulk messages. Threads are an
approximate convenience: the largest has 193 messages. The first version of these rules had no
header, letter or three-line condition and made one early message the "source" of 1,287 others
(`dataset/audit/2026-11-13-4-pilot-review.md`).

## Capture (S2)

Real eleman inboxes hold short notes written as things happen; long raw material goes to the
archive. The capture step reproduces that: one call per message, seeing the message's new text,
its headers, and up to three of the earlier messages it quotes as context, and nothing else (no
memory, no later mail), so capturing the whole mailbox upfront cannot leak the future into any
snapshot. Text that is still in the new-text view is new to the memory, even under a "Forwarded
by" banner; "quote_only" is meant for a message that holds nothing but quote markers. Prompt v2
let a forwarded memo of the owner's pass as quote_only; the v3 wording and a guard that asks once
more are the fix. Requests are reproducible from `capture.py`, its `PROMPT_VERSION` and the
manifest (their SHA-256 is stored); responses, including a first verdict that was retried, are
stored verbatim with token usage and cost.

Known limitation: the verbatim check on owner quotes is a plain substring test against the raw
text, so a quote the model joined across a quoted-printable line break fails it and the note is
dropped (`unverified_dropped` in the capture record). Over the whole stream that is 116 notes in
94 messages; two messages lost every note and were recorded as not durable (m00369, m05777; the
substance of m00369 reached L1 through m00370). They were not re-captured.

## Consolidation (S5)

The prompt is `memory/tools/sleep-run.sh`'s, read at run time, with a preamble (the exact text
is in `run.sh`) that adds: the simulated date; that notes are model inference and quoted owner
words are the owner's own statement; that every fact line ends with `←[[m<seq>]]` and is dated by
its source message; that the run lists in `dataset/drops/sleep-<kkk>.tsv` every message with notes
it chose not to keep, with a class (redundant, logistics, social, no_owner_content, other) and a
reason; and that it commits but does not push.

The preamble also asks for an entity file for every person who appears in five or more messages
with notes, from the consolidation in which the fifth arrives. Without it, Opus kept people inside
topic files: after ten weeks 15 people seen in five or more messages had no entity file
(`dataset/audit/2026-11-13-5-checks-a-and-b.md`).

Unattended, nobody approves an alias, an entity merge or a new domain (eleman's approval gates):
those proposals stay in `questions.md` and close by status quo. The dataset therefore offers alias
questions, not a curated alias table.

## Gates (S6), checked from outside after every slice

1. The harness exited 0 and committed at least once.
2. Every inbox file the feed wrote was consumed; the tree is clean. A fed file counts as
   unconsumed while it still holds mail blocks, not merely because a file of that name exists: a
   run may log its own work (a question closed by status quo, say) in the inbox file of the
   simulated day, which has the fed file's name. Slice 12 stopped on that before the rule was
   changed and carries a note in `sleep-012.json`; since then the runs log to
   `<day>--mail-2.md` (17 such files by slice 30), consumed by the next sleep like any inbox file.
3. `lint.py` green; `sleep-audit.py --last <the run's commit>` green.
4. `date_leaks.py`: no date more than a year outside [first message, simulated today].
5. `ledger.py`: every message the capture step marked durable is either cited by an L1 fact or
   listed as dropped (no silent loss), and no fact cites a later message. One repair turn is
   allowed and recorded; a second failure stops the run.
6. Quota: when the subscription's weekly meter is at 90% or more the runner waits for the weekly
   reset, and when the five-hour window is at 90% or more it waits for that to refill; a slice
   whose capture records are not written yet is waited for as well. Waiting changes nothing in
   the data; it only spreads the run over more days.
7. The harness is Claude Code 2.1.323; the runner refuses any other version.

The ledger also records the kept rate excluding drops classed as redundant, the classes of the
drops, and the ids whose fact lines carry a bracket date different from their source message.
"Kept" is measured in the week of the slice: a message kept then may later leave L1 when its topic
is retired to `memory/archive/<domain>/`, which is eleman's way of forgetting. At slice 30, 1,169
of the 1,605 messages kept so far were still cited in `memory/domains/` or `memory/people/`.

Reruns. When a run finds its own pass failing a gate and, as eleman's rules require, resets to
`pre-sleep` and commits nothing, the slice is run once more on the same committed feed (`RERUN` in
`run.sh`). The first attempt's record, transcript and ledger stay in the repository as
`sleep-<kkk>.attempt1.*`; `summary.py` does not count them. This happened once, at slice 67: in
the first attempt the second `sleep-audit.py` pass was red because `work/dabhol-power-sale.md`,
already over its target, grew by 152 characters where the ratchet check allows 150, so the run
reset itself (list-price cost about $4.1).

`sleep-audit.py`'s FABRICATION check exempts lines carrying `←[[...]]`, which here is every
fact; gate 5 and the ledger's date-match metric (bracket date equals the cited message's date)
take its place.

## Deviations from eleman as shipped

eleman is pinned at `66bd1af`. Everything below differs on purpose, and nothing else does.

- Root `README.md` and `CITATION.cff` describe the dataset; eleman's are in `docs/`.
- `people_index` budget raised from [2300, 2900] to [5000, 6500] characters, and the domain
  `index` budget from [1600, 2000] to [3200, 4000]: after ten of 122 weeks two indexes stood at 89%
  of the shipped ceiling.
- From slice 31 on, `people_index` raised again, to [20000, 25000]. The entity-file sentence
  makes the alias table grow with every person who reaches five messages, and the budget did not:
  from slice 15 to 29 the table stayed within 10% of the 6,500 ceiling, and to fit it the runs
  dropped the domains column, then aliases (slices 16-29), then at slice 30 the file id, keeping one
  line per person (202 people, 4,356 characters; every name still maps to its file). The model
  asked twice in `questions.md` for a higher budget; nobody answers, so both closed by status quo.
  At 7.5 new entity files per slice (slices 10-30) the 6,500 ceiling would hold about 300 people,
  reached near slice 43; a linear projection gives about 900 people, about 19,000 characters, by
  slice 122. The new target sits above that so the number changes once. Slices 16-29 therefore
  carry a thinner alias table; that is a record of the old budget, not an error
  (`dataset/audit/2026-11-14-6-review-030.md`). After the raise the table kept its one-line form
  (459 people at slice 60, every name mapping to its file).
- From slice 61 on, the domain `index` budget raised again, to [6400, 8000]. In 60 slices the runs
  retired no topic file (no deletion, no rename) and met the ceiling by shortening the index
  instead: `work` lost its descriptions at slice 36 and its paths at slice 38 and lists 104 topics
  as bare names; `organization` and `industry` stood at 93% and 91% of the ceiling at slice 60,
  about to be stripped the same way. No fact was lost: every fact line that left L1 moved verbatim
  to `memory/archive/<domain>/` or was rewritten in place with its citation, except one citation
  (m02565) dropped at slice 36 from a line that survives with its other sources. One active topic,
  `work/vendor-reviews-nov-2000`, was listed only under "Hot" and dropped out of the index at
  slice 56; the file and its citations are intact, only its route is missing. Projected to
  slice 122, the largest index needs about 6,500 characters with descriptions
  (`dataset/audit/2026-11-14-7-review-060.md`).
- The preamble's entity-file sentence (above).
- Raw mail lives in `memory/archive/mail/YYYY/`, a source segment like `archive/inbox/`, not a
  domain segment.
- The replay preamble above; the `pre-sleep` checkpoint is set by the runner; the lock commit of
  `sleep-run.sh` is skipped (one machine); the runner, not the model, pushes.
- Nobody answers `questions.md`: approval items pile up and close by status quo when due.
- `python3` is a shim to `python` on the Windows machine that runs it.

## The data is not altered

Nothing in the mail is anonymised, redacted, corrected or filtered: the corpus has been public
for two decades and is used as the CMU release holds it. Concretely:

- L2 stores each source file whole, headers and body, decoded from Windows-1252 (zero bytes
  needed a replacement character) with line endings normalised; `raw_sha256` is the checksum of
  the original bytes.
- No body is capped. Long messages are split into parts for the capture call only.
- Quote pointers and the "new text" view exist only as input to the capture step; L2 keeps the
  quoted text where it was.
- Duplicate copies of one message across folders are replayed once; every copy's path is listed
  in the manifest (`alias_paths`).
- 26 messages carry no placeable date (25 with the 1979 placeholder, one dated 2005). They are not
  replayed, because there is no week in which the owner could have received them, and are kept
  verbatim in `memory/archive/mail/unplaced/`.
- Neither the capture prompt nor the consolidation preamble asks the models to leave anything
  out on grounds of privacy. On its own, the consolidation model dropped three messages that carry
  passwords or login details (m04445, m04462, m04604; class `other`, "credentials deliberately not
  kept"). They are recorded as drops, and the messages are whole in L2.

## Model choice and controls

Each role uses one model throughout (README, "Models"), measured against Claude Opus 5.5, the
model the reference deployment of eleman runs on (`dataset/validation/`):

- **Capture: Claude Opus 5.5.** On 96 stratified pilot messages, judged blind both ways, Claude
  Haiku 5.5 and Opus each miss about a third of the other's facts (after prompt v3: Haiku 73% of
  Opus's, Opus 61% of Haiku's), and DeepSeek V4 Pro reached 41% of Opus's facts. Haiku would have
  done; Opus was chosen so that one model does all model work in the dataset, which makes it
  simpler to describe and to reuse. On a subscription the price difference is quota, not money:
  a measured $0.018 list-equivalent per capture call.
- **Consolidation: Claude Opus 5.5.** On pilot slices 1-3 (branch `control-opus`) Opus kept every
  durable message, wrote standing topics instead of dated one-off files, stayed inside every
  budget, and cost 1.19 times Sonnet 5.5 with a third of the turns (review in
  `dataset/audit/2026-11-13-4-pilot-review.md`).

## Pilots kept as records

| Branch | What it is |
|---|---|
| `pilot-raw` (tags `pilot-raw-01..03`) | raw mail fed straight into the inbox, 100 messages per consolidation, Sonnet 5.5 |
| `pilot-v2` (tags `pilot-v2-001..007`) | the capture pipeline before the stream and prompt fixes, weekly slices 1-7, Sonnet 5.5, Claude Code 2.1.263 |
| `control-opus` (tags `control-opus-001..003`) | slices 1-3 of `pilot-v2`'s feed consolidated by Opus 5.5 |
| `pilot-v3` (tags `pilot-v3-001..010`) | the corrected pipeline with Haiku capture and Opus consolidation, slices 1-10; checks A and B ran on it |

`main` was restarted from the setup commit after the review; its slices are the dataset.

## Run plan

Checks A and B (`dataset/audit/2026-11-13-5-checks-a-and-b.md`) settled the pipeline; the
three changes they led to (Opus capture, the entity sentence, the index budget) start `main` from
slice 1 again. The capture step runs ahead over the whole mailbox while the weekly
consolidations follow, each waiting for its slice's records; the run waits out quota windows and
is resumable at any slice. A review of the first thirty slices decides whether anything changes
before the rest.
