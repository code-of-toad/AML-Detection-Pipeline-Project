# ml_algorithms

Pluggable ML / anomaly models whose outputs feed the pipeline fusion (the "30%" partner score). The pipeline does **not** run any model here; it only reads **one** partner score CSV chosen via config.

## Naming and layout (strict convention)

- **Output files:** All model output CSVs live in **outputs/** and must be named **`scores_[ml_model].csv`** (e.g. `scores_isolation_forest.csv`, `scores_full_LOF.csv`).
- **Per-model directory:** Each model has its own folder **`model_[ml_model]/`** (e.g. `model_isolation_forest/`, `model_full_LOF/`) containing everything needed to produce that model’s output (scripts, README, artifacts).

```
ml_algorithms/
├── outputs/
│   ├── scores_isolation_forest.csv
│   ├── scores_full_LOF.csv
│   └── ...
├── model_isolation_forest/
│   ├── run.py
│   ├── README.md
│   └── artifacts/
├── model_full_LOF/
│   └── ...
└── README.md (this file)
```

## Contract for each output CSV

- **Columns:** `customer_id` and one numeric score column (`score`, `scores`, `risk_score`, or `outlier_score_01`).
- **Rows:** One per customer in the pipeline input; same customer set.
- **Values:** Numeric; pipeline may min-max normalize to [0, 1].

## Using a model’s output in the pipeline

1. Run the model (e.g. `python run.py` from `model_isolation_forest/`) so that **outputs/scores_&lt;model&gt;.csv** exists.
2. Set **config/config.yaml** → **paths.partner_score_file** to `ml_algorithms/outputs/scores_<model>.csv`.
3. Run the pipeline.
