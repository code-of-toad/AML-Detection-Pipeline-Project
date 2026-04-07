"""
Cluster-informed rule-based risk scorer for AML detection (pipeline v2).

Reads master_features_with_clustering.csv, applies 5-category red-flag rules
plus per-cluster uplift from a cluster label → amount map. Outputs rule_based_scores.csv with
customer_id, rule_based_score (0-1), category breakdown, cluster, cluster_risk.

Does not import config; receives input_path, output_path, and rule_based config from the runner.
"""

import pandas as pd
import numpy as np
from pathlib import Path

# ---------------------------------------------------------------------------
# Category 1: Structuring & Amount Patterns
# ---------------------------------------------------------------------------
STRUCTURING_FEATURES = {
    "just_below_threshold_count": {"threshold": 3, "weight": 0.15},
    "structuring_pattern_flag": {"threshold": 1, "weight": 0.20},
    "round_amount_pct": {"threshold": 0.5, "weight": 0.10},
    "round_amount_flag": {"threshold": 1, "weight": 0.10},
    "large_txn_count_10k": {"threshold": 5, "weight": 0.15},
    "large_txn_count_50k": {"threshold": 2, "weight": 0.20},
    "amount_near_50k_increment_count": {"threshold": 3, "weight": 0.10},
}

# ---------------------------------------------------------------------------
# Category 2: High-Risk Channels (optional ABM_cash_weight if column exists)
# ---------------------------------------------------------------------------
CHANNEL_FEATURES = {
    "has_wire_transfers": {"threshold": 1, "weight": 0.15},
    "wire_large_count": {"threshold": 2, "weight": 0.20},
    "wire_volume_total": {"threshold": 5_000_000, "weight": 0.15},
    "has_western_union": {"threshold": 1, "weight": 0.25},
    "abm_cash_txn_count": {"threshold": 10, "weight": 0.10},
    "abm_cash_large_count": {"threshold": 3, "weight": 0.15},
    "structured_cash_deposits_same_day": {"threshold": 1, "weight": 0.20},
    "multi_channel_flag": {"threshold": 1, "weight": 0.10},
    "ABM_cash_weight": {"threshold": 0.7, "weight": 0.15},
}

# ---------------------------------------------------------------------------
# Category 3: Geographic Risk
# ---------------------------------------------------------------------------
GEOGRAPHIC_FEATURES = {
    "cross_border_flag": {"threshold": 1, "weight": 0.15},
    "cross_border_txn_pct": {"threshold": 0.3, "weight": 0.20},
    "is_country_offshore_structure_jurisdiction": {"threshold": 1, "weight": 0.15},
    "is_country_tbml_high_risk": {"threshold": 1, "weight": 0.20},
    "is_country_shell_company_jurisdiction": {"threshold": 1, "weight": 0.15},
    "high_geographic_dispersion": {"threshold": 1, "weight": 0.15},
    "customer_country_offshore_structure_jurisdiction": {"threshold": 1, "weight": 0.10},
}

# ---------------------------------------------------------------------------
# Category 4: Behavioral (optional credit_share / credit_share_low if present)
# ---------------------------------------------------------------------------
BEHAVIORAL_FEATURES = {
    "lifestyle_mismatch": {"threshold": 1, "weight": 0.20},
    "severe_lifestyle_mismatch": {"threshold": 1, "weight": 0.30},
    "flow_through_velocity_hours": {"threshold": 24, "weight": 0.15, "comparison": "less_than"},
    "account_turnover_rate": {"threshold": 2.0, "weight": 0.15},
    "sudden_inflow_outflow_pattern": {"threshold": 1, "weight": 0.20},
    "volume_eft_sudden_increase": {"threshold": 1, "weight": 0.15},
    "rapid_fire_flag": {"threshold": 1, "weight": 0.10},
    "single_txn_exceeds_revenue": {"threshold": 1, "weight": 0.25},
    "credit_share": {"threshold": 0.9, "weight": 0.10},
    "credit_share_low": {"threshold": 0.05, "weight": 0.10, "comparison": "less_than", "column": "credit_share"},
}

# ---------------------------------------------------------------------------
# Category 5: Profile Risk
# ---------------------------------------------------------------------------
PROFILE_FEATURES = {
    "is_msb_business": {"threshold": 1, "weight": 0.25},
    "is_shell_company": {"threshold": 1, "weight": 0.25},
    "is_cash_intensive": {"threshold": 1, "weight": 0.15},
    "new_account_flag": {"threshold": 1, "weight": 0.10},
    "very_new_business_flag": {"threshold": 1, "weight": 0.15},
    "high_profile_risk": {"threshold": 1, "weight": 0.20},
    "has_missing_income": {"threshold": 1, "weight": 0.05},
    "has_missing_sales": {"threshold": 1, "weight": 0.05},
}


def _get_feature_config_without_optional(df_columns, base_config, optional_keys):
    out = {}
    for k, v in base_config.items():
        if k not in df_columns:
            if k in optional_keys:
                continue
        out[k] = v
    return out


