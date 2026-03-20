# Top-level runner for convenience
# Allows running `python app.py` from the repo root.
import runpy
import os
import sys

THIS_DIR = os.path.dirname(__file__)
INNER_PROJECT_DIR = os.path.join(THIS_DIR, 'SkillGapAnalysisProject')
INNER_APP = os.path.join(INNER_PROJECT_DIR, 'app.py')

if __name__ == '__main__':
    # Add inner project directory to sys.path so relative imports inside
    # the inner app (e.g. `from utils import db`) succeed when running
    # from the repo root.
    if INNER_PROJECT_DIR not in sys.path:
        sys.path.insert(0, INNER_PROJECT_DIR)
    runpy.run_path(INNER_APP, run_name='__main__')
