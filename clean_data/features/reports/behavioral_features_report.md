# Feature Report: Behavioral Features
**Generated**: 2026-01-27 15:30:57
---

## Basic Information

- **Total Customers**: 61,410
- **Total Features**: 27
- **Feature Columns**: total_volume, avg_transaction_amount, max_transaction_amount, transaction_amount_std, amount_to_income_ratio, amount_to_sales_ratio, amount_to_revenue_ratio, lifestyle_mismatch, severe_lifestyle_mismatch, has_missing_income, has_missing_sales, amount_cv, high_amount_variability, debit_volume, credit_volume, net_flow, debit_credit_ratio, high_debit_ratio, max_txn_to_income_ratio, max_txn_to_sales_ratio, max_txn_to_revenue_ratio, single_txn_exceeds_revenue, txn_count_total, transaction_consistency, consistent_pattern_flag, behavioral_risk_score, high_behavioral_risk

## Data Quality Checks

### ✅ No Null Values

All features have complete data.

### ✅ No Duplicate Customer IDs

## Feature Statistics

| Feature | Type | Min | Max | Mean | Median | Std Dev | Zero Count | Zero % |
|---------|------|-----|-----|------|--------|---------|------------|--------|
| `total_volume` | Float | 0.00 | 2677539042.00 | 6120900.64 | 2311184.50 | 28812801.85 | 6 | 0.01% |
| `avg_transaction_amount` | Float | 0.00 | 224838493.00 | 98145.85 | 35126.97 | 1135873.73 | 6 | 0.01% |
| `max_transaction_amount` | Float | 0.00 | 2051810761.00 | 2248623.79 | 350000.00 | 15858254.32 | 6 | 0.01% |
| `transaction_amount_std` | Float | 0.00 | 483604743.40 | 301463.30 | 66953.72 | 2721253.14 | 702 | 1.14% |
| `amount_to_income_ratio` | Float | 0.00 | 641237.23 | 266.81 | 0.22 | 3365.03 | 22,992 | 37.44% |
| `amount_to_sales_ratio` | Float | 0.00 | 453407871.00 | 58007.52 | 0.00 | 3101551.92 | 57,379 | 93.44% |
| `amount_to_revenue_ratio` | Float | 0.00 | 453407871.00 | 58274.34 | 0.35 | 3101548.75 | 18,961 | 30.88% |
| `lifestyle_mismatch` | Integer | 0 | 1 | 0.22 | 0 | 0.41 | 48,063 | 78.27% |
| `severe_lifestyle_mismatch` | Integer | 0 | 1 | 0.17 | 0 | 0.37 | 51,072 | 83.17% |
| `has_missing_income` | Integer | 0 | 1 | 0.24 | 0 | 0.43 | 46,732 | 76.10% |
| `has_missing_sales` | Integer | 0 | 1 | 0.07 | 0 | 0.25 | 57,132 | 93.03% |
| `amount_cv` | Float | 0.00 | 10.00 | 2.45 | 2.09 | 1.54 | 702 | 1.14% |
| `high_amount_variability` | Integer | 0 | 1 | 0.54 | 1 | 0.50 | 28,297 | 46.08% |
| `debit_volume` | Float | 0.00 | 1437637276.00 | 2861381.83 | 886504.50 | 14983096.02 | 550 | 0.90% |
| `credit_volume` | Float | 0.00 | 2052481891.00 | 3259518.81 | 1213366.50 | 18248172.39 | 2,080 | 3.39% |
| `net_flow` | Float | -628883171.00 | 2052309612.00 | 398136.98 | 191413.50 | 16876029.55 | 6 | 0.01% |
| `debit_credit_ratio` | Float | 0.00 | 10.00 | 1.54 | 0.70 | 2.29 | 2,624 | 4.27% |
| `high_debit_ratio` | Integer | 0 | 1 | 0.19 | 0 | 0.39 | 49,627 | 80.81% |
| `max_txn_to_income_ratio` | Float | 0.00 | 630987.45 | 98.18 | 0.04 | 3157.55 | 22,992 | 37.44% |
| `max_txn_to_sales_ratio` | Float | 0.00 | 299434000.00 | 23841.46 | 0.00 | 1512651.10 | 57,379 | 93.44% |
| `max_txn_to_revenue_ratio` | Float | 0.00 | 299434000.00 | 23939.64 | 0.06 | 1512652.85 | 18,961 | 30.88% |
| `single_txn_exceeds_revenue` | Integer | 0 | 1 | 0.19 | 0 | 0.39 | 49,939 | 81.32% |
| `txn_count_total` | Integer | 1 | 4,991 | 96.13 | 63 | 102.92 | 0 | 0.00% |
| `transaction_consistency` | Float | 0.00 | 1.00 | 0.33 | 0.32 | 0.12 | 6 | 0.01% |
| `consistent_pattern_flag` | Integer | 0 | 0 | 0.00 | 0 | 0.00 | 61,410 | 100.00% |
| `behavioral_risk_score` | Integer | 0 | 9 | 2.35 | 1 | 2.66 | 12,844 | 20.92% |
| `high_behavioral_risk` | Integer | 0 | 1 | 0.25 | 0 | 0.44 | 45,809 | 74.60% |

## Validation Checks

### ✅ No Unexpected Negative Values

### ✅ No Infinite Values

### Outlier Detection (Values > 3 Standard Deviations)

- `total_volume`: 510 outliers (0.83%)
- `avg_transaction_amount`: 99 outliers (0.16%)
- `max_transaction_amount`: 361 outliers (0.59%)
- `transaction_amount_std`: 225 outliers (0.37%)
- `amount_to_income_ratio`: 141 outliers (0.23%)
- `amount_to_sales_ratio`: 66 outliers (0.11%)
- `amount_to_revenue_ratio`: 66 outliers (0.11%)
- `has_missing_sales`: 4,278 outliers (6.97%)
- `amount_cv`: 1,721 outliers (2.80%)
- `debit_volume`: 544 outliers (0.89%)

... and 8 more features with outliers

## Flag Feature Distributions

| Feature | True Count | True Percentage | False Count | False Percentage |
|---------|------------|-----------------|-------------|------------------|
| `consistent_pattern_flag` | 0 | 0.00% | 61,410 | 100.00% |

## Summary

- ✅ **Total Features**: 27
- ✅ **Data Completeness**: 3.70%
- ✅ **Customers Covered**: 61,410
- ✅ **Flag Features**: 1

---
*Report generated automatically by feature engineering pipeline*
