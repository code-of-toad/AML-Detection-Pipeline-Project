"""
Create Directory Structure
Purpose: Set up the feature engineering directory structure
"""

from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent.parent

# Directories to create
directories = [
    BASE_DIR / 'features' / 'intermediate',
    BASE_DIR / 'features' / 'by_category',
    BASE_DIR / 'features' / 'final',
    BASE_DIR / 'scripts',
]

# Create directories
for directory in directories:
    directory.mkdir(parents=True, exist_ok=True)
    print(f"Created/verified: {directory}")

print("\nDirectory structure created successfully!")