def calculate_category_score(features_df, feature_config, category_weight):
    category_score = pd.Series(0.0, index=features_df.index, dtype=float)
    for feature_name, config in feature_config.items():
        col = config.get("column", feature_name)
        if col not in features_df.columns:
            continue
        vals = features_df[col].fillna(0)
        thresh = config["threshold"]
        w = config["weight"]
        cmp = config.get("comparison", "greater_equal")
        if cmp == "less_than":
            triggered = (vals < thresh).astype(float)
        else:
            triggered = (vals >= thresh).astype(float)
        category_score += triggered * w
    return category_score * category_weight


def apply_cluster_boost(risk_scores, cluster_series, cluster_boost):
    """
    cluster_boost: dict mapping cluster label (str) -> uplift amount.
    Unknown or empty labels get 0.
    """
    cluster_risk = pd.Series(0.0, index=risk_scores.index, dtype=float)
    if not cluster_boost:
        adjusted = (risk_scores + cluster_risk).clip(0.0, 1.0)
        return adjusted, cluster_risk
    boost_map = {str(k).strip(): float(v) for k, v in cluster_boost.items()}
    cluster_clean = cluster_series.dropna()
    for idx in cluster_clean.index:
        c = cluster_clean.loc[idx]
        c_str = str(c).strip() if pd.notna(c) else ""
        if not c_str:
            continue
        if c_str in boost_map:
            cluster_risk.loc[idx] = boost_map[c_str]
    adjusted = (risk_scores + cluster_risk).clip(0.0, 1.0)
    return adjusted, cluster_risk


def calculate_rule_based_risk(features_df, category_weights):
    idx = features_df.index
    risk_scores = pd.Series(0.0, index=idx, dtype=float)
    risk_details = pd.DataFrame(index=idx)
    channel_config = _get_feature_config_without_optional(
        features_df.columns, CHANNEL_FEATURES, optional_keys=["ABM_cash_weight"]
    )
    behavioral_config = _get_feature_config_without_optional(
        features_df.columns, BEHAVIORAL_FEATURES, optional_keys=["credit_share", "credit_share_low"]
    )
    if "credit_share" in features_df.columns and "credit_share_low" not in behavioral_config and "credit_share_low" in BEHAVIORAL_FEATURES:
        behavioral_config["credit_share_low"] = BEHAVIORAL_FEATURES["credit_share_low"]

    w_s = category_weights.get("structuring_amount", 0.25)
    s = calculate_category_score(features_df, STRUCTURING_FEATURES, w_s)
    risk_scores += s
    risk_details["structuring_risk"] = s.values
    w_c = category_weights.get("channel", 0.25)
    s = calculate_category_score(features_df, channel_config, w_c)
    risk_scores += s
    risk_details["channel_risk"] = s.values
    w_g = category_weights.get("geographic", 0.20)
    s = calculate_category_score(features_df, GEOGRAPHIC_FEATURES, w_g)
    risk_scores += s
    risk_details["geographic_risk"] = s.values
    w_b = category_weights.get("behavioral", 0.20)
    s = calculate_category_score(features_df, behavioral_config, w_b)
    risk_scores += s
    risk_details["behavioral_risk"] = s.values
    w_p = category_weights.get("profile", 0.10)
    s = calculate_category_score(features_df, PROFILE_FEATURES, w_p)
    risk_scores += s
    risk_details["profile_risk"] = s.values
    risk_scores = risk_scores.clip(0.0, 1.0)
    return risk_scores, risk_details


def run(
    input_path,
    output_path,
    category_weights,
    cluster_boost=None,
):
    """
    Run the rule-based scorer.
    input_path: Path to master_features_with_clustering.csv.
    cluster_boost: optional dict cluster label -> uplift (default none applied).
    """
    input_path = Path(input_path)
    output_path = Path(output_path)
    if not input_path.exists():
        raise FileNotFoundError(f"Input not found: {input_path}")
    df = pd.read_csv(input_path)
    if "customer_id" not in df.columns:
        raise ValueError("Input must contain customer_id")
    risk_scores, risk_details = calculate_rule_based_risk(df, category_weights)
    cluster_series = df["cluster"] if "cluster" in df.columns else pd.Series(index=df.index, dtype=float)
    risk_scores, cluster_risk_series = apply_cluster_boost(
        risk_scores, cluster_series, cluster_boost if cluster_boost is not None else {},
    )
    out = df[["customer_id"]].copy()
    out["rule_based_score"] = risk_scores.values
    out["structuring_risk"] = risk_details["structuring_risk"].values
    out["channel_risk"] = risk_details["channel_risk"].values
    out["geographic_risk"] = risk_details["geographic_risk"].values
    out["behavioral_risk"] = risk_details["behavioral_risk"].values
    out["profile_risk"] = risk_details["profile_risk"].values
    out["cluster_risk"] = cluster_risk_series.values
    if "cluster" in df.columns:
        out["cluster"] = df["cluster"].values
    float_cols = ["rule_based_score", "structuring_risk", "channel_risk", "geographic_risk", "behavioral_risk", "profile_risk", "cluster_risk"]
    out[float_cols] = out[float_cols].round(4)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(output_path, index=False)
    return out
