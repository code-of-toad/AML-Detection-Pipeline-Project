# Professional Money Laundering through Trade and Money Services Businesses

## Source Information

**Source**: FINTRAC Operational Alert  
**Reference Number**: 18/19-SIDEL-025  
**Publication Date**: July 18, 2018  
**URL**: https://fintrac-canafe.canada.ca/intel/operation/oai-ml-eng  
**PDF Version**: Available at source URL (150 KB)

---

## Overview

Professional money launderers are sophisticated actors who engage in large-scale money laundering on behalf of **transnational organized crime groups** such as:
- Drug cartels
- Motorcycle gangs
- Traditional organized crime organizations

**Key Characteristics**:
- Professional money launderers sell their services to criminal groups
- They are involved in the majority of sophisticated money laundering schemes
- They are **not** members of the criminal organizations nor involved in predicate offences
- They present unique identification challenges

**Common Occupations**:
- Accountants, bankers, or lawyers
- **Owners of, or associated with, trading companies or money-services businesses**

---

## Trade-Based Money Laundering

Professional money launderers use trade transactions to legitimize proceeds of crime and move them between jurisdictions and currencies.

### Scheme Type 1: Falsified Documents

**Description**: Schemes involving falsified customs, shipping, and trade finance documents.

#### Red Flags:

1. **Phantom Shipments**
   - **Indicator**: Transferring funds to buy goods that are never shipped, received, or documented
   - **Data Signal**: Large EFT payments to trading companies with no corresponding goods movement
   - **Feature Mapping**: `volume_eft_to_trading_companies`, `txn_count_without_verification`

2. **Falsely Described Goods and Services**
   - **Indicator**: Misrepresenting the quality, quantity, or type of goods or services traded
   - **Data Signal**: Invoice amounts inconsistent with typical prices for described goods
   - **Feature Mapping**: `amount_vs_typical_price_ratio`, `merchant_category_anomalies`

3. **Multiple Invoicing**
   - **Indicator**: Issuing a single invoice but receiving multiple payments
   - **Data Signal**: Multiple payments to same entity for same invoice number
   - **Feature Mapping**: `duplicate_invoice_payments`, `payment_frequency_per_invoice`

4. **Over/Under Invoicing**
   - **Indicator**: Invoicing goods or services at a price above or below market value to move money between exporter and importer
   - **Data Signal**: Transaction amounts significantly different from market prices
   - **Feature Mapping**: `amount_vs_market_price_deviation`, `over_invoice_flag`, `under_invoice_flag`

### Scheme Type 2: Black Market Peso Exchange

**Description**: A form of unregistered foreign currency exchange, typically involving:
- Transnational organized crime groups (Colombian or Mexican drug cartels)
- Placement of proceeds through structured cash deposits in U.S. financial system
- Purchase of U.S. dollars by importers paying in pesos
- Goods purchased with U.S. funds and shipped to origin country
- Pesos returned to cartel through brokers

**Variations Observed by FINTRAC**:

1. **Canadian Trading Company Route**
   - **Indicator**: Brokers send suspected illicit funds from Latin America or U.S. to Canadian trading companies, wholesalers, dealers, and brokers via EFT
   - **Data Signal**: Large EFT transfers from Latin American countries to Canadian trading entities
   - **Feature Mapping**: `volume_eft_from_high_risk_countries`, `txn_count_to_trading_companies`

2. **Correspondent Bank Route**
   - **Indicator**: Brokers send suspected illicit funds from Latin America to U.S.-based entities or China/Hong Kong trading companies through EFT via Canadian financial institution as correspondent bank
   - **Data Signal**: EFT flows through Canadian banks to/from high-risk jurisdictions
   - **Feature Mapping**: `correspondent_bank_flows`, `high_risk_jurisdiction_transfers`

---

## Indicators of Trade-Based Money Laundering by Professional Money Laundering Networks

### Entity Characteristics

