from flask import Flask
from flask_cors import CORS
import os
import logging
from logging.handlers import RotatingFileHandler

from .md5_model import db

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    # Default configuration
    app.config.from_mapping(
        UPLOAD_FOLDER=os.path.join(app.root_path, 'keys'),
        ALLOWED_EXTENSIONS={'pem'},
        SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL', 'sqlite:///md5.db'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SECRET_KEY=os.urandom(24),
    )

    if test_config is not None:
        # Load the test config if passed in
        app.config.update(test_config)

    # Initialize plugins
    db.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Register your blueprints and routes here
    # app.register_blueprint(your_blueprint)

    return app

def setup_logger(app):
    if app.debug or os.getenv('FLASK_DEBUG') == '1':
        app.logger.setLevel(logging.DEBUG)
    else:
        app.logger.setLevel(logging.WARNING)

        # Create a file handler for production logs
        file_handler = RotatingFileHandler('production.log', maxBytes=1024 * 1024 * 100, backupCount=10)
        file_handler.setLevel(logging.WARNING)
        formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
        file_handler.setFormatter(formatter)
        app.logger.addHandler(file_handler)
