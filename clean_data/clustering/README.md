# clustering

Clustering assignments used to produce `master_features_with_clustering.csv`.

- **Kmeans_Seperate.csv** — Columns: `customer_id`, `cluster`. Cluster values are string labels (e.g. `individual_0` … `individual_8`, `business_0` … `business_6`). One row per customer.

Script `scripts/11_merge_clustering.py` reads this file and merges it with `master_features.csv` to create the final pipeline input.
