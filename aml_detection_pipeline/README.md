# AML Detection Pipeline v2

Single input: **master_features_with_clustering.csv** (from clean_data). The pipeline **discovers** all **scores_*.csv** in **ml_algorithms/outputs/** and for each produces **model_output_[ml_model].csv** and **model_output_[ml_model]_explanations.csv**. No config edit when adding or swapping score files.

## Layout

```
aml_detection_pipeline/
├── config/          config.yaml, load_config.py
├── data/
│   ├── input/      master_features_with_clustering.csv (from clean_data)
│   ├── intermediate/  rule_based_scores.csv
│   └── output/     model_output_[ml_model].csv, model_output_[ml_model]_explanations.csv (per discovered scores_*.csv)
├── docs/            CLIENT_CONTRACT.md
├── ml_algorithms/
│   ├── outputs/    scores_[ml_model].csv (drop here; pipeline discovers all)
│   └── model_*/    one directory per model (run scripts, write to outputs/)
└── scripts/        rule_based_scorer, run_pipeline, explanation_generator, explanation_viewer_gui
```

## Run

1. Put **data/input/master_features_with_clustering.csv** in place (from clean_data).
2. Put any **scores_[ml_model].csv** files in **ml_algorithms/outputs/** (from model scripts or your own).
3. From pipeline root: `python scripts/run_pipeline.py`  
   The pipeline finds every scores_*.csv and generates the corresponding model_output_* and explanations files. Add or remove score files and re-run as needed; no config change.
4. If **config: viewer: launch_after_run: true** (default), the explanation viewer GUI opens at the end so you can browse results. Close the window to exit. To run without the GUI (e.g. headless), set **launch_after_run: false**. You can also run the viewer alone: `python scripts/explanation_viewer_gui.py`.

Submission deliverables (Task 2 and Task 3) are written to `data/output/` and copied to `../task_2_model_outputs/` and `../task_3_model_outputs_explanations/` when run from the submission package. See `../README.md` for the full checklist.

## Contract

See **docs/CLIENT_CONTRACT.md** for input/output and partner CSV contract.
