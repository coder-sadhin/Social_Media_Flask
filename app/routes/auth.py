from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from app.models.user import User
from app import db
from app.utils.security import hash_password, check_password

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
@auth.route("/forget-password", methods=["GET", "POST"])
def forget_password():
    if request.method == "POST":
        email = request.form["email"]

        user = User.query.filter_by(email=email).first()
        if not user:
            flash("Email not found")
            return redirect(url_for("auth.forget_password"))

        # TODO: Send reset email (implement this part)
        flash("Password reset email sent")
        return redirect(url_for("auth.login"))

    return render_template("auth/forget_password.html")