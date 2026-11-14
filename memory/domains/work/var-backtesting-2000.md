---
id: var-backtesting-2000
type: topic
domain: work
title: "VaR methodology: backtesting, factor loadings, component VaR (2000)"
summary: "VaR methodology, 2000: missing factor loadings for primary curves, London expiration dates; historical-vol (FFVols) VaR kept out of production, hybrid vols tested; Tamarchenko's 3-methodology comparison (Sep 2000); backtesting tests, Zadorozhny's write-up, Gorny's plan archived."
status: active
updated: 2000-10-01
---
# VaR methodology: backtesting, factor loadings, component VaR (2000)

Detail ←[[var-backtesting-2000-2000-06-w26]] ←[[var-backtesting-2000-2000-07-w28]] ←[[var-backtesting-2000-2000-07-w29]] ←[[var-backtesting-2000-2000-08-w34]] ←[[var-backtesting-2000-2000-09-w35]] ←[[var-backtesting-2000-2000-09-w38]] ←[[var-backtesting-2000-2000-10-w39]]

Storage book VaR: memory/domains/work/storage-book-var.md. Credit Reserve Model: memory/domains/work/vega-var.md.

- [2000-09-21] Factor loadings: only WTI and HU of 13 Liquids primary curves have them (LeBroc: Liquids VaR may be mis-stated); coal borrows NBSK, emissions and Southern Cone power WTI, gas NG (Roenz, Figueroa); Tamarchenko agrees with Hagelmann that every primary curve needs its own; data gaps, mostly London curves without expiration dates; Winston Jia and Jin Yu debug. ←[[m03303]]
- [2000-09-27] FFVols (Naveen Andrews to Ted Murphy): Agg-Gas historical VaR runs ~17MM under implied-vol VaR (25 Sep 19.2MM vs 37MM; implied vols price a strong winter), so it stays out of production ("still in testing"); hybrid vols (historical scaled by the prompt/historical-prompt ratio) give higher VaR but poorer backtests (Tamarchenko); Winston tests them for production; all VaRs still computed as indicators. ←[[m03333]]
- [2000-09-28] Tamarchenko asks the owner to review her comparison of 3 vol methodologies; he takes it to AOL. ←[[m03401]]
