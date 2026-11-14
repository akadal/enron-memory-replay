---
id: argentina-modelling
type: topic
domain: work
title: "Argentina modelling (Enron Development)"
summary: "Argentina modelling: Halliburton finds ModReg unsatisfactory, proposes SDDP (28 Sep 2001); after a meeting with the owner Gumucio sets Argentina up in SDDP and recalibrates on Jan-Jun data; Halliburton leaves Enron 2 Nov, advises only (18 Oct 2001); Guerriero's 1999-2000 model team archived."
status: active
updated: 2001-10-21
---
# Argentina modelling (Enron Development)

Detail ←[[argentina-modelling-2001-10-21]]

- [2001-09-28] Tom Halliburton on ModReg, Enron's Argentina model (to Jorge Gumucio, M. Rosenberg, Remi Collonges; cc the owner, Zimin Lu): Fortran by Buenos Aires consultants (a modified grid-operator model), needs CPLEX; Spanish-only docs, column text input, no source or algorithm notes; weekly steps, five load blocks, one-year horizon, ~30 busses and 71 lines, ~6 hours a run, hydro schedules input from elsewhere. ←[[m09218]]
- [2001-09-28] Halliburton: unsatisfactory (hard to use, undocumented, consultant-dependent); Enron should not use an undocumented consultant model and needs a GUI. He proposes SDDP instead: needs inflow data, DC loadflow with zero-impedance lines and guessed resistances for quadratic losses; slow to set up but documented, with a GUI and flexible output. ←[[m09218]]
- [2001-10-18] After a meeting with the owner and a ModReg calibration review, Jorge Gumucio sets Argentina up in SDDP and reruns the calibration on Jan-Jun actuals; he asks the consultants about transmission losses, forced dispatch and gas. Halliburton (last day 2 Nov; next week with the Oslo team) only advises: about 4 hydro and 4 thermal stations, two regions, an interchange limit. ←[[m09339]] ←[[m09340]]
