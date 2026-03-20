from flask import Blueprint, request, jsonify
from ml_models import nlp_resume_parser
from utils.job_data import JOB_DATA
import json

analysis = Blueprint('analysis', __name__)


@analysis.route('/api/analyze', methods=['POST'])
def analyze_api():
    payload = request.get_json() or {}
    # payload can contain: resume_path (optional), skills (list), role, company
    skills = set([s.strip().title() for s in payload.get('skills', []) if s and isinstance(s, str)])
    resume_path = payload.get('resume_path')
    role = payload.get('role')
    company = payload.get('company')

    # If resume provided, parse and merge skills
    if resume_path:
        parsed = nlp_resume_parser.parse_resume(resume_path)
        for s in parsed.get('skills', []):
            skills.add(s.title())

    # Enhanced AI Analysis with better algorithms
    analysis_result = perform_enhanced_analysis(skills, role, company)
    
    return jsonify(analysis_result)


def perform_enhanced_analysis(user_skills, target_role=None, target_company=None):
    """Enhanced AI analysis with improved scoring algorithms"""
    
    # Get required skills based on target role/company
    required_skills = get_required_skills(target_role, target_company)
    
    # Calculate skill matches and gaps
    matched_skills = list(required_skills.intersection(user_skills))
    missing_skills = list(required_skills.difference(user_skills))
    
    # Enhanced scoring algorithm
    career_fit_score = calculate_career_fit_score(user_skills, required_skills, matched_skills)
    skill_gap_index = calculate_skill_gap_index(missing_skills, required_skills)
    job_readiness = determine_job_readiness(career_fit_score, skill_gap_index)
    
    # Generate priority skills with importance scoring
    priority_skills = calculate_skill_priorities(missing_skills, target_role)
    
    # Generate personalized recommendations
    recommended_courses = generate_course_recommendations(missing_skills, target_role)
    suggested_companies = generate_company_recommendations(user_skills, matched_skills)
    
    # Market insights
    market_insights = generate_market_insights(target_role, missing_skills)
    
    # Learning path recommendations
    learning_path = generate_learning_path(user_skills, missing_skills, target_role)
    
    result = {
        'careerFitScore': career_fit_score,
        'skillGapIndex': skill_gap_index,
        'jobReadiness': job_readiness,
        'matchedSkills': matched_skills,
        'missingSkills': missing_skills,
        'prioritySkills': priority_skills,
        'recommendedCourses': recommended_courses,
        'suggestedCompanies': suggested_companies,
        'marketInsights': market_insights,
        'learningPath': learning_path,
        'visualData': {
            'matchPercent': career_fit_score,
            'gapPercent': 100 - career_fit_score,
            'topMissingSkills': priority_skills[:5],
            'skillProfile': generate_skill_profile(user_skills, required_skills),
            'progressData': generate_progress_data(user_skills)
        }
    }
    
    return result


def get_required_skills(target_role=None, target_company=None):
    """Get required skills based on target role/company"""
    required = set()
    
    for job in JOB_DATA:
        if target_role and job['role'].lower() == target_role.lower():
            required.update([s.title() for s in job['skills']])
        elif target_company and job['company'].lower() == target_company.lower():
            required.update([s.title() for s in job['skills']])
        elif not target_role and not target_company:
            # Aggregate all skills if no specific target
            required.update([s.title() for s in job['skills']])
    
    return required


def calculate_career_fit_score(user_skills, required_skills, matched_skills):
    """Enhanced career fit scoring algorithm"""
    if not required_skills:
        return 0
    
    # Base score from skill matches
    base_score = (len(matched_skills) / len(required_skills)) * 100
    
    # Bonus for having high-demand skills
    high_demand_skills = {'Python', 'SQL', 'Machine Learning', 'Data Analysis', 'Statistics'}
    bonus_skills = user_skills.intersection(high_demand_skills)
    bonus_score = len(bonus_skills) * 5  # 5 points per high-demand skill
    
    # Penalty for having too many missing critical skills
    critical_skills = {'Python', 'SQL', 'Communication', 'Problem Solving'}
    missing_critical = critical_skills.difference(user_skills)
    penalty = len(missing_critical) * 10  # 10 points penalty per missing critical skill
    
    final_score = min(100, max(0, base_score + bonus_score - penalty))
    return int(final_score)


def calculate_skill_gap_index(missing_skills, required_skills):
    """Calculate skill gap index (0-100, higher means more gaps)"""
    if not required_skills:
        return 0
    
    gap_percentage = (len(missing_skills) / len(required_skills)) * 100
    return int(gap_percentage)


def determine_job_readiness(career_fit_score, skill_gap_index):
    """Determine job readiness level"""
    if career_fit_score >= 80 and skill_gap_index <= 20:
        return 'Advanced'
    elif career_fit_score >= 60 and skill_gap_index <= 40:
        return 'Intermediate'
    elif career_fit_score >= 40:
        return 'Beginner'
    else:
        return 'Entry Level'


def calculate_skill_priorities(missing_skills, target_role):
    """Calculate skill priorities with importance scoring"""
    # Skill importance weights based on role
    skill_weights = {
        'Python': 10,
        'SQL': 9,
        'Machine Learning': 8,
        'Data Analysis': 8,
        'Statistics': 7,
        'Communication': 6,
        'Problem Solving': 6,
        'Data Visualization': 5,
        'Excel': 4,
        'R': 3
    }
    
    priorities = []
    for skill in missing_skills:
        importance = skill_weights.get(skill, 5)  # Default importance of 5
        priorities.append({
            'skill': skill,
            'importance': importance,
            'priority': 'High' if importance >= 8 else 'Medium' if importance >= 5 else 'Low'
        })
    
    # Sort by importance
    priorities.sort(key=lambda x: x['importance'], reverse=True)
    return priorities


