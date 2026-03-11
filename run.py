"""Entry point to run the Secure Career System Flask application."""
import os
import sys

# Ensure the repo root is on the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from secure_career_system.app import app, db

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=os.getenv('FLASK_DEBUG', '0') == '1')
