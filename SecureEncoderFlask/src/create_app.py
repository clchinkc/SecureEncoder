from typing import Optional
from flask import Flask
from flask_cors import CORS
import os
import logging
from logging.handlers import RotatingFileHandler
from .md5_model import db
from .file_routes import file_bp
from .text_routes import text_bp
from decouple import config


def setup_logger(app: Flask) -> None:
    # Set the logging configuration
    logging.basicConfig(
        level=logging.DEBUG if app.debug else logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        filename="app.log",  # General app log file
        filemode="a",
    )

    # Setup for console output
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG if app.debug else logging.INFO)
    console_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console.setFormatter(console_formatter)
    logging.getLogger("").addHandler(console)

    # Adjust logger settings based on the debug mode
    level = logging.DEBUG if app.debug else logging.WARNING
    app.logger.setLevel(level)

    # File handler for production, with more limited logging
    if not app.debug:
        file_handler = RotatingFileHandler(
            "production.log", maxBytes=1024 * 1024 * 100, backupCount=10
        )
        file_handler.setLevel(logging.WARNING)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s: %(message)s")
        file_handler.setFormatter(formatter)
        app.logger.addHandler(file_handler)


def create_app(test_config: Optional[dict[str, any]] = None) -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    setup_logger(app)

    # Default configuration
    app.config.from_object(config("APP_SETTINGS"))
    app.config.from_mapping(UPLOAD_FOLDER=os.path.join(app.root_path, "keys"))

    if test_config is not None:
        # Load the test config if passed in
        app.config.update(test_config)

    # Initialize plugins
    db.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Register blueprints
    app.register_blueprint(file_bp)
    app.register_blueprint(text_bp)

    return app
