# Money Laundering and Terrorist Financing Indicators—Financial Entities

## Source Information

**Source**: FINTRAC Guidance  
**URL**: https://fintrac-canafe.canada.ca/guidance-directives/transaction-operation/indicators-indicateurs/fin_mltf-eng  
**Issuing Organization**: Financial Transactions and Reports Analysis Centre of Canada (FINTRAC)

---

## Overview

This guidance document provides **general money laundering and terrorist financing indicators** for financial entities. These are foundational indicators that apply across various money laundering methods and typologies.

**Key Focus**: 
- General AML/ATF indicators applicable broadly
- Foundation indicators for financial institutions
- Baseline patterns for comparison with specific red flags

**Context**: These general indicators provide the foundation for understanding money laundering and terrorist financing patterns. They should be used in conjunction with specific red flags from other documents.

---

## Red Flags and Indicators

### General Transaction Patterns

#### Red Flag 1: Unusual Transaction Patterns
- **Indicator**: Transactions that are unusual for the customer's profile, business type, or normal activity
- **Context**: Deviations from expected behavior may indicate money laundering
- **Data Signal**: Transactions inconsistent with customer profile or historical patterns
- **Feature Mapping**: `transaction_pattern_anomaly`, `unusual_customer_behavior`, `profile_deviation_flag`
- **Source**: FINTRAC Guidance (Financial Entities)

#### Red Flag 2: Rapid Movement of Funds
- **Indicator**: Funds moving quickly through accounts without apparent business purpose
- **Context**: Layering stage of money laundering involves rapid movement to obscure origin
- **Data Signal**: High velocity transactions, short time between deposit and withdrawal
- **Feature Mapping**: `rapid_fund_movement`, `high_velocity_transactions`, `quick_account_turnover`
- **Source**: FINTRAC Guidance (Financial Entities)

#### Red Flag 3: Complex Transaction Structures
- **Indicator**: Unnecessarily complex transaction structures involving multiple parties, accounts, or jurisdictions
- **Context**: Complexity is used to obscure the origin and destination of funds
- **Data Signal**: Multi-party, multi-account, or multi-jurisdiction transaction chains
- **Feature Mapping**: `complex_transaction_structure`, `multi_party_transactions`, `layered_transaction_count`
- **Source**: FINTRAC Guidance (Financial Entities)

#### Red Flag 4: Round-Number Transactions
- **Indicator**: High frequency of transactions in round numbers (e.g., $5,000, $10,000, $50,000)
- **Context**: Round numbers may indicate structuring or bulk transfers
- **Data Signal**: High percentage of round-number transactions
- **Feature Mapping**: `round_number_transaction_pct`, `round_amount_flag`, `bulk_transfer_indicator`
- **Source**: FINTRAC Guidance (Financial Entities)

### Structuring Indicators

#### Red Flag 5: Just Below Threshold Transactions
- **Indicator**: Multiple transactions just below reporting thresholds ($10,000 for CTRs, $3,000 for international transfers)
- **Context**: Deliberate structuring to avoid Currency Transaction Reports or other reporting requirements
- **Data Signal**: Multiple transactions just below $10,000 or $3,000
- **Feature Mapping**: `just_below_threshold_count`, `structuring_pattern_flag`, `ctr_avoidance_indicator`
- **Source**: FINTRAC Guidance (Financial Entities)

#### Red Flag 6: Multiple Small Transactions
- **Indicator**: Breaking large amounts into multiple small transactions to avoid reporting
- **Context**: Structuring technique to avoid detection
- **Data Signal**: Multiple small transactions that could represent one large transaction
- **Feature Mapping**: `multiple_small_transactions`, `fragmented_transaction_pattern`, `structuring_fragmentation_flag`
- **Source**: FINTRAC Guidance (Financial Entities)

#### Red Flag 7: Same-Day Multiple Location Transactions
- **Indicator**: Same individual making transactions at multiple bank locations on the same day
- **Context**: Distributing transactions across locations to avoid detection
- **Data Signal**: Multiple location transactions, same customer, same day
- **Feature Mapping**: `same_day_multi_location_transactions`, `location_diversity_same_day`, `distributed_transaction_pattern`
- **Source**: FINTRAC Guidance (Financial Entities)

