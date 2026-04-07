"""
Load pipeline config from config.yaml.
Paths are relative to the pipeline root; resolved to absolute Paths.
"""

import yaml
from pathlib import Path

CONFIG_DIR = Path(__file__).resolve().parent
PIPELINE_ROOT = CONFIG_DIR.parent
CONFIG_FILE = CONFIG_DIR / "config.yaml"


def load_config(pipeline_root=None):
    root = Path(pipeline_root) if pipeline_root else PIPELINE_ROOT
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    if "paths" in cfg:
        for key, value in cfg["paths"].items():
            if isinstance(value, str) and not value.startswith(("/", "\\")):
                cfg["paths"][key] = (root / value).resolve()
            else:
                cfg["paths"][key] = Path(value) if isinstance(value, str) else value

    return cfg
