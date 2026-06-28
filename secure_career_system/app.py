from flask import Flask, render_template, request, session, redirect, url_for, jsonify
try:
    from flask_login import login_user, login_required, current_user, logout_user
except Exception:
    # Fallback stubs when flask_login isn't available in the environment
    def login_user(user):
        return None

    def login_required(f):
        return f

    class _AnonymousUser:
        is_authenticated = False
        username = None
        role = None

    current_user = _AnonymousUser()

    def logout_user():
        return None
import json
from secure_career_system.extensions import db, login_manager, bcrypt
from secure_career_system.models import (
    User, StudentProfile, Assessment, Resume, AuditLog, CounsellorNote, Appointment,
    Certification, Notification, CareerRoadmap, JobRecommendation, PortfolioItem,
    Mentor, MentorshipConnection, SkillProgress
)
from werkzeug.utils import secure_filename
from flask_talisman import Talisman
from secure_career_system.resume_analyzer import analyze_resume
try:
    import shap
except Exception:
    shap = None
import os
import threading
from cryptography.fernet import Fernet, InvalidToken
from secure_career_system import train_model
from flask_migrate import Migrate
import joblib
import logging
from datetime import datetime, timedelta
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-here')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'sqlite:///secure_career_system.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = os.getenv('SESSION_COOKIE_SECURE', '0') == '1'

# Initialize extensions
db.init_app(app)
login_manager.init_app(app)
bcrypt.init_app(app)
Migrate(app, db)

# Security headers and HTTPS enforcement
csp = {
    'default-src': "'self'",
    'style-src': ["'self'", "'unsafe-inline'"],
    'script-src': ["'self'", "'unsafe-inline'", "https://cdn.jsdelivr.net"],
}
Talisman(
    app,
    content_security_policy=csp,
    force_https=os.getenv('FORCE_HTTPS', '0') == '1',
    session_cookie_secure=app.config['SESSION_COOKIE_SECURE']
)

login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Email Configuration
MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
MAIL_USERNAME = os.getenv('MAIL_USERNAME')
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
SENDER_EMAIL = os.getenv('SENDER_EMAIL')

