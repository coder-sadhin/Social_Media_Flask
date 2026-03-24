from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from app.models.user import User
from app import db
from app.utils.security import hash_password, check_password
from app.utils.token import verify_token
from app import limiter

auth = Blueprint("auth", __name__)


# start function for register
@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        existing = User.query.filter_by(email=email).first()
        if existing:
            flash("Email already exists")
            return redirect(url_for("auth.register"))

        user = User(
            name=name,
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

            remember = True if request.form.get("remember") else False

            login_user(user, remember=remember)
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

# start function for forget password for token
# @auth.route("/forgot-password", methods=["GET", "POST"])
# def forgot_password():
#     if request.method == "POST":
#         email = request.form["email"]

#         user = User.query.filter_by(email=email).first()

#         if user:
#             from app.services.email_service import send_reset_email
#             send_reset_email(user)

#         flash("If email exists, a reset link has been sent")

#     return render_template("auth/forgot_password.html")

# forget password for code
@auth.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form.get("email").lower().strip()
        user = User.query.filter_by(email=email).first()

        if user:
            try:
                from app.services.email_service import send_verification_code
                send_verification_code(user)
            except Exception as e:
                current_app.logger.error(f"Mail Error: {e}")
                # Don't tell the user the mail server is down, just say try again
                flash("An error occurred. Please try again later.", "danger")
                return redirect(url_for("auth.forgot_password"))

        if not user:
            session['reset_email'] = email
            session['temp_code'] = "NON-EXISTENT" 

        flash("If an account is associated with this email, a 4-digit code has been sent.", "info")
        return redirect(url_for("auth.verify_code"))
    return render_template("auth/forgot_password.html")

# function for verify code
@auth.route("/verify-code", methods=["GET", "POST"])
def verify_code():
    # ERROR HANDLING: Ensure the user actually has a reset process in progress
    if 'reset_email' not in session or 'temp_code' not in session:
        flash("Please enter your email to receive a code first.", "warning")
        return redirect(url_for("auth.forgot_password"))

    if request.method == "POST":
        # Combine the 4 input fields
        digits = [request.form.get(f"code{i}") for i in range(1, 5)]
        
        # Check if any digit is missing
        if None in digits or "" in digits:
            flash("Please enter all 4 digits.", "danger")
            return render_template("auth/verification_code.html")

        user_code = "".join(digits)
        
        if user_code == str(session.get('temp_code')):
            session['code_verified'] = True
            return redirect(url_for("auth.set_new_password"))
        
        flash("The code you entered is incorrect.", "danger")

    return render_template("auth/verification_code.html", email=session.get('reset_email'))

# function for resend code
@auth.route("/resend-code")
@limiter.limit("3 per hour") # Prevent spamming your email server
def resend_code():
    email = session.get('reset_email')
    if not email:
        flash("Session expired. Please start over.", "danger")
        return redirect(url_for("auth.forgot_password"))

    user = User.query.filter_by(email=email).first()
    if user:
        try:
            from app.services.email_service import send_verification_code
            send_verification_code(user)
            flash("A new code has been sent to your email.", "success")
        except Exception as e:
            current_app.logger.error(f"Resend failed: {e}")
            flash("Failed to resend email. Try again later.", "danger")
    else:
        # Even if user doesn't exist, we pretend we sent it for security
        flash("A new code has been sent if the account exists.", "success")

    return redirect(url_for("auth.verify_code"))


# @auth.route("/reset-password/<token>", methods=["GET", "POST"])
# def reset_password(token):
#     email = verify_token(token)

#     if not email:
#         flash("Invalid or expired token")
#         return redirect(url_for("auth.forgot_password"))

#     user = User.query.filter_by(email=email).first()

#     if request.method == "POST":
#         password = request.form["password"]

#         user.password_hash = hash_password(password)
#         db.session.commit()

#         flash("Password updated successfully")
#         return redirect(url_for("auth.login"))

#     return render_template("auth/reset_password.html")

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
