"""
Feature Engineering Script: Phase 2.7 - Profile Features
Purpose: Engineer customer profile-based risk features for AML detection model
Input: features/intermediate/customer_base.csv
Output: features/by_category/profile_features.csv

Features Created:
- Industry/Occupation risk indicators
- Account age and business age
- Missing data flags
- Profile-based risk flags
"""

import pandas as pd
import numpy as np
from pathlib import Path
from report_utils import generate_feature_report

# Configuration
BASE_DIR = Path(__file__).parent.parent
INPUT_DIR = BASE_DIR / 'features' / 'intermediate'
OUTPUT_DIR = BASE_DIR / 'features' / 'by_category'
REPORT_DIR = BASE_DIR / 'features' / 'reports'

# Industry/Occupation risk code mappings
INDUSTRY_OCCUPATION_INDICATORS = {
    'oil_company': ['0711', '0919', '4112', '4113'],
    'msb_business': ['7499', '7214', '7215'],
    'maybe_massage_parlor': ['8639', '8665', '8669', '9799'],
    'ecom_business': ['7721', '6921', '7799', '9699'],
    'hotel_or_motel': ['9111', '9114'],
    'shell_company': ['7215', '7214', '7771', '7739', '7761'],
    'cash_intensive': ['6331', '6561', '6311', '6312', '6599', '6391', '9211', '9212', '9213', '6412', '6413'],
    'real_estate': ['7511', '7512', '7599', '7611', '4491'],
    'precious_metal_business': ['6561', '6311', '6312'],
    'professional_service': ['7731', '7739', '7761', '7771'],
    'transportation': ['4842', '4581', '4561', '4569'],
    'vague_category': ['3999', '5999', '6599', '7799', '9999', '9699', '9799', '7499']
}

def load_data():
    """Load intermediate data files"""
    print("Loading data...")
    customers = pd.read_csv(INPUT_DIR / 'customer_base.csv')
    print(f"  Loaded {len(customers):,} customers")
    return customers

def engineer_profile_features(customers):
    """Engineer profile-based features for each customer"""
    print("\nEngineering profile features...")
    
    # Initialize features dataframe
    features = pd.DataFrame()
    features['customer_id'] = customers['customer_id']
    
    # 1. Account Age and Business Age
    print("  Calculating account and business age...")
    
    features['account_age'] = customers['account_age'].fillna(0)
    features['business_age'] = customers['birth_business_age'].fillna(0)
    
    # New account flag (account age < 1 year)
    features['new_account_flag'] = (features['account_age'] < 1.0).astype(int)
    
    # Very new business flag (business age < 1 year for businesses)
    business_mask = customers['kyc_type'] == 'business'
    features['very_new_business_flag'] = (
        business_mask & (features['business_age'] < 1.0)
    ).astype(int)
    
    # 2. Industry/Occupation Risk Indicators
    print("  Calculating industry/occupation risk indicators...")
    
    # Combine industry_code and occupation_code (one will be null depending on customer type)
    customers['industry_occupation_code'] = customers['industry_code'].fillna(customers['occupation_code'])
    
    # Create indicator features for each risk category
    for indicator_name, codes in INDUSTRY_OCCUPATION_INDICATORS.items():
        # Check if customer's code matches any in the list
        features[f'is_{indicator_name}'] = customers['industry_occupation_code'].isin(codes).astype(int)
    
    # 3. Missing Data Flags
    print("  Calculating missing data flags...")
    
    # Income/sales missing
    features['has_missing_income'] = (
        (customers['income_cad'].isna()) | (customers['income_cad'] <= 0)
    ).astype(int)
    
    features['has_missing_sales'] = (
        (customers['sales_cad'].isna()) | (customers['sales_cad'] <= 0)
    ).astype(int)
    
    # Industry/occupation code missing
    features['has_missing_industry_occupation'] = (
        customers['industry_occupation_code'].isna()
    ).astype(int)
    
    # Geographic data missing
    features['has_missing_country'] = customers['country'].isna().astype(int)
    features['has_missing_province'] = customers['province'].isna().astype(int)
    features['has_missing_city'] = customers['city'].isna().astype(int)
    
    # 4. High-Risk Industry/Occupation Flags
    print("  Calculating high-risk flags...")
    
    # High-risk trade industries (for businesses)
    high_risk_industries = ['7499', '7214', '7215', '7771', '7739', '7761']  # MSB, shell companies, professional services
    features['industry_code_high_risk_trade'] = (
        business_mask & 
        customers['industry_code'].isin(high_risk_industries)
    ).astype(int)
    
    # Suspicious occupations (for individuals)
    # Low-income occupations with high transaction volumes are suspicious
    suspicious_occupations = ['10019', '10020']  # Student, Homemaker, Unemployed (if available)
    individual_mask = customers['kyc_type'] == 'individual'
    features['suspicious_occupation_flag'] = (
        individual_mask & 
        customers['occupation_code'].isin(suspicious_occupations)
    ).astype(int)
    
    # 5. Customer Type Features
    print("  Calculating customer type features...")
    
    features['is_individual'] = individual_mask.astype(int)
    features['is_business'] = business_mask.astype(int)
    
    # 6. Profile Risk Score (Composite)
    print("  Calculating profile risk score...")
    
    risk_score = 0
    risk_score += features['new_account_flag'] * 1
    risk_score += features['very_new_business_flag'] * 2
    risk_score += features['is_msb_business'] * 3
    risk_score += features['is_shell_company'] * 3
    risk_score += features['is_cash_intensive'] * 2
    risk_score += features['is_vague_category'] * 1
    risk_score += features['has_missing_income'] * 1
    risk_score += features['has_missing_sales'] * 1
    risk_score += features['has_missing_industry_occupation'] * 1
    risk_score += features['industry_code_high_risk_trade'] * 2
    risk_score += features['suspicious_occupation_flag'] * 1
    
    features['profile_risk_score'] = risk_score
    
    # High risk flag
    features['high_profile_risk'] = (features['profile_risk_score'] >= 3).astype(int)
    
    # Fill NaN values
    features = features.fillna(0)
    
    # Ensure integer columns are integers
    int_columns = [col for col in features.columns if col != 'customer_id' and (
        'flag' in col.lower() or 
        'has_' in col.lower() or
        'is_' in col.lower() or
        'score' in col.lower() or
        'age' in col.lower()
    )]
    for col in int_columns:
        if col in features.columns:
            features[col] = features[col].astype(int)
    
    return features

