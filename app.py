import os
import sys

# Get absolute paths to handle different execution environments
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
INNER_PROJECT_DIR = os.path.join(THIS_DIR, 'SkillGapAnalysisProject')

# Add inner project directory to sys.path so its sub-packages
# (routes, utils, ml_models) can be imported
if INNER_PROJECT_DIR not in sys.path:
    sys.path.insert(0, INNER_PROJECT_DIR)

# Import the create_app factory from the inner SkillGapAnalysisProject/app.py
try:
    # Explicit absolute import if added to sys.path correctly
    from app import create_app
except ImportError:
    # Fallback to namespaced import
    from SkillGapAnalysisProject.app import create_app

# Create the application instance that Vercel looks for by default
app = create_app()

if __name__ == '__main__':
    # Local development server
    app.run(host='127.0.0.1', port=5001, debug=True)
