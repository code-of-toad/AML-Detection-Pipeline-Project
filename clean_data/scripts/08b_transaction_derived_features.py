"""
Feature Engineering Script: Stream B - Transaction-Derived Customer Summary
Purpose: Score each transaction (rules), aggregate by customer_id → max/mean/count/% of transaction-level scores.
Input: features/intermediate/transactions_combined.csv, features/intermediate/customer_base.csv
Output: features/by_category/transaction_derived_features.csv

Stream B feeds into 09_combine_features and is merged into master_features.csv (Stream A + Stream B).

Features Created (per customer):
- txn_score_max: Max transaction-level risk score (0-1)
- txn_score_mean: Mean transaction-level risk score
- txn_score_std: Std of transaction-level risk scores
- txn_score_count_above_threshold: Count of transactions with score >= threshold (default 0.5)
- txn_score_pct_above_threshold: Percentage of transactions with score >= threshold
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

# Threshold for "high-risk transaction" counts/percentages (0-1)
TXN_SCORE_THRESHOLD = 0.5

# Amount thresholds in cents ($10K = 1_000_000, $9K = 900_000, $50K = 5_000_000)
AMOUNT_10K_CENTS = 1_000_000
AMOUNT_9K_CENTS = 900_000
AMOUNT_50K_CENTS = 5_000_000


def load_data():
    """Load transactions and customer base"""
    print("Loading data...")
    transactions = pd.read_csv(INPUT_DIR / 'transactions_combined.csv', low_memory=False)
    customers = pd.read_csv(INPUT_DIR / 'customer_base.csv')
    print(f"  Loaded {len(transactions):,} transactions")
    print(f"  Loaded {len(customers):,} customers")
    return transactions, customers


def score_transactions(transactions):
    """
    Score each transaction with simple AML rules. Returns a risk score in [0, 1] per transaction.
    Higher = more suspicious.
    """
    print("\nScoring each transaction...")
    txn = transactions.copy()

    # Ensure amount_cad is numeric
    txn['amount_cad'] = pd.to_numeric(txn['amount_cad'], errors='coerce').fillna(0)

    score = np.zeros(len(txn), dtype=float)

    # Large transaction (>$10K) - weight 0.2
    score += (txn['amount_cad'] >= AMOUNT_10K_CENTS).astype(float) * 0.2

    # Structuring: just below $10K ($9K–$10K) - weight 0.25
    structuring = (txn['amount_cad'] >= AMOUNT_9K_CENTS) & (txn['amount_cad'] < AMOUNT_10K_CENTS)
    score += structuring.astype(float) * 0.25

    # Round amount (divisible by $100 = 10_000 cents) - weight 0.1
    round_100 = (txn['amount_cad'] > 0) & ((txn['amount_cad'] % 10_000) == 0)
    score += round_100.astype(float) * 0.1

    # Wire or Western Union channel - weight 0.25
    high_risk_channel = txn['transaction_channel'].isin(['WIRE', 'WESTERN_UNION'])
    score += high_risk_channel.astype(float) * 0.25

    # Cash indicator - weight 0.1
    cash = pd.to_numeric(txn.get('cash_indicator', 0), errors='coerce').fillna(0) == 1
    score += cash.astype(float) * 0.1

    # Very large (>$50K) - extra weight 0.15
    score += (txn['amount_cad'] >= AMOUNT_50K_CENTS).astype(float) * 0.15

    # Clip to [0, 1]
    score = np.clip(score, 0.0, 1.0)
    return score


def aggregate_by_customer(transactions, txn_scores, customers):
    """Aggregate transaction-level scores by customer_id. One row per customer in customer_base."""
    print("\nAggregating by customer...")
    txn = transactions.copy()
    txn['txn_score'] = txn_scores

    agg = txn.groupby('customer_id')['txn_score'].agg([
        ('txn_score_max', 'max'),
        ('txn_score_mean', 'mean'),
        ('txn_score_std', 'std'),
    ]).reset_index()

    txn_count = txn.groupby('customer_id').size().reset_index(name='txn_count')
    agg = agg.merge(txn_count, on='customer_id', how='left')

    above = (txn['txn_score'] >= TXN_SCORE_THRESHOLD).astype(int)
    txn['above_threshold'] = above
    count_above = txn.groupby('customer_id')['above_threshold'].sum().reset_index(
        name='txn_score_count_above_threshold'
    )
    agg = agg.merge(count_above, on='customer_id', how='left')

    agg['txn_score_pct_above_threshold'] = np.where(
        agg['txn_count'] > 0,
        agg['txn_score_count_above_threshold'] / agg['txn_count'],
        0.0
    )
    agg = agg.drop(columns=['txn_count'])

    # Ensure all customers from customer_base have a row
    features = customers[['customer_id']].merge(agg, on='customer_id', how='left')
    features['txn_score_max'] = features['txn_score_max'].fillna(0.0)
    features['txn_score_mean'] = features['txn_score_mean'].fillna(0.0)
    features['txn_score_std'] = features['txn_score_std'].fillna(0.0)
    features['txn_score_count_above_threshold'] = features['txn_score_count_above_threshold'].fillna(0).astype(int)
    features['txn_score_pct_above_threshold'] = features['txn_score_pct_above_threshold'].fillna(0.0)

    return features


def engineer_transaction_derived_features(transactions, customers):
    """Build Stream B features: score each txn, aggregate by customer."""
    txn_scores = score_transactions(transactions)
    features = aggregate_by_customer(transactions, txn_scores, customers)
    return features


def validate_features(features):
    """Validate Stream B features"""
    print("\nValidating features...")
    null_counts = features.isnull().sum()
    if null_counts.sum() > 0:
        print(f"  Warning: Nulls in {null_counts[null_counts > 0].to_dict()}")
    else:
        print("  No null values")
    print(f"  txn_score_max range: {features['txn_score_max'].min():.2f} to {features['txn_score_max'].max():.2f}")
    print(f"  txn_score_mean range: {features['txn_score_mean'].min():.2f} to {features['txn_score_mean'].max():.2f}")
    print(f"  Customers with >=1 txn above threshold: {(features['txn_score_count_above_threshold'] > 0).sum():,}")
    print("  Validation complete")


def main():
    """Main execution"""
    print("=" * 60)
    print("Stream B: Transaction-Derived Features")
    print("=" * 60)

    transactions, customers = load_data()
    features = engineer_transaction_derived_features(transactions, customers)
    validate_features(features)

    print("\nSaving features...")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / 'transaction_derived_features.csv'
    features.to_csv(output_path, index=False)

    print(f"\nSaved: {output_path}")
    print(f"Features created: {len(features.columns) - 1}")
    print(f"Customers: {len(features):,}")
    print(f"Feature columns: {list(features.columns)}")

    print("\nGenerating report...")
    generate_feature_report(features, 'transaction_derived_features', REPORT_DIR)

    print("\n" + "=" * 60)
    print("Stream B Complete!")
    print("=" * 60)
    print("Run 09_combine_features to merge Stream A + Stream B -> master_features.csv")


if __name__ == '__main__':
    main()