#### Red Flag 1: Canadian Small/Medium Import/Export Company Profile
- **Indicator**: Entity is a Canadian small or medium-size import/export company, wholesaler, dealer, or broker
- **Sector Focus**: Operating in sectors dealing with high-volume, high-demand commodities with variable price ranges:
  - Agri-food
  - Textiles
  - Electronics
  - Toys
  - Lumber and paper
  - Automotive or heavy equipment
- **Data Signal**: Business type in KYC data matches above sectors
- **Feature Mapping**: `industry_code_high_risk_trade`, `business_type_trading_company`

#### Red Flag 2: Unusual Business Activities
- **Indicator**: Business activities or business model outside the norm for its sector, or conducts no business activities in Canada
- **Indicator**: Difficult to confirm the exact nature of the business
- **Data Signal**: Missing or vague business descriptions, unusual business patterns
- **Feature Mapping**: `business_activity_anomaly`, `missing_business_info_flag`, `unusual_business_model`

### Transaction Patterns

#### Red Flag 3: Sudden Large Inflows
- **Indicator**: Entity receives a sudden inflow of large-value electronic funds transfers
- **Data Signal**: Sudden spike in EFT volume or count
- **Feature Mapping**: `volume_eft_sudden_increase`, `txn_count_eft_spike`, `velocity_change_eft`

#### Red Flag 4: Geographic Patterns - China/Hong Kong
- **Indicator**: Orders electronic funds transfers to the benefit of China- or Hong Kong-based trading companies or individuals
- **Indicator**: Receives electronic funds transfers from the U.S. and Latin American countries
- **Data Signal**: EFT transactions to/from China, Hong Kong, U.S., Latin America
- **Feature Mapping**: `volume_eft_to_china_hk`, `volume_eft_from_latin_america`, `high_risk_geography_flag`

#### Red Flag 5: Geographic Patterns - U.S./Mexico/Latin America
- **Indicator**: Orders electronic funds transfers to the benefit of entities or individuals in the U.S., Mexico, or Latin American countries
- **Indicator**: Receives such transfers from the U.S.
- **Data Signal**: EFT flows to/from U.S., Mexico, Latin America
- **Feature Mapping**: `volume_eft_to_us_mexico_latam`, `volume_eft_from_us`, `cross_border_flows`

#### Red Flag 6: Offshore Financial Centers
- **Indicator**: Orders or receives electronic funds transfers to/from entities holding bank accounts in Latvia or Cyprus, registered to addresses in:
  - U.K., Cyprus, British Virgin Islands, Panama, Seychelles, Belize, Marshall Islands
  - Other offshore financial centers
- **Data Signal**: Transactions to/from known offshore financial centers
- **Feature Mapping**: `offshore_financial_center_flag`, `high_risk_jurisdiction_count`

#### Red Flag 7: Round Figure Payments
- **Indicator**: Orders or receives payments for goods in round figures or in increments of approximately US$50,000
- **Data Signal**: Transactions in round numbers (e.g., $50,000, $100,000)
- **Feature Mapping**: `round_amount_flag`, `just_below_threshold_count`, `amount_modulo_50000`

#### Red Flag 8: UAE to Canada Transfers
- **Indicator**: Trading company based in United Arab Emirates orders electronic funds transfers to the benefit of individuals or entities in Canada
- **Data Signal**: EFT from UAE to Canada
- **Feature Mapping**: `volume_eft_from_uae`, `uae_to_canada_flag`

#### Red Flag 9: Flow-Through Activity
- **Indicator**: Entity's U.S. dollar business accounts held in Canada exhibit flow-through activity (money taken or transferred out as quickly as it flows in)
- **Data Signal**: High velocity, short time between deposit and withdrawal
- **Feature Mapping**: `flow_through_velocity`, `time_between_deposit_withdrawal`, `account_turnover_rate`

#### Red Flag 10: Currency Import
- **Indicator**: Entity imports currency (predominantly U.S. dollars) from Latin American countries
- **Data Signal**: Cash deposits from Latin American sources
- **Feature Mapping**: `cash_deposits_from_latam`, `usd_import_flag`

#### Red Flag 11: Credit Card Overpayments
- **Indicator**: Entity makes large business purchases by credit card, funded by overpayments
- **Data Signal**: Credit card transactions funded by overpayments
- **Feature Mapping**: `credit_card_overpayment_flag`, `large_business_purchase_cc`

#### Red Flag 12: Legal Professional Accounts
- **Indicator**: Individual issues cheques, purchases drafts, or orders electronic funds transfers through the account of a legal professional for trade-related payments
- **Data Signal**: Transactions through legal professional accounts for trade
- **Feature Mapping**: `legal_professional_account_usage`, `trade_payment_through_lawyer`

---

## Money Services Businesses (MSB) Indicators

### MSB Entity Indicators

#### Red Flag 13: Sudden Inflows Followed by Outflows
- **Indicator**: Canadian money services business receives a sudden inflow of large electronic funds transfers and cash deposits, followed by increased outflow of electronic funds transfers, cheques, and bank drafts made out to multiple unrelated third parties for loans or investments, or to the individual conducting the transaction
- **Data Signal**: Sudden increase in deposits followed by multiple outgoing payments to unrelated parties
- **Feature Mapping**: `sudden_inflow_outflow_pattern`, `multiple_unrelated_party_payments`, `msb_flow_pattern`

#### Red Flag 14: Currency Exchange Patterns
- **Indicator**: Undertakes numerous currency exchanges involving Canadian and U.S. dollars and/or Euros
- **Data Signal**: High frequency of currency exchanges
- **Feature Mapping**: `currency_exchange_frequency`, `cad_usd_eur_exchanges`

#### Red Flag 15: High-Risk Country Business
- **Indicator**: Carries out business largely with or through:
  - Iran or other countries subject to sanctions
  - United Arab Emirates
  - Kuwait
  - Hong Kong
  - China
  - Countries with internal capital controls
- **Data Signal**: Transactions with sanctioned or high-risk countries
- **Feature Mapping**: `sanctioned_country_transactions`, `high_risk_country_business_pct`

#### Red Flag 16: Foreign Exchange and Trading Company Transfers
- **Indicator**: Receives electronic funds transfers from foreign exchange and trading companies based in above-noted countries for real estate transactions, loans, or investments
- **Data Signal**: EFT from foreign exchange/trading companies for real estate/loans/investments
- **Feature Mapping**: `eft_from_fx_trading_companies`, `real_estate_loan_investment_flows`

### MSB Owner/Associate/Employee Indicators

#### Red Flag 17: Personal Account Activity Similar to MSB
- **Indicator**: Money services business owner, associate, or employee maintains personal account activity similar to that of a money services business
- **Data Signal**: Personal account shows business-like transaction patterns
- **Feature Mapping**: `personal_account_business_activity`, `msb_like_personal_account`

#### Red Flag 18: Avoidance of Reporting Obligations
- **Indicator**: Attempts to avoid reporting obligations when exchanging currency on behalf of another money services business
- **Data Signal**: Currency exchanges structured to avoid reporting thresholds
- **Feature Mapping**: `structured_currency_exchanges`, `just_below_reporting_threshold`

#### Red Flag 19: Multiple Identities
- **Indicator**: Lists multiple occupations, addresses, and/or telephone numbers with financial institutions or online
- **Data Signal**: Inconsistent or multiple identity information
- **Feature Mapping**: `multiple_occupations_flag`, `multiple_addresses_flag`, `identity_inconsistency`

#### Red Flag 20: Suspicious Occupations
- **Indicator**: Lists occupation as immigration consultant, student, homemaker, or unemployed
- **Data Signal**: Occupation codes indicating low-income but high transaction volume
- **Feature Mapping**: `occupation_income_mismatch`, `suspicious_occupation_flag`

