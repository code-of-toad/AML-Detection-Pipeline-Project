"""
Task 3: Algorithmic explanation generator for AML detection pipeline v2.

Builds one non-technical explanation per customer from model_output, rule_based_scores,
and optional partner (anomaly) scores. Uses fixed red-flag phrases; optionally
mentions cluster label when cluster_risk > 0.
"""

from pathlib import Path

import numpy as np
import pandas as pd

CATEGORY_PHRASES = {
    "structuring_risk": "Activity suggestive of structuring or round-figure or just-below-threshold transactions (e.g. multiple transactions just below reporting thresholds, round amounts).",
    "channel_risk": "Use of higher-risk channels such as wire transfers, cash-intensive activity, or structured cash deposits.",
    "geographic_risk": "Cross-border or high-risk jurisdiction exposure (e.g. offshore structures, TBML-high-risk or shell-company jurisdictions).",
    "behavioral_risk": "Unusual account behaviour such as rapid turnover, flow-through activity, lifestyle mismatch, or sudden inflow/outflow patterns.",
    "profile_risk": "Higher-risk profile (e.g. MSB, cash-intensive business, shell company, new or very new account).",
    "cluster_risk": "Assignment to a higher-risk behavioural cluster (unusual channel or geographic mix, per clustering analysis).",
}
ANOMALY_PHRASE = "Behaviour is relatively unusual compared to the overall customer population."
BORDERLINE_PHRASE = "This customer is just below the review threshold; small changes in activity could place them in the review set."
NO_BREAKDOWN_PHRASE = "Detailed breakdown not available."
NO_RULE_INDICATORS_PHRASE = "No specific rule-based indicators above threshold; risk score is driven by overall population comparison."
CONTRIBUTING_HEADER = "Reasons contributing to the score:"

EPSILON = 1e-6
ANOMALY_HIGH_THRESHOLD = 0.5


def _build_explanation(row, threshold, borderline_band, max_length_chars, category_columns):
    risk_score = float(row["risk_score"])
    flagged = int(row["predicted_label"]) == 1
    outcome = "flagged" if flagged else "not flagged"
    parts = [f"This customer was {outcome} for review (top 5% by risk score). Overall risk score: {risk_score:.2f}."]

    bullets = []
    for col in category_columns:
        if col not in row.index or pd.isna(row[col]):
            continue
        score = float(row[col])
        if score <= EPSILON:
            continue
        phrase = CATEGORY_PHRASES.get(col)
        if phrase:
            bullets.append((score, phrase))

    bullets.sort(key=lambda x: -x[0])
    bullet_lines = [phrase for _, phrase in bullets]
    # When cluster_risk contributed, optionally add cluster label (string from Kmeans_Seperate)
    if "cluster_risk" in row.index and float(row.get("cluster_risk", 0)) > EPSILON and "cluster" in row.index and pd.notna(row.get("cluster")):
        cluster_val = str(row["cluster"]).strip()
        if cluster_val:
            bullet_lines.append(f"Customer is in cluster {cluster_val} (higher-risk segment).")

    if "anomaly_score" in row.index and pd.notna(row.get("anomaly_score")):
        a = float(row["anomaly_score"])
        if a >= ANOMALY_HIGH_THRESHOLD:
            bullet_lines.append(ANOMALY_PHRASE)

    if bullet_lines:
        parts.append("")
        parts.append(CONTRIBUTING_HEADER)
        for line in bullet_lines:
            parts.append("• " + line)
    else:
        if "rule_based_score" in row.index and pd.notna(row.get("rule_based_score")):
            parts.append("")
            parts.append(NO_RULE_INDICATORS_PHRASE)
        else:
            parts.append("")
            parts.append(NO_BREAKDOWN_PHRASE)

    if not flagged and threshold is not None and borderline_band > 0:
        if threshold - borderline_band <= risk_score < threshold:
            parts.append("")
            parts.append(BORDERLINE_PHRASE)

    text = "\n".join(parts)
    if len(text) > max_length_chars:
        text = text[: max_length_chars - len(" [truncated]")] + " [truncated]"
    return text


def run(
    model_output_path,
    rule_scores_path,
    output_path,
    anomaly_scores_path=None,
    max_length_chars=2000,
    threshold=None,
    borderline_band=0.02,
):
    model_output_path = Path(model_output_path)
    rule_scores_path = Path(rule_scores_path)
    output_path = Path(output_path)

    if not model_output_path.exists():
        raise FileNotFoundError(f"Model output not found: {model_output_path}")

    out = pd.read_csv(model_output_path)
    if "customer_id" not in out.columns or "risk_score" not in out.columns or "predicted_label" not in out.columns:
        raise ValueError("model_output must contain customer_id, predicted_label, risk_score")

    rule_df = pd.read_csv(rule_scores_path) if rule_scores_path.exists() else None
    if rule_df is not None:
        merged = out.merge(rule_df, on="customer_id", how="left", suffixes=("", "_rule"))
        to_drop = [c for c in merged.columns if c.endswith("_rule")]
        merged = merged.drop(columns=to_drop, errors="ignore")
    else:
        merged = out.copy()

    if anomaly_scores_path and Path(anomaly_scores_path).exists():
        anom = pd.read_csv(anomaly_scores_path)
        anom = anom.rename(columns={"scores": "anomaly_score"} if "scores" in anom.columns else {"score": "anomaly_score"})
        merged = merged.merge(anom[["customer_id", "anomaly_score"]], on="customer_id", how="left")
    else:
        merged["anomaly_score"] = np.nan

    category_columns = [c for c in CATEGORY_PHRASES if c in merged.columns]

    explanations = []
    for _, row in merged.iterrows():
        text = _build_explanation(
            row,
            threshold=threshold,
            borderline_band=borderline_band,
            max_length_chars=max_length_chars,
            category_columns=category_columns,
        )
        explanations.append(text)

    result = pd.DataFrame({"customer_id": merged["customer_id"], "explanation": explanations})
    output_path.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(output_path, index=False)
    return result
