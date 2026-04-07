"""
Feature Engineering Script: Phase 3 - Feature Combination
Purpose: Combine all feature files into a single master features table
Input: features/by_category/*.csv, features/intermediate/customer_base.csv
Output: features/final/master_features.csv

This script merges all feature categories into one comprehensive feature table
for machine learning model training (Task 2).
"""

import pandas as pd
import numpy as np
from pathlib import Path
from report_utils import generate_feature_report

# Configuration
BASE_DIR = Path(__file__).parent.parent
INPUT_DIR = BASE_DIR / 'features' / 'by_category'
INTERMEDIATE_DIR = BASE_DIR / 'features' / 'intermediate'
OUTPUT_DIR = BASE_DIR / 'features' / 'final'
REPORT_DIR = BASE_DIR / 'features' / 'reports'

# Feature files to combine (in order): Stream A + Stream B
FEATURE_FILES = [
    'velocity_features.csv',
    'amount_features.csv',
    'channel_features.csv',
    'geographic_features.csv',
    'time_features.csv',
    'behavioral_features.csv',
    'profile_features.csv',
    'transaction_derived_features.csv',  # Stream B: txn-level scores aggregated by customer
]

def load_customer_base():
    """Load customer base with KYC data and labels"""
    print("Loading customer base...")
    customers = pd.read_csv(INTERMEDIATE_DIR / 'customer_base.csv')
    print(f"  Loaded {len(customers):,} customers")
    return customers

def load_feature_files():
    """Load all feature category files"""
    print("\nLoading feature files...")
    features_dict = {}
    
    for feature_file in FEATURE_FILES:
        file_path = INPUT_DIR / feature_file
        if file_path.exists():
            print(f"  Loading {feature_file}...")
            df = pd.read_csv(file_path)
            category_name = feature_file.replace('_features.csv', '')
            features_dict[category_name] = df
            print(f"    {len(df):,} customers, {len(df.columns) - 1} features")  # -1 for customer_id
        else:
            print(f"  Warning: {feature_file} not found, skipping...")
    
    return features_dict

def combine_features(customers, features_dict):
    """Combine all features into master features table"""
    print("\nCombining features...")
    
    # Start with customer base (includes customer_id, kyc_type, and potentially label)
    master_features = customers[['customer_id']].copy()
    
    # Add KYC type and label if available
    if 'kyc_type' in customers.columns:
        master_features['kyc_type'] = customers['kyc_type']
    if 'label' in customers.columns:
        master_features['label'] = customers['label']
    
    # Merge each feature category
    for category_name, feature_df in features_dict.items():
        print(f"  Merging {category_name} features...")
        
        # Ensure customer_id is the key
        if 'customer_id' not in feature_df.columns:
            print(f"    Warning: {category_name} missing customer_id, skipping...")
            continue
        
        # Merge on customer_id
        before_count = len(master_features)
        master_features = master_features.merge(
            feature_df,
            on='customer_id',
            how='outer',
            suffixes=('', f'_{category_name}')
        )
        after_count = len(master_features)
        
        if after_count != before_count:
            print(f"    Warning: Row count changed from {before_count} to {after_count}")
    
    # Ensure all customers are present
    print(f"\n  Total customers in master features: {len(master_features):,}")
    print(f"  Total features: {len(master_features.columns) - 1}")  # -1 for customer_id
    
    return master_features

def validate_combined_features(master_features):
    """Validate the combined features"""
    print("\nValidating combined features...")
    
    # Check for duplicate customer_ids
    duplicate_count = master_features['customer_id'].duplicated().sum()
    if duplicate_count > 0:
        print(f"  Warning: Found {duplicate_count} duplicate customer_ids")
    else:
        print("  No duplicate customer_ids")
    
    # Check for null values
    null_counts = master_features.isnull().sum()
    null_cols = null_counts[null_counts > 0]
    if len(null_cols) > 0:
        print(f"  Warning: Found null values in {len(null_cols)} columns")
        print(f"    Top 10 columns with nulls: {null_cols.head(10).to_dict()}")
    else:
        print("  No null values")
    
    # Check feature counts by category
    print("\n  Feature counts by category:")
    for feature_file in FEATURE_FILES:
        category_name = feature_file.replace('_features.csv', '')
        category_cols = [col for col in master_features.columns if category_name in col.lower() or col.startswith(category_name)]
        if category_cols:
            print(f"    {category_name}: {len(category_cols)} features")
    
    # Summary statistics
    print(f"\n  Total columns: {len(master_features.columns)}")
    print(f"  Total rows: {len(master_features):,}")
    
    # Check for label column if available
    if 'label' in master_features.columns:
        label_counts = master_features['label'].value_counts()
        print(f"\n  Label distribution:")
        for label, count in label_counts.items():
            print(f"    {label}: {count:,} ({count/len(master_features)*100:.1f}%)")
    
    print("  Validation complete")

def main():
    """Main execution"""
    print("=" * 60)
    print("Phase 3: Feature Combination")
    print("=" * 60)
    
    # Load customer base
    customers = load_customer_base()
    
    # Load all feature files
    features_dict = load_feature_files()
    
    if not features_dict:
        print("\nError: No feature files found. Please run feature engineering scripts first.")
        return
    
    # Combine features
    master_features = combine_features(customers, features_dict)
    
    # Validate
    validate_combined_features(master_features)
    
    # Save output
    print("\nSaving master features...")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / 'master_features.csv'
    master_features.to_csv(output_path, index=False)
    
    print(f"\nSaved: {output_path}")
    print(f"   Features: {len(master_features.columns) - 1}")  # -1 for customer_id
    print(f"   Customers: {len(master_features):,}")
    
    # Generate summary report
    print("\nGenerating summary report...")
    generate_feature_report(master_features, 'master_features', REPORT_DIR)
    
    print("\n" + "=" * 60)
    print("Phase 3 Complete!")
    print("=" * 60)
    print(f"\nMaster features table ready for Task 2 (Detection Model)")
    print(f"   File: {output_path}")

if __name__ == '__main__':
    main()
