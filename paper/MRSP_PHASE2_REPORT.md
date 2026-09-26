# When History Stops Working: Selective Prediction and Regime Resilience in Consumer Forecasting

**Why knowing what to predict is not enough - and how recent market signals can protect forecasts when historical patterns begin to fail**

**Ting-Yi Lin** - Independent Researcher  
ORCID: 0000-0002-1018-8735  
Phase 2 Public Release v1.0

> **Core idea:** A prediction system needs two controls. First ask whether the event is predictable enough to answer. Then ask whether the historical market structure behind that answer is still trustworthy.

## Executive summary

The usual question in forecasting is, "How accurate is the model?" That is often the wrong operational starting point. A business does not have to predict every event, and historical patterns do not remain equally reliable in every market state.

MRSP Phase 2 therefore separates two problems:

1. **Selective Prediction** - *Is this event predictable enough to act on?*
2. **Regime Resilience** - *Is the historical market structure still trustworthy, or has the market changed enough that recent information deserves more weight?*

On grocery data, frozen P1 thresholds reproduce a clear accuracy-coverage trade-off. All-event accuracy sits around 60-62%. Restricting predictions to progressively more predictable events raises accuracy to roughly 78-79% at about 40% coverage, 85-86% at about 22%, and 90-91% at about 11%.

That solves the first problem, but it hides an assumption: the historical market structure used by the predictor must still resemble the current market.

A frozen V1 transfer to H&M fashion exposed that weakness. All-event V1 accuracy was **43.52%** across **292,846** evaluation events. Selectivity still existed, but usable coverage collapsed: at the frozen P1 tiers, coverage fell to **1.24%**, **0.107%**, and **0.014%**. A major constraint was sparse same-category personal history: **257,890 of 292,846** events had no such prior purchase history (`k=0`).

Replacing the cumulative market prior with a recent 28-day market prior, D28, raised H&M development accuracy from **43.52% to 50.07% (+6.55 percentage points)**. Because D28 was developed after inspecting the H&M failure, that result is **development evidence, not independent V2 external validation**.

The important test was what happened when the same 28-day window was carried back to grocery **without searching for a better grocery window**. Average gains looked modest: **+0.89pp** in the Representative cohort and **+0.67pp** in the Department Challenge cohort.

The average, however, hid the mechanism. In the Representative cohort, the frozen high-shock region gained **+3.50pp**, and the strongest three-signal transition region gained **+9.48pp**, covering about **8.0%** of events. In the Department Challenge cohort, the same frozen three-signal definition gained **+3.58pp** at about **10.3%** coverage. The practical interpretation is not that D28 improves every event. Its value is concentrated in a minority of changing-market states where long-run history appears more fragile.

This leads to a two-dimensional operating framework: **use P1 to control whether to predict; use regime signals to monitor whether historical information is becoming stale.** The two gains are not additive, and the regime evidence is descriptive rather than causal.

![Accuracy-coverage frontier under frozen P1 tiers](figures/figure_1_accuracy_coverage_frontier.png)

## 1. Why average accuracy is the wrong starting point

An all-event accuracy number mixes together events that are easy, events that are ambiguous, mature household-product relationships, cold-start relationships, stable markets, and changing markets. That mixture is operationally convenient but analytically weak.

For a business, the relevant choice is often not "Which model wins on average?" It is "At what confidence or predictability level is a prediction worth acting on?"

MRSP V1 addressed that by estimating predictability before the outcome. The frozen P1 score uses only pre-event household behavior: purchase-history maturity, top-choice concentration, entropy, switching, and recent concentration. It has no product-specific learned weights.

In the Representative grocery cohort, V1 accuracy rises from **59.37% on all 40,474 events** to **77.17% at 41.08% coverage**, **84.78% at 22.00% coverage**, and **90.06% at 11.01% coverage**. The Department Challenge cohort shows the same practical shape, reaching **79.33%**, **86.14%**, and **90.67%** at similar coverage levels.

The point is not that a system is "90% accurate." The point is that **about one-tenth of events meet a frozen predictability threshold that supports roughly 90% accuracy in these grocery cohorts**.

## 2. Selective Prediction solves one problem

P1 is a deployment control. It lets an organization choose an accuracy-coverage operating point rather than forcing a prediction on every event.

That is especially useful when a prediction triggers an action with a cost: a recommendation slot, a personalized offer, a replenishment decision, a targeted message, or a human review queue. If low-predictability events are cheap to abstain on, selective prediction can be more useful than maximizing average coverage.

But selective prediction is not enough.

## 3. The hidden assumption: history still represents the market

The V1 predictor combines household history with a market prior. That means the system implicitly assumes that older market structure is still informative about the current choice environment.

This assumption is easy to miss when development and evaluation occur inside a relatively stable retail environment. It becomes visible when the domain shifts.

