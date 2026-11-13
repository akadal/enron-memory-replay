# Capture control: the capture model against Claude Opus 5.5

Question: does the capture model the dataset uses (Claude Haiku 5.5) lose information that
Claude Opus 5.5, the model the reference deployment of eleman runs on, would have captured? A
third model, DeepSeek V4 Pro (`deepseek/deepseek-v4-pro-0813`), was measured the same way as an
open-weights alternative of the same tier as Opus.

The runs below used prompt `capture-v2` on the first stream description. Both were later found
to have a defect that hid forwarded text (`dataset/audit/2026-11-13-4-pilot-review.md`); the
control is repeated on the corrected pipeline (prompt `capture-v3`) before the dataset proceeds,
and its results will be added here.

## Method

- Sample: 96 of the 349 pilot messages (`sample.txt`), half sent by the owner, half received,
  spread over the four quartiles of new-text length; fixed seed.
- Each control model captured the sample with the identical prompt and input
  (`control-opus-capture.jsonl` $0.90, `control-deepseek-capture.jsonl` $0.37; the dataset's
  Haiku capture of these 96 cost about $0.04).
- A judge model (Claude Sonnet 5.5 via OpenRouter) read the complete source file of each message
  and two unlabelled note sets, A and B, and listed: facts in B missing from A, items in A the
  message does not support, and both durable verdicts. Each pair was judged twice with the sets
  swapped.

## Result

| | Haiku 5.5 | Opus 5.5 | DeepSeek V4 Pro |
|---|---|---|---|
| durable verdicts (of 96) | 45 | 52 | 50 |
| notes written | 120 | 123 | 112 |
| recall against Opus's facts | 69.3% | | 41.1% |
| Opus's recall against this model's facts | 60.6% | | 68.6% (59 of 96 judged) |
| items flagged unsupported | 35 | 25 (vs Haiku), 21 (vs DeepSeek, partial) | 7 |
| not durable where Opus says durable | 8 | | 10 |
| durable where Opus says not durable | 1 | | 8 |

How to read it:

- **Haiku and Opus pick different details, not more and less of them.** Each misses about a
  third of what the other writes down; Haiku holds more facts per note and more items the judge
  could not support (many of those are judge quibbles, see the review).
- **Haiku's real weakness is the durable verdict:** 8 messages Opus kept were judged not durable,
  against 1 the other way, and five of the 8 were "quote_only". One was the owner's own memo on
  model risk, forwarded from a private account (`m00125`); it never reached the memory. This is
  what the corrected pipeline addresses, and the repeated control will show whether it did.
- **DeepSeek V4 Pro writes short, precise notes and misses most facts:** 41% recall against
  Opus, at about eight times Haiku's cost. Its durable verdicts also disagree with Opus in both
  directions (10 and 8). It is not a better capture model for this dataset.
- The DeepSeek-as-B run lost 37 of 96 judgments to OpenRouter 402 responses (the credit ran out);
  its row is marked partial.

## Superseded runs, kept as a record

`superseded/` holds three earlier judge runs of the Haiku/Opus pair. The first showed the judge
only From, Subject and the new text; the second added the quoted text but not To, Cc and Date.
Both flagged as "unsupported" facts the capture model had correctly taken from the parts the
judge could not see (names from Cc, facts from quoted messages): 77-88 flags against Haiku, 35
once the judge saw the whole file. One run was a repeat of the first by mistake.
