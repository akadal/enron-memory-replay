---
id: var-backtesting-2000
type: topic
domain: work
title: "VaR methodology: backtesting, factor loadings, component VaR (2000)"
summary: "VaR methodology, 2000: factor loadings for every primary curve, fewer forward prices (Oct 2000); power correlation term structure proposed; Tamarchenko's open VAR and credit issue list (5 Oct); FFVols VaR kept out of production, hybrid vols, backtesting archived."
status: active
updated: 2000-10-08
---
# VaR methodology: backtesting, factor loadings, component VaR (2000)

Detail ←[[var-backtesting-2000-2000-06-w26]] ←[[var-backtesting-2000-2000-07-w28]] ←[[var-backtesting-2000-2000-07-w29]] ←[[var-backtesting-2000-2000-08-w34]] ←[[var-backtesting-2000-2000-09-w35]] ←[[var-backtesting-2000-2000-09-w38]] ←[[var-backtesting-2000-2000-10-w39]] ←[[var-backtesting-2000-2000-10-w40]] ←[[var-backtesting-2000-2000-10-w40]]

Storage book VaR: memory/domains/work/storage-book-var.md. Credit Reserve Model: memory/domains/work/vega-var.md.

- [2000-09-28] Tamarchenko asks the owner to review her comparison of 3 vol methodologies; he takes it to AOL. ←[[m03401]]
- [2000-10-04] Factor loadings: Jin Yu's debugged vatrfacs code covers every primary curve but power; 60 forward prices gave poor factors, 12-48 per commodity much better; Tamarchenko adds a per-commodity count to rms_main_curve_list; Naveen Andrews: Liquids sensible, but Brent and Dubai should be WTI clones. ←[[m03443]]
- [2000-10-05] Tamarchenko's open list (Research, IT, RAC; to Brackett, Gorny): factor loadings, power VAR (correlation term structure, caps, intramonth jumps), IR and FX VAR into RiskTrack, credit model differing on identical runs, FF vols, MG metals and UK curves into RiskTrack, merchant/equity VAR, fat tails. Power: one correlation matrix per prompt month (R10/R11 yearly periodic, 12 reusable); Andrews: periodicity differs by region. ←[[m03440]] ←[[m03445]]
