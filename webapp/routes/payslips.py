"""Payslips route — shows received payslips for the logged-in employee."""
from flask import Blueprint, render_template, session, Response
from webapp.auth import login_required
from webapp.models import get_payslips, get_payslip_pdf, mark_payslip_viewed

payslips_bp = Blueprint("payslips", __name__)


@payslips_bp.route("/payslips")
@login_required
def index():
    payslips = get_payslips(session["employee_id"])
    return render_template("payslips.html", payslips=payslips)


@payslips_bp.route("/payslips/<int:payslip_id>/view")
@login_required
def view(payslip_id):
    payslip = get_payslip_pdf(payslip_id, session["employee_id"])
    if payslip is None:
        return "Payslip not found", 404

    employee_name, period_start, period_end, pdf_data = payslip
    mark_payslip_viewed(payslip_id)

    return Response(pdf_data, mimetype="application/pdf")