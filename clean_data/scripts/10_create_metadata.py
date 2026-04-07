"""
Feature Engineering Script: Phase 4 - Feature Metadata
Purpose: Create feature metadata linking features to AML red flags for Task 3 (Explainability)
Input: All feature files, Red_Flag_to_Feature_Mapping.md
Output: features/final/feature_metadata.csv

This metadata enables explainability by linking model features back to specific AML red flags.
"""

import pandas as pd
from pathlib import Path

# Configuration
BASE_DIR = Path(__file__).parent.parent
OUTPUT_DIR = BASE_DIR / 'features' / 'final'

# Feature metadata mapping
# Format: feature_name -> (category, red_flag_source, red_flag_description, data_signal, feature_type, description)
FEATURE_METADATA = {
    # Velocity Features
    'txn_count_total': ('velocity_features', 'General indicators', 'High Transaction Frequency', 
                       'Unusually high number of transactions', 'count', 'Total transaction count'),
    'txn_per_day_avg': ('velocity_features', 'General indicators', 'High Transaction Frequency',
                       'Average transactions per day', 'average', 'Average transactions per day'),
    'txn_velocity': ('velocity_features', 'General indicators', 'High Transaction Frequency',
                    'Transactions per day', 'rate', 'Transaction velocity (transactions per day)'),
    'high_frequency_customer_flag': ('velocity_features', 'General indicators', 'High Transaction Frequency',
                                    'Customers with >500 transactions', 'flag', 'Boolean flag for high-frequency customers'),
    'flow_through_velocity_hours': ('velocity_features', '01_Professional_Money_Laundering_Trade_MSB.md', 'Flow-Through Activity',
                                    'Average time between deposit and withdrawal', 'hours', 'Average hours between credit and debit transactions'),
    'time_between_deposit_withdrawal': ('velocity_features', '01_Professional_Money_Laundering_Trade_MSB.md', 'Flow-Through Activity',
                                       'Hours between credit and debit', 'hours', 'Time between deposit and withdrawal'),
    'account_turnover_rate': ('velocity_features', '01_Professional_Money_Laundering_Trade_MSB.md', 'Flow-Through Activity',
                             'Volume out / Volume in ratio', 'ratio', 'Account turnover rate (debit volume / credit volume)'),
    'sudden_inflow_outflow_pattern': ('velocity_features', '01_Professional_Money_Laundering_Trade_MSB.md', 'Sudden Inflow/Outflow Patterns',
                                     'Large inflow followed by multiple outflows', 'flag', 'Boolean flag for sudden inflow/outflow pattern'),
    
    # Amount Features
    'amount_mean': ('amount_features', 'General indicators', 'Unusual Amount Patterns',
                   'Average transaction amount', 'average', 'Mean transaction amount'),
    'amount_stddev': ('amount_features', 'General indicators', 'Unusual Amount Patterns',
                     'Standard deviation of amounts', 'statistic', 'Standard deviation of transaction amounts'),
    'round_amount_pct': ('amount_features', 'General indicators', 'Round Number Transactions',
                        'Percentage of transactions with round amounts', 'percentage', 'Percentage of transactions with round numbers'),
    'round_amount_flag': ('amount_features', 'General indicators', 'Round Number Transactions',
                         'If >50% of transactions are round numbers', 'flag', 'Boolean flag for round number pattern'),
    'just_below_threshold_count': ('amount_features', '01_Professional_Money_Laundering_Trade_MSB.md', 'Structuring',
                                   'Count of transactions $9,000-$10,000', 'count', 'Number of transactions just below $10K threshold'),
    'structuring_pattern_flag': ('amount_features', '01_Professional_Money_Laundering_Trade_MSB.md', 'Structuring',
                                'Multiple just-below-threshold transactions', 'flag', 'Boolean flag for structuring pattern'),
    'large_txn_count_10k': ('amount_features', 'General indicators', 'Large Transaction Outliers',
                           'Count of transactions > $10K', 'count', 'Number of transactions exceeding $10,000'),
    'large_txn_count_50k': ('amount_features', 'General indicators', 'Large Transaction Outliers',
                           'Count of transactions > $50K', 'count', 'Number of transactions exceeding $50,000'),
    'large_txn_count_100k': ('amount_features', 'General indicators', 'Large Transaction Outliers',
                            'Count of transactions > $100K', 'count', 'Number of transactions exceeding $100,000'),
    'amount_max_ratio_mean': ('amount_features', 'General indicators', 'Large Transaction Outliers',
                             'Max transaction / Mean transaction', 'ratio', 'Ratio of maximum to mean transaction amount'),
    
    # Channel Features
    'wire_txn_count': ('channel_features', '01_Professional_Money_Laundering_Trade_MSB.md', 'Wire Transfer Usage',
                      'Total number of wire transfer transactions', 'count', 'Count of wire transfer transactions'),
    'wire_volume_total': ('channel_features', '01_Professional_Money_Laundering_Trade_MSB.md', 'Wire Transfer Usage',
                         'Total wire transfer volume', 'sum', 'Total volume of wire transfers'),
    'has_wire_transfers': ('channel_features', '01_Professional_Money_Laundering_Trade_MSB.md', 'Wire Transfer Usage',
                          'Customer uses wire transfers', 'flag', 'Boolean flag indicating wire transfer usage'),
    'abm_cash_txn_count': ('channel_features', '01_Professional_Money_Laundering_Trade_MSB.md', 'Cash Transactions',
                          'Count of cash withdrawal transactions', 'count', 'Number of cash transactions via ABM'),
    'abm_cash_volume': ('channel_features', '01_Professional_Money_Laundering_Trade_MSB.md', 'Cash Transactions',
                       'Total cash withdrawal volume', 'sum', 'Total volume of cash transactions'),
    'structured_cash_deposits_same_day': ('channel_features', '01_Professional_Money_Laundering_Trade_MSB.md', 'Cash Transactions',
                                         'Multiple cash deposits same day', 'count', 'Number of days with multiple cash deposits'),
    'has_western_union': ('channel_features', '01_Professional_Money_Laundering_Trade_MSB.md', 'MSB-Like Activity',
                         'Customer uses Western Union', 'flag', 'Boolean flag for Western Union usage'),
    'channels_used_count': ('channel_features', 'General indicators', 'Channel Diversification',
                           'Number of unique transaction channels used', 'count', 'Count of different channels used'),
    'multi_channel_flag': ('channel_features', 'General indicators', 'Channel Diversification',
                          'Uses 3+ channels', 'flag', 'Boolean flag for multi-channel usage'),
    
    # Geographic Features
    'country_diversity': ('geographic_features', '01_Professional_Money_Laundering_Trade_MSB.md', 'Cross-Border Patterns',
                         'Number of unique countries in transactions', 'count', 'Count of unique countries in transactions'),
    'cross_border_flag': ('geographic_features', '01_Professional_Money_Laundering_Trade_MSB.md', 'Cross-Border Patterns',
                         'Transactions in different country than customer', 'flag', 'Boolean flag for cross-border transactions'),
    'is_country_financial_hub': ('geographic_features', '01_Professional_Money_Laundering_Trade_MSB.md', 'High-Risk Country Transactions',
                                'Transactions in financial hubs (US, GB, SG, HK)', 'flag', 'Boolean flag for financial hub transactions'),
    'is_country_offshore_structure_jurisdiction': ('geographic_features', '01_Professional_Money_Laundering_Trade_MSB.md', 'High-Risk Country Transactions',
                                                   'Transactions in offshore jurisdictions (LU, CY, IE, NL)', 'flag', 'Boolean flag for offshore jurisdiction'),
    
    # Time Features
    'after_hours_txn_pct': ('time_features', 'General indicators', 'Unusual Transaction Times',
                           'Percentage of transactions outside 9 AM - 5 PM', 'percentage', 'Percentage of after-hours transactions'),
    'weekend_txn_pct': ('time_features', 'General indicators', 'Unusual Transaction Times',
                       'Percentage of transactions on weekends', 'percentage', 'Percentage of weekend transactions'),
    'midnight_txn_count': ('time_features', 'General indicators', 'Unusual Transaction Times',
                          'Count of transactions between midnight and 6 AM', 'count', 'Number of midnight transactions'),
    'rapid_fire_flag': ('time_features', 'General indicators', 'High Transaction Frequency',
                       'Multiple transactions within 1 hour', 'flag', 'Boolean flag for rapid-fire pattern'),
    
    # Behavioral Features
    'amount_to_income_ratio': ('behavioral_features', '01_Professional_Money_Laundering_Trade_MSB.md', 'Living Beyond Means',
                               'Transaction volume / Declared income', 'ratio', 'Ratio of total transaction volume to declared income'),
    'amount_to_sales_ratio': ('behavioral_features', '01_Professional_Money_Laundering_Trade_MSB.md', 'Living Beyond Means',
                             'Transaction volume / Declared sales', 'ratio', 'Ratio of total transaction volume to declared sales'),
    'lifestyle_mismatch': ('behavioral_features', '01_Professional_Money_Laundering_Trade_MSB.md', 'Living Beyond Means',
                         'Transactions > 2x income/sales', 'flag', 'Boolean flag for lifestyle mismatch'),
    'severe_lifestyle_mismatch': ('behavioral_features', '01_Professional_Money_Laundering_Trade_MSB.md', 'Living Beyond Means',
                                 'Transactions > 5x income/sales', 'flag', 'Boolean flag for severe lifestyle mismatch'),
    'has_missing_income': ('behavioral_features', '01_Professional_Money_Laundering_Trade_MSB.md', 'Missing Business Information',
                          'Missing or invalid income data', 'flag', 'Boolean flag for missing income'),
    'has_missing_sales': ('behavioral_features', '01_Professional_Money_Laundering_Trade_MSB.md', 'Missing Business Information',
                         'Missing or invalid sales data', 'flag', 'Boolean flag for missing sales'),
    
    # Profile Features
    'new_account_flag': ('profile_features', 'General indicators', 'New Account Risk',
                        'Account age < 1 year', 'flag', 'Boolean flag for new account'),
    'very_new_business_flag': ('profile_features', 'General indicators', 'New Account Risk',
                              'Business age < 1 year', 'flag', 'Boolean flag for very new business'),
    'is_msb_business': ('profile_features', '01_Professional_Money_Laundering_Trade_MSB.md', 'MSB-Like Activity',
                       'Industry code indicates MSB', 'flag', 'Boolean flag for MSB business'),
    'is_shell_company': ('profile_features', '01_Professional_Money_Laundering_Trade_MSB.md', 'Shell Company Indicators',
                       'Industry code indicates shell company', 'flag', 'Boolean flag for shell company'),
    'is_cash_intensive': ('profile_features', '01_Professional_Money_Laundering_Trade_MSB.md', 'Cash-Intensive Business',
                         'Industry code indicates cash-intensive business', 'flag', 'Boolean flag for cash-intensive business'),
    'is_real_estate': ('profile_features', '01_Professional_Money_Laundering_Trade_MSB.md', 'Real Estate ML Risk',
                      'Industry code indicates real estate', 'flag', 'Boolean flag for real estate business'),
    'industry_code_high_risk_trade': ('profile_features', '01_Professional_Money_Laundering_Trade_MSB.md', 'High-Risk Trade Industries',
                                     'Business in high-risk trade industry', 'flag', 'Boolean flag for high-risk trade industry'),
    'suspicious_occupation_flag': ('profile_features', '01_Professional_Money_Laundering_Trade_MSB.md', 'Suspicious Occupation',
                                  'Occupation inconsistent with transaction volume', 'flag', 'Boolean flag for suspicious occupation'),

    # Stream B: Transaction-Derived Features (aggregates of transaction-level risk scores)
    'txn_score_max': ('transaction_derived_features', 'General indicators', 'Transaction-Level Risk',
                      'Max per-transaction risk score (0-1)', 'statistic', 'Maximum transaction-level risk score per customer'),
    'txn_score_mean': ('transaction_derived_features', 'General indicators', 'Transaction-Level Risk',
                       'Mean per-transaction risk score', 'average', 'Mean transaction-level risk score per customer'),
    'txn_score_std': ('transaction_derived_features', 'General indicators', 'Transaction-Level Risk',
                      'Std of per-transaction risk scores', 'statistic', 'Standard deviation of transaction-level risk scores per customer'),
    'txn_score_count_above_threshold': ('transaction_derived_features', 'General indicators', 'Transaction-Level Risk',
                                        'Count of transactions with score >= threshold (e.g. 0.5)', 'count', 'Number of high-risk transactions per customer'),
    'txn_score_pct_above_threshold': ('transaction_derived_features', 'General indicators', 'Transaction-Level Risk',
                                     'Percentage of transactions with score >= threshold', 'percentage', 'Proportion of high-risk transactions per customer'),
}

