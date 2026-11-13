---
id: var-backtesting-2000
type: topic
domain: work
title: "VaR methodology: backtesting, factor loadings, component VaR (2000)"
summary: "VaR methodology, 2000: Tamarchenko's NG backtest favours historical vols (archived); Ted Murphy on the factor-loadings rewrite; component VaR stability; VAR priorities of 11 Jul, hourly power vol (#5) needs IT (Jul 2000)."
status: active
updated: 2000-07-14
---
# VaR methodology: backtesting, factor loadings, component VaR (2000)

Detail ←[[var-backtesting-2000-2000-06-w26]] ←[[var-backtesting-2000-2000-07-w28]]

Storage book VaR: memory/domains/work/storage-book-var.md. Credit Reserve Model: memory/domains/work/vega-var.md.

- [2000-06-22] Ted Murphy's factor-loadings memo (via Shankman to the owner and Delainey): a VAR input for all curves, refreshed every 2 weeks (Research the math, IT the code, Operations the runs, RAC the review); RAC rejected results from February until recoded software went live the week before (VAR about 10% different; the rewrite was asked for 6/10/99); dozens of other VAR processes need work, e.g. North American Power jump-diffusion factors not refreshed in 2000. ←[[m02076]]
- [2000-06-29] Component VaR stability (Naveen Andrews; cc owner, Masson, Murphy): NG-PRICE with averaging window 10 or 20 (28 Jun) gives very similar numbers; STORAGE-PRC (no gamma, 27 Jun): FFVols and RiskMetrics VaR comparable to the code. ←[[m02197]]
- [2000-07-11] VAR priorities (Murphy, Buy, Lavorato): monthly index positions (NA gas), re-running correlations and factor loadings, a factor-loading database, forward/forward vol; #5 scoping hourly power vol; all but #5 under way (Tamarchenko, Masson). Owner: "Item # 5 will require help from IT." (positions come daily-aggregated); Tamarchenko to see MG in NY with Murphy before her 26 Jul leave: "it makes a lot of sense for her to visit MG and to kick the tires." ←[[m02357]] ←[[m02359]]