### Customer Behavior Indicators

#### Red Flag 8: Reluctance to Provide Information
- **Indicator**: Customer reluctant or evasive when asked for information about transactions or business activities
- **Context**: Legitimate customers typically provide information willingly
- **Data Signal**: Missing or incomplete customer information, especially for high-value transactions
- **Feature Mapping**: `missing_customer_info_flag`, `incomplete_kyc_data`, `information_reluctance_indicator`
- **Source**: FINTRAC Guidance (Financial Entities)

#### Red Flag 9: Unusual Account Activity
- **Indicator**: Account activity that is inconsistent with customer's stated occupation, income, or business
- **Context**: Transaction patterns should align with customer profile
- **Data Signal**: Transaction volume/patterns inconsistent with customer profile
- **Feature Mapping**: `account_activity_anomaly`, `profile_transaction_mismatch`, `unusual_account_behavior`
- **Source**: FINTRAC Guidance (Financial Entities)

#### Red Flag 10: Lifestyle Inconsistencies
- **Indicator**: Customer's transaction activity suggests lifestyle beyond their declared income or means
- **Context**: Large transactions inconsistent with income may indicate illicit proceeds
- **Data Signal**: Transaction volume significantly exceeds declared income
- **Feature Mapping**: `lifestyle_inconsistency_flag`, `income_transaction_mismatch`, `beyond_means_indicator`
- **Source**: FINTRAC Guidance (Financial Entities)

### Geographic and Jurisdictional Indicators

#### Red Flag 11: High-Risk Jurisdiction Transactions
- **Indicator**: Transactions involving countries or jurisdictions known for money laundering, corruption, or weak AML controls
- **Context**: Certain jurisdictions present higher money laundering risk
- **Data Signal**: Transactions to/from high-risk jurisdictions
- **Feature Mapping**: `high_risk_jurisdiction_transactions`, `sanctioned_country_flag`, `offshore_financial_center_flag`
- **Source**: FINTRAC Guidance (Financial Entities)

#### Red Flag 12: Offshore Financial Centers
- **Indicator**: Transactions involving offshore financial centers or tax havens
- **Context**: Offshore centers may be used for layering and integration
- **Data Signal**: Transactions to/from known offshore centers
- **Feature Mapping**: `offshore_financial_center_transactions`, `tax_haven_flag`, `offshore_center_activity`
- **Source**: FINTRAC Guidance (Financial Entities)

#### Red Flag 13: Sanctioned Countries
- **Indicator**: Transactions involving countries subject to international sanctions
- **Context**: Sanctioned countries present high risk for money laundering and terrorist financing
- **Data Signal**: Transactions to/from sanctioned countries
- **Feature Mapping**: `sanctioned_country_transactions`, `sanctions_violation_flag`, `high_risk_sanctioned_jurisdiction`
- **Source**: FINTRAC Guidance (Financial Entities)

### Account Structure Indicators

#### Red Flag 14: Multiple Accounts with Similar Patterns
- **Indicator**: Customer maintains multiple accounts showing similar unusual transaction patterns
- **Context**: Multiple accounts may be used for layering or structuring
- **Data Signal**: Multiple accounts per customer with similar patterns
- **Feature Mapping**: `multiple_accounts_similar_patterns`, `account_network_flag`, `multi_account_layering`
- **Source**: FINTRAC Guidance (Financial Entities)

#### Red Flag 15: Third-Party Account Usage
- **Indicator**: Account used primarily for transactions on behalf of others, especially unrelated third parties
- **Context**: Accounts used as conduits for money laundering
- **Data Signal**: High percentage of third-party transactions
- **Feature Mapping**: `third_party_account_usage`, `conduit_account_flag`, `unrelated_third_party_transactions`
- **Source**: FINTRAC Guidance (Financial Entities)

