"""Authentication blueprint — login / logout endpoints."""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_wtf import FlaskForm
from functools import wraps
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from webapp.config import get_connection

bp = Blueprint("auth", __name__)


# ------------------------------- Form ---------------------------------------
class LoginForm(FlaskForm):
    name        = StringField("Username", validators=[DataRequired()])
    password    = PasswordField("Password", validators=[DataRequired()])
    submit      = SubmitField("Login")

SESSION_LIFETIME = 3600  # 1 hour in seconds


def login_required(view):
    """Decorator: redirect unauthenticated users back to the login page."""

    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if "name" not in session:
            flash("Please log in first.", "warning")
            return redirect(url_for("auth.login"))
        return view(*args, **kwargs)

    return wrapped_view


@bp.before_app_request
def refresh_session_lifetime():
    """Ping the session expiry on every request for logged-in users."""
    session.permanent = True


@bp.route("/", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.name.data.strip()
        pw       = form.password.data.strip()

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT name, department, password, employee_id FROM attendance WHERE name = %s",
            (username,),
        )
        row = cursor.fetchone()
        cursor.close()
        conn.close()

        if row and row[2] == pw:
            session["name"]         = row[0]
            session["department"]   = row[1]
            session["employee_id"]  = row[3]
            flash(f"Welcome back, {row[0]}!", "success")
            return redirect(url_for("dashboard.index"))

        flash("Invalid Username or password.", "danger")

    return render_template("login.html", form=form)


@bp.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))
