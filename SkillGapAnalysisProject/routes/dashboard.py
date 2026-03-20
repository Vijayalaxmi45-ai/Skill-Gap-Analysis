from flask import Blueprint, render_template, session, redirect, url_for

dashboard = Blueprint("dashboard", __name__)

@dashboard.route("/skill-gap")
def skill_gap():
    if "user" not in session:
        return redirect(url_for("auth.login"))
    return render_template("dashboard.html", user=session["user"])
