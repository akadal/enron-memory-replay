# Checks A and B after the restart, 2026-11-13

The pilot review (`2026-11-13-4-pilot-review.md`) set two checks with fixed pass criteria before
the full run. Both ran on the corrected pipeline (stream description v3, prompt `capture-v3`,
consolidation by Claude Opus 5.5 on Claude Code 2.1.323).

## A. Capture

| Criterion | Result | Pass |
|---|---|---|
| messages Haiku judged not durable where Opus judged durable (of 96) | 4 (was 8); the reverse 2 | yes (at most 4) |
| `quote_only`/`empty` verdicts on more than 500 new characters, messages 1-1000 | 3 (was 27), each read: a one-line reply above a quoted chain | yes (at most 5) |
| mutual recall within 10 points | Haiku 73.3% of Opus's facts, Opus 60.9% of Haiku's: 12.4 points apart | no, in Haiku's favour |

Evidence: `dataset/validation/capture-control-v3/`. Unsupported items: Haiku 32, Opus 28. Durable
verdict agreement 89-91%. The retry guard re-asked 17 messages in 1-1000 and 12 became durable;
`m00125`, the owner's model-risk memo lost by prompt v2, is now captured. Cost of the v3 capture:
$0.43 per 1,000 messages.

The recall criterion was meant to show that Haiku is not worse than Opus; the gap is in the other
direction (Haiku writes down more of what Opus finds than the reverse).

## B. Consolidation, slices 1-10 (554 messages)

| Criterion | Result | Pass |
|---|---|---|
| ten green, at most one repair turn | 10 green, 0 repair turns | yes |
| no index over its ceiling, no topic closed to make room | none over 2,000; `work` 1,783 and `organization` 1,763 after 10 of 122 slices | yes, but the ceiling will be reached early in the full run |
| every person in 5+ durable messages has an entity file | 8 entity files; 15 people in 5+ messages have none (Grant Masson 25, Mike Roberts 17, Zimin Lu 15, ...) | no |
| weekly quota moves at most 12 points | 44% to 46%, 2 points | yes |

Also measured: $14.32 at list price, 37 minutes; zero silent loss in every slice; drops 61 of 387
durable (40 of them in the promotions week, 2000-W02); 16 topic files over target, none over a
ceiling. The run stopped once (slice 8) on a false date leak: a fact correctly cited 1998-04-19
from its source; `date_leaks.py` no longer limits past dates.

## Subscription capture with Opus (measured on request)

20 sample messages captured by Opus 5.5 through `claude -p` with Claude Code's system prompt
replaced by the capture prompt and no tools: 20 of 20 valid JSON, 7.3 s per call, $0.0184 per call
at list price (one-hour cache writes; OpenRouter's Opus cost was $0.0096), no visible move on the
quota meters. For 11,523 messages: about $210 list-equivalent; at check B's ratio of $7 per weekly
point, about 30 points (estimate).
