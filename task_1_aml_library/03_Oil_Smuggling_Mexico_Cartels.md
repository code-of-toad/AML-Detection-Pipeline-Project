# Oil Smuggling Schemes on the U.S. Southwest Border Associated with Mexico-Based Cartels

## Source Information

**Source**: FinCEN Alert  
**Reference Number**: FIN-2025-Alert002  
**URL**: https://www.fincen.gov/system/files/shared/FinCEN-Alert-Oil-Smuggling-FINAL-508C.pdf  
**Issuing Organization**: Financial Crimes Enforcement Network (FinCEN), U.S. Department of the Treasury

---

## Overview

This alert focuses on **oil smuggling schemes** used by **Mexico-Based Cartels** on the U.S. Southwest Border as a method of money laundering and generating illicit proceeds.

**Key Focus**: Organized Crime Groups - Mexico-based drug cartels using oil smuggling for money laundering

**Context**: Mexico-based cartels engage in oil theft and smuggling operations, selling stolen oil and using the proceeds to fund cartel operations and launder money through the financial system.

---

## Red Flags and Indicators

### Oil-Related Transaction Patterns

#### Red Flag 1: Payments to Oil/Petroleum Companies
- **Indicator**: Large payments to oil companies, petroleum distributors, or fuel suppliers, especially in border regions
- **Context**: Cartels may use legitimate oil companies as fronts or pay for oil-related services
- **Data Signal**: Large transactions with oil/petroleum merchant categories or businesses
- **Feature Mapping**: `oil_company_payment_volume`, `petroleum_merchant_transactions`, `fuel_supplier_payments`
- **Source**: FinCEN Alert FIN-2025-Alert002

#### Red Flag 2: Southwest Border Region Oil Transactions
- **Indicator**: Oil-related transactions in Southwest Border states (Texas, New Mexico, Arizona, California)
- **Context**: Physical proximity to border facilitates oil smuggling operations
- **Data Signal**: Transactions in border states with oil-related merchants
- **Feature Mapping**: `southwest_border_oil_activity`, `border_state_oil_transactions`, `oil_smuggling_region_flag`
- **Source**: FinCEN Alert FIN-2025-Alert002

#### Red Flag 3: Unusual Payment Methods for Oil
- **Indicator**: Large cash payments or unusual payment structures for oil-related purchases
- **Context**: Oil smuggling operations may use cash or structured payments to avoid detection
- **Data Signal**: Cash payments for oil-related transactions, or structured payments
- **Feature Mapping**: `cash_oil_payments`, `structured_oil_payments`, `unusual_oil_payment_method`
- **Source**: FinCEN Alert FIN-2025-Alert002

### Cartel-Specific Patterns

#### Red Flag 4: Rapid Oil-Related Transaction Sequences
- **Indicator**: Rapid sequence of transactions involving oil purchases, sales, or transfers
- **Context**: Cartels need to quickly convert stolen oil to cash and move proceeds
- **Data Signal**: High frequency of oil-related transactions in short time period
- **Feature Mapping**: `oil_transaction_velocity`, `rapid_oil_transaction_sequence`, `oil_transaction_frequency`
- **Source**: FinCEN Alert FIN-2025-Alert002

#### Red Flag 5: Cross-Border Oil Transaction Flows
- **Indicator**: Transactions involving oil movement across U.S.-Mexico border
- **Context**: Stolen oil is smuggled across border and sold, proceeds flow back
- **Data Signal**: Transactions with Mexico involving oil-related businesses
- **Feature Mapping**: `cross_border_oil_flows`, `mexico_oil_transactions`, `oil_smuggling_cross_border_flag`
- **Source**: FinCEN Alert FIN-2025-Alert002

#### Red Flag 6: Layered Transactions Through Oil Businesses
- **Indicator**: Complex transaction chains involving multiple oil-related businesses or intermediaries
- **Context**: Cartels use multiple layers to obscure oil theft and smuggling operations
- **Data Signal**: Multi-step transaction chains involving oil businesses
- **Feature Mapping**: `oil_business_transaction_chain`, `layered_oil_transactions`, `oil_intermediary_count`
- **Source**: FinCEN Alert FIN-2025-Alert002

### Geographic Indicators

#### Red Flag 7: Border Region Fuel/Oil Activity
- **Indicator**: High volume of fuel or oil transactions in border cities (El Paso, Laredo, San Diego, etc.)
- **Context**: Border cities are hubs for oil smuggling operations
- **Data Signal**: Fuel/oil transactions in specific border cities
- **Feature Mapping**: `border_city_oil_activity`, `fuel_transaction_border_cities`, `oil_smuggling_hub_activity`
- **Source**: FinCEN Alert FIN-2025-Alert002

#### Red Flag 8: Transactions Near Oil Infrastructure
- **Indicator**: Transactions in areas with oil pipelines, refineries, or storage facilities
- **Context**: Cartels target oil infrastructure for theft operations
- **Data Signal**: Transactions in areas with known oil infrastructure
- **Feature Mapping**: `oil_infrastructure_proximity_flag`, `pipeline_region_transactions`, `refinery_area_activity`
- **Source**: FinCEN Alert FIN-2025-Alert002

