# model_isolation_forest

Isolation Forest anomaly detection. Reads the pipeline input (`master_features_with_clustering.csv`), trains on numeric features, and writes **scores_isolation_forest.csv** to `ml_algorithms/outputs/`.

## Output

- **File:** `../outputs/scores_isolation_forest.csv` (columns: `customer_id`, `score`).
- **Artifacts:** `artifacts/isolation_forest.pkl`, `artifacts/scaler.pkl` (saved by default).

## Run

From this directory:

```bash
python run.py
```

Optional: `--input`, `--output`, `--model-dir`, `--contamination`, `--n-estimators`, `--random-state`.

Then set the pipeline config `paths.partner_score_file` to `ml_algorithms/outputs/scores_isolation_forest.csv` and run the pipeline.
