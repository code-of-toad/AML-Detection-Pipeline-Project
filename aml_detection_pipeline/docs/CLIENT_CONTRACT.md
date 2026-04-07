# Client contract — Pipeline v2

## 1. Pipeline input (single file)

| Input | Location | Responsibility |
|-------|----------|----------------|
| **master_features_with_clustering.csv** | `data/input/master_features_with_clustering.csv` | Client. Produced by **clean_data** (see repo `clean_data/`). One row per customer; all feature columns + **cluster** (string labels, e.g. individual_0, business_2). |

The pipeline has **no** prep or merge step. It starts from this one file.

## 2. Partner score contract (fusion “30%”)

| Requirement | Spec |
|-------------|------|
| **Format** | CSV, UTF-8. |
| **Naming** | **Strict:** `scores_[ml_model].csv` (e.g. `scores_isolation_forest.csv`). All live in **ml_algorithms/outputs/**. |
| **Per-model dir** | Each model in **ml_algorithms/model_[ml_model]/** (e.g. `model_isolation_forest/`) with scripts to generate its output. |
| **Required columns** | **customer_id** and one numeric score column: `score`, `scores`, `risk_score`, or `outlier_score_01`. |
| **Rows** | One per customer in the pipeline input. Same customer set. |
| **Score values** | Numeric; pipeline may min-max normalize to [0, 1]. |
| **Path** | Set in config: **paths.partner_score_file** (e.g. `ml_algorithms/outputs/scores_isolation_forest.csv`). |

## 3. Pipeline outputs

| Output | Path / pattern |
|--------|-----------------|
| **rule_based_scores.csv** | data/intermediate/rule_based_scores.csv |
| **model_output_[ml_model].csv** (Task 2) | data/output/model_output_[ml_model].csv — one per discovered scores_[ml_model].csv (customer_id, predicted_label, risk_score) |
| **model_output_[ml_model]_explanations.csv** (Task 3) | data/output/model_output_[ml_model]_explanations.csv — one per model (customer_id, explanation) |
| **model_report_[ml_model].pdf** | data/output/model_report_[ml_model].pdf — one per model (overview, distribution, score bands) |
| **model_comparison_report.pdf** | data/output/model_comparison_report.pdf — similarities/differences and overlap across all models |
| **consistently_flagged_customers.csv** | data/output/consistently_flagged_customers.csv — customer_id only; customers flagged by **all** models (when 2+ models exist) |
| **consistently_flagged_explanations.csv** | data/output/consistently_flagged_explanations.csv — customer_id, model, explanation; one row per (customer, model) so you see each model’s explanation (explanations differ by model) |

The pipeline **discovers** all **scores_*.csv** in **ml_algorithms/outputs/** and generates the CSVs and PDFs above for each. **Each run clears data/output** (deletes all existing CSVs and PDFs) and re-creates everything.

## 4. Client workflow

1. Produce **master_features_with_clustering.csv** (via clean_data) and place it in **data/input/**.
2. Run one or more models (e.g. from ml_algorithms/model_*/); each writes **scores_[ml_model].csv** into **ml_algorithms/outputs/**.
3. Run: `python scripts/run_pipeline.py`. The pipeline finds every scores_*.csv and writes model_output_[ml_model].csv and model_output_[ml_model]_explanations.csv.
4. Use the generated files in **data/output/** for submission. Add or remove scores_*.csv files and re-run anytime.
