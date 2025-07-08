#!/usr/bin/env python3
"""Database initialization script."""

import sys
import os

# Add the parent directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask
from backend.config import settings
from backend.extensions import db, migrate
from backend.models.company import Company
from backend.api import api_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(settings)
    db.init_app(app)
    migrate.init_app(app, db)
    app.register_blueprint(api_bp, url_prefix="/api")
    return app

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("Database tables created successfully!")
