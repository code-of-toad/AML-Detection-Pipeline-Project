# Red Flag to Feature Mapping

## Purpose

This document maps AML red flags and indicators from the Knowledge Library to:
1. **Data Signals** - What patterns in the data indicate this red flag
2. **Engineered Features** - Specific features to create for model detection
3. **Feature Categories** - How features group together

This mapping enables:
- **Task 2**: Feature engineering based on AML knowledge
- **Task 3**: Explaining model decisions using red flag context

---

## Mapping Structure

For each red flag:
- **Red Flag**: Description of the suspicious pattern
- **Data Signal**: What to look for in transaction/KYC data
- **Features to Engineer**: Specific features that detect this pattern
- **Source**: Which knowledge library document contains this red flag

---

## 1. Trade-Based Money Laundering Features

### Red Flag: Phantom Shipments
- **Data Signal**: Large EFT payments to trading companies with no corresponding goods movement
- **Features**:
  - `volume_eft_to_trading_companies` (SUM of EFT to trading company merchant categories)
  - `txn_count_eft_to_trading_companies` (COUNT of EFT to trading companies)
  - `eft_to_trading_ratio` (Percentage of EFT going to trading companies)
- **Source**: `01_Professional_Money_Laundering_Trade_MSB.md`

### Red Flag: Over/Under Invoicing
- **Data Signal**: Transaction amounts significantly different from market prices
- **Features**:
  - `amount_vs_market_price_deviation` (Deviation from typical prices for merchant category)
  - `over_invoice_flag` (Boolean: amount > 2x typical price)
  - `under_invoice_flag` (Boolean: amount < 0.5x typical price)
- **Source**: `01_Professional_Money_Laundering_Trade_MSB.md`

### Red Flag: Round Figure Payments
- **Data Signal**: Transactions in round numbers (e.g., $50,000, $100,000)
- **Features**:
  - `round_amount_flag` (Boolean: amount is round number)
  - `just_below_threshold_count` (COUNT: transactions $9,000-$10,000)
  - `amount_modulo_50000` (Remainder when divided by $50,000 - detects $50K increments)
- **Source**: `01_Professional_Money_Laundering_Trade_MSB.md`

### Red Flag: Flow-Through Activity
- **Data Signal**: Money taken or transferred out as quickly as it flows in
- **Features**:
  - `flow_through_velocity` (Average time between deposit and withdrawal)
  - `time_between_deposit_withdrawal` (Hours between credit and debit)
  - `account_turnover_rate` (Volume out / Volume in ratio)
- **Source**: `01_Professional_Money_Laundering_Trade_MSB.md`

---

## 2. Geographic Risk Features

### Red Flag: High-Risk Country Transactions
- **Data Signal**: Transactions to/from sanctioned countries, offshore financial centers, or high-risk jurisdictions
- **Features**:
  - `high_risk_country_transaction_count` (COUNT: transactions to/from high-risk countries)
  - `offshore_financial_center_flag` (Boolean: transaction to/from offshore center)
  - `sanctioned_country_transactions` (COUNT: transactions to/from sanctioned countries)
  - `volume_eft_to_china_hk` (SUM: EFT volume to China/Hong Kong)
  - `volume_eft_from_latin_america` (SUM: EFT volume from Latin America)
  - `volume_eft_from_uae` (SUM: EFT volume from UAE)
- **Source**: `01_Professional_Money_Laundering_Trade_MSB.md`

### Red Flag: Cross-Border Patterns
- **Data Signal**: Unusual cross-border transaction patterns
- **Features**:
  - `cross_border_flows` (COUNT: transactions crossing borders)
  - `high_risk_geography_flag` (Boolean: transaction involves high-risk geography)
  - `country_diversity` (COUNT: unique countries in transactions)
- **Source**: `01_Professional_Money_Laundering_Trade_MSB.md`

---

## 3. Transaction Velocity Features

### Red Flag: Sudden Inflow/Outflow Patterns
- **Data Signal**: Sudden increase in deposits followed by multiple outgoing payments
- **Features**:
  - `sudden_inflow_outflow_pattern` (Boolean: large inflow followed by multiple outflows)
  - `volume_eft_sudden_increase` (Change in EFT volume over time window)
  - `txn_count_eft_spike` (Sudden increase in EFT transaction count)
  - `velocity_change_eft` (Rate of change in EFT velocity)
- **Source**: `01_Professional_Money_Laundering_Trade_MSB.md`

### Red Flag: High Transaction Frequency
- **Data Signal**: Unusually high number of transactions
- **Features**:
  - `txn_count_total` (Total transaction count)
  - `txn_per_day_avg` (Average transactions per day)
  - `txn_velocity` (Transactions per day)
  - `high_frequency_customer_flag` (Boolean: >500 transactions)
- **Source**: General indicators + Data insights

---

## 4. Channel-Specific Risk Features

### Red Flag: Wire Transfer Usage
- **Data Signal**: Use of wire transfers, especially high-value
- **Features**:
  - `wire_txn_count` (COUNT: wire transactions)
  - `wire_volume_total` (SUM: wire transaction volume)
  - `wire_volume_avg` (AVG: average wire transaction amount)
  - `wire_large_count` (COUNT: wire transfers > $10K)
  - `has_wire_transfers` (Boolean: customer uses wire transfers)
- **Source**: `01_Professional_Money_Laundering_Trade_MSB.md` + Data insights

### Red Flag: Cash Transactions
- **Data Signal**: Large or frequent cash transactions
- **Features**:
  - `abm_cash_txn_count` (COUNT: cash withdrawal transactions)
  - `abm_cash_volume` (SUM: cash withdrawal volume)
  - `abm_cash_pct` (Percentage of ABM transactions that are cash)
  - `abm_cash_large_count` (COUNT: cash withdrawals > $5K)
  - `structured_cash_deposits_same_day` (COUNT: multiple cash deposits same day)
- **Source**: `01_Professional_Money_Laundering_Trade_MSB.md`

### Red Flag: Currency Exchange Activity
- **Data Signal**: Frequent currency exchanges
- **Features**:
  - `currency_exchange_frequency` (COUNT: currency exchange transactions)
  - `cad_usd_eur_exchanges` (COUNT: exchanges involving CAD/USD/EUR)
- **Source**: `01_Professional_Money_Laundering_Trade_MSB.md`

---

## 5. Time-Based Pattern Features

### Red Flag: Unusual Timing
- **Data Signal**: Transactions at unusual times (midnight, weekends, after hours)
- **Features**:
  - `txn_hour_mode` (Most common transaction hour)
  - `after_hours_txn_pct` (Percentage of transactions outside 9 AM - 5 PM)
  - `weekend_txn_pct` (Percentage of weekend transactions)
  - `midnight_txn_count` (COUNT: transactions at hour 0)
  - `midnight_txn_volume` (SUM: transaction volume at hour 0)
- **Source**: Data insights + General indicators

### Red Flag: Rapid Transaction Velocity
- **Data Signal**: Very short time between transactions
- **Features**:
  - `time_between_txn_mean` (Average hours between transactions)
  - `time_between_txn_min` (Minimum time between transactions - detects rapid-fire)
  - `time_between_txn_stddev` (Consistency of timing)
- **Source**: General indicators

---

## 6. Behavioral Anomaly Features

### Red Flag: Living Beyond Means
- **Data Signal**: Transaction volume significantly exceeds declared income
- **Features**:
  - `amount_to_income_ratio` (Total transaction volume / declared income)
  - `amount_to_sales_ratio` (For businesses: transaction volume / sales)
  - `transaction_volume_vs_income` (Difference between volume and income)
  - `lifestyle_mismatch` (Boolean: volume >> income)
- **Source**: `01_Professional_Money_Laundering_Trade_MSB.md`

