#!/usr/bin/env python3
"""preprocess.py: describe each message of the stream without a model, and without changing it.

Every column this script adds is a description; the message itself stays verbatim in L2. That is
what makes the step lossless: a wrong pointer costs nothing but a wrong pointer.

- quoted_from: earlier messages whose lines this message repeats verbatim (reply chains,
  forwards). Matching is by line, not by "-----Original Message-----" markers: about half of all
  text sits below such a marker, but much of it is forwarded material that never arrived as its
  own message, and marker stripping would throw it away. A line counts when its normalised form
  has at least 30 characters and was first seen in an earlier message.
- novel_text: the body with each run of repeated lines replaced by
  "[quoted from m<seq>, k lines]". This is what the capture step reads; L2 keeps the original.
- same_body_as: the first earlier message with an identical normalised body.
- class: "bulk" for automated senders or received mail with more than 20 recipients, else
  "direct". A tag, never a filter.
- thread_id: connected components over normalised subject and quote pointers; metadata only.

  python preprocess.py --stream <cache>/<owner>.jsonl --base-manifest <stream.csv>
                       --out <enriched.jsonl> --manifest dataset/manifest.csv

Stdlib only, deterministic.
"""
import argparse
import csv
import hashlib
import json
import re

MIN_LINE = 30
MIN_ALNUM = 15          # separator rules and date stamps carry fewer letters and digits
MIN_SOURCE_LINES = 3    # a quote pointer needs three recurring lines from one earlier message
HEADER_LIKE = re.compile(r"^(to|cc|bcc|from|subject|date|sent|re|fw|fwd|importance)\s*:", re.I)


def alnum(s):
    return sum(ch.isalnum() for ch in s)
BULK_SENDER = re.compile(
    r"(no-?reply|newsletter|listserv|majordomo|mailer-daemon|announce|subscri|bulletin|digest|"
    r"webmaster|alerts?@|news@|info@|marketing@|promo|^lists?\.|@lists?\.|enron\.announcements|"
    r"office\.chairman|chairman\.ken)", re.I)
SUBJ_PREFIX = re.compile(r"^\s*((re|fw|fwd|aw)\s*(\[\d+\])?\s*:\s*)+", re.I)


def norm_line(ln):
    s = ln.strip().lstrip(">").strip()
    return " ".join(s.split()).lower()


def norm_subject(s):
    prev = None
    s = s or ""
    while prev != s:
        prev, s = s, SUBJ_PREFIX.sub("", s)
    return " ".join(s.split()).lower()


