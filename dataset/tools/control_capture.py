#!/usr/bin/env python3
"""control_capture.py: does the small capture model lose anything against Claude Opus 5.5?

Three steps, all recorded under dataset/validation/capture-control/:
  sample   pick a stratified sample of messages (half sent, half received; spread over length
           quartiles), deterministic
  (capture the sample with capture.py --model anthropic/claude-opus-5.5 --seqs sample.txt)
  judge    for each sampled message, a judge model reads the message, the dataset's notes (A)
           and the control notes (B), and lists: facts in B missing from A; notes in A with no
           support in the message; whether the durable verdicts agree. The judge does not know
           which model wrote which set.
  report   aggregate: recall of A against B, unsupported notes, verdict agreement.

  python control_capture.py sample --manifest dataset/manifest.csv --first 1 --last 349 --n 100
  OPENROUTER_API_KEY=... python control_capture.py judge --enriched <enriched.jsonl>
         --a <haiku records> --b <opus records> [--judge anthropic/claude-sonnet-5.5]
  python control_capture.py report
"""
import argparse
import concurrent.futures as cf
import csv
import json
import os
import random
import re
import sys
import urllib.request
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "validation" / "capture-control"
URL = "https://openrouter.ai/api/v1/chat/completions"

JUDGE_SYSTEM = """You compare two sets of notes taken from the same email for a personal memory. \
Set A and set B were written independently. Use the email as the only ground truth.

Answer with JSON only:
{"b_facts": <number of distinct facts in set B>,
 "missing_in_a": [<each fact stated in B that A does not state, short>],
 "unsupported_in_a": [<each note in A that the email does not support, short>],
 "a_durable": true/false, "b_durable": true/false}
A fact counts as stated in A when A says the same thing, even in other words. Count facts, not \
notes: one note may hold two facts."""


def sample(a):
    rows = [r for r in csv.DictReader(open(a.manifest, encoding="utf-8"))
            if a.first <= int(r["seq"]) <= a.last]
    rnd = random.Random(20261113)
    picked = []
    for direction in ("sent", "received"):
        rs = sorted((r for r in rows if r["direction"] == direction), key=lambda r: int(r["novel_chars"]))
        q = [rs[i * len(rs) // 4:(i + 1) * len(rs) // 4] for i in range(4)]
        for part in q:
            picked += rnd.sample(part, min(len(part), a.n // 8))
    OUT.mkdir(parents=True, exist_ok=True)
    seqs = sorted(int(r["seq"]) for r in picked)
    (OUT / "sample.txt").write_text("\n".join(map(str, seqs)) + "\n", encoding="utf-8")
    print(f"{len(seqs)} messages -> {OUT / 'sample.txt'}")


def load(path):
    out = {}
    for ln in open(path, encoding="utf-8"):
        r = json.loads(ln)
        if not r.get("error"):
            out[r["seq"]] = r
    return out


def notes_text(r):
    if not r["durable"]:
        return f"(not durable: {r.get('reason')})"
    return "\n".join(f"- {n['text']}" for n in r["notes"])


def judge(a):
    key = os.environ.get("OPENROUTER_API_KEY") or sys.exit("OPENROUTER_API_KEY is not set")
    seqs = [int(x) for x in (OUT / "sample.txt").read_text(encoding="utf-8").split()]
    msgs = {m["seq"]: m for m in (json.loads(l) for l in open(a.enriched, encoding="utf-8")) if m["seq"] in seqs}
    A, B = load(a.a), load(a.b)

    def one(seq):
        m = msgs[seq]
        user = (f"Email (new text; earlier quoted messages are replaced by pointers):\n<<<\n"
                f"From: {', '.join(m['from'])}\nSubject: {m['subject']}\n\n{m['novel_text'][:20000]}\n>>>\n\n"
                f"Set A:\n{notes_text(A[seq])}\n\nSet B:\n{notes_text(B[seq])}")
        body = {"model": a.judge, "max_tokens": 1500, "usage": {"include": True},
                "messages": [{"role": "system", "content": JUDGE_SYSTEM}, {"role": "user", "content": user}]}
        req = urllib.request.Request(URL, data=json.dumps(body).encode("utf-8"),
                                     headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"})
        for _ in range(3):
            try:
                with urllib.request.urlopen(req, timeout=120) as r:
                    d = json.load(r)
                t = d["choices"][0]["message"]["content"]
                t = re.sub(r"^```(?:json)?\s*|\s*```$", "", t.strip())
                v = json.loads(t[t.find("{"):t.rfind("}") + 1])
                return {"seq": seq, "judge": a.judge, "verdict": v, "cost_usd": (d.get("usage") or {}).get("cost")}
            except Exception as e:  # recorded, never silent
                err = f"{type(e).__name__}: {str(e)[:150]}"
        return {"seq": seq, "judge": a.judge, "error": err}

    with cf.ThreadPoolExecutor(max_workers=10) as ex, \
            open(OUT / "judgments.jsonl", "w", encoding="utf-8", newline="\n") as f:
        for rec in ex.map(one, seqs):
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(f"judged {len(seqs)} -> {OUT / 'judgments.jsonl'}")


def report(a):
    J = [json.loads(l) for l in open(OUT / "judgments.jsonl", encoding="utf-8")]
    ok = [j for j in J if "verdict" in j]
    bf = sum(int(j["verdict"].get("b_facts") or 0) for j in ok)
    miss = sum(len(j["verdict"].get("missing_in_a") or []) for j in ok)
    unsup = sum(len(j["verdict"].get("unsupported_in_a") or []) for j in ok)
    agree = sum(1 for j in ok if j["verdict"].get("a_durable") == j["verdict"].get("b_durable"))
    res = {"judged": len(ok), "errors": len(J) - len(ok), "control_facts": bf,
           "missing_in_capture": miss, "recall_vs_control": round(1 - miss / bf, 3) if bf else None,
           "unsupported_capture_notes": unsup, "durable_verdict_agreement": round(agree / len(ok), 3) if ok else None,
           "judge_cost_usd": round(sum(float(j.get("cost_usd") or 0) for j in ok), 4)}
    (OUT / "report.json").write_text(json.dumps(res, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(res, indent=1))


def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("sample")
    s.add_argument("--manifest", required=True)
    s.add_argument("--first", type=int, default=1)
    s.add_argument("--last", type=int, required=True)
    s.add_argument("--n", type=int, default=100)
    j = sub.add_parser("judge")
    j.add_argument("--enriched", required=True)
    j.add_argument("--a", required=True)
    j.add_argument("--b", required=True)
    j.add_argument("--judge", default="anthropic/claude-sonnet-5.5")
    sub.add_parser("report")
    a = p.parse_args()
    {"sample": sample, "judge": judge, "report": report}[a.cmd](a)


if __name__ == "__main__":
    main()
