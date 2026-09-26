# Technical Appendix - MRSP Phase 2

## A. Evidence hierarchy

The public numerical source of truth is the machine-derived result tables in `data/`, traced through `evidence/CLAIM_EVIDENCE_LEDGER.csv`. This appendix does not introduce new experiments or tuned parameters.

## B. Frozen model definitions

### B1. V1 cumulative market prior

For SKU `j` before event time `t`:

`other_count_j = max(global_count_j_before_t - household_count_hj_before_t, 0) + 1`

`market_j = other_count_j / sum(other_count)`

For the event's frozen maturity bin:

`score_j = lambda_bin * market_j + household_count_hj_before_t`

The frozen lambda grid is `[0.5, 1, 2, 3, 5, 8, 12, 20, 40]`. Maturity bins are `0_2`, `3_9`, and `10_plus`, based on cumulative personal-history count `k`.

### B2. D28 recent-market prior

Only the market prior changes. Personal counts remain cumulative pre-event household counts. For each event, D28 uses strictly earlier events in the same frozen product group during the prior 28 x 24 hours. Same-timestamp events are batch-scored before update.

`other28_j = max(rolling_global_j - rolling_household_hj, 0) + 1`

`D28_market_j = other28_j / sum(other28)`

`D28_score_j = lambda_bin * D28_market_j + cumulative_household_count_hj_before_t`

### B3. D91 diagnostic state

D91 is a strictly pre-event, other-household 91-day rolling market-share vector. It is used as a state descriptor, not promoted as a competing predictive model.

### B4. P1 predictability score

`maturity = clip(log(1+k) / log(21), 0, 1)`

`core = 0.30*top_share + 0.25*(1-normalized_entropy) + 0.25*(1-switch_rate) + 0.20*recent_concentration`

`P1 = clip(maturity * core, 0, 1)`

Frozen P1 cutoffs:

- 0.3608488067145302
- 0.5231119438280639
- 0.6660270791857679

### B5. High-shock state

Frozen threshold: `T = 0.011499030019266684`.

`HIGH_SHOCK` iff `JS(D28_market, D91_market) >= T`; otherwise `LOW_SHOCK`.

The threshold was frozen in Representative and not recomputed on Department Challenge.

### B6. Three regime signals

- **A - distribution shock:** HIGH_SHOCK.
- **B - leader switch:** cumulative-market leader differs from D28-market leader.
- **C - local old-leader absence proxy:** the cumulative-market leader is absent from same-store, same-six-SKU, strictly prior-28-day other-household purchase support.

Signal C is not proof of inventory or shelf availability.

## C. Core numerical results

### C1. P1 selective frontier

| Cohort | Tier | Coverage | V1 accuracy | D28 accuracy |
|---|---|---:|---:|---:|
| Representative | All | 100.00% | 59.37% | 60.26% |
| Representative | 0.6 | 41.08% | 77.17% | 78.09% |
| Representative | 0.7 | 22.00% | 84.78% | 85.49% |
| Representative | 0.8 | 11.01% | 90.06% | 90.51% |
| Department Challenge | All | 100.00% | 61.18% | 61.85% |
| Department Challenge | 0.6 | 40.22% | 79.33% | 79.43% |
| Department Challenge | 0.7 | 22.12% | 86.14% | 86.20% |
| Department Challenge | 0.8 | 11.28% | 90.67% | 90.75% |

### C2. High-shock transfer

| Cohort | Coverage | V1 | D28 | Difference |
|---|---:|---:|---:|---:|
| Representative | 25.00% | 55.00% | 58.49% | +3.50pp |
| Department Challenge | 29.34% | 54.02% | 55.49% | +1.47pp |

### C3. Three-signal stratum

| Cohort | Coverage | V1 | D28 | Difference |
|---|---:|---:|---:|---:|
| Representative | 7.97% | 42.70% | 52.18% | +9.48pp |
| Department Challenge | 10.31% | 43.61% | 47.19% | +3.58pp |

## D. Uncertainty

The main D28-V1 differences were evaluated with clustered uncertainty summaries. Publication interpretation should emphasize direction and evidence boundaries, not treat these intervals as proof of a causal mechanism.

| Cohort | Stratum | Cluster unit | Mean delta | 95% interval |
|---|---|---|---:|---:|
| Representative | All | household | +0.89pp | +0.64 to +1.13 |
| Representative | All | product set | +0.89pp | +0.07 to +2.15 |
| Representative | High shock | household | +3.50pp | +2.72 to +4.30 |
| Representative | High shock | product set | +3.37pp | +0.18 to +7.75 |
| Representative | Three signals | household | +9.52pp | +7.54 to +11.56 |
| Representative | Three signals | product set | +9.06pp | +1.75 to +17.67 |
| Department Challenge | High shock | household | +1.46pp | +0.77 to +2.14 |
| Department Challenge | High shock | product set | +1.49pp | +0.11 to +3.11 |
| Department Challenge | Three signals | household | +3.57pp | +1.88 to +5.20 |
| Department Challenge | Three signals | product set | +3.56pp | +0.68 to +7.25 |

## E. Negative results retained

1. **Binary regime gate:** improved over V1 but remained below all-D28 in both cohorts.
2. **Linear state weighting:** 21 fewer correct than D28 in Representative and 20 more in Department Challenge, with uncertainty crossing zero; not robust.
3. **Promotion / merchandising attribution:** unresolved because the available subset was sparse and semantically selective.
4. **Later W54-W102 holdout:** not valid from current provenance because public raw data could not reproduce the frozen CJ9 identity.

## F. Evidence boundaries

- H&M frozen V1 is an independent frozen external test.
- H&M D28 is development evidence on the same environment used for diagnosis.
- Grocery D28 back-transfer used the H&M-discovered 28-day window without grocery window search, but grocery was previously studied.
- Regime maps are developmental / cross-cohort descriptive evidence, not causal effects and not a new external-dataset validation.
- P1 and Regime are distinct decision dimensions; their percentage-point gains are not additive.

## G. Public verification

Run:

```bash
python reproduce/verify_release.py
```

The verifier checks the released tables against frozen key results and confirms that required public artifacts are present.
