import os
import sys

# Get absolute paths to handle different execution environments
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
INNER_PROJECT_DIR = os.path.join(THIS_DIR, 'SkillGapAnalysisProject')

# Add inner project directory to sys.path so its sub-packages
# (routes, utils, ml_models) can be imported
if INNER_PROJECT_DIR not in sys.path:
    sys.path.insert(0, INNER_PROJECT_DIR)

# Import the uniquely named 'main_app' from the inner folder
# We renamed app.py to main_app.py to avoid 500 error name clash on Vercel
try:
    from main_app import create_app
except ImportError:
    # Fallback if package structure is needed
    try:
        from SkillGapAnalysisProject.main_app import create_app
    except ImportError:
        # One last try to find it
        sys.path.append(THIS_DIR)
        from SkillGapAnalysisProject.main_app import create_app

# Create the application instance that Vercel looks for by default
app = create_app()

if __name__ == '__main__':
    # Local development server
    app.run(host='127.0.0.1', port=5001, debug=True)