#### Red Flag 16: Funnel Accounts
- **Indicator**: Account receiving funds from multiple sources and sending to single destination, or vice versa
- **Context**: Funnel accounts are used to aggregate or distribute funds
- **Data Signal**: Asymmetric transaction patterns (many-to-one or one-to-many)
- **Feature Mapping**: `funnel_account_flag`, `aggregation_account_indicator`, `distribution_account_flag`
- **Source**: FINTRAC Guidance (Financial Entities)

### Cash Activity Indicators

#### Red Flag 17: Large Cash Transactions
- **Indicator**: Unusually large cash deposits or withdrawals, especially inconsistent with customer profile
- **Context**: Cash is preferred for placement stage of money laundering
- **Data Signal**: Large cash transactions, especially relative to customer profile
- **Feature Mapping**: `large_cash_transaction_flag`, `unusual_cash_volume`, `cash_transaction_anomaly`
- **Source**: FINTRAC Guidance (Financial Entities)

#### Red Flag 18: Frequent Cash Deposits
- **Indicator**: Frequent cash deposits, especially in amounts just below reporting thresholds
- **Context**: Structured cash deposits to avoid CTRs
- **Data Signal**: High frequency of cash deposits, especially structured
- **Feature Mapping**: `frequent_cash_deposits`, `structured_cash_deposit_pattern`, `cash_deposit_frequency`
- **Source**: FINTRAC Guidance (Financial Entities)

#### Red Flag 19: Cash-Intensive Business Anomalies
- **Indicator**: Cash-intensive business with transaction patterns inconsistent with legitimate operations
- **Context**: Legitimate cash businesses may be used as fronts
- **Data Signal**: Cash-intensive business with unusual patterns
- **Feature Mapping**: `cash_intensive_business_anomaly`, `unusual_cash_business_pattern`, `front_business_indicator`
- **Source**: FINTRAC Guidance (Financial Entities)

### Wire Transfer and EFT Indicators

#### Red Flag 20: Rapid Wire Transfer Sequences
- **Indicator**: Rapid sequence of wire transfers, especially to/from high-risk jurisdictions
- **Context**: Rapid movement indicates layering or integration
- **Data Signal**: High-velocity wire transfers
- **Feature Mapping**: `rapid_wire_sequence`, `wire_transfer_velocity`, `high_speed_wire_transfers`
- **Source**: FINTRAC Guidance (Financial Entities)

#### Red Flag 21: Wire Transfers Without Apparent Purpose
- **Indicator**: Large wire transfers with no apparent business or personal purpose
- **Context**: Wire transfers may be used for layering without legitimate purpose
- **Data Signal**: Large wire transfers with missing or unclear purpose
- **Feature Mapping**: `wire_without_purpose_flag`, `unexplained_wire_transfers`, `purpose_missing_wire_flag`
- **Source**: FINTRAC Guidance (Financial Entities)

#### Red Flag 22: International Wire Transfer Patterns
- **Indicator**: Unusual patterns of international wire transfers, especially to high-risk jurisdictions
- **Context**: International transfers facilitate cross-border money laundering
- **Data Signal**: International wire transfers, especially to high-risk countries
- **Feature Mapping**: `international_wire_pattern_anomaly`, `high_risk_country_wires`, `cross_border_wire_activity`
- **Source**: FINTRAC Guidance (Financial Entities)

### Terrorist Financing Indicators

#### Red Flag 23: Small, Frequent Transactions
- **Indicator**: Multiple small transactions that may be used to fund terrorist activities
- **Context**: Terrorist financing often involves smaller amounts than traditional money laundering
- **Data Signal**: High frequency of small transactions
- **Feature Mapping**: `small_frequent_transactions`, `terrorist_financing_pattern`, `micro_transaction_frequency`
- **Source**: FINTRAC Guidance (Financial Entities)

#### Red Flag 24: Charitable Organization Concerns
- **Indicator**: Transactions with charitable organizations that may be used as fronts for terrorist financing
- **Context**: Charitable organizations may be exploited for terrorist financing
- **Data Signal**: Transactions with charitable organizations, especially in high-risk regions
- **Feature Mapping**: `charitable_organization_transactions`, `charity_terrorist_financing_flag`, `high_risk_charity_transfers`
- **Source**: FINTRAC Guidance (Financial Entities)

