"""
Feature Engineering Script: Phase 2.5 - Time Features
Purpose: Engineer time-based pattern features for AML detection model
Input: features/intermediate/transactions_combined.csv, features/intermediate/customer_base.csv
Output: features/by_category/time_features.csv

Features Created:
- Transaction hour patterns (mode, after-hours percentage)
- Weekend/weekday patterns
- Midnight/early morning transactions
- Time between transactions
- Unusual time pattern flags
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

def load_data():
    """Load intermediate data files"""
    print("Loading data...")
    transactions = pd.read_csv(INPUT_DIR / 'transactions_combined.csv', low_memory=False)
    customers = pd.read_csv(INPUT_DIR / 'customer_base.csv')
    
    # Parse transaction datetime
    transactions['transaction_datetime'] = pd.to_datetime(transactions['transaction_datetime'], errors='coerce')
    transactions = transactions[transactions['transaction_datetime'].notna()].copy()
    
    print(f"  Loaded {len(transactions):,} transactions with valid timestamps")
    print(f"  Loaded {len(customers):,} customers")
    return transactions, customers

def engineer_time_features(transactions, customers):
    """Engineer time-based features for each customer"""
    print("\nEngineering time features...")
    
    # Initialize features dataframe
    features = pd.DataFrame()
    features['customer_id'] = customers['customer_id']
    
    # Sort transactions by customer and datetime for time difference calculations
    transactions_sorted = transactions.sort_values(['customer_id', 'transaction_datetime']).copy()
    
    # Extract time components
    transactions_sorted['hour'] = transactions_sorted['transaction_datetime'].dt.hour
    transactions_sorted['day_of_week'] = transactions_sorted['transaction_datetime'].dt.dayofweek  # 0=Monday, 6=Sunday
    transactions_sorted['is_weekend'] = transactions_sorted['day_of_week'].isin([5, 6]).astype(int)
    transactions_sorted['is_after_hours'] = (
        (transactions_sorted['hour'] < 9) | (transactions_sorted['hour'] >= 17)
    ).astype(int)
    transactions_sorted['is_midnight'] = (
        (transactions_sorted['hour'] >= 0) & (transactions_sorted['hour'] < 6)
    ).astype(int)
    transactions_sorted['is_early_morning'] = (
        (transactions_sorted['hour'] >= 6) & (transactions_sorted['hour'] < 9)
    ).astype(int)
    transactions_sorted['is_late_night'] = (
        (transactions_sorted['hour'] >= 22) | (transactions_sorted['hour'] < 2)
    ).astype(int)
    
    # 1. Transaction Hour Patterns
    print("  Calculating transaction hour patterns...")
    
    # Most common transaction hour (mode)
    hour_mode = transactions_sorted.groupby('customer_id')['hour'].agg(lambda x: x.mode().iloc[0] if len(x.mode()) > 0 else -1)
    features['txn_hour_mode'] = features['customer_id'].map(hour_mode).fillna(-1).astype(int)
    
    # After-hours transaction percentage (outside 9 AM - 5 PM)
    after_hours_counts = transactions_sorted.groupby('customer_id')['is_after_hours'].sum()
    total_txn_counts = transactions_sorted.groupby('customer_id').size()
    features['after_hours_txn_pct'] = (
        features['customer_id'].map(after_hours_counts) / 
        features['customer_id'].map(total_txn_counts)
    ).fillna(0)
    
    # After-hours flag (if >50% of transactions are after hours)
    features['after_hours_flag'] = (features['after_hours_txn_pct'] > 0.5).astype(int)
    
    # 2. Weekend/Weekday Patterns
    print("  Calculating weekend/weekday patterns...")
    
    weekend_counts = transactions_sorted.groupby('customer_id')['is_weekend'].sum()
    features['weekend_txn_count'] = features['customer_id'].map(weekend_counts).fillna(0).astype(int)
    features['weekend_txn_pct'] = (
        features['weekend_txn_count'] / 
        features['customer_id'].map(total_txn_counts)
    ).fillna(0)
    
    # Weekend-heavy flag (if >30% of transactions are on weekends)
    features['weekend_heavy_flag'] = (features['weekend_txn_pct'] > 0.3).astype(int)
    
    # 3. Midnight/Early Morning Transactions
    print("  Calculating midnight/early morning patterns...")
    
    midnight_counts = transactions_sorted.groupby('customer_id')['is_midnight'].sum()
    early_morning_counts = transactions_sorted.groupby('customer_id')['is_early_morning'].sum()
    late_night_counts = transactions_sorted.groupby('customer_id')['is_late_night'].sum()
    
    features['midnight_txn_count'] = features['customer_id'].map(midnight_counts).fillna(0).astype(int)
    features['early_morning_txn_count'] = features['customer_id'].map(early_morning_counts).fillna(0).astype(int)
    features['late_night_txn_count'] = features['customer_id'].map(late_night_counts).fillna(0).astype(int)
    
    # Midnight transaction percentage
    features['midnight_txn_pct'] = (
        features['midnight_txn_count'] / 
        features['customer_id'].map(total_txn_counts)
    ).fillna(0)
    
    # Unusual hours flag (midnight or early morning transactions)
    features['unusual_hours_flag'] = (
        (features['midnight_txn_count'] > 0) | 
        (features['early_morning_txn_count'] > 5)
    ).astype(int)
    
    # 4. Time Between Transactions
    print("  Calculating time between transactions...")
    
    # Calculate time differences between consecutive transactions per customer
    transactions_sorted['time_diff'] = transactions_sorted.groupby('customer_id')['transaction_datetime'].diff()
    transactions_sorted['time_diff_hours'] = transactions_sorted['time_diff'].dt.total_seconds() / 3600
    
    # Filter out negative or zero differences (shouldn't happen, but safety check)
    time_diffs = transactions_sorted[
        transactions_sorted['time_diff_hours'].notna() & 
        (transactions_sorted['time_diff_hours'] > 0)
    ]
    
    if len(time_diffs) > 0:
        time_diff_stats = time_diffs.groupby('customer_id')['time_diff_hours'].agg([
            'mean', 'median', 'min', 'max', 'std'
        ])
        
        features['time_between_txn_mean'] = features['customer_id'].map(time_diff_stats['mean']).fillna(0)
        features['time_between_txn_median'] = features['customer_id'].map(time_diff_stats['median']).fillna(0)
        features['time_between_txn_min'] = features['customer_id'].map(time_diff_stats['min']).fillna(0)
        features['time_between_txn_max'] = features['customer_id'].map(time_diff_stats['max']).fillna(0)
        features['time_between_txn_std'] = features['customer_id'].map(time_diff_stats['std']).fillna(0)
        
        # Very short time between transactions (potential rapid-fire pattern)
        very_short = time_diffs[time_diffs['time_diff_hours'] < 0.1]  # Less than 6 minutes
        very_short_counts = very_short.groupby('customer_id').size()
        features['very_short_time_between_txn'] = features['customer_id'].map(very_short_counts).fillna(0).astype(int)
        
        # Rapid-fire flag (multiple transactions within 1 hour)
        rapid_fire = time_diffs[time_diffs['time_diff_hours'] < 1.0]
        rapid_fire_counts = rapid_fire.groupby('customer_id').size()
        features['rapid_fire_txn_count'] = features['customer_id'].map(rapid_fire_counts).fillna(0).astype(int)
        features['rapid_fire_flag'] = (features['rapid_fire_txn_count'] >= 10).astype(int)
    else:
        features['time_between_txn_mean'] = 0
        features['time_between_txn_median'] = 0
        features['time_between_txn_min'] = 0
        features['time_between_txn_max'] = 0
        features['time_between_txn_std'] = 0
        features['very_short_time_between_txn'] = 0
        features['rapid_fire_txn_count'] = 0
        features['rapid_fire_flag'] = 0
    
    # 5. Time Pattern Consistency
    print("  Calculating time pattern consistency...")
    
    # Hour standard deviation (lower = more consistent timing, higher = more varied)
    hour_std = transactions_sorted.groupby('customer_id')['hour'].std()
    features['txn_hour_std'] = features['customer_id'].map(hour_std).fillna(0)
    
    # Consistent timing flag (low hour std, indicating transactions at similar times)
    features['consistent_timing_flag'] = (
        (features['txn_hour_std'] < 3) & 
        (features['txn_hour_std'] > 0) &
        (features['customer_id'].map(total_txn_counts) >= 10)
    ).astype(int)
    
    # 6. Business Hours vs Non-Business Hours
    print("  Calculating business hours patterns...")
    
    # Business hours: 9 AM - 5 PM, Monday-Friday
    transactions_sorted['is_business_hours'] = (
        (transactions_sorted['hour'] >= 9) & 
        (transactions_sorted['hour'] < 17) &
        (transactions_sorted['day_of_week'] < 5)
    ).astype(int)
    
    business_hours_counts = transactions_sorted.groupby('customer_id')['is_business_hours'].sum()
    features['business_hours_txn_pct'] = (
        features['customer_id'].map(business_hours_counts) / 
        features['customer_id'].map(total_txn_counts)
    ).fillna(0)
    
    # Non-business hours heavy flag (if <20% of transactions during business hours)
    features['non_business_hours_heavy'] = (features['business_hours_txn_pct'] < 0.2).astype(int)
    
    # 7. Monthly/Seasonal Patterns (if data spans multiple months)
    print("  Calculating monthly patterns...")
    
    transactions_sorted['month'] = transactions_sorted['transaction_datetime'].dt.month
    month_counts = transactions_sorted.groupby('customer_id')['month'].nunique()
    features['months_active'] = features['customer_id'].map(month_counts).fillna(0).astype(int)
    
    # Transactions per month (if customer has transactions across multiple months)
    features['txn_per_month'] = np.where(
        features['months_active'] > 0,
        features['customer_id'].map(total_txn_counts) / features['months_active'],
        0
    )
    features['txn_per_month'] = features['txn_per_month'].fillna(0)
    
    # Fill NaN values
    features = features.fillna(0)
    
    # Ensure integer columns are integers
    int_columns = [col for col in features.columns if col != 'customer_id' and (
        'count' in col.lower() or 
        'flag' in col.lower() or 
        'mode' in col.lower() or
        'months_active' in col.lower()
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
    print(f"  Transaction hour mode range: {features['txn_hour_mode'].min()} to {features['txn_hour_mode'].max()}")
    print(f"  After-hours transaction percentage: {features['after_hours_txn_pct'].min():.2%} to {features['after_hours_txn_pct'].max():.2%}")
    print(f"  Weekend transaction percentage: {features['weekend_txn_pct'].min():.2%} to {features['weekend_txn_pct'].max():.2%}")
    print(f"  Midnight transactions: {features['midnight_txn_count'].sum():,}")
    print(f"  After-hours flag: {features['after_hours_flag'].sum():,} customers")
    print(f"  Weekend-heavy flag: {features['weekend_heavy_flag'].sum():,} customers")
    print(f"  Unusual hours flag: {features['unusual_hours_flag'].sum():,} customers")
    print(f"  Rapid-fire flag: {features['rapid_fire_flag'].sum():,} customers")
    
    print("  Validation complete")

def main():
    """Main execution"""
    print("=" * 60)
    print("Phase 2.5: Time Features")
    print("=" * 60)
    
    # Load data
    transactions, customers = load_data()
    
    # Engineer features
    features = engineer_time_features(transactions, customers)
    
    # Validate
    validate_features(features)
    
    # Save output
    print("\nSaving features...")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / 'time_features.csv'
    features.to_csv(output_path, index=False)
    
    print(f"\nSaved: {output_path}")
    print(f"Features created: {len(features.columns) - 1}")  # -1 for customer_id
    print(f"Customers: {len(features):,}")
    print(f"\nFeature columns: {list(features.columns)}")
    
    # Generate report
    print("\nGenerating validation report...")
    generate_feature_report(features, 'time_features', REPORT_DIR)
    
    print("\n" + "=" * 60)
    print("Phase 2.5 Complete!")
    print("=" * 60)

if __name__ == '__main__':
    main()
