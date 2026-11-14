---
id: var-backtesting-2000
type: topic
domain: work
title: "VaR methodology: backtesting, factor loadings, component VaR (2000)"
summary: "VaR methodology, 2000: UK VaR on NBP, SYSTEMDAY, SYSTEMNIGHT factors, RisktRac stage run vs the spreadsheet (Dec 2000); ff vol smoothing documented for Winston; non-normal log-returns proposal (Tamarchenko, Rabi De, 7 Dec); power-law fits, joint factor loadings and older work archived."
status: active
updated: 2000-12-10
---
# VaR methodology: backtesting, factor loadings, component VaR (2000)

Detail ←[[var-backtesting-2000-2000-06-w26]] … (one archive file per week) ←[[var-backtesting-2000-2000-10-w41]] ←[[var-backtesting-2000-2000-10-w43]] ←[[var-backtesting-2000-2000-11-w45]] ←[[var-backtesting-2000-2000-11-w46]] ←[[var-backtesting-2000-2000-11-w47]] ←[[var-backtesting-2000-2000-12-w48]] ←[[var-backtesting-2000-2000-12-w49]]

Storage book VaR: memory/domains/work/storage-book-var.md. Credit Reserve Model: memory/domains/work/vega-var.md.
- [2000-12-06] UK VaR (Tamarchenko to Rudi Zipter, Stephen Stock): factor loadings for 17 UK curves (end Sep, RisktRac forwards; to Vlady and Naveen 4 Oct) are decent only for NBP, SYSTEMDAY, SYSTEMNIGHT, so map the others onto those; Winston's code is ready, Risk Control supplies the mappings. 8 Dec: UK VaR runs from RisktRac in stage beside the spreadsheet; Oliver Gaylard and Kirstee Hewitt get Winston's factors, correlations and ff vols to compare. ←[[m04641]] ←[[m04689]]
- [2000-12-06] FF vol smoothing documented for Winston (Wenyao Jia): fit each monthly implied-vol curve with y=a+A/(x+b)^beta, then bootstrap; Excel Solver prototype, simulated annealing (Numerical Recipes) in her code; owner to AOL: "Review for Tue." ←[[m04645]] ←[[m04670]]
- [2000-12-07] Tamarchenko's 3-page proposal for non-normal log-returns in the Monte-Carlo VAR (O:\_Dropbox\Tanya\non_normal_logs.doc) to the owner, Jaesoo Lew, Rabi De; Rabi De: strong non-normality distorts correlations; he offers to document it and build a correlation mapping. ←[[m04662]] ←[[m04677]]