The question is therefore different from P1:

> **Even if an event looks predictable from the household side, is the market history supporting that prediction still current enough to trust?**

## 4. H&M exposed the weakness

The frozen V1 system was transferred without recalibration to an H&M fashion-retail environment. It evaluated 222 of 225 configured groups and **292,846 events**. All-event V1 accuracy was **43.52%**.

Selectivity itself did not disappear: the highest-P1 events remained much more accurate. What disappeared was usable coverage.

![Frozen P1 coverage collapses in H&M relative to the grocery cohorts](figures/figure_2_hm_coverage_collapse.png)

At the frozen P1 thresholds, H&M coverage was only:

- **1.24%** at the P1 0.6 tier, with **72.78%** accuracy;
- **0.107%** at the P1 0.7 tier, with **91.08%** accuracy;
- **0.014%** at the P1 0.8 tier, with **97.56%** accuracy.

This is a calibration and data-availability warning, not evidence that selective prediction failed conceptually. The score still ranked unusually predictable events, but too few H&M events had the mature personal history needed to enter the old operating region.

## 5. Recent market state mattered

Phase 2 then tested a simple change: replace the cumulative market prior with a strictly pre-event 28-day market prior while keeping personal household counts cumulative. Events sharing a timestamp were scored before update so same-time peer ordering could not leak outcomes.

On H&M, this D28 version increased development accuracy from **43.52% to 50.07%**, a **+6.55pp** improvement.

More complex decay and guard variants produced only marginal gains beyond D28. That made the simple recent-market prior the strongest practical candidate among the tested variants.

The evidence boundary matters: **H&M D28 is development evidence on the same environment that exposed the failure. It is not an independent V2 external validation.**

## 6. The grocery paradox: a useful mechanism can look small on average

The next test did not search for a new grocery window. The 28-day choice was carried back as-is.

![D28 effect is large in H&M development but modest on grocery all-event averages](figures/figure_3_cross_domain_d28_effect.png)

The average result looked almost trivial compared with H&M:

| Grocery cohort | V1 | D28 | Difference | Net additional correct |
|---|---:|---:|---:|---:|
| Representative | 59.37% | 60.26% | +0.89pp | +359 |
| Department Challenge | 61.18% | 61.85% | +0.67pp | +241 |

If evaluation stopped at the all-event average, D28 would look like a minor refinement.

But **354 of the Representative cohort's 359 net wins** occurred in the frozen high-shock region. The improvement was not spread evenly across events.

## 7. Regime decomposition reveals concentrated failure protection

Three pre-outcome signals were frozen for the mechanism analysis:

1. **Distribution shock** - Jensen-Shannon divergence between the recent D28 and longer D91 market-state vectors exceeds a frozen threshold.
2. **Leader switch** - the cumulative-market leader differs from the D28-market leader.
3. **Local old-leader absence proxy** - the cumulative-market leader is absent from recent same-store, same-choice-set, other-household purchase support.

The third signal is a proxy for recent local support. It is **not proof of shelf availability or inventory**.

The result is the central Phase 2 finding:

![D28 rescue rises sharply when all three frozen regime signals are present](figures/figure_4_regime_rescue_by_signal_count.png)

In the Representative cohort, D28 and V1 were close when zero, one, or two signals were present. When all three appeared, V1 accuracy fell to **42.70%** while D28 reached **52.18%**, a **+9.48pp** difference over **7.97%** of events.

The Department Challenge cohort showed a smaller but directionally consistent pattern: **43.61% to 47.19%, +3.58pp**, over **10.31%** of events.

The high-shock definition also transferred directionally without retuning. D28 outperformed V1 by **+3.50pp** in the Representative high-shock stratum and **+1.47pp** in Department Challenge.

Clustered uncertainty checks support the direction of the main high-shock and three-signal differences under both household and product-set clustering. These intervals are reported in the technical appendix rather than treated as proof of a causal regime mechanism.

The operational interpretation is therefore narrower and more useful than "D28 is better":

> **Recent-market information provides disproportionate failure protection when long-run market structure appears to be changing.**

## 8. Why not build a smarter switch?

A natural next step is to route stable states to V1 and high-shock states to D28. That was tested.

A binary LOW_SHOCK->V1 / HIGH_SHOCK->D28 gate improved on V1, but it did **not** outperform simply using D28 on all events. A fixed linear state-weighting scheme also failed to robustly beat D28 across cohorts.

These negative results matter. They prevent the evidence from being turned into an unnecessarily complex router.

The current practical default is therefore simple: **D28 is the strongest tested market-prior default, while regime signals are better treated as monitoring and risk information than as a validated switching policy.**

## 9. Two controls, not one score

![P1 and Regime form two operational dimensions rather than one additive score](figures/figure_5_operational_map.png)

P1 and Regime answer different questions.