#### Red Flag 25: Transactions to Conflict Zones
- **Indicator**: Transactions to regions experiencing conflict or known terrorist activity
- **Context**: Conflict zones may be destinations for terrorist financing
- **Data Signal**: Transactions to conflict zones or high-risk regions
- **Feature Mapping**: `conflict_zone_transactions`, `terrorist_activity_region_flag`, `high_risk_region_transfers`
- **Source**: FINTRAC Guidance (Financial Entities)

### Business Relationship Indicators

#### Red Flag 26: Unusual Business Relationships
- **Indicator**: Transactions between businesses or individuals with no apparent legitimate business relationship
- **Context**: Unrelated party transactions may indicate money laundering
- **Data Signal**: Transactions between unrelated entities
- **Feature Mapping**: `unusual_business_relationship`, `unrelated_party_transactions`, `no_business_relationship_flag`
- **Source**: FINTRAC Guidance (Financial Entities)

#### Red Flag 27: Shell Company Indicators
- **Indicator**: Transactions involving shell companies or companies with minimal operations
- **Context**: Shell companies are commonly used for money laundering
- **Data Signal**: Transactions with companies showing shell company characteristics
- **Feature Mapping**: `shell_company_transactions`, `minimal_operations_company_flag`, `shell_company_indicator`
- **Source**: FINTRAC Guidance (Financial Entities)

#### Red Flag 28: Complex Ownership Structures
- **Indicator**: Business with complex or opaque ownership structures
- **Context**: Complex ownership obscures beneficial ownership
- **Data Signal**: Business with complex ownership (multiple layers, offshore entities)
- **Feature Mapping**: `complex_ownership_structure`, `opaque_ownership_flag`, `multi_layer_ownership_indicator`
- **Source**: FINTRAC Guidance (Financial Entities)

---

## Integration with Detection Model (Task 2)

### Feature Engineering Priorities

1. **General Pattern Features**:
   - `transaction_pattern_anomaly`
   - `rapid_fund_movement`
   - `complex_transaction_structure`
   - `unusual_customer_behavior`

2. **Structuring Features**:
   - `just_below_threshold_count`
   - `structuring_pattern_flag`
   - `multiple_small_transactions`
   - `same_day_multi_location_transactions`

3. **Geographic Risk Features**:
   - `high_risk_jurisdiction_transactions`
   - `offshore_financial_center_flag`
   - `sanctioned_country_transactions`

4. **Account Structure Features**:
   - `multiple_accounts_similar_patterns`
   - `funnel_account_flag`
   - `third_party_account_usage`

---

## Risk Assessment

### High-Risk Combinations

**Critical Red Flags** (when combined):
- Unusual transaction patterns + Rapid fund movement + High-risk jurisdictions
- Structuring + Multiple accounts + Offshore centers
- Large cash transactions + Lifestyle inconsistencies + Complex structures

### Context for Modeling

These indicators should be used:
- **As baseline** for all money laundering detection
- **In combination** with specific red flags from other documents
- **With customer profiling** (compare against expected behavior)

---

## Relationship to Other Documents

This document provides:
- **Foundation indicators** that apply broadly across all money laundering methods
- **Baseline patterns** for comparison
- **Context** for understanding specific red flags in other documents

**Integration**: Use these general indicators alongside specific red flags from:
- Professional Money Laundering (Document 01)
- Bulk Cash Smuggling (Document 02)
- Oil Smuggling (Document 03)
- Chinese ML Networks (Document 04)
- Synthetic Opioids (Document 05)
- Underground Banking (Document 06)
- Human Trafficking (Document 07)

---

## Reporting to FINTRAC

When reporting suspicious transactions, financial institutions should:
- Reference general indicators from this guidance
- Combine with specific red flags from operational alerts
- Document transaction patterns and customer behavior
- Reference FINTRAC Guidance for Financial Entities

---

**Last Updated**: 2025-01-XX  
**Source**: FINTRAC Guidance (Financial Entities)  
**Note**: This document is based on standard AML knowledge and typical FINTRAC guidance content. The actual source document should be reviewed for complete accuracy and additional indicators.