#### Red Flag 21: Living Beyond Means
- **Indicator**: Lives outside of their reasonable means (e.g., buys real estate beyond what they could reasonably afford on their claimed income)
- **Data Signal**: Transaction volume significantly exceeds declared income
- **Feature Mapping**: `amount_to_income_ratio`, `transaction_volume_vs_income`, `lifestyle_mismatch`

#### Red Flag 22: Account Closure to Avoid Due Diligence
- **Indicator**: Attempts to close account(s) to avoid due diligence questioning
- **Data Signal**: Account closure after suspicious activity flags
- **Feature Mapping**: `account_closure_after_flag`, `due_diligence_avoidance`

#### Red Flag 23: Multiple Bank Accounts with Wires
- **Indicator**: Receives wires and transfers from multiple sources in accounts at numerous banks and credit unions; the individual then depletes these amounts through drafts payable to self or for real estate purchases
- **Data Signal**: Multiple accounts receiving wires, then depleted through self-drafts or real estate
- **Feature Mapping**: `multiple_account_wire_receipts`, `self_draft_pattern`, `real_estate_purchase_from_wires`

#### Red Flag 24: Structured Cash Deposits
- **Indicator**: Places large structured cash deposits into the same account at multiple locations on the same day
- **Data Signal**: Multiple cash deposits on same day, likely structured to avoid reporting
- **Feature Mapping**: `structured_cash_deposits_same_day`, `multiple_location_deposits`, `cash_deposit_structuring`

#### Red Flag 25: Multiple Financial Institutions
- **Indicator**: Is a customer at many banks and credit unions, and negotiates many self-addressed bank drafts from various financial institutions
- **Data Signal**: Accounts at multiple institutions, many self-addressed drafts
- **Feature Mapping**: `multiple_fi_count`, `self_addressed_draft_frequency`

### Import/Export Company with MSB-Like Activity

#### Red Flag 26: MSB-Like Account Activity
- **Indicator**: Canadian import/export company has account activity similar to that of a money services business
- **Sub-indicators**:
  - Receives one or two large electronic funds transfers and then orders multiple outgoing cheques and drafts to multiple third-party individuals and companies
  - Receives large incoming electronic funds transfers from Iran, United Arab Emirates, Kuwait, Hong Kong, and China for living costs, expenses, or spare parts
- **Data Signal**: Import/export company showing MSB-like transaction patterns
- **Feature Mapping**: `import_export_msb_activity`, `large_inflow_multiple_outflows`, `high_risk_country_personal_expense_transfers`

---

## Risk Assessment

### High-Risk Combinations

**Critical Red Flags** (when combined):
- Trade company in high-risk sector + Sudden large EFT inflows + Transfers to China/Hong Kong
- MSB + Sudden inflows + Multiple unrelated party outflows
- Personal account with MSB-like activity + Living beyond means + Multiple financial institutions

### Context for Modeling

These indicators should be used:
- **In combination** (multiple indicators increase risk)
- **With risk-based approach** (not all indicators are equally significant)
- **In conjunction with other money laundering indicators** (from other sources)

---

## Integration with Detection Model (Task 2)

### Feature Engineering Priorities

1. **Geographic Risk Features**:
   - `high_risk_country_transaction_count`
   - `offshore_financial_center_flag`
   - `sanctioned_country_transactions`

2. **Transaction Pattern Features**:
   - `flow_through_velocity`
   - `sudden_inflow_outflow_pattern`
   - `round_amount_transactions`

3. **Business Profile Features**:
   - `industry_code_high_risk_trade`
   - `business_activity_anomaly`
   - `occupation_income_mismatch`

4. **Channel-Specific Features**:
   - `volume_eft_to_trading_companies`
   - `currency_exchange_frequency`
   - `structured_cash_deposits`

---

## Reporting to FINTRAC

When reporting suspicious transactions related to professional money laundering, include the term **#pml** in Part G—Description of suspicious activity on the Suspicious Transaction Report.

---

**Last Updated**: 2025-01-XX  
**Source**: FINTRAC Operational Alert 18/19-SIDEL-025

