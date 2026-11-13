#!/usr/bin/env python3
"""ledger.py: where did each message of a slice end up, and did anything vanish silently?

The consolidation model does not write the ledger; it is derived here from what the model left
behind, so the model cannot misreport it:
- kept: the message id appears in a provenance link ←[[m<seq>]] somewhere in L1;
- dropped: the run listed it in dataset/drops/sleep-<kkk>.tsv with a reason;
- missing: the capture step marked it durable, and it is neither kept nor dropped.

Gates (exit 1): any missing message (silent loss), or any cited id later than the slice
(a fact sourced from the future). Metrics (recorded, not gated): how often a fact's bracket date
equals the date of a message it cites, and the kept rate by position within the slice, whose
fall toward the end of a slice would be the signature of skimming.

  python ledger.py --slice 3 --slices dataset/slices.csv --manifest dataset/manifest.csv
Writes dataset/ledger/sleep-<kkk>.tsv and prints a JSON summary.
"""
import argparse
import csv
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MEM = ROOT / "memory"
LINK = re.compile(r"\[\[(m\d{5})\]\]")
BRACKET = re.compile(r"^\s*-\s*\[([^\]]+)\]")
DATE = re.compile(r"\d{4}-\d{2}-\d{2}")


def l1_files():
    out = [MEM / n for n in ("state.md", "todo.md", "questions.md")]
    out += sorted((MEM / "domains").rglob("*.md")) + sorted((MEM / "people").rglob("*.md"))
    return [p for p in out if p.exists()]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--slice", type=int, required=True)
    p.add_argument("--slices", required=True)
    p.add_argument("--manifest", required=True)
    a = p.parse_args()
    kkk = f"{a.slice:03d}"
    sl = {int(r["slice"]): r for r in csv.DictReader(open(a.slices, encoding="utf-8"))}[a.slice]
    lo, hi = int(sl["first_seq"]), int(sl["last_seq"])
    day = {r["id"]: r["local"][:10] for r in csv.DictReader(open(a.manifest, encoding="utf-8"))}

    caps = [json.loads(ln) for ln in open(ROOT / "dataset" / "capture" / f"s{kkk}.jsonl", encoding="utf-8")]
    cited, lines_total, lines_dated, lines_match = defaultdict(set), 0, 0, 0
    mismatch = []   # sources of dated fact lines whose bracket date is not the source's date
    for f in l1_files():
        rel = f.relative_to(MEM).as_posix()
        for ln in f.read_text(encoding="utf-8").splitlines():
            ids = LINK.findall(ln)
            for i in ids:
                cited[i].add(rel)
            b = BRACKET.match(ln)
            if ids and b:
                lines_total += 1
                ds = DATE.findall(b.group(1))
                if ds:
                    lines_dated += 1
                    if set(ds) & {day.get(i) for i in ids}:
                        lines_match += 1
                    else:
                        mismatch.extend(i for i in ids if lo <= int(i[1:]) <= hi)

    drops = {}
    dpath = ROOT / "dataset" / "drops" / f"sleep-{kkk}.tsv"
    if dpath.exists():
        for ln in dpath.read_text(encoding="utf-8").splitlines():
            parts = [x.strip() for x in ln.strip().split("\t")]
            if parts and re.fullmatch(r"m\d{5}", parts[0]):
                # id<TAB>class<TAB>reason; an older two-column line has no class
                cls = parts[1] if len(parts) > 2 else ""
                reason = parts[-1] if len(parts) > 1 else ""
                drops[parts[0]] = (cls, reason)

    rows, missing = [], []
    decile_kept, decile_durable = [0] * 10, [0] * 10
    n = len(caps)
    for pos, r in enumerate(caps):
        mid = r["id"]
        if not r["durable"]:
            status, detail = "not_durable", r.get("reason") or ""
        elif mid in cited:
            status, detail = "kept", " ".join(sorted(cited[mid]))
        elif mid in drops:
            status, detail = "dropped", (f"{drops[mid][0]}: " if drops[mid][0] else "") + drops[mid][1]
        else:
            status, detail = "missing", ""
            missing.append(mid)
        if r["durable"]:
            d = min(9, pos * 10 // max(n, 1))
            decile_durable[d] += 1
            decile_kept[d] += status == "kept"
        rows.append([mid, "yes" if r["durable"] else "no", status, detail])

    future = sorted(i for i in cited if int(i[1:]) > hi)
    (ROOT / "dataset" / "ledger").mkdir(parents=True, exist_ok=True)
    with open(ROOT / "dataset" / "ledger" / f"sleep-{kkk}.tsv", "w", encoding="utf-8", newline="\n") as f:
        f.write("id\tdurable\tstatus\tdetail\n")
        for r in rows:
            f.write("\t".join(r) + "\n")

    durable = sum(1 for r in caps if r["durable"])
    redundant = sum(1 for r in rows if r[2] == "dropped" and r[3].startswith("redundant:"))
    kept = sum(1 for r in rows if r[2] == "kept")
    classes = {}
    for cls, _ in drops.values():
        classes[cls or "unclassed"] = classes.get(cls or "unclassed", 0) + 1
    summary = {
        "slice": a.slice, "messages": n, "durable": durable,
        "kept": kept,
        "kept_rate_excluding_redundant": round(kept / (durable - redundant), 3) if durable > redundant else None,
        "drop_classes": dict(sorted(classes.items())),
        "dropped": sum(1 for r in rows if r[2] == "dropped"),
        "missing": len(missing), "missing_ids": missing[:30],
        "future_citations": future[:30],
        "cited_ids_total": len(cited),
        "fact_lines_with_source": lines_total, "dated": lines_dated,
        "date_matches_source": lines_match,
        "date_mismatch_ids_this_slice": sorted(set(mismatch))[:30],
        "kept_rate_by_decile": [round(k / d, 2) if d else None for k, d in zip(decile_kept, decile_durable)],
    }
    print(json.dumps(summary))
    sys.exit(1 if missing or future else 0)


if __name__ == "__main__":
    main()
