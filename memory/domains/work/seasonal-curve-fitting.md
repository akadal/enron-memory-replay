---
id: seasonal-curve-fitting
type: topic
domain: work
title: "Seasonal factors and forward-curve fitting (Alex Huang, Dec 2000)"
summary: "Alex Huang's C++ tool filters seasonal factors from a forward curve and fits a smooth form usable for forward-forward vols; for plant valuation and credit exposure simulation, not VaR (Dec 2000)."
status: active
updated: 2000-12-31
---
# Seasonal factors and forward-curve fitting

- [2000-12-28] Alex Huang (to the owner and the group) wrote C++ code that filters seasonal factors (two patterns allowed) from a forward curve and fits the deseasoned curve to f(t)=a+A/(t+B)^c, 0<c<.5, by conjugate gradient; as Tanya noted, the form keeps f(t)^2*t - f(t-1)^2*(t-1) > 0, so it yields forward-forward vols. Not useful for VaR; useful for power plant valuation and credit exposure simulation (seasonality in forward-forward vols when simulating forward prices). Spreadsheet and XLL circulated; C code on request. ←[[m05061]]
