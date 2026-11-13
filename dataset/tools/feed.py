#!/usr/bin/env python3
"""feed.py: deliver one slice of the mailbox into the memory core, the way a read tap would.

For every message of the slice:
- L2: the message verbatim and uncapped, in memory/archive/mail/YYYY/m<seq>.md. The file name is
  the message's id, so an L1 fact can point at its source with the provenance link ←[[m<seq>]].
- Inbox: one short block in memory/inbox/<day>--mail.md carrying the capture step's notes
  (dataset/tools/capture.py), or, for a message the capture step judged not durable, the header
  line and the reason only. Every message of the slice appears; none is silently skipped.
- The slice's capture records go to dataset/capture/s<slice>.jsonl in the same commit, so no
  git tag ever contains notes about mail that has not yet arrived.

A calendar day that straddles two slices continues in <day>--mail-2.md (then -3, ...), so the
consolidation's archive move is always a plain rename.

  python feed.py --enriched <enriched.jsonl> --captures <records.jsonl>
                 --slices dataset/slices.csv --slice 3

Prints one JSON line describing what was written. Stdlib only.
"""
import argparse
import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MEM = ROOT / "memory"
INBOX = MEM / "inbox"
ARCH_INBOX = MEM / "archive" / "inbox"
MAIL = MEM / "archive" / "mail"
CAPDIR = ROOT / "dataset" / "capture"
MACHINE = "mail"


def fence_for(text):
    longest = max((len(r) for r in re.findall(r"`+", text)), default=0)
    return "`" * max(3, longest + 1)


def addrs(lst, n=10):
    return ", ".join(lst[:n]) + (f" (+{len(lst) - n} more)" if len(lst) > n else "")


def l2_file(m, mid=None, date=None):
    """The source file exactly as it is in the CMU tarball, headers and body, inside a fence.
    Only line endings are normalised (CRLF to LF); raw_sha256 is the checksum of the original
    bytes. The frontmatter and the title line describe the message; they do not replace it."""
    mid = mid or f"m{m['seq']:05d}"
    raw = m["raw_text"]
    f = fence_for(raw)
    if date is None:
        date = m["local"][:10]
    head = ["---", "type: archive"] + ([f"date: {date}"] if date else []) + [
        f"source: \"{m['path']}\"", f"raw_sha256: {m['raw_sha256']}", f"direction: {m['direction']}"]
    if "cls" in m:
        head += [f"class: {m['cls']}", f"thread: {m['thread_id']}"]
    if m.get("quoted_from"):
        head.append("quotes: [" + ", ".join(f"m{q:05d}" for q in m["quoted_from"]) + "]")
    head += ["---", f"# {mid} · {m['subject'] or '(no subject)'}"]
    return "\n".join(head) + f"\n\n{f}text\n{raw}\n{f}\n"


def inbox_block(m, rec):
    mid = f"m{m['seq']:05d}"
    tag = f"(mail · {m['direction']} · {mid} · automatic capture"
    if not rec["durable"]:
        tag += f" · not durable: {rec['reason']}"
    sender = m.get("x_from") or ", ".join(m["from"])
    lines = [f"## {m['local'][11:16]}", "", tag + ")",
             f"From: {sender} · Subject: {m['subject'] or '(no subject)'}"]
    if rec["durable"]:
        lines.append("")
        for n in rec["notes"]:
            text = n["text"].replace("[[", "[ [").replace("]]", "] ]")  # never a link in the inbox
            quote = f' (owner, verbatim: "{n["quote"]}")' if n.get("quote") else ""
            lines.append(f"- {text}{quote}")
    return "\n".join(lines) + "\n"


def unplaced(src):
    """--slice 0 --enriched <owner>.unplaced.jsonl: write the messages that have no placeable
    date (dataset/SOURCE.md) to memory/archive/mail/unplaced/u<nnn>.md. They are kept, verbatim,
    outside the replay: there is no point in the timeline at which the owner could have
    received them. Their frontmatter carries no date; the header date is in the raw text."""
    out = MAIL / "unplaced"
    out.mkdir(parents=True, exist_ok=True)
    n = 0
    for ln in open(src, encoding="utf-8"):
        m = json.loads(ln)
        (out / f"{m['uid']}.md").write_text(l2_file(m, mid=m["uid"], date=""),
                                            encoding="utf-8", newline="\n")
        n += 1
    print(json.dumps({"unplaced": n, "dir": str(out.relative_to(ROOT))}))


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--enriched", required=True)
    p.add_argument("--captures", required=True)
    p.add_argument("--slices", required=True)
    p.add_argument("--slice", type=int, required=True)
    a = p.parse_args()
    if a.slice == 0:
        return unplaced(a.enriched)

    sl = {int(r["slice"]): r for r in csv.DictReader(open(a.slices, encoding="utf-8"))}[a.slice]
    lo, hi = int(sl["first_seq"]), int(sl["last_seq"])
    msgs = [m for m in (json.loads(ln) for ln in open(a.enriched, encoding="utf-8")) if lo <= m["seq"] <= hi]
    caps = {}
    for ln in open(a.captures, encoding="utf-8"):
        r = json.loads(ln)
        if lo <= r["seq"] <= hi and not r.get("error"):
            caps[r["seq"]] = r        # the last good record for a message wins
    missing = [m["seq"] for m in msgs if m["seq"] not in caps]
    if missing:
        sys.exit(f"slice {a.slice}: no capture record for {len(missing)} messages, e.g. m{missing[0]:05d}")

    INBOX.mkdir(parents=True, exist_ok=True)
    CAPDIR.mkdir(parents=True, exist_ok=True)
    touched, inbox_chars, l2_chars = [], 0, 0

    def name(day, n):
        return f"{day}--{MACHINE}.md" if n == 1 else f"{day}--{MACHINE}-{n}.md"

    def target(day):
        n = 1
        while (ARCH_INBOX / name(day, n)).exists():
            n += 1
        return INBOX / name(day, n)

    for m in msgs:
        y = m["local"][:4]
        (MAIL / y).mkdir(parents=True, exist_ok=True)
        txt = l2_file(m)
        (MAIL / y / f"m{m['seq']:05d}.md").write_text(txt, encoding="utf-8", newline="\n")
        l2_chars += len(txt)
        day = m["local"][:10]
        path = target(day)
        text = "" if path.exists() else (f"---\ntype: log\ndate: {day}\nmachine: {MACHINE}\n---\n"
                                          f"# {day} ({MACHINE})\n")
        text += "\n" + inbox_block(m, caps[m["seq"]])
        with open(path, "a", encoding="utf-8", newline="\n") as f:
            f.write(text)
        inbox_chars += len(text)
        if path.name not in touched:
            touched.append(path.name)

    with open(CAPDIR / f"s{a.slice:03d}.jsonl", "w", encoding="utf-8", newline="\n") as f:
        for m in msgs:
            f.write(json.dumps(caps[m["seq"]], ensure_ascii=False) + "\n")

    durable = [f"m{s:05d}" for s in sorted(caps) if caps[s]["durable"]]
    print(json.dumps({"slice": a.slice, "iso_week": sl["iso_week"], "first_seq": lo, "last_seq": hi,
                      "messages": len(msgs), "durable": len(durable), "first_date": msgs[0]["local"],
                      "last_date": msgs[-1]["local"], "today": sl["today"], "inbox_files": touched,
                      "inbox_chars": inbox_chars, "l2_chars": l2_chars}))


if __name__ == "__main__":
    main()
