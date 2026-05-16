"""Data-access helpers — all queries are automatically scoped to the logged-in employee."""
from webapp.config import get_connection


def get_employee_info(employee_id):
    """Return one tuple from `attendance` for the given employee, or None."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT employee_id, name, department, actual_hours, "
        "late_minutes, overtime, absences "
        "FROM attendance WHERE employee_id = %s",
        (employee_id,),
    )
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row


def get_timelogs(employee_id):
    """Return ordered timelog rows for the given employee."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT date, week, time_in, time_out "
        "FROM timelogs WHERE employee_id = %s ORDER BY date",
        (employee_id,),
    )
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def get_payslips(employee_id):
    """Return all payslips for the logged-in employee."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, employee_name, period_start, period_end, sent_at, viewed "
        "FROM payslips WHERE employee_id = %s ORDER BY sent_at DESC",
        (employee_id,),
    )
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def get_payslip_pdf(payslip_id, employee_id):
    """Return PDF data for a specific payslip, verifying ownership."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT employee_name, period_start, period_end, pdf_data "
        "FROM payslips WHERE id = %s AND employee_id = %s",
        (payslip_id, employee_id),
    )
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row


def mark_payslip_viewed(payslip_id):
    """Mark a payslip as viewed."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE payslips SET viewed = TRUE WHERE id = %s",
        (payslip_id,),
    )
    conn.commit()
    cursor.close()
    conn.close()
