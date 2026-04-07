# Cluster relative risk analysis (Version A � plots only)

**Date:** 2026-03-30  
**Scope:** Ranking and rationale derived **only** from Version A clustering deliverables listed below. This document does **not** prescribe or assume any particular `config.yaml` settings.

## Evidence sources

| Asset | Path |
|--------|------|
| Cluster sizes & PDF-style profiles | `Cluster_Profile_Pages/page-1.png` � `page-6.png` |
| Business categoricals | `Clustering_Business_Plots/Heatmap_categorical.png` |
| Business numerical (median, 0�1 scaled) | `Clustering_Business_Plots/Heatmap_Numerical.png` |
| Business province mix | `Clustering_Business_Plots/Province_Distribution.png` |
| Individual categoricals | `Clustering_Individual_Plots/Heatmap_categorical.png` |
| Individual numerical (median, 0�1 scaled) | `Clustering_Individual_Plots/Heatmap_Numerical.png` |
| Individual province mix | `Clustering_Individual_Plots/province_distribution.png` |

---

## What �riskier� means in this report

Segment-level **relative** risk is assessed using patterns that often matter in AML monitoring when interpreting **engineered behavioral features** (not proof of wrongdoing):

| Theme | Example features |
|--------|------------------|
| International exposure | `multi_country_transactions` |
| Channel / rail mix | EMT, EFT, cheque, card, ABM, cash-style counts |
| Concentration / burstiness | `pct_transactions_top10_busiest_days` |
| Materiality | transaction counts and amounts, `sales_cents` (businesses) |
| Complexity / dispersion | unique cities/provinces, card ecommerce/non-ecommerce, MCC diversity |
| Opacity (categorical plots) | high `MCC_N/A`, `Province_other`, `City_other`, `IndustryCode_other` |

Clusters that combine **several** of these themes rank **higher** than clusters dominated by a single dimension (e.g. only sparse timing).

---

## Individual clusters � ranked (riskier ? less risky)

**Approximate order:** **individual_5 ? individual_3 > individual_4 ? individual_6 > individual_1 ? individual_2**

### Tier A � strongest AML-shaped signal in these artifacts

| Cluster | n (from profile pages) | Why it ranks high |
|---------|------------------------|-------------------|
| **individual_5** | 14,509 | Numerical heatmap: **highest** levels across the **broadest** set of features�totals, card, EMT/EFT, debit/credit amounts, `multi_country_transactions`, card ecommerce/non-ecommerce, MCC diversity. Profile **High** list is dominated by volume, geography, and multi-channel activity. |
| **individual_3** | 15,659 | **Largest** **High** feature set: ABM, EFT, `abm_cash_count`, `cheque_user`, `pct_transactions_top10_busiest_days`, `multi_country_transactions`, strong credit metrics. Categorical heatmap: highest share of **`OccupationCode_SELF_EMPLOYED`**. Strong multi-rail + cash/cheque + burst + international story. |

**Note:** **5** vs **3** is a judgment call: **5** emphasizes **breadth and volume**; **3** emphasizes **explicit cash/ABM/cheque/burst** plus self-employment concentration.

### Tier B � strong, slightly narrower than Tier A

| Cluster | n | Why |
|---------|---|-----|
| **individual_4** | 3,892 | **High** on multi-country, EMT/EFT, credit, burstiness. Province/categorical plots: **concentrated in Alberta** (Calgary/Edmonton). |
| **individual_6** | 1,309 | **High** on multi-country, burstiness, `cheque_user`, credit. Province plot: **concentrated in Quebec**. |

### Tier C � notable but weaker bundle than Tier A/B

| Cluster | n | Why |
|---------|---|-----|
| **individual_1** | 1,844 | **High** on multi-country, EFT, credit amount; many signals (ABM, burstiness) are **Moderate** not **High**. Categorical: **`Province_other` / `City_other`** at maximum (opaque geography). |

### Tier D � distinct segment, weakest �high-flow international� profile here

| Cluster | n | Why |
|---------|---|-----|
| **individual_2** | 15,886 | **High** list is mostly **average debit/credit amounts** and **long gaps** between transactions (`Averagetime_between_transaction_day`, std/median time). Numerical heatmap: **low** transaction counts, **high** timing/amount axes. **`multi_country_transactions`** is **not** elevated like other clusters. Reads as **sparse / lumpy** activity, not the same multi-rail + international + burst pattern. |

---

## Business clusters � ranked (riskier ? less risky)

**Approximate order:** **business_3 > business_4 ? business_6 > business_1 > business_2 ? business_5**

### Tier A � strongest AML-shaped signal in these artifacts

| Cluster | n | Why it ranks high |
|---------|-----|-------------------|
| **business_3** | 196 | Numerical heatmap: **very high** on cheque, EFT, EMT, debit/credit counts and amounts, burstiness, materiality. Small segment but **maximum intensity** on traditional-banking rails and amounts. |
| **business_4** | 2,687 | **High** on `sales_cents`, `transaction_count_EMT`, `multi_country_transactions`, `card_top_mcc_weight`. Strong **scale + international + EMT**. Categorical summary: relatively more **`MCC_other`**. |
| **business_6** | 698 | **High** on card + EMT, `multi_country_transactions`, many cities/provinces, ecommerce/non-ecommerce, MCC diversity. Numerical heatmap: strong on **geography + card complexity + international**. |

### Tier B � weaker multi-driver AML pattern

| Cluster | n | Why |
|---------|---|-----|
| **business_1** | 4,004 | **High** on account/business age, **long time between transactions**, burstiness on busiest days; **lower** volume/spread on numerical heatmap. Categorical: very high **`MCC_N/A`** and **`City_other`** (opacity). Overall more **dormant/bursty** than high-flow international. |
| **business_2** | 618 | **High** mainly on EMT + time variability; province plot **Alberta-only**; generally **low** activity on many numerical features. |
| **business_5** | 108 | **High** only on account age + std time between transactions; **Manitoba**-concentrated; categorical: extreme **`Province_other` / `City_other`** (label opacity). **2** has clearer **EMT** signal; **5** is more **opaque �other�** geography�different concerns, both below 3/4/6 on typology strength. |

---

## Cross-cutting observations

1. **`multi_country_transactions` (individual numerical heatmap):** elevated for **all individual clusters except `individual_2`**, which separates **2** from the rest on international exposure in this view.

2. **Opacity:** High **`MCC_N/A`** and **`other`** buckets appear for **`business_1`**, **`business_3`**, **`business_5`**, and **`individual_2`** (MCC N/A). Treat as **attribution / data-quality** signal unless paired with behavioral red flags.

3. **Geographic concentration:** **`individual_4`** (Alberta), **`individual_6`** (Quebec), **`business_2`** (Alberta), **`business_5`** (Manitoba) are **highly province-specific**. Any **incremental** jurisdiction risk depends on **external** policy, not these plots alone.

---

## Summary table

| Population | Highest relative risk (this analysis) | Lowest relative risk (this analysis) |
|------------|----------------------------------------|----------------------------------------|
| Individuals | **individual_5**, **individual_3**; then **individual_4**, **individual_6** | **individual_2** |
| Businesses | **business_3**; then **business_4**, **business_6** | **business_2**, **business_5** (both weak vs 3/4/6; different subordinate stories) |

---

## Disclaimer

Clustering describes **statistical segments** in historical features. This ranking supports **prioritization for review or model design**, not labels of illicit behavior. Policy, legal context, and investigation outcomes sit outside this document.
