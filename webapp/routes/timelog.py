"""Time-log route — shows only the logged-in employee's timelog records."""
from flask import Blueprint, render_template, session
from webapp.auth import login_required
from webapp.models import get_timelogs

timelog_bp = Blueprint("timelog", __name__)


@timelog_bp.route("/timelog")
@login_required
def index():
    rows = get_timelogs(session["employee_id"])
    return render_template("timelog.html", rows=rows)
