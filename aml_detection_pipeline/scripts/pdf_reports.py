"""
Generate PDF reports in data/output: one per model (model_report_[ml_model].pdf)
and one comparison report (model_comparison_report.pdf).
Requires: reportlab, pandas.
"""

from pathlib import Path

import numpy as np
import pandas as pd

try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
    HAS_REPORTLAB = True
except ImportError:
    HAS_REPORTLAB = False


def _add_table(doc_story, data, col_widths=None):
    t = Table(data, colWidths=col_widths)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 9),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
        ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
        ("FONTSIZE", (0, 1), (-1, -1), 8),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    doc_story.append(t)
    doc_story.append(Spacer(1, 12))


def _add_insight(doc_story, text, styles):
    """Append a plain-English insight paragraph (slightly indented, normal style)."""
    doc_story.append(Paragraph(f"<i>Insight:</i> {text}", styles["Normal"]))
    doc_story.append(Spacer(1, 14))


def build_model_report(model_output_path, output_pdf_path):
    """Build model_report_[ml_model].pdf from model_output_[ml_model].csv."""
    if not HAS_REPORTLAB:
        raise RuntimeError("reportlab is required for PDF reports. Install with: pip install reportlab")
    df = pd.read_csv(model_output_path)
    if "customer_id" not in df.columns or "risk_score" not in df.columns or "predicted_label" not in df.columns:
        raise ValueError("CSV must have customer_id, risk_score, predicted_label")
    ml_model = model_output_path.stem.replace("model_output_", "")
    n_total = len(df)
    risk = df["risk_score"]
    flagged = df[df["predicted_label"] == 1]
    not_flagged = df[df["predicted_label"] == 0]
    n_flagged = len(flagged)
    pct_flagged = 100 * n_flagged / n_total if n_total else 0
    threshold = float(risk.quantile(1 - n_flagged / n_total)) if n_flagged else float("nan")
    bins = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.01]
    risk_bins = pd.cut(risk, bins=bins, right=False)
    bin_counts = risk_bins.value_counts().sort_index()
    iqr = float(risk.quantile(0.75) - risk.quantile(0.25))
    borderline_band = 0.02
    n_borderline = int(((risk >= threshold - borderline_band) & (risk < threshold)).sum()) if not np.isnan(threshold) else 0
    pct_high_band = 100 * (risk >= 0.5).sum() / n_total if n_total else 0

    doc = SimpleDocTemplate(
        str(output_pdf_path),
        pagesize=letter,
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=50,
    )
    styles = getSampleStyleSheet()
    story = []
    story.append(Paragraph(f"Model output report: {ml_model}", styles["Title"]))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"Summary of model_output_{ml_model}.csv (fusion of rule-based + {ml_model} scores).", styles["Normal"]))
    story.append(Spacer(1, 16))

    story.append(Paragraph("1. Overview", styles["Heading2"]))
    story.append(Spacer(1, 6))
    overview_data = [
        ["Item", "Value"],
        ["Total customers", f"{n_total:,}"],
        ["Flagged (top 5%)", f"{n_flagged:,} ({pct_flagged:.2f}%)"],
        ["Not flagged", f"{len(not_flagged):,}"],
        ["Effective threshold (risk_score ≥)", f"{threshold:.4f}"],
    ]
    _add_table(story, overview_data, col_widths=[220, 200])
    _add_insight(
        story,
        f"This model flags the top 5% of customers by combined risk score (rule-based plus {ml_model} anomaly score), "
        f"so {n_flagged:,} customers are marked for review. The threshold {threshold:.4f} is the minimum score needed to be in that top 5%. "
        "All flagged customers should be prioritised for further investigation; the rest of the population is below the cutoff.",
        styles,
    )

    story.append(Paragraph("2. Risk score distribution", styles["Heading2"]))
    story.append(Spacer(1, 6))
    dist_data = [
        ["Statistic", "All", "Flagged", "Not flagged"],
        ["Min", f"{risk.min():.4f}", f"{flagged['risk_score'].min():.4f}", f"{not_flagged['risk_score'].min():.4f}"],
        ["Max", f"{risk.max():.4f}", f"{flagged['risk_score'].max():.4f}", f"{not_flagged['risk_score'].max():.4f}"],
        ["Mean", f"{risk.mean():.4f}", f"{flagged['risk_score'].mean():.4f}", f"{not_flagged['risk_score'].mean():.4f}"],
    ]
    _add_table(story, dist_data)
    _add_insight(
        story,
        f"The spread of scores (min to max, and standard deviation) shows how much the model separates customers. "
        f"Flagged customers have higher mean and max scores than the rest; the gap between flagged and not-flagged means "
        f"indicates how distinct the high-risk group is. IQR (interquartile range) is {iqr:.3f}, so the middle 50% of scores "
        "span this range; a wider IQR suggests more variation in risk across the population.",
        styles,
    )

    story.append(Paragraph("3. Distribution by score band", styles["Heading2"]))
    story.append(Spacer(1, 6))
    band_data = [["Score band", "Count", "% of total"]]
    for interval in bin_counts.index.sort_values():
        cnt = bin_counts[interval]
        pct = 100 * cnt / n_total
        band_data.append([f"[{interval.left:.1f}, {interval.right:.1f})", f"{cnt:,}", f"{pct:.1f}%"])
    _add_table(story, band_data, col_widths=[120, 80, 100])
    _add_insight(
        story,
        f"Most customers fall in the lower score bands; only a small share have scores in the 0.5+ range ({pct_high_band:.1f}% here). "
        f"The top 5% flagged set sits at the right tail of this distribution. "
        f"If there are customers just below the threshold (within {borderline_band}), there are {n_borderline:,} in that borderline band—"
        "these may warrant monitoring as small changes in behaviour could push them into the review set.",
        styles,
    )

    story.append(Paragraph("4. How to use this output", styles["Heading2"]))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "Use the corresponding model_output_*.csv and model_output_*_explanations.csv for Task 2 and Task 3. "
        "The explanations file gives a plain-English reason for each customer's score; the report above summarises the overall "
        "distribution and helps you understand how this model's fusion (rule + anomaly) behaves across the population.",
        styles["Normal"],
    ))
    story.append(Spacer(1, 12))

    doc.build(story)


