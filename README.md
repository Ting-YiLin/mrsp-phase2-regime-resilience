# MRSP Phase 2 - Selective Prediction + Regime Resilience

**When History Stops Working: Selective Prediction and Regime Resilience in Consumer Forecasting**

Why knowing what to predict is not enough - and how recent market signals can protect forecasts when historical patterns begin to fail

**Author:** Ting-Yi Lin, Independent Researcher - ORCID 0000-0002-1018-8735

## What this project adds

MRSP Phase 2 separates two deployment questions that average accuracy tends to blur:

1. **Selective Prediction:** Is this event predictable enough to answer?
2. **Regime Resilience:** Is the historical market structure behind the prediction still trustworthy?

## Main result

On grocery data, frozen P1 thresholds produce an accuracy-coverage frontier: roughly **60-62%** on all events, rising to about **78-79% at 40% coverage**, **85-86% at 22%**, and **90-91% at 11%**.

A recent 28-day market prior (D28) added only **+0.89pp** and **+0.67pp** on average across two grocery cohorts. But the gain was concentrated. When all three frozen regime signals were present:

| Cohort | V1 | D28 | D28 - V1 | Coverage |
|---|---:|---:|---:|---:|
| Representative | 42.70% | 52.18% | **+9.48pp** | 7.97% |
| Department Challenge | 43.61% | 47.19% | **+3.58pp** | 10.31% |

The evidence supports a practical interpretation: **use P1 to decide whether to predict, and use regime monitoring to judge whether long-run market history is becoming stale.**

![Regime rescue](figures/figure_4_regime_rescue_by_signal_count.png)

## Important boundary

H&M D28 is **development evidence, not independent V2 external validation**. The regime results are **descriptive, not causal**. P1 and Regime answer different questions, so their percentage-point gains must not be added.

## Read the project

- [Flagship practitioner article](ARTICLE.md)
- [Traditional Chinese edition](ARTICLE_zh-TW.md)
- [Technical appendix](technical/TECHNICAL_APPENDIX.md)
- [Frozen claims](CLAIMS.md)
- [Evidence ledger](evidence/CLAIM_EVIDENCE_LEDGER.csv)
- [Release verification](reproduce/verify_release.py)
- [Rights notice](RIGHTS_NOTICE.md)

## Archive and citation

Zenodo DOI: 10.5281/zenodo.22969898  
Zenodo record: https://zenodo.org/uploads/22969898

This repository is a companion to the earlier MRSP V1 selective-prediction project: https://github.com/Ting-YiLin/mrsp-predictability

Copyright (c) 2026 Ting-Yi Lin. All rights reserved.
