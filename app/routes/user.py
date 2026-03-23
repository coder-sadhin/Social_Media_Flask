from flask import Blueprint

user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route('/<name>')
def user(name):
    return f"Hello, {name}!"