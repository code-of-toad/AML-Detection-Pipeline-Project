"""
Merge master_features.csv with clustering assignments to produce the final pipeline input.

Input:
  - features/final/master_features.csv
  - clustering/Kmeans_Seperate.csv (customer_id, cluster)
Input for metadata:
  - features/final/master_features_metadata.csv

Output:
  - features/final/master_features_with_clustering.csv (all feature columns + cluster)
  - features/final/master_features_with_clustering_metadata.csv (existing metadata + cluster row)

Run from clean_data/scripts: python 11_merge_clustering.py
"""

import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
FINAL_DIR = BASE_DIR / "features" / "final"
CLUSTERING_DIR = BASE_DIR / "clustering"

MASTER_FEATURES = FINAL_DIR / "master_features.csv"
MASTER_METADATA = FINAL_DIR / "master_features_metadata.csv"
CLUSTER_FILE = CLUSTERING_DIR / "Kmeans_Seperate.csv"
OUTPUT_CSV = FINAL_DIR / "master_features_with_clustering.csv"
OUTPUT_METADATA = FINAL_DIR / "master_features_with_clustering_metadata.csv"


def main():
    if not MASTER_FEATURES.exists():
        raise FileNotFoundError(
            f"Master features not found: {MASTER_FEATURES}\n"
            "Run scripts 01–09 to produce master_features.csv first."
        )
    if not CLUSTER_FILE.exists():
        raise FileNotFoundError(
            f"Clustering file not found: {CLUSTER_FILE}\n"
            "Place Kmeans_Seperate.csv (customer_id, cluster) in clean_data/clustering/."
        )

    print("Loading master_features...")
    features = pd.read_csv(MASTER_FEATURES)
    print(f"  {len(features):,} rows, {len(features.columns)} columns")

    print("Loading clustering (Kmeans_Seperate)...")
    cluster_df = pd.read_csv(CLUSTER_FILE)
    if "customer_id" not in cluster_df.columns or "cluster" not in cluster_df.columns:
        raise ValueError("Clustering file must have columns: customer_id, cluster")
    cluster_df = cluster_df[["customer_id", "cluster"]]
    print(f"  {len(cluster_df):,} rows")

    print("Merging on customer_id (left join)...")
    merged = features.merge(cluster_df, on="customer_id", how="left")
    print(f"  Result: {len(merged):,} rows, {len(merged.columns)} columns")

    missing = merged["cluster"].isna().sum()
    if missing > 0:
        print(f"  Note: {missing:,} customers have no cluster (NaN).")

    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    merged.to_csv(OUTPUT_CSV, index=False)
    print(f"Wrote {OUTPUT_CSV.name}")

    # Metadata: copy master_features_metadata and add one row for cluster
    if MASTER_METADATA.exists():
        meta = pd.read_csv(MASTER_METADATA)
        cluster_row = pd.DataFrame([{
            "feature_name": "cluster",
            "feature_category": "clustering",
            "red_flag_source": "Clustering analysis",
            "red_flag_description": "Behavioural segment assignment",
            "data_signal": "K-means cluster label (individual_0..individual_8, business_0..business_6)",
            "feature_type": "categorical",
            "description": "Customer segment from separate individual/business K-means clustering (Kmeans_Seperate).",
        }])
        meta_with_cluster = pd.concat([meta, cluster_row], ignore_index=True)
        meta_with_cluster.to_csv(OUTPUT_METADATA, index=False)
        print(f"Wrote {OUTPUT_METADATA.name}")
    else:
        print(f"  (No {MASTER_METADATA.name} found; skipping metadata.)")

    print("Done. Final pipeline input: features/final/master_features_with_clustering.csv")


if __name__ == "__main__":
    main()
