"""
Isolation Forest: train on pipeline input, write scores_isolation_forest.csv to ml_algorithms/outputs/.

Reads master_features_with_clustering.csv (or given input_path), preprocesses numeric features,
trains Isolation Forest, outputs (customer_id, score) normalized to [0, 1] (higher = more anomalous).
Writes to ../outputs/scores_isolation_forest.csv and saves detector/scaler under artifacts/.

Usage:
  From model_isolation_forest: python run.py
  Or: python run.py --input ../../data/input/master_features_with_clustering.csv --output ../outputs/scores_isolation_forest.csv
"""

import argparse
import pickle
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

SCRIPT_DIR = Path(__file__).resolve().parent
ML_ALGORITHMS_ROOT = SCRIPT_DIR.parent
PIPELINE_ROOT = ML_ALGORITHMS_ROOT.parent
DEFAULT_INPUT = PIPELINE_ROOT / "data" / "input" / "master_features_with_clustering.csv"
DEFAULT_OUTPUT = ML_ALGORITHMS_ROOT / "outputs" / "scores_isolation_forest.csv"
DEFAULT_MODEL_DIR = SCRIPT_DIR / "artifacts"


def _select_features(features_df):
    numeric_cols = features_df.select_dtypes(include=[np.number]).columns.tolist()
    if "customer_id" in numeric_cols:
        numeric_cols.remove("customer_id")
    exclude = [
        "structuring_risk", "channel_risk", "geographic_risk",
        "behavioral_risk", "profile_risk", "rule_based_score", "cluster_risk",
    ]
    selected = [c for c in numeric_cols if not any(x in c.lower() for x in exclude)]
    return features_df[selected]


def _preprocess(features_df, scaler=None, fit_scaler=True):
    X = _select_features(features_df)
    X = X.fillna(X.median()).replace([np.inf, -np.inf], np.nan).fillna(X.median())
    if scaler is None:
        scaler = StandardScaler()
    if fit_scaler:
        X_scaled = scaler.fit_transform(X)
    else:
        X_scaled = scaler.transform(X)
    preprocessed = pd.DataFrame(X_scaled, columns=X.columns, index=X.index)
    return preprocessed, scaler


def _train(features_df, contamination=0.05, n_estimators=100, max_samples="auto", random_state=42):
    preprocessed, scaler = _preprocess(features_df, fit_scaler=True)
    detector = IsolationForest(
        contamination=contamination,
        n_estimators=n_estimators,
        max_samples=max_samples,
        random_state=random_state,
        n_jobs=-1,
    )
    detector.fit(preprocessed)
    return detector, scaler, preprocessed


def _predict(detector, scaler, features_df):
    preprocessed, _ = _preprocess(features_df, scaler=scaler, fit_scaler=False)
    raw = detector.score_samples(preprocessed)
    lo, hi = raw.min(), raw.max()
    if hi == lo:
        norm = np.full(len(raw), 0.5)
    else:
        norm = 1.0 - ((raw - lo) / (hi - lo))
    return pd.DataFrame({
        "customer_id": features_df["customer_id"].values,
        "score": np.round(norm, 4),
    })


def _save_model(detector, scaler, model_dir):
    model_dir = Path(model_dir)
    model_dir.mkdir(parents=True, exist_ok=True)
    with open(model_dir / "isolation_forest.pkl", "wb") as f:
        pickle.dump(detector, f)
    with open(model_dir / "scaler.pkl", "wb") as f:
        pickle.dump(scaler, f)


def run(input_path, output_path, model_dir, contamination=0.05, n_estimators=100, max_samples="auto", random_state=42):
    input_path = Path(input_path)
    output_path = Path(output_path)
    model_dir = Path(model_dir)
    if not input_path.exists():
        raise FileNotFoundError(f"Input not found: {input_path}")
    df = pd.read_csv(input_path)
    if "customer_id" not in df.columns:
        raise ValueError("Input must contain customer_id")
    detector, scaler, _ = _train(
        df, contamination=contamination, n_estimators=n_estimators, max_samples=max_samples, random_state=random_state
    )
    scores_df = _predict(detector, scaler, df)
    _save_model(detector, scaler, model_dir)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    scores_df.to_csv(output_path, index=False)
    return scores_df


def main():
    parser = argparse.ArgumentParser(description="Run Isolation Forest and write scores_isolation_forest.csv")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT, help="Pipeline input CSV")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="Output CSV path")
    parser.add_argument("--model-dir", type=Path, default=DEFAULT_MODEL_DIR, help="Directory to save detector/scaler")
    parser.add_argument("--contamination", type=float, default=0.05, help="Expected fraction of anomalies (0–0.5)")
    parser.add_argument("--n-estimators", type=int, default=100, help="Number of trees")
    parser.add_argument("--max-samples", default="auto", help="Samples per tree: 'auto', int, or float in (0,1)")
    parser.add_argument("--random-state", type=int, default=42)
    args = parser.parse_args()
    max_samples = args.max_samples
    if max_samples != "auto":
        try:
            max_samples = int(max_samples)
        except ValueError:
            max_samples = float(max_samples)
    run(
        input_path=args.input,
        output_path=args.output,
        model_dir=args.model_dir,
        contamination=args.contamination,
        n_estimators=args.n_estimators,
        max_samples=max_samples,
        random_state=args.random_state,
    )
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
