"""Entry point: python run.py"""
import os
from secure_career_system.app import app, db

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    debug = os.getenv('FLASK_DEBUG', '0') == '1'
    app.run(debug=debug)
