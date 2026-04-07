# AML Knowledge Library - Comprehensive Red Flags Master Document

## Quick Navigation

- [Overview](#overview)
- [How to Use This Document](#how-to-use-this-document)
- [Red Flags by Category](#red-flags-by-category)
  - [Professional Money Laundering](#1-professional-money-laundering-trade-msb)
  - [Bulk Cash Smuggling](#2-bulk-cash-smuggling-mexico-tcos)
  - [Oil Smuggling](#3-oil-smuggling-mexico-cartels)
  - [Chinese ML Networks](#4-chinese-ml-networks-mexico-tcos)
  - [Synthetic Opioids](#5-synthetic-opioids-proceeds)
  - [Underground Banking](#6-underground-banking-schemes)
  - [Human Trafficking](#7-human-trafficking-proceeds)
  - [General ML/TF Indicators](#8-general-mltf-indicators)
- [Feature Mapping Quick Reference](#feature-mapping-quick-reference)
- [Source Documents](#source-documents)

---

## Overview

This master document consolidates **147+ red flags and indicators** from 8 authoritative AML/ATF sources. Each red flag includes:
- **Indicator Description**: What to look for
- **Data Signal**: What patterns in data indicate this
- **Feature Mapping**: Suggested features for model development
- **Source Reference**: Original document reference (see [Source Documents](#source-documents) section for full citations)

**Source Reference Format**: Each red flag includes a source reference in the format:
- `FINTRAC 18/19-SIDEL-025, Red Flag X` = FINTRAC Operational Alert reference number and red flag number
- `FinCEN FIN-2025-Alert001, Red Flag X` = FinCEN Alert reference number and red flag number
- `FinCEN FIN-2025-A003, Red Flag X` = FinCEN Advisory reference number and red flag number
- `FINTRAC ISO-OSI, Red Flag X` = FINTRAC Operational Alert (synthetic opioids)
- `FINTRAC ML-REC, Red Flag X` = FINTRAC Operational Alert (underground banking)
- `FINTRAC OAI-HTS-2021, Red Flag X` = FINTRAC Operational Alert (human trafficking)
- `FINTRAC Guidance, Red Flag X` = FINTRAC Guidance document

**Purpose**: 
- Quick reference for all AML red flags in one place
- Feature engineering guide for Task 2
- Explanation reference for Task 3
- Comprehensive indicator library

**Note**: For detailed context, methodology, and additional information, refer to the individual source documents (01-08).

---

## How to Use This Document

### For Feature Engineering (Task 2)
1. Review red flags relevant to your data
2. Check "Data Signal" and "Feature Mapping" columns
3. Engineer features based on suggested mappings
4. Reference individual documents for detailed context

### For Model Explainability (Task 3)
1. When a customer is flagged, identify which red flags match
2. Use "Indicator Description" and "Context" to explain why
3. Reference source documents for authoritative backing

### For Risk Assessment
1. Review red flags by category
2. Note "High-Risk Combinations" sections in individual documents
3. Combine multiple indicators for stronger signals

---

## Red Flags by Category

### 1. Professional Money Laundering (Trade & MSB)

**Source**: FINTRAC Operational Alert 18/19-SIDEL-025  
**Document**: `01_Professional_Money_Laundering_Trade_MSB.md`

| # | Red Flag | Data Signal | Feature Mapping | Source Reference |
|---|----------|-------------|-----------------|------------------|
| 1 | Phantom Shipments | Large EFT to trading companies, no goods movement | `volume_eft_to_trading_companies`, `txn_count_without_verification` | FINTRAC 18/19-SIDEL-025, Red Flag 1 |
| 2 | Falsely Described Goods | Invoice amounts inconsistent with typical prices | `amount_vs_typical_price_ratio`, `merchant_category_anomalies` | FINTRAC 18/19-SIDEL-025, Red Flag 2 |
| 3 | Multiple Invoicing | Multiple payments for same invoice | `duplicate_invoice_payments`, `payment_frequency_per_invoice` | FINTRAC 18/19-SIDEL-025, Red Flag 3 |
| 4 | Over/Under Invoicing | Amounts significantly different from market prices | `amount_vs_market_price_deviation`, `over_invoice_flag`, `under_invoice_flag` | FINTRAC 18/19-SIDEL-025, Red Flag 4 |
| 5 | Black Market Peso Exchange | EFT from Latin America to Canadian trading companies | `volume_eft_from_high_risk_countries`, `txn_count_to_trading_companies` | FINTRAC 18/19-SIDEL-025, Scheme Type 2 |
| 6 | Canadian Trading Company Route | EFT from Latin America/U.S. to Canadian trading companies | `volume_eft_from_latin_america`, `high_risk_geography_flag` | FINTRAC 18/19-SIDEL-025, Red Flag 4 |
| 7 | Correspondent Bank Route | EFT flows through Canadian banks to/from high-risk jurisdictions | `correspondent_bank_flows`, `high_risk_jurisdiction_transfers` | FINTRAC 18/19-SIDEL-025, Red Flag 4 |
| 8 | High-Risk Trade Sector | Business in agri-food, textiles, electronics, toys, lumber, automotive | `industry_code_high_risk_trade`, `business_type_trading_company` | FINTRAC 18/19-SIDEL-025, Red Flag 1 |
| 9 | Unusual Business Activities | Business activities outside norm or difficult to confirm | `business_activity_anomaly`, `missing_business_info_flag` | FINTRAC 18/19-SIDEL-025, Red Flag 2 |
| 10 | Sudden Large Inflows | Sudden increase in EFT volume or count | `volume_eft_sudden_increase`, `txn_count_eft_spike` | FINTRAC 18/19-SIDEL-025, Red Flag 3 |
| 11 | Geographic: China/Hong Kong | EFT to China/Hong Kong, from U.S./Latin America | `volume_eft_to_china_hk`, `volume_eft_from_latin_america` | FINTRAC 18/19-SIDEL-025, Red Flag 4 |
| 12 | Geographic: U.S./Mexico/Latin America | EFT to/from U.S., Mexico, Latin America | `volume_eft_to_us_mexico_latam`, `cross_border_flows` | FINTRAC 18/19-SIDEL-025, Red Flag 5 |
| 13 | Offshore Financial Centers | Transactions to/from Latvia, Cyprus, BVI, Panama, etc. | `offshore_financial_center_flag`, `high_risk_jurisdiction_count` | FINTRAC 18/19-SIDEL-025, Red Flag 6 |
| 14 | Round Figure Payments | Payments in round figures or $50K increments | `round_amount_flag`, `just_below_threshold_count`, `amount_modulo_50000` | FINTRAC 18/19-SIDEL-025, Red Flag 7 |
| 15 | UAE to Canada Transfers | EFT from UAE to Canada | `volume_eft_from_uae`, `uae_to_canada_flag` | FINTRAC 18/19-SIDEL-025, Red Flag 8 |
| 16 | Flow-Through Activity | Money taken out as quickly as it flows in | `flow_through_velocity`, `time_between_deposit_withdrawal` | FINTRAC 18/19-SIDEL-025, Red Flag 9 |
| 17 | Currency Import | Imports currency (USD) from Latin America | `cash_deposits_from_latam`, `usd_import_flag` | FINTRAC 18/19-SIDEL-025, Red Flag 10 |
| 18 | Credit Card Overpayments | Large business purchases by credit card, funded by overpayments | `credit_card_overpayment_flag`, `large_business_purchase_cc` | FINTRAC 18/19-SIDEL-025, Red Flag 11 |
| 19 | Legal Professional Accounts | Trade payments through legal professional accounts | `legal_professional_account_usage`, `trade_payment_through_lawyer` | FINTRAC 18/19-SIDEL-025, Red Flag 12 |
| 20 | MSB Sudden Inflows/Outflows | Sudden large EFT/cash in, followed by multiple outflows | `sudden_inflow_outflow_pattern`, `multiple_unrelated_party_payments` | FINTRAC 18/19-SIDEL-025, Red Flag 13 |
| 21 | MSB Currency Exchanges | Numerous CAD/USD/EUR exchanges | `currency_exchange_frequency`, `cad_usd_eur_exchanges` | FINTRAC 18/19-SIDEL-025, Red Flag 14 |
| 22 | MSB High-Risk Country Business | Business with Iran, UAE, Kuwait, Hong Kong, China | `sanctioned_country_transactions`, `high_risk_country_business_pct` | FINTRAC 18/19-SIDEL-025, Red Flag 15 |
| 23 | MSB Foreign Exchange Transfers | EFT from foreign exchange/trading companies for real estate/loans | `eft_from_fx_trading_companies`, `real_estate_loan_investment_flows` | FINTRAC 18/19-SIDEL-025, Red Flag 16 |
| 24 | Personal Account MSB Activity | Personal account showing MSB-like patterns | `personal_account_business_activity`, `msb_like_personal_account` | FINTRAC 18/19-SIDEL-025, Red Flag 17 |
| 25 | Multiple Identities | Multiple occupations, addresses, telephone numbers | `multiple_occupations_flag`, `multiple_addresses_flag` | FINTRAC 18/19-SIDEL-025, Red Flag 19 |
| 26 | Living Beyond Means | Transaction volume exceeds declared income | `amount_to_income_ratio`, `lifestyle_mismatch` | FINTRAC 18/19-SIDEL-025, Red Flag 21 |

---

### 2. Bulk Cash Smuggling (Mexico TCOs)

**Source**: FinCEN Alert FIN-2025-Alert001  
**Document**: `02_Bulk_Cash_Smuggling_Mexico_TCOs.md`

| # | Red Flag | Data Signal | Feature Mapping | Source Reference |
|---|----------|-------------|-----------------|------------------|
| 1 | Structured Cash Deposits | Multiple cash deposits $9K-$10K in quick succession | `structured_cash_deposits_count`, `just_below_threshold_cash_deposits` | FinCEN FIN-2025-Alert001, Red Flag 1 |
| 2 | Cross-Border Cash Movement | Large cash withdrawals before travel to Mexico | `large_cash_withdrawal_flag`, `border_region_cash_activity` | FinCEN FIN-2025-Alert001, Red Flag 2 |
| 3 | Multiple Location Cash Deposits | Same person, multiple locations, same day | `multiple_location_cash_deposits_same_day`, `cash_deposit_location_diversity` | FinCEN FIN-2025-Alert001, Red Flag 3 |
| 4 | Third-Party Cash Deposits | Cash deposits into accounts of others, especially Mexico-linked | `third_party_cash_deposit_flag`, `mexico_linked_account_deposits` | FinCEN FIN-2025-Alert001, Red Flag 4 |
| 5 | Wire Transfers to Mexico After Cash | Large wires to Mexico following cash deposits | `wire_to_mexico_after_cash`, `cash_to_wire_repatriation_pattern` | FinCEN FIN-2025-Alert001, Red Flag 5 |
| 6 | MSB Usage for Repatriation | MSB transfers to Mexico after cash deposits | `msb_to_mexico_transfers`, `western_union_mexico_flag` | FinCEN FIN-2025-Alert001, Red Flag 6 |
| 7 | Money Orders/Bank Drafts | Money orders/drafts to Mexico, funded by cash | `money_order_purchase_to_mexico`, `cash_funded_money_orders` | FinCEN FIN-2025-Alert001, Red Flag 7 |
| 8 | Rapid Cash Accumulation | Sudden cash spike followed by immediate transfers | `rapid_cash_accumulation`, `cash_to_transfer_velocity` | FinCEN FIN-2025-Alert001, Red Flag 8 |
| 9 | Smuggling Corridors | Transactions in border regions or known corridors | `border_region_transaction_flag`, `smuggling_corridor_activity` | FinCEN FIN-2025-Alert001, Red Flag 9 |
| 10 | Layered Transactions | Cash → multiple accounts → Mexico | `layered_transaction_count`, `multi_account_chain_flag` | FinCEN FIN-2025-Alert001, Red Flag 10 |
| 11 | Mexico-U.S. Border Activity | High volume in border cities (El Paso, Laredo, etc.) | `border_region_transaction_count`, `border_city_activity_flag` | FinCEN FIN-2025-Alert001, Red Flag 11 |
| 12 | Mexico-Based Entity Transactions | Frequent transactions with Mexico-based entities | `mexico_transaction_volume`, `mexico_entity_transaction_count` | FinCEN FIN-2025-Alert001, Red Flag 12 |
| 13 | Lifestyle Inconsistencies | Low income, large cash deposits, Mexico connections | `income_transaction_mismatch_mexico`, `low_income_high_volume_mexico` | FinCEN FIN-2025-Alert001, Red Flag 13 |
| 14 | Avoidance of Reporting Thresholds | Consistent just-below-threshold transactions | `just_below_ctr_threshold_count`, `structuring_pattern_mexico` | FinCEN FIN-2025-Alert001, Red Flag 14 |
| 15 | Rapid Account Turnover | Accounts: cash in → immediate transfer out | `account_turnover_rate`, `cash_deposit_to_transfer_time` | FinCEN FIN-2025-Alert001, Red Flag 15 |

---

### 3. Oil Smuggling (Mexico Cartels)

**Source**: FinCEN Alert FIN-2025-Alert002  
**Document**: `03_Oil_Smuggling_Mexico_Cartels.md`

| # | Red Flag | Data Signal | Feature Mapping | Source Reference |
|---|----------|-------------|-----------------|------------------|
| 1 | Payments to Oil Companies | Large payments to oil/petroleum companies, border regions | `oil_company_payment_volume`, `petroleum_merchant_transactions` | FinCEN FIN-2025-Alert002, Red Flag 1 |
| 2 | Southwest Border Oil Transactions | Oil transactions in TX, NM, AZ, CA border states | `southwest_border_oil_activity`, `border_state_oil_transactions` | FinCEN FIN-2025-Alert002, Red Flag 2 |
| 3 | Unusual Payment Methods | Large cash or structured payments for oil | `cash_oil_payments`, `structured_oil_payments` | FinCEN FIN-2025-Alert002, Red Flag 3 |
| 4 | Rapid Oil Transaction Sequences | High frequency oil transactions in short time | `oil_transaction_velocity`, `rapid_oil_transaction_sequence` | FinCEN FIN-2025-Alert002, Red Flag 4 |
| 5 | Cross-Border Oil Flows | Oil transactions across U.S.-Mexico border | `cross_border_oil_flows`, `mexico_oil_transactions` | FinCEN FIN-2025-Alert002, Red Flag 5 |
| 6 | Layered Oil Transactions | Complex chains through multiple oil businesses | `oil_business_transaction_chain`, `layered_oil_transactions` | FinCEN FIN-2025-Alert002, Red Flag 6 |
| 7 | Border Region Fuel Activity | High volume in border cities (El Paso, Laredo, San Diego) | `border_city_oil_activity`, `fuel_transaction_border_cities` | FinCEN FIN-2025-Alert002, Red Flag 7 |
| 8 | Transactions Near Oil Infrastructure | Transactions near pipelines, refineries, storage | `oil_infrastructure_proximity_flag`, `pipeline_region_transactions` | FinCEN FIN-2025-Alert002, Red Flag 8 |
| 9 | Oil Business Unusual Activity | Oil business with patterns inconsistent with operations | `oil_business_anomaly_flag`, `unusual_oil_business_activity` | FinCEN FIN-2025-Alert002, Red Flag 9 |
| 10 | New Oil Business High Volume | Recently established oil business with immediate high volume | `new_oil_business_high_volume`, `recent_oil_business_flag` | FinCEN FIN-2025-Alert002, Red Flag 10 |
| 11 | Round-Number Oil Transactions | Oil transactions in round numbers ($50K, $100K) | `round_oil_transaction_flag`, `bulk_oil_sale_indicator` | FinCEN FIN-2025-Alert002, Red Flag 11 |
| 12 | Large-Value Oil Transactions | Exceptionally large oil/fuel purchases | `large_oil_transaction_flag`, `excessive_oil_purchase_amount` | FinCEN FIN-2025-Alert002, Red Flag 12 |
| 13 | Oil + Drug Proceeds Patterns | Oil transactions + cash activity + structuring | `oil_drug_proceeds_combination`, `multi_criminal_activity_flag` | FinCEN FIN-2025-Alert002, Red Flag 13 |
| 14 | Oil Business Cartel Links | Oil business transacting with cartel-linked accounts | `oil_cartel_linked_transactions`, `cartel_network_oil_flag` | FinCEN FIN-2025-Alert002, Red Flag 14 |

---

### 4. Chinese ML Networks (Mexico TCOs)

**Source**: FinCEN Advisory FIN-2025-A003  
**Document**: `04_Chinese_ML_Networks_Mexico_TCOs.md`

| # | Red Flag | Data Signal | Feature Mapping | Source Reference |
|---|----------|-------------|-----------------|------------------|
| 1 | China/Hong Kong Transactions | Large/frequent EFT to China/Hong Kong | `volume_eft_to_china_hk`, `txn_count_to_china_hk` | FinCEN FIN-2025-A003, Red Flag 1 |
| 2 | Chinese Network Intermediaries | Transactions through Chinese ML network accounts | `chinese_network_intermediary_flag`, `chinese_ml_network_account_transactions` | FinCEN FIN-2025-A003, Red Flag 2 |
| 3 | Rapid China-Bound Sequences | Rapid transaction sequences ending in China/HK | `rapid_china_bound_sequence`, `china_transfer_velocity` | FinCEN FIN-2025-A003, Red Flag 3 |
| 4 | Mexico-to-China Flows | EFT from Mexico-based entities to China/HK | `mexico_to_china_flows`, `mexico_china_network_flow_flag` | FinCEN FIN-2025-A003, Red Flag 4 |
| 5 | Layered Through Chinese Networks | Complex chains through Chinese intermediaries | `chinese_network_layering_count`, `layered_china_transactions` | FinCEN FIN-2025-A003, Red Flag 5 |
| 6 | U.S.-China-Mexico Triangle | Transactions: U.S. → China → Mexico (or vice versa) | `us_china_mexico_triangle_flag`, `triangle_transaction_chain` | FinCEN FIN-2025-A003, Red Flag 6 |
| 7 | Currency Exchange Through Chinese Networks | Exchanges involving CNY or HKD | `chinese_yuan_exchange_flag`, `hkd_exchange_volume` | FinCEN FIN-2025-A003, Red Flag 7 |
| 8 | Multi-Currency Transactions | Transactions: USD, CNY, MXN with China connections | `multi_currency_china_flag`, `usd_cny_mxn_transactions` | FinCEN FIN-2025-A003, Red Flag 8 |
| 9 | Chinese-Owned Business TCO Links | Chinese businesses transacting with TCO-linked accounts | `chinese_business_tco_connections`, `china_mexico_business_links` | FinCEN FIN-2025-A003, Red Flag 9 |
| 10 | Import/Export China-Mexico Trade | Import/export companies with China-Mexico trade, unusual patterns | `china_mexico_trade_company_flag`, `trade_based_ml_china_mexico` | FinCEN FIN-2025-A003, Red Flag 10 |
| 11 | Chinese Financial Hubs | Transactions: Hong Kong, Shanghai, Beijing, Shenzhen | `chinese_financial_hub_transactions`, `hong_kong_transaction_flag` | FinCEN FIN-2025-A003, Red Flag 11 |
| 12 | Offshore Centers + Chinese Connections | Offshore centers (BVI, Cayman) with China connections | `offshore_china_connections`, `chinese_offshore_network_flag` | FinCEN FIN-2025-A003, Red Flag 12 |
| 13 | Structured Transactions to China | Multiple just-below-$3K transactions to China/HK | `structured_china_transfers`, `china_structuring_pattern` | FinCEN FIN-2025-A003, Red Flag 13 |
| 14 | Round-Number Transfers to China | Transfers to China/HK in round numbers | `round_china_transfers`, `bulk_china_transfer_indicator` | FinCEN FIN-2025-A003, Red Flag 14 |
| 15 | Cash-to-China Transfer Patterns | Large cash deposits → wire transfers to China/HK | `cash_to_china_transfer_pattern`, `drug_proceeds_china_flow` | FinCEN FIN-2025-A003, Red Flag 15 |
| 16 | Mexico TCO Proceeds Through Chinese Networks | Mexico TCO drug proceeds laundered through Chinese networks | `mexico_tco_china_network_flag`, `tco_china_collaboration_indicator` | FinCEN FIN-2025-A003, Red Flag 16 |

---

### 5. Synthetic Opioids Proceeds

**Source**: FINTRAC Operational Alert (ISO-OSI)  
**Document**: `05_Synthetic_Opioids_Proceeds.md`

| # | Red Flag | Data Signal | Feature Mapping | Source Reference |
|---|----------|-------------|-----------------|------------------|
| 1 | Large Cash Deposits | Large/frequent cash deposits, especially structured | `large_cash_deposit_count`, `structured_cash_deposits` | FINTRAC ISO-OSI, Red Flag 1 |
| 2 | Rapid Cash Accumulation | Sudden increase in cash deposits | `rapid_cash_accumulation`, `sudden_cash_spike_flag` | FINTRAC ISO-OSI, Red Flag 2 |
| 3 | Multiple Location Cash Deposits | Same person, multiple locations, same day | `multiple_location_cash_deposits`, `cash_deposit_location_diversity` | FINTRAC ISO-OSI, Red Flag 3 |
| 4 | Cash-Intensive Businesses | Cash businesses (restaurants, retail) with unusually high cash | `cash_intensive_business_flag`, `unusual_cash_business_volume` | FINTRAC ISO-OSI, Red Flag 4 |
| 5 | New Business High Cash | Recently established business with immediate high cash | `new_business_high_cash`, `recent_business_cash_flag` | FINTRAC ISO-OSI, Red Flag 5 |
| 6 | No Legitimate Operations | Business with cash deposits but no business activity | `front_business_flag`, `no_legitimate_operations` | FINTRAC ISO-OSI, Red Flag 6 |
| 7 | Rapid Money Movement | Cash deposits → immediate wire transfers/EFTs | `rapid_money_movement`, `cash_to_transfer_velocity` | FINTRAC ISO-OSI, Red Flag 7 |
| 8 | High Transaction Frequency | Unusually high number of transactions, especially cash | `high_transaction_frequency`, `cash_transaction_frequency` | FINTRAC ISO-OSI, Red Flag 8 |
| 9 | High-Risk Area Transactions | Transactions in areas known for opioid trafficking | `high_risk_area_transactions`, `opioid_epidemic_region_flag` | FINTRAC ISO-OSI, Red Flag 9 |
| 10 | Cross-Border Patterns | Transactions with countries known for opioid production | `cross_border_opioid_flows`, `high_risk_country_transactions` | FINTRAC ISO-OSI, Red Flag 10 |
| 11 | Just Below Threshold | Multiple transactions just below $10K | `just_below_threshold_count`, `structuring_pattern_flag` | FINTRAC ISO-OSI, Red Flag 11 |
| 12 | Round-Number Transactions | High percentage of round-number transactions | `round_amount_pct`, `round_number_transaction_count` | FINTRAC ISO-OSI, Red Flag 12 |
| 13 | Lifestyle Inconsistencies | Low income, large cash deposits, high-value purchases | `lifestyle_inconsistency_flag`, `income_transaction_mismatch` | FINTRAC ISO-OSI, Red Flag 13 |
| 14 | High-Value Cash Purchases | Large purchases (vehicles, real estate) funded by cash | `high_value_cash_purchase_flag`, `luxury_asset_cash_funding` | FINTRAC ISO-OSI, Red Flag 14 |
| 15 | Multiple Related Accounts | Network of related accounts with similar cash patterns | `related_account_network_flag`, `network_cash_pattern_similarity` | FINTRAC ISO-OSI, Red Flag 15 |
| 16 | Third-Party Cash Deposits | Multiple individuals depositing into same account | `third_party_cash_deposits`, `multiple_depositors_same_account` | FINTRAC ISO-OSI, Red Flag 16 |

---

### 6. Underground Banking Schemes

**Source**: FINTRAC Operational Alert (ML-REC)  
**Document**: `06_Underground_Banking_Schemes.md`

| # | Red Flag | Data Signal | Feature Mapping | Source Reference |
|---|----------|-------------|-----------------|------------------|
| 1 | Informal Value Transfer Indicators | Transactions suggesting hawala/hundi/IVTS | `hawala_indicator_flag`, `informal_value_transfer_pattern` | FINTRAC ML-REC, Red Flag 1 |
| 2 | Transactions Without Business Purpose | Large transactions between unrelated parties | `unrelated_party_large_transactions`, `no_business_relationship_flag` | FINTRAC ML-REC, Red Flag 2 |
| 3 | Rapid Cross-Border Value Movement | Value moves across borders without formal transactions | `cross_border_informal_transfer`, `underground_cross_border_flag` | FINTRAC ML-REC, Red Flag 3 |
| 4 | Hawala Operator Patterns | Accounts: multiple unrelated sources → multiple destinations | `hawala_operator_pattern`, `intermediary_hawala_flag` | FINTRAC ML-REC, Red Flag 4 |
| 5 | Settlement Through Alternative Means | Transactions settled through goods/services | `alternative_settlement_flag`, `trade_based_settlement` | FINTRAC ML-REC, Red Flag 5 |
| 6 | Minimal Documentation | Large transactions with minimal documentation | `minimal_documentation_flag`, `undocumented_large_transactions` | FINTRAC ML-REC, Red Flag 6 |
| 7 | High-Risk Country Connections | Transactions with countries known for underground banking | `underground_banking_country_flag`, `hawala_prevalent_region_transactions` | FINTRAC ML-REC, Red Flag 7 |
| 8 | Unbanked Population Transactions | Transactions with unbanked communities | `unbanked_population_transactions`, `informal_financial_system_usage` | FINTRAC ML-REC, Red Flag 8 |
| 9 | Asymmetric Transaction Patterns | Large in → many small out, or many small in → large out | `asymmetric_transaction_pattern`, `funnel_account_indicator` | FINTRAC ML-REC, Red Flag 9 |
| 10 | Round-Number Transactions | Round numbers, especially foreign currency equivalents | `round_number_underground_transactions`, `hawala_round_amounts` | FINTRAC ML-REC, Red Flag 10 |
| 11 | Unregistered MSB Activity | MSB-like activity without MSB registration | `unregistered_msb_activity`, `msb_like_underground_flag` | FINTRAC ML-REC, Red Flag 11 |
| 12 | Multiple Currency Exchanges | Frequent currency exchanges, multiple currencies | `frequent_currency_exchanges`, `multi_currency_underground_flag` | FINTRAC ML-REC, Red Flag 12 |
| 13 | Cash-to-Underground Banking | Large cash deposits → underground banking indicators | `cash_to_underground_banking`, `criminal_proceeds_underground_flag` | FINTRAC ML-REC, Red Flag 13 |
| 14 | Layering Through Underground Banking | Complex chains through underground banking intermediaries | `underground_banking_layering`, `hawala_intermediary_chain` | FINTRAC ML-REC, Red Flag 14 |

---

### 7. Human Trafficking Proceeds

**Source**: FINTRAC Operational Alert (OAI-HTS-2021)  
**Document**: `07_Human_Trafficking_Proceeds.md`

| # | Red Flag | Data Signal | Feature Mapping | Source Reference |
|---|----------|-------------|-----------------|------------------|
| 1 | High-Volume Cash Deposits | Frequent cash deposits, often just below thresholds | `high_volume_cash_deposits`, `frequent_cash_deposit_pattern` | FINTRAC OAI-HTS-2021, Red Flag 1 |
| 2 | Multiple Location Cash Deposits | Same person, multiple locations, same day | `multiple_location_cash_deposits_trafficking`, `same_day_multi_location_cash` | FINTRAC OAI-HTS-2021, Red Flag 2 |
| 3 | Third-Party Cash Deposits | Multiple individuals depositing into trafficker account | `third_party_cash_deposits_trafficking`, `trafficker_account_deposits` | FINTRAC OAI-HTS-2021, Red Flag 3 |
| 4 | Cash-Intensive Trafficking Businesses | Massage parlors, escort services with high cash | `cash_intensive_trafficking_business`, `massage_parlor_high_cash` | FINTRAC OAI-HTS-2021, Red Flag 4 |
| 5 | Online Advertisement Revenue | Revenue from escort websites, adult services | `online_adult_service_revenue`, `escort_website_transactions` | FINTRAC OAI-HTS-2021, Red Flag 5 |
| 6 | Hotel/Motel Transactions | Frequent hotel/motel transactions, especially cash | `hotel_motel_transaction_frequency`, `cash_hotel_payments` | FINTRAC OAI-HTS-2021, Red Flag 6 |
| 7 | Rapid Cash-to-Asset Conversion | Cash deposits → immediate asset purchases | `rapid_cash_to_asset_conversion`, `trafficking_asset_integration` | FINTRAC OAI-HTS-2021, Red Flag 7 |
| 8 | Structured Transactions | Multiple just-below-$10K transactions | `structured_trafficking_transactions`, `just_below_threshold_trafficking` | FINTRAC OAI-HTS-2021, Red Flag 8 |
| 9 | Round-Number Transactions | High percentage of round-number transactions | `round_number_trafficking_transactions`, `round_service_payments` | FINTRAC OAI-HTS-2021, Red Flag 9 |
| 10 | High-Risk Area Transactions | Transactions in known trafficking areas | `high_risk_trafficking_area_transactions`, `trafficking_hub_activity` | FINTRAC OAI-HTS-2021, Red Flag 10 |
| 11 | Cross-Border Patterns | Transactions with source countries for victims | `cross_border_trafficking_flows`, `source_country_transactions` | FINTRAC OAI-HTS-2021, Red Flag 11 |
| 12 | Control Over Victim Accounts | One person controlling multiple accounts (victims) | `account_control_flag`, `multiple_account_control` | FINTRAC OAI-HTS-2021, Red Flag 12 |
| 13 | Lifestyle Inconsistencies | Low income, large cash deposits, high-value purchases | `lifestyle_inconsistency_trafficking`, `low_income_high_volume_trafficking` | FINTRAC OAI-HTS-2021, Red Flag 13 |
| 14 | High-Value Purchases | Large purchases (vehicles, jewelry, real estate) with cash | `high_value_trafficking_purchases`, `luxury_asset_trafficking_funding` | FINTRAC OAI-HTS-2021, Red Flag 14 |
| 15 | Network of Related Accounts | Related accounts with similar cash/transaction patterns | `trafficking_network_accounts`, `network_cash_similarity_trafficking` | FINTRAC OAI-HTS-2021, Red Flag 15 |
| 16 | MSB Usage | MSB transfers, especially to source countries | `msb_trafficking_usage`, `western_union_trafficking_flag` | FINTRAC OAI-HTS-2021, Red Flag 16 |
| 17 | Unusual Transaction Timing | Transactions at unusual times (late night, early morning) | `unusual_timing_trafficking`, `late_night_trafficking_transactions` | FINTRAC OAI-HTS-2021, Red Flag 17 |
| 18 | Weekend/Peak Period Activity | High activity during weekends or peak periods | `weekend_trafficking_activity`, `peak_period_transactions` | FINTRAC OAI-HTS-2021, Red Flag 18 |

---

### 8. General ML/TF Indicators

**Source**: FINTRAC Guidance (Financial Entities)  
**Document**: `08_General_ML_TF_Indicators.md`

| # | Red Flag | Data Signal | Feature Mapping | Source Reference |
|---|----------|-------------|-----------------|------------------|
| 1 | Unusual Transaction Patterns | Transactions unusual for customer profile | `transaction_pattern_anomaly`, `unusual_customer_behavior` | FINTRAC Guidance, Red Flag 1 |
| 2 | Rapid Movement of Funds | Funds moving quickly through accounts | `rapid_fund_movement`, `high_velocity_transactions` | FINTRAC Guidance, Red Flag 2 |
| 3 | Complex Transaction Structures | Complex structures: multiple parties/accounts/jurisdictions | `complex_transaction_structure`, `layered_transaction_count` | FINTRAC Guidance, Red Flag 3 |
| 4 | Round-Number Transactions | High frequency of round-number transactions | `round_number_transaction_pct`, `bulk_transfer_indicator` | FINTRAC Guidance, Red Flag 4 |
| 5 | Just Below Threshold | Multiple just-below-$10K or $3K transactions | `just_below_threshold_count`, `structuring_pattern_flag` | FINTRAC Guidance, Red Flag 5 |
| 6 | Multiple Small Transactions | Breaking large amounts into small transactions | `multiple_small_transactions`, `fragmented_transaction_pattern` | FINTRAC Guidance, Red Flag 6 |
| 7 | Same-Day Multi-Location | Same person, multiple locations, same day | `same_day_multi_location_transactions`, `distributed_transaction_pattern` | FINTRAC Guidance, Red Flag 7 |
| 8 | Reluctance to Provide Information | Missing/incomplete customer information | `missing_customer_info_flag`, `information_reluctance_indicator` | FINTRAC Guidance, Red Flag 8 |
| 9 | Unusual Account Activity | Activity inconsistent with customer profile | `account_activity_anomaly`, `profile_transaction_mismatch` | FINTRAC Guidance, Red Flag 9 |
| 10 | Lifestyle Inconsistencies | Transactions beyond declared income/means | `lifestyle_inconsistency_flag`, `beyond_means_indicator` | FINTRAC Guidance, Red Flag 10 |
| 11 | High-Risk Jurisdiction Transactions | Transactions with high-risk countries | `high_risk_jurisdiction_transactions`, `sanctioned_country_flag` | FINTRAC Guidance, Red Flag 11 |
| 12 | Offshore Financial Centers | Transactions with offshore centers/tax havens | `offshore_financial_center_transactions`, `tax_haven_flag` | FINTRAC Guidance, Red Flag 12 |
| 13 | Sanctioned Countries | Transactions with sanctioned countries | `sanctioned_country_transactions`, `sanctions_violation_flag` | FINTRAC Guidance, Red Flag 13 |
| 14 | Multiple Accounts Similar Patterns | Multiple accounts showing similar unusual patterns | `multiple_accounts_similar_patterns`, `account_network_flag` | FINTRAC Guidance, Red Flag 14 |
| 15 | Third-Party Account Usage | Account used primarily for third-party transactions | `third_party_account_usage`, `conduit_account_flag` | FINTRAC Guidance, Red Flag 15 |
| 16 | Funnel Accounts | Many-to-one or one-to-many transaction patterns | `funnel_account_flag`, `aggregation_account_indicator` | FINTRAC Guidance, Red Flag 16 |
| 17 | Large Cash Transactions | Unusually large cash deposits/withdrawals | `large_cash_transaction_flag`, `unusual_cash_volume` | FINTRAC Guidance, Red Flag 17 |
| 18 | Frequent Cash Deposits | Frequent cash deposits, especially structured | `frequent_cash_deposits`, `structured_cash_deposit_pattern` | FINTRAC Guidance, Red Flag 18 |
| 19 | Cash-Intensive Business Anomalies | Cash business with unusual patterns | `cash_intensive_business_anomaly`, `front_business_indicator` | FINTRAC Guidance, Red Flag 19 |
| 20 | Rapid Wire Transfer Sequences | Rapid wire sequences, especially high-risk jurisdictions | `rapid_wire_sequence`, `wire_transfer_velocity` | FINTRAC Guidance, Red Flag 20 |
| 21 | Wire Transfers Without Purpose | Large wires with no apparent business purpose | `wire_without_purpose_flag`, `unexplained_wire_transfers` | FINTRAC Guidance, Red Flag 21 |
| 22 | International Wire Patterns | Unusual international wire patterns, high-risk countries | `international_wire_pattern_anomaly`, `cross_border_wire_activity` | FINTRAC Guidance, Red Flag 22 |
| 23 | Small, Frequent Transactions | Multiple small transactions (terrorist financing) | `small_frequent_transactions`, `terrorist_financing_pattern` | FINTRAC Guidance, Red Flag 23 |
| 24 | Charitable Organization Concerns | Transactions with charities, especially high-risk regions | `charitable_organization_transactions`, `charity_terrorist_financing_flag` | FINTRAC Guidance, Red Flag 24 |
| 25 | Transactions to Conflict Zones | Transactions to conflict zones or terrorist activity regions | `conflict_zone_transactions`, `terrorist_activity_region_flag` | FINTRAC Guidance, Red Flag 25 |
| 26 | Unusual Business Relationships | Transactions between unrelated businesses/individuals | `unusual_business_relationship`, `unrelated_party_transactions` | FINTRAC Guidance, Red Flag 26 |
| 27 | Shell Company Indicators | Transactions with shell companies or minimal operations | `shell_company_transactions`, `minimal_operations_company_flag` | FINTRAC Guidance, Red Flag 27 |
| 28 | Complex Ownership Structures | Business with complex/opaque ownership | `complex_ownership_structure`, `opaque_ownership_flag` | FINTRAC Guidance, Red Flag 28 |

---

## Feature Mapping Quick Reference

### High-Priority Features (Critical Red Flags)

**Wire Transfer Features**:
- `wire_txn_count`, `wire_volume_total`, `wire_volume_avg`, `has_wire_transfers`

**Geographic Risk Features**:
- `high_risk_country_transaction_count`, `offshore_financial_center_flag`, `sanctioned_country_transactions`

**Cash Activity Features**:
- `large_cash_deposit_count`, `structured_cash_deposits`, `multiple_location_cash_deposits_same_day`

**Velocity Features**:
- `rapid_fund_movement`, `flow_through_velocity`, `cash_to_transfer_velocity`

**Structuring Features**:
- `just_below_threshold_count`, `structuring_pattern_flag`, `round_amount_pct`

### Feature Categories

1. **Transaction Amount Features**: `amount_mean`, `amount_max_ratio_mean`, `large_txn_count`
2. **Transaction Frequency Features**: `txn_count_total`, `txn_per_day_avg`, `high_frequency_customer_flag`
3. **Channel Features**: `wire_txn_count`, `abm_cash_txn_count`, `channels_used_count`
4. **Geographic Features**: `high_risk_country_transaction_count`, `country_diversity`, `border_region_activity_flag`
5. **Time-Based Features**: `after_hours_txn_pct`, `weekend_txn_pct`, `midnight_txn_count`
6. **Business Profile Features**: `industry_code_high_risk_trade`, `business_activity_anomaly`, `occupation_income_mismatch`
7. **Behavioral Features**: `lifestyle_inconsistency_flag`, `account_turnover_rate`, `funnel_account_flag`

---

## Source Documents

For detailed context, methodology, and additional information, refer to:

1. **01_Professional_Money_Laundering_Trade_MSB.md**
   - **Source**: FINTRAC Operational Alert
   - **Reference**: 18/19-SIDEL-025
   - **Publication Date**: July 18, 2018
   - **URL**: https://fintrac-canafe.canada.ca/intel/operation/oai-ml-eng

2. **02_Bulk_Cash_Smuggling_Mexico_TCOs.md**
   - **Source**: FinCEN Alert
   - **Reference**: FIN-2025-Alert001
   - **URL**: https://www.fincen.gov/system/files/shared/BCS-Alert-FINAL-508C.pdf

3. **03_Oil_Smuggling_Mexico_Cartels.md**
   - **Source**: FinCEN Alert
   - **Reference**: FIN-2025-Alert002
   - **URL**: https://www.fincen.gov/system/files/shared/FinCEN-Alert-Oil-Smuggling-FINAL-508C.pdf

4. **04_Chinese_ML_Networks_Mexico_TCOs.md**
   - **Source**: FinCEN Advisory
   - **Reference**: FIN-2025-A003
   - **URL**: https://www.fincen.gov/resources/advisories/fincen-advisory-fin-2025-a003

5. **05_Synthetic_Opioids_Proceeds.md**
   - **Source**: FINTRAC Operational Alert
   - **Reference**: ISO-OSI (Illicit Synthetic Opioids)
   - **URL**: https://fintrac-canafe.canada.ca/intel/operation/iso-osi-eng

6. **06_Underground_Banking_Schemes.md**
   - **Source**: FINTRAC Operational Alert
   - **Reference**: ML-REC (Money Laundering - Underground Banking)
   - **URL**: https://fintrac-canafe.canada.ca/intel/operation/ml-rec-eng

7. **07_Human_Trafficking_Proceeds.md**
   - **Source**: FINTRAC Operational Alert
   - **Reference**: OAI-HTS-2021 (Human Trafficking for Sexual Exploitation)
   - **URL**: https://fintrac-canafe.canada.ca/intel/operation/oai-hts-2021-eng

8. **08_General_ML_TF_Indicators.md**
   - **Source**: FINTRAC Guidance
   - **Reference**: Financial Entities
   - **URL**: https://fintrac-canafe.canada.ca/guidance-directives/transaction-operation/indicators-indicateurs/fin_mltf-eng

### Source Document Contents

All source documents include:
- **Detailed red flag descriptions** with full context and explanations
- **Risk assessment guidance** and high-risk combination indicators
- **Integration notes** for Tasks 2 (Detection Model) and 3 (Explainability)
- **Full source citations** with URLs, publication dates, and reference numbers
- **Methodology and background** information

### Traceability

Every red flag in this master document:
- ✅ Has a source reference linking to the original document
- ✅ Can be traced back to the authoritative source
- ✅ Includes document reference number for verification
- ✅ Links to full source document for detailed context

---

## Usage Tips

### For Quick Reference
- Use the tables above to quickly identify relevant red flags
- Check "Data Signal" column to understand what to look for in data
- Use "Feature Mapping" column for feature engineering

### For Detailed Analysis
- Refer to individual source documents (01-08) for:
  - Detailed context and explanations
  - Risk assessment frameworks
  - High-risk combination guidance
  - Source citations and traceability

### For Feature Engineering
1. Review red flags relevant to your data
2. Check feature mapping suggestions
3. Engineer customer-level aggregations
4. Combine multiple features for stronger signals

### For Model Explainability
1. Identify which red flags match flagged customers
2. Use indicator descriptions to explain decisions
3. Reference source documents for authoritative backing

---

**Last Updated**: 2025-01-XX  
**Total Red Flags**: 147+  
**Source Documents**: 8  
**Status**: Complete and Comprehensive