### Red Flag: Structuring (Just Below Threshold)
- **Data Signal**: Multiple transactions just below reporting thresholds
- **Features**:
  - `just_below_threshold_count` (COUNT: transactions $9,000-$10,000)
  - `structuring_pattern_flag` (Boolean: multiple just-below-threshold transactions)
- **Source**: `01_Professional_Money_Laundering_Trade_MSB.md` + General indicators

### Red Flag: Round Number Transactions
- **Data Signal**: High percentage of round-number transactions
- **Features**:
  - `round_amount_pct` (Percentage of transactions with round amounts)
  - `round_amount_flag` (Boolean: transaction is round number)
- **Source**: `01_Professional_Money_Laundering_Trade_MSB.md`

---

## 7. Business Profile Features

### Red Flag: High-Risk Industry
- **Data Signal**: Business in high-risk trade sectors
- **Features**:
  - `industry_code_high_risk_trade` (Boolean: industry in high-risk trade sectors)
  - `business_type_trading_company` (Boolean: business type is trading company)
- **Source**: `01_Professional_Money_Laundering_Trade_MSB.md`

### Red Flag: Unusual Business Activity
- **Data Signal**: Business activities outside norm or difficult to confirm
- **Features**:
  - `business_activity_anomaly` (Boolean: unusual business patterns)
  - `missing_business_info_flag` (Boolean: missing business information)
  - `unusual_business_model` (Boolean: business model outside sector norm)
- **Source**: `01_Professional_Money_Laundering_Trade_MSB.md`

### Red Flag: Suspicious Occupation
- **Data Signal**: Occupation inconsistent with transaction volume
- **Features**:
  - `occupation_income_mismatch` (Boolean: occupation suggests low income but high volume)
  - `suspicious_occupation_flag` (Boolean: occupation is student/homemaker/unemployed)
- **Source**: `01_Professional_Money_Laundering_Trade_MSB.md`

---

## 8. Amount Statistics Features

### Red Flag: Large Transaction Outliers
- **Data Signal**: Transactions significantly larger than customer's typical amounts
- **Features**:
  - `amount_max_ratio_mean` (Max transaction / Mean transaction - detects outliers)
  - `amount_stddev_ratio_mean` (Coefficient of variation)
  - `large_txn_count` (COUNT: transactions > $10K, $50K, $100K thresholds)
- **Source**: General indicators + Data insights

### Red Flag: Unusual Amount Patterns
- **Data Signal**: Inconsistent transaction amounts
- **Features**:
  - `amount_mean` (Average transaction amount)
  - `amount_stddev` (Standard deviation of amounts)
  - `amount_cv_by_channel` (Coefficient of variation by channel)
- **Source**: General indicators

---

## 9. Multi-Channel Features

### Red Flag: Channel Diversification
- **Data Signal**: Use of multiple transaction channels
- **Features**:
  - `channels_used_count` (COUNT: unique transaction channels used)
  - `multi_channel_flag` (Boolean: uses 3+ channels)
- **Source**: General indicators

### Red Flag: MSB-Like Activity
- **Data Signal**: Personal or business account showing money services business patterns
- **Features**:
  - `personal_account_business_activity` (Boolean: personal account shows business patterns)
  - `msb_like_personal_account` (Boolean: personal account similar to MSB)
  - `import_export_msb_activity` (Boolean: import/export company shows MSB patterns)
- **Source**: `01_Professional_Money_Laundering_Trade_MSB.md`

---

## Feature Engineering Priority

### High Priority (Critical Red Flags)
1. Wire transfer features (high-risk channel)
2. Geographic risk features (high-risk countries)
3. Flow-through velocity (professional money laundering)
4. Amount-to-income ratio (living beyond means)
5. Structuring indicators (just below threshold)

### Medium Priority (Important Patterns)
1. Time-based features (unusual timing)
2. Channel-specific features (cash, currency exchange)
3. Business profile features (high-risk industries)
4. Transaction velocity features

### Lower Priority (Supporting Indicators)
1. Round number features
2. Multi-channel features
3. Amount statistics (for context)

