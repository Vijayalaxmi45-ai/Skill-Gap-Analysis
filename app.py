import os
import sys
import traceback
from flask import Flask

# Initialize with a dummy app so the linter is happy and we have a fallback
app = Flask(__name__)
STARTUP_ERROR = None

# Get absolute paths to handle different execution environments
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
INNER_PROJECT_DIR = os.path.join(THIS_DIR, 'SkillGapAnalysisProject')

# Add inner project directory to sys.path
if INNER_PROJECT_DIR not in sys.path:
    sys.path.insert(0, INNER_PROJECT_DIR)

try:
    from main_app import create_app
    # Overwrite dummy app with real one
    app = create_app()
except Exception:
    STARTUP_ERROR = traceback.format_exc()

if STARTUP_ERROR:
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def catch_all(path):
        return f"<h1>Startup Error</h1><pre>{STARTUP_ERROR}</pre>", 500

# Add a debug route to check filesystem on Vercel
@app.route('/debug/ls')
def debug_ls():
    try:
        root_files = os.listdir('.')
        inner = 'SkillGapAnalysisProject'
        inner_files = os.listdir(inner) if os.path.exists(inner) else "Not Found"
        return f"Root: {root_files}<br>Inner: {inner_files}<br>CWD: {os.getcwd()}"
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    # Local development server
    app.run(host='127.0.0.1', port=5001, debug=True)
