import os
import sys
from flask import Flask

# Get absolute paths to handle different execution environments
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
INNER_PROJECT_DIR = os.path.join(THIS_DIR, 'SkillGapAnalysisProject')

# Add inner project directory to sys.path
if INNER_PROJECT_DIR not in sys.path:
    sys.path.insert(0, INNER_PROJECT_DIR)

# Import the factory from its new unique name to avoid circular import with this file
try:
    from main_app import create_app
except ImportError:
    # Error will be caught by Vercel if it persists
    raise RuntimeError(f"Could not find main_app.py in {INNER_PROJECT_DIR}")

# Create the application instance that Vercel looks for by default
app = create_app()

if __name__ == '__main__':
    # Local development server
    app.run(host='127.0.0.1', port=5001, debug=True)