class Union:
    def __init__(self):
        self.p = {}

    def find(self, x):
        self.p.setdefault(x, x)
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def join(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.p[max(ra, rb)] = min(ra, rb)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--stream", required=True)
    p.add_argument("--base-manifest", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--manifest", required=True)
    a = p.parse_args()

    msgs = [json.loads(ln) for ln in open(a.stream, encoding="utf-8")]
    base = {int(r["seq"]): r for r in csv.DictReader(open(a.base_manifest, encoding="utf-8"))}

    first_seen = {}      # normalised line -> seq where it first appeared
    body_seen = {}       # body hash -> seq
    subject_first = {}   # normalised subject -> [(seq, participants other than the owner)]
    uf = Union()
    by_seq = {m["seq"]: m for m in msgs}
    # The owner's addresses: every From of a message the stream marks as sent.
    owners = {x for m in msgs if m["direction"] == "sent" for x in m["from"]}

    for m in msgs:
        seq = m["seq"]
        uf.find(seq)
        lines = m["body"].split("\n")
        out, run_src, run_len, quoted, novel_chars = [], [], 0, set(), 0

        def flush():
            nonlocal run_src, run_len
            if run_len:
                srcs = ", ".join(f"m{s:05d}" for s in sorted(set(run_src)))
                out.append(f"[quoted from {srcs}, {run_len} lines]")
            run_src, run_len = [], 0

        # Pass 1: which earlier message does each line come from? Header-like and separator lines
        # never count: they recur in every Lotus Notes reply ("To: Vince J Kaminski/HOU/ECT@ECT")
        # and made one early message the "source" of 1,287 others in the first version.
        matched = []
        for ln in lines:
            n = norm_line(ln)
            src = None
            if len(n) >= MIN_LINE and not HEADER_LIKE.match(n) and alnum(n) >= MIN_ALNUM:
                s = first_seen.get(n)
                if s is not None and s < seq:
                    src = s
            matched.append((ln, n, src))
        # A source counts only when at least MIN_SOURCE_LINES of its lines recur here.
        per_src = {}
        for _, _, s in matched:
            if s is not None:
                per_src[s] = per_src.get(s, 0) + 1
        valid = {s for s, c in per_src.items() if c >= MIN_SOURCE_LINES}

        new_lines = []
        for ln, n, src in matched:
            if src in valid:
                run_src.append(src)
                run_len += 1
                quoted.add(src)
            else:
                flush()
                out.append(ln)
                novel_chars += len(ln) + 1
                if len(n) >= MIN_LINE and src is None:
                    new_lines.append(n)
        flush()
        for n in new_lines:
            first_seen.setdefault(n, seq)

        h = hashlib.sha256(" ".join(m["body"].split()).encode("utf-8")).hexdigest()
        same = body_seen.get(h) if m["body"].strip() else None
        body_seen.setdefault(h, seq)

        sender = " ".join(m["from"]) + " " + m.get("x_from", "")
        n_rcpt = len(m["to"]) + len(m["cc"])
        bulk = m["direction"] == "received" and (bool(BULK_SENDER.search(sender)) or n_rcpt > 20)

        # Threads: a shared subject joins two messages only when they also share a participant
        # other than the mailbox owner ("hello", "resume" and "lunch" otherwise chain hundreds of
        # unrelated conversations), and quote pointers join only non-bulk mail (newsletters
        # repeat their boilerplate in every issue).
        people = {x for x in m["from"] + m["to"] + m["cc"]} - owners
        subj = norm_subject(m["subject"])
        if subj:
            for prev_seq, prev_people in subject_first.get(subj, []):
                if people & prev_people:
                    uf.join(seq, prev_seq)
                    break
            subject_first.setdefault(subj, []).append((seq, people))
        if not bulk:
            for q in quoted:
                if by_seq[q]["cls"] != "bulk":
                    uf.join(seq, q)

        m.update(quoted_from=sorted(quoted), novel_text="\n".join(out).strip(),
                 novel_chars=novel_chars, same_body_as=same,
                 cls="bulk" if bulk else "direct", n_recipients=n_rcpt)

    for m in msgs:
        m["thread_id"] = f"t{uf.find(m['seq']):05d}"

    with open(a.out, "w", encoding="utf-8", newline="\n") as f:
        for m in msgs:
            f.write(json.dumps(m, ensure_ascii=False) + "\n")

    cols = ["seq", "id", "path", "raw_sha256", "date", "local", "utc", "direction", "class",
            "n_recipients", "chars", "novel_chars", "quoted_from", "same_body_as", "thread_id",
            "alias_paths"]
    with open(a.manifest, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(cols)
        for m in msgs:
            b = base[m["seq"]]
            w.writerow([m["seq"], f"m{m['seq']:05d}", m["path"], m["raw_sha256"], m["date"],
                        m["local"], m["utc"], m["direction"], m["cls"], m["n_recipients"],
                        len(m["body"]), m["novel_chars"],
                        " ".join(f"m{q:05d}" for q in m["quoted_from"]),
                        f"m{m['same_body_as']:05d}" if m["same_body_as"] else "",
                        m["thread_id"], b["alias_paths"]])

    total = sum(len(m["body"]) for m in msgs)
    novel = sum(m["novel_chars"] for m in msgs)
    print(json.dumps({
        "messages": len(msgs), "body_chars": total, "novel_chars": novel,
        "repeated_share": round(1 - novel / total, 3),
        "with_quotes": sum(1 for m in msgs if m["quoted_from"]),
        "same_body": sum(1 for m in msgs if m["same_body_as"]),
        "bulk": sum(1 for m in msgs if m["cls"] == "bulk"),
        "threads": len({m["thread_id"] for m in msgs}),
    }, indent=1))


if __name__ == "__main__":
    main()
