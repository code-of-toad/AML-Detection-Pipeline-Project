"""
Run the explanation viewer GUI by itself (from the AML_Submission directory).

Usage (from AML_Submission/):
  python run_viewer.py

Opens the viewer to browse model outputs and explanations in
aml_detection_pipeline/data/output/. Run the pipeline first so that
model_output_*_explanations.csv and model_output_*.csv exist.
"""

import sys
from pathlib import Path

SUBMISSION_ROOT = Path(__file__).resolve().parent
PIPELINE_ROOT = SUBMISSION_ROOT / "aml_detection_pipeline"
SCRIPT = PIPELINE_ROOT / "scripts" / "explanation_viewer_gui.py"

if not SCRIPT.exists():
    print(f"Error: Viewer script not found at {SCRIPT}")
    sys.exit(1)

import subprocess
result = subprocess.run(
    [sys.executable, str(SCRIPT)],
    cwd=str(PIPELINE_ROOT),
)
sys.exit(result.returncode)
