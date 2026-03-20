from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from utils import db

auth = Blueprint('auth', __name__)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash("Passwords do not match!", "danger")
            return redirect(url_for('auth.register'))

        # Check if email already exists in DB
        existing = db.query_db('SELECT * FROM users WHERE email = ?', (email,), one=True)
        if existing:
            flash("Email already registered!", "danger")
            return redirect(url_for('auth.register'))

        # Insert user into DB with hashed password
        conn = db.get_db()
        cur = conn.cursor()
        cur.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                    (username, email, generate_password_hash(password)))
        conn.commit()

        flash("Registration successful! Please login.", "success")
        return redirect(url_for('auth.login'))

    return render_template('register.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        identifier = request.form.get('email') or request.form.get('identifier')
        password = request.form.get('password')

        # Try to find user by email or username
        user = db.query_db('SELECT * FROM users WHERE email = ? OR username = ?', (identifier, identifier), one=True)
        if user and check_password_hash(user['password'], password):
            session['user'] = user['username']
            flash(f"Welcome {user['username']}!", "success")
            return redirect(url_for('main.dashboard'))

        flash("Invalid credentials!", "danger")
        return redirect(url_for('auth.login'))

    return render_template('login.html')


@auth.route('/logout')
def logout():
    session.pop('user', None)
    flash("Logged out successfully.", "info")
    return redirect(url_for('auth.login'))
