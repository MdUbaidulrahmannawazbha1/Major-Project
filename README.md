# Major-Project — Secure Career System

A Flask-based career guidance system with ML-backed career predictions, resume analysis, and counsellor features.

## Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure environment variables

Create a `.env` file inside `secure_career_system/` with the following keys:

```env
SECRET_KEY=your-secret-key
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-email-password
SENDER_EMAIL=your-email@gmail.com
# Optional – defaults to SQLite
DATABASE_URI=sqlite:///secure_career_system.db
# Generate with: python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
SECRET_FERNET_KEY=your-fernet-key
```

### 3. Run the application

```bash
python run.py
```

The app will be available at <http://127.0.0.1:5000>.

### 4. (Optional) Retrain the ML models

```bash
cd secure_career_system
python train_model.py      # career prediction model
python placement_train.py  # placement probability model
```

## Running tests

```bash
python -m pytest secure_career_system/tests/ -q
```

## Project structure

```
.
├── run.py                        # Application entry point
├── requirements.txt              # Python dependencies
├── secure_career_system/
│   ├── app.py                    # Flask application
│   ├── models.py                 # SQLAlchemy models
│   ├── extensions.py             # Flask extensions (db, login_manager, bcrypt)
│   ├── ai_service.py             # Groq AI integration
│   ├── resume_analyzer.py        # Resume PDF analysis
│   ├── train_model.py            # Career model training script
│   ├── placement_train.py        # Placement model training script
│   ├── requirements.txt          # Package requirements
│   ├── templates/                # Jinja2 HTML templates
│   └── tests/                   # Pytest test suite
```