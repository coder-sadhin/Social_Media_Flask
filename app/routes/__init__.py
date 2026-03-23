from .main import main
from .user import user_bp
from .auth import auth

def register_blueprints(app):
    app.register_blueprint(main)
    app.register_blueprint(user_bp)
    app.register_blueprint(auth)