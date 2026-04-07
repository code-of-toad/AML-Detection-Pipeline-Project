"""
Feature Engineering Script: Phase 2.2 - Amount Features
Purpose: Engineer transaction amount-based features for AML detection model
Input: features/intermediate/transactions_combined.csv, features/intermediate/customer_base.csv
Output: features/by_category/amount_features.csv

Features Created:
- amount_mean, amount_stddev, amount_max, amount_min, amount_median
- round_amount_pct: Percentage of transactions with round amounts
- round_amount_flag: Boolean flag for round number transactions
- just_below_threshold_count: Count of transactions $9,000-$10,000 (structuring)
- large_txn_count_10k: Count of transactions > $10K
- large_txn_count_50k: Count of transactions > $50K
- large_txn_count_100k: Count of transactions > $100K
- amount_max_ratio_mean: Max transaction / Mean transaction (outlier detection)
- amount_stddev_ratio_mean: Coefficient of variation
- amount_cv_by_channel: Coefficient of variation by channel
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
    print(f"  Loaded {len(transactions):,} transactions")
    print(f"  Loaded {len(customers):,} customers")
    return transactions, customers

def is_round_number(amount, round_to=100):
    """Check if amount is a round number (divisible by round_to)"""
    return (amount % round_to == 0) & (amount > 0)

def engineer_amount_features(transactions, customers):
    """Engineer amount-based features for each customer"""
    print("\nEngineering amount features...")
    
    # Initialize features dataframe
    features = pd.DataFrame()
    features['customer_id'] = customers['customer_id']
    
    # Filter out null amounts
    transactions_clean = transactions[transactions['amount_cad'].notna()].copy()
    
    # 1. Basic Amount Statistics
    print("  Calculating basic amount statistics...")
    amount_stats = transactions_clean.groupby('customer_id')['amount_cad'].agg([
        'mean', 'std', 'min', 'max', 'median'
    ]).fillna(0)
    
    features['amount_mean'] = features['customer_id'].map(amount_stats['mean']).fillna(0)
    features['amount_stddev'] = features['customer_id'].map(amount_stats['std']).fillna(0)
    features['amount_min'] = features['customer_id'].map(amount_stats['min']).fillna(0)
    features['amount_max'] = features['customer_id'].map(amount_stats['max']).fillna(0)
    features['amount_median'] = features['customer_id'].map(amount_stats['median']).fillna(0)
    
    # 2. Round Number Features
    print("  Calculating round number features...")
    # Check for round numbers in cents: $100=10,000 cents, $1,000=100,000 cents, $10,000=1,000,000 cents
    transactions_clean['is_round_100'] = is_round_number(transactions_clean['amount_cad'], 10000)
    transactions_clean['is_round_1000'] = is_round_number(transactions_clean['amount_cad'], 100000)
    transactions_clean['is_round_10000'] = is_round_number(transactions_clean['amount_cad'], 1000000)
    transactions_clean['is_round_any'] = (
        transactions_clean['is_round_100'] | 
        transactions_clean['is_round_1000'] | 
        transactions_clean['is_round_10000']
    )
    
    # Count round number transactions per customer
    round_counts = transactions_clean.groupby('customer_id')['is_round_any'].sum()
    txn_counts = transactions_clean.groupby('customer_id').size()
    
    features['round_amount_count'] = features['customer_id'].map(round_counts).fillna(0).astype(int)
    features['round_amount_pct'] = (
        features['customer_id'].map(round_counts) / 
        features['customer_id'].map(txn_counts)
    ).fillna(0)
    
    # Round amount flag (if >50% of transactions are round numbers)
    features['round_amount_flag'] = (features['round_amount_pct'] > 0.5).astype(int)
    
    # 3. Structuring Indicators (Just Below Threshold)
    print("  Calculating structuring indicators...")
    # Transactions just below $10,000 CAD threshold (structuring) - in cents: $9,000-$10,000 = 900,000-1,000,000 cents
    structuring_range = transactions_clean[
        (transactions_clean['amount_cad'] >= 900000) & 
        (transactions_clean['amount_cad'] < 1000000)
    ]
    structuring_counts = structuring_range.groupby('customer_id').size()
    features['just_below_threshold_count'] = features['customer_id'].map(structuring_counts).fillna(0).astype(int)
    
    # Structuring pattern flag (multiple just-below-threshold transactions)
    features['structuring_pattern_flag'] = (features['just_below_threshold_count'] >= 3).astype(int)
    
    # 4. Large Transaction Counts
    print("  Calculating large transaction counts...")
    # Thresholds in cents: $10K=1M, $50K=5M, $100K=10M cents
    large_10k = transactions_clean[transactions_clean['amount_cad'] > 1000000]
    large_50k = transactions_clean[transactions_clean['amount_cad'] > 5000000]
    large_100k = transactions_clean[transactions_clean['amount_cad'] > 10000000]
    
    features['large_txn_count_10k'] = features['customer_id'].map(
        large_10k.groupby('customer_id').size()
    ).fillna(0).astype(int)
    
    features['large_txn_count_50k'] = features['customer_id'].map(
        large_50k.groupby('customer_id').size()
    ).fillna(0).astype(int)
    
    features['large_txn_count_100k'] = features['customer_id'].map(
        large_100k.groupby('customer_id').size()
    ).fillna(0).astype(int)
    
    # 5. Amount Ratio Features (Outlier Detection)
    print("  Calculating amount ratio features...")
    # Max to mean ratio (detects outliers)
    features['amount_max_ratio_mean'] = np.where(
        features['amount_mean'] > 0,
        features['amount_max'] / features['amount_mean'],
        0
    )
    # Cap at reasonable maximum (100x) to avoid extreme outliers
    features['amount_max_ratio_mean'] = features['amount_max_ratio_mean'].clip(upper=100)
    
    # Coefficient of variation (stddev / mean)
    features['amount_stddev_ratio_mean'] = np.where(
        features['amount_mean'] > 0,
        features['amount_stddev'] / features['amount_mean'],
        0
    )
    # Cap at reasonable maximum (10x)
    features['amount_stddev_ratio_mean'] = features['amount_stddev_ratio_mean'].clip(upper=10)
    
    # 6. Amount Statistics by Channel
    print("  Calculating amount statistics by channel...")
    # Calculate CV by channel using vectorized operations
    channel_stats = transactions_clean.groupby(['customer_id', 'transaction_channel'])['amount_cad'].agg(['mean', 'std']).reset_index()
    channel_stats['cv'] = np.where(
        channel_stats['mean'] > 0,
        channel_stats['std'] / channel_stats['mean'],
        0
    )
    # Average CV across channels per customer
    avg_cv_by_customer = channel_stats.groupby('customer_id')['cv'].mean()
    features['amount_cv_by_channel'] = features['customer_id'].map(avg_cv_by_customer).fillna(0)
    features['amount_cv_by_channel'] = features['amount_cv_by_channel'].clip(upper=10)
    
    # 7. Amount Modulo Features (for detecting specific increments)
    print("  Calculating amount modulo features...")
    # Amount modulo $50,000 (detects $50K increments - common in structuring) - in cents: $50K = 5,000,000 cents
    transactions_clean['amount_modulo_50000'] = transactions_clean['amount_cad'] % 5000000
    # Count transactions that are close to $50K increments (within $100 = 10,000 cents)
    transactions_clean['near_50k_increment'] = (
        (transactions_clean['amount_modulo_50000'] < 10000) | 
        (transactions_clean['amount_modulo_50000'] > 4990000)
    )
    
    near_50k_counts = transactions_clean.groupby('customer_id')['near_50k_increment'].sum()
    features['amount_near_50k_increment_count'] = features['customer_id'].map(near_50k_counts).fillna(0).astype(int)
    
    # Fill NaN values
    features = features.fillna(0)
    
    # Ensure integer columns are integers
    int_columns = ['round_amount_count', 'round_amount_flag', 'just_below_threshold_count',
                   'structuring_pattern_flag', 'large_txn_count_10k', 'large_txn_count_50k',
                   'large_txn_count_100k', 'amount_near_50k_increment_count']
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
    print(f"  Amount mean range: ${features['amount_mean'].min():.2f} to ${features['amount_mean'].max():.2f}")
    print(f"  Round amount percentage: {features['round_amount_pct'].min():.2%} to {features['round_amount_pct'].max():.2%}")
    print(f"  Just below threshold transactions: {features['just_below_threshold_count'].sum():,}")
    print(f"  Structuring pattern flags: {features['structuring_pattern_flag'].sum():,}")
    print(f"  Large transactions (>$10K): {features['large_txn_count_10k'].sum():,}")
    
    print("  Validation complete")

def main():
    """Main execution"""
    print("=" * 60)
    print("Phase 2.2: Amount Features")
    print("=" * 60)
    
    # Load data
    transactions, customers = load_data()
    
    # Engineer features
    features = engineer_amount_features(transactions, customers)
    
    # Validate
    validate_features(features)
    
    # Save output
    print("\nSaving features...")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / 'amount_features.csv'
    features.to_csv(output_path, index=False)
    
    print(f"\nSaved: {output_path}")
    print(f"Features created: {len(features.columns) - 1}")  # -1 for customer_id
    print(f"Customers: {len(features):,}")
    print(f"\nFeature columns: {list(features.columns)}")
    
    # Generate report
    print("\nGenerating validation report...")
    generate_feature_report(features, 'amount_features', REPORT_DIR)
    
    print("\n" + "=" * 60)
    print("Phase 2.2 Complete!")
    print("=" * 60)

if __name__ == '__main__':
    main()
