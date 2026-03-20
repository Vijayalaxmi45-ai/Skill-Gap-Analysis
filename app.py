import os
import sys
import importlib.util

# Get absolute paths to handle different execution environments
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
INNER_PROJECT_DIR = os.path.join(THIS_DIR, 'SkillGapAnalysisProject')

# Add inner project directory to sys.path so its sub-packages
# (routes, utils, ml_models) can be imported
if INNER_PROJECT_DIR not in sys.path:
    sys.path.insert(0, INNER_PROJECT_DIR)

# Dynamically load the inner app.py to avoid name conflicts with the root app.py shim
inner_app_path = os.path.join(INNER_PROJECT_DIR, 'app.py')
spec = importlib.util.spec_from_file_location("inner_app", inner_app_path)
if spec and spec.loader:
    inner_app = importlib.util.module_from_spec(spec)
    # This allows 'from utils import db' to work inside the inner app
    sys.modules["inner_app"] = inner_app
    spec.loader.exec_module(inner_app)
    # Create the application instance that Vercel looks for by default
    app = inner_app.create_app()
else:
    raise ImportError(f"Could not load inner app.py at {inner_app_path}")

if __name__ == '__main__':
    # Local development server
    app.run(host='127.0.0.1', port=5001, debug=True)
