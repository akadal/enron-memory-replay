---
id: vega-var
type: topic
domain: work
title: "Vega VaR, vega positions and the new Credit Reserve Model"
summary: "Vega VaR documented but waiting for IT, which first codes the new Credit Reserve Model (full evaluation, still debugging) and a 'Prudency' model; Tamarchenko's convergence test of the old model; vega positions captured daily (Nov 1999-Jan 2000)."
status: active
updated: 2000-01-30
---
# Vega VaR, vega positions and the new Credit Reserve Model

Thread in the owner's research group (owner cc'd): Vincent Tang, Jonathan Le, Grant Masson,
Ganapathy Ramesh, Tanya Tamarchenko; Debbie Brackett and Rudi Zipter on the validation side.

- [1999-11-30] Vincent Tang (29 Nov): vega VaR "will be implemented soon"; asked whether all vega positions are in the database. ←[[m00001]]
- [1999-11-30→] Vega positions are captured in the database every day (Jonathan Le). ←[[m00001]]
- [1999-11-30→] Limit validation on vega is down; Jonathan Le proposed coordinating with Debbie Brackett and Rudi Zipter to fix it. ←[[m00001]]
- [2000-01-10] Tang sent Masson a draft Vega VaR implementation document. Index VaR and Vega VaR wait for IT to code them into the new VaR version; per Jonathan Le, IT does the Credit model first, then a "Prudency" model, so the start is uncertain. ←[[m00213]]
- [2000-01-10] IT's new Credit Reserve Model (full evaluation; the old one is delta-gamma) is still being debugged; testing against the current version comes after. IT is unsure of its spread option and swaption valuation (Tang is helping) and asked Research for help with the new insurance projects. ←[[m00213]]
- [2000-01-26] Tanya Tamarchenko's convergence test of the old Research credit reserve model (one counterparty, SITHE IND POWER, 10 to 100,000 simulations) for Mike Fowler: the count matters little for the reserve, given rough price and correlation assumptions, but matters for reserve sensitivities near calculation accuracy. ←[[m00446]]