def build_comparison_report(model_output_paths_by_label, output_pdf_path):
    """Build model_comparison_report.pdf from multiple model_output_*.csv paths. """
    if not HAS_REPORTLAB:
        raise RuntimeError("reportlab is required for PDF reports. Install with: pip install reportlab")
    labels = list(model_output_paths_by_label.keys())
    frames = {}
    for label, path in model_output_paths_by_label.items():
        frames[label] = pd.read_csv(path)
    first = frames[labels[0]]
    customers = first["customer_id"].values
    n_total = len(customers)

    flag_cols = {}
    for label in labels:
        df = frames[label].set_index("customer_id")
        flag_cols[label] = df.reindex(customers)["predicted_label"].fillna(0).astype(int)
    flag_df = pd.DataFrame(flag_cols, index=customers)
    n_models = len(labels)
    n_models_flagged = flag_df.sum(axis=1)
    consistently_flagged = flag_df.index[n_models_flagged == n_models].tolist()
    n_consistent = len(consistently_flagged)

    doc = SimpleDocTemplate(
        str(output_pdf_path),
        pagesize=letter,
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=50,
    )
    styles = getSampleStyleSheet()
    story = []
    story.append(Paragraph("Comparison of all model outputs", styles["Title"]))
    story.append(Spacer(1, 12))
    story.append(Paragraph(
        f"Differences and similarities across the {n_models} fusion outputs (rule-based + partner score per model).",
        styles["Normal"],
    ))
    story.append(Spacer(1, 16))

    story.append(Paragraph("1. Summary per model", styles["Heading2"]))
    story.append(Spacer(1, 6))
    summary_data = [["Model", "Flagged count", "% of total", "Threshold (approx.)"]]
    for label in labels:
        df = frames[label]
        n_fl = int((df["predicted_label"] == 1).sum())
        pct = 100 * n_fl / n_total
        thresh = df["risk_score"].quantile(1 - n_fl / n_total) if n_fl else np.nan
        summary_data.append([label.replace("_", " "), f"{n_fl:,}", f"{pct:.2f}%", f"{thresh:.4f}"])
    _add_table(story, summary_data, col_widths=[120, 100, 80, 120])
    _add_insight(
        story,
        "Each row is one model (rule-based + that model's anomaly score). Flagged count is always the top 5% of customers for that model. "
        "Thresholds can differ because the partner scores (e.g. Isolation Forest vs LOF) have different scales and distributions; "
        "a higher threshold means the model needs a higher combined score to reach the top 5%. Comparing counts and thresholds "
        "shows which models are more or less conservative in practice.",
        styles,
    )

    story.append(Paragraph("2. Overlap: how many models flagged each customer", styles["Heading2"]))
    story.append(Spacer(1, 6))
    overlap_data = [["# models that flagged", "Customer count", "% of total"]]
    for k in range(1, n_models + 1):
        cnt = int((n_models_flagged == k).sum())
        pct = 100 * cnt / n_total
        overlap_data.append([str(k), f"{cnt:,}", f"{pct:.2f}%"])
    _add_table(story, overlap_data)
    _add_insight(
        story,
        f"Row 'k' is the number of customers flagged by exactly k models. Customers flagged by only one model are unique to that model's view of risk; "
        f"customers flagged by all {n_models} models are the strongest consensus alerts. "
        f"The distribution tells you how much the models agree: if most customers are in the '1' or '{n_models}' column, "
        "models tend to either disagree or fully agree; if many sit in the middle, there is partial overlap across model pairs.",
        styles,
    )

    story.append(Paragraph(f"3. Consistently flagged (by all {n_models} models)", styles["Heading2"]))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        f"Count: {n_consistent:,} customers were flagged by every model. These are the strongest candidates for review.",
        styles["Normal"],
    ))
    story.append(Spacer(1, 6))
    _add_insight(
        story,
        f"These {n_consistent:,} customers rank in the top 5% under every fusion (rule + each partner score). "
        "They should be prioritised first: the rule-based logic and every anomaly model agree they are high risk. "
        "Use the per-model explanation files to see why each was flagged; the reasons will often emphasise both rule-driven and anomaly-driven factors.",
        styles,
    )

    story.append(Paragraph("4. Pairwise overlap (customers flagged by both models)", styles["Heading2"]))
    story.append(Spacer(1, 6))
    header = [""] + [l.replace("_", " ")[:12] for l in labels]
    matrix_data = [header]
    for la in labels:
        row = [la.replace("_", " ")[:14]]
        for lb in labels:
            both = int(((flag_df[la] == 1) & (flag_df[lb] == 1)).sum())
            row.append(str(both))
        matrix_data.append(row)
    _add_table(story, matrix_data)
    _add_insight(
        story,
        "Each cell (A, B) is the number of customers flagged by both model A and model B. The diagonal is the total flagged per model. "
        "High off-diagonal values mean those two models often flag the same customers; lower values mean they focus on different subsets. "
        "Comparing pairs helps you see which models are most aligned (e.g. LOF variants vs Isolation Forest) and which add distinct signal.",
        styles,
    )

    story.append(Paragraph("5. Similarities and differences", styles["Heading2"]))
    story.append(Spacer(1, 6))
    story.append(Paragraph("<b>Similarities</b>", styles["Normal"]))
    story.append(Paragraph(
        "All outputs use the same rule-based score (weight 0.7) and the same top-5% rule; only the partner (anomaly) score (weight 0.3) changes per model. "
        f"The {n_consistent:,} consistently flagged customers are the core high-risk set on which all models agree and should be reviewed first. "
        "Flag counts are similar in size because each model flags 5% of the population; what changes is which customers make up that 5%.",
        styles["Normal"],
    ))
    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>Differences</b>", styles["Normal"]))
    story.append(Paragraph(
        "Each model uses a different anomaly or ML score (e.g. Isolation Forest vs LOF variants), so the combined risk score and the effective threshold differ. "
        "That is why some models have a higher or lower threshold: the scale of the partner score affects where the top 5% cutoff falls. "
        "Customers flagged by only one or two models are more model-specific; those flagged by four or all models are more robust candidates. "
        "Use the pairwise overlap table to see which model pairs agree most, and use the per-model reports to interpret each model's distribution in detail.",
        styles["Normal"],
    ))
    story.append(Spacer(1, 12))

    doc.build(story)


def run_all_reports(output_dir, model_output_paths_by_label):
    """
    output_dir: Path to data/output.
    model_output_paths_by_label: dict mapping ml_model -> Path to model_output_[ml_model].csv
    """
    output_dir = Path(output_dir)
    for ml_model, csv_path in model_output_paths_by_label.items():
        pdf_path = output_dir / f"model_report_{ml_model}.pdf"
        build_model_report(csv_path, pdf_path)
    comparison_path = output_dir / "model_comparison_report.pdf"
    build_comparison_report(model_output_paths_by_label, comparison_path)
    return list(model_output_paths_by_label.keys()) + ["comparison"]
