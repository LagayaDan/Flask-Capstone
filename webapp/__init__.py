"""Flask app factory."""
from flask import Flask
from flask_wtf import CSRFProtect
import os

from webapp import auth, routes


def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get("FLASK_SECRET_KEY", "capstone-payroll-portal-secret-key-change-me")

    # ---- CSRF protection ---------------------------------------------------
    csrf = CSRFProtect(app)

    # ---- Register blueprints -----------------------------------------------
    app.register_blueprint(auth.bp)
    app.register_blueprint(routes.dashboard_bp)
    app.register_blueprint(routes.timelog_bp)
    app.register_blueprint(routes.payslips_bp)

    return app
