---
id: monte-carlo-library
type: topic
domain: work
title: "Research option model libraries (McLib, Exotica)"
summary: "Research option model libraries: Issler's strip-of-spread-options function for Calgary (31 May 2001); OStrip change misvalues larryoptmodel's gas daily options, Griffith: never change models without the traders, Barkley's mistake fixed (8 Nov 2001); Issler's C HJM simulator out for review (9 Nov 2001); Lu's 1-factor HJM simulator and the Exotica Houston/London versions archived."
status: active
updated: 2001-11-09
---
# Research Monte-Carlo library

Detail ←[[monte-carlo-library-2001-05-13]] ←[[monte-carlo-library-2001-05-26]] ←[[monte-carlo-library-2001-06-03]] ←[[monte-carlo-library-2001-11-09]]

- [2001-05-31] Lon Draper (Calgary desk, sizable new daily spread option position) asks for a strip-of-daily-spread-options function like Ostrip; Lu assigns Paulo Issler: Ostrip with Spdopt() instead of EURO(), about a week. ←[[m08113]]
- [2001-11-08] OStrip: John Griffith (to Larry May; cc owner, Arnold, Issler, Lu): the old Ostrip wrongly used NowToSet days for fixed-price options, larryoptmodel relied on it and now misvalues gas daily options; it needs one date input (today, or the strike-setting date for forward starts); changing models without consulting traders is "unexcusable". Barkley: his honest mistake, settled with May and Griffith; Jeremy Wong updates ERMS; Eric Moon: structurers always used it as documented; power users being checked; Lu (in Paris): it must not happen again. ←[[m09865]] ←[[m09868]]
- [2001-11-09] Issler's HJM simulation in C (o:\research\common\project\options\HJM; spreadsheet functions in o:\research\custom) to the group for bugs: prices and vols in, daily spot grid with transition probabilities out; fwd-fwd vols, PCA loadings per month, as many factors as curve points; next-day spot interpolated to the prompt forward, so spot vol converges to prompt vol. Owner: "Any news?"; no results yet. ←[[m09877]] ←[[m09879]] ←[[m09880]]
