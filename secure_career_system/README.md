# Secure Career System

This project is a Flask-based career guidance system with ML-backed career predictions, resume analysis, and counsellor features.

Quick setup (Windows):

1. Create and activate virtualenv:

```powershell
python -m venv .venv
& .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Create `.env` with keys:

- `SECRET_KEY`
- `MAIL_USERNAME`, `MAIL_PASSWORD`, `SENDER_EMAIL` (for OTP email)
- `DATABASE_URI` (optional, defaults to sqlite)
- `SECRET_FERNET_KEY` (32 url-safe base64 key for Fernet)

3. Train the model (optional):

```powershell
python train_model.py
```

4. Run the app:

```powershell
python app.py
```

Notes:
- This repository includes basic SHAP explainability endpoints, resume analyzer, and admin/counsellor flows.
- For production: configure real email provider, HTTPS reverse proxy, secret rotation, and virus scanning for uploads.
 
CI:
- A GitHub Actions workflow is included at `.github/workflows/ci.yml` which installs dependencies and runs `pytest` on pushes and pull requests to `main`.

Security & Production checklist:
- Use a managed email provider (SendGrid, SES) and store credentials in repository secrets.
- Add virus scanning for uploads (clamav or cloud provider file scan).
- Rotate `SECRET_FERNET_KEY` and `SECRET_KEY` securely and do not store them in the repo.
- Serve behind HTTPS / reverse proxy and configure `SESSION_COOKIE_SECURE`.

Database migrations:
- This project includes `Flask-Migrate`. Initialize migrations and create the first migration:

```powershell
set FLASK_APP=app.py
python -m flask db init
python -m flask db migrate -m "initial"
python -m flask db upgrade
```

Placement model:
- A simple placement model trainer is available at `placement_train.py`. Train and save the placement model with:

```powershell
python placement_train.py
```

The app will use `placement_model.pkl` and `placement_scaler.pkl` if present to compute placement probability.
