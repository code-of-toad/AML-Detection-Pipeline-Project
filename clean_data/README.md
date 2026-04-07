# clean_data — Data wrangling from raw to pipeline input

This directory contains the full data cleaning and feature-engineering process that produces the **single input file** used by the detection pipeline: **`master_features_with_clustering.csv`**.

## Flow (start to end)

1. **Starting point:** `clean_original/` — cleaned raw tables (customers, transactions by channel, etc.). If you have only raw data, produce `clean_original/` first (e.g. via your own raw-cleaning step); scripts here expect it to exist.
2. **Intermediate:** `features/intermediate/` — combined transactions, customer base.
3. **Feature build:** Scripts `01_load_and_combine.py` … `09_combine_features.py` — by-category features → **`features/final/master_features.csv`** and **`features/final/master_features_metadata.csv`**.
4. **Clustering merge:** Script `11_merge_clustering.py` — merges `master_features.csv` with **`clustering/Kmeans_Seperate.csv`** (customer_id, cluster) → **`features/final/master_features_with_clustering.csv`** and **`features/final/master_features_with_clustering_metadata.csv`**.

**Final output:** `features/final/master_features_with_clustering.csv` is the only file the detection pipeline needs as input.

## Key paths

| Path | Description |
|------|-------------|
| `clean_original/` | Cleaned raw inputs (start of wrangling). |
| `scripts/` | All scripts (01–11); run in order for a full rebuild. |
| `features/by_category/` | Feature CSVs by category (velocity, amount, channel, etc.). |
| `features/intermediate/` | customer_base, transactions_combined. |
| `features/final/` | master_features.csv, master_features_metadata.csv, **master_features_with_clustering.csv**, **master_features_with_clustering_metadata.csv**. |
| `clustering/` | Clustering input: Kmeans_Seperate.csv (customer_id, cluster). |

## Run order (full rebuild)

From `clean_data/scripts/`:

1. Run `01_load_and_combine.py` through `09_combine_features.py` (and `10_create_metadata.py` if used).
2. Run `11_merge_clustering.py` to produce `master_features_with_clustering.csv` and its metadata.
