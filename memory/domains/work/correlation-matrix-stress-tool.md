---
id: correlation-matrix-stress-tool
type: topic
domain: work
title: "Stressing a single correlation in a correlation matrix (Tamarchenko tool)"
summary: "Jan 2000: Tanya Tamarchenko's spreadsheet and DLL show which values of one correlation keep the matrix positive definite; next step is a minimum-norm adjustment for disallowed values; to be discussed with Risk Control."
status: active
updated: 2000-02-06
---
# Stressing a single correlation (Tamarchenko tool)

- [2000-01-31] Tanya Tamarchenko (to Grant Masson, Kevin Kindall, the owner): spreadsheet plus DLL; inputs are matrix size, the element's row and column, N_iter and the matrix; for N_iter+1 values from -1 to 1 it reports the smallest eigenvalue, and a positive one means the value is allowed. ←[[m00507]]
- [2000-01-31] For a disallowed value, two options: (1) change all elements by the smallest matrix-norm amount, her next step; (2) change only one row and column, Kindall's idea, user picks the index. She proposed discussing it with Risk Control; only the example spreadsheet was sent. ←[[m00507]]
