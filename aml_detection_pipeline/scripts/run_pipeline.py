"""
AML Detection Pipeline v2 — single entry point.

Input: master_features_with_clustering.csv (from clean_data).
Discovers all scores_[ml_model].csv in ml_algorithms/outputs/ and for each:
  - Fuses rule-based + partner score -> model_output_[ml_model].csv
  - Generates explanations -> model_output_[ml_model]_explanations.csv

No config edit needed: drop new scores_*.csv files in ml_algorithms/outputs/ and re-run.

Run from pipeline root: python scripts/run_pipeline.py
"""

import sys
import shutil
from pathlib import Path

import numpy as np
import pandas as pd

PIPELINE_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PIPELINE_ROOT))

from config.load_config import load_config  # pylint: disable=import-error,wrong-import-position
from scripts.rule_based_scorer import run as run_rule_based_scorer  # pylint: disable=import-error,wrong-import-position
from scripts.explanation_generator import run as run_explanation_generator  # pylint: disable=import-error,wrong-import-position


def _clear_output_dir(output_dir):
    """Delete all files in data/output so each run starts clean."""
    output_dir = Path(output_dir)
    if not output_dir.exists():
        return
    removed = 0
    for f in output_dir.iterdir():
        if f.is_file():
            f.unlink()
            removed += 1
    if removed:
        print(f"  Cleared {output_dir} ({removed} file(s) removed).")


def _get_partner_score_column(df):
    for col in ("scores", "score", "risk_score", "outlier_score_01"):
        if col in df.columns:
            return col
    return None


def _normalize_01(series):
    mn, mx = series.min(), series.max()
    if mx <= mn:
        return pd.Series(0.0, index=series.index)
    return (series - mn) / (mx - mn)


def _discover_score_files(ml_outputs_dir):
    """Return list of (path, ml_model) for each scores_[ml_model].csv in dir."""
    ml_outputs_dir = Path(ml_outputs_dir)
    if not ml_outputs_dir.exists():
        return []
    out = []
    for p in sorted(ml_outputs_dir.glob("scores_*.csv")):
        # scores_foo.csv -> ml_model = foo
        stem = p.stem
        if stem.startswith("scores_") and len(stem) > 7:
            ml_model = stem[7:]
            out.append((p, ml_model))
    return out