---

## Integration Notes

### For Task 2 (Detection Model)
- Use these features to engineer customer-level aggregations
- Combine multiple features to detect red flag combinations
- Focus on features that maximize signal for extreme class imbalance

### For Task 3 (Explainability)
- Map model feature importance back to red flags
- Use red flag descriptions to explain why customers were flagged
- Reference specific red flags in explanations

---

## 10. Bulk Cash Smuggling Features (Document 02)

### Red Flag: Structured Cash Deposits for Smuggling
- **Data Signal**: Multiple cash deposits just below $10,000 in quick succession
- **Features**:
  - `structured_cash_deposits_count` (COUNT: structured cash deposits)
  - `just_below_threshold_cash_deposits` (COUNT: cash deposits $9,000-$10,000)
  - `rapid_cash_deposit_sequence` (Velocity of cash deposits)
- **Source**: `02_Bulk_Cash_Smuggling_Mexico_TCOs.md`

### Red Flag: Mexico Repatriation Patterns
- **Data Signal**: Cash deposits followed by wire transfers to Mexico
- **Features**:
  - `wire_to_mexico_after_cash` (Boolean: wire to Mexico after cash deposit)
  - `cash_to_wire_repatriation_pattern` (Pattern indicator)
  - `mexico_wire_transfer_volume` (SUM: wire volume to Mexico)
- **Source**: `02_Bulk_Cash_Smuggling_Mexico_TCOs.md`

---

## 11. Oil Smuggling Features (Document 03)

### Red Flag: Oil-Related Transactions
- **Data Signal**: Transactions with oil/petroleum companies, especially in border regions
- **Features**:
  - `oil_company_payment_volume` (SUM: payments to oil companies)
  - `southwest_border_oil_activity` (Boolean: oil transactions in border states)
  - `oil_transaction_velocity` (Velocity of oil-related transactions)
- **Source**: `03_Oil_Smuggling_Mexico_Cartels.md`

### Red Flag: Cross-Border Oil Flows
- **Data Signal**: Oil transactions involving Mexico or border regions
- **Features**:
  - `cross_border_oil_flows` (COUNT: cross-border oil transactions)
  - `mexico_oil_transactions` (COUNT: transactions with Mexico involving oil)
  - `oil_smuggling_cross_border_flag` (Boolean indicator)
- **Source**: `03_Oil_Smuggling_Mexico_Cartels.md`

---

## 12. Chinese ML Network Features (Document 04)

### Red Flag: China/Hong Kong Transactions
- **Data Signal**: Large or frequent EFT to China/Hong Kong
- **Features**:
  - `volume_eft_to_china_hk` (SUM: EFT volume to China/Hong Kong)
  - `txn_count_to_china_hk` (COUNT: transactions to China/Hong Kong)
  - `rapid_china_bound_sequence` (Velocity of China-bound transactions)
- **Source**: `04_Chinese_ML_Networks_Mexico_TCOs.md`

### Red Flag: Mexico-China Network Flows
- **Data Signal**: Transactions from Mexico to China/Hong Kong
- **Features**:
  - `mexico_to_china_flows` (COUNT: Mexico to China transactions)
  - `mexico_china_network_flow_flag` (Boolean indicator)
  - `chinese_network_layering_count` (COUNT: Chinese network intermediaries)
- **Source**: `04_Chinese_ML_Networks_Mexico_TCOs.md`

---

## 13. Synthetic Opioids Features (Document 05)

### Red Flag: Cash-Intensive Drug Proceeds
- **Data Signal**: Large or frequent cash deposits, especially structured
- **Features**:
  - `large_cash_deposit_count` (COUNT: large cash deposits)
  - `rapid_cash_accumulation` (Velocity of cash accumulation)
  - `cash_intensive_business_flag` (Boolean: cash-intensive business)
- **Source**: `05_Synthetic_Opioids_Proceeds.md`

