# Feature Report: Master Features
**Generated**: 2026-01-27 15:31:57
---

## Basic Information

- **Total Customers**: 61,410
- **Total Features**: 182
- **Feature Columns**: kyc_type, txn_count_total, txn_per_day_avg, txn_velocity, high_frequency_customer_flag, volume_debit_total, volume_credit_total, account_turnover_rate, flow_through_velocity_hours, time_between_deposit_withdrawal, sudden_inflow_outflow_pattern, txn_count_eft, volume_eft_total, txn_velocity_eft, volume_eft_sudden_increase, txn_count_eft_spike, velocity_change_eft, amount_mean, amount_stddev, amount_min, amount_max, amount_median, round_amount_count, round_amount_pct, round_amount_flag, just_below_threshold_count, structuring_pattern_flag, large_txn_count_10k, large_txn_count_50k, large_txn_count_100k, amount_max_ratio_mean, amount_stddev_ratio_mean, amount_cv_by_channel, amount_near_50k_increment_count, channels_used_count, multi_channel_flag, wire_txn_count, wire_volume_total, wire_volume_avg, wire_volume_max, wire_large_count, has_wire_transfers, abm_cash_txn_count, abm_cash_volume, abm_cash_volume_avg, abm_cash_volume_max, abm_cash_large_count, abm_cash_pct, structured_cash_deposits_same_day, western_union_txn_count, western_union_volume_total, western_union_volume_avg, has_western_union, eft_txn_count, eft_volume_total, eft_volume_avg, emt_txn_count, emt_volume_total, emt_volume_avg, card_ecommerce_txn_count, card_ecommerce_pct, card_txn_count, card_volume_total, card_volume_avg, cheque_txn_count, cheque_volume_total, cheque_volume_avg, cheque_volume_max, cheque_large_count, country_diversity, province_diversity, city_diversity, cross_border_txn_count, cross_border_txn_pct, cross_border_flag, is_country_financial_hub, is_country_offshore_structure_jurisdiction, is_country_trade_conduit, is_country_private_banking_hub, is_country_shell_company_jurisdiction, is_country_tbml_high_risk, is_country_major_port, is_country_real_estate_ml_risk, is_country_hnwi_concentration, is_country_high_cash_usage, txn_per_unique_location, high_geographic_dispersion, customer_country_financial_hub, customer_country_offshore_structure_jurisdiction, customer_country_trade_conduit, customer_country_private_banking_hub, customer_country_shell_company_jurisdiction, customer_country_tbml_high_risk, customer_country_major_port, customer_country_real_estate_ml_risk, customer_country_hnwi_concentration, customer_country_high_cash_usage, txn_hour_mode, after_hours_txn_pct, after_hours_flag, weekend_txn_count, weekend_txn_pct, weekend_heavy_flag, midnight_txn_count, early_morning_txn_count, late_night_txn_count, midnight_txn_pct, unusual_hours_flag, time_between_txn_mean, time_between_txn_median, time_between_txn_min, time_between_txn_max, time_between_txn_std, very_short_time_between_txn, rapid_fire_txn_count, rapid_fire_flag, txn_hour_std, consistent_timing_flag, business_hours_txn_pct, non_business_hours_heavy, months_active, txn_per_month, total_volume, avg_transaction_amount, max_transaction_amount, transaction_amount_std, amount_to_income_ratio, amount_to_sales_ratio, amount_to_revenue_ratio, lifestyle_mismatch, severe_lifestyle_mismatch, has_missing_income, has_missing_sales, amount_cv, high_amount_variability, debit_volume, credit_volume, net_flow, debit_credit_ratio, high_debit_ratio, max_txn_to_income_ratio, max_txn_to_sales_ratio, max_txn_to_revenue_ratio, single_txn_exceeds_revenue, txn_count_total_behavioral, transaction_consistency, consistent_pattern_flag, behavioral_risk_score, high_behavioral_risk, account_age, business_age, new_account_flag, very_new_business_flag, is_oil_company, is_msb_business, is_maybe_massage_parlor, is_ecom_business, is_hotel_or_motel, is_shell_company, is_cash_intensive, is_real_estate, is_precious_metal_business, is_professional_service, is_transportation, is_vague_category, has_missing_income_profile, has_missing_sales_profile, has_missing_industry_occupation, has_missing_country, has_missing_province, has_missing_city, industry_code_high_risk_trade, suspicious_occupation_flag, is_individual, is_business, profile_risk_score, high_profile_risk, txn_score_max, txn_score_mean, txn_score_std, txn_score_count_above_threshold, txn_score_pct_above_threshold

