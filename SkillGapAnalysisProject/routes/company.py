from flask import Blueprint, render_template, request, redirect, flash, url_for
from utils.db import get_db

company_bp = Blueprint("company", __name__)

@company_bp.route("/requirements", methods=["GET"])
def company_requirements():
    return render_template("company_requirements.html")

@company_bp.route("/add_requirement", methods=["POST"])
def add_requirement():
    job_title = request.form["job_title"]
    skills = request.form["skills"]

    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO company_requirements (job_title, skills) VALUES (?, ?)",
        (job_title, skills),
    )
    db.commit()

    flash("Company requirement added successfully!")
    return redirect(url_for("dashboard"))