### Red Flag: Drug Proceeds Business Fronts
- **Data Signal**: New businesses with high cash volume or no legitimate operations
- **Features**:
  - `new_business_high_cash` (Boolean: new business with high cash)
  - `front_business_flag` (Boolean: business with no legitimate operations)
  - `business_cash_anomaly` (Anomaly score for business cash patterns)
- **Source**: `05_Synthetic_Opioids_Proceeds.md`

---

## 14. Underground Banking Features (Document 06)

### Red Flag: Hawala/Informal Value Transfer
- **Data Signal**: Transactions suggesting informal value transfer systems
- **Features**:
  - `hawala_indicator_flag` (Boolean: hawala indicators present)
  - `informal_value_transfer_pattern` (Pattern matching score)
  - `underground_banking_transaction_flag` (Boolean indicator)
- **Source**: `06_Underground_Banking_Schemes.md`

### Red Flag: Underground Banking Layering
- **Data Signal**: Complex transaction chains with underground banking characteristics
- **Features**:
  - `underground_banking_layering` (COUNT: underground banking layers)
  - `hawala_intermediary_chain` (COUNT: hawala intermediaries)
  - `asymmetric_transaction_pattern` (Boolean: asymmetric patterns)
- **Source**: `06_Underground_Banking_Schemes.md`

---

## 15. Human Trafficking Features (Document 07)

### Red Flag: Trafficking Cash Patterns
- **Data Signal**: High-volume cash deposits, especially at multiple locations
- **Features**:
  - `high_volume_cash_deposits` (SUM: high-volume cash deposits)
  - `multiple_location_cash_deposits_trafficking` (COUNT: multi-location deposits)
  - `third_party_cash_deposits_trafficking` (COUNT: third-party deposits)
- **Source**: `07_Human_Trafficking_Proceeds.md`

### Red Flag: Trafficking Business Fronts
- **Data Signal**: Cash-intensive businesses (massage parlors, escort services) with unusual patterns
- **Features**:
  - `cash_intensive_trafficking_business` (Boolean indicator)
  - `online_adult_service_revenue` (SUM: adult service platform revenue)
  - `hotel_motel_transaction_frequency` (COUNT: hotel/motel transactions)
- **Source**: `07_Human_Trafficking_Proceeds.md`

### Red Flag: Account Control Indicators
- **Data Signal**: One person controlling multiple accounts, especially accounts of others
- **Features**:
  - `account_control_flag` (Boolean: account control indicators)
  - `multiple_account_control` (COUNT: accounts controlled)
  - `victim_account_control_indicator` (Boolean: potential victim account control)
- **Source**: `07_Human_Trafficking_Proceeds.md`

---

## 16. General ML/TF Features (Document 08)

### Red Flag: General Transaction Anomalies
- **Data Signal**: Transactions unusual for customer profile
- **Features**:
  - `transaction_pattern_anomaly` (Anomaly score)
  - `unusual_customer_behavior` (Boolean indicator)
  - `rapid_fund_movement` (Velocity metric)
- **Source**: `08_General_ML_TF_Indicators.md`

### Red Flag: General Structuring
- **Data Signal**: Multiple transactions just below thresholds
- **Features**:
  - `just_below_threshold_count` (COUNT: just-below-threshold transactions)
  - `structuring_pattern_flag` (Boolean indicator)
  - `multiple_small_transactions` (COUNT: fragmented transactions)
- **Source**: `08_General_ML_TF_Indicators.md`

### Red Flag: General Geographic Risk
- **Data Signal**: Transactions with high-risk jurisdictions
- **Features**:
  - `high_risk_jurisdiction_transactions` (COUNT: high-risk jurisdiction transactions)
  - `offshore_financial_center_flag` (Boolean indicator)
  - `sanctioned_country_transactions` (COUNT: sanctioned country transactions)
- **Source**: `08_General_ML_TF_Indicators.md`

---

**Last Updated**: 2025-01-XX  
**Status**: Complete - Includes all 8 red flag documents

