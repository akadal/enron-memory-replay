# Review after slice 090, second pass (2001-07-21), 2026-11-15

**Decision: CONTINUE.** No fix before slice 91. The Topics paragraph did its job, nothing is lost
or false, and its side effect is the budget working as designed. Three sentences for
`dataset/DESIGN.md` are at the end; none changes the pipeline.

## 3. Topics paragraph, against `drift-*` on the same feed

| slices 77-90 | second pass | first pass | 61-76 |
|---|---|---|---|
| new fact lines into existing topics, per slice | 36.8 | 13.1 | 40 |
| into new files / month- or week-named | 0.9 / 0.3 | 30.3 / 28.8 | 7 / 2 |
| lines moved verbatim to `archive/<domain>/2001/` | 513 | 140 | 38 per slice |
| lines rewritten in place, citations kept | 38 | 30 | 49 |
| lines or message ids lost | 0 | 0 | 0 |
| topic files at 090 (208 at 076) | 212 | 286 | |
| named by month / week | 36 / 0 | 75 / 32 | 34 / 0 |
| L1 growth per durable message | 58 chars | 220 | 101 |

- Four new topics: `rice-energy-derivatives-course`, `project-x-var-2001`, `poland-trip-jul-2001`,
  `california-trip-jul-2001`. The trips are events; the second also holds the family's move back
  to Houston (mild mis-home, no action).
- First-pass one-off subjects landed in standing topics (CrudeAPO in `monte-carlo-library`); the
  June storage fact m08491 is in `work/storage-model.md`.
- No squeezing: new fact lines average 276 characters (61-76: 280). Rewrites append a later
  clause and citation to an older line, as before.
- Side effect: topics are a sliding window. 152 of 212 are over the 1,600 target and take lines
  only by shedding. Topic fact lines 708 -> 688 while 954 messages were kept; topics with two
  facts or fewer 46 -> 56; kept messages still cited in L1 57% -> 52% (first pass 62%); of ids new
  at 77-80, 20-40% are in a topic five slices later (62-65: 40-49%). Archive-link chains take
  budget (fact share of topic text 0.57 -> 0.55); the runs shorten them themselves.
- Ratchet: one self-reset in 14 slices. Expect about two in 91-122 (estimate), $2 each.

## 1. Gates and ledger

- 14 of 14 green, 0 repair turns, 0 missing, 0 future citations, 0 date leaks. 975 durable: 954
  kept, 21 dropped (2.2%): logistics 9, other 6, no_owner_content 4, redundant 2. Date match
  2,087 of 2,139 fact lines.
- Six drops read against notes and raw mail (m07826, m07953, m08100, m08381, m08561, m08678):
  sound.
- Slice 89, attempt 1: audit red after its repair (`lacima-book-2000` +165, `people/ed-krapels`
  +213 against 150), reset, 0 commits; record sizes equal slice 88's except the fed mail; its
  commit adds three files under `dataset/`. Rerun: one commit, 17 kept; record, ledger and tag
  agree. The attempt's $1.99 is outside `summary.py`'s total, as designed.
- L2 mail trees of both passes are identical at 077, 083, 090.

## 2. Memory quality

- `var-credit-system-2001`, `people/glen-dixon`, `california-trip-jul-2001` against six messages
  (m08697, m08701, m08708, m08721, m08733, m08741): names, numbers, dates, owner quotes match.
- Topics max 2,412 of 2,800, none above 90%. Entities 685, max 1,324 of 1,600. Alias table
  13,093 of 25,000. `state.md` 691 of 800.
- All 136 senders with five or more durable messages resolve to a file, apart from the owner,
  bulk senders and the "Julie"/"Les" alias questions. Three people named in five or more noted
  messages have none (first pass made them at slice 79): Peter McNabb, Jeff Andrews, Michael
  Moore.

## 4. Carried over

- m07700: kept. `people/martin-jermakyan.md` says Jermakyan left TXU after three days.
- Indexes: `organization` 5,415 (first pass 5,600), `industry` 4,813, `work` 4,643 of 8,000.
  `organization` at 122: about 5,900 (estimate, 5,600-6,500). No raise.
- `work` index: bare names under one "Path:" line, 17 of 124 with a full path; unlisted still
  `vendor-reviews-nov-2000` and `1999-12-29-robert-lee-visit`. Declared, no action.
- Log file: all 128 fed files of 77-90 are byte-identical in `archive/inbox/`; every run logged
  to `<today>--run.md`. Slice 90 archived its own log in its own commit; harmless.

## 5. Capture

11,523 records, 0 errors; 77-90: 39 retried verdicts, 12 unverified notes dropped. Durable rate
82% (61-70), 69% (77-90), 86% (91-102), then 50% falling to 37% (103-122) as bulk mail reaches
30-48%. Slice 109: 18 durable of 103.

## 6. Cost and quota

- Second pass 77-90: $48.42, $3.46 per slice, $0.050 per durable message (first pass $42.65).
  Total on `main` $365.98. Fit 61-90: $2.11 + $0.020 per durable message; no trend with size.
- Meters: weekly 48% -> 53%; five-hour 58% -> 73%, reset, -> 26%.
- Slices 91-122 (2,782 messages, 1,436 durable), estimates: **$96 ($85-105), about five hours,
  weekly near 63%, at most one five-hour wait.**

## For DESIGN.md (documentation only)

1. Slice 89's attempt 1: the second ratchet self-reset, the first rerun by the runner itself.
2. From slice 77 a topic holds about three fact lines; older lines sit in
   `memory/archive/<domain>/YYYY/`, one file per topic and week.
3. McNabb, Andrews and Moore have no entity file in the second pass.

---

## Checked and applied by the main session, 2026-11-15

- Verified against the data: fact lines into existing topic files per slice in the second pass
  (between 11 and 56, about 37 on average) and new files (0-5 per slice), counted from the diffs
  between tags; topic files 208 at `sleep-076`, 212 at `sleep-090`, 286 at `drift-090`; the three
  missing entity files (present at `drift-090`, absent at `sleep-090`); slice 89's attempt-1
  commit touches only `dataset/` and its last audit pass names `lacima-book-2000` (+165) and
  `ed-krapels` (+213); the total of $365.98.
- Recounted: kept messages still cited in L1 are 3,186 of 5,628 (57%) at `sleep-076`, 3,367 of
  6,582 (51%) at `sleep-090` and 4,034 of 6,589 (61%) at `drift-090`; the review's 52% and 62%
  differ by one point.
- Applied: the three sentences, in `dataset/DESIGN.md` (slice 89 under "Reruns"; the sliding
  window and the missing entity files under "Second pass from slice 77"). No pipeline change.
