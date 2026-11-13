# Questions — consolidation to human

No cap: the queue shrinks by being drained, not trimmed (memory/rules/format.md). Approval gates
that land here: merging entities, adding an alias, content disappearing without a source,
proposing a new domain.

- [2000-03-19] approval · due 2000-04-18 — The alias table (memory/people/_index.md) dropped its domains column; lines now read `name — aliases — id`, the domains living only in each entity file's `domains:` frontmatter (single home). Reason: the table stood at 6420 chars, inside sleep-audit.py's ceiling band (above 6175 of 6500), where any growth is a RATCHET error, and seven people crossed five noted messages this week (now 4765 chars). Keep the shorter form, or restore the column and raise the people_index budget in memory/rules/format.md and dataset/DESIGN.md?
- [2000-04-14] approval · due 2000-05-14 — Add alias "Bill Bradford" to memory/people/william-bradford.md? "Bill Bradford" (Credit) appears in 11 noted messages, most recently on the IT/Credit lunch list (m01275, memory/domains/work/internal-meetings.md), and in memory/domains/work/credit-markets.md and memory/domains/work/ljm-put-valuation.md, but matches no alias exactly, so those lines stay unattached. Status quo: kept apart.
