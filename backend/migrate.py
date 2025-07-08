import os
import sys

# Add parent directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask
from backend.extensions import db, migrate
from backend.models.company import Company  # Import all models that need to be migrated

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/vatcrm.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    migrate.init_app(app, db)
    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        if not os.path.exists('migrations'):
            # If migrations folder doesn't exist, initialize migrations
            os.system('flask db init')
        os.system('flask db migrate -m "Add email, bank_details, and other fields to Company model"')
        os.system('flask db upgrade')
        print("Migration complete. Database schema updated.")
