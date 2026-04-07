"""
Feature Engineering Script: Phase 1 - Load and Combine Data
Purpose: Load all original CSV files, create base customer table, and combine all transaction files
Input: clean_original/*.csv
Output: features/intermediate/customer_base.csv, features/intermediate/transactions_combined.csv
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime

# Configuration
BASE_DIR = Path(__file__).parent.parent
ORIGINAL_DIR = BASE_DIR / 'clean_original'
OUTPUT_DIR = BASE_DIR / 'features' / 'intermediate'

def load_customer_data():
    """Load and prepare customer base table from master_customers.csv"""
    print("Loading customer data...")
    
    customers = pd.read_csv(ORIGINAL_DIR / 'master_customers.csv')
    
    print(f"  Loaded {len(customers):,} customers")
    print(f"  Columns: {list(customers.columns)}")
    
    # Convert date columns to datetime
    date_columns = ['onboard_date', 'birth_establish_date']
    for col in date_columns:
        if col in customers.columns:
            customers[col] = pd.to_datetime(customers[col], errors='coerce')
    
    # Keep income/sales in cents (no conversion)
    if 'income_cents' in customers.columns:
        customers['income_cad'] = customers['income_cents'].copy()
    
    if 'sales_cents' in customers.columns:
        customers['sales_cad'] = customers['sales_cents'].copy()
    
    return customers

def load_transaction_files():
    """Load all transaction files and combine into one dataframe"""
    print("\nLoading transaction files...")
    
    transaction_files = {
        'ABM': 'clean_txn_abm.csv',
        'CARD': 'clean_txn_card.csv',
        'CHEQUE': 'clean_txn_cheque.csv',
        'EFT': 'clean_txn_eft.csv',
        'EMT': 'clean_txn_emt.csv',
        'WESTERN_UNION': 'clean_txn_western_union.csv',
        'WIRE': 'clean_txn_wire.csv',
    }
    
    all_transactions = []
    
    for channel, filename in transaction_files.items():
        filepath = ORIGINAL_DIR / filename
        
        if not filepath.exists():
            print(f"  Warning: {filename} not found, skipping...")
            continue
        
        print(f"  Loading {channel} transactions from {filename}...")
        df = pd.read_csv(filepath)
        
        # Add channel identifier
        df['transaction_channel'] = channel
        
        # Standardize amount to cents (amount_cad) - keep in cents
        if 'amount_cad_cents' in df.columns:
            # Keep in cents (no conversion)
            df['amount_cad'] = df['amount_cad_cents'].copy()
            df = df.drop(columns=['amount_cad_cents'])
        elif 'amount_cad' in df.columns:
            # Already in cents (assume)
            df['amount_cad'] = df['amount_cad']
        else:
            print(f"    Warning: No amount column found in {filename}")
            df['amount_cad'] = np.nan
        
        # Standardize datetime column
        if 'transaction_datetime' in df.columns:
            df['transaction_datetime'] = pd.to_datetime(df['transaction_datetime'], errors='coerce')
        else:
            print(f"    Warning: No transaction_datetime column found in {filename}")
            df['transaction_datetime'] = pd.NaT
        
        # Ensure required columns exist
        required_cols = ['transaction_id', 'customer_id', 'debit_credit', 'transaction_datetime', 'amount_cad']
        for col in required_cols:
            if col not in df.columns:
                print(f"    Warning: Missing column {col} in {filename}, adding as NaN")
                df[col] = np.nan
        
        # Select and reorder columns (keep all original columns plus channel)
        # Put channel first, then standard columns, then channel-specific columns
        standard_cols = ['transaction_id', 'customer_id', 'debit_credit', 'transaction_datetime', 'amount_cad']
        other_cols = [col for col in df.columns if col not in standard_cols + ['transaction_channel']]
        df = df[['transaction_channel'] + standard_cols + other_cols]
        
        print(f"    Loaded {len(df):,} transactions")
        all_transactions.append(df)
    
    # Combine all transactions
    print("\nCombining all transactions...")
    combined = pd.concat(all_transactions, ignore_index=True)
    
    print(f"  Total transactions: {len(combined):,}")
    print(f"  Date range: {combined['transaction_datetime'].min()} to {combined['transaction_datetime'].max()}")
    print(f"  Channels: {combined['transaction_channel'].unique()}")
    print(f"  Columns: {list(combined.columns)}")
    
    return combined

def validate_data(customers, transactions):
    """Validate the loaded data"""
    print("\nValidating data...")
    
    # Check for missing customer IDs
    missing_customer_ids = transactions[~transactions['customer_id'].isin(customers['customer_id'])]
    if len(missing_customer_ids) > 0:
        print(f"  Warning: {len(missing_customer_ids):,} transactions have customer_ids not in customer table")
        print(f"    Unique missing customer_ids: {missing_customer_ids['customer_id'].nunique()}")
    
    # Check for null amounts
    null_amounts = transactions['amount_cad'].isna().sum()
    if null_amounts > 0:
        print(f"  Warning: {null_amounts:,} transactions have null amounts")
    
    # Check for null datetimes
    null_datetimes = transactions['transaction_datetime'].isna().sum()
    if null_datetimes > 0:
        print(f"  Warning: {null_datetimes:,} transactions have null datetimes")
    
    # Check debit/credit values
    debit_credit_values = transactions['debit_credit'].value_counts()
    print(f"  Debit/Credit distribution: {dict(debit_credit_values)}")
    
    print("  Validation complete")

def main():
    """Main execution"""
    print("=" * 60)
    print("Phase 1: Load and Combine Data")
    print("=" * 60)
    
    # Create output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Load customer data
    customers = load_customer_data()
    
    # Load and combine transaction data
    transactions = load_transaction_files()
    
    # Validate data
    validate_data(customers, transactions)
    
    # Save outputs
    print("\nSaving outputs...")
    
    # Save customer base
    customer_output = OUTPUT_DIR / 'customer_base.csv'
    customers.to_csv(customer_output, index=False)
    print(f"  Saved customer_base.csv: {len(customers):,} customers")
    
    # Save combined transactions
    transactions_output = OUTPUT_DIR / 'transactions_combined.csv'
    transactions.to_csv(transactions_output, index=False)
    print(f"  Saved transactions_combined.csv: {len(transactions):,} transactions")
    
    print("\n" + "=" * 60)
    print("Phase 1 Complete!")
    print("=" * 60)
    print(f"\nOutput files:")
    print(f"  - {customer_output}")
    print(f"  - {transactions_output}")

if __name__ == '__main__':
    main()
