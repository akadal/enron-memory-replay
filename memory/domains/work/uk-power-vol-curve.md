---
id: uk-power-vol-curve
type: topic
domain: work
title: "UK power volatility curves (London)"
summary: "Anjam Ahmad's UK power vol curve model, marked to swaption vols for 5-6 years, audit asked of Gibner (Dec 1999-Jan 2000); half-hourly option vol study (Mar 2000); Surbey asks Research to compare long-term gas and power vols, North America vs Europe (Aug 2000)."
status: active
updated: 2000-08-26
---
# UK power volatility curve generator (London)

- [1999-12-22] Anjam Ahmad built a new UK power vol curve generator: EFA/monthly detail, marked to market up to 6 years, then decaying to a long-term level. Swaption traders fit the first 5-6 years to baseload swaption implied vols (underlying swaps 3-12 months) and price other swaptions, incl. single EFA slots; daily VaR may change; curves reset as the market moves. File: T:\READWRTE\ELEC_UK\MODELS\VOLCURVEGENERATORNEW.XLS. He asked Stinson Gibner to review/audit it (owner copied). ←[[m00098]]
- [2000-01-18] Owner to Gibner: "Did you have the chance to audit the UK vol generator?" ←[[m00383]]
- [2000-03-17] Ahmad's half-hourly option forward vols (to London traders, cc the owner): a "reverse basvol" from half-hourly return correlations scales EFA-slot monthly vols by ~1.30; weekly and half-hourly vols from several years of history; HalfHourlyVolModel.xls (S:\RESEARCH\ANJAM\HHOPTIONVOLMODEL), semi-final numbers. Owner sent it to his AOL. ←[[m01033]]
- [2000-08-21] Dale Surbey to Masson (cc the owner): compare long-term (beyond 10 years) gas and power vol curves, North America vs Europe; UK marks look different though long-term vol should not depend on geography, and it feeds VAR-based position limits. 24 Aug, owner to Masson: "Did you respond to this one?" ←[[m02921]] ←[[m02997]]
