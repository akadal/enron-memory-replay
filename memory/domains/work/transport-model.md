---
id: transport-model
type: topic
domain: work
title: "Gas transportation model review (Aug 2000)"
summary: "Research signs off the greeks of the desk's new gas transportation (spread option) model: Shulklapper's gamma and rho questions, Colleen Sullivan's meeting 11 Aug, Zimin Lu's finite-difference P/L attribution; meeting 16 Aug (Aug 2000)."
status: active
updated: 2000-09-03
---
# Gas transportation model review (Aug 2000)

Detail ←[[transport-model-2000-09-w35]]

Storage model: memory/domains/work/storage-model.md.

- [2000-08-07] Ken Shulklapper (with Greg Couch; via Victor Guggenheim) wants Research to sign off the new transport model's greeks before floor release: high gamma in out years, high rho (example tab "LongTerm9", Kingsgate to Malin); Zimin Lu: gamma and cross gamma from the research spread option model look right, the oddity comes from price change by maturity. ←[[m02718]]
- [2000-08-10] Lu to Shulklapper and Couch: Taylor-series risk bucketing of P/L fails on big moves; he proposes finite differences (reprice with one input moved to today: curve shifts, Vega1, Vega2, Rho, Eta, Theta; gamma 0.5 x gamma x shift squared); sprdopt's theta is annual, convert to daily (365.25). ←[[m02795]]
- [2000-08-11] Gas Transportation meeting Wed 16 Aug 4:00 pm, EB1938: the owner, Bob Lee, Larry May, Gibner, Lu. ←[[m02810]]
- [2000-08-30] Zimin Lu (for Colleen Sullivan) checks fuel P/L on NBPL transport deals 1, 2, 25, 26: positive on 1, 25, 26, negative on 2, as the 23 Aug NYMEX curve rose short-term and fell long-term; fuel tracks the index price (NYMEX + basis + premium), so read P/L off the index curve; the book's fuel P/Ls look right. ←[[m03079]]
