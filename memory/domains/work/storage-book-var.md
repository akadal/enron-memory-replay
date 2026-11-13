---
id: storage-book-var
type: topic
domain: work
title: "Storage book VaR review"
summary: "Counterintuitive VaR on Jim Schwieger's gas storage book (25-26 May 2000): abnormal forward-forward vols suspected; owner proposes a fwd-fwd vol generator for traders and, until fixed, summing the sub-portfolio VaRs (Jun 2000)."
status: active
updated: 2000-06-04
---
# Storage book VaR review

The storage valuation model: memory/domains/work/storage-model.md. Vega VaR: memory/domains/work/vega-var.md.

- [2000-06-01] To John Arnold (cc Shankman, Schwieger, Tamarchenko): Schwieger's storage book gave counterintuitive VaR on 25-26 May: "This book is a good candidate for a systematic review of the VaR process."; cumulative VaR jumps on Jan 04, where an abnormal forward-forward vol meets a large position: "It seems that the problem arises from forward - forward vols used by the VaR system." Cause: a code bug (reviewed with the IT author) or a kinked forward vol curve. ←[[m01872]]
- [2000-06-01] Proposal: "develop for the traders a fwd-fwd vol generator  allowing them to review the fwd vol curve before it is posted." ←[[m01872]]
- [2000-06-03] To Michael Moscoso (cc Shankman, Vladimir Gorny): the system's aggregate storage book VaR is wrong; "we should use instead the number produced by straightforward addition of Value-at-Risk numbers for the storage book"; Research and IT review the code and the spreadsheet-to-VaR-database link ("Letter to Mike Moscoso" was on his 3 Jun to-do list). ←[[m01905]] ←[[m01904]]
