# Feature Report: Profile Features
**Generated**: 2026-01-27 15:31:01
---

## Basic Information

- **Total Customers**: 61,410
- **Total Features**: 28
- **Feature Columns**: account_age, business_age, new_account_flag, very_new_business_flag, is_oil_company, is_msb_business, is_maybe_massage_parlor, is_ecom_business, is_hotel_or_motel, is_shell_company, is_cash_intensive, is_real_estate, is_precious_metal_business, is_professional_service, is_transportation, is_vague_category, has_missing_income, has_missing_sales, has_missing_industry_occupation, has_missing_country, has_missing_province, has_missing_city, industry_code_high_risk_trade, suspicious_occupation_flag, is_individual, is_business, profile_risk_score, high_profile_risk

## Data Quality Checks

### ✅ No Null Values

All features have complete data.

### ✅ No Duplicate Customer IDs

## Feature Statistics

| Feature | Type | Min | Max | Mean | Median | Std Dev | Zero Count | Zero % |
|---------|------|-----|-----|------|--------|---------|------------|--------|
| `account_age` | Integer | 0 | 123 | 14.01 | 11 | 11.68 | 4,862 | 7.92% |
| `business_age` | Integer | 0 | 155 | 40.24 | 39 | 23.78 | 3,936 | 6.41% |
| `new_account_flag` | Integer | 0 | 1 | 0.08 | 0 | 0.27 | 56,548 | 92.08% |
| `very_new_business_flag` | Integer | 0 | 1 | 0.01 | 0 | 0.08 | 61,000 | 99.33% |
| `is_oil_company` | Integer | 0 | 1 | 0.00 | 0 | 0.03 | 61,340 | 99.89% |
| `is_msb_business` | Integer | 0 | 1 | 0.01 | 0 | 0.11 | 60,723 | 98.88% |
| `is_maybe_massage_parlor` | Integer | 0 | 1 | 0.00 | 0 | 0.04 | 61,293 | 99.81% |
| `is_ecom_business` | Integer | 0 | 1 | 0.01 | 0 | 0.07 | 61,085 | 99.47% |
| `is_hotel_or_motel` | Integer | 0 | 1 | 0.00 | 0 | 0.02 | 61,374 | 99.94% |
| `is_shell_company` | Integer | 0 | 1 | 0.02 | 0 | 0.15 | 60,081 | 97.84% |
| `is_cash_intensive` | Integer | 0 | 1 | 0.00 | 0 | 0.07 | 61,134 | 99.55% |
| `is_real_estate` | Integer | 0 | 1 | 0.00 | 0 | 0.07 | 61,147 | 99.57% |
| `is_precious_metal_business` | Integer | 0 | 1 | 0.00 | 0 | 0.03 | 61,366 | 99.93% |
| `is_professional_service` | Integer | 0 | 1 | 0.01 | 0 | 0.11 | 60,697 | 98.84% |
| `is_transportation` | Integer | 0 | 1 | 0.01 | 0 | 0.08 | 61,015 | 99.36% |
| `is_vague_category` | Integer | 0 | 1 | 0.01 | 0 | 0.08 | 61,048 | 99.41% |
| `has_missing_income` | Integer | 0 | 1 | 0.37 | 0 | 0.48 | 38,421 | 62.56% |
| `has_missing_sales` | Integer | 0 | 1 | 0.93 | 1 | 0.25 | 4,033 | 6.57% |
| `has_missing_industry_occupation` | Integer | 0 | 1 | 0.00 | 0 | 0.04 | 61,303 | 99.83% |
| `has_missing_country` | Integer | 0 | 0 | 0.00 | 0 | 0.00 | 61,410 | 100.00% |
| `has_missing_province` | Integer | 0 | 0 | 0.00 | 0 | 0.00 | 61,410 | 100.00% |
| `has_missing_city` | Integer | 0 | 0 | 0.00 | 0 | 0.00 | 61,410 | 100.00% |
| `industry_code_high_risk_trade` | Integer | 0 | 1 | 0.02 | 0 | 0.15 | 60,068 | 97.81% |
| `suspicious_occupation_flag` | Integer | 0 | 1 | 0.02 | 0 | 0.15 | 59,906 | 97.55% |
| `is_individual` | Integer | 0 | 1 | 0.86 | 1 | 0.34 | 8,311 | 13.53% |
| `is_business` | Integer | 0 | 1 | 0.14 | 0 | 0.34 | 53,099 | 86.47% |
| `profile_risk_score` | Integer | 1 | 13 | 1.58 | 1 | 1.20 | 0 | 0.00% |
| `high_profile_risk` | Integer | 0 | 1 | 0.07 | 0 | 0.26 | 57,099 | 92.98% |

## Validation Checks

### ✅ No Unexpected Negative Values

### ✅ No Infinite Values

### Outlier Detection (Values > 3 Standard Deviations)

- `account_age`: 40 outliers (0.07%)
- `business_age`: 8 outliers (0.01%)
- `new_account_flag`: 4,862 outliers (7.92%)
- `very_new_business_flag`: 410 outliers (0.67%)
- `is_oil_company`: 70 outliers (0.11%)
- `is_msb_business`: 687 outliers (1.12%)
- `is_maybe_massage_parlor`: 117 outliers (0.19%)
- `is_ecom_business`: 325 outliers (0.53%)
- `is_hotel_or_motel`: 36 outliers (0.06%)
- `is_shell_company`: 1,329 outliers (2.16%)

... and 12 more features with outliers

## Flag Feature Distributions

| Feature | True Count | True Percentage | False Count | False Percentage |
|---------|------------|-----------------|-------------|------------------|
| `new_account_flag` | 4,862 | 7.92% | 56,548 | 92.08% |
| `very_new_business_flag` | 410 | 0.67% | 61,000 | 99.33% |
| `suspicious_occupation_flag` | 1,504 | 2.45% | 59,906 | 97.55% |

## Summary

- ✅ **Total Features**: 28
- ✅ **Data Completeness**: 3.57%
- ✅ **Customers Covered**: 61,410
- ✅ **Flag Features**: 3

---
*Report generated automatically by feature engineering pipeline*
