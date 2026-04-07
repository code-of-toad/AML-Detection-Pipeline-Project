"""
Feature Engineering Script: Phase 2.3 - Channel Features
Purpose: Engineer channel-specific risk features for AML detection model
Input: features/intermediate/transactions_combined.csv, features/intermediate/customer_base.csv
Output: features/by_category/channel_features.csv

Features Created:
- Wire transfer features (high-risk channel)
- ABM/Cash features (cash transactions)
- Channel diversity features
- Channel-specific transaction counts and volumes
- Multi-channel usage flags
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

def engineer_channel_features(transactions, customers):
    """Engineer channel-specific features for each customer"""
    print("\nEngineering channel features...")
    
    # Initialize features dataframe
    features = pd.DataFrame()
    features['customer_id'] = customers['customer_id']
    
    # Filter out null amounts
    transactions_clean = transactions[transactions['amount_cad'].notna()].copy()
    
    # 1. Channel Usage Counts
    print("  Calculating channel usage counts...")
    channels_used = transactions_clean.groupby('customer_id')['transaction_channel'].nunique()
    features['channels_used_count'] = features['customer_id'].map(channels_used).fillna(0).astype(int)
    
    # Multi-channel flag (uses 3+ channels)
    features['multi_channel_flag'] = (features['channels_used_count'] >= 3).astype(int)
    
    # 2. Wire Transfer Features (HIGH RISK)
    print("  Calculating wire transfer features...")
    wire_txns = transactions_clean[transactions_clean['transaction_channel'] == 'WIRE']
    
    if len(wire_txns) > 0:
        wire_counts = wire_txns.groupby('customer_id').size()
        wire_volumes = wire_txns.groupby('customer_id')['amount_cad'].agg(['sum', 'mean', 'max'])
        # Large wire transfers: $10K = 1,000,000 cents
        wire_large = wire_txns[wire_txns['amount_cad'] > 1000000].groupby('customer_id').size()
        
        features['wire_txn_count'] = features['customer_id'].map(wire_counts).fillna(0).astype(int)
        features['wire_volume_total'] = features['customer_id'].map(wire_volumes['sum']).fillna(0)
        features['wire_volume_avg'] = features['customer_id'].map(wire_volumes['mean']).fillna(0)
        features['wire_volume_max'] = features['customer_id'].map(wire_volumes['max']).fillna(0)
        features['wire_large_count'] = features['customer_id'].map(wire_large).fillna(0).astype(int)
        features['has_wire_transfers'] = (features['wire_txn_count'] > 0).astype(int)
    else:
        features['wire_txn_count'] = 0
        features['wire_volume_total'] = 0
        features['wire_volume_avg'] = 0
        features['wire_volume_max'] = 0
        features['wire_large_count'] = 0
        features['has_wire_transfers'] = 0
    
    # 3. ABM/Cash Features (HIGH RISK)
    print("  Calculating ABM/cash features...")
    abm_txns = transactions_clean[transactions_clean['transaction_channel'] == 'ABM']
    
    if len(abm_txns) > 0:
        # Cash transactions (cash_indicator = 1)
        abm_cash = abm_txns[abm_txns.get('cash_indicator', pd.Series([0] * len(abm_txns))) == 1]
        
        if len(abm_cash) > 0:
            abm_cash_counts = abm_cash.groupby('customer_id').size()
            abm_cash_volumes = abm_cash.groupby('customer_id')['amount_cad'].agg(['sum', 'mean', 'max'])
            # Large cash withdrawals: $5K = 500,000 cents
            abm_cash_large = abm_cash[abm_cash['amount_cad'] > 500000].groupby('customer_id').size()
            
            features['abm_cash_txn_count'] = features['customer_id'].map(abm_cash_counts).fillna(0).astype(int)
            features['abm_cash_volume'] = features['customer_id'].map(abm_cash_volumes['sum']).fillna(0)
            features['abm_cash_volume_avg'] = features['customer_id'].map(abm_cash_volumes['mean']).fillna(0)
            features['abm_cash_volume_max'] = features['customer_id'].map(abm_cash_volumes['max']).fillna(0)
            features['abm_cash_large_count'] = features['customer_id'].map(abm_cash_large).fillna(0).astype(int)
            
            # Percentage of ABM transactions that are cash
            abm_total_counts = abm_txns.groupby('customer_id').size()
            abm_cash_mapped = features['customer_id'].map(abm_cash_counts).fillna(0)
            abm_total_mapped = features['customer_id'].map(abm_total_counts).fillna(0)
            features['abm_cash_pct'] = np.where(
                abm_total_mapped > 0,
                abm_cash_mapped / abm_total_mapped,
                0
            )
        else:
            features['abm_cash_txn_count'] = 0
            features['abm_cash_volume'] = 0
            features['abm_cash_volume_avg'] = 0
            features['abm_cash_volume_max'] = 0
            features['abm_cash_large_count'] = 0
            features['abm_cash_pct'] = 0
        
        # Structured cash deposits (multiple cash deposits same day)
        print("    Calculating structured cash deposits...")
        abm_cash_deposits = abm_cash[abm_cash['debit_credit'] == 'C'].copy()
        if len(abm_cash_deposits) > 0 and 'transaction_datetime' in abm_cash_deposits.columns:
            abm_cash_deposits['transaction_datetime'] = pd.to_datetime(abm_cash_deposits['transaction_datetime'], errors='coerce')
            abm_cash_deposits = abm_cash_deposits[abm_cash_deposits['transaction_datetime'].notna()]
            if len(abm_cash_deposits) > 0:
                abm_cash_deposits['date'] = abm_cash_deposits['transaction_datetime'].dt.date
                same_day_deposits = abm_cash_deposits.groupby(['customer_id', 'date']).size()
                structured_deposits = same_day_deposits[same_day_deposits >= 3].groupby('customer_id').size()
                features['structured_cash_deposits_same_day'] = features['customer_id'].map(structured_deposits).fillna(0).astype(int)
            else:
                features['structured_cash_deposits_same_day'] = 0
        else:
            features['structured_cash_deposits_same_day'] = 0
    else:
        features['abm_cash_txn_count'] = 0
        features['abm_cash_volume'] = 0
        features['abm_cash_volume_avg'] = 0
        features['abm_cash_volume_max'] = 0
        features['abm_cash_large_count'] = 0
        features['abm_cash_pct'] = 0
        features['structured_cash_deposits_same_day'] = 0
    
    # 4. Western Union Features (VERY HIGH RISK)
    print("  Calculating Western Union features...")
    wu_txns = transactions_clean[transactions_clean['transaction_channel'] == 'WESTERN_UNION']
    
    if len(wu_txns) > 0:
        wu_counts = wu_txns.groupby('customer_id').size()
        wu_volumes = wu_txns.groupby('customer_id')['amount_cad'].agg(['sum', 'mean', 'max'])
        
        features['western_union_txn_count'] = features['customer_id'].map(wu_counts).fillna(0).astype(int)
        features['western_union_volume_total'] = features['customer_id'].map(wu_volumes['sum']).fillna(0)
        features['western_union_volume_avg'] = features['customer_id'].map(wu_volumes['mean']).fillna(0)
        features['has_western_union'] = (features['western_union_txn_count'] > 0).astype(int)
    else:
        features['western_union_txn_count'] = 0
        features['western_union_volume_total'] = 0
        features['western_union_volume_avg'] = 0
        features['has_western_union'] = 0
    
    # 5. EFT Features
    print("  Calculating EFT features...")
    eft_txns = transactions_clean[transactions_clean['transaction_channel'] == 'EFT']
    
    if len(eft_txns) > 0:
        eft_counts = eft_txns.groupby('customer_id').size()
        eft_volumes = eft_txns.groupby('customer_id')['amount_cad'].agg(['sum', 'mean'])
        
        features['eft_txn_count'] = features['customer_id'].map(eft_counts).fillna(0).astype(int)
        features['eft_volume_total'] = features['customer_id'].map(eft_volumes['sum']).fillna(0)
        features['eft_volume_avg'] = features['customer_id'].map(eft_volumes['mean']).fillna(0)
    else:
        features['eft_txn_count'] = 0
        features['eft_volume_total'] = 0
        features['eft_volume_avg'] = 0
    
    # 6. EMT Features
    print("  Calculating EMT features...")
    emt_txns = transactions_clean[transactions_clean['transaction_channel'] == 'EMT']
    
    if len(emt_txns) > 0:
        emt_counts = emt_txns.groupby('customer_id').size()
        emt_volumes = emt_txns.groupby('customer_id')['amount_cad'].agg(['sum', 'mean'])
        
        features['emt_txn_count'] = features['customer_id'].map(emt_counts).fillna(0).astype(int)
        features['emt_volume_total'] = features['customer_id'].map(emt_volumes['sum']).fillna(0)
        features['emt_volume_avg'] = features['customer_id'].map(emt_volumes['mean']).fillna(0)
    else:
        features['emt_txn_count'] = 0
        features['emt_volume_total'] = 0
        features['emt_volume_avg'] = 0
    
    # 7. Card Features
    print("  Calculating card features...")
    card_txns = transactions_clean[transactions_clean['transaction_channel'] == 'CARD']
    
    if len(card_txns) > 0:
        card_counts = card_txns.groupby('customer_id').size()
        card_volumes = card_txns.groupby('customer_id')['amount_cad'].agg(['sum', 'mean'])
        
        # E-commerce transactions (if ecommerce_ind available)
        if 'ecommerce_ind' in card_txns.columns:
            card_ecom = card_txns[card_txns['ecommerce_ind'] == 1]
            ecom_counts = card_ecom.groupby('customer_id').size()
            ecom_mapped = features['customer_id'].map(ecom_counts).fillna(0)
            card_counts_mapped = features['customer_id'].map(card_counts).fillna(0)
            features['card_ecommerce_txn_count'] = ecom_mapped.astype(int)
            features['card_ecommerce_pct'] = np.where(
                card_counts_mapped > 0,
                ecom_mapped / card_counts_mapped,
                0
            )
        else:
            features['card_ecommerce_txn_count'] = 0
            features['card_ecommerce_pct'] = 0
        
        features['card_txn_count'] = features['customer_id'].map(card_counts).fillna(0).astype(int)
        features['card_volume_total'] = features['customer_id'].map(card_volumes['sum']).fillna(0)
        features['card_volume_avg'] = features['customer_id'].map(card_volumes['mean']).fillna(0)
    else:
        features['card_txn_count'] = 0
        features['card_volume_total'] = 0
        features['card_volume_avg'] = 0
        features['card_ecommerce_txn_count'] = 0
        features['card_ecommerce_pct'] = 0
    
    # 8. Cheque Features
    print("  Calculating cheque features...")
    cheque_txns = transactions_clean[transactions_clean['transaction_channel'] == 'CHEQUE']
    
    if len(cheque_txns) > 0:
        cheque_counts = cheque_txns.groupby('customer_id').size()
        cheque_volumes = cheque_txns.groupby('customer_id')['amount_cad'].agg(['sum', 'mean', 'max'])
        cheque_large = cheque_txns[cheque_txns['amount_cad'] > 1000000].groupby('customer_id').size()  # 1M cents = $10K
        
        features['cheque_txn_count'] = features['customer_id'].map(cheque_counts).fillna(0).astype(int)
        features['cheque_volume_total'] = features['customer_id'].map(cheque_volumes['sum']).fillna(0)
        features['cheque_volume_avg'] = features['customer_id'].map(cheque_volumes['mean']).fillna(0)
        features['cheque_volume_max'] = features['customer_id'].map(cheque_volumes['max']).fillna(0)
        features['cheque_large_count'] = features['customer_id'].map(cheque_large).fillna(0).astype(int)
    else:
        features['cheque_txn_count'] = 0
        features['cheque_volume_total'] = 0
        features['cheque_volume_avg'] = 0
        features['cheque_volume_max'] = 0
        features['cheque_large_count'] = 0
    
    # Fill NaN values
    features = features.fillna(0)
    
    # Ensure integer columns are integers
    int_columns = [col for col in features.columns if col != 'customer_id' and ('count' in col.lower() or 'flag' in col.lower() or 'has_' in col.lower())]
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
    print(f"  Channels used: {features['channels_used_count'].min()} to {features['channels_used_count'].max()}")
    print(f"  Multi-channel customers: {features['multi_channel_flag'].sum():,}")
    print(f"  Wire transfer users: {features['has_wire_transfers'].sum():,}")
    print(f"  Western Union users: {features['has_western_union'].sum():,}")
    print(f"  Cash transaction users: {features[features['abm_cash_txn_count'] > 0].shape[0]:,}")
    
    print("  Validation complete")

def main():
    """Main execution"""
    print("=" * 60)
    print("Phase 2.3: Channel Features")
    print("=" * 60)
    
    # Load data
    transactions, customers = load_data()
    
    # Engineer features
    features = engineer_channel_features(transactions, customers)
    
    # Validate
    validate_features(features)
    
    # Save output
    print("\nSaving features...")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / 'channel_features.csv'
    features.to_csv(output_path, index=False)
    
    print(f"\nSaved: {output_path}")
    print(f"Features created: {len(features.columns) - 1}")  # -1 for customer_id
    print(f"Customers: {len(features):,}")
    print(f"\nFeature columns: {list(features.columns)}")
    
    # Generate report
    print("\nGenerating validation report...")
    generate_feature_report(features, 'channel_features', REPORT_DIR)
    
    print("\n" + "=" * 60)
    print("Phase 2.3 Complete!")
    print("=" * 60)

if __name__ == '__main__':
    main()
