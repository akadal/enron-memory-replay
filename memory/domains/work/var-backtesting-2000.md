---
id: var-backtesting-2000
type: topic
domain: work
title: "VaR methodology: backtesting, factor loadings, component VaR (2000)"
summary: "VaR methodology, 2000: factor loadings for every primary curve, Tamarchenko's open VAR list (Oct 2000, archived); UK VaR over limit, gas-power and EFA correlations reworked (9 Oct); NG correlations weighted to recent data, contract prices (13 Oct); FFVols, hybrid vols, backtesting archived."
status: active
updated: 2000-10-29
---
# VaR methodology: backtesting, factor loadings, component VaR (2000)

Detail ←[[var-backtesting-2000-2000-06-w26]] … (one archive file per week) ←[[var-backtesting-2000-2000-10-w41]] ←[[var-backtesting-2000-2000-10-w43]]

Storage book VaR: memory/domains/work/storage-book-var.md. Credit Reserve Model: memory/domains/work/vega-var.md.

- [2000-10-13] NG VaR correlations (Gorny; Ted agrees): weight 3 months of data toward recent, use each contract's own prices instead of prompt; NA gas first, then all commodities; Cassandra and Veronica document it for desk heads; the owner's view asked. Jin Yu weights factor loadings; Winston: matrix unchanged until cross-commodity prompt issues are solved. ←[[m03648]]
- [2000-10-24] newvatrfacs V1 (unweighted) and V2 (weighted) by Jin Yu, tested for 20 Oct; Tamarchenko reviews results but no code outside SCCS, asks Jin Yu and Wenyao Jia to put every version there (cc owner, Gorny). ←[[m03769]]
- [2000-10-26] Tamarchenko to Andrews: NG prompt-month log-returns over 5 years 9 months show weak fat tails (clearer in Oct-00 prices), non-normal, fit the volatility switching model. ←[[m03860]]
