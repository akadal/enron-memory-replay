---
id: correlation-stress
type: topic
domain: work
title: "Stressing correlation matrices"
summary: "Tanya Tamarchenko's spreadsheet and DLL showing which stressed values of one correlation keep the matrix valid (smallest eigenvalue), with two repair options for non-permitted values; to discuss with Risk Control (Jan 2000)."
status: active
updated: 2000-02-06
---
# Stressing correlation matrices

- [2000-01-31] Tamarchenko's spreadsheet and DLL: for a chosen element of a correlation matrix, step its value from -1 to 1 (N_iter+1 steps) and show the smallest eigenvalue of the stressed matrix, so the permitted values (eigenvalue positive) are visible. Sent with an example to Grant Masson, Kevin Kindall and the owner; she proposed discussing it with Risk Control. ←[[m00507]]
- [2000-01-31] For a value that is not permitted: her next step changes all elements by the smallest amount in matrix norm; Kindall's alternative changes only the chosen column (and row). ←[[m00507]]
