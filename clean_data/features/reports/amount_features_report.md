# Feature Report: Amount Features
**Generated**: 2026-01-27 15:28:16
---

## Basic Information

- **Total Customers**: 61,410
- **Total Features**: 17
- **Feature Columns**: amount_mean, amount_stddev, amount_min, amount_max, amount_median, round_amount_count, round_amount_pct, round_amount_flag, just_below_threshold_count, structuring_pattern_flag, large_txn_count_10k, large_txn_count_50k, large_txn_count_100k, amount_max_ratio_mean, amount_stddev_ratio_mean, amount_cv_by_channel, amount_near_50k_increment_count

## Data Quality Checks

### ✅ No Null Values

All features have complete data.

### ✅ No Duplicate Customer IDs

## Feature Statistics

| Feature | Type | Min | Max | Mean | Median | Std Dev | Zero Count | Zero % |
|---------|------|-----|-----|------|--------|---------|------------|--------|
| `amount_mean` | Float | 0.00 | 224838493.00 | 98145.85 | 35126.97 | 1135873.73 | 6 | 0.01% |
| `amount_stddev` | Float | 0.00 | 483604743.40 | 301463.30 | 66953.72 | 2721253.14 | 702 | 1.14% |
| `amount_min` | Float | 0.00 | 224838493.00 | 7101.84 | 99.00 | 910656.87 | 28,888 | 47.04% |
| `amount_max` | Float | 0.00 | 2051810761.00 | 2248623.79 | 350000.00 | 15858254.32 | 6 | 0.01% |
| `amount_median` | Float | 0.00 | 224838493.00 | 24742.14 | 8328.75 | 916757.00 | 6 | 0.01% |
| `round_amount_count` | Integer | 0 | 150 | 1.32 | 0 | 3.10 | 37,115 | 60.44% |
| `round_amount_pct` | Float | 0.00 | 1.00 | 0.02 | 0.00 | 0.05 | 37,115 | 60.44% |
| `round_amount_flag` | Integer | 0 | 1 | 0.00 | 0 | 0.02 | 61,396 | 99.98% |
| `just_below_threshold_count` | Integer | 0 | 33 | 0.06 | 0 | 0.41 | 58,770 | 95.70% |
| `structuring_pattern_flag` | Integer | 0 | 1 | 0.00 | 0 | 0.06 | 61,178 | 99.62% |
| `large_txn_count_10k` | Integer | 0 | 320 | 0.64 | 0 | 3.55 | 48,078 | 78.29% |
| `large_txn_count_50k` | Integer | 0 | 56 | 0.12 | 0 | 0.71 | 57,108 | 92.99% |
| `large_txn_count_100k` | Integer | 0 | 26 | 0.05 | 0 | 0.36 | 59,006 | 96.09% |
| `amount_max_ratio_mean` | Float | 0.00 | 100.00 | 18.40 | 11.95 | 19.56 | 6 | 0.01% |
| `amount_stddev_ratio_mean` | Float | 0.00 | 10.00 | 2.45 | 2.09 | 1.54 | 702 | 1.14% |
| `amount_cv_by_channel` | Float | 0.00 | 10.00 | 1.52 | 1.41 | 0.69 | 791 | 1.29% |
| `amount_near_50k_increment_count` | Integer | 0 | 1,101 | 60.15 | 29 | 74.88 | 1,585 | 2.58% |

## Validation Checks

### ✅ No Unexpected Negative Values

### ✅ No Infinite Values

### Outlier Detection (Values > 3 Standard Deviations)

- `amount_mean`: 99 outliers (0.16%)
- `amount_stddev`: 225 outliers (0.37%)
- `amount_min`: 10 outliers (0.02%)
- `amount_max`: 361 outliers (0.59%)
- `amount_median`: 21 outliers (0.03%)
- `round_amount_count`: 1,132 outliers (1.84%)
- `round_amount_pct`: 1,499 outliers (2.44%)
- `round_amount_flag`: 14 outliers (0.02%)
- `just_below_threshold_count`: 556 outliers (0.91%)
- `structuring_pattern_flag`: 232 outliers (0.38%)

... and 7 more features with outliers

## Flag Feature Distributions

| Feature | True Count | True Percentage | False Count | False Percentage |
|---------|------------|-----------------|-------------|------------------|
| `round_amount_flag` | 14 | 0.02% | 61,396 | 99.98% |
| `structuring_pattern_flag` | 232 | 0.38% | 61,178 | 99.62% |

## Summary

- ✅ **Total Features**: 17
- ✅ **Data Completeness**: 5.88%
- ✅ **Customers Covered**: 61,410
- ✅ **Flag Features**: 2

---
*Report generated automatically by feature engineering pipeline*
