# enron-memory-replay

**An AI assistant's long-term memory, built week by week from one real mailbox, with every
intermediate layer kept.**

One Enron employee's email (the `kaminski-v` mailbox of the public CMU Enron corpus: 11,523
messages, 30 November 1999 to 3 February 2002) is replayed in the order it arrived into a
file-based agent memory ([eleman](https://doi.org/10.5281/zenodo.23975338): markdown files in git,
a raw layer and a distilled layer). Each message is turned into short notes by a model; once per
week of mail an unattended consolidation run distils the notes into the memory. The repository
holds every layer: the raw messages, the notes, the memory as it stood after each of the 122
consolidations (one git tag each), a ledger that says what happened to every message, and the
full transcript and cost of every model run.

It exists because work on agent memory needs a long, real, dated stream and a memory that really
lived through it, where every distilled fact can be traced to its source and every loss is
recorded. Synthetic dialogues do not give that; this is one such memory, built once, in the open.

Version 1.0.0. DOI: [10.5281/zenodo.24241955](https://doi.org/10.5281/zenodo.24241955) (all
versions; this version is 10.5281/zenodo.24241956). See [How to cite](#how-to-cite).

## In numbers

| | |
|---|---|
| Messages replayed | 11,523 (5,689 sent by the mailbox owner, 5,834 received; 635 tagged bulk) |
| Period | 1999-11-30 to 2002-02-03, 114 ISO weeks, 122 consolidation slices |
| Capture verdicts | 8,250 durable (notes written), 3,273 not durable |
| Fate of the durable messages | 7,951 kept in memory in the week they arrived, 299 dropped (3.6%), each with a class and a reason; 0 lost silently |
| Memory at the end (`sleep-122`) | 224 topic files, 776 people files, about 934,000 characters; 2,147 archive files of fact lines moved out of topics verbatim |
| Model work at list price | $242 capture + $466 consolidation (21.7 hours of consolidation wall time) |
| Model | Claude Opus 5.5 for every model call |

## What is inside

| Layer | Path | What it is |
|---|---|---|
| Stream | `dataset/manifest.csv` | One row per message, in replay order: `seq`, `id` (`m00001`...), source path in the CMU release, SHA-256 of the original bytes, dates (header, local, UTC), direction, bulk class, sizes, quote pointers, same-body link, thread id (approximate), duplicate copies. |
| Slices | `dataset/slices.csv` | The 122 slices: ISO week, first and last message, and `today`, the simulated date of that consolidation. |
| L2, raw | `memory/archive/mail/YYYY/m<seq>.md` | Every message verbatim (headers and body, uncapped) with a small frontmatter. 26 messages without a usable date are in `memory/archive/mail/unplaced/`. |
| Capture | `dataset/capture/s<slice>.jsonl` | One record per message: durable or not (with a reason), up to five notes, the model's full response, token usage, cost. |
| Inbox as fed | `memory/archive/inbox/<day>--mail.md` | The notes as the memory received them, one block per message, one file per day. |
| L1, distilled | `memory/domains/<domain>/`, `memory/people/`, `memory/state.md`, `memory/questions.md` | The memory. Each fact line is dated and ends with a link to its source message: `- [2000-11-06] ... ←[[m04019]]`. |
| Archive of L1 | `memory/archive/<domain>/YYYY/` | Fact lines moved out of over-budget topic files, verbatim, still citing their messages. |
| Snapshots | git tags `sleep-001` ... `sleep-122` | The whole repository as it stood after each consolidation. A tag never contains mail or notes from a later week. |
| Ledger | `dataset/ledger/sleep-<kkk>.tsv` | For every message of the slice: `kept` (and the files citing it), `dropped`, or `not_durable` (and the reason). |
| Drops | `dataset/drops/sleep-<kkk>.tsv` | Written by the consolidation model: each message with notes it chose not to keep, with a class (`redundant`, `logistics`, `social`, `no_owner_content`, `other`) and a reason. |
| Runs | `dataset/runs/sleep-<kkk>.json`, `.transcript.jsonl.gz` | Per consolidation: gates, sizes, tokens, cost, wall time, and the complete tool-by-tool transcript. |
| Method | `dataset/DESIGN.md`, `dataset/SOURCE.md`, `dataset/tools/` | The full description of the pipeline, the source and mailbox choice, and the code that ran. |
| Reviews | `dataset/audit/`, `dataset/validation/` | The dated design decisions and run reviews, and the model comparisons made before the run. |

Everything else (`AGENTS.md`, `CLAUDE.md`, `INSTALL.md`, `CONTRIBUTING.md`, `docs/`, `setup/`,
`memory/rules/`, `memory/tools/`, `.claude/`) is the eleman template at commit `66bd1af`, the
memory mechanism the replay ran on. It is kept unchanged, apart from the deviations listed in
`dataset/DESIGN.md`, because the consolidation runs read these files; it is not dataset content.
Those files describe eleman, not this dataset.

## What you can study with it

- Question answering against a memory as it stood on a given date.
- How facts are updated, superseded and forgotten over two years.
- Consolidation loss: what a model keeps, drops and compresses, message by message.
- Retrieval over distilled memory (L1) against retrieval over the raw archive (L2).
- Re-consolidation: the notes are frozen, so the weekly runs can be repeated with another model
  or another memory design on identical input and compared with this one.
- Growth of a long-lived memory under size budgets; person and alias resolution.

The dataset ships no question set and no recall measurement of its own.

## How the data was prepared

`dataset/DESIGN.md` is the complete description; this is the same process in order. Only steps 4
and 7 call a model. Every other step is deterministic Python (standard library only) and gives
byte-identical output when run twice.

1. **Source.** The CMU release of 7 May 2015, `enron_mail_20150507.tar.gz` (443,254,787 bytes,
   SHA-256 `b3da1b3fe0369ec3140bb4fbce94702c33b7da810ec15d718b3fadf5cd748ca7`).
   `build_stream.py` reads the tarball directly and refuses a file with any other checksum.

2. **Choosing the mailbox.** The rule was fixed before any content was read: at least 3,000
   unique messages, at least 25% sent by the owner, at least 24 months, and among those the
   largest mailbox under 15,000 unique messages. 15 of the 150 mailboxes qualify
   (`dataset/mailbox-stats.csv`); the rule selects `kaminski-v` (`dataset/SOURCE.md`).

3. **Building the stream** (`build_stream.py`). The mailbox has 28,465 files. Copies of one
   message in several folders are merged (every copy's path stays in the manifest), giving 11,523
   unique messages ordered by UTC time. 26 messages whose Date header cannot be placed (a 1979
   placeholder, one dated 2005) are set aside and not replayed. Bytes are decoded as Windows-1252
   and line endings normalised; nothing else is changed. The owner's eight addresses come from a
   hand-checked list, which decides `sent` or `received`.

4. **Describing the stream** (`preprocess.py`, no model). For each message: which earlier
   messages it quotes (line-level matching: a line counts when it has at least 30 characters, at
   least 15 letters or digits, is not a header line, and was seen in an earlier message; a source
   counts when at least three of its lines recur), an identical-body link, a `bulk` tag (automated
   sender or more than 20 recipients), and an approximate thread id. 23.5% of all body characters
   repeat earlier messages; 4,156 messages quote at least one. The step also makes each message's
   "new text" view, with quoted runs replaced by `[quoted from m<seq>, k lines]`. That view is
   input to the next step only; L2 keeps the full text.

5. **Capture** (`capture.py`, one model call per message). The model sees one message: headers,
   new text, and up to three of the earlier messages it quotes. It sees no memory and no later
   mail, so capturing the whole mailbox in advance cannot leak the future into any snapshot. It
   answers in JSON: durable or not, a reason class when not, and up to five short notes. A note
   that reports the owner's own words carries a verbatim quote; the code checks that the quote is
   a substring of the message and drops the note if it is not (116 notes in 94 messages). A
   "quote only" or "empty" verdict on more than 500 new characters is asked once more, and both
   answers are stored. Prompt version `capture-v3`; the prompt text is in `capture.py`.

6. **Slicing and feeding** (`slices.py`, `feed.py`). One slice per ISO week; a week with more
   than 200 messages is split evenly (largest slice: 194 messages). The simulated date of a slice
   is the date of its last message. Feeding a slice writes its raw messages to L2, its notes to
   the inbox (one block per message; a not-durable message gets its header line and reason only),
   and its capture records to `dataset/capture/`, in one commit.

7. **Consolidation** (`run.sh`, one unattended model run per slice). The model receives eleman's
   own consolidation prompt plus a replay preamble (full text in `run.sh`): the simulated date;
   notes are model inference and quoted owner words are the owner's statement; every fact line
   ends with `←[[m<seq>]]` and is dated by its source message; every person named in five or more
   noted messages gets a people file; a topic file is a standing subject, never a period of time;
   every message with notes that is not kept must be listed in the drops file with a class and a
   reason. The model works with the harness's file and shell tools inside the repository, follows
   eleman's rules (`AGENTS.md`, `memory/rules/`), and commits once. Nobody answers the questions
   it raises; they close by status quo.

8. **Gates, checked from outside after every slice** (`run.sh`, `ledger.py`, `date_leaks.py`).
   The run exited cleanly and committed; every fed inbox file was consumed and the tree is clean;
   eleman's `lint.py` and `sleep-audit.py` are green on the run's own commit; no date from the
   real clock appears in the memory; and every durable message is either cited by an L1 fact or
   listed as dropped, with no fact citing a later message. One repair turn is allowed and
   recorded. Only then is the slice recorded, tagged `sleep-<kkk>` and the next one fed.

9. **Ledger.** `ledger.py` derives the ledger from the citation links and the drops file; the
   model does not write it. "Kept" means cited in L1 in the week of the slice. A kept message can
   later leave L1 when its fact lines move to `memory/archive/<domain>/`; at `sleep-120`, 48% of
   the messages kept so far were still cited in L1 and the rest from the archive.

10. **Reviews and reruns.** The run paused after slices 30, 60, 90 and 120 for a review by a
    separate model instance, each checked against the data (`dataset/audit/`). The reviews led to
    three declared changes: the people-index size budget was raised from slice 31, the domain-index
    budget from slice 61, and slices 77 to 90 were run a second time with the "standing subject"
    paragraph added to the preamble, because the first pass had started to file facts by week
    instead of by subject. The first pass is kept in the history (tags `drift-077` to
    `drift-090`). Two slices (67, 89) were rerun on the same feed after the run reset its own
    pass, and one (71) was fed again after the run was cut off from outside; the first attempts
    are kept as `sleep-<kkk>.attempt1.*`.

**Model and settings.** Every model call uses Claude Opus 5.5 (`claude-opus-5-5`), effort `high`,
through Claude Code 2.1.323 (`claude -p`, a pinned copy with auto-update off).

| Role | Call |
|---|---|
| Capture | Claude Code's system prompt replaced by the capture prompt, no tools, one turn, run from an empty directory |
| Consolidation and repair turn | eleman's consolidation prompt plus the replay preamble, Claude Code's own tools, permissions bypassed, project settings only, no MCP servers |

Model output is not reproducible call for call, so every response is stored: the dataset can be
checked from the repository without calling a model. Before the run, cheaper models were compared
with Opus on a sample (`dataset/validation/`, `dataset/audit/2026-11-13-4-pilot-review.md`).

## How to use it

Clone with full history; the snapshots are git tags.

```bash
git clone https://github.com/akadal/enron-memory-replay
cd enron-memory-replay
```

**The memory as it stood on a date.** Find the last slice whose simulated date is not after your
date, then read that tag:

```bash
python -c "import csv; d='2001-08-15'; print(max(int(r['slice']) for r in csv.DictReader(open('dataset/slices.csv', encoding='utf-8')) if r['today'] <= d))"
# 93
git worktree add ../memory-at-093 sleep-093       # a second working copy at that snapshot
git show sleep-093:memory/state.md                # or read single files without checking out
git diff --stat sleep-092 sleep-093 -- memory/domains memory/people   # what one week changed
```

**A message, its notes and the facts that cite it.**

```bash
cat memory/archive/mail/2000/m04019.md                      # the raw message
grep '"id": "m04019"' dataset/capture/s050.jsonl            # its capture record
grep m04019 dataset/ledger/sleep-050.tsv                    # kept, dropped or not durable
git grep -n "m04019" sleep-050 -- memory/domains memory/people      # facts citing it that week
git grep -n "m04019" -- memory/domains memory/people memory/archive # where it is cited now
```

The manifest row of a message gives its slice through `dataset/slices.csv` (`first_seq` to
`last_seq`).

**Manifest and ledger in Python** (standard library):

```python
import csv, glob

manifest = {r["id"]: r for r in csv.DictReader(open("dataset/manifest.csv", encoding="utf-8"))}

ledger = {}
for path in sorted(glob.glob("dataset/ledger/sleep-[0-9][0-9][0-9].tsv")):
    for r in csv.DictReader(open(path, encoding="utf-8"), delimiter="\t"):
        ledger[r["id"]] = dict(r, slice=int(path[-7:-4]))

# 11,523 messages: 7,951 kept, 299 dropped, 3,273 not_durable
sent_dropped = [i for i, r in ledger.items()
                if r["status"] == "dropped" and manifest[i]["direction"] == "sent"]
```

Capture records are JSON lines (`json.loads` per line; the fields `durable`, `reason`, `notes`
are the parsed answer, `parts` holds the raw responses). Run records are JSON
(`dataset/runs/sleep-<kkk>.json`); `python dataset/tools/summary.py` prints one table over all of
them with cost recomputed from tokens.

**Rerun the consolidations with another model on the frozen notes.** The capture layer is the
fixed input; only L2 text has to be rebuilt from the source tarball, which is deterministic.

```bash
# 1. the source (443 MB), then the stream; the rebuilt manifest must equal the shipped one
#    (work files stay outside the repository: the runner refuses a tree with untracked files)
mkdir ../work
curl -o ../work/enron_mail_20150507.tar.gz https://www.cs.cmu.edu/~enron/enron_mail_20150507.tar.gz
python dataset/tools/build_stream.py build --tar ../work/enron_mail_20150507.tar.gz --owner kaminski-v --cache ../work --manifest ../work/stream.csv
python dataset/tools/preprocess.py --stream ../work/kaminski-v.jsonl --base-manifest ../work/stream.csv --out ../work/enriched.jsonl --manifest ../work/manifest.csv
cmp ../work/manifest.csv dataset/manifest.csv

# 2. the frozen capture records, in order
cat dataset/capture/s*.jsonl > ../work/captures.jsonl

# 3. a branch at the empty memory, with the final tools and budgets
git switch -c rerun replay-start
git checkout v1.0.0 -- dataset/tools memory/rules/format.md
git commit -m "rerun: final tools and budgets from slice 1"

# 4. run slices 1 to 122 with another model and its own tag prefix
MODEL=<model id> TAG_PREFIX=rerun- PY=python sh dataset/tools/run.sh ../work/enriched.jsonl ../work/captures.jsonl 1 122
```

`run.sh` is the runner as it ran: it drives Claude Code, refuses any version other than 2.1.323
(`CLAUDE_VERSION`), waits on a Claude subscription's quota, and pushes to `origin` after each
slice, so run it in your own fork. For another harness, replace its `harness()` function; the
feed, the gates and the ledger do not depend on the model. A rerun started this way applies the
final budgets and preamble from slice 1, which the original run reached in steps (step 10).

## Limitations and declared deviations

Short form; `dataset/DESIGN.md` has each one with its numbers.

- One mailbox, one model, one pass. Nothing here measures run-to-run variance.
- No question set and no recall measurement are included.
- The capture step decides what is durable. A message it judged not durable never reaches the
  consolidation; the gates only cover the 8,250 it passed on. Notes are model inference and can
  be wrong; only quoted owner words are verified.
- The run was unattended. Alias, merge and new-domain proposals were never approved, so the
  dataset has open alias questions, not a curated alias table, and a few recurring people have no
  people file.
- Budgets changed twice during the run (from slices 31 and 61) and the preamble once (second pass
  from slice 77). Slices 16 to 29 carry a thinner people index and slices 36 to 60 thinner domain
  indexes as a result.
- Topic files are small windows: most hold a few recent fact lines and a list of archive files.
  About half of the archived topic files are reachable only by their filename prefix.
- The harness offered a slightly different tool list before and after slice 71 (the runner was
  restarted from a terminal instead of the desktop application); the extra tools were never
  called, and each transcript's first event records the list.
- Each consolidation also received a 371-byte instruction file from a parent directory of the
  build machine, which only names `AGENTS.md` and `memory/MEMORY.md`; the files it imports were
  not loaded (`dataset/DESIGN.md`, "Consolidation").
- Threads and quote pointers in the manifest are approximate.
- Transcripts are stored as produced, except that three directory names of the build machine
  were replaced; commit hashes quoted inside transcripts and run records are those of the build
  history and are mapped to the published ones in `dataset/commit-map.tsv`.

## The data is used as it is, and it is about real people

The Enron mail was made public by the US Federal Energy Regulatory Commission in 2003 and has
been distributed for research by Carnegie Mellon University since 2004. It is used here exactly
as the CMU release of 2015 holds it: nothing is anonymised, redacted, corrected or filtered.
The messages name real people and include private matters and, in a few messages, login details,
as the public release does. The notes and the distilled memory are model-written statements
about those people and can be wrong. Use the dataset for research on memory systems, not to
learn about the individuals. To ask for the removal of content, open an issue on the repository;
a removal is published as a new version.

## Licence

- Code (`dataset/tools/` and the eleman template): MIT, see `LICENSE`.
- Data made for this dataset (manifest, capture records, inbox notes, distilled memory, ledger,
  drops, run records and transcripts, reviews): CC BY 4.0, see `LICENSE-DATA.md`.
- Message text (`memory/archive/mail/`, and quotations from it elsewhere) comes from the CMU
  release. No rights are claimed over it and the licences above do not cover it.

## How to cite

> Akadal, E. (2026). *enron-memory-replay: an agent memory replayed week by week through one
> mailbox of the Enron corpus* (Version 1.0.0) [Data set]. Zenodo.
> https://doi.org/10.5281/zenodo.24241955

`CITATION.cff` holds the same record. Please also cite the source corpus: Klimt, B., & Yang, Y.
(2004). The Enron Corpus: A New Dataset for Email Classification Research. *ECML 2004*.
https://doi.org/10.1007/978-3-540-30115-8_22. The memory mechanism is eleman,
https://doi.org/10.5281/zenodo.23975338.

The Zenodo record holds two files: the repository at `v1.0.0`, and a git bundle with the full
history and every tag (`git clone enron-memory-replay-1.0.0.bundle`), so the weekly snapshots are
part of the archived dataset.
