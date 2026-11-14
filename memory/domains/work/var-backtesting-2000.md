---
id: var-backtesting-2000
type: topic
domain: work
title: "VaR methodology: backtesting, factor loadings, component VaR (2000)"
summary: "VaR methodology, 2000: NGI-SOCAL fat tails, owner: separate the price process from position changes; Gorny's VaR priority list, IR and FX VaR first (Tamarchenko); ff vols by power-law fits, R8 smoothing ready for the test environment (Nov 2000); Niamh Clarke's Brent/61NY VaR and older work archived."
status: active
updated: 2000-11-26
---
# VaR methodology: backtesting, factor loadings, component VaR (2000)

Detail ←[[var-backtesting-2000-2000-06-w26]] … (one archive file per week) ←[[var-backtesting-2000-2000-10-w41]] ←[[var-backtesting-2000-2000-10-w43]] ←[[var-backtesting-2000-2000-11-w45]] ←[[var-backtesting-2000-2000-11-w46]] ←[[var-backtesting-2000-2000-11-w47]]

Storage book VaR: memory/domains/work/storage-book-var.md. Credit Reserve Model: memory/domains/work/vega-var.md.

- [2000-11-13] NGI-SOCAL fat tails (from 10 Nov): Tamarchenko finds none in vol-normalised log-returns; Andrews: portfolio value change is what matters. Owner: position jumps inflate changes, "Of course, the correct approach is to separate the price process from the position changes."; Andrews agrees. ←[[m04176]] ←[[m04178]] ←[[m04181]] ←[[m04200]] ←[[m04204]] ←[[m04205]]
- [2000-11-16] VaR priorities (Gorny's 9 Nov list): Tamarchenko: NG correlations on 1 month of data, weekly, weighted version to production; correlation term structure by joint factor loadings (IT: vatrfacs); IR and FX VaR in RiskTrack first (FX tweaks, Infinity data, FX books); NG jumps not evident. ←[[m04272]]
- [2000-11-17] FF vols: Tamarchenko fits 12 monthly implied-vol curves with a power law, beta in (0, 0.5) keeping ff vols positive (NG; power next); Andrews: exponential fits went negative. ←[[m04280]] ←[[m04285]] ←[[m04288]]
- [2000-11-20] FF vol smoothing on the R8 curve (8 Nov): Tamarchenko fits each of 12 monthly vol curves with a+A*(t+B)^(-beta), bootstraps ff vols and rebuilds the curve; more results before the test environment? Andrews's a+b(t+c)^(-1) is her beta=1; any class needs parameter ranges that guarantee the bootstrap (a+b*exp(-tc) only if a/b > 2*exp(-1.5)). 21 Nov Alex Huang's "My 2 pennies on forward-forward vol" (owner to AOL). ←[[m04305]] ←[[m04312]] ←[[m04383]]
