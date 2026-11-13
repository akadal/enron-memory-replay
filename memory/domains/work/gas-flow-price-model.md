---
id: gas-flow-price-model
type: topic
domain: work
title: "Clayton Vernon's gas flow/price model"
summary: "Gas price model from interconnect flows and spot prices; untested, the owner decides on release (Mar 2000); Vernon vets Breese's commercial model (Apr 2000); EOL trade-booking software and slow Gas Model LP, IT gaps (Jul 2000); basis and GPG archived."
status: active
updated: 2000-07-23
---
# Clayton Vernon's gas flow/price model

Clayton Vernon works on it with Vasant Shanbhogue. Inputs (Chris Germany, EIA's Roy Kass) and the simplified no-arbitrage version ←[[gas-flow-price-model-2000-03-w09]] ←[[gas-flow-price-model-2000-03-w13]] ←[[gas-flow-price-model-2000-04-w14]] ←[[m00042]] ←[[gas-flow-price-model-2000-04-w17]] ←[[gas-flow-price-model-2000-07-w29]]

- [1999-12-15] Proposal: from interconnect flows and spot prices, detect capacity hoarding, market power and storage (exotic calls at the consumption hub) → a stochastic basis model in weather. ←[[m00025]]
- [2000-03-28] Vernon to Kevin Presto: the gas model is "completely untested and unvalidated"; only the owner decides on its release. ←[[m01116]] ←[[m01117]]
- [2000-04-24] Mark Breese (Long Term) pushes his former employer's commercial model; Shanbhogue sends Vernon to judge its backtesting and data, not to pitch his own economic model; owner: "I concur." ←[[m01472]]
- [2000-07-20] Vernon's status (to Shanbhogue): Unix C software now listens to EOL trades, books them, marks them to market and stores open positions (no flag yet for credit-rejected trades); the Gas Model LP is slow on the Compaq, Dell lends a test machine; he documents both; IT gaps: SAS server space, the data warehouse, no record of hourly NWS GOES observations. ←[[m02440]]
