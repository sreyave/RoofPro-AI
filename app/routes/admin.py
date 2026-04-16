from flask import Blueprint, render_template, session, redirect, url_for
from functools import wraps
from app.services.lead_service import get_all_leads
import csv
from flask import Response


admin_bp = Blueprint("admin", __name__)

# 🔐 Login protection decorator
def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get("admin_logged_in"):
            return redirect(url_for("auth.login"))  # make sure auth.login exists
        return f(*args, **kwargs)
    return wrapper


# ---------------- DASHBOARD ----------------
@admin_bp.route("/dashboard")
@admin_required
def dashboard():
    leads = get_all_leads()
    total_leads = len(leads)

    return render_template("dashboard.html", total_leads=total_leads)


# ---------------- LEADS PAGE ----------------
@admin_bp.route("/leads")
@admin_required
def leads():
    leads = get_all_leads()

    return render_template("leads.html", leads=leads)

@admin_bp.route("/export-leads")
def export_leads():
    leads = get_all_leads()

    def generate():
        yield "Name,Phone,Issue\n"
        for lead in leads:
            yield f"{lead['Name']},{lead['Phone']},{lead['Issue']}\n"

    return Response(
        generate(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=leads.csv"}
    )

