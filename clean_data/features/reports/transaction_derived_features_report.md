# Feature Report: Transaction Derived Features
**Generated**: 2026-01-27 15:31:26
---

## Basic Information

- **Total Customers**: 61,410
- **Total Features**: 5
- **Feature Columns**: txn_score_max, txn_score_mean, txn_score_std, txn_score_count_above_threshold, txn_score_pct_above_threshold

## Data Quality Checks

### ✅ No Null Values

All features have complete data.

### ✅ No Duplicate Customer IDs

## Feature Statistics

| Feature | Type | Min | Max | Mean | Median | Std Dev | Zero Count | Zero % |
|---------|------|-----|-----|------|--------|---------|------------|--------|
| `txn_score_max` | Float | 0.00 | 0.60 | 0.13 | 0.20 | 0.12 | 22,366 | 36.42% |
| `txn_score_mean` | Float | 0.00 | 0.60 | 0.01 | 0.00 | 0.02 | 22,366 | 36.42% |
| `txn_score_std` | Float | 0.00 | 0.42 | 0.03 | 0.02 | 0.03 | 22,440 | 36.54% |
| `txn_score_count_above_threshold` | Integer | 0 | 26 | 0.01 | 0 | 0.20 | 60,978 | 99.30% |
| `txn_score_pct_above_threshold` | Float | 0.00 | 1.00 | 0.00 | 0.00 | 0.01 | 60,978 | 99.30% |

## Validation Checks

### ✅ No Unexpected Negative Values

### ✅ No Infinite Values

### Outlier Detection (Values > 3 Standard Deviations)

- `txn_score_max`: 432 outliers (0.70%)
- `txn_score_mean`: 821 outliers (1.34%)
- `txn_score_std`: 620 outliers (1.01%)
- `txn_score_count_above_threshold`: 432 outliers (0.70%)
- `txn_score_pct_above_threshold`: 136 outliers (0.22%)

## Summary

- ✅ **Total Features**: 5
- ✅ **Data Completeness**: 20.00%
- ✅ **Customers Covered**: 61,410

---
*Report generated automatically by feature engineering pipeline*