## Data Quality Checks

### ✅ No Null Values

All features have complete data.

### ✅ No Duplicate Customer IDs

## Feature Statistics

| Feature | Type | Min | Max | Mean | Median | Std Dev | Zero Count | Zero % |
|---------|------|-----|-----|------|--------|---------|------------|--------|
| `kyc_type` | object | N/A | N/A | N/A | N/A | N/A | 0 | 0.00% |
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
| `txn_count_total_behavioral` | Integer | 1 | 4,991 | 96.13 | 63 | 102.92 | 0 | 0.00% |
| `transaction_consistency` | Float | 0.00 | 1.00 | 0.33 | 0.32 | 0.12 | 6 | 0.01% |
| `consistent_pattern_flag` | Integer | 0 | 0 | 0.00 | 0 | 0.00 | 61,410 | 100.00% |
| `behavioral_risk_score` | Integer | 0 | 9 | 2.35 | 1 | 2.66 | 12,844 | 20.92% |
| `high_behavioral_risk` | Integer | 0 | 1 | 0.25 | 0 | 0.44 | 45,809 | 74.60% |
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
| `has_missing_income_profile` | Integer | 0 | 1 | 0.37 | 0 | 0.48 | 38,421 | 62.56% |
| `has_missing_sales_profile` | Integer | 0 | 1 | 0.93 | 1 | 0.25 | 4,033 | 6.57% |
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
| `txn_score_max` | Float | 0.00 | 0.60 | 0.13 | 0.20 | 0.12 | 22,366 | 36.42% |
| `txn_score_mean` | Float | 0.00 | 0.60 | 0.01 | 0.00 | 0.02 | 22,366 | 36.42% |
| `txn_score_std` | Float | 0.00 | 0.42 | 0.03 | 0.02 | 0.03 | 22,440 | 36.54% |
| `txn_score_count_above_threshold` | Integer | 0 | 26 | 0.01 | 0 | 0.20 | 60,978 | 99.30% |
| `txn_score_pct_above_threshold` | Float | 0.00 | 1.00 | 0.00 | 0.00 | 0.01 | 60,978 | 99.30% |

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

... and 127 more features with outliers

## Flag Feature Distributions

| Feature | True Count | True Percentage | False Count | False Percentage |
|---------|------------|-----------------|-------------|------------------|
| `high_frequency_customer_flag` | 365 | 0.59% | 61,045 | 99.41% |
| `round_amount_flag` | 14 | 0.02% | 61,396 | 99.98% |
| `structuring_pattern_flag` | 232 | 0.38% | 61,178 | 99.62% |
| `multi_channel_flag` | 45,204 | 73.61% | 16,206 | 26.39% |
| `cross_border_flag` | 41,958 | 68.32% | 19,452 | 31.68% |
| `after_hours_flag` | 11,593 | 18.88% | 49,817 | 81.12% |
| `weekend_heavy_flag` | 41,767 | 68.01% | 19,643 | 31.99% |
| `unusual_hours_flag` | 53,340 | 86.86% | 8,070 | 13.14% |
| `rapid_fire_flag` | 15,219 | 24.78% | 46,191 | 75.22% |
| `consistent_timing_flag` | 77 | 0.13% | 61,333 | 99.87% |
| `consistent_pattern_flag` | 0 | 0.00% | 61,410 | 100.00% |
| `new_account_flag` | 4,862 | 7.92% | 56,548 | 92.08% |
| `very_new_business_flag` | 410 | 0.67% | 61,000 | 99.33% |
| `suspicious_occupation_flag` | 1,504 | 2.45% | 59,906 | 97.55% |

## Summary

- ✅ **Total Features**: 182
- ✅ **Data Completeness**: 0.55%
- ✅ **Customers Covered**: 61,410
- ✅ **Flag Features**: 14

---
*Report generated automatically by feature engineering pipeline*
