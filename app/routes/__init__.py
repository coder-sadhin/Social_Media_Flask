from .main import main
from .user import user_bp
from .auth import auth
from .friend import friend

def register_blueprints(app):
    app.register_blueprint(main)
    app.register_blueprint(user_bp)
    app.register_blueprint(auth)
    app.register_blueprint(friend)