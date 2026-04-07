# Feature Report: Channel Features
**Generated**: 2026-01-27 15:28:45
---

## Basic Information

- **Total Customers**: 61,410
- **Total Features**: 35
- **Feature Columns**: channels_used_count, multi_channel_flag, wire_txn_count, wire_volume_total, wire_volume_avg, wire_volume_max, wire_large_count, has_wire_transfers, abm_cash_txn_count, abm_cash_volume, abm_cash_volume_avg, abm_cash_volume_max, abm_cash_large_count, abm_cash_pct, structured_cash_deposits_same_day, western_union_txn_count, western_union_volume_total, western_union_volume_avg, has_western_union, eft_txn_count, eft_volume_total, eft_volume_avg, emt_txn_count, emt_volume_total, emt_volume_avg, card_ecommerce_txn_count, card_ecommerce_pct, card_txn_count, card_volume_total, card_volume_avg, cheque_txn_count, cheque_volume_total, cheque_volume_avg, cheque_volume_max, cheque_large_count

## Data Quality Checks

### ✅ No Null Values

All features have complete data.

### ✅ No Duplicate Customer IDs

## Feature Statistics

| Feature | Type | Min | Max | Mean | Median | Std Dev | Zero Count | Zero % |
|---------|------|-----|-----|------|--------|---------|------------|--------|
| `channels_used_count` | Integer | 1 | 7 | 3.36 | 4 | 1.32 | 0 | 0.00% |
| `multi_channel_flag` | Integer | 0 | 1 | 0.74 | 1 | 0.44 | 16,206 | 26.39% |
| `wire_txn_count` | Integer | 0 | 467 | 0.08 | 0 | 2.06 | 59,375 | 96.69% |
| `wire_volume_total` | Float | 0.00 | 2051810761.00 | 359996.42 | 0.00 | 12658290.86 | 59,375 | 96.69% |
| `wire_volume_avg` | Float | 0.00 | 2051810761.00 | 140638.16 | 0.00 | 8948653.09 | 59,375 | 96.69% |
| `wire_volume_max` | Float | 0.00 | 2051810761.00 | 283374.76 | 0.00 | 11138066.69 | 59,375 | 96.69% |
| `wire_large_count` | Integer | 0 | 65 | 0.03 | 0 | 0.43 | 60,464 | 98.46% |
| `has_wire_transfers` | Integer | 0 | 1 | 0.03 | 0 | 0.18 | 59,375 | 96.69% |
| `abm_cash_txn_count` | Integer | 0 | 294 | 2.68 | 0 | 6.06 | 30,984 | 50.45% |
| `abm_cash_volume` | Float | 0.00 | 7729793.00 | 78347.04 | 0.00 | 201468.45 | 30,984 | 50.45% |
| `abm_cash_volume_avg` | Float | 0.00 | 1890000.00 | 14642.29 | 0.00 | 27433.95 | 30,984 | 50.45% |
| `abm_cash_volume_max` | Float | 0.00 | 5473000.00 | 32498.58 | 0.00 | 75546.76 | 30,984 | 50.45% |
| `abm_cash_large_count` | Integer | 0 | 8 | 0.00 | 0 | 0.07 | 61,245 | 99.73% |
| `abm_cash_pct` | Float | 0.00 | 1.00 | 0.45 | 0.00 | 0.47 | 30,984 | 50.45% |
| `structured_cash_deposits_same_day` | Integer | 0 | 1 | 0.00 | 0 | 0.01 | 61,407 | 100.00% |
| `western_union_txn_count` | Integer | 0 | 24 | 0.03 | 0 | 0.47 | 60,735 | 98.90% |
| `western_union_volume_total` | Float | 0.00 | 1325575.00 | 1244.83 | 0.00 | 18111.68 | 60,735 | 98.90% |
| `western_union_volume_avg` | Float | 0.00 | 410378.00 | 402.98 | 0.00 | 4859.64 | 60,735 | 98.90% |
| `has_western_union` | Integer | 0 | 1 | 0.01 | 0 | 0.10 | 60,735 | 98.90% |
| `eft_txn_count` | Integer | 0 | 4,959 | 17.44 | 11 | 43.14 | 10,863 | 17.69% |
| `eft_volume_total` | Float | 0.00 | 2675109760.00 | 2750979.67 | 790347.50 | 21009517.50 | 10,863 | 17.69% |
| `eft_volume_avg` | Float | 0.00 | 93885128.67 | 103304.91 | 60811.11 | 654431.91 | 10,863 | 17.69% |
| `emt_txn_count` | Integer | 0 | 1,948 | 13.78 | 6 | 31.19 | 18,518 | 30.15% |
| `emt_volume_total` | Float | 0.00 | 81206623.00 | 584529.65 | 176767.00 | 1618428.24 | 18,518 | 30.15% |
| `emt_volume_avg` | Float | 0.00 | 1100756.50 | 29378.88 | 23057.12 | 39124.60 | 18,518 | 30.15% |
| `card_ecommerce_txn_count` | Integer | 0 | 155 | 8.47 | 2 | 13.01 | 21,458 | 34.94% |
| `card_ecommerce_pct` | Float | 0.00 | 1.00 | 0.12 | 0.12 | 0.13 | 21,458 | 34.94% |
| `card_txn_count` | Integer | 0 | 974 | 57.86 | 17 | 85.71 | 12,184 | 19.84% |
| `card_volume_total` | Float | 0.00 | 26289170.00 | 566823.66 | 120248.50 | 1358013.20 | 12,295 | 20.02% |
| `card_volume_avg` | Float | 0.00 | 3581565.00 | 8714.93 | 5561.91 | 39065.45 | 12,295 | 20.02% |
| `cheque_txn_count` | Integer | 0 | 1,186 | 3.92 | 0 | 19.38 | 31,806 | 51.79% |
| `cheque_volume_total` | Float | 0.00 | 867939383.00 | 1719608.04 | 0.00 | 13954568.59 | 31,806 | 51.79% |
| `cheque_volume_avg` | Float | 0.00 | 113648725.00 | 147925.21 | 0.00 | 1176734.58 | 31,806 | 51.79% |
| `cheque_volume_max` | Float | 0.00 | 567888708.00 | 921058.13 | 0.00 | 7782465.08 | 31,806 | 51.79% |
| `cheque_large_count` | Integer | 0 | 103 | 0.24 | 0 | 1.67 | 55,686 | 90.68% |

