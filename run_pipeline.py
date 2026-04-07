"""
Run the AML detection pipeline from the AML_Submission directory.

Usage (from AML_Submission/):
  python run_pipeline.py

This runs the full pipeline (rule-based scorer, fusion, explanations, PDF reports)
and, if configured, launches the explanation viewer. Input must be in
aml_detection_pipeline/data/input/master_features_with_clustering.csv.

The pipeline config copies outputs into task_2_model_outputs/ and
task_3_model_outputs_explanations/ as soon as files are written (before the
viewer opens), so those directories are populated without waiting for the viewer to close.
"""

import sys
from pathlib import Path

SUBMISSION_ROOT = Path(__file__).resolve().parent
PIPELINE_ROOT = SUBMISSION_ROOT / "aml_detection_pipeline"
SCRIPT = PIPELINE_ROOT / "scripts" / "run_pipeline.py"

if not SCRIPT.exists():
    print(f"Error: Pipeline script not found at {SCRIPT}")
    sys.exit(1)

sys.path.insert(0, str(PIPELINE_ROOT))

import subprocess
result = subprocess.run(
    [sys.executable, str(SCRIPT)],
    cwd=str(PIPELINE_ROOT),
)
sys.exit(result.returncode)
