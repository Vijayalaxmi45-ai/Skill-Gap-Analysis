# AI Agent Instructions for Skill Gap Analysis Project

## Project Architecture

This is a Flask-based web application for analyzing skill gaps between user resumes and job requirements. Key components:

- **Routes (`/routes/`)**: Flask blueprints for different functionalities
  - `main.py`: Core application routes (dashboard, profile, learning path)
  - `auth.py`: Authentication flows
  - `upload_resume.py`: Resume upload and parsing

- **ML Models (`/ml_models/`)**: 
  - `nlp_resume_parser.py`: Lightweight resume text analysis
  - Skills matching uses simple keyword extraction against predefined vocabularies

- **Data Layer (`/utils/`)**: 
  - `db.py`: SQLite database interface
  - `job_data.py`: Job requirements reference data
  - Schema uses `resumes` table with columns: id, username, filename, skills (JSON), education, experience

## Key Patterns

1. **User Skills Storage**:
   - Skills are stored as JSON arrays in the `resumes` table
   - Example: `UPDATE resumes SET skills = ? WHERE id = ?`

2. **Skill Gap Analysis**:
   ```python
   # Pattern from main.py
   required_skills = set()
   for job in JOB_DATA:
       req = set(job['skills'])
       matched = req.intersection(set(user_skills))
   ```

3. **Database Access**:
   ```python
   from utils import db
   row = db.query_db('SELECT * FROM resumes WHERE username = ? ORDER BY id DESC', 
                     (username,), one=True)
   ```

## Development Workflow

1. **Environment Setup**:
   - Python virtual environment required
   - SQLite database initialization needed on first run
   - Static files served from `/static/` directory

2. **Database Operations**:
   - Uses SQLite with connection per request pattern
   - Always use parameterized queries via `db.query_db()`
   - JSON serialization required for skills arrays

## Integration Points

1. **Resume Parsing**: 
   - Plain text resumes supported via `nlp_resume_parser.py`
   - Skills extraction based on keyword matching against `JOB_DATA`

2. **Front-end Integration**:
   - Templates in `/templates/`
   - Chart data formatted in `dashboard()` route
   - JavaScript expects specific JSON structures for visualizations

## Maintenance Notes

- Keep `JOB_DATA` updated in `utils/job_data.py` for accurate matching
- Skills are case-sensitive in storage but case-insensitive in matching
- Dashboard metrics heavily depend on quality of skill extraction