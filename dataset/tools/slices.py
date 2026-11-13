#!/usr/bin/env python3
"""slices.py: cut the stream into consolidation slices, one per ISO week of mail.

eleman sleeps when the inbox has accumulated, roughly nightly; a nightly replay would mean 669
consolidations. A week is the nearest affordable cadence that still has calendar meaning. A
week with more than --cap messages is split into equal parts, so no sleep has to triage an
unbounded inbox. The simulated "today" of a slice is the local date of its last message.

  python slices.py --manifest dataset/manifest.csv --out dataset/slices.csv [--cap 200]
"""
import argparse
import csv
import datetime
import math
from collections import OrderedDict


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--manifest", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--cap", type=int, default=200)
    a = p.parse_args()
    weeks = OrderedDict()
    for r in csv.DictReader(open(a.manifest, encoding="utf-8")):
        y, w, _ = datetime.date.fromisoformat(r["local"][:10]).isocalendar()
        weeks.setdefault(f"{y}-W{w:02d}", []).append(r)
    rows, k = [], 0
    for week, rs in weeks.items():
        parts = math.ceil(len(rs) / a.cap)
        size = math.ceil(len(rs) / parts)
        for i in range(parts):
            chunk = rs[i * size:(i + 1) * size]
            k += 1
            rows.append([k, week, i + 1, parts, chunk[0]["seq"], chunk[-1]["seq"], len(chunk),
                         chunk[0]["local"][:10], chunk[-1]["local"][:10]])
    with open(a.out, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["slice", "iso_week", "part", "parts", "first_seq", "last_seq", "messages",
                    "first_day", "today"])
        w.writerows(rows)
    print(f"{len(rows)} slices over {len(weeks)} weeks -> {a.out}")


if __name__ == "__main__":
    main()
