from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, User, bcrypt  # Import bcrypt from models.py
from flask_login import login_user

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)  # ✅ Log in the user
            flash("Login successful!", "success")
            return redirect(url_for("profile_bp.profile"))  # Use the correct Blueprint and function name
        else:
            flash("Invalid credentials, try again.", "danger")
    return render_template("login.html")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        employee_number = request.form["employee_number"]
        email = request.form["email"]
        password = request.form["password"]

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already registered. Please login.", "warning")
            return redirect(url_for("auth.login"))

        new_user = User(
            name=name,
            employee_number=employee_number,
            email=email,
        )
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html")