def main():
    cfg = load_config()
    paths = cfg["paths"]
    rb = cfg["rule_based"]
    fusion = cfg["fusion"]
    pred = cfg["predictions"]
    expl_cfg = cfg.get("explanations", {})

    input_path = paths["input_file"]
    rule_scores_path = paths["rule_scores"]
    output_dir = Path(paths["output_dir"])
    ml_outputs_dir = paths["ml_algorithms_outputs"]

    # Task 2 / task 3 output dirs if configured (paths are already resolved by load_config)
    task2_path = paths.get("task_2_model_outputs")
    task3_path = paths.get("task_3_model_outputs_explanations")

    # --- 0. Clear data/output and task_2 / task_3 dirs (re-created each run) ---
    print("Step 0: Clearing output directories...")
    _clear_output_dir(output_dir)
    if task2_path is not None:
        _clear_output_dir(task2_path)
    if task3_path is not None:
        _clear_output_dir(task3_path)

    # --- 1. Rule-based scorer (once) ---
    print("Step 1: Rule-based scorer...")
    run_rule_based_scorer(
        input_path=input_path,
        output_path=rule_scores_path,
        category_weights=rb["category_weights"],
        cluster_boost=rb.get("cluster_boost") or {},
    )
    print(f"  Wrote {rule_scores_path}")

    # --- 2. Discover partner score files ---
    score_files = _discover_score_files(ml_outputs_dir)
    if not score_files:
        print("Step 2: No scores_*.csv found in ml_algorithms/outputs/. Nothing to fuse.")
        print("  Add files named scores_[ml_model].csv to generate model_output_[ml_model].csv and explanations.")
        return

    print(f"Step 2: Found {len(score_files)} model score file(s). Fusing and generating explanations...")
    rule_df = pd.read_csv(rule_scores_path)
    rule_weight = fusion["rule_weight"]
    anomaly_weight = fusion.get("anomaly_weight", 0.3)
    normalize_partner = fusion.get("normalize_partner_score", True)
    top_pct = pred.get("top_percentile", 5)
    output_dir.mkdir(parents=True, exist_ok=True)
    if task2_path is not None:
        task2_path.mkdir(parents=True, exist_ok=True)
    if task3_path is not None:
        task3_path.mkdir(parents=True, exist_ok=True)
    model_output_paths_by_label = {}

    for partner_path, ml_model in score_files:
        # Fusion
        partner_df = pd.read_csv(partner_path)
        score_col = _get_partner_score_column(partner_df)
        if score_col is None:
            print(f"  {ml_model}: SKIP (no score column)")
            continue
        merged = rule_df.merge(partner_df[["customer_id", score_col]], on="customer_id", how="left")
        partner_score = merged[score_col].fillna(0.0)
        if normalize_partner:
            partner_score = _normalize_01(partner_score)
        risk_score = (
            rule_weight * rule_df["rule_based_score"].values
            + anomaly_weight * partner_score.values
        )
        risk_score = np.clip(risk_score, 0.0, 1.0)
        threshold = float(np.percentile(risk_score, 100 - top_pct))
        predicted_label = (risk_score >= threshold).astype(int)
        n_flagged = int(predicted_label.sum())

        model_output_path = output_dir / f"model_output_{ml_model}.csv"
        out = pd.DataFrame({
            "customer_id": rule_df["customer_id"],
            "predicted_label": predicted_label,
            "risk_score": np.round(risk_score, 4),
        })
        out.to_csv(model_output_path, index=False)
        model_output_paths_by_label[ml_model] = model_output_path
        if task2_path is not None:
            shutil.copy2(model_output_path, task2_path / model_output_path.name)

        # Explanations
        expl_path = output_dir / f"model_output_{ml_model}_explanations.csv"
        run_explanation_generator(
            model_output_path=model_output_path,
            rule_scores_path=rule_scores_path,
            output_path=expl_path,
            anomaly_scores_path=partner_path,
            max_length_chars=expl_cfg.get("max_length_chars", 2000),
            threshold=threshold,
            borderline_band=0.02,
        )
        if task3_path is not None:
            shutil.copy2(expl_path, task3_path / expl_path.name)
        print(f"  {ml_model}: {model_output_path.name} (threshold={threshold:.4f}, {n_flagged} flagged), {expl_path.name}")

    # --- 2b. Consistently flagged (by ALL models): customer list + explanations CSV ---
    if len(model_output_paths_by_label) >= 2:
        # Customers who are flagged (predicted_label==1) in every model
        flagged_sets = []
        for ml_model, mo_path in model_output_paths_by_label.items():
            mo = pd.read_csv(mo_path)
            flagged_sets.append(set(mo.loc[mo["predicted_label"] == 1, "customer_id"].astype(str)))
        consistently_flagged_ids = list(flagged_sets[0].intersection(*flagged_sets[1:]))
        consistently_flagged_ids.sort()

        # consistently_flagged_customers.csv: one column customer_id
        cust_path = output_dir / "consistently_flagged_customers.csv"
        pd.DataFrame({"customer_id": consistently_flagged_ids}).to_csv(cust_path, index=False)
        print(f"  Consistently flagged (all {len(model_output_paths_by_label)} models): {len(consistently_flagged_ids):,} customers -> {cust_path.name}")

        # consistently_flagged_explanations.csv: customer_id, model, explanation (one row per customer per model; explanations differ by model)
        expl_rows = []
        for ml_model in model_output_paths_by_label:
            expl_path = output_dir / f"model_output_{ml_model}_explanations.csv"
            if not expl_path.exists():
                continue
            expl_df = pd.read_csv(expl_path)
            expl_df["customer_id"] = expl_df["customer_id"].astype(str)
            for cid in consistently_flagged_ids:
                row = expl_df.loc[expl_df["customer_id"] == cid]
                if len(row):
                    expl_rows.append({
                        "customer_id": cid,
                        "model": ml_model,
                        "explanation": row["explanation"].iloc[0] if "explanation" in row.columns else "",
                    })
        if expl_rows:
            expl_out_path = output_dir / "consistently_flagged_explanations.csv"
            pd.DataFrame(expl_rows).to_csv(expl_out_path, index=False)
            print(f"  -> {expl_out_path.name} (customer_id, model, explanation)")

    # --- 3. PDF reports (one per model + comparison), optional ---
    reports_cfg = cfg.get("reports", {})
    if reports_cfg.get("generate_pdf", False):
        print("Step 3: PDF reports...")
        try:
            from scripts.pdf_reports import run_all_reports  # pylint: disable=import-error,wrong-import-position
            run_all_reports(output_dir, model_output_paths_by_label)
            for ml_model in model_output_paths_by_label:
                print(f"  model_report_{ml_model}.pdf")
            print(f"  model_comparison_report.pdf")
        except Exception as e:
            print(f"  Warning: Could not generate PDF reports ({e}). Install reportlab: pip install reportlab")
    else:
        print("Step 3: PDF reports skipped (generate_pdf: false).")

    print("Pipeline complete.")

    # --- 4. Launch explanation viewer (optional) ---
    viewer_cfg = cfg.get("viewer", {})
    if viewer_cfg.get("launch_after_run", False):
        print("Step 4: Launching explanation viewer...")
        try:
            from scripts.explanation_viewer_gui import main as launch_viewer  # pylint: disable=import-error
            launch_viewer(output_dir=output_dir)
        except Exception as e:
            print(f"  Warning: Could not launch viewer ({e}). Run: python scripts/explanation_viewer_gui.py")


if __name__ == "__main__":
    main()
