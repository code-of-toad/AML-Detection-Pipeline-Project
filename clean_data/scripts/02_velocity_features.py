"""
Feature Engineering Script: Phase 2.1 - Velocity Features
Purpose: Engineer transaction velocity features for AML detection model
Input: features/intermediate/transactions_combined.csv, features/intermediate/customer_base.csv
Output: features/by_category/velocity_features.csv

Features Created:
- txn_count_total: Total number of transactions
- txn_per_day_avg: Average transactions per day
- txn_velocity: Transactions per day (overall)
- sudden_inflow_outflow_pattern: Boolean flag for sudden inflow followed by outflows
- flow_through_velocity: Average time between deposit and withdrawal
- time_between_deposit_withdrawal: Hours between credit and debit transactions
- account_turnover_rate: Volume out / Volume in ratio
- volume_eft_sudden_increase: Change in EFT volume over time window
- txn_count_eft_spike: Sudden increase in EFT transaction count
- velocity_change_eft: Rate of change in EFT velocity
- high_frequency_customer_flag: Boolean flag for >500 transactions
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import timedelta
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
    # Ensure datetime column is properly parsed
    transactions['transaction_datetime'] = pd.to_datetime(transactions['transaction_datetime'], errors='coerce')
    customers = pd.read_csv(INPUT_DIR / 'customer_base.csv')
    print(f"  Loaded {len(transactions):,} transactions")
    print(f"  Loaded {len(customers):,} customers")
    return transactions, customers

def engineer_velocity_features(transactions, customers):
    """Engineer velocity features for each customer"""
    print("\nEngineering velocity features...")
    
    # Initialize features dataframe
    features = pd.DataFrame()
    features['customer_id'] = customers['customer_id']
    
    # Sort transactions by customer and datetime for time-based calculations
    print("  Sorting transactions...")
    transactions = transactions.sort_values(['customer_id', 'transaction_datetime']).copy()
    
    # 1. Basic Transaction Count Features
    print("  Calculating basic transaction counts...")
    txn_counts = transactions.groupby('customer_id').size()
    features['txn_count_total'] = features['customer_id'].map(txn_counts).fillna(0).astype(int)
    
    # 2. Transaction Velocity (transactions per day)
    print("  Calculating transaction velocity...")
    # Calculate date range for each customer
    customer_date_ranges = transactions.groupby('customer_id')['transaction_datetime'].agg(['min', 'max'])
    customer_date_ranges['date_range_days'] = (
        (customer_date_ranges['max'] - customer_date_ranges['min']).dt.total_seconds() / 86400
    )
    # Add 1 to avoid division by zero (at least 1 day)
    customer_date_ranges['date_range_days'] = customer_date_ranges['date_range_days'] + 1
    
    # Map to features
    features['txn_per_day_avg'] = (
        features['customer_id'].map(txn_counts) / 
        features['customer_id'].map(customer_date_ranges['date_range_days'])
    ).fillna(0)
    
    # Overall velocity (same as per day avg for now)
    features['txn_velocity'] = features['txn_per_day_avg']
    
    # 3. High Frequency Customer Flag
    print("  Identifying high frequency customers...")
    features['high_frequency_customer_flag'] = (features['txn_count_total'] > 500).astype(int)
    
    # 4. Debit/Credit Volume Calculations (for flow-through and turnover)
    print("  Calculating debit/credit volumes...")
    debit_volumes = transactions[transactions['debit_credit'] == 'D'].groupby('customer_id')['amount_cad'].sum()
    credit_volumes = transactions[transactions['debit_credit'] == 'C'].groupby('customer_id')['amount_cad'].sum()
    
    features['volume_debit_total'] = features['customer_id'].map(debit_volumes).fillna(0)
    features['volume_credit_total'] = features['customer_id'].map(credit_volumes).fillna(0)
    
    # 5. Account Turnover Rate (Volume out / Volume in)
    print("  Calculating account turnover rate...")
    # Avoid division by zero
    features['account_turnover_rate'] = np.where(
        features['volume_credit_total'] > 0,
        features['volume_debit_total'] / features['volume_credit_total'],
        np.where(features['volume_debit_total'] > 0, 10.0, 0)  # Cap at 10 for infinite cases
    )
    # Cap at reasonable maximum (10x) to avoid extreme outliers
    features['account_turnover_rate'] = features['account_turnover_rate'].clip(upper=10)
    
    # 6. Flow-Through Velocity (time between deposit and withdrawal)
    print("  Calculating flow-through velocity...")
    # Use vectorized approach: shift to find credit->debit pairs
    transactions_sorted = transactions.sort_values(['customer_id', 'transaction_datetime']).copy()
    transactions_sorted['next_debit_credit'] = transactions_sorted.groupby('customer_id')['debit_credit'].shift(-1)
    transactions_sorted['next_datetime'] = transactions_sorted.groupby('customer_id')['transaction_datetime'].shift(-1)
    
    # Filter for credit->debit pairs
    credit_debit_pairs = transactions_sorted[
        (transactions_sorted['debit_credit'] == 'C') & 
        (transactions_sorted['next_debit_credit'] == 'D')
    ].copy()
    
    if len(credit_debit_pairs) > 0:
        credit_debit_pairs['time_diff_hours'] = (
            (credit_debit_pairs['next_datetime'] - credit_debit_pairs['transaction_datetime']).dt.total_seconds() / 3600
        )
        flow_through_avg = credit_debit_pairs.groupby('customer_id')['time_diff_hours'].mean()
        features['flow_through_velocity_hours'] = features['customer_id'].map(flow_through_avg).fillna(0)
        features['time_between_deposit_withdrawal'] = features['flow_through_velocity_hours']
    else:
        features['flow_through_velocity_hours'] = 0
        features['time_between_deposit_withdrawal'] = 0
    
    # 7. Sudden Inflow/Outflow Pattern (simplified for performance)
    print("  Detecting sudden inflow/outflow patterns (simplified)...")
    # Simplified: Check if customer has large credits and high debit frequency
    customer_avg_credits = transactions[transactions['debit_credit'] == 'C'].groupby('customer_id')['amount_cad'].mean()
    customer_max_credits = transactions[transactions['debit_credit'] == 'C'].groupby('customer_id')['amount_cad'].max()
    customer_debit_counts = transactions[transactions['debit_credit'] == 'D'].groupby('customer_id').size()
    
    # Pattern: max credit > 2x avg credit AND high debit count (>10 debits)
    features['sudden_inflow_outflow_pattern'] = (
        (features['customer_id'].map(customer_max_credits) > 
         features['customer_id'].map(customer_avg_credits) * 2) &
        (features['customer_id'].map(customer_debit_counts) > 10)
    ).fillna(False).astype(int)
    
    # 8. EFT-Specific Velocity Features
    print("  Calculating EFT-specific velocity features...")
    eft_transactions = transactions[transactions['transaction_channel'] == 'EFT'].copy()
    
    if len(eft_transactions) > 0:
        # EFT transaction count
        eft_counts = eft_transactions.groupby('customer_id').size()
        features['txn_count_eft'] = features['customer_id'].map(eft_counts).fillna(0).astype(int)
        
        # EFT volume
        eft_volumes = eft_transactions.groupby('customer_id')['amount_cad'].sum()
        features['volume_eft_total'] = features['customer_id'].map(eft_volumes).fillna(0)
        
        # EFT velocity (if customer has EFT transactions)
        eft_customers = eft_transactions.groupby('customer_id')['transaction_datetime'].agg(['min', 'max'])
        eft_customers['eft_days'] = (
            (eft_customers['max'] - eft_customers['min']).dt.total_seconds() / 86400 + 1
        )
        features['txn_velocity_eft'] = (
            features['customer_id'].map(eft_counts) / 
            features['customer_id'].map(eft_customers['eft_days'])
        ).fillna(0)
        
        # EFT sudden increase (simplified: compare early vs late period volumes)
        print("    Calculating EFT sudden increase patterns (simplified)...")
        eft_sorted = eft_transactions.sort_values(['customer_id', 'transaction_datetime'])
        eft_sorted['period'] = eft_sorted.groupby('customer_id').cumcount()
        eft_sorted['total_txns'] = eft_sorted.groupby('customer_id')['period'].transform('max')
        eft_sorted['is_second_half'] = (eft_sorted['period'] > eft_sorted['total_txns'] / 2).astype(int)
        
        # Calculate volumes by period
        eft_volumes_by_period = eft_sorted.groupby(['customer_id', 'is_second_half'])['amount_cad'].sum().unstack(fill_value=0)
        if 0 in eft_volumes_by_period.columns and 1 in eft_volumes_by_period.columns:
            eft_volumes_by_period['sudden_increase'] = (
                (eft_volumes_by_period[1] > eft_volumes_by_period[0] * 2) & 
                (eft_volumes_by_period[0] > 0)
            ).astype(int)
            features['volume_eft_sudden_increase'] = features['customer_id'].map(eft_volumes_by_period['sudden_increase']).fillna(0).astype(int)
        else:
            features['volume_eft_sudden_increase'] = 0
        
        # EFT transaction count spike (simplified)
        eft_counts_by_period = eft_sorted.groupby(['customer_id', 'is_second_half']).size().unstack(fill_value=0)
        if 0 in eft_counts_by_period.columns and 1 in eft_counts_by_period.columns:
            eft_counts_by_period['spike'] = (
                (eft_counts_by_period[1] > eft_counts_by_period[0] * 2) & 
                (eft_counts_by_period[0] > 0)
            ).astype(int)
            features['txn_count_eft_spike'] = features['customer_id'].map(eft_counts_by_period['spike']).fillna(0).astype(int)
        else:
            features['txn_count_eft_spike'] = 0
        
        # EFT velocity change
        features['velocity_change_eft'] = features['txn_count_eft_spike']  # Use spike as proxy
    else:
        # No EFT transactions
        features['txn_count_eft'] = 0
        features['volume_eft_total'] = 0
        features['txn_velocity_eft'] = 0
        features['volume_eft_sudden_increase'] = 0
        features['txn_count_eft_spike'] = 0
        features['velocity_change_eft'] = 0
    
    # Fill NaN values
    features = features.fillna(0)
    
    # Ensure integer columns are integers
    int_columns = ['txn_count_total', 'high_frequency_customer_flag', 'txn_count_eft', 
                   'volume_eft_sudden_increase', 'txn_count_eft_spike', 'velocity_change_eft',
                   'sudden_inflow_outflow_pattern']
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
    
    # Check for negative values where not expected
    non_negative_cols = ['txn_count_total', 'txn_per_day_avg', 'txn_velocity', 
                         'volume_debit_total', 'volume_credit_total']
    for col in non_negative_cols:
        if col in features.columns:
            negative_count = (features[col] < 0).sum()
            if negative_count > 0:
                print(f"  Warning: {col} has {negative_count} negative values")
    
    # Check ranges
    print(f"  Transaction count range: {features['txn_count_total'].min()} to {features['txn_count_total'].max()}")
    print(f"  Transactions per day range: {features['txn_per_day_avg'].min():.2f} to {features['txn_per_day_avg'].max():.2f}")
    print(f"  High frequency customers: {features['high_frequency_customer_flag'].sum():,}")
    print(f"  Sudden inflow/outflow patterns: {features['sudden_inflow_outflow_pattern'].sum():,}")
    
    print("  Validation complete")

def main():
    """Main execution"""
    print("=" * 60)
    print("Phase 2.1: Velocity Features")
    print("=" * 60)
    
    # Load data
    transactions, customers = load_data()
    
    # Engineer features
    features = engineer_velocity_features(transactions, customers)
    
    # Validate
    validate_features(features)
    
    # Save output
    print("\nSaving features...")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / 'velocity_features.csv'
    features.to_csv(output_path, index=False)
    
    print(f"\nSaved: {output_path}")
    print(f"Features created: {len(features.columns) - 1}")  # -1 for customer_id
    print(f"Customers: {len(features):,}")
    print(f"\nFeature columns: {list(features.columns)}")
    
    # Generate report
    print("\nGenerating validation report...")
    generate_feature_report(features, 'velocity_features', REPORT_DIR)
    
    print("\n" + "=" * 60)
    print("Phase 2.1 Complete!")
    print("=" * 60)

if __name__ == '__main__':
    main()
