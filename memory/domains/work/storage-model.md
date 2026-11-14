---
id: storage-model
type: topic
domain: work
title: "Zimin Lu's storage model"
summary: "Zimin Lu's gas storage model (SAM): extends the swing model (Oct 2000); Duffie's review found it appropriate (Sep 2000); Lu proposes merging his DP model with Halliburton's optimisation model (8 Jun 2001) and sends him the HJM forward-curve module (16 Aug 2001); total-PV output, Halliburton's LP documentation archived. Storage book VaR: memory/domains/work/storage-book-var.md."
status: active
updated: 2001-08-19
---
# Zimin Lu's storage model

Detail ←[[storage-model-2000-08-w34]] ←[[storage-model-2000-10-w39]] ←[[storage-model-2000-10-w43]] ←[[storage-model-2000-11-w44]] ←[[storage-model-2001-01-w02]] ←[[storage-model-2001-03-w10]] ←[[storage-model-2001-06-09]] ←[[storage-model-2001-08-19]]

Gas storage LP solver (XPRESS): memory/domains/organization/software-licenses.md. Detail (Bridgeline implementation, March audit package, London's virtual storage, the transportation sibling) ←[[storage-model-2000-04-w17]] ←[[storage-model-2000-05-w18]] ←[[storage-model-2000-05-w19]] ←[[storage-model-2000-05-w21]] ←[[storage-model-2000-06-w22]] ←[[storage-model-2000-06-w24]] ←[[m00638]] ←[[m01032]] ←[[storage-model-2000-08-w31]]

- [2001-06-08] Lu to Tom Halliburton (cc owner, Huang): Lukens' storage model, per a paper from its lead developer Dr. Hugh Li, is very similar to Tom's; Lu uses dynamic programming, Tom optimisation; proposes combining both into one storage model product, maybe to sell, if the owner agrees. ←[[m08491]]
- [2001-08-16] Zimin Lu sends Halliburton HJMsim, the storage model's n-factor HJM forward-curve simulator (spot = prompt plus a mean-reverting spread; binned states give a transition matrix), to use in Tom's optimisation model; owner to AOL. ←[[m08962]]
