---
id: storage-book-var
type: topic
domain: work
title: "Storage book VaR review"
summary: "Counterintuitive VaR on Jim Schwieger's gas storage book (25-26 May 2000) traced to forward-forward vols; until fixed, sum the sub-portfolio VaRs; fwd-fwd vols from historical curves tested ($3.14M vs 3.37M), VaR to accept fwd-fwd vol inputs (Jun 2000)."
status: active
updated: 2000-06-11
---
# Storage book VaR review

The storage valuation model: memory/domains/work/storage-model.md. Vega VaR: memory/domains/work/vega-var.md.

- [2000-06-01] To John Arnold (cc Shankman, Schwieger, Tamarchenko): Schwieger's storage book gave counterintuitive VaR on 25-26 May: "This book is a good candidate for a systematic review of the VaR process."; cumulative VaR jumps on Jan 04, where an abnormal forward-forward vol meets a large position: "It seems that the problem arises from forward - forward vols used by the VaR system." Cause: a code bug (reviewed with the IT author) or a kinked forward vol curve. ←[[m01872]]
- [2000-06-01] Proposal: "develop for the traders a fwd-fwd vol generator  allowing them to review the fwd vol curve before it is posted." ←[[m01872]]
- [2000-06-03] To Michael Moscoso (cc Shankman, Vladimir Gorny): the system's aggregate storage book VaR is wrong; "we should use instead the number produced by straightforward addition of Value-at-Risk numbers for the storage book"; Research and IT review the code and the spreadsheet-to-VaR-database link ("Letter to Mike Moscoso" was on his 3 Jun to-do list). ←[[m01905]] ←[[m01904]]
- [2000-06-05] To Winston Jia (cc Tamarchenko, Masson): Tanya tests storage VaR on 20-day historical fwd-fwd vols by close of business; "We should also push ahead to get the ability to use the fwd-fwd vols input" (historical, trader's input, other sources). Jia's Excel rerun of AGG-STORAGE matched production; Storage-Prc deltas moved (Jul 2.68M to 5.70M, Sep 4.63M to 1.68M) and the Dec-01 NG fwd-fwd vol fell from 0.278 (30 May) to 0.0123 (31 May) with the vol curve almost unchanged; VaR code now reads the fwd-fwd curve from a file; Jin suspects the factor-loading program. ←[[m01913]]
- [2000-06-05] Tamarchenko's fwd-fwd vols from historical forward curves (1 month, 18 log-returns, decay 0.97) give STORAGE-PRC VaR $3.14M vs 3.37 in production for 30 May. ←[[m01923]]
