---
id: erms-option-precision
type: topic
domain: work
title: "ERMS option valuation: precision and P&L attribution"
summary: "ERMS uses a cruder cumulative normal than structuring's spreadsheets (Issler; Zhiyong Wei's group must change it, Aug 2000); Brad Horn asks how ERMS computes gamma P&L, Zimin Lu explains the curve-shift split and its weakness for big moves (Oct 2000)."
status: active
updated: 2000-10-15
---
# ERMS option valuation: precision and P&L attribution

- [2000-08-23] Paulo Issler (with Eric Moon, structuring) traces a slight option-price mismatch between ERMS and the structuring spreadsheets to ERMS's less accurate approximation of the cumulative normal; Gibner offers Allan Severude Research's help with the code (cc the owner, Ed McMichael, Zimin Lu); Severude: Zhiyong Wei's group, with Jeremy Wong, maintains ERMS and must make the change. ←[[m02959]] ←[[m02962]]
- [2000-10-12] Brad Horn (Bridgeline's NYMEX and Gas Daily option books: dynamically hedged, yet underlying P&L did not offset gamma P&L in a big move) asks Gibner and Lu how ERMS computes gamma dollars (P&L split: new deals, curve shift, gamma, vega, theta, rho, drift, 2nd order). 13 Oct Lu: curve shift is a full revaluation on today's vs yesterday's curve, gamma = 0.5*gamma*(dP)^2, delta the rest; higher-order terms spoil it for big moves. ←[[m03554]] ←[[m03627]]
