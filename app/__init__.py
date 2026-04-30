from flask import Flask, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user
from flask_mail import Mail

# Initialize extensions (global)
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
mail = Mail()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)

    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # disable cache

    # Load config
    app.config.from_object("config.Config")

    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    

    @login_manager.user_loader
    def load_user(user_id):
        from app.models.user import User
        return User.query.get(int(user_id))

    # Initialize mail with app
    mail.init_app(app)

    # Login manager config
    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "info"

    # Register all routes
    from .routes import register_blueprints
    register_blueprints(app)

    # --- THE SECURITY GUARD START ---
    @app.before_request
    def restrict_access():
        auth_routes = ['auth.login', 'auth.register', 'auth.forgot_password', 'auth.verify_code', 'auth.set_new_password', 'auth.resend_code']
        
        # 1. Skip check for static files (CSS, JS, Images)
        if request.endpoint == 'static':
            return

        # 2. If user is ALREADY logged in and tries to go to Login/Register
        if current_user.is_authenticated and request.endpoint in auth_routes:
            return redirect(url_for('main.feed')) # Redirect to their feed
            
    # --- THE SECURITY GUARD END ---

    return app
