# Frozen Model and Signal Definitions

This file centralizes definitions already present in upstream authority/result packages. It does not introduce new science.

## 1. V1_CUM — cumulative market prior

For SKU `j` before event time `t`:

`other_count_j = max(global_count_j_before_t - household_count_hj_before_t, 0) + 1`

`market_j = other_count_j / sum(other_count)`

For the event's frozen maturity bin:

`score_j = lambda_bin * market_j + household_count_hj_before_t`

Prediction uses the original normalized B1 probability vector.

Frozen lambda grid:

`[0.5, 1, 2, 3, 5, 8, 12, 20, 40]`

Frozen maturity bins use cumulative personal history count `k`:

- `0_2`
- `3_9`
- `10_plus`

Lambda tuning is allowed only in the original TUNE interval; future EVAL outcomes are forbidden.

## 2. D28_CUM — recent 28-day market prior

Only the market prior changes. Personal counts remain cumulative pre-event household counts.

For an event at time `t`, use only strictly earlier events in the same frozen product group within the prior 28×24 hours.

`rolling_global_j` = prior-28 count selecting SKU `j`

`rolling_household_hj` = current household's count among those rolling events

`other28_j = max(rolling_global_j - rolling_household_hj, 0) + 1`

`D28_market_j = other28_j / sum(other28)`

`D28_score_j = lambda_bin * D28_market_j + cumulative_household_count_hj_before_t`

Events sharing an identical timestamp are batch-scored before update so peer ordering cannot leak information.

D28 may select a different lambda from V1 only through the same frozen TUNE procedure and frozen lambda grid.

## 3. D91 — diagnostic market state only

D91 is a strictly pre-event, other-household 91-day rolling market-share vector constructed with the same no-peer-leakage convention as D28.

D91 is a **state descriptor only** in the mechanism work. It was not promoted as a competing predictive model.

## 4. P1 — frozen predictability score

Let `k` be the number of prior household purchases in the six-SKU choice set.

`maturity = clip(log(1+k) / log(21), 0, 1)`

`core = 0.30*top_share`
`     + 0.25*(1-normalized_entropy)`
`     + 0.25*(1-switch_rate)`
`     + 0.20*recent_concentration`

`P1 = clip(maturity * core, 0, 1)`

P1 uses only pre-event household behavior and has no product-specific fitted weights.

Frozen P1 cutoffs:
- `0.3608488067145302`
- `0.5231119438280639`
- `0.6660270791857679`

The accepted event set is identical between V1 and D28 because P1 itself is unchanged.

## 5. HIGH_SHOCK

Frozen threshold:

`T = 0.011499030019266684`

For each W3–W6 event:

`HIGH_SHOCK iff JS(D28_market, D91_market) >= T`

Otherwise:

`LOW_SHOCK`

The threshold was frozen from the Representative discovery stratum and must not be recomputed on Department Challenge.

## 6. Three regime signals

Signal A — **distribution shock**
- `HIGH_SHOCK` as defined above.

Signal B — **leader switch**
- cumulative-market leader differs from D28-market leader.

Signal C — **local old-leader absence proxy**
- the cumulative-market leader is not observed in same-store, same-six-SKU, strictly prior-28-day **other-household** purchase support.

Important:
- Signal C is a proxy for recent local support, **not proof of shelf availability or inventory**.
- `signal_count = A + B + C`, so it can be `0,1,2,3`.
- No signal-count threshold is validated as a superior deployment gate.

## 7. P1 and Regime answer different questions

P1:
- What is the event's absolute predictability / accuracy–coverage position?

Regime:
- How fragile is the long-run market history, and how much relative rescue value does D28 have?

Their percentage-point gains are not additive.

## 8. Evidence boundary

- H&M frozen V1: external frozen test.
- H&M D28: development evidence on the same H&M data used for diagnosis.
- Grocery D28 back-transfer: frozen cross-domain mechanism transfer on previously studied grocery data.
- Regime maps: developmental / cross-cohort descriptive evidence, not a causal effect and not a new external dataset validation.
