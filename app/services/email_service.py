from flask_mail import Message
from app import mail
from flask import url_for

def send_reset_email(user):
    from app.utils.token import generate_token

    token = generate_token(user.email)

    reset_url = url_for("auth.reset_password", token=token, _external=True)

    msg = Message(
        subject="Password Reset Request",
        recipients=[user.email]
    )

    msg.body = f"""
    To reset your password, click the link below:

    {reset_url}

    If you did not request this, ignore this email.
    """

    mail.send(msg)