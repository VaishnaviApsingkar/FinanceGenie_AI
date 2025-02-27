from flask import Flask, redirect, url_for

from flask_migrate import Migrate
from sqlalchemy.exc import OperationalError
from sqlalchemy.sql import text  # Import the text function for raw SQL queries

import os
from config import Config
from flask_sqlalchemy import SQLAlchemy

from flask_login import LoginManager
from .models import User
from .models import db

login_manager = LoginManager()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    migrate.init_app(app, db)

    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # Redirect to login page if not authenticated

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))  # Load user by ID
    
    # Test database connection
    with app.app_context():
        try:
            db.session.execute(text("SELECT 1"))  # Execute a simple query to check connectivity
            print("Database connection successful!")
        except OperationalError as e:
            print(f"Failed to connect to the database: {e}")

    #code for AI agent
    # UPLOAD_FOLDER = './uploads'
    # os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    # app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['UPLOAD_FOLDER'] = './uploads'
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Register blueprints
    from .auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from .home import home_bp
    app.register_blueprint(home_bp, url_prefix='/home')

    # Define the default route
    @app.route('/')
    def index():
        return redirect(url_for('auth.login_page'))  # Correct usage

    return app


