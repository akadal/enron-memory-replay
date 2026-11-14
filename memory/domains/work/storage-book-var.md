---
id: storage-book-var
type: topic
domain: work
title: "Storage book VaR review"
summary: "Counterintuitive VaR on Jim Schwieger's gas storage book (25-26 May 2000) traced to forward-forward vols; until fixed, sum the sub-portfolio VaRs; fwd-fwd vols from historical curves tested ($3.14M vs 3.37M), VaR to accept fwd-fwd vol inputs (Jun 2000)."
status: active
updated: 2001-07-03
---
# Storage book VaR review

Detail ←[[storage-book-var-2001-07-03]]

The storage valuation model: memory/domains/work/storage-model.md. Vega VaR: memory/domains/work/vega-var.md.

- [2000-06-01] Schwieger's storage book showed counterintuitive VaR on 25-26 May; owner to John Arnold: forward-forward vols in the VaR system cause it (code bug or kinked vol curve); proposes a fwd-fwd vol generator so traders review the curve before posting. ←[[m01872]]
- [2000-06-03] Owner to Michael Moscoso: until fixed, use the plain sum of the storage sub-portfolio VaRs; Research and IT review the code. ←[[m01905]]
- [2000-06-05] Tamarchenko's historical fwd-fwd vols give STORAGE-PRC VaR $3.14M vs 3.37M in production (30 May); the VaR system is to accept fwd-fwd vol inputs. ←[[m01913]] ←[[m01923]]
