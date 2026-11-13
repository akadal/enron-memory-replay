---
id: var-backtesting-2000
type: topic
domain: work
title: "VaR methodology: backtesting, factor loadings, component VaR (2000)"
summary: "VaR methodology in June 2000: Barbara Lewis's VAR meeting 21 Jun; Tamarchenko's NG backtest favours historical over implied vols (fat tails); Ted Murphy on the factor-loadings rewrite and stale VAR processes; component VaR checks."
status: active
updated: 2000-06-25
---
# VaR methodology: backtesting, factor loadings, component VaR (2000)

Storage book VaR: memory/domains/work/storage-book-var.md. Credit Reserve Model: memory/domains/work/vega-var.md.

- [2000-06-20] Barbara Lewis's "important" VAR meeting, Wed 21 Jun 4 pm, EB 3241 (Beck, Gorny, Masson, Moscoso, Murphy, Perlman, Stock); Masson passes it to Tamarchenko and the owner. ←[[m02036]]
- [2000-06-20] Tamarchenko's backtest for Vladimir Gorny on NG forward prices, 1/1/99-6/7/00 (NG-PRICE-PRC and STORAGE-PRC positions): with implied vols PnL breaks VAR95/90/85 on only 2.9-4.1/4.1-6.7/5.6-10.0% of days; with historical vols 6.5-7.6/10.6-12/15.5-16.1%, near the theoretical 5/10/15% whatever the decay factor (1, 0.97, 0.94); she favours historical vols; VAR95 breaks above 5% show fat tails. ←[[m02042]] ←[[m02052]]
- [2000-06-21] Owner: "Can you E-mail to me the graph showing VaR for a frozen portfolio, over one year?"; she resends her 1.5-year frozen-portfolio VAR. ←[[m02052]] ←[[m02055]]
- [2000-06-22] Ted Murphy's factor-loadings memo (via Shankman to the owner and Delainey): a VAR input for all curves, refreshed every 2 weeks (Research the math, IT the code, Operations the runs, RAC the review); RAC rejected results from February until recoded software went live the week before (VAR about 10% different; the rewrite was asked for 6/10/99); dozens of other VAR processes need work, e.g. North American Power jump-diffusion factors not refreshed in 2000. ←[[m02076]]
- [2000-06-23] Component VAR: Tamarchenko has Sunil's AGG-GAS results and asks Naveen Andrews for NG-PRICE results with positions and forward price and vol curves, to verify them. ←[[m02093]]
