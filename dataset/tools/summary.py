#!/usr/bin/env python3
"""summary.py: one table over dataset/runs/sleep-*.json, with cost recomputed from tokens.

Why recompute: the Claude Code CLI used for the pilot (2.1.263) did not know the model id
claude-sonnet-5-5 ("costBasis": "unknown", "unrecognized_model" on stderr) and priced its
tokens at a fallback rate that matches Opus 5 list prices. The token counts are exact; the CLI's
dollar figure is not. Prices below are Anthropic first-party list prices per million tokens
(cache writes: 1.25x input for the 5-minute TTL, 2x for the 1-hour TTL).

  python summary.py            prints a markdown table and totals
  python summary.py --json     the same as JSON
"""
import glob
import json
import os
import sys

PRICES = {  # USD per million tokens
    "claude-sonnet-5-5": {"in": 2.00, "out": 10.00, "read": 0.10, "w5m": 2.50, "w1h": 4.00},
    "claude-opus-5-5": {"in": 4.00, "out": 20.00, "read": 0.20, "w5m": 5.00, "w1h": 8.00},
}
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "runs")


def cost(rec):
    usd, tok = 0.0, {"in": 0, "out": 0, "read": 0, "write": 0}
    for part in (rec.get("harness") or {}).values():
        if not part:
            continue
        u, t = cost_one(part)
        if u is None:
            return None, tok
        usd += u
        for k in tok:
            tok[k] += t[k]
    return usd, tok


def cost_one(h):
    usage = h.get("usage") or {}
    cc = usage.get("cache_creation") or {}
    total_cc = (cc.get("ephemeral_1h_input_tokens") or 0) + (cc.get("ephemeral_5m_input_tokens") or 0)
    share_1h = (cc.get("ephemeral_1h_input_tokens") or 0) / total_cc if total_cc else 1.0
    usd, tok = 0.0, {"in": 0, "out": 0, "read": 0, "write": 0}
    for model, m in (h.get("modelUsage") or {}).items():
        p = PRICES.get(model)
        if p is None:
            return None, tok
        w = m.get("cacheCreationInputTokens", 0)
        usd += (m.get("inputTokens", 0) * p["in"] + m.get("outputTokens", 0) * p["out"]
                + m.get("cacheReadInputTokens", 0) * p["read"]
                + w * (share_1h * p["w1h"] + (1 - share_1h) * p["w5m"])) / 1e6
        tok["in"] += m.get("inputTokens", 0)
        tok["out"] += m.get("outputTokens", 0)
        tok["read"] += m.get("cacheReadInputTokens", 0)
        tok["write"] += w
    return usd, tok


def main():
    rows = []
    for f in sorted(glob.glob(os.path.join(ROOT, "sleep-[0-9][0-9][0-9].json"))):
        with open(f, encoding="utf-8") as fh:
            r = json.load(fh)
        usd, tok = cost(r)
        s = r["sizes"]
        l1 = sum(s[k]["chars"] for k in ("root", "state", "questions", "todo", "domains", "people"))
        h = (r.get("harness") or {}).get("main") or {}
        feed = r.get("feed") or {}
        led = r.get("ledger") or {}
        rows.append({
            "slice": r["slice"], "today": r["simulated_today"], "msgs": feed.get("messages"),
            "durable": feed.get("durable"), "inbox_chars": feed.get("inbox_chars"),
            "kept": led.get("kept"), "dropped": led.get("dropped"), "missing": led.get("missing"),
            "repair": r.get("repair_turn"),
            "usd": round(usd, 3) if usd is not None else None,
            "tok_in_total": tok["in"] + tok["read"] + tok["write"], "tok_out": tok["out"],
            "turns": h.get("num_turns"), "seconds": r["wall_seconds"],
            "week_before": (r.get("quota_before") or {}).get("seven_day"),
            "week_after": (r.get("quota_after") or {}).get("seven_day"),
            "l1_chars": l1, "l1_files": s["domains"]["files"] + s["people"]["files"],
            "people": s["people"]["files"] - 1, "questions": r["open_questions"],
            "gates": f"{r['gates']['lint']}/{r['gates']['sleep_audit']}",
        })
    if "--json" in sys.argv:
        print(json.dumps(rows, indent=1))
        return
    cols = list(rows[0]) if rows else []
    print("| " + " | ".join(cols) + " |")
    print("|" + "---|" * len(cols))
    for r in rows:
        print("| " + " | ".join("" if r[c] is None else str(r[c]) for c in cols) + " |")
    if rows:
        tot = sum(r["usd"] or 0 for r in rows)
        print(f"\nTotal {len(rows)} consolidations: ${tot:.2f} at list price; "
              f"{sum(r['seconds'] for r in rows) / 60:.0f} min wall time.")


if __name__ == "__main__":
    main()