def validate_features(features):
    """Validate the engineered features"""
    print("\nValidating features...")
    
    # Check for null values
    null_counts = features.isnull().sum()
    if null_counts.sum() > 0:
        print(f"  Warning: Found null values in columns: {null_counts[null_counts > 0].to_dict()}")
    else:
        print("  No null values found")
    
    # Check ranges
    print(f"  Account age range: {features['account_age'].min():.2f} to {features['account_age'].max():.2f} years")
    print(f"  Business age range: {features['business_age'].min():.2f} to {features['business_age'].max():.2f} years")
    print(f"  New accounts: {features['new_account_flag'].sum():,} customers")
    print(f"  Very new businesses: {features['very_new_business_flag'].sum():,} customers")
    
    # Industry/occupation indicators summary
    indicator_cols = [col for col in features.columns if col.startswith('is_') and col != 'is_individual' and col != 'is_business']
    print(f"\n  Industry/Occupation indicators:")
    for col in indicator_cols[:5]:  # Show first 5
        count = features[col].sum()
        print(f"    {col}: {count:,} customers")
    if len(indicator_cols) > 5:
        print(f"    ... and {len(indicator_cols) - 5} more indicators")
    
    print(f"  High profile risk: {features['high_profile_risk'].sum():,} customers")
    
    print("  Validation complete")

def main():
    """Main execution"""
    print("=" * 60)
    print("Phase 2.7: Profile Features")
    print("=" * 60)
    
    # Load data
    customers = load_data()
    
    # Engineer features
    features = engineer_profile_features(customers)
    
    # Validate
    validate_features(features)
    
    # Save output
    print("\nSaving features...")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / 'profile_features.csv'
    features.to_csv(output_path, index=False)
    
    print(f"\nSaved: {output_path}")
    print(f"Features created: {len(features.columns) - 1}")  # -1 for customer_id
    print(f"Customers: {len(features):,}")
    print(f"\nFeature columns: {list(features.columns)}")
    
    # Generate report
    print("\nGenerating validation report...")
    generate_feature_report(features, 'profile_features', REPORT_DIR)
    
    print("\n" + "=" * 60)
    print("Phase 2.7 Complete!")
    print("=" * 60)

if __name__ == '__main__':
    main()
