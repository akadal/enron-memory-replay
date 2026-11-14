---
id: argentina-modelling
type: topic
domain: work
title: "Argentina modelling (Enron Development)"
summary: "Argentina models: Guerriero's team to improve the power and gas market models by 1 Jun 2000; Halliburton finds ModReg (consultants' undocumented Fortran model) unsatisfactory and proposes SDDP instead (28 Sep 2001)."
status: active
updated: 2001-09-28
---
# Argentina modelling (Enron Development)

- [1999-12-30] Michael Guerriero (ENRON_DEVELOPMENT, responsible for the Argentina operation) asked on 20 Dec to meet on modelling issues; owner: "I shall be glad to meet with you in the 1st week of January", via his ext. 3-3848 or Shirley Crenshaw. ←[[m00121]]
- [2000-03-17] After reviewing the work with the owner, Guerriero forms a team to improve the Argentine power and gas market models by 1 Jun 2000 (Argentine winter): Julian Poole (BA) leads, with Mario Benitez and BA associates Diego Hollweck, Bernardo Andrews, Santiago Porta; Houston members to be named. Phase I data request (regional weather, hydrology, transmission), II power model (weather, hydrology, supply and transmission capacity), III gas supply/demand model. Owner away next week, so Grant Masson holds the process discussion while the associates are in Houston (Tuesday call, Jeff Kabel). ←[[m01024]] ←[[m01029]]
- [2000-03-20] Benitez acknowledged Poole's note ("Okay"); Houston members still unnamed. ←[[m01047]]
- [2001-09-28] Tom Halliburton on ModReg, Enron's Argentina model (to Jorge Gumucio, M. Rosenberg, Remi Collonges; cc the owner, Zimin Lu): Fortran by Buenos Aires consultants (a modified grid-operator model), needs CPLEX; Spanish-only docs, column text input, no source or algorithm notes; weekly steps, five load blocks, one-year horizon, ~30 busses and 71 lines, ~6 hours a run, hydro schedules input from elsewhere. ←[[m09218]]
- [2001-09-28] Halliburton: unsatisfactory (hard to use, undocumented, consultant-dependent); Enron should not use an undocumented consultant model and needs a GUI. He proposes SDDP instead: needs inflow data, DC loadflow with zero-impedance lines and guessed resistances for quadratic losses; slow to set up but documented, with a GUI and flexible output. ←[[m09218]]