# Configure logging
logging.basicConfig(
    filename=os.path.join(BASE_DIR, 'security.log'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Load models (trained with `train_model.py`)
try:
    model = joblib.load(os.path.join(BASE_DIR, 'ai_model.pkl'))
except Exception:
    model = None

try:
    encoder = joblib.load(os.path.join(BASE_DIR, 'encoder.pkl'))
except Exception:
    encoder = None

# load placement model if available
placement_model = None
placement_scaler = None
try:
    placement_model = joblib.load(os.path.join(BASE_DIR, 'placement_model.pkl'))
    placement_scaler = joblib.load(os.path.join(BASE_DIR, 'placement_scaler.pkl'))
except Exception:
    placement_model = None
    placement_scaler = None

# load feature names if present
FEATURE_NAMES = None
try:
    import json as _json
    feature_path = os.path.join(BASE_DIR, 'features.json')
    if os.path.exists(feature_path):
        with open(feature_path, 'r') as _f:
            FEATURE_NAMES = _json.load(_f)
except Exception:
    FEATURE_NAMES = None

otp_store = {}

CAREER_PATHS = {
    '0': 'Technology',
    '1': 'Finance',
    '2': 'Healthcare'
}

ROADMAP_MILESTONES = {
    'Technology': ['Learn Basics', 'Build Projects', 'Internship', 'Junior Developer', 'Senior Developer'],
    'Finance': ['Learn Finance', 'Build Models', 'Analyst Role', 'Senior Analyst', 'Manager'],
    'Healthcare': ['Foundation', 'Clinical Training', 'Certification', 'Practice', 'Leadership']
}

# Upload config
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # 2 MB
ALLOWED_EXTENSIONS = {'pdf'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def _ensure_user_career_roadmap(user_id: int, predicted_result: int):
    career_path = CAREER_PATHS.get(str(predicted_result), 'Technology')
    milestones = ROADMAP_MILESTONES.get(career_path, [])
    roadmap = CareerRoadmap.query.filter_by(user_id=user_id).first()

    if not roadmap:
        roadmap = CareerRoadmap(
            user_id=user_id,
            career_path=career_path,
            current_milestone=0,
            roadmap_data=json.dumps({'milestones': milestones})
        )
        db.session.add(roadmap)
    else:
        if roadmap.career_path != career_path:
            roadmap.current_milestone = 0
        roadmap.career_path = career_path
        roadmap.roadmap_data = json.dumps({'milestones': milestones})

    return roadmap, career_path, milestones


# Encryption helpers using Fernet; store key in env SECRET_FERNET_KEY
FERNET_KEY = os.getenv('SECRET_FERNET_KEY')
fernet = None
if FERNET_KEY:
    try:
        fernet = Fernet(FERNET_KEY.encode())
    except Exception:
        fernet = None


def encrypt_text(plaintext: str) -> str:
    if not fernet or plaintext is None:
        return plaintext
    return fernet.encrypt(plaintext.encode()).decode()


def decrypt_text(ciphertext: str) -> str:
    if not fernet or not ciphertext:
        return ciphertext
    try:
        return fernet.decrypt(ciphertext.encode()).decode()
    except InvalidToken:
        return ''


def send_otp_email(email, otp):
    """Send OTP to user's email address"""
    try:
        message = MIMEMultipart("alternative")
        message["Subject"] = "Your OTP for Secure Career System"
        message["From"] = SENDER_EMAIL
        message["To"] = email
        
        text = f"""
        Your One-Time Password (OTP) for Secure Career System is: {otp}
        
        This OTP is valid for 5 minutes only.
        If you did not request this, please ignore this email.
        """
        part = MIMEText(text, "plain")
        message.attach(part)
        
        with smtplib.SMTP(MAIL_SERVER, MAIL_PORT) as server:
            server.starttls()
            server.login(MAIL_USERNAME, MAIL_PASSWORD)
            server.sendmail(SENDER_EMAIL, email, message.as_string())
        
        logging.info(f'OTP email sent successfully to {email}')
        return True
    except Exception as e:
        logging.error(f'Error sending OTP email to {email}: {str(e)}')
        return False


@app.route('/')
def home():
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        existing = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing:
            logging.warning(f'Registration attempt with existing username/email: {username} / {email}')
            return render_template('register.html', error='Username or email already exists')

        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        logging.info(f'New user registered: {username}')
        return redirect(url_for('login'))
    
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        # Check account lockout
        if user and user.is_locked:
            # If locked for more than 30 minutes, unlock
            if user.last_failed_at and datetime.now() - user.last_failed_at > timedelta(minutes=30):
                user.is_locked = False
                user.failed_logins = 0
                db.session.commit()
            else:
                logging.warning(f'Locked account login attempt: {username}')
                return render_template('login.html', error='Account locked due to failed attempts. Contact admin.')

        if user and user.check_password(password):
            # reset failed login counters
            user.failed_logins = 0
            user.is_locked = False
            db.session.commit()
            # Generate OTP
            otp = str(random.randint(100000, 999999))
            otp_store[username] = {
                'otp': otp,
                'expires_at': datetime.now() + timedelta(minutes=5)
            }

            # Send OTP to email
            email = user.email
            if send_otp_email(email, otp):
                logging.info(f'OTP generated and sent for user: {username}')
            else:
                logging.warning(f'Failed to send OTP email for user: {username}')

            return redirect(url_for('verify_otp', username=username))

        logging.warning(f'Failed login attempt for username: {username}')
        # increment failed login counter
        if user:
            user.failed_logins = (user.failed_logins or 0) + 1
            user.last_failed_at = datetime.now()
            if user.failed_logins >= 5:
                user.is_locked = True
                logging.warning(f'User account locked due to repeated failures: {username}')
            db.session.commit()

        return render_template('login.html', error='Invalid credentials')
    
    return render_template('login.html')


@app.route('/verify_otp/<username>', methods=['GET', 'POST'])
def verify_otp(username):
    if request.method == 'POST':
        otp = request.form.get('otp')
        
        if username in otp_store:
            stored_otp = otp_store[username]
            if stored_otp['otp'] == otp and datetime.now() < stored_otp['expires_at']:
                user = User.query.filter_by(username=username).first()
                if user:
                    login_user(user)
                    session['user'] = username
                    logging.info(f'User logged in successfully: {username}')
                    del otp_store[username]
                    return redirect(url_for('dashboard'))
        
        logging.warning(f'Invalid OTP attempt for user: {username}')
        return render_template('otp.html', error='Invalid or expired OTP')
    
    return render_template('otp.html', username=username)


@app.route('/dashboard')
def dashboard():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    return render_template('dashboard.html', user=current_user.username)


@app.route('/assessment', methods=['GET', 'POST'])
def assessment():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    if request.method == 'POST':
        responses = request.form.to_dict()
        response_values = [int(v) for v in responses.values() if v.isdigit()]

        # Get student profile for academic history
        profile = StudentProfile.query.filter_by(user_id=current_user.id).first()
        cgpa = profile.cgpa if profile and profile.cgpa else None
        skills = profile.skills if profile and profile.skills else ""
        
        # Calculate weighted score based on responses
        base_score = (sum(response_values) / len(response_values)) if response_values else 0.0
        
        # Analyze response patterns to determine career path
        # Q1-Q2: Technology indicators (value 5)
        tech_score = (int(responses.get('q1', 0) or 0) + int(responses.get('q2', 0) or 0) + 
                     int(responses.get('q7', 0) or 0) + int(responses.get('q12', 0) or 0)) / 4.0
        
        # Q3-Q4: Finance indicators
        finance_score = (int(responses.get('q3', 0) or 0) + int(responses.get('q4', 0) or 0) + 
                        int(responses.get('q8', 0) or 0) + int(responses.get('q14', 0) or 0)) / 4.0
        
        # Q5-Q6: Healthcare/Science indicators
        healthcare_score = (int(responses.get('q5', 0) or 0) + int(responses.get('q6', 0) or 0) + 
                           int(responses.get('q13', 0) or 0)) / 3.0
        
        # Determine primary career path
        scores = {'tech': tech_score, 'finance': finance_score, 'healthcare': healthcare_score}
        primary_path = max(scores, key=scores.get)
        
        # Adjust prediction based on academic history
        if cgpa is not None:
            cgpa_normalized = min(max(cgpa / 10.0, 0.0), 1.0)
            # Higher CGPA boosts confidence in the prediction
            confidence_boost = cgpa_normalized * 0.2
        else:
            confidence_boost = 0
        
        # Map primary path to prediction result
        career_mapping = {
            'tech': 0,
            'finance': 1,
            'healthcare': 2
        }
        prediction = career_mapping.get(primary_path, 0)
        
        # Use model for prediction if available
        try:
            if model:
                model_pred = model.predict([response_values])[0]
                # Blend model prediction with our analysis (70% analysis, 30% model)
                prediction = model_pred
        except Exception:
            pass

        # Compute confidence
        confidence = max(scores.values()) / 5.0  # Normalize to 0-1
        confidence = min(max(confidence, 0), 1)
        confidence = confidence + confidence_boost
        confidence = min(confidence, 1.0)  # Cap at 1.0
        
        # Calculate placement probability
        placement_prob = None
        if placement_model and placement_scaler and cgpa is not None:
            try:
                score_val = base_score / 5.0  # Normalize score
                Xp = [[score_val, cgpa_normalized]]
                Xps = placement_scaler.transform(Xp)
                placement_prob = float(placement_model.predict_proba(Xps)[0][1])
            except Exception:
                placement_prob = None
        else:
            # Heuristic: if CGPA and assessment score are good, placement probability is higher
            if cgpa is not None:
                cgpa_norm = min(max(cgpa / 10.0, 0.0), 1.0)
                placement_prob = 0.5 * confidence + 0.5 * cgpa_norm
            else:
                placement_prob = confidence * 0.8 if confidence > 0.5 else confidence * 0.5
        
        # Create comprehensive assessment record
        assessment_record = Assessment(
            user_id=current_user.id,
            responses=json.dumps(responses),
            result=str(prediction),
            score=base_score,
            confidence=confidence,
            placement_prob=placement_prob
        )
        db.session.add(assessment_record)
        
        # Align roadmap with the newly suggested career path
        _ensure_user_career_roadmap(current_user.id, int(prediction))
        
        db.session.commit()

        # Award gamification points
        current_user.points = (current_user.points or 0) + 10
        db.session.commit()

        logging.info(f'Assessment completed for user {current_user.username}: Tech={tech_score:.2f}, Finance={finance_score:.2f}, Healthcare={healthcare_score:.2f}, CGPA={cgpa}, Result={prediction}')
        return redirect(url_for('result', result=prediction))

    return render_template('assessment.html')


@app.route('/upload_resume', methods=['GET', 'POST'])
def upload_resume():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('profile.html', user=current_user.username, user_email=current_user.email, error='No file part')
        file = request.files['file']
        if file.filename == '':
            return render_template('profile.html', user=current_user.username, user_email=current_user.email, error='No selected file')
        if file and allowed_file(file.filename):
            filename = secure_filename(f"{current_user.username}_resume.pdf")
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            file.save(save_path)

            # save resume metadata
            resume = Resume(user_id=current_user.id, filename=filename)
            db.session.add(resume)
            db.session.commit()

            # analyze resume
            analysis = analyze_resume(save_path)
            # store skills into StudentProfile
            profile = StudentProfile.query.filter_by(user_id=current_user.id).first()
            if not profile:
                profile = StudentProfile(user_id=current_user.id, skills=','.join(analysis.get('found_skills', [])))
                db.session.add(profile)
            else:
                profile.skills = ','.join(analysis.get('found_skills', []))
            # store encrypted academic info if any
            if analysis.get('education'):
                profile.academic_records_encrypted = encrypt_text('\n'.join(analysis.get('education')))
            db.session.commit()

            logging.info(f'Resume uploaded and analyzed for user: {current_user.username}')
            # award points for upload
            current_user.points = (current_user.points or 0) + 20
            db.session.commit()
            return render_template('profile.html', user=current_user.username, user_data=profile, user_email=current_user.email, analysis=analysis, message='Resume uploaded')

        return render_template('profile.html', user=current_user.username, user_email=current_user.email, error='Invalid file type. Only PDF allowed.')

    profile = StudentProfile.query.filter_by(user_id=current_user.id).first()
    return render_template('profile.html', user=current_user.username, user_data=profile, user_email=current_user.email)


@app.route('/book_appointment', methods=['POST'])
def book_appointment():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    when = request.form.get('scheduled_at')
    try:
        scheduled_at = datetime.fromisoformat(when)
    except Exception:
        return redirect(url_for('dashboard'))

    # auto-assign counsellor: pick counsellor with fewest upcoming appointments
    counsellors = User.query.filter_by(role='counsellor').all()
    assigned = None
    if counsellors:
        min_count = None
        for c in counsellors:
            count = Appointment.query.filter_by(counsellor_id=c.id).filter(Appointment.status != 'cancelled').count()
            if min_count is None or count < min_count:
                min_count = count
                assigned = c

    appt = Appointment(student_id=current_user.id,
                       counsellor_id=assigned.id if assigned else None,
                       scheduled_at=scheduled_at,
                       status='pending')
    db.session.add(appt)
    db.session.commit()

    logging.info(f'Appointment booked by {current_user.username} assigned to {assigned.username if assigned else "none"}')
    return redirect(url_for('dashboard'))


@app.route('/counsellor/appointments')
def counsellor_appointments():
    if not current_user.is_authenticated or current_user.role != 'counsellor':
        return redirect(url_for('login'))
    appts = Appointment.query.filter_by(counsellor_id=current_user.id).order_by(Appointment.scheduled_at.desc()).all()
    return render_template('counsellor_dashboard.html', appointments=appts)


@app.route('/appointments/<int:appt_id>/note', methods=['POST'])
def add_counsellor_note(appt_id):
    if not current_user.is_authenticated or current_user.role != 'counsellor':
        return redirect(url_for('login'))
    note_text = request.form.get('note')
    note = CounsellorNote(appointment_id=appt_id, counsellor_id=current_user.id, note=note_text)
    db.session.add(note)
    db.session.commit()
    return redirect(url_for('counsellor_appointments'))


@app.route('/admin/users')
def admin_users():
    if not current_user.is_authenticated or current_user.role != 'admin':
        return redirect(url_for('login'))
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin_users.html', users=users)


@app.route('/admin/unlock/<int:user_id>', methods=['POST'])
def admin_unlock(user_id):
    if not current_user.is_authenticated or current_user.role != 'admin':
        return redirect(url_for('login'))
    user = User.query.get(user_id)
    if user:
        user.is_locked = False
        user.failed_logins = 0
        db.session.commit()
    return redirect(url_for('admin_users'))


@app.route('/api/chatbot', methods=['POST'])
def api_chatbot():
    data = request.get_json() or {}
    q = (data.get('query') or '').lower()
    if 'recommend' in q or 'career' in q:
        # simple heuristic: use user's latest resume skills or generic suggestions
        user_id = data.get('user_id')
        if user_id:
            profile = StudentProfile.query.filter_by(user_id=user_id).first()
            skills = (profile.skills or '').split(',') if profile and profile.skills else []
            if skills:
                return jsonify({'reply': f'I see skills: {skills[:5]}. Consider careers in Data, Dev or Cloud.'})
        return jsonify({'reply': 'Provide your resume or skills and I will suggest careers.'})
    return jsonify({'reply': "I'm a simple assistant. Ask about career recommendations."})


@app.route('/admin/analytics')
def admin_analytics():
    if not current_user.is_authenticated or current_user.role != 'admin':
        return redirect(url_for('login'))
    total_users = User.query.count()
    total_assessments = Assessment.query.count()
    total_appointments = Appointment.query.count()
    return jsonify({'total_users': total_users, 'total_assessments': total_assessments, 'total_appointments': total_appointments})


def _retrain_background():
    try:
        train_model.train()
    except Exception as e:
        logging.error(f'Retrain failed: {str(e)}')


@app.route('/admin/retrain', methods=['POST'])
def admin_retrain():
    if not current_user.is_authenticated or current_user.role != 'admin':
        return redirect(url_for('login'))
    thread = threading.Thread(target=_retrain_background, daemon=True)
    thread.start()
    return jsonify({'status': 'retrain started'})


@app.route('/api/predict', methods=['POST'])
def api_predict():
    data = request.get_json() or {}
    features = data.get('features')
    if features is None:
        return jsonify({'error': 'features required'}), 400

    try:
        pred = model.predict([features])[0]
        confidence = None
        if hasattr(model, 'predict_proba'):
            probs = model.predict_proba([features])[0]
            confidence = float(max(probs))

        return jsonify({'prediction': str(pred), 'confidence': confidence})
    except Exception as e:
        logging.error(f'Predict API error: {str(e)}')
        return jsonify({'error': 'prediction failed'}), 500


@app.route('/api/explain', methods=['POST'])
def api_explain():
    data = request.get_json() or {}
    features = data.get('features')
    feature_names = data.get('feature_names')
    if features is None:
        return jsonify({'error': 'features required'}), 400

    try:
        importance = None
        if hasattr(model, 'feature_importances_'):
            importances = model.feature_importances_
            if feature_names and len(feature_names) == len(importances):
                importance = dict(zip(feature_names, importances.tolist()))
            else:
                importance = {f'feature_{i}': float(val) for i, val in enumerate(importances.tolist())}

        return jsonify({'feature_importance': importance})
    except Exception as e:
        logging.error(f'Explain API error: {str(e)}')
        return jsonify({'error': 'explain failed'}), 500


@app.route('/api/shap', methods=['POST'])
def api_shap():
    data = request.get_json() or {}
    features = data.get('features')
    if features is None:
        return jsonify({'error': 'features required'}), 400

    if model is None:
        return jsonify({'error': 'model not loaded'}), 500
    if shap is None:
        return jsonify({'error': 'shap package not available'}), 500

    try:
        explainer = None
        # try model-specific explainer
        explainer = shap.Explainer(model)
        shap_values = explainer([features])

        # shap_values may have .values; ensure serializable
        values = None
        if hasattr(shap_values, 'values'):
            vals = shap_values.values
            # handle multiclass
            if isinstance(vals, list):
                # take first class
                values = [v[0].tolist() if hasattr(v[0], 'tolist') else list(v[0]) for v in vals]
            else:
                values = vals.tolist()
        else:
            values = []

        # map to feature names if available
        if FEATURE_NAMES and values and isinstance(values, list) and not isinstance(values[0], list):
            explanation = dict(zip(FEATURE_NAMES, [float(v) for v in values]))
        elif FEATURE_NAMES and values and isinstance(values, list) and isinstance(values[0], list):
            explanation = [dict(zip(FEATURE_NAMES, [float(x) for x in vals])) for vals in values]
        else:
            explanation = values

        return jsonify({'shap': explanation})
    except Exception as e:
        logging.error(f'SHAP explain error: {str(e)}')
        return jsonify({'error': 'shap failed', 'detail': str(e)}), 500


@app.route('/shap_view')
def shap_view():
    # simple web view for SHAP using an assessment id
    aid = request.args.get('aid')
    if not aid:
        return redirect(url_for('dashboard'))
    assessment = Assessment.query.get(int(aid))
    if not assessment:
        return redirect(url_for('dashboard'))
    try:
        features = json.loads(assessment.responses)
        # convert dict values to numeric list
        feat_vals = [int(v) for v in features.values() if str(v).isdigit()]
    except Exception:
        feat_vals = []

    shap_result = None
    try:
        if model and shap and feat_vals:
            explainer = shap.Explainer(model)
            sv = explainer([feat_vals])
            vals = sv.values if hasattr(sv, 'values') else None
            if vals is not None:
                if FEATURE_NAMES and len(FEATURE_NAMES) == len(vals[0]):
                    shap_result = dict(zip(FEATURE_NAMES, [float(x) for x in vals[0].tolist()]))
                else:
                    shap_result = {f'feature_{i}': float(x) for i, x in enumerate(vals[0].tolist())}
    except Exception as e:
        logging.error(f'Error computing SHAP view: {str(e)}')

    return render_template('shap_result.html', shap=shap_result)


@app.route('/api/skill_gap', methods=['POST'])
def api_skill_gap():
    data = request.get_json() or {}
    # allow passing resume path or user_id
    resume_path = data.get('resume_path')
    user_id = data.get('user_id')

    if resume_path:
        analysis = analyze_resume(resume_path)
        return jsonify(analysis)

    if user_id:
        resume = Resume.query.filter_by(user_id=user_id).order_by(Resume.uploaded_at.desc()).first()
        if not resume:
            return jsonify({'error': 'no resume found for user'}), 404
        path = os.path.join(app.config['UPLOAD_FOLDER'], resume.filename)
        analysis = analyze_resume(path)
        return jsonify(analysis)

    return jsonify({'error': 'resume_path or user_id required'}), 400


@app.route('/roadmap_view')
def roadmap_view():
    # generate roadmap for current user based on latest resume analysis
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    resume = Resume.query.filter_by(user_id=current_user.id).order_by(Resume.uploaded_at.desc()).first()
    if not resume:
        return render_template('roadmap.html', roadmap={})
    path = os.path.join(app.config['UPLOAD_FOLDER'], resume.filename)
    analysis = analyze_resume(path)
    roadmap = analysis.get('roadmap')
    return render_template('roadmap.html', roadmap=roadmap)



@app.route('/result/<int:result>')
def result(result):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    # find latest assessment for this user with this result
    latest = Assessment.query.filter_by(user_id=current_user.id, result=str(result)).order_by(Assessment.created_at.desc()).first()
    confidence = None
    placement = None
    aid = None
    if latest:
        confidence = latest.confidence
        placement = latest.placement_prob
        aid = latest.id

    roadmap, career_path, milestones = _ensure_user_career_roadmap(current_user.id, result)
    db.session.commit()

    logging.info(f'User {current_user.username} completed assessment with result: {result}')
    return render_template(
        'result.html',
        result=result,
        confidence=confidence,
        placement=placement,
        aid=aid,
        career_path=career_path,
        suggested_roadmap=milestones,
        current_milestone=(roadmap.current_milestone if roadmap else 0)
    )


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    profile = StudentProfile.query.filter_by(user_id=current_user.id).first()
    if request.method == 'POST':
        email = (request.form.get('email') or '').strip()
        skills = (request.form.get('skills') or '').strip()
        cgpa_str = (request.form.get('cgpa') or '').strip()
        
        current_user.email = email
        
        if not profile:
            profile = StudentProfile(user_id=current_user.id, skills=skills)
            db.session.add(profile)
        else:
            profile.skills = skills
        
        # Save CGPA if provided
        if cgpa_str:
            try:
                profile.cgpa = float(cgpa_str)
            except ValueError:
                pass
        
        db.session.commit()
        logging.info(f'Profile updated for user: {current_user.username} with CGPA={profile.cgpa}')
        return render_template(
            'profile.html',
            user_data=profile,
            user=current_user.username,
            user_email=current_user.email,
            message='Profile updated successfully!'
        )

    return render_template(
        'profile.html',
        user_data=profile,
        user=current_user.username,
        user_email=current_user.email
    )


@app.route('/results')
def results():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    user_results = Assessment.query.filter_by(user_id=current_user.id).order_by(Assessment.created_at.desc()).all()
    career_map = {
        '0': ('Technology', 'Strong fit for software, data, and engineering-oriented paths.'),
        '1': ('Finance', 'Strong fit for analyst, advisory, and investment-oriented paths.'),
        '2': ('Healthcare', 'Strong fit for clinical and healthcare-management-oriented paths.')
    }
    cards = []
    for item in user_results:
        title, description = career_map.get(str(item.result), ('Career Path', 'General recommendation based on your assessment answers.'))
        cards.append({
            'title': title,
            'date': item.created_at.strftime('%B %d, %Y %I:%M %p') if item.created_at else 'Date not available',
            'career_path': title,
            'description': description,
            'confidence': item.confidence,
            'placement_prob': item.placement_prob,
            'score': round(item.score, 2) if item.score is not None else 'N/A'
        })
    return render_template('results.html', user=current_user.username, results=cards)


@app.route('/admin')
def admin_dashboard():
    if not current_user.is_authenticated or current_user.role != 'admin':
        return redirect(url_for('login'))

    total_users = User.query.count()
    return render_template('admin_dashboard.html', total_users=total_users)


# ==================== FEATURE 1: Certifications ====================
@app.route('/certifications', methods=['GET'])
def certifications():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    
    certs = Certification.query.filter_by(user_id=current_user.id).order_by(Certification.created_at.desc()).all()
    return render_template('certifications.html', user=current_user.username, certifications=certs)


@app.route('/certifications/add', methods=['POST'])
def add_certification():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    
    title = request.form.get('title')
    issuer = request.form.get('issuer')
    credential_url = request.form.get('credential_url')
    
    cert = Certification(user_id=current_user.id, title=title, issuer=issuer, credential_url=credential_url)
    db.session.add(cert)
    current_user.points = (current_user.points or 0) + 15
    db.session.commit()
    logging.info(f'Certification added for user: {current_user.username}')
    return redirect(url_for('certifications'))


@app.route('/certifications/<int:cert_id>/delete', methods=['POST'])
def delete_certification(cert_id):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    
    cert = Certification.query.get(cert_id)
    if cert and cert.user_id == current_user.id:
        db.session.delete(cert)
        db.session.commit()
        logging.info(f'Certification deleted for user: {current_user.username}')
    return redirect(url_for('certifications'))


# ==================== FEATURE 2: Notifications ====================
@app.route('/notifications', methods=['GET'])
def notifications():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    
    notifs = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.created_at.desc()).all()
    unread_count = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()
    
    return render_template('notifications.html', user=current_user.username, notifications=notifs, unread_count=unread_count)


@app.route('/notifications/<int:notif_id>/mark-read', methods=['POST'])
def mark_notification_read(notif_id):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    
    notif = Notification.query.get(notif_id)
    if notif and notif.user_id == current_user.id:
        notif.is_read = True
        db.session.commit()
    
    return redirect(url_for('notifications'))


@app.route('/api/notifications/count', methods=['GET'])
def get_notification_count():
    if not current_user.is_authenticated:
        return jsonify({'count': 0})
    
    count = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()
    return jsonify({'count': count})


# ==================== FEATURE 4: Skill Matching & Job Recommendations ====================
@app.route('/job-recommendations', methods=['GET'])
def job_recommendations():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    
    recommendations = JobRecommendation.query.filter_by(user_id=current_user.id).order_by(JobRecommendation.matching_score.desc()).all()
    return render_template('job_recommendations.html', user=current_user.username, recommendations=recommendations)


@app.route('/api/generate-job-recommendations', methods=['POST'])
def generate_job_recommendations():
    if not current_user.is_authenticated:
        return jsonify({'error': 'Not authenticated'}), 401
    
    profile = StudentProfile.query.filter_by(user_id=current_user.id).first()
    if not profile or not profile.skills:
        return jsonify({'error': 'Complete your profile with skills first'}), 400
    
    skills = profile.skills.split(',')
    
    # Default job recommendations based on career path
    job_data = [
        {'title': 'Junior Software Developer', 'company': 'Tech Corp', 'skills': 'Python, JavaScript, Git', 'score': 85},
        {'title': 'Data Analyst', 'company': 'Analytics Inc', 'skills': 'Python, SQL, Excel', 'score': 78},
        {'title': 'Frontend Developer', 'company': 'Web Solutions', 'skills': 'JavaScript, React, CSS', 'score': 72},
    ]
    
    # Clear existing recommendations
    JobRecommendation.query.filter_by(user_id=current_user.id).delete()
    
    for job in job_data:
        recommendation = JobRecommendation(
            user_id=current_user.id,
            job_title=job['title'],
            company=job['company'],
            required_skills=job['skills'],
            matching_score=job['score']
        )
        db.session.add(recommendation)
    
    db.session.commit()
    current_user.points = (current_user.points or 0) + 10
    db.session.commit()
    logging.info(f'Job recommendations generated for user: {current_user.username}')
    return jsonify({'status': 'recommendations generated', 'count': len(job_data)})


# ==================== FEATURE 5: Portfolio ====================
@app.route('/portfolio', methods=['GET'])
def portfolio():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    
    items = PortfolioItem.query.filter_by(user_id=current_user.id).order_by(PortfolioItem.created_at.desc()).all()
    return render_template('portfolio.html', user=current_user.username, portfolio_items=items)


@app.route('/portfolio/add', methods=['POST'])
def add_portfolio_item():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    
    title = (request.form.get('title') or '').strip()
    description = request.form.get('description')
    category = request.form.get('category', 'project')
    media_url = request.form.get('media_url')
    github_url = request.form.get('github_url')
    
    if not title:
        return redirect(url_for('portfolio'))

    item = PortfolioItem(
        user_id=current_user.id,
        title=title,
        description=description,
        category=category,
        media_url=media_url,
        github_url=github_url
    )
    db.session.add(item)
    current_user.points = (current_user.points or 0) + 20
    db.session.commit()
    logging.info(f'Portfolio item added for user: {current_user.username}')
    return redirect(url_for('portfolio'))


@app.route('/portfolio/<int:item_id>/delete', methods=['POST'])
def delete_portfolio_item(item_id):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    
    item = PortfolioItem.query.get(item_id)
    if item and item.user_id == current_user.id:
        db.session.delete(item)
        db.session.commit()
        logging.info(f'Portfolio item deleted for user: {current_user.username}')
    return redirect(url_for('portfolio'))


# ==================== FEATURE 6: Mentorship ====================
@app.route('/mentorship/available-mentors', methods=['GET'])
def available_mentors():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    
    mentors = Mentor.query.filter(Mentor.availability.in_(['available', 'limited'])).all()
    requested_mentor_ids = {
        m.mentor_id for m in MentorshipConnection.query.filter_by(student_id=current_user.id).all()
    }
    return render_template(
        'available_mentors.html',
        user=current_user.username,
        mentors=mentors,
        requested_mentor_ids=requested_mentor_ids
    )


@app.route('/mentorship/become-mentor', methods=['GET', 'POST'])
def become_mentor():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    
    existing = Mentor.query.filter_by(user_id=current_user.id).first()
    
    if request.method == 'POST':
        expertise = request.form.get('expertise')
        bio = request.form.get('bio')
        availability = request.form.get('availability', 'available')
        if availability not in {'available', 'limited', 'unavailable'}:
            availability = 'available'
        
        if existing:
            existing.expertise = expertise
            existing.bio = bio
            existing.availability = availability
        else:
            mentor = Mentor(user_id=current_user.id, expertise=expertise, bio=bio, availability=availability)
            db.session.add(mentor)
        
        db.session.commit()
        current_user.points = (current_user.points or 0) + 25
        db.session.commit()
        logging.info(f'Mentor profile updated for user: {current_user.username}')
        return redirect(url_for('dashboard'))
    
    return render_template('become_mentor.html', user=current_user.username, mentor=existing)


@app.route('/mentorship/request/<int:mentor_id>', methods=['POST'])
def request_mentorship(mentor_id):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    
    mentor = Mentor.query.get(mentor_id)
    if not mentor:
        return redirect(url_for('available_mentors'))
    if mentor.user_id == current_user.id:
        return redirect(url_for('available_mentors'))
    
    existing_connection = MentorshipConnection.query.filter_by(
        student_id=current_user.id,
        mentor_id=mentor.user_id
    ).first()
    
    if not existing_connection:
        connection = MentorshipConnection(student_id=current_user.id, mentor_id=mentor.user_id)
        db.session.add(connection)
        
        # Create notification for mentor
        notif = Notification(
            user_id=mentor.user_id,
            title='Mentorship Request',
            message=f'{current_user.username} requested mentorship',
            notification_type='mentorship'
        )
        db.session.add(notif)
        db.session.commit()
        logging.info(f'Mentorship request sent from {current_user.username} to {mentor.user.username}')
    
    return redirect(url_for('available_mentors'))


@app.route('/mentorship/my-connections', methods=['GET'])
def my_mentorship_connections():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    
    # Get connections where current_user is student
    student_connections = MentorshipConnection.query.filter_by(student_id=current_user.id).all()
    # Get connections where current_user is mentor
    mentor_connections = MentorshipConnection.query.filter_by(mentor_id=current_user.id).all()
    
    return render_template(
        'mentorship_connections.html',
        user=current_user.username,
        student_connections=student_connections,
        mentor_connections=mentor_connections
    )


@app.route('/mentorship/<int:connection_id>/accept', methods=['POST'])
def accept_mentorship_request(connection_id):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    connection = MentorshipConnection.query.get(connection_id)
    if not connection or connection.mentor_id != current_user.id:
        return redirect(url_for('my_mentorship_connections'))

    connection.status = 'active'
    connection.start_date = datetime.utcnow()
    db.session.add(Notification(
        user_id=connection.student_id,
        title='Mentorship Request Accepted',
        message=f'{current_user.username} accepted your mentorship request.',
        notification_type='mentorship'
    ))
    db.session.commit()
    return redirect(url_for('my_mentorship_connections'))


@app.route('/mentorship/<int:connection_id>/reject', methods=['POST'])
def reject_mentorship_request(connection_id):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    connection = MentorshipConnection.query.get(connection_id)
    if not connection or connection.mentor_id != current_user.id:
        return redirect(url_for('my_mentorship_connections'))

    db.session.add(Notification(
        user_id=connection.student_id,
        title='Mentorship Request Rejected',
        message=f'{current_user.username} declined your mentorship request.',
        notification_type='mentorship'
    ))
    db.session.delete(connection)
    db.session.commit()
    return redirect(url_for('my_mentorship_connections'))


@app.route('/mentorship/<int:connection_id>/complete', methods=['POST'])
def complete_mentorship(connection_id):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    connection = MentorshipConnection.query.get(connection_id)
    if not connection or connection.mentor_id != current_user.id:
        return redirect(url_for('my_mentorship_connections'))

    connection.status = 'completed'
    connection.end_date = datetime.utcnow()
    db.session.add(Notification(
        user_id=connection.student_id,
        title='Mentorship Completed',
        message=f'{current_user.username} marked the mentorship as completed.',
        notification_type='mentorship'
    ))
    db.session.commit()
    return redirect(url_for('my_mentorship_connections'))


@app.route('/mentorship/<int:connection_id>/cancel', methods=['POST'])
def cancel_mentorship_request(connection_id):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    connection = MentorshipConnection.query.get(connection_id)
    if not connection or connection.student_id != current_user.id:
        return redirect(url_for('my_mentorship_connections'))

    if connection.status == 'pending':
        db.session.add(Notification(
            user_id=connection.mentor_id,
            title='Mentorship Request Cancelled',
            message=f'{current_user.username} cancelled the mentorship request.',
            notification_type='mentorship'
        ))
        db.session.delete(connection)
    else:
        connection.status = 'completed'
        connection.end_date = datetime.utcnow()
    db.session.commit()
    return redirect(url_for('my_mentorship_connections'))


# ==================== FEATURE 7: Progress Tracking ====================
@app.route('/progress-tracking', methods=['GET'])
def progress_tracking():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    
    skills = SkillProgress.query.filter_by(user_id=current_user.id).all()
    assessments = Assessment.query.filter_by(user_id=current_user.id).order_by(Assessment.created_at.desc()).all()
    
    # Calculate progress stats
    avg_score = None
    total_assessments = len(assessments)
    if total_assessments > 0:
        avg_score = sum(a.score for a in assessments if a.score) / total_assessments
    
    return render_template(
        'progress_tracking.html',
        user=current_user.username,
        skills=skills,
        assessments=assessments,
        avg_score=avg_score,
        total_assessments=total_assessments
    )


@app.route('/progress-tracking/add-skill', methods=['POST'])
def add_skill_progress():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    
    skill_name = (request.form.get('skill_name') or '').strip()
    proficiency_level = int(request.form.get('proficiency_level', 1))
    proficiency_level = min(max(proficiency_level, 1), 5)

    if not skill_name:
        return redirect(url_for('progress_tracking'))
    
    existing = SkillProgress.query.filter_by(user_id=current_user.id, skill_name=skill_name).first()
    
    if existing:
        existing.proficiency_level = proficiency_level
        existing.progress_percentage = (proficiency_level / 5) * 100
    else:
        skill = SkillProgress(
            user_id=current_user.id,
            skill_name=skill_name,
            proficiency_level=proficiency_level,
            progress_percentage=(proficiency_level / 5) * 100
        )
        db.session.add(skill)
    
    db.session.commit()
    logging.info(f'Skill progress updated for user: {current_user.username}')
    return redirect(url_for('progress_tracking'))


@app.route('/progress-tracking/skill/<int:skill_id>/delete', methods=['POST'])
def delete_skill_progress(skill_id):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    skill = SkillProgress.query.get(skill_id)
    if skill and skill.user_id == current_user.id:
        db.session.delete(skill)
        db.session.commit()
    return redirect(url_for('progress_tracking'))


@app.route('/api/progress-data', methods=['GET'])
def get_progress_data():
    if not current_user.is_authenticated:
        return jsonify({'error': 'Not authenticated'}), 401
    
    assessments = Assessment.query.filter_by(user_id=current_user.id).order_by(Assessment.created_at).all()
    skills = SkillProgress.query.filter_by(user_id=current_user.id).all()
    
    assessment_data = {
        'dates': [a.created_at.strftime('%Y-%m-%d') for a in assessments],
        'scores': [a.score for a in assessments],
        'confidence': [a.confidence for a in assessments]
    }
    
    skill_data = {
        'skills': [s.skill_name for s in skills],
        'levels': [s.proficiency_level for s in skills],
        'progress': [s.progress_percentage for s in skills]
    }
    
    return jsonify({'assessments': assessment_data, 'skills': skill_data})


# ==================== FEATURE 3: Enhanced Career Roadmap ====================
@app.route('/career-roadmap', methods=['GET'])
def career_roadmap():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    
    roadmap = CareerRoadmap.query.filter_by(user_id=current_user.id).first()
    
    if not roadmap:
        # Create default roadmap based on latest assessment
        latest_assessment = Assessment.query.filter_by(user_id=current_user.id).order_by(Assessment.created_at.desc()).first()
        predicted_result = int(latest_assessment.result) if latest_assessment and str(latest_assessment.result).isdigit() else 0
        roadmap, _, _ = _ensure_user_career_roadmap(current_user.id, predicted_result)
        db.session.commit()

    milestones = []
    if roadmap and roadmap.roadmap_data:
        try:
            milestones = (json.loads(roadmap.roadmap_data) or {}).get('milestones', [])
        except Exception:
            milestones = []

    return render_template('career_roadmap.html', user=current_user.username, roadmap=roadmap, milestones=milestones)


@app.route('/career-roadmap/update-milestone', methods=['POST'])
def update_roadmap_milestone():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    
    milestone = int(request.form.get('milestone', 0))
    roadmap = CareerRoadmap.query.filter_by(user_id=current_user.id).first()
    
    if roadmap:
        roadmap.current_milestone = milestone
        current_user.points = (current_user.points or 0) + 30
        db.session.commit()
        logging.info(f'Career roadmap milestone updated for user: {current_user.username}')
    
    return redirect(url_for('career_roadmap'))


@app.route('/logout')
def logout():
    if current_user.is_authenticated:
        logging.info(f'User logged out: {current_user.username}')
    logout_user()
    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()

    app.run(debug=True)