def create_metadata():
    """Create feature metadata DataFrame"""
    print("Creating feature metadata...")
    
    metadata_rows = []
    
    for feature_name, (category, red_flag_source, red_flag_description, data_signal, feature_type, description) in FEATURE_METADATA.items():
        metadata_rows.append({
            'feature_name': feature_name,
            'feature_category': category,
            'red_flag_source': red_flag_source,
            'red_flag_description': red_flag_description,
            'data_signal': data_signal,
            'feature_type': feature_type,
            'description': description
        })
    
    metadata_df = pd.DataFrame(metadata_rows)
    
    print(f"  Created metadata for {len(metadata_df)} features")
    return metadata_df

def main():
    """Main execution"""
    print("=" * 60)
    print("Phase 4: Feature Metadata")
    print("=" * 60)
    
    # Create metadata
    metadata_df = create_metadata()
    
    # Save output
    print("\nSaving metadata...")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / 'feature_metadata.csv'
    metadata_df.to_csv(output_path, index=False)
    
    print(f"\nSaved: {output_path}")
    print(f"Features documented: {len(metadata_df)}")
    print(f"\nMetadata columns: {list(metadata_df.columns)}")
    
    print("\n" + "=" * 60)
    print("Phase 4 Complete!")
    print("=" * 60)
    print(f"\nFeature metadata ready for Task 3 (Explainability)")
    print(f"   File: {output_path}")

if __name__ == '__main__':
    main()
