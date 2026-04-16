from flask import Blueprint, render_template, request, redirect, session, url_for

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/admin/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "1234":
            session["admin_logged_in"] = True
            return redirect(url_for("admin.dashboard"))

        return "Invalid credentials"

    return render_template("login.html")

@auth_bp.route("/admin/logout")
def logout():
    session.pop("admin_logged_in", None)
    return redirect(url_for("auth.login"))
