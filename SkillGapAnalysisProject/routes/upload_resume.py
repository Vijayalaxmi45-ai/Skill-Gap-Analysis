from flask import Blueprint, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
import os
import json
from utils import db
from ml_models import nlp_resume_parser

upload = Blueprint('upload', __name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads', 'resumes')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@upload.route('/upload-resume', methods=['GET', 'POST'])
def upload_resume():
	if 'user' not in session:
		flash('Please login to upload a resume.', 'warning')
		return redirect(url_for('auth.login'))

	if request.method == 'POST':
		file = request.files.get('resume')
		if not file:
			flash('No file provided.', 'danger')
			return redirect(url_for('upload.upload_resume'))

		filename = secure_filename(file.filename)
		filepath = os.path.join(UPLOAD_FOLDER, filename)
		file.save(filepath)

		# Parse resume (returns skills, education, experience)
		parsed = nlp_resume_parser.parse_resume(filepath)

		# Persist parsed info in resumes table
		conn = db.get_db()
		cur = conn.cursor()
		cur.execute('INSERT INTO resumes (username, filename, skills, education, experience) VALUES (?, ?, ?, ?, ?)',
					(session['user'], filename, json.dumps(parsed.get('skills', [])), parsed.get('education', ''), parsed.get('experience', '')))
		conn.commit()

		flash('Resume uploaded and parsed successfully.', 'success')
		return redirect(url_for('main.dashboard'))

	# GET: show a minimal upload form
	return '''
	<h3>Upload Resume</h3>
	<form method="post" enctype="multipart/form-data">
	  <input type="file" name="resume" accept=".txt,.pdf,.doc,.docx" required>
	  <button type="submit">Upload</button>
	</form>
	'''
