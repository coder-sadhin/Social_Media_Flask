# from flask_mail import Message
# from app import mail
# from flask import url_for

# def send_reset_email(user):
#     from app.utils.token import generate_token

#     token = generate_token(user.email)

#     reset_url = url_for("auth.reset_password", token=token, _external=True)

#     msg = Message(
#         subject="Password Reset Request",
#         recipients=[user.email]
#     )

#     msg.body = f"""
#     To reset your password, click the link below:

#     {reset_url}

#     If you did not request this, ignore this email.
#     """

#     mail.send(msg)

import random
from flask_mail import Message
from flask import session, current_app, render_template
from app import mail

def send_verification_code(user):
    # Generate a random 4-digit code
    code = f"{random.randint(1000, 9999)}"
    
    # Store the code and email in the session to verify later
    session['temp_code'] = code
    session['reset_email'] = user.email

    msg = Message(
        subject="Your Verification Code",
        recipients=[user.email],
        sender=current_app.config.get('MAIL_USERNAME'),
    )
    msg.body = f"Your verification code is: {code}"


    msg.html = render_template(
        'emails/verify_code.html', 
        name=user.name, 
        otp_code=code
    )

    try:
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False