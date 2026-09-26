# Novelty and Prior Art Map

The building blocks are not individually new.

## Established prior ideas
- **Selective classification / reject option:** El-Yaniv & Wiener (2010), JMLR — risk–coverage trade-off.
- **Concept drift:** Gama et al. (2014), ACM Computing Surveys — learned relationships can change over time.
- **Retail forecasting:** Fildes, Ma & Kolassa — dynamic retail demand and operational complexity.
- **Fashion forecasting:** Swaminathan & Venkitasubramony (2024) — short life cycles, seasonality, variety and uncertainty.
- **Supermarket recommender drift:** Viniski et al. (2021) — streaming methods can outperform static batch approaches in drifting/cold-start settings.

## Industry parallels
- Stitch Fix publicly describes client states, state transitions and demand modeling.
- Instacart publicly describes production ML across demand forecasting, search, recommendations and personalization.
- McKinsey's 2026 grocery CEO survey reports high AI priority but still limited measurable EBIT impact for many grocers.

## MRSP Phase 2's practical contribution
The strongest contribution is the empirical separation of two operational questions:

1. **Event predictability:** Is this event predictable enough to act on?
2. **Historical validity:** Is the historical market state still trustworthy?

The project further shows:
- recent-market value is strongly state-dependent
- all-event averages can hide concentrated rescue value
- a fashion-domain failure exposed a mechanism that back-transferred positively to grocery
- simple gating / weighting did not automatically outperform the recent-market default

This is a practitioner-facing empirical synthesis, not a claim to have invented selective prediction or concept drift.


See `sources/EXTERNAL_SOURCE_REGISTRY.csv` for URLs and relevance.
