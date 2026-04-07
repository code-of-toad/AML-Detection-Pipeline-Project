"""
Explanation viewer GUI — runs as final step of AML Detection Pipeline v2.

Reads outputs from pipeline data/output. Supports multiple model outputs:
model_output_<label>_explanations.csv with matching model_output_<label>.csv; dropdown to switch.

Features: pagination, jump by customer ID, show only flagged, search, sort (ID / risk / flagged),
copy/save page, font size, dark/light theme, keyboard shortcuts, status bar.

Usage:
  From pipeline: launched automatically after run_pipeline.py (when launch_viewer: true in config).
  Standalone: python scripts/explanation_viewer_gui.py
  Or: python scripts/explanation_viewer_gui.py path/to/model_output_<label>_explanations.csv
"""

import sys
from pathlib import Path

# When run from pipeline scripts/: pipeline root is parent of scripts/
PIPELINE_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT_DIR = PIPELINE_ROOT / "data" / "output"

PER_PAGE_OPTIONS = [1, 5, 10, 20, 50, 100, 250, 500]
DEFAULT_PER_PAGE = 10
FONT_SIZES = {"Small": 9, "Medium": 10, "Large": 12}
DEFAULT_FONT_SIZE_NAME = "Large"
DEFAULT_THEME = "dark"
SORT_OPTIONS = [
    "Customer ID",
    "Risk score (high first)",
    "Risk score (low first)",
    "Flagged first, then risk",
]
THEMES = {
    "light": {
        "bg": "#f8fafc",
        "fg": "#1e293b",
        "insert": "#1e293b",
        "card": "#ffffff",
        "text_bg": "#ffffff",
        "input_bg": "#ffffff",
        "accent": "#2563eb",
        "muted": "#64748b",
        "border": "#e2e8f0",
    },
    "dark": {
        "bg": "#0f172a",
        "fg": "#e2e8f0",
        "insert": "#e2e8f0",
        "card": "#1e293b",
        "text_bg": "#1e293b",
        "input_bg": "#1e293b",
        "accent": "#60a5fa",
        "muted": "#94a3b8",
        "border": "#334155",
    },
}


def discover_output_labels(output_dir):
    """Find all model_output_*_explanations.csv in output_dir; return list of (label, path) sorted by label."""
    output_dir = Path(output_dir)
    found = []
    for p in output_dir.glob("model_output_*_explanations.csv"):
        stem = p.stem  # model_output_isolation_forest_explanations
        if stem.startswith("model_output_") and stem.endswith("_explanations"):
            label = stem[13:-13]  # isolation_forest
            found.append((label, p))
    return sorted(found, key=lambda x: x[0])


