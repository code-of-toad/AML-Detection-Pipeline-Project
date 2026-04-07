# Feature Report: Geographic Features
**Generated**: 2026-01-27 15:29:38
---

## Basic Information

- **Total Customers**: 61,410
- **Total Features**: 28
- **Feature Columns**: country_diversity, province_diversity, city_diversity, cross_border_txn_count, cross_border_txn_pct, cross_border_flag, is_country_financial_hub, is_country_offshore_structure_jurisdiction, is_country_trade_conduit, is_country_private_banking_hub, is_country_shell_company_jurisdiction, is_country_tbml_high_risk, is_country_major_port, is_country_real_estate_ml_risk, is_country_hnwi_concentration, is_country_high_cash_usage, txn_per_unique_location, high_geographic_dispersion, customer_country_financial_hub, customer_country_offshore_structure_jurisdiction, customer_country_trade_conduit, customer_country_private_banking_hub, customer_country_shell_company_jurisdiction, customer_country_tbml_high_risk, customer_country_major_port, customer_country_real_estate_ml_risk, customer_country_hnwi_concentration, customer_country_high_cash_usage

## Data Quality Checks

### ✅ No Null Values

All features have complete data.

### ✅ No Duplicate Customer IDs

## Feature Statistics

| Feature | Type | Min | Max | Mean | Median | Std Dev | Zero Count | Zero % |
|---------|------|-----|-----|------|--------|---------|------------|--------|
| `country_diversity` | Integer | 0 | 12 | 2.34 | 2 | 1.77 | 11,979 | 19.51% |
| `province_diversity` | Integer | 0 | 20 | 6.60 | 7 | 4.83 | 11,980 | 19.51% |
| `city_diversity` | Integer | 0 | 96 | 16.42 | 9 | 17.61 | 11,972 | 19.50% |
| `cross_border_txn_count` | Integer | 0 | 196 | 10.83 | 3 | 16.36 | 19,452 | 31.68% |
| `cross_border_txn_pct` | Float | 0.00 | 1.00 | 0.14 | 0.14 | 0.14 | 19,452 | 31.68% |
| `cross_border_flag` | Integer | 0 | 1 | 0.68 | 1 | 0.47 | 19,452 | 31.68% |
| `is_country_financial_hub` | Integer | 0 | 1 | 0.39 | 0 | 0.49 | 37,707 | 61.40% |
| `is_country_offshore_structure_jurisdiction` | Integer | 0 | 1 | 0.13 | 0 | 0.34 | 53,429 | 87.00% |
| `is_country_trade_conduit` | Integer | 0 | 1 | 0.08 | 0 | 0.28 | 56,219 | 91.55% |
| `is_country_private_banking_hub` | Integer | 0 | 1 | 0.07 | 0 | 0.26 | 56,958 | 92.75% |
| `is_country_shell_company_jurisdiction` | Integer | 0 | 1 | 0.19 | 0 | 0.39 | 49,921 | 81.29% |
| `is_country_tbml_high_risk` | Integer | 0 | 1 | 0.08 | 0 | 0.28 | 56,219 | 91.55% |
| `is_country_major_port` | Integer | 0 | 1 | 0.08 | 0 | 0.28 | 56,219 | 91.55% |
| `is_country_real_estate_ml_risk` | Integer | 0 | 1 | 0.80 | 1 | 0.40 | 12,360 | 20.13% |
| `is_country_hnwi_concentration` | Integer | 0 | 1 | 0.07 | 0 | 0.26 | 56,958 | 92.75% |
| `is_country_high_cash_usage` | Integer | 0 | 1 | 0.04 | 0 | 0.20 | 58,802 | 95.75% |
| `txn_per_unique_location` | Float | 0.00 | 15.00 | 1.64 | 1.53 | 1.16 | 11,972 | 19.50% |
| `high_geographic_dispersion` | Integer | 0 | 1 | 0.67 | 1 | 0.47 | 20,221 | 32.93% |
| `customer_country_financial_hub` | Integer | 0 | 0 | 0.00 | 0 | 0.00 | 61,410 | 100.00% |
| `customer_country_offshore_structure_jurisdiction` | Integer | 0 | 0 | 0.00 | 0 | 0.00 | 61,410 | 100.00% |
| `customer_country_trade_conduit` | Integer | 0 | 0 | 0.00 | 0 | 0.00 | 61,410 | 100.00% |
| `customer_country_private_banking_hub` | Integer | 0 | 0 | 0.00 | 0 | 0.00 | 61,410 | 100.00% |
| `customer_country_shell_company_jurisdiction` | Integer | 0 | 0 | 0.00 | 0 | 0.00 | 61,410 | 100.00% |
| `customer_country_tbml_high_risk` | Integer | 0 | 0 | 0.00 | 0 | 0.00 | 61,410 | 100.00% |
| `customer_country_major_port` | Integer | 0 | 0 | 0.00 | 0 | 0.00 | 61,410 | 100.00% |
| `customer_country_real_estate_ml_risk` | Integer | 1 | 1 | 1.00 | 1 | 0.00 | 0 | 0.00% |
| `customer_country_hnwi_concentration` | Integer | 0 | 0 | 0.00 | 0 | 0.00 | 61,410 | 100.00% |
| `customer_country_high_cash_usage` | Integer | 0 | 0 | 0.00 | 0 | 0.00 | 61,410 | 100.00% |

## Validation Checks

### ✅ No Unexpected Negative Values

### ✅ No Infinite Values

### Outlier Detection (Values > 3 Standard Deviations)

- `country_diversity`: 314 outliers (0.51%)
- `city_diversity`: 388 outliers (0.63%)
- `cross_border_txn_count`: 1,271 outliers (2.07%)
- `cross_border_txn_pct`: 719 outliers (1.17%)
- `is_country_trade_conduit`: 5,191 outliers (8.45%)
- `is_country_private_banking_hub`: 4,452 outliers (7.25%)
- `is_country_tbml_high_risk`: 5,191 outliers (8.45%)
- `is_country_major_port`: 5,191 outliers (8.45%)
- `is_country_hnwi_concentration`: 4,452 outliers (7.25%)
- `is_country_high_cash_usage`: 2,608 outliers (4.25%)

... and 1 more features with outliers

## Flag Feature Distributions

| Feature | True Count | True Percentage | False Count | False Percentage |
|---------|------------|-----------------|-------------|------------------|
| `cross_border_flag` | 41,958 | 68.32% | 19,452 | 31.68% |

## Summary

- ✅ **Total Features**: 28
- ✅ **Data Completeness**: 3.57%
- ✅ **Customers Covered**: 61,410
- ✅ **Flag Features**: 1

---
*Report generated automatically by feature engineering pipeline*
