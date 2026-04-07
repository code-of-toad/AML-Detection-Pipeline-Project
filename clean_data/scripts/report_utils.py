"""
Reporting Utilities for Feature Engineering
Purpose: Generate summary and validation reports for feature files
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime

def generate_feature_report(features, feature_category, output_dir):
    """
    Generate a comprehensive summary and validation report for feature file
    
    Args:
        features: DataFrame with features (must include 'customer_id')
        feature_category: Name of feature category (e.g., 'velocity_features')
        output_dir: Directory to save report
    """
    report_path = output_dir / f'{feature_category}_report.md'
    
    report = []
    report.append(f"# Feature Report: {feature_category.replace('_', ' ').title()}\n")
    report.append(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    report.append("---\n\n")
    
    # Basic Information
    report.append("## Basic Information\n\n")
    report.append(f"- **Total Customers**: {len(features):,}\n")
    report.append(f"- **Total Features**: {len(features.columns) - 1}\n")  # -1 for customer_id
    report.append(f"- **Feature Columns**: {', '.join([col for col in features.columns if col != 'customer_id'])}\n\n")
    
    # Data Quality Checks
    report.append("## Data Quality Checks\n\n")
    
    # Null values
    null_counts = features.isnull().sum()
    null_cols = null_counts[null_counts > 0]
    if len(null_cols) > 0:
        report.append("### ⚠️ Null Values Found\n\n")
        report.append("| Column | Null Count | Null Percentage |\n")
        report.append("|--------|------------|------------------|\n")
        for col, count in null_cols.items():
            pct = (count / len(features)) * 100
            report.append(f"| `{col}` | {count:,} | {pct:.2f}% |\n")
        report.append("\n")
    else:
        report.append("### ✅ No Null Values\n\n")
        report.append("All features have complete data.\n\n")
    
    # Duplicate customer IDs
    duplicate_customers = features['customer_id'].duplicated().sum()
    if duplicate_customers > 0:
        report.append(f"### ⚠️ Duplicate Customer IDs: {duplicate_customers}\n\n")
    else:
        report.append("### ✅ No Duplicate Customer IDs\n\n")
    
    # Feature Statistics
    report.append("## Feature Statistics\n\n")
    
    feature_cols = [col for col in features.columns if col != 'customer_id']
    
    # Exclude non-numeric columns from statistics
    exclude_cols = ['kyc_type', 'label']  # Add other non-numeric columns as needed
    numeric_cols = [col for col in feature_cols if col not in exclude_cols]
    
    report.append("| Feature | Type | Min | Max | Mean | Median | Std Dev | Zero Count | Zero % |\n")
    report.append("|---------|------|-----|-----|------|--------|---------|------------|--------|\n")
    
    for col in feature_cols:
        col_data = features[col]
        
        # Determine type
        if col_data.dtype in ['int64', 'int32']:
            dtype = 'Integer'
        elif col_data.dtype in ['float64', 'float32']:
            dtype = 'Float'
        else:
            dtype = str(col_data.dtype)
        
        # Calculate statistics (only for numeric columns)
        if col in numeric_cols and col_data.dtype in ['int64', 'int32', 'float64', 'float32']:
            try:
                min_val = col_data.min()
                max_val = col_data.max()
                mean_val = col_data.mean()
                median_val = col_data.median()
                std_val = col_data.std()
                zero_count = (col_data == 0).sum()
                zero_pct = (zero_count / len(features)) * 100
            except (TypeError, ValueError):
                # If calculation fails, use N/A
                min_val = max_val = mean_val = median_val = std_val = None
                zero_count = 0
                zero_pct = 0
        else:
            # For non-numeric columns, show value counts or N/A
            min_val = max_val = mean_val = median_val = std_val = None
            zero_count = 0
            zero_pct = 0
        
        # Format values
        if min_val is None or pd.isna(min_val):
            min_str = max_str = mean_str = median_str = std_str = "N/A"
        elif dtype == 'Integer':
            min_str = f"{int(min_val):,}"
            max_str = f"{int(max_val):,}"
            mean_str = f"{mean_val:.2f}"
            median_str = f"{int(median_val):,}"
            std_str = f"{std_val:.2f}"
        else:
            min_str = f"{min_val:.2f}"
            max_str = f"{max_val:.2f}"
            mean_str = f"{mean_val:.2f}"
            median_str = f"{median_val:.2f}"
            std_str = f"{std_val:.2f}"
        
        report.append(f"| `{col}` | {dtype} | {min_str} | {max_str} | {mean_str} | {median_str} | {std_str} | {zero_count:,} | {zero_pct:.2f}% |\n")
    
    report.append("\n")
    
    # Validation Checks
    report.append("## Validation Checks\n\n")
    
    # Check for negative values in non-negative features
    non_negative_features = [col for col in feature_cols if 'count' in col.lower() or 'flag' in col.lower() or 'pct' in col.lower()]
    negative_issues = []
    for col in non_negative_features:
        negative_count = (features[col] < 0).sum()
        if negative_count > 0:
            negative_issues.append(f"- `{col}`: {negative_count:,} negative values")
    
    if negative_issues:
        report.append("### ⚠️ Negative Values Found\n\n")
        for issue in negative_issues:
            report.append(f"{issue}\n")
        report.append("\n")
    else:
        report.append("### ✅ No Unexpected Negative Values\n\n")
    
    # Check for infinite values
    inf_issues = []
    for col in feature_cols:
        if features[col].dtype in ['float64', 'float32']:
            inf_count = np.isinf(features[col]).sum()
            if inf_count > 0:
                inf_issues.append(f"- `{col}`: {inf_count:,} infinite values")
    
    if inf_issues:
        report.append("### ⚠️ Infinite Values Found\n\n")
        for issue in inf_issues:
            report.append(f"{issue}\n")
        report.append("\n")
    else:
        report.append("### ✅ No Infinite Values\n\n")
    
    # Check for extreme outliers (beyond 3 standard deviations)
    report.append("### Outlier Detection (Values > 3 Standard Deviations)\n\n")
    outlier_summary = []
    for col in feature_cols:
        if features[col].dtype in ['float64', 'float32', 'int64', 'int32']:
            mean = features[col].mean()
            std = features[col].std()
            if std > 0:
                outliers = ((features[col] - mean).abs() > 3 * std).sum()
                if outliers > 0:
                    outlier_pct = (outliers / len(features)) * 100
                    outlier_summary.append(f"- `{col}`: {outliers:,} outliers ({outlier_pct:.2f}%)")
    
    if outlier_summary:
        for item in outlier_summary[:10]:  # Limit to first 10
            report.append(f"{item}\n")
        if len(outlier_summary) > 10:
            report.append(f"\n... and {len(outlier_summary) - 10} more features with outliers\n")
        report.append("\n")
    else:
        report.append("No significant outliers detected.\n\n")
    
    # Distribution Summary for Flags
    flag_features = [col for col in feature_cols if 'flag' in col.lower()]
    if flag_features:
        report.append("## Flag Feature Distributions\n\n")
        report.append("| Feature | True Count | True Percentage | False Count | False Percentage |\n")
        report.append("|---------|------------|-----------------|-------------|------------------|\n")
        
        for col in flag_features:
            true_count = (features[col] == 1).sum()
            false_count = (features[col] == 0).sum()
            true_pct = (true_count / len(features)) * 100
            false_pct = (false_count / len(features)) * 100
            report.append(f"| `{col}` | {true_count:,} | {true_pct:.2f}% | {false_count:,} | {false_pct:.2f}% |\n")
        
        report.append("\n")
    
    # Summary
    report.append("## Summary\n\n")
    report.append(f"- ✅ **Total Features**: {len(feature_cols)}\n")
    report.append(f"- ✅ **Data Completeness**: {((len(features) - null_counts.sum()) / (len(features) * len(feature_cols)) * 100):.2f}%\n")
    report.append(f"- ✅ **Customers Covered**: {len(features):,}\n")
    
    if flag_features:
        report.append(f"- ✅ **Flag Features**: {len(flag_features)}\n")
    
    report.append("\n---\n")
    report.append(f"*Report generated automatically by feature engineering pipeline*\n")
    
    # Write report
    output_dir.mkdir(parents=True, exist_ok=True)
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(''.join(report))
    
    print(f"  Report saved: {report_path}")
    return report_path
