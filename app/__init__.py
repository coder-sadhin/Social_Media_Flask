from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Initialize extensions (global)
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # disable cache

    # Load config
    app.config.from_object("config.Config")

    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)

    # Register all routes
    from .routes import register_blueprints
    register_blueprints(app)

    return app