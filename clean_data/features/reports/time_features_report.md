# Feature Report: Time Features
**Generated**: 2026-01-27 15:30:31
---

## Basic Information

- **Total Customers**: 61,410
- **Total Features**: 25
- **Feature Columns**: txn_hour_mode, after_hours_txn_pct, after_hours_flag, weekend_txn_count, weekend_txn_pct, weekend_heavy_flag, midnight_txn_count, early_morning_txn_count, late_night_txn_count, midnight_txn_pct, unusual_hours_flag, time_between_txn_mean, time_between_txn_median, time_between_txn_min, time_between_txn_max, time_between_txn_std, very_short_time_between_txn, rapid_fire_txn_count, rapid_fire_flag, txn_hour_std, consistent_timing_flag, business_hours_txn_pct, non_business_hours_heavy, months_active, txn_per_month

## Data Quality Checks

### ✅ No Null Values

All features have complete data.

### ✅ No Duplicate Customer IDs

## Feature Statistics

| Feature | Type | Min | Max | Mean | Median | Std Dev | Zero Count | Zero % |
|---------|------|-----|-----|------|--------|---------|------------|--------|
| `txn_hour_mode` | Integer | -1 | 23 | 11.99 | 12 | 4.18 | 992 | 1.62% |
| `after_hours_txn_pct` | Float | 0.00 | 1.00 | 0.43 | 0.43 | 0.14 | 1,663 | 2.71% |
| `after_hours_flag` | Integer | 0 | 1 | 0.19 | 0 | 0.39 | 49,817 | 81.12% |
| `weekend_txn_count` | Integer | 0 | 2,039 | 30.42 | 21 | 32.84 | 2,157 | 3.51% |
| `weekend_txn_pct` | Float | 0.00 | 1.00 | 0.35 | 0.33 | 0.13 | 2,157 | 3.51% |
| `weekend_heavy_flag` | Integer | 0 | 1 | 0.68 | 1 | 0.47 | 19,643 | 31.99% |
| `midnight_txn_count` | Integer | 0 | 467 | 5.77 | 4 | 7.31 | 8,850 | 14.41% |
| `early_morning_txn_count` | Integer | 0 | 225 | 7.43 | 5 | 7.46 | 6,898 | 11.23% |
| `late_night_txn_count` | Integer | 0 | 385 | 6.69 | 4 | 8.29 | 9,038 | 14.72% |
| `midnight_txn_pct` | Float | 0.00 | 1.00 | 0.07 | 0.06 | 0.09 | 8,850 | 14.41% |
| `unusual_hours_flag` | Integer | 0 | 1 | 0.87 | 1 | 0.34 | 8,070 | 13.14% |
| `time_between_txn_mean` | Float | 0.00 | 2194.13 | 74.00 | 35.23 | 139.42 | 1,660 | 2.70% |
| `time_between_txn_median` | Float | 0.00 | 2194.13 | 57.91 | 23.38 | 134.76 | 1,660 | 2.70% |
| `time_between_txn_min` | Float | 0.00 | 2194.13 | 16.08 | 0.22 | 112.30 | 1,660 | 2.70% |
| `time_between_txn_max` | Float | 0.00 | 2194.13 | 230.56 | 162.46 | 226.25 | 1,660 | 2.70% |
| `time_between_txn_std` | Float | 0.00 | 1510.38 | 61.34 | 34.58 | 88.29 | 2,233 | 3.64% |
| `very_short_time_between_txn` | Integer | 0 | 913 | 1.33 | 0 | 6.21 | 38,323 | 62.41% |
| `rapid_fire_txn_count` | Integer | 0 | 1,662 | 9.97 | 2 | 25.46 | 20,785 | 33.85% |
| `rapid_fire_flag` | Integer | 0 | 1 | 0.25 | 0 | 0.43 | 46,191 | 75.22% |
| `txn_hour_std` | Float | 0.00 | 16.26 | 5.04 | 5.09 | 1.21 | 1,826 | 2.97% |
| `consistent_timing_flag` | Integer | 0 | 1 | 0.00 | 0 | 0.04 | 61,333 | 99.87% |
| `business_hours_txn_pct` | Float | 0.00 | 1.00 | 0.37 | 0.38 | 0.12 | 2,189 | 3.56% |
| `non_business_hours_heavy` | Integer | 0 | 1 | 0.06 | 0 | 0.23 | 57,822 | 94.16% |
| `months_active` | Integer | 0 | 3 | 2.89 | 3 | 0.47 | 907 | 1.48% |
| `txn_per_month` | Float | 0.00 | 1663.67 | 30.80 | 19.67 | 33.84 | 907 | 1.48% |

## Validation Checks

### ✅ No Unexpected Negative Values

### ✅ No Infinite Values

### Outlier Detection (Values > 3 Standard Deviations)

- `txn_hour_mode`: 907 outliers (1.48%)
- `after_hours_txn_pct`: 2,473 outliers (4.03%)
- `weekend_txn_count`: 795 outliers (1.29%)
- `weekend_txn_pct`: 611 outliers (0.99%)
- `midnight_txn_count`: 720 outliers (1.17%)
- `early_morning_txn_count`: 954 outliers (1.55%)
- `late_night_txn_count`: 797 outliers (1.30%)
- `midnight_txn_pct`: 725 outliers (1.18%)
- `time_between_txn_mean`: 1,087 outliers (1.77%)
- `time_between_txn_median`: 1,060 outliers (1.73%)

... and 11 more features with outliers

## Flag Feature Distributions

| Feature | True Count | True Percentage | False Count | False Percentage |
|---------|------------|-----------------|-------------|------------------|
| `after_hours_flag` | 11,593 | 18.88% | 49,817 | 81.12% |
| `weekend_heavy_flag` | 41,767 | 68.01% | 19,643 | 31.99% |
| `unusual_hours_flag` | 53,340 | 86.86% | 8,070 | 13.14% |
| `rapid_fire_flag` | 15,219 | 24.78% | 46,191 | 75.22% |
| `consistent_timing_flag` | 77 | 0.13% | 61,333 | 99.87% |

## Summary

- ✅ **Total Features**: 25
- ✅ **Data Completeness**: 4.00%
- ✅ **Customers Covered**: 61,410
- ✅ **Flag Features**: 5

---
*Report generated automatically by feature engineering pipeline*
