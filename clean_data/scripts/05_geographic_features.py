"""
Feature Engineering Script: Phase 2.4 - Geographic Features
Purpose: Engineer geographic risk features for AML detection model
Input: features/intermediate/transactions_combined.csv, features/intermediate/customer_base.csv
Output: features/by_category/geographic_features.csv

Features Created:
- Geographic diversity (countries, provinces, cities)
- Cross-border transaction indicators
- High-risk geography flags (based on country risk indicators)
- Geographic dispersion metrics
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

# Country risk indicator mappings
COUNTRY_RISK_INDICATORS = {
    'financial_hub': ['US', 'GB', 'SG', 'HK'],
    'offshore_structure_jurisdiction': ['LU', 'CY', 'IE', 'NL'],
    'trade_conduit': ['HK', 'NL', 'SG'],
    'private_banking_hub': ['SG', 'LU', 'HK'],
    'shell_company_jurisdiction': ['GB', 'CY', 'IE'],
    'tbml_high_risk': ['HK', 'NL', 'SG'],
    'major_port': ['NL', 'HK', 'SG'],
    'real_estate_ml_risk': ['US', 'GB', 'CA'],
    'hnwi_concentration': ['SG', 'LU', 'HK'],
    'high_cash_usage': ['DE']
}

def load_data():
    """Load intermediate data files"""
    print("Loading data...")
    transactions = pd.read_csv(INPUT_DIR / 'transactions_combined.csv', low_memory=False)
    customers = pd.read_csv(INPUT_DIR / 'customer_base.csv')
    print(f"  Loaded {len(transactions):,} transactions")
    print(f"  Loaded {len(customers):,} customers")
    return transactions, customers

def engineer_geographic_features(transactions, customers):
    """Engineer geographic features for each customer"""
    print("\nEngineering geographic features...")
    
    # Initialize features dataframe
    features = pd.DataFrame()
    features['customer_id'] = customers['customer_id']
    
    # Create customer location mapping
    customer_locations = customers[['customer_id', 'country', 'province', 'city']].copy()
    customer_locations = customer_locations.rename(columns={
        'country': 'customer_country',
        'province': 'customer_province',
        'city': 'customer_city'
    })
    
    # Filter transactions with geographic data (ABM and Card only)
    transactions_geo = transactions[
        transactions['country'].notna() | 
        transactions['province'].notna() | 
        transactions['city'].notna()
    ].copy()
    
    print(f"  Transactions with geographic data: {len(transactions_geo):,} ({len(transactions_geo)/len(transactions)*100:.1f}%)")
    
    if len(transactions_geo) == 0:
        print("  Warning: No geographic data found in transactions")
        # Return empty features with zeros
        features['country_diversity'] = 0
        features['province_diversity'] = 0
        features['city_diversity'] = 0
        features['cross_border_flag'] = 0
        features['cross_border_txn_count'] = 0
        features['cross_border_txn_pct'] = 0
        features['province_diversity'] = 0
        features['city_diversity'] = 0
        # Add all country risk indicators as zeros
        for risk_type in COUNTRY_RISK_INDICATORS.keys():
            features[f'is_country_{risk_type}'] = 0
        return features
    
    # Merge with customer locations
    transactions_geo = transactions_geo.merge(
        customer_locations,
        on='customer_id',
        how='left'
    )
    
    # 1. Geographic Diversity (from transactions)
    print("  Calculating geographic diversity...")
    
    # Country diversity
    country_counts = transactions_geo[transactions_geo['country'].notna()].groupby('customer_id')['country'].nunique()
    features['country_diversity'] = features['customer_id'].map(country_counts).fillna(0).astype(int)
    
    # Province diversity
    province_counts = transactions_geo[transactions_geo['province'].notna()].groupby('customer_id')['province'].nunique()
    features['province_diversity'] = features['customer_id'].map(province_counts).fillna(0).astype(int)
    
    # City diversity
    city_counts = transactions_geo[transactions_geo['city'].notna()].groupby('customer_id')['city'].nunique()
    features['city_diversity'] = features['customer_id'].map(city_counts).fillna(0).astype(int)
    
    # 2. Cross-Border Transactions
    print("  Calculating cross-border indicators...")
    
    # Transactions in different country than customer's country
    cross_border_mask = (
        transactions_geo['country'].notna() & 
        transactions_geo['customer_country'].notna() &
        (transactions_geo['country'] != transactions_geo['customer_country'])
    )
    cross_border_txns = transactions_geo[cross_border_mask]
    
    if len(cross_border_txns) > 0:
        cross_border_counts = cross_border_txns.groupby('customer_id').size()
        total_txn_counts = transactions_geo.groupby('customer_id').size()
        
        features['cross_border_txn_count'] = features['customer_id'].map(cross_border_counts).fillna(0).astype(int)
        features['cross_border_txn_pct'] = (
            features['cross_border_txn_count'] / 
            features['customer_id'].map(total_txn_counts).fillna(1)
        ).fillna(0)
        features['cross_border_flag'] = (features['cross_border_txn_count'] > 0).astype(int)
    else:
        features['cross_border_txn_count'] = 0
        features['cross_border_txn_pct'] = 0
        features['cross_border_flag'] = 0
    
    # 3. High-Risk Geography Flags (Country Risk Indicators)
    print("  Calculating country risk indicators...")
    
    # For each risk type, check if customer has transactions in those countries
    for risk_type, countries in COUNTRY_RISK_INDICATORS.items():
        risk_countries_mask = transactions_geo['country'].isin(countries)
        customers_with_risk = transactions_geo[risk_countries_mask]['customer_id'].unique()
        
        features[f'is_country_{risk_type}'] = features['customer_id'].isin(customers_with_risk).astype(int)
    
    # 4. Geographic Dispersion Metrics
    print("  Calculating geographic dispersion metrics...")
    
    # Transactions per unique location (lower = more concentrated, higher = more dispersed)
    total_txn_counts = transactions_geo.groupby('customer_id').size()
    
    # Count unique location combinations per customer
    unique_locations = transactions_geo.groupby('customer_id')[['country', 'province', 'city']].apply(
        lambda x: len(x.drop_duplicates())
    )
    
    total_txn_mapped = features['customer_id'].map(total_txn_counts).fillna(0)
    unique_locations_mapped = features['customer_id'].map(unique_locations).fillna(0)
    
    features['txn_per_unique_location'] = np.where(
        unique_locations_mapped > 0,
        total_txn_mapped / unique_locations_mapped,
        0
    )
    features['txn_per_unique_location'] = features['txn_per_unique_location'].fillna(0)
    
    # High dispersion flag (many unique locations relative to transaction count)
    features['high_geographic_dispersion'] = (
        (features['txn_per_unique_location'] < 5) & 
        (features['txn_per_unique_location'] > 0) &
        (features['country_diversity'] > 1)
    ).astype(int)
    
    # 5. Customer Location Risk (based on customer's home country)
    print("  Calculating customer location risk...")
    
    # Check if customer's home country is high-risk
    customer_country_risk = {}
    for risk_type, countries in COUNTRY_RISK_INDICATORS.items():
        customer_country_risk[risk_type] = customers['country'].isin(countries).astype(int)
    
    # Add customer location risk flags
    for risk_type in COUNTRY_RISK_INDICATORS.keys():
        features[f'customer_country_{risk_type}'] = features['customer_id'].map(
            pd.Series(customer_country_risk[risk_type].values, index=customers['customer_id'])
        ).fillna(0).astype(int)
    
    # Fill NaN values
    features = features.fillna(0)
    
    # Ensure integer columns are integers
    int_columns = [col for col in features.columns if col != 'customer_id' and (
        'diversity' in col.lower() or 
        'flag' in col.lower() or 
        'count' in col.lower() or
        'is_country' in col.lower() or
        'customer_country' in col.lower()
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
    print(f"  Country diversity: {features['country_diversity'].min()} to {features['country_diversity'].max()}")
    print(f"  Province diversity: {features['province_diversity'].min()} to {features['province_diversity'].max()}")
    print(f"  City diversity: {features['city_diversity'].min()} to {features['city_diversity'].max()}")
    print(f"  Cross-border customers: {features['cross_border_flag'].sum():,}")
    print(f"  High geographic dispersion: {features['high_geographic_dispersion'].sum():,}")
    
    # Country risk indicators summary
    risk_indicators = [col for col in features.columns if col.startswith('is_country_')]
    print(f"\n  Country risk indicators:")
    for col in risk_indicators:
        count = features[col].sum()
        print(f"    {col}: {count:,} customers")
    
    print("  Validation complete")

def main():
    """Main execution"""
    print("=" * 60)
    print("Phase 2.4: Geographic Features")
    print("=" * 60)
    
    # Load data
    transactions, customers = load_data()
    
    # Engineer features
    features = engineer_geographic_features(transactions, customers)
    
    # Validate
    validate_features(features)
    
    # Save output
    print("\nSaving features...")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / 'geographic_features.csv'
    features.to_csv(output_path, index=False)
    
    print(f"\nSaved: {output_path}")
    print(f"Features created: {len(features.columns) - 1}")  # -1 for customer_id
    print(f"Customers: {len(features):,}")
    print(f"\nFeature columns: {list(features.columns)}")
    
    # Generate report
    print("\nGenerating validation report...")
    generate_feature_report(features, 'geographic_features', REPORT_DIR)
    
    print("\n" + "=" * 60)
    print("Phase 2.4 Complete!")
    print("=" * 60)

if __name__ == '__main__':
    main()