## Validation Checks

### ✅ No Unexpected Negative Values

### ✅ No Infinite Values

### Outlier Detection (Values > 3 Standard Deviations)

- `wire_txn_count`: 65 outliers (0.11%)
- `wire_volume_total`: 99 outliers (0.16%)
- `wire_volume_avg`: 39 outliers (0.06%)
- `wire_volume_max`: 83 outliers (0.14%)
- `wire_large_count`: 260 outliers (0.42%)
- `has_wire_transfers`: 2,035 outliers (3.31%)
- `abm_cash_txn_count`: 1,126 outliers (1.83%)
- `abm_cash_volume`: 1,020 outliers (1.66%)
- `abm_cash_volume_avg`: 986 outliers (1.61%)
- `abm_cash_volume_max`: 873 outliers (1.42%)

... and 22 more features with outliers

## Flag Feature Distributions

| Feature | True Count | True Percentage | False Count | False Percentage |
|---------|------------|-----------------|-------------|------------------|
| `multi_channel_flag` | 45,204 | 73.61% | 16,206 | 26.39% |

## Summary

- ✅ **Total Features**: 35
- ✅ **Data Completeness**: 2.86%
- ✅ **Customers Covered**: 61,410
- ✅ **Flag Features**: 1

---
*Report generated automatically by feature engineering pipeline*