- **P1** asks about the event's absolute predictability.
- **Regime signals** ask how fragile the historical market state is and where recent-market rescue is unusually valuable.

A high-P1 event can still occur during a market transition. A low-P1 event can occur in a stable market. Their percentage-point gains therefore cannot be added.

The most useful deployment picture is a two-axis map, not a single blended score.

## 10. What a business can use today

The research supports a practical decision architecture, not a finished universal production system.

**At the event level:**

1. Compute a pre-outcome predictability score such as P1.
2. Choose a coverage tier that matches the cost of being wrong.
3. Predict only when the event is sufficiently predictable; otherwise abstain or use a lower-stakes fallback.

**At the market-state level:**

1. Monitor whether recent market composition is diverging from longer-run history.
2. Track simple signs such as distribution shift and leader change.
3. Treat clustered regime warnings as evidence that historical priors may be stale.
4. Prefer recent-market information or reduce decision confidence during those states.

This architecture is relevant to recommender systems, retail personalization, forecasting, targeted offers, and other systems where historical behavior drives decisions and the cost of stale patterns is asymmetric.

## 11. What this study does not establish

The following claims are outside the evidence:

- MRSP is universally 90% accurate.
- D28 universally adds 9.5 percentage points.
- The three regime signals cause the observed rescue effect.
- D28=28 days is universally optimal.
- A binary regime gate beats the all-D28 default.
- Promotion or merchandising has been established as the main mechanism.
- H&M D28 is an independent V2 external validation.
- A clean later W54-W102 temporal validation has been completed.

The available promotion and placement data were too sparse and semantically selective for clean attribution. A later-time grocery holdout route was also closed because the public raw source could not reproduce the frozen CJ9 identity required for a valid comparison.

## 12. What comes next

The highest-value next scientific step is not more tuning on the current datasets. It is an **independent validation in a new market or genuinely later data environment**, with P1, D28, and regime definitions frozen before outcomes are examined.

The test should ask two separate questions:

1. Does selective prediction preserve a useful accuracy-coverage frontier?
2. Do the frozen regime signals continue to identify states where recent-market information offers disproportionate protection?

That would turn the current two-dimensional framework from a strong practitioner hypothesis with cross-cohort support into a more credible generalization claim.

## Evidence status at a glance

| Result | Evidence status | Boundary |
|---|---|---|
| Frozen V1 on H&M | Independent frozen external test | Validates V1 transport stress, not D28 |
| D28 on H&M | Development evidence | Not independent V2 validation |
| D28 back-transfer to grocery | Frozen mechanism transfer | Grocery environment previously studied |
| Regime maps | Developmental / cross-cohort descriptive evidence | Not causal; not new-dataset validation |
| P1 x Regime framework | Interpretive operational synthesis | Gains are not additive |

## Technical and reproducibility material

- `technical/TECHNICAL_APPENDIX.md` - frozen definitions, uncertainty, negative results, and evidence boundaries.
- `evidence/CLAIM_EVIDENCE_LEDGER.csv` - claim-to-evidence trace.
- `data/` - publication-level result tables derived from machine outputs.
- `reproduce/verify_release.py` - deterministic release verification without raw transaction data.

Raw transaction data are not redistributed in this Phase 2 release.

## AI use disclosure

Generative AI tools were used to assist with literature discovery, research workflow design, code and artifact preparation, drafting, editing, and translation. All scientific claims, evidence boundaries, numerical results, and final publication decisions were reviewed under the author's supervision. The author remains fully responsible for the content of this report.

## Prior work and context

The individual ideas behind selective classification, concept drift, and dynamic retail forecasting are established. The contribution here is the empirical separation of **event predictability** and **historical validity** as two operational controls, together with evidence that recent-market rescue can be highly concentrated in a small changing-market region.

Selected context:

1. El-Yaniv, R. & Wiener, Y. (2010). *On the Foundations of Noise-free Selective Classification*. JMLR. https://www.jmlr.org/papers/v11/el-yaniv10a.html
2. Gama, J. et al. (2014). *A Survey on Concept Drift Adaptation*. ACM Computing Surveys. https://doi.org/10.1145/2523813
3. Fildes, R., Ma, S. & Kolassa, S. (2022). *Retail forecasting: Research and practice*. International Journal of Forecasting.
4. Swaminathan, A. & Venkitasubramony, R. (2024). *Demand forecasting for fashion products: A systematic review*. International Journal of Forecasting.
5. Viniski, A. D. et al. (2021). *A case study of batch and incremental recommender systems in supermarket data under concept drifts and cold start*. Expert Systems with Applications.

## Citation and archival record

Repository: https://github.com/Ting-YiLin/mrsp-phase2-regime-resilience  
Archival record: this report is deposited as the Phase 2 Zenodo release associated with the public repository.

Copyright (c) 2026 Ting-Yi Lin. All rights reserved.
