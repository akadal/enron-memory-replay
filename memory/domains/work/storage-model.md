---
id: storage-model
type: topic
domain: work
title: "Zimin Lu's storage model"
summary: "Zimin Lu's gas storage model (SAM): extends the swing model (Oct 2000 note to Khanna, Griffith); Duffie's review found it appropriate (Sep 2000); output switched to total PV so its delta is the hedge's commodity delta (Jan 2001); Liberty County and Alaska pipeline work archived. Storage book VaR: memory/domains/work/storage-book-var.md."
status: active
updated: 2001-03-09
---
# Zimin Lu's storage model

Detail ←[[storage-model-2000-08-w34]] ←[[storage-model-2000-10-w39]] ←[[storage-model-2000-10-w43]] ←[[storage-model-2000-11-w44]] ←[[storage-model-2001-01-w02]] ←[[storage-model-2001-03-w10]]

Gas storage LP solver (XPRESS): memory/domains/organization/software-licenses.md. Detail (Bridgeline implementation, March audit package, London's virtual storage, the transportation sibling) ←[[storage-model-2000-04-w17]] ←[[storage-model-2000-05-w18]] ←[[storage-model-2000-05-w19]] ←[[storage-model-2000-05-w21]] ←[[storage-model-2000-06-w22]] ←[[storage-model-2000-06-w24]] ←[[m00638]] ←[[m01032]] ←[[storage-model-2000-08-w31]]

- [2001-01-10] Lu to Kenneth Parkhill (cc Gibner): the model now outputs the total PV of the storage capacity, not unit value ((Total PV - S*capacity taken)/capacity turns negative at high spot S); its delta is then the total commodity delta for the hedge; Duffie's audit review suggested the same; new XLL attached. ←[[m05249]]
- [2001-03-07] Tom Halliburton sends the LP storage model documentation (cc Chonawee Supatgiat); owner copies it to AOL. ←[[m06121]]
