---
id: var-backtesting-2000
type: topic
domain: work
title: "VaR methodology: backtesting, factor loadings, component VaR (2000)"
summary: "VaR methodology, 2000: ff vols by power-law fits, R8 smoothing ready for the test environment; joint factor loadings for Brent and 61NY on 18 forward months, effect on Niamh Clarke's book (Nov 2000); fat tails, priorities and older work archived."
status: active
updated: 2000-12-03
---
# VaR methodology: backtesting, factor loadings, component VaR (2000)

Detail ←[[var-backtesting-2000-2000-06-w26]] … (one archive file per week) ←[[var-backtesting-2000-2000-10-w41]] ←[[var-backtesting-2000-2000-10-w43]] ←[[var-backtesting-2000-2000-11-w45]] ←[[var-backtesting-2000-2000-11-w46]] ←[[var-backtesting-2000-2000-11-w47]] ←[[var-backtesting-2000-2000-12-w48]]

Storage book VaR: memory/domains/work/storage-book-var.md. Credit Reserve Model: memory/domains/work/vega-var.md.

- [2000-11-17] FF vols: Tamarchenko fits 12 monthly implied-vol curves with a power law, beta in (0, 0.5) keeping ff vols positive (NG; power next); Andrews: exponential fits went negative. ←[[m04280]] ←[[m04285]] ←[[m04288]]
- [2000-11-20] FF vol smoothing on the R8 curve (8 Nov): Tamarchenko fits each of 12 monthly vol curves with a+A*(t+B)^(-beta), bootstraps ff vols and rebuilds the curve; more results before the test environment? Andrews's a+b(t+c)^(-1) is her beta=1; any class needs parameter ranges that guarantee the bootstrap (a+b*exp(-tc) only if a/b > 2*exp(-1.5)). 21 Nov Alex Huang's "My 2 pennies on forward-forward vol" (owner to AOL). ←[[m04305]] ←[[m04312]] ←[[m04383]]
- [2000-11-28] Joint factor loadings (the stage tool now takes commodity groups and forward counts): Tamarchenko asks Jin Yu and Winston to rerun 61NY and Brent on 18 forward months (not 60) and see the VAR effect on Niamh Clarke's 'Financial Products' book; can power curves go into rms_comm_name_history? ←[[m04485]]
