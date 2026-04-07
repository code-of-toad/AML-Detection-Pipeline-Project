# Feature Report: Velocity Features
**Generated**: 2026-01-27 15:27:49
---

## Basic Information

- **Total Customers**: 61,410
- **Total Features**: 16
- **Feature Columns**: txn_count_total, txn_per_day_avg, txn_velocity, high_frequency_customer_flag, volume_debit_total, volume_credit_total, account_turnover_rate, flow_through_velocity_hours, time_between_deposit_withdrawal, sudden_inflow_outflow_pattern, txn_count_eft, volume_eft_total, txn_velocity_eft, volume_eft_sudden_increase, txn_count_eft_spike, velocity_change_eft

## Data Quality Checks

### ✅ No Null Values

All features have complete data.

### ✅ No Duplicate Customer IDs

## Feature Statistics

| Feature | Type | Min | Max | Mean | Median | Std Dev | Zero Count | Zero % |
|---------|------|-----|-----|------|--------|---------|------------|--------|
| `txn_count_total` | Integer | 1 | 4,991 | 96.13 | 63 | 102.92 | 0 | 0.00% |
| `txn_per_day_avg` | Float | 0.00 | 393.00 | 1.19 | 0.72 | 3.97 | 907 | 1.48% |
| `txn_velocity` | Float | 0.00 | 393.00 | 1.19 | 0.72 | 3.97 | 907 | 1.48% |
| `high_frequency_customer_flag` | Integer | 0 | 1 | 0.01 | 0 | 0.08 | 61,045 | 99.41% |
| `volume_debit_total` | Float | 0.00 | 1437637276.00 | 2861381.83 | 886504.50 | 14983096.02 | 550 | 0.90% |
| `volume_credit_total` | Float | 0.00 | 2052481891.00 | 3259518.81 | 1213366.50 | 18248172.39 | 2,080 | 3.39% |
| `account_turnover_rate` | Float | 0.00 | 10.00 | 1.87 | 0.77 | 2.73 | 550 | 0.90% |
| `flow_through_velocity_hours` | Float | 0.00 | 2184.00 | 57.24 | 28.17 | 108.68 | 4,391 | 7.15% |
| `time_between_deposit_withdrawal` | Float | 0.00 | 2184.00 | 57.24 | 28.17 | 108.68 | 4,391 | 7.15% |
| `sudden_inflow_outflow_pattern` | Integer | 0 | 1 | 0.79 | 1 | 0.41 | 13,171 | 21.45% |
| `txn_count_eft` | Integer | 0 | 4,959 | 17.44 | 11 | 43.14 | 10,863 | 17.69% |
| `volume_eft_total` | Float | 0.00 | 2675109760.00 | 2750979.67 | 790347.50 | 21009517.50 | 10,863 | 17.69% |
| `txn_velocity_eft` | Float | 0.00 | 53.35 | 0.24 | 0.16 | 0.48 | 10,863 | 17.69% |
| `volume_eft_sudden_increase` | Integer | 0 | 1 | 0.16 | 0 | 0.37 | 51,582 | 84.00% |
| `txn_count_eft_spike` | Integer | 0 | 0 | 0.00 | 0 | 0.00 | 61,410 | 100.00% |
| `velocity_change_eft` | Integer | 0 | 0 | 0.00 | 0 | 0.00 | 61,410 | 100.00% |

## Validation Checks

### ✅ No Unexpected Negative Values

### ✅ No Infinite Values

### Outlier Detection (Values > 3 Standard Deviations)

- `txn_count_total`: 924 outliers (1.50%)
- `txn_per_day_avg`: 145 outliers (0.24%)
- `txn_velocity`: 145 outliers (0.24%)
- `high_frequency_customer_flag`: 365 outliers (0.59%)
- `volume_debit_total`: 544 outliers (0.89%)
- `volume_credit_total`: 363 outliers (0.59%)
- `flow_through_velocity_hours`: 1,009 outliers (1.64%)
- `time_between_deposit_withdrawal`: 1,009 outliers (1.64%)
- `txn_count_eft`: 380 outliers (0.62%)
- `volume_eft_total`: 326 outliers (0.53%)

... and 1 more features with outliers

## Flag Feature Distributions

| Feature | True Count | True Percentage | False Count | False Percentage |
|---------|------------|-----------------|-------------|------------------|
| `high_frequency_customer_flag` | 365 | 0.59% | 61,045 | 99.41% |

## Summary

- ✅ **Total Features**: 16
- ✅ **Data Completeness**: 6.25%
- ✅ **Customers Covered**: 61,410
- ✅ **Flag Features**: 1

---
*Report generated automatically by feature engineering pipeline*
