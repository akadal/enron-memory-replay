---
id: erms-option-precision
type: topic
domain: work
title: "ERMS option valuation: precision and P&L attribution"
summary: "ERMS uses a cruder cumulative normal than structuring's spreadsheets (Aug 2000); Lu explains ERMS gamma P&L (Oct 2000); Lu's UnitCorrPremium() fix for spread options at correl=1, vol1=vol2 (Jan 2001)."
status: active
updated: 2001-01-07
---
# ERMS option valuation: precision and P&L attribution

- [2000-08-23] Paulo Issler (with Eric Moon, structuring) traces a slight option-price mismatch between ERMS and the structuring spreadsheets to ERMS's less accurate approximation of the cumulative normal; Gibner offers Allan Severude Research's help with the code (cc the owner, Ed McMichael, Zimin Lu); Severude: Zhiyong Wei's group, with Jeremy Wong, maintains ERMS and must make the change. ←[[m02959]] ←[[m02962]]
- [2000-10-12] Brad Horn (Bridgeline's NYMEX and Gas Daily option books: dynamically hedged, yet underlying P&L did not offset gamma P&L in a big move) asks Gibner and Lu how ERMS computes gamma dollars (P&L split: new deals, curve shift, gamma, vega, theta, rho, drift, 2nd order). 13 Oct Lu: curve shift is a full revaluation on today's vs yesterday's curve, gamma = 0.5*gamma*(dP)^2, delta the rest; higher-order terms spoil it for big moves. ←[[m03554]] ←[[m03627]]
- [2001-01-03] London's spread options fail at correl=1, vol1=vol2 (zero effective vol, no time value; reported by the owner): Lu's UnitCorrPremium() returns the discounted intrinsic value; Zhiyong Wei and Zhiyun Yang to add it; 4 Jan Lu explains spread options to Yang (Enpower). ←[[m05129]] ←[[m05162]]
