# Design consultation, 2026-11-13 (Claude Fable 5.2), with verification

Question: the most economical way to turn the whole mailbox into the dataset without losing
information. Fable's recommendation: Python annotates without a model (owner addresses, quote
pointers by line match, no body cap, same-body links, bulk tags, thread ids); a stateless
per-message capture step by a cheap model writes 0-5 durable notes per message to the inbox,
raw mail goes straight to archive/; Sonnet sleeps once per ISO week (split above 200 notes,
about 122-125 sleeps); every L1 fact carries its source seq and each sleep writes a disposition
ledger per note; skimming measured by kept-rate by position in batch; an independent recall
probe on 500 stratified messages; the raw 1,000-message pilot kept as branch pilot-raw as an
ablation; the first 10 sleeps rerun once for variance.

Verified independently before acting (own script over the same stream):
- Owner mislabelled: kaminski@enron.com (250 messages, X-From "Kaminski, Vince J") and
  vkaminski@aol.com (251, X-From VKaminski@aol.com) are marked "received". Confirmed: 501 owner
  statements on the wrong trust rung. The sent-folder heuristic in build_stream.py misses them.
- The 6,000-character cap hides 2,704,162 characters in 560 messages. Confirmed exactly.
- Text repeated verbatim from earlier messages: 34.8% of body characters by our line-level
  count (lines of 20+ characters seen before); Fable reported 32.8% with its own definition.
  Same order of magnitude.

Not yet verified: cost and time estimates; Haiku 5.5 availability and model id on OpenRouter.
