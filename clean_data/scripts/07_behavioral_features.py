"""
Feature Engineering Script: Phase 2.6 - Behavioral Features
Purpose: Engineer behavioral pattern features for AML detection model
Input: features/intermediate/transactions_combined.csv, features/intermediate/customer_base.csv
Output: features/by_category/behavioral_features.csv

Features Created:
- Amount to income/sales ratios (lifestyle mismatch)
- Transaction pattern anomalies
- Behavioral consistency metrics
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

def engineer_behavioral_features(transactions, customers):
    """Engineer behavioral features for each customer"""
    print("\nEngineering behavioral features...")
    
    # Initialize features dataframe
    features = pd.DataFrame()
    features['customer_id'] = customers['customer_id']
    
    # Merge customer data for income/sales
    customer_data = customers[['customer_id', 'income_cad', 'sales_cad', 'kyc_type']].copy()
    
    # Calculate total transaction volume per customer
    print("  Calculating transaction volumes...")
    transaction_volumes = transactions.groupby('customer_id')['amount_cad'].agg(['sum', 'mean', 'max', 'std']).fillna(0)
    
    features['total_volume'] = features['customer_id'].map(transaction_volumes['sum']).fillna(0)
    features['avg_transaction_amount'] = features['customer_id'].map(transaction_volumes['mean']).fillna(0)
    features['max_transaction_amount'] = features['customer_id'].map(transaction_volumes['max']).fillna(0)
    features['transaction_amount_std'] = features['customer_id'].map(transaction_volumes['std']).fillna(0)
    
    # Merge customer income/sales data
    features = features.merge(customer_data, on='customer_id', how='left')
    
    # 1. Amount to Income/Sales Ratios (Lifestyle Mismatch)
    print("  Calculating amount to income/sales ratios...")
    
    # For individuals: amount to income ratio
    individual_mask = features['kyc_type'] == 'individual'
    features['amount_to_income_ratio'] = 0.0
    features.loc[individual_mask & (features['income_cad'] > 0), 'amount_to_income_ratio'] = (
        features.loc[individual_mask & (features['income_cad'] > 0), 'total_volume'] / 
        features.loc[individual_mask & (features['income_cad'] > 0), 'income_cad']
    )
    
    # For businesses: amount to sales ratio
    business_mask = features['kyc_type'] == 'business'
    features['amount_to_sales_ratio'] = 0.0
    features.loc[business_mask & (features['sales_cad'] > 0), 'amount_to_sales_ratio'] = (
        features.loc[business_mask & (features['sales_cad'] > 0), 'total_volume'] / 
        features.loc[business_mask & (features['sales_cad'] > 0), 'sales_cad']
    )
    
    # Combined ratio (income for individuals, sales for businesses)
    features['amount_to_revenue_ratio'] = np.where(
        individual_mask,
        features['amount_to_income_ratio'],
        features['amount_to_sales_ratio']
    )
    
    # Lifestyle mismatch flags
    # High ratio indicates transactions exceed declared income/sales
    features['lifestyle_mismatch'] = (features['amount_to_revenue_ratio'] > 2.0).astype(int)  # Transactions > 2x income/sales
    features['severe_lifestyle_mismatch'] = (features['amount_to_revenue_ratio'] > 5.0).astype(int)  # Transactions > 5x income/sales
    
    # 2. Missing Income/Sales Indicators
    print("  Calculating missing income/sales indicators...")
    
    # For individuals
    features['has_missing_income'] = (
        individual_mask & 
        ((features['income_cad'].isna()) | (features['income_cad'] <= 0))
    ).astype(int)
    
    # For businesses
    features['has_missing_sales'] = (
        business_mask & 
        ((features['sales_cad'].isna()) | (features['sales_cad'] <= 0))
    ).astype(int)
    
    # 3. Transaction Pattern Anomalies
    print("  Calculating transaction pattern anomalies...")
    
    # Coefficient of variation (std/mean) - high indicates inconsistent amounts
    features['amount_cv'] = np.where(
        features['avg_transaction_amount'] > 0,
        features['transaction_amount_std'] / features['avg_transaction_amount'],
        0
    )
    features['amount_cv'] = features['amount_cv'].fillna(0)
    features['amount_cv'] = features['amount_cv'].clip(upper=10)  # Cap at 10x
    
    # High variability flag (inconsistent transaction amounts)
    features['high_amount_variability'] = (features['amount_cv'] > 2.0).astype(int)
    
    # 4. Debit/Credit Balance Analysis
    print("  Calculating debit/credit balance...")
    
    debit_volumes = transactions[transactions['debit_credit'] == 'D'].groupby('customer_id')['amount_cad'].sum()
    credit_volumes = transactions[transactions['debit_credit'] == 'C'].groupby('customer_id')['amount_cad'].sum()
    
    features['debit_volume'] = features['customer_id'].map(debit_volumes).fillna(0)
    features['credit_volume'] = features['customer_id'].map(credit_volumes).fillna(0)
    
    # Net flow (credits - debits)
    features['net_flow'] = features['credit_volume'] - features['debit_volume']
    
    # Debit/credit ratio
    features['debit_credit_ratio'] = np.where(
        features['credit_volume'] > 0,
        features['debit_volume'] / features['credit_volume'],
        0
    )
    features['debit_credit_ratio'] = features['debit_credit_ratio'].fillna(0)
    features['debit_credit_ratio'] = features['debit_credit_ratio'].clip(upper=10)  # Cap at 10x
    
    # Unusual flow patterns
    # High debit ratio (more money going out than coming in)
    features['high_debit_ratio'] = (features['debit_credit_ratio'] > 2.0).astype(int)
    
    # 5. Large Transaction Relative to Income/Sales
    print("  Calculating large transaction indicators...")
    
    # Max transaction relative to income/sales
    features['max_txn_to_income_ratio'] = 0.0
    features.loc[individual_mask & (features['income_cad'] > 0), 'max_txn_to_income_ratio'] = (
        features.loc[individual_mask & (features['income_cad'] > 0), 'max_transaction_amount'] / 
        features.loc[individual_mask & (features['income_cad'] > 0), 'income_cad']
    )
    
    features['max_txn_to_sales_ratio'] = 0.0
    features.loc[business_mask & (features['sales_cad'] > 0), 'max_txn_to_sales_ratio'] = (
        features.loc[business_mask & (features['sales_cad'] > 0), 'max_transaction_amount'] / 
        features.loc[business_mask & (features['sales_cad'] > 0), 'sales_cad']
    )
    
    # Combined ratio
    features['max_txn_to_revenue_ratio'] = np.where(
        individual_mask,
        features['max_txn_to_income_ratio'],
        features['max_txn_to_sales_ratio']
    )
    
    # Flag for single transaction exceeding annual income/sales
    features['single_txn_exceeds_revenue'] = (features['max_txn_to_revenue_ratio'] > 1.0).astype(int)
    
    # 6. Transaction Pattern Consistency
    print("  Calculating transaction pattern consistency...")
    
    # Load velocity features to get transaction counts
    try:
        velocity_features = pd.read_csv(INPUT_DIR.parent / 'by_category' / 'velocity_features.csv')
        txn_counts = velocity_features.set_index('customer_id')['txn_count_total']
        features['txn_count_total'] = features['customer_id'].map(txn_counts).fillna(0)
        
        # Average transaction amount consistency (lower std relative to mean = more consistent)
        features['transaction_consistency'] = np.where(
            features['avg_transaction_amount'] > 0,
            1 / (1 + features['amount_cv']),  # Inverse of CV, normalized
            0
        )
        
        # Consistent pattern flag (low variability in amounts)
        features['consistent_pattern_flag'] = (
            (features['amount_cv'] < 0.5) & 
            (features['txn_count_total'] >= 10)
        ).astype(int)
    except FileNotFoundError:
        print("    Warning: velocity_features.csv not found, skipping some consistency metrics")
        features['txn_count_total'] = 0
        features['transaction_consistency'] = 0
        features['consistent_pattern_flag'] = 0
    
    # 7. Behavioral Risk Score (Composite)
    print("  Calculating behavioral risk score...")
    
    # Simple risk score based on multiple indicators
    risk_score = 0
    risk_score += features['lifestyle_mismatch'] * 2
    risk_score += features['severe_lifestyle_mismatch'] * 3
    risk_score += features['has_missing_income'] * 1
    risk_score += features['has_missing_sales'] * 1
    risk_score += features['high_amount_variability'] * 1
    risk_score += features['high_debit_ratio'] * 1
    risk_score += features['single_txn_exceeds_revenue'] * 2
    
    features['behavioral_risk_score'] = risk_score
    
    # High risk flag
    features['high_behavioral_risk'] = (features['behavioral_risk_score'] >= 3).astype(int)
    
    # Drop temporary columns
    features = features.drop(columns=['kyc_type', 'income_cad', 'sales_cad'], errors='ignore')
    
    # Fill NaN values
    features = features.fillna(0)
    
    # Ensure integer columns are integers
    int_columns = [col for col in features.columns if col != 'customer_id' and (
        'flag' in col.lower() or 
        'has_' in col.lower() or
        'mismatch' in col.lower() or
        'score' in col.lower() or
        'count' in col.lower()
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
    print(f"  Amount to revenue ratio range: {features['amount_to_revenue_ratio'].min():.2f} to {features['amount_to_revenue_ratio'].max():.2f}")
    print(f"  Lifestyle mismatch: {features['lifestyle_mismatch'].sum():,} customers")
    print(f"  Severe lifestyle mismatch: {features['severe_lifestyle_mismatch'].sum():,} customers")
    print(f"  Missing income: {features['has_missing_income'].sum():,} customers")
    print(f"  Missing sales: {features['has_missing_sales'].sum():,} customers")
    print(f"  High behavioral risk: {features['high_behavioral_risk'].sum():,} customers")
    
    print("  Validation complete")

def main():
    """Main execution"""
    print("=" * 60)
    print("Phase 2.6: Behavioral Features")
    print("=" * 60)
    
    # Load data
    transactions, customers = load_data()
    
    # Engineer features
    features = engineer_behavioral_features(transactions, customers)
    
    # Validate
    validate_features(features)
    
    # Save output
    print("\nSaving features...")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / 'behavioral_features.csv'
    features.to_csv(output_path, index=False)
    
    print(f"\nSaved: {output_path}")
    print(f"Features created: {len(features.columns) - 1}")  # -1 for customer_id
    print(f"Customers: {len(features):,}")
    print(f"\nFeature columns: {list(features.columns)}")
    
    # Generate report
    print("\nGenerating validation report...")
    generate_feature_report(features, 'behavioral_features', REPORT_DIR)
    
    print("\n" + "=" * 60)
    print("Phase 2.6 Complete!")
    print("=" * 60)

if __name__ == '__main__':
    main()