def load_data(explanations_path):
    """Load explanations CSV and optional model_output.csv; return merged DataFrame.
    If filename is model_output_<label>_explanations.csv, looks for model_output_<label>.csv for risk/flagged."""
    import pandas as pd
    path = Path(explanations_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    df = pd.read_csv(path)
    if "customer_id" not in df.columns or "explanation" not in df.columns:
        raise ValueError("CSV must have columns: customer_id, explanation")

    stem = path.stem
    if stem.startswith("model_output_") and stem.endswith("_explanations"):
        label = stem[13:-13]
        model_path = path.parent / f"model_output_{label}.csv"
    else:
        model_path = path.parent / "model_output.csv"

    if model_path.exists():
        mo = pd.read_csv(model_path)
        if "customer_id" in mo.columns and "risk_score" in mo.columns and "predicted_label" in mo.columns:
            df = df.merge(mo[["customer_id", "risk_score", "predicted_label"]], on="customer_id", how="left")
        else:
            df["risk_score"] = float("nan")
            df["predicted_label"] = -1
    else:
        df["risk_score"] = float("nan")
        df["predicted_label"] = -1

    return df


def main(output_dir=None):
    """Launch the explanation viewer. output_dir: optional Path; if None, use DEFAULT_OUTPUT_DIR or argv[1]."""
    import pandas as pd
    try:
        import tkinter as tk
        from tkinter import ttk, scrolledtext, filedialog, messagebox
    except ImportError:
        print("tkinter is required. On Linux install python3-tk.")
        sys.exit(1)

    if output_dir is not None:
        output_dir = Path(output_dir)
    elif len(sys.argv) > 1:
        csv_path = Path(sys.argv[1])
        output_dir = csv_path.parent
    else:
        output_dir = DEFAULT_OUTPUT_DIR

    available = discover_output_labels(output_dir)
    if available:
        csv_path = available[0][1]
    else:
        print(
            f"Error: no model_output_*_explanations.csv found in {output_dir}. "
            "Run the pipeline first to generate outputs."
        )
        sys.exit(1)

    if not csv_path.exists() and available:
        csv_path = available[0][1]
    if not csv_path.exists():
        print(f"Error: no explanations file found in {output_dir}")
        sys.exit(1)
    try:
        df = load_data(csv_path)
    except Exception as e:
        print(f"Error loading data: {e}")
        sys.exit(1)
    if not available:
        available = [(csv_path.stem.replace("model_output_", "").replace("_explanations", ""), csv_path)]
    labels_only = [x[0] for x in available]
    if available and csv_path.stem.startswith("model_output_") and csv_path.stem.endswith("_explanations"):
        initial_label = csv_path.stem[13:-13]
        if initial_label not in labels_only:
            initial_label = labels_only[0]
    else:
        initial_label = labels_only[0] if labels_only else ""

    has_model_output = "risk_score" in df.columns and df["risk_score"].notna().any()
    n_total_all = len(df)

    # Load set of customer_ids flagged by ALL models (for "Only consistently flagged" filter)
    consistently_flagged_ids = set()
    try:
        cf_path = output_dir / "consistently_flagged_customers.csv"
        if cf_path.exists():
            cf_df = pd.read_csv(cf_path)
            if "customer_id" in cf_df.columns:
                consistently_flagged_ids = set(cf_df["customer_id"].astype(str))
    except Exception:
        pass

    root = tk.Tk()
    root.title("AML Model Explanations Viewer — pipeline v2")
    root.geometry("980x720")
    root.minsize(720, 520)

    style = ttk.Style()
    if "clam" in style.theme_names():
        style.theme_use("clam")

    def apply_palette(theme_name="light"):
        c = THEMES.get(theme_name, THEMES["light"])
        root.configure(bg=c["bg"])
        style.configure("TFrame", background=c["bg"])
        style.configure("Card.TFrame", background=c["card"])
        style.configure(
            "TLabel",
            background=c["bg"],
            foreground=c["fg"],
            font=("Segoe UI", 10),
        )
        style.configure(
            "Header.TLabel",
            background=c["bg"],
            foreground=c["fg"],
            font=("Segoe UI", 14, "bold"),
        )
        style.configure(
            "Muted.TLabel",
            background=c["bg"],
            foreground=c["muted"],
            font=("Segoe UI", 9),
        )
        btn_bg = c["border"]
        btn_fg = c["fg"]
        style.configure(
            "TButton",
            background=btn_bg,
            foreground=btn_fg,
            font=("Segoe UI", 10),
            padding=(10, 4),
        )
        style.map(
            "TButton",
            background=[
                ("active", c["muted"]),
                ("pressed", c["accent"]),
                ("focus", btn_bg),
            ],
            foreground=[("pressed", "#ffffff" if theme_name == "light" else "#0f172a")],
        )
        input_bg = c.get("input_bg", c["card"])
        style.configure("TEntry", background=input_bg, fieldbackground=input_bg, foreground=c["fg"], padding=6)
        style.configure("TCombobox", background=input_bg, fieldbackground=input_bg, foreground=c["fg"], padding=6)
        style.map(
            "TEntry",
            fieldbackground=[("focus", input_bg), ("readonly", input_bg)],
            background=[("focus", input_bg)],
        )
        style.map(
            "TCombobox",
            fieldbackground=[("readonly", input_bg), ("focus", input_bg)],
            background=[("readonly", input_bg), ("focus", input_bg)],
        )
        style.configure(
            "TCheckbutton",
            background=c["bg"],
            foreground=c["fg"],
            font=("Segoe UI", 10),
            indicatorbackground=c["card"],
            indicatorforeground=c["accent"],
        )
        style.map(
            "TCheckbutton",
            background=[("active", c["bg"]), ("pressed", c["bg"]), ("selected", c["bg"])],
            foreground=[("active", c["fg"]), ("pressed", c["fg"]), ("selected", c["fg"])],
            indicatorbackground=[("active", c["card"]), ("pressed", c["card"]), ("selected", c["card"])],
            indicatorforeground=[("active", c["accent"]), ("pressed", c["accent"]), ("selected", c["accent"])],
        )
        style.configure("TStatus.TLabel", background=c["border"], foreground=c["muted"], font=("Segoe UI", 9), padding=6)

    per_page = tk.IntVar(value=DEFAULT_PER_PAGE)
    current_page = tk.IntVar(value=1)
    only_flagged = tk.BooleanVar(value=False)
    only_consistently_flagged = tk.BooleanVar(value=False)
    search_var = tk.StringVar(value="")
    sort_var = tk.StringVar(value=SORT_OPTIONS[0])
    font_var = tk.StringVar(value=DEFAULT_FONT_SIZE_NAME)
    theme_var = tk.StringVar(value=DEFAULT_THEME)

    view_df = df.copy()
    id_to_view_index = {}

    def rebuild_view():
        nonlocal view_df, id_to_view_index
        base = df.copy()
        if only_flagged.get() and has_model_output:
            base = base[base["predicted_label"] == 1].copy()
        if only_consistently_flagged.get() and consistently_flagged_ids:
            base["customer_id_str"] = base["customer_id"].astype(str)
            base = base[base["customer_id_str"].isin(consistently_flagged_ids)].drop(columns=["customer_id_str"])
        phrase = search_var.get().strip()
        if phrase:
            base = base[base["explanation"].astype(str).str.contains(phrase, case=False, na=False)]
        sort_choice = sort_var.get()
        if sort_choice == "Customer ID":
            base = base.sort_values("customer_id").reset_index(drop=True)
        elif sort_choice == "Risk score (high first)" and has_model_output:
            base = base.sort_values("risk_score", ascending=False).reset_index(drop=True)
        elif sort_choice == "Risk score (low first)" and has_model_output:
            base = base.sort_values("risk_score", ascending=True).reset_index(drop=True)
        elif sort_choice == "Flagged first, then risk" and has_model_output:
            base = base.sort_values(["predicted_label", "risk_score"], ascending=[False, False]).reset_index(drop=True)
        else:
            base = base.reset_index(drop=True)
        view_df = base
        id_to_view_index = {cid: i for i, cid in enumerate(view_df["customer_id"].astype(str))}

    def get_pp():
        try:
            pp = int(per_page.get())
            return pp if pp in PER_PAGE_OPTIONS else DEFAULT_PER_PAGE
        except (TypeError, ValueError):
            return DEFAULT_PER_PAGE

    def get_view_stats():
        n = len(view_df)
        pp = get_pp()
        max_p = max(1, (n + pp - 1) // pp)
        return n, pp, max_p

    main_container = ttk.Frame(root, padding=8)
    main_container.pack(fill=tk.BOTH, expand=True)

    header = ttk.Frame(main_container)
    header.pack(fill=tk.X, pady=(0, 6))
    ttk.Label(header, text="AML Explanations Viewer", style="Header.TLabel").pack(side=tk.LEFT)
    ttk.Label(header, text=f"  ·  {n_total_all:,} customers  ·  Source: pipeline data/output", style="Muted.TLabel").pack(side=tk.LEFT, padx=(4, 0))

    if len(labels_only) > 1:
        ttk.Label(header, text="  ·  Output:", style="Muted.TLabel").pack(side=tk.LEFT, padx=(12, 4))
        output_var = tk.StringVar(value=initial_label)
        last_loaded_output = [initial_label]

        output_combo = ttk.Combobox(
            header, textvariable=output_var, values=labels_only, width=16, state="readonly"
        )
        output_combo.pack(side=tk.LEFT, padx=2)

        def switch_output(event=None):
            nonlocal df, has_model_output, n_total_all
            label = output_var.get().strip()
            if not label or label not in labels_only:
                return
            if label == last_loaded_output[0]:
                return
            path = output_dir / f"model_output_{label}_explanations.csv"
            if not path.exists():
                return
            try:
                df = load_data(path)
            except Exception:
                return
            last_loaded_output[0] = label
            has_model_output = "risk_score" in df.columns and df["risk_score"].notna().any()
            n_total_all = len(df)
            total_label.config(text=f"{n_total_all:,}")
            rebuild_view()
            current_page.set(1)
            refresh_display()
            update_status_bar()

        output_combo.bind("<<ComboboxSelected>>", switch_output)
        output_var.trace_add("write", lambda *a: switch_output())

    ttk.Frame(header, width=1).pack(side=tk.LEFT, fill=tk.X, expand=True)

    top = ttk.Frame(main_container, padding=4)
    top.pack(fill=tk.X, pady=(0, 2))

    ttk.Label(top, text="Total:").pack(side=tk.LEFT, padx=(0, 4))
    total_label = ttk.Label(top, text=f"{n_total_all:,}")
    total_label.pack(side=tk.LEFT, padx=(0, 12))

    ttk.Button(top, text="Previous", command=lambda: _go_prev()).pack(side=tk.LEFT, padx=2)
    ttk.Button(top, text="Next", command=lambda: _go_next()).pack(side=tk.LEFT, padx=2)
    page_label = ttk.Label(top, text="")
    page_label.pack(side=tk.LEFT, padx=10)

    ttk.Label(top, text="Per page:").pack(side=tk.LEFT, padx=(8, 4))
    per_page_combo = ttk.Combobox(top, textvariable=per_page, values=PER_PAGE_OPTIONS, width=4, state="readonly")
    per_page_combo.pack(side=tk.LEFT, padx=2)
    per_page_combo.set(DEFAULT_PER_PAGE)

    ttk.Frame(top, width=1).pack(side=tk.LEFT, fill=tk.X, expand=True)

    def _go_prev():
        p = current_page.get()
        if p > 1:
            current_page.set(p - 1)
            refresh_display()

    def _go_next():
        n_view, pp, max_p = get_view_stats()
        p = current_page.get()
        if p < max_p:
            current_page.set(p + 1)
            refresh_display()

    def on_per_page_change(_=None):
        try:
            p = int(per_page.get())
            if p not in PER_PAGE_OPTIONS:
                return
            n_view, _, max_p = get_view_stats()
            if current_page.get() > max_p:
                current_page.set(max_p)
            refresh_display()
        except (TypeError, ValueError):
            pass

    per_page_combo.bind("<<ComboboxSelected>>", lambda e: on_per_page_change())
    per_page.trace_add("write", lambda *a: on_per_page_change())

    def on_sort_change():
        rebuild_view()
        current_page.set(1)
        refresh_display()
        update_status_bar()

    top2 = ttk.Frame(main_container, padding=4)
    top2.pack(fill=tk.X, pady=(0, 2))
    ttk.Label(top2, text="Sort:").pack(side=tk.LEFT, padx=(0, 4))
    sort_combo = ttk.Combobox(top2, textvariable=sort_var, values=SORT_OPTIONS, width=22, state="readonly")
    sort_combo.pack(side=tk.LEFT, padx=2)
    sort_combo.set(SORT_OPTIONS[0])
    sort_combo.bind("<<ComboboxSelected>>", lambda e: on_sort_change())

    ttk.Label(top2, text="Jump to ID:").pack(side=tk.LEFT, padx=(12, 4))
    jump_entry = ttk.Entry(top2, width=14)
    jump_entry.pack(side=tk.LEFT, padx=2)

    def jump_to_customer():
        cid = jump_entry.get().strip()
        if not cid:
            return
        rebuild_view()
        idx = id_to_view_index.get(cid)
        if idx is None:
            messagebox.showinfo("Not found", f"Customer ID '{cid}' not in current view.")
            return
        pp = get_pp()
        page = (idx // pp) + 1
        current_page.set(page)
        refresh_display()

    ttk.Button(top2, text="Go", command=jump_to_customer).pack(side=tk.LEFT, padx=(0, 8))
    jump_entry.bind("<Return>", lambda e: jump_to_customer())

    ttk.Label(top2, text="Go to page:").pack(side=tk.LEFT, padx=(8, 4))
    goto_page_entry = ttk.Entry(top2, width=5)
    goto_page_entry.pack(side=tk.LEFT, padx=2)

    def goto_page():
        try:
            p = int(goto_page_entry.get().strip())
            n_view, pp, max_p = get_view_stats()
            if 1 <= p <= max_p:
                current_page.set(p)
                refresh_display()
            else:
                messagebox.showinfo("Invalid", f"Page must be 1–{max_p}.")
        except ValueError:
            messagebox.showinfo("Invalid", "Enter a number.")

    ttk.Button(top2, text="Go", command=goto_page).pack(side=tk.LEFT, padx=(0, 8))
    goto_page_entry.bind("<Return>", lambda e: goto_page())
    ttk.Frame(top2, width=1).pack(side=tk.LEFT, fill=tk.X, expand=True)

    def on_filter_change():
        rebuild_view()
        current_page.set(1)
        refresh_display()
        update_status_bar()

    row2 = ttk.Frame(main_container, padding=4)
    row2.pack(fill=tk.X, pady=(0, 2))
    if has_model_output:
        only_flagged_cb = ttk.Checkbutton(row2, text="Show only flagged", variable=only_flagged, command=on_filter_change)
        only_flagged_cb.pack(side=tk.LEFT, padx=(0, 8))
    if consistently_flagged_ids:
        only_consistent_cb = ttk.Checkbutton(
            row2,
            text=f"Only consistently flagged (all models, n={len(consistently_flagged_ids):,})",
            variable=only_consistently_flagged,
            command=on_filter_change,
        )
        only_consistent_cb.pack(side=tk.LEFT, padx=(0, 8))

    ttk.Label(row2, text="Search:").pack(side=tk.LEFT, padx=(8, 4))
    search_entry = ttk.Entry(row2, width=14, textvariable=search_var)
    search_entry.pack(side=tk.LEFT, padx=2)
    search_after_id = [None]

    def do_search_refresh():
        search_after_id[0] = None
        rebuild_view()
        current_page.set(1)
        refresh_display()
        update_status_bar()

    def on_search():
        if search_after_id[0] is not None:
            root.after_cancel(search_after_id[0])
        do_search_refresh()

    def schedule_search_refresh(*args):
        if search_after_id[0] is not None:
            root.after_cancel(search_after_id[0])
        search_after_id[0] = root.after(400, do_search_refresh)

    search_entry.bind("<Return>", lambda e: on_search())
    search_var.trace_add("write", schedule_search_refresh)

    ttk.Button(row2, text="Search", command=on_search).pack(side=tk.LEFT, padx=2)
    ttk.Button(row2, text="Clear", command=lambda: _clear_search()).pack(side=tk.LEFT, padx=2)
    ttk.Frame(row2, width=1).pack(side=tk.LEFT, fill=tk.X, expand=True)

    def _clear_search():
        if search_after_id[0] is not None:
            root.after_cancel(search_after_id[0])
            search_after_id[0] = None
        search_var.set("")
        rebuild_view()
        current_page.set(1)
        refresh_display()
        update_status_bar()

    row3 = ttk.Frame(main_container, padding=4)
    row3.pack(fill=tk.X, pady=(0, 2))

    def copy_page():
        text_content = text.get(1.0, tk.END)
        root.clipboard_clear()
        root.clipboard_append(text_content)
        status_var.set("Current page copied to clipboard.")

    ttk.Button(row3, text="Copy page to clipboard", command=copy_page).pack(side=tk.LEFT, padx=(0, 8))

    def save_page():
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        )
        if path:
            text_content = text.get(1.0, tk.END)
            Path(path).write_text(text_content, encoding="utf-8")
            status_var.set(f"Saved to {path}")

    ttk.Button(row3, text="Save page as…", command=save_page).pack(side=tk.LEFT, padx=(0, 16))

    ttk.Label(row3, text="Font:").pack(side=tk.LEFT, padx=(8, 4))
    font_combo = ttk.Combobox(row3, textvariable=font_var, values=list(FONT_SIZES), width=8, state="readonly")
    font_combo.pack(side=tk.LEFT, padx=2)
    font_combo.set(DEFAULT_FONT_SIZE_NAME)
    font_combo.bind("<<ComboboxSelected>>", lambda e: apply_font())

    def apply_font():
        name = font_var.get()
        size = FONT_SIZES.get(name, 10)
        text.config(font=("Segoe UI", size))

    ttk.Label(row3, text="Theme:").pack(side=tk.LEFT, padx=(12, 4))
    theme_combo = ttk.Combobox(row3, textvariable=theme_var, values=list(THEMES), width=8, state="readonly")
    theme_combo.pack(side=tk.LEFT, padx=2)
    theme_combo.set(DEFAULT_THEME)
    theme_combo.bind("<<ComboboxSelected>>", lambda e: apply_theme())
    ttk.Frame(row3, width=1).pack(side=tk.LEFT, fill=tk.X, expand=True)

    def apply_theme():
        name = theme_var.get()
        apply_palette(name)
        colors = THEMES.get(name, THEMES["light"])
        text.config(
            bg=colors["text_bg"],
            fg=colors["fg"],
            insertbackground=colors["insert"],
            highlightbackground=colors["border"],
            highlightcolor=colors["accent"],
        )
        root.configure(bg=colors["bg"])

    text_frame = ttk.Frame(main_container, padding=0)
    text_frame.pack(fill=tk.BOTH, expand=True)

    _initial_font_size = FONT_SIZES.get(DEFAULT_FONT_SIZE_NAME, 12)
    _initial_theme = THEMES.get(DEFAULT_THEME, THEMES["dark"])
    text = scrolledtext.ScrolledText(
        text_frame,
        wrap=tk.WORD,
        font=("Segoe UI", _initial_font_size),
        state=tk.DISABLED,
        padx=14,
        pady=14,
        relief=tk.FLAT,
        borderwidth=0,
        highlightthickness=1,
        highlightbackground=_initial_theme["border"],
        highlightcolor=_initial_theme["accent"],
        bg=_initial_theme["text_bg"],
        fg=_initial_theme["fg"],
        insertbackground=_initial_theme["insert"],
    )
    text.pack(fill=tk.BOTH, expand=True)

    status_var = tk.StringVar(value="")
    status_bar = ttk.Label(root, textvariable=status_var, style="TStatus.TLabel", anchor=tk.W)
    status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def update_status_bar():
        n_view, pp, max_p = get_view_stats()
        page = current_page.get()
        start = (page - 1) * pp
        end = min(start + pp, n_view)
        parts = [f"Viewing {start + 1}–{end} of {n_view:,}"]
        if only_flagged.get() and has_model_output:
            parts.append("(flagged only)")
        if only_consistently_flagged.get() and consistently_flagged_ids:
            parts.append("(consistently flagged)")
        if search_var.get().strip():
            parts.append("(filtered by search)")
        status_var.set("  |  ".join(parts))

    def refresh_display():
        n_view, pp, max_p = get_view_stats()
        page = current_page.get()
        if page < 1:
            current_page.set(1)
            page = 1
        if page > max_p:
            current_page.set(max_p)
            page = max_p

        start = (page - 1) * pp
        end = min(start + pp, n_view)
        chunk = view_df.iloc[start:end]

        page_label.config(text=f"Page {page} of {max_p}  ({start + 1}–{end} of {n_view:,})")

        content = []
        for _, row in chunk.iterrows():
            cid = row["customer_id"]
            expl = row["explanation"]
            if pd.isna(expl):
                expl = "(No explanation)"
            else:
                expl = str(expl).strip()

            risk = row.get("risk_score")
            pred = row.get("predicted_label")
            if pd.notna(risk) and risk != "":
                risk_str = f"{float(risk):.2f}"
            else:
                risk_str = "—"
            flag_str = "Flagged" if (pred == 1) else "Not flagged"
            header = f"Customer ID: {cid}  ·  Risk score: {risk_str}  ·  {flag_str}"
            content.append(f"{'─' * 60}\n{header}\n{'─' * 60}\n\n{expl}\n\n")

        text.config(state=tk.NORMAL)
        text.delete(1.0, tk.END)
        text.insert(tk.END, "".join(content))
        text.config(state=tk.DISABLED)
        text.see(1.0)
        update_status_bar()

    def on_key(e):
        if e.keysym in ("Left", "Prior"):
            _go_prev()
        elif e.keysym in ("Right", "Next"):
            _go_next()
        elif e.state & 0x4 and e.keysym.lower() == "g":
            goto_page_entry.focus_set()

    root.bind("<Control-Left>", on_key)
    root.bind("<Control-Right>", on_key)
    root.bind("<Prior>", on_key)
    root.bind("<Next>", on_key)
    root.bind("<Control-g>", on_key)

    apply_palette(DEFAULT_THEME)
    apply_theme()
    rebuild_view()
    refresh_display()

    root.mainloop()


if __name__ == "__main__":
    main()