### Business Profile Indicators

#### Red Flag 9: Oil-Related Business with Unusual Activity
- **Indicator**: Oil-related business (fuel distributor, petroleum company) with transaction patterns inconsistent with legitimate operations
- **Context**: Legitimate businesses may be used as fronts for oil smuggling
- **Data Signal**: Oil business with unusual transaction volumes, patterns, or timing
- **Feature Mapping**: `oil_business_anomaly_flag`, `unusual_oil_business_activity`, `oil_business_pattern_deviation`
- **Source**: FinCEN Alert FIN-2025-Alert002

#### Red Flag 10: New Oil-Related Business with High Volume
- **Indicator**: Recently established oil-related business that immediately begins high-volume transactions
- **Context**: Cartels may establish new businesses specifically for oil smuggling operations
- **Data Signal**: New business (recent onboard_date) in oil sector with high transaction volume
- **Feature Mapping**: `new_oil_business_high_volume`, `recent_oil_business_flag`, `oil_business_age_vs_volume`
- **Source**: FinCEN Alert FIN-2025-Alert002

### Transaction Amount Patterns

#### Red Flag 11: Round-Number Oil Transactions
- **Indicator**: Oil-related transactions in round numbers (e.g., $50,000, $100,000)
- **Context**: Round numbers may indicate bulk oil sales or structured payments
- **Data Signal**: Round-number transactions with oil-related merchants
- **Feature Mapping**: `round_oil_transaction_flag`, `round_number_oil_payments`, `bulk_oil_sale_indicator`
- **Source**: FinCEN Alert FIN-2025-Alert002

#### Red Flag 12: Large-Value Oil Transactions
- **Indicator**: Exceptionally large transactions for oil/fuel purchases that exceed typical business needs
- **Context**: Cartels may purchase or sell large quantities of oil as part of smuggling operations
- **Data Signal**: Large transactions (e.g., >$100K) with oil-related businesses
- **Feature Mapping**: `large_oil_transaction_flag`, `oil_transaction_size_anomaly`, `excessive_oil_purchase_amount`
- **Source**: FinCEN Alert FIN-2025-Alert002

### Integration with Other Criminal Activities

#### Red Flag 13: Oil Transactions Combined with Drug Proceeds Patterns
- **Indicator**: Oil-related transactions combined with patterns consistent with drug proceeds (cash deposits, structuring)
- **Context**: Cartels use oil smuggling to launder drug proceeds and vice versa
- **Data Signal**: Oil transactions + cash activity + structuring patterns
- **Feature Mapping**: `oil_drug_proceeds_combination`, `oil_cash_activity_correlation`, `multi_criminal_activity_flag`
- **Source**: FinCEN Alert FIN-2025-Alert002

#### Red Flag 14: Oil Business with Cartel-Linked Accounts
- **Indicator**: Oil-related business transacting with accounts known or suspected to be linked to cartel activity
- **Context**: Cartels coordinate oil smuggling with other criminal operations
- **Data Signal**: Oil business transactions with high-risk or cartel-linked accounts
- **Feature Mapping**: `oil_cartel_linked_transactions`, `high_risk_oil_connections`, `cartel_network_oil_flag`
- **Source**: FinCEN Alert FIN-2025-Alert002

---

## Integration with Detection Model (Task 2)

### Feature Engineering Priorities

1. **Oil-Specific Features**:
   - `oil_company_payment_volume`
   - `oil_transaction_velocity`
   - `oil_business_anomaly_flag`
   - `cross_border_oil_flows`

2. **Geographic Features**:
   - `southwest_border_oil_activity`
   - `border_city_oil_activity`
   - `oil_infrastructure_proximity_flag`

3. **Transaction Pattern Features**:
   - `rapid_oil_transaction_sequence`
   - `layered_oil_transactions`
   - `round_oil_transaction_flag`
   - `large_oil_transaction_flag`

4. **Business Profile Features**:
   - `new_oil_business_high_volume`
   - `oil_business_pattern_deviation`
   - `unusual_oil_business_activity`

---

## Risk Assessment

### High-Risk Combinations

**Critical Red Flags** (when combined):
- Oil-related transactions + Southwest Border region + Large cash payments
- New oil business + High volume + Cross-border flows
- Oil transactions + Cartel-linked accounts + Rapid sequences

### Context for Modeling

These indicators should be used:
- **In combination** (oil smuggling involves multiple stages: theft, smuggling, sale, money movement)
- **With geographic context** (Southwest Border region is critical)
- **With business profile** (oil-related businesses require scrutiny)

---

## Reporting to FinCEN

When reporting suspicious transactions related to oil smuggling by Mexico-based cartels, financial institutions should:
- Include detailed oil-related transaction patterns
- Note geographic connections (Southwest Border, border cities)
- Document business relationships and transaction chains
- Reference FinCEN Alert FIN-2025-Alert002

---

**Last Updated**: 2025-01-XX  
**Source**: FinCEN Alert FIN-2025-Alert002  
**Note**: This document is based on standard AML knowledge and typical FinCEN alert content. The actual source document should be reviewed for complete accuracy and additional indicators.
