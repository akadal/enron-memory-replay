# Pilot review: go/no-go, 2026-11-13

**Decision: RESTART `main` from the setup commit, after two fixes in the deterministic layer and
one in the capture prompt. Capture: Haiku 5.5. Consolidation: Opus 5.5. One short check first;
if it passes, its ten slices are the first ten of the dataset.**

Everything below was checked in the repository, `D:\data\enron-work\` and the control clone.

## 1. Restart, not continue

Three independent reasons, any one sufficient:

- **The quote pointers and threads in the manifest are wrong.** `preprocess.py` treats any single
  line of 30+ characters seen before as a quote. Lines such as `to: vince j kaminski/hou/ect@ect`
  (1,437 hits) and separator rules match. Measured on `enriched.jsonl`: 17,405 of 25,115 pointers
  (69%) rest on fewer than 3 matched lines; 3,307 messages have only such pointers; `m00002` is
  "quoted" by 1,287 messages; **thread `t00002` holds 8,339 of 11,523 messages (72%)**. The
  manifest is layer 1 of the citable object, and these pointers pick the context shown to the
  capture model. Fixing it changes capture input, so everything downstream is rebuilt.
- **Capture loses forwarded content** (section 2).
- **Harness:** one CLI version for the whole dataset (2.1.323; 2.1.263 cannot run Opus and
  mispriced Sonnet).

Keep the current `main` as branch `pilot-v2` with tags `pilot-v2-001..007`, and `control-opus`
as it is; both are pilot records, like `pilot-raw`.

## 2. Capture model: Haiku 5.5, prompt v3

The control does not justify a 20-40x model: mutual recall is symmetric (69% / 61%), and the
"unsupported" flags I read are mostly judge quibbles on both sides ("HP" brand, "Enron
Building"), not fabrication.

The real defect is the durable verdict, which the control README understates. From the capture
records themselves (not the judge): Haiku durable 45/96, Opus 52/96; **Haiku says not-durable
where Opus says durable in 8 messages, the reverse in 1.** Five of the 8 are `quote_only`. Example:
`m00125`, the owner's own memo saying responsibility for model validation at Enron is dispersed
and Research does not validate models (1,840 new characters, forwarded from his AOL account,
never seen as its own message). It is `not_durable / quote_only` in `ledger/sleep-005.tsv` and
absent from L1. Gate 5 cannot see this: it only covers messages capture marked durable. In
messages 1-1000, 86 are `quote_only`; 27 of them have more than 500 new characters, 12 more than
1,500.

Fix (prompt `capture-v3`): text that is still present in the new-text view has not been seen
before, even under a "Forwarded by" banner, and is captured; `quote_only` is allowed only when
nothing but `[quoted from ...]` markers and a few words remain. Deterministic guard in
`capture.py`: a `quote_only` or `empty` verdict with `novel_chars > 500` gets one recorded retry.

## 3. Consolidation model: Opus 5.5

Read at `sleep-003` vs `control-opus-003`, same 64 messages:

- **Coverage:** Opus cites 34/34 durable; Sonnet 32. Sonnet's two drops include `m00057`, dropped
  as "forwarded newspaper article", although it carries the owner's own stated view ("I agree
  completely with his points" on IMF policy), which Opus kept with the quote. In slice 6 Sonnet
  dropped `m00194` and `m00197`, both requests for the owner's comments, as "forward only".
  Roughly 3-4 of Sonnet's 34 drops are losses. They are judgement errors, not gate-gaming.
- **Compression:** eleman's rule says "compress as hard as you can". Opus: 37 fact lines, 17k
  chars, 0 L1 files over target. Sonnet: 64 lines, 15 files over target by slice 7. What Sonnet
  keeps extra is mostly narrative and logistics (how a visitor gets past reception).
  Names, dates, numbers and owner quotes are in both.
- **File structure:** Opus writes standing topics (`recruiting`, `research-group`,
  `conferences-2000`). Sonnet writes dated one-off files (`pending-replies-dec-1999`,
  `calendar-jan-2000` then `calendar-mid-jan-2000`, `1999-12-29-robert-lee-visit`): 86 files after
  349 messages. `work/_index.md` is at 1,713 of a 2,000-character hard ceiling after 3% of the
  mailbox, and Sonnet has already cut index lines to bare slugs to fit.
- **People:** Sonnet's 15 entity files at slice 3 are mostly one-mention stubs (300 characters
  restating one line), and it then nearly stopped: 15, 15, 15, 15, 17 over slices 3-7 while new
  correspondents kept arriving. That is an inconsistent policy, not better recall. Opus's 2 files
  are restraint, and every other person is named with role in a topic file. Open risk: Opus gave
  no entity file to Shanbhogue, Vernon or Krishnarao (3-4 messages each); three slices cannot show
  whether it adds them as they recur. Checked in section 6.
- **Cost:** $2.13 vs $1.79 (1.19x), a third of the turns, 0.6x the wall time. Opus is also the
  reference model, so the consolidation role needs no smaller-model control.

## 4. Budget (122 slices, mean 94 messages, about 60-65% durable)

Fitted on few points, so estimates:

- Sonnet pilot: about $0.45 + $0.016 per durable message. Opus control (3 points): about
  $0.50 + $0.012.
- Opus, average slice at pilot memory size: about $1.25. With an assumed 1.5-2x growth as memory
  fills: **$180-330 list price, central $250** (estimate). Wall time 8-12 hours (estimate).
- Capture: $5 (measured rate $0.43 per 1,000). Control rerun about $1.7.
- Quota: Sonnet moved the weekly meter 1 point for $5.73; Opus 0 points for $2.13; the five-hour
  meter about 1 point per two small slices. That gives **30-80 weekly points (estimate), at least
  two quota weeks** with the 80% stop and a 44% base.

The pilot supports: base and per-message cost up to 95k characters of L1 and 151-message slices.
It does not support: the slope against memory size, behaviour at any budget ceiling (none was
reached), repair-turn frequency (never fired), how Opus weighs on the weekly meter, or Opus on
slices above 64 messages.

## 5. Changes before the full run (smallest fix each)

1. `preprocess.py`: ignore header-like and separator lines (`to:/cc:/from:/subject:/date:/sent:`
   prefixes, fewer than 15 alphanumerics); a pointer and a thread join need 3+ matched lines from
   one source. Assert largest thread under 200 messages. Refresh the numbers in `SOURCE.md`.
2. `capture.py`: prompt v3 and the retry guard above.
3. `run.sh`: refuse to start unless `claude --version` equals the pinned 2.1.323; disable
   auto-update for the run; add a five-hour quota wait next to the weekly stop.
4. Preamble, drops: `id<TAB>class<TAB>reason`, class one of `redundant|logistics|social|
   no_owner_content|other`. No other preamble change.
5. `ledger.py` / record: report kept rate excluding `redundant` drops and list the ids whose
   bracket date differs from the source (7 of 194 at slice 7). Slice 7's decile curve
   (1.0, .56, .67, .38, 1.0, -, .29, .5, .6, .89) is not skimming: 20 of 24 drops are
   congratulation notes after the 11 January promotion memo, and the last decile is 0.89.
6. `summary.py`: add the Opus 5.5 price (the control prints $0.00).
7. Docs: models table and CLI version; capture-control README must report the 8:1 durable
   asymmetry instead of "does not lose information"; state that aliases are never approved in
   unattended mode, so alias questions, not an alias table, are what the dataset offers.

Slice cap 200 stays (151 ran clean). Gates stay.

## 6. One short check, two parts

**A. Capture (about $2.5 OpenRouter).** Rebuild the manifest, re-capture messages 1-1000 with v3,
rerun the Opus control on the same 96 and the judge both ways. Pass: Haiku-not-durable where
Opus-durable in at most 4 of 96 (now 8); at most 5 `quote_only` with over 500 new characters in
1-1000 (now 27), each read by hand; mutual recall within 10 points.

**B. Consolidation (about $10-12 list, estimate).** Restart `main`, Opus 5.5, CLI 2.1.323,
slices 1-10 (554 messages). Pass:
- ten green, at most one repair turn;
- no index over its ceiling, and no topic closed while its thread is still active in the next
  slice. If this fails, raise `index` to [3200, 4000] as a declared deviation and restart once;
- every person cited in 5 or more messages has an entity file. If not, add one preamble
  sentence with that threshold, declared as a deviation;
- weekly quota moves at most 12 points over the ten slices. If more, stop and report before the
  full run.

On pass, continue from slice 11 without another restart.
