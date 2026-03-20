from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from utils import db
import json
from utils.job_data import JOB_DATA

main = Blueprint('main', __name__)


# Home route
@main.route('/')
def home():
    return render_template("home.html")


# Dashboard route
@main.route('/dashboard')
def dashboard():
    if 'user' not in session:
        flash("Please login first!", "warning")
        return redirect(url_for('auth.login'))

    username = session['user']

    # Load the latest parsed resume for this user (if any)
    row = db.query_db('SELECT * FROM resumes WHERE username = ? ORDER BY id DESC', (username,), one=True)
    if row:
        try:
            user_skills = json.loads(row['skills']) if row['skills'] else []
        except Exception:
            user_skills = []
    else:
        user_skills = []

    show_analysis = bool(user_skills)
    gaps = []
    recommendations = []
    chart_data = {}
    suggested = []

    if show_analysis:
        # Aggregate required skills from JOB_DATA for role suggestions
        required_skills = set()
        role_scores = []  # for each job, compute match count
        for job in JOB_DATA:
            req = set(job['skills'])
            matched = req.intersection(set(user_skills))
            role_scores.append({
                'company': job['company'],
                'role': job['role'],
                'required': list(req),
                'matched': list(matched),
                'match_count': len(matched),
                'req_count': len(req)
            })
            required_skills.update(req)

        # Compute gaps (skills required by dataset but missing in user's skills)
        gaps = sorted(list(required_skills.difference(set(user_skills))))

        # Simple recommendations: top 6 missing skills
        recommendations = [f"Learn {g}" for g in gaps[:6]]

        # Prepare data for charts (matched vs gap)
        match_count = sum(r['match_count'] for r in role_scores)
        total_required = sum(r['req_count'] for r in role_scores)
        # avoid division by zero
        if total_required == 0:
            percent_matched = 0
        else:
            percent_matched = int((match_count / total_required) * 100)

        chart_data = {
            'matched': match_count,
            'gap': max(total_required - match_count, 0),
            'percent_matched': percent_matched,
            'top_missing': gaps[:6]
        }

        # Simple AI-based scoring (baseline heuristics)
        # Career Fit Score: normalized percent matched (0-100)
        career_fit_score = percent_matched

        # Skill Gap Index: proportion of missing skills among required (0-100)
        total_unique_required = len(required_skills) if required_skills else 0
        missing_count = len(gaps)
        if total_unique_required == 0:
            skill_gap_index = 0
        else:
            skill_gap_index = int((missing_count / total_unique_required) * 100)

        # Job readiness simple mapping
        if career_fit_score >= 75:
            readiness = 'Advanced'
        elif career_fit_score >= 40:
            readiness = 'Intermediate'
        else:
            readiness = 'Beginner'

        chart_data.update({
            'career_fit_score': career_fit_score,
            'skill_gap_index': skill_gap_index,
            'job_readiness': readiness
        })

        # Suggest top roles by match_count
        suggested = sorted(role_scores, key=lambda r: (-r['match_count'], r['req_count']))[:4]

    from utils.job_data import JOB_DATA as JD
    return render_template("dashboard.html",
                           username=username,
                           user_skills=user_skills,
                           gap=gaps,
                           recommendations=recommendations,
                           chart_data=chart_data,
                           suggested=suggested,
                           show_analysis=show_analysis,
                           job_data=JD)


# Add Skill route (kept for backward compatibility)
@main.route('/add_skill', methods=['POST'])
def add_skill():
    if 'user' not in session:
        flash("Please login first!", "warning")
        return redirect(url_for('auth.login'))

    skill = request.form.get('skill')
    username = session['user']

    # Persist skill by adding a resume-like record if no resume exists
    row = db.query_db('SELECT * FROM resumes WHERE username = ? ORDER BY id DESC', (username,), one=True)
    if row:
        try:
            skills = json.loads(row['skills']) if row['skills'] else []
        except Exception:
            skills = []
    else:
        skills = []

    if skill and skill not in skills:
        skills.append(skill)
        conn = db.get_db()
        cur = conn.cursor()
        # either update latest resume or insert a new one
        if row:
            cur.execute('UPDATE resumes SET skills = ? WHERE id = ?', (json.dumps(skills), row['id']))
        else:
            cur.execute('INSERT INTO resumes (username, filename, skills, education, experience) VALUES (?, ?, ?, ?, ?)',
                        (username, '', json.dumps(skills), '', ''))
        conn.commit()
        flash(f"Skill '{skill}' added successfully!", "success")
    else:
        flash(f"Skill '{skill}' already exists or is invalid!", "info")

    return redirect(url_for('main.dashboard'))


# About route
@main.route('/about')
def about():
    return render_template("about.html")


# Contact route (to prevent BuildError in base.html)
@main.route('/contact')
def contact():
    return render_template("contact.html")


# Jobs route
@main.route('/jobs')
def jobs():
    return render_template("jobs.html", job_data=JOB_DATA)


# Learning Path route
@main.route('/learning_path')
def learning_path():
    if 'user' not in session:
        flash("Please login first!", "warning")
        return redirect(url_for('auth.login'))
    
    # Get user's skills and generate learning path
    username = session['user']
    row = db.query_db('SELECT * FROM resumes WHERE username = ? ORDER BY id DESC', (username,), one=True)
    
    if row:
        try:
            user_skills = json.loads(row['skills']) if row['skills'] else []
        except Exception:
            user_skills = []
    else:
        user_skills = []
    
    # Generate learning recommendations based on user skills
    learning_recommendations = generate_learning_recommendations(user_skills)
    
    return render_template("learning_path.html", 
                         user_skills=user_skills,
                         recommendations=learning_recommendations)


# Profile route
@main.route('/profile')
def profile():
    if 'user' not in session:
        flash("Please login first!", "warning")
        return redirect(url_for('auth.login'))
    
    username = session['user']
    
    # Get user's profile data
    row = db.query_db('SELECT * FROM resumes WHERE username = ? ORDER BY id DESC', (username,), one=True)
    
    if row:
        try:
            user_skills = json.loads(row['skills']) if row['skills'] else []
            education = row['education'] if row['education'] else ''
            experience = row['experience'] if row['experience'] else ''
        except Exception:
            user_skills = []
            education = ''
            experience = ''
    else:
        user_skills = []
        education = ''
        experience = ''
    
    return render_template("profile.html", 
                         username=username,
                         user_skills=user_skills,
                         education=education,
                         experience=experience)


def generate_learning_recommendations(user_skills):
    """Generate personalized learning recommendations based on user skills"""
    all_skills = set()
    for job in JOB_DATA:
        all_skills.update(job['skills'])
    
    missing_skills = list(all_skills.difference(set(user_skills)))
    
    recommendations = []
    for skill in missing_skills[:5]:  # Top 5 missing skills
        if skill.lower() in ['python', 'sql', 'machine learning']:
            recommendations.append({
                'skill': skill,
                'course': f'{skill} for Beginners',
                'platform': 'Coursera',
                'duration': '4-6 weeks',
                'difficulty': 'Beginner'
            })
        elif skill.lower() in ['data visualization', 'statistics']:
            recommendations.append({
                'skill': skill,
                'course': f'Advanced {skill}',
                'platform': 'Udemy',
                'duration': '3-4 weeks',
                'difficulty': 'Intermediate'
            })
        else:
            recommendations.append({
                'skill': skill,
                'course': f'Master {skill}',
                'platform': 'NPTEL',
                'duration': '6-8 weeks',
                'difficulty': 'Advanced'
            })
    
    return recommendations