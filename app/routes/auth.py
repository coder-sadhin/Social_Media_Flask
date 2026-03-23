from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from app.models.user import User
from app import db
from app.utils.security import hash_password, check_password
from app.utils.token import verify_token

auth = Blueprint("auth", __name__)


# start function for register
@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        existing = User.query.filter_by(email=email).first()
        if existing:
            flash("Email already exists")
            return redirect(url_for("auth.register"))

        user = User(
            username=username,
            email=email,
            password_hash=hash_password(password)
        )

        db.session.add(user)
        db.session.commit()

        flash("Account created successfully")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")

# start function for login 
@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user and check_password(user.password_hash, password):
            login_user(user)
            return redirect(url_for("main.home"))

        flash("Invalid credentials")

    return render_template("auth/login.html")

# start function for logout
@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out")
    return redirect(url_for("auth.login"))

# start function for forget password
@auth.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form["email"]

        user = User.query.filter_by(email=email).first()

        if user:
            from app.services.email_service import send_reset_email
            send_reset_email(user)

        flash("If email exists, a reset link has been sent")

    return render_template("auth/forgot_password.html")

@auth.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    email = verify_token(token)

    if not email:
        flash("Invalid or expired token")
        return redirect(url_for("auth.forgot_password"))

    user = User.query.filter_by(email=email).first()

    if request.method == "POST":
        password = request.form["password"]

        user.password_hash = hash_password(password)
        db.session.commit()

        flash("Password updated successfully")
        return redirect(url_for("auth.login"))

    return render_template("auth/reset_password.html")

@auth.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():
    if request.method == "POST":
        current = request.form["current_password"]
        new = request.form["new_password"]
        confirm = request.form["confirm_password"]

        if not check_password(current_user.password_hash, current):
            flash("Wrong current password")
            return redirect(url_for("auth.change_password"))

        if new != confirm:
            flash("Passwords do not match")
            return redirect(url_for("auth.change_password"))

        current_user.password_hash = hash_password(new)
        db.session.commit()

        flash("Password changed successfully")
        return redirect(url_for("main.home"))

    return render_template("auth/change_password.html")
