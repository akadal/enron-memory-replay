---
id: var-backtesting-2000
type: topic
domain: work
title: "VaR methodology: backtesting, factor loadings, component VaR (2000)"
summary: "VaR methodology, 2000: NGI-SOCAL fat tails, owner: separate the price process from position changes; Brent/61NY correlation term structure drives Niamh Clarke's VaR; Gorny's VaR priority list, IR and FX VaR first (Tamarchenko); ff vols by power-law fits (Nov 2000); older work archived."
status: active
updated: 2000-11-19
---
# VaR methodology: backtesting, factor loadings, component VaR (2000)

Detail ←[[var-backtesting-2000-2000-06-w26]] … (one archive file per week) ←[[var-backtesting-2000-2000-10-w41]] ←[[var-backtesting-2000-2000-10-w43]] ←[[var-backtesting-2000-2000-11-w45]] ←[[var-backtesting-2000-2000-11-w46]]

Storage book VaR: memory/domains/work/storage-book-var.md. Credit Reserve Model: memory/domains/work/vega-var.md.

- [2000-11-13] NGI-SOCAL fat tails (from 10 Nov): Tamarchenko finds none in vol-normalised log-returns; Andrews: portfolio value change is what matters, single-contract returns need stochastic vol. Owner: position jumps make changes look artificially big, "Of course, the correct approach is to separate the price process from the position changes."; Andrews agrees (their EVT work froze delta-gamma; Garman's gross changes are distorted by big NOPs). ←[[m04176]] ←[[m04178]] ←[[m04181]] ←[[m04200]] ←[[m04204]] ←[[m04205]]
- [2000-11-13] Niamh Clarke's 'Financial Products' VaR hinges on Brent/61NY correlations: $424,199 at 1, $1,868,949 from 18 contracts, $1,106,773 from 12; Tamarchenko prefers all liquid contracts. ←[[m04213]]
- [2000-11-16] VaR priorities (Gorny's 9 Nov list): Tamarchenko: NG correlations on 1 month of data, weekly, weighted version to production; correlation term structure by joint factor loadings (IT: vatrfacs); IR and FX VaR in RiskTrack first (FX tweaks, Infinity data, FX books); NG jumps not evident. ←[[m04272]]
- [2000-11-17] FF vols: Tamarchenko fits 12 monthly implied-vol curves with y=a+A/power(x+b, beta), beta in (0, 0.5) keeping ff vols positive (NG; power next); Andrews: exponential fits went negative, the power law works, though he prefers mean-reverting exp(-t) forms. ←[[m04280]] ←[[m04285]] ←[[m04288]]