def generate_course_recommendations(missing_skills, target_role):
    """Generate personalized course recommendations"""
    courses = []
    
    course_database = {
        'Python': {
            'name': 'Python for Data Science',
            'platform': 'Coursera',
            'duration': '4-6 weeks',
            'difficulty': 'Beginner',
            'rating': 4.8,
            'url': '#'
        },
        'SQL': {
            'name': 'SQL Fundamentals',
            'platform': 'Udemy',
            'duration': '2-3 weeks',
            'difficulty': 'Beginner',
            'rating': 4.7,
            'url': '#'
        },
        'Machine Learning': {
            'name': 'Machine Learning Specialization',
            'platform': 'Coursera',
            'duration': '8-10 weeks',
            'difficulty': 'Intermediate',
            'rating': 4.9,
            'url': '#'
        },
        'Data Analysis': {
            'name': 'Data Analysis with Python',
            'platform': 'NPTEL',
            'duration': '6-8 weeks',
            'difficulty': 'Intermediate',
            'rating': 4.6,
            'url': '#'
        },
        'Statistics': {
            'name': 'Statistics for Data Science',
            'platform': 'edX',
            'duration': '4-5 weeks',
            'difficulty': 'Beginner',
            'rating': 4.5,
            'url': '#'
        }
    }
    
    for skill in missing_skills[:5]:  # Top 5 missing skills
        if skill in course_database:
            course_info = course_database[skill].copy()
            course_info['targetSkill'] = skill
            courses.append(course_info)
    
    return courses


def generate_company_recommendations(user_skills, matched_skills):
    """Generate company recommendations based on skills"""
    companies = []
    
    # Company matching algorithm
    for job in JOB_DATA:
        job_skills = set(job['skills'])
        match_count = len(user_skills.intersection(job_skills))
        total_skills = len(job_skills)
        match_percentage = (match_count / total_skills) * 100 if total_skills > 0 else 0
        
        if match_percentage >= 50:  # Only recommend if 50%+ match
            companies.append({
                'company': job['company'],
                'role': job['role'],
                'matchPercentage': int(match_percentage),
                'matchedSkills': list(user_skills.intersection(job_skills)),
                'salary': '$50,000 - $80,000',
                'location': 'Remote/Hybrid'
            })
    
    # Sort by match percentage
    companies.sort(key=lambda x: x['matchPercentage'], reverse=True)
    return companies[:5]  # Top 5 recommendations


def generate_market_insights(target_role, missing_skills):
    """Generate market insights and trends"""
    insights = {
        'inDemandSkills': ['Python', 'SQL', 'Machine Learning', 'Data Analysis', 'Statistics'],
        'salaryRange': '$50,000 - $80,000',
        'growthRate': '15%',
        'topLocations': ['San Francisco', 'New York', 'Seattle', 'Austin'],
        'trendingSkills': ['AI/ML', 'Cloud Computing', 'Data Engineering', 'Automation'],
        'skillGapAnalysis': {
            'criticalGaps': missing_skills[:3],
            'emergingSkills': ['Deep Learning', 'Cloud Platforms', 'DevOps'],
            'softSkills': ['Communication', 'Leadership', 'Critical Thinking']
        }
    }
    return insights


def generate_learning_path(user_skills, missing_skills, target_role):
    """Generate personalized learning path"""
    learning_path = {
        'beginner': [],
        'intermediate': [],
        'advanced': []
    }
    
    # Categorize skills by difficulty
    beginner_skills = ['Excel', 'Basic SQL', 'Communication']
    intermediate_skills = ['Python', 'Data Analysis', 'Statistics']
    advanced_skills = ['Machine Learning', 'Deep Learning', 'AI/ML']
    
    for skill in missing_skills:
        if skill in beginner_skills:
            learning_path['beginner'].append(skill)
        elif skill in intermediate_skills:
            learning_path['intermediate'].append(skill)
        elif skill in advanced_skills:
            learning_path['advanced'].append(skill)
    
    return learning_path


def generate_skill_profile(user_skills, required_skills):
    """Generate skill profile for radar chart"""
    categories = {
        'Technical': ['Python', 'SQL', 'Machine Learning', 'Statistics'],
        'Analytical': ['Data Analysis', 'Problem Solving', 'Critical Thinking'],
        'Communication': ['Communication', 'Presentation', 'Writing'],
        'Tools': ['Excel', 'Power BI', 'Tableau', 'Git'],
        'Domain': ['Business Intelligence', 'Data Engineering', 'Research']
    }
    
    profile = {}
    for category, skills in categories.items():
        user_category_skills = user_skills.intersection(skills)
        required_category_skills = required_skills.intersection(skills)
        
        if required_category_skills:
            score = (len(user_category_skills) / len(required_category_skills)) * 10
        else:
            score = 5  # Neutral score if no requirements
        
        profile[category] = min(10, max(0, score))
    
    return profile


def generate_progress_data(user_skills):
    """Generate progress data for line chart"""
    # Simulate progress over time
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    progress = []
    
    base_skills = 2  # Starting skills
    for i, month in enumerate(months):
        if i == len(months) - 1:  # Current month
            progress.append(len(user_skills))
        else:
            # Simulate gradual growth
            growth = (len(user_skills) - base_skills) * (i + 1) / len(months)
            progress.append(int(base_skills + growth))
    
    return {
        'months': months,
        'progress': progress
    }
from flask import Blueprint, render_template
from utils.db import query_db

analysis_bp = Blueprint('analysis', __name__)

@analysis_bp.route('/analysis')
def skill_analysis():
    results = query_db("SELECT skills FROM resumes")
    return render_template('analysis.html', results=results)
