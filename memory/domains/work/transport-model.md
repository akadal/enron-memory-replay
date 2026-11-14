---
id: transport-model
type: topic
domain: work
title: "Gas transportation model review (Aug 2000)"
summary: "Research signs off the greeks of the desk's gas transportation (spread option) model: Zimin Lu's finite-difference P/L attribution and fuel P/L check (Aug 2000); the level effect explained to Andrew Lewis (Oct 2000); Shulklapper's questions and the 16 Aug meeting archived."
status: active
updated: 2000-10-22
---
# Gas transportation model review (Aug 2000)

Detail ←[[transport-model-2000-09-w35]] ←[[transport-model-2000-10-w42]]

Storage model: memory/domains/work/storage-model.md.

- [2000-08-10] Lu to Shulklapper and Couch: Taylor-series risk bucketing of P/L fails on big moves; he proposes finite differences (reprice with one input moved to today: curve shifts, Vega1, Vega2, Rho, Eta, Theta; gamma 0.5 x gamma x shift squared); sprdopt's theta is annual, convert to daily (365.25). ←[[m02795]]
- [2000-08-30] Zimin Lu (for Colleen Sullivan) checks fuel P/L on NBPL transport deals 1, 2, 25, 26: positive on 1, 25, 26, negative on 2, as the 23 Aug NYMEX curve rose short-term and fell long-term; fuel tracks the index price (NYMEX + basis + premium), so read P/L off the index curve; the book's fuel P/Ls look right. ←[[m03079]]
- [2000-10-20] Lu to Andrew Lewis (cc owner, Colleen Sullivan, Greg Couch, John Griffith): the level effect is right; with fuel-percentage strikes intrinsic value falls as NYMEX rises, but premium rises unless fuel tops ~8% (usually under 5%). ←[[m03754]]
