"""Dashboard route — shows only the logged-in employee's summary."""
from flask import Blueprint, render_template, session
from webapp.auth import login_required, LoginForm
from webapp.models import get_employee_info

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard")
@login_required
def index():
    emp = get_employee_info(session["employee_id"])
    return render_template("dashboard.html", emp=emp, form=LoginForm())
