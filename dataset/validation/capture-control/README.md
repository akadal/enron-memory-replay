# Capture control: Claude Haiku 5.5 against Claude Opus 5.5

Question: does the capture model the dataset uses (Haiku 5.5) lose information that Opus 5.5,
the model the reference deployment of eleman runs on, would have captured?

## Method

- Sample: 96 of the 349 pilot messages (`sample.txt`), half sent by the owner, half received,
  spread over the four quartiles of new-text length; fixed seed.
- The sample was captured again by Opus 5.5 with the identical prompt (`capture-v2`) and input
  (`control-opus-capture.jsonl`, $0.90).
- A judge model (Claude Sonnet 5.5 via OpenRouter) read the complete source file of each message
  (headers and quoted text included) and two unlabelled note sets, A and B, and listed: facts in
  B missing from A, notes in A the message does not support, and both durable verdicts. It was run
  twice with the sets swapped, so each model was measured as A once.

## Result

| | Haiku as A (`report-dataset-as-A.json`) | Opus as A (`report-control-as-A.json`) |
|---|---|---|
| messages judged | 96 | 95 (1 judge error) |
| facts in the other set | 290 | 277 |
| of those, missing in A | 89 | 109 |
| recall of A against the other | 69.3% | 60.6% |
| items in A flagged as unsupported | 35 | 25 |
| durable verdicts agree | 90.6% | 85.3% |

Read across the row: each model misses about a third of what the other wrote down, and Haiku's
notes hold more facts than Opus's (the judge counted 290 facts in Haiku's notes against 277 in
Opus's), so Haiku does not lose information against Opus; the two choose different details. The
cost is precision: the judge flagged more of Haiku's items as unsupported (35 against 25 over
about 120 notes each). The two runs disagree on agreement (90.6% and 85.3%) because the judge
itself varies between calls; read it as about 88%.

## Superseded runs, kept as a record

`superseded/` holds three earlier judge runs. The first showed the judge only From, Subject and
the new text; the second added the quoted text but not To, Cc and Date. Both flagged as
"unsupported" facts the capture model had correctly taken from the parts the judge could not
see (names from Cc, facts from quoted messages): 77-88 flags against Haiku in those runs, 35 once
the judge saw the whole file. One run was a repeat of the first by mistake. A quarter of the last
pair's first attempt failed on OpenRouter 402 responses (credit reservation with 20 concurrent
calls) and was completed with three workers.
