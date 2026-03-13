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
    Mentor, MentorshipConnection, SkillProgress, AIResult
)
from secure_career_system import ai_engine
from werkzeug.utils import secure_filename
from flask_talisman import Talisman
try:
    from secure_career_system.resume_analyzer import analyze_resume
    _RESUME_ANALYZER_LOADED = True
except ImportError:
    _RESUME_ANALYZER_LOADED = False
    def analyze_resume(path, education_level=None, career_goal=None):
        return {"found_skills": [], "skill_gaps": [], "contact_info": {}, "education": [], "roadmap": {}}
try:
    import shap
except Exception:
    shap = None
import os
import threading
import time
import uuid
from cryptography.fernet import Fernet, InvalidToken
import secure_career_system.train_model as train_model
from flask_migrate import Migrate
import joblib
import logging
from datetime import datetime, timedelta
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

from secure_career_system import ai_service

# ── Universal Platform Modules ──────────────────────────────────────
try:
    from secure_career_system.services import stream_recommender, course_recommender
    from secure_career_system.services import college_recommender, exam_guidance
    from secure_career_system.services import learning_engine, career_map as career_map_service
    from secure_career_system.ai_modules import career_simulator, career_twin, market_analysis
    from secure_career_system.resume_analyzer import (
        generate_resume_draft, generate_linkedin_suggestions,
        generate_portfolio_recommendations, analyze_skill_gap_by_stage
    )
    _UNIVERSAL_MODULES_LOADED = True
except ImportError as _e:
    _UNIVERSAL_MODULES_LOADED = False
    logging.warning(f"Universal platform modules not loaded: {_e}")

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
APP_ENV = os.getenv('APP_ENV', os.getenv('FLASK_ENV', 'development')).lower()
IS_PRODUCTION = APP_ENV == 'production'

secret_key = os.getenv('SECRET_KEY')
if IS_PRODUCTION and not secret_key:
    raise RuntimeError('SECRET_KEY must be set when APP_ENV=production')

app.secret_key = secret_key or 'dev-secret-key-change-me'

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'sqlite:///secure_career_system.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_pre_ping': True}
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = (
    os.getenv('SESSION_COOKIE_SECURE', '1' if IS_PRODUCTION else '0') == '1'
)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(
    minutes=int(os.getenv('SESSION_TTL_MINUTES', '120'))
)
app.config['PREFERRED_URL_SCHEME'] = 'https' if app.config['SESSION_COOKIE_SECURE'] else 'http'

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


def _validate_startup_config():
    if not IS_PRODUCTION:
        return

    if app.secret_key == 'dev-secret-key-change-me':
        raise RuntimeError('Insecure secret key detected in production')

    if not app.config['SESSION_COOKIE_SECURE']:
        raise RuntimeError('SESSION_COOKIE_SECURE must be enabled in production')


_validate_startup_config()

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


@app.before_request
def _set_request_context():
    request.request_id = request.headers.get('X-Request-ID') or str(uuid.uuid4())
    request.start_time = time.time()


@app.after_request
def _add_request_headers(response):
    response.headers['X-Request-ID'] = getattr(request, 'request_id', 'unknown')
    started = getattr(request, 'start_time', None)
    if started is not None:
        duration_ms = int((time.time() - started) * 1000)
        response.headers['X-Response-Time-Ms'] = str(duration_ms)
    return response


@app.errorhandler(404)
def handle_not_found(error):
    if request.path.startswith('/api/'):
        return jsonify({'error': 'not found', 'request_id': getattr(request, 'request_id', None)}), 404
    return error


@app.errorhandler(500)
def handle_internal_error(error):
    logging.exception('Unhandled server error')
    if request.path.startswith('/api/'):
        return jsonify({'error': 'internal server error', 'request_id': getattr(request, 'request_id', None)}), 500
    return render_template('login.html', error='Unexpected server error. Please try again.'), 500


@app.route('/healthz', methods=['GET'])
def healthz():
    return jsonify({'status': 'ok', 'service': 'secure-career-system', 'env': APP_ENV}), 200


@app.route('/readyz', methods=['GET'])
def readyz():
    checks = {'database': False, 'model_loaded': model is not None}
    status_code = 200
    status = 'ready'

    try:
        db.session.execute(db.text('SELECT 1'))
        checks['database'] = True
    except Exception as exc:
        logging.error(f'Readiness DB check failed: {exc}')
        status = 'not_ready'
        status_code = 503

    return jsonify({'status': status, 'checks': checks, 'env': APP_ENV}), status_code


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
                return redirect(url_for('verify_otp', username=username))
            else:
                allow_local_otp = os.getenv('ALLOW_LOCAL_OTP_FALLBACK', '1') == '1'
                if app.debug and allow_local_otp:
                    logging.warning(
                        f'OTP email failed for user {username}; using local fallback OTP: {otp}'
                    )
                    return redirect(url_for('verify_otp', username=username))

                logging.warning(f'Failed to send OTP email for user: {username}')
                return render_template(
                    'login.html',
                    error='Unable to send OTP email. Please check email settings and try again.'
                )

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
        cgpa_normalized = 0.0  # default; overwritten below if cgpa is available
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
        db.session.flush()  # get assessment_record.id for AI result linkage
        
        # ---- Central AI Engine Integration ----
        user_skills_list = [s.strip() for s in skills.split(',') if s.strip()] if skills else []

        ai_career = ai_engine.predict_career(responses, cgpa=cgpa, skills=skills)
        ai_career_id = ai_career.get('career_id', int(prediction))

        ai_gaps = ai_engine.analyze_skill_gaps(user_skills_list, ai_career_id)

        ai_placement = ai_engine.predict_placement(
            assessment_score=base_score,
            cgpa=cgpa if cgpa is not None else 0.0,
            skills_count=len(user_skills_list),
        )

        ai_jobs = ai_engine.match_jobs(ai_career_id, user_skills_list)
        ai_roadmap = ai_engine.generate_roadmap(ai_career_id, user_skills_list)

        # Fetch mentors for matching
        mentor_list = []
        for m in Mentor.query.filter(Mentor.availability.in_(['available', 'limited'])).all():
            mentor_list.append({
                'user_id': m.user_id,
                'expertise': m.expertise or '',
                'availability': m.availability,
            })
        ai_mentors = ai_engine.match_mentors(ai_career_id, ai_gaps.get('missing_skills', []), mentor_list)

        # Portfolio feedback
        portfolio_items = PortfolioItem.query.filter_by(user_id=current_user.id).all()
        portfolio_data = [
            {'title': p.title, 'description': p.description, 'skills_used': p.category or '', 'url': p.github_url or p.media_url or ''}
            for p in portfolio_items
        ]
        ai_portfolio = ai_engine.get_portfolio_feedback(portfolio_data, ai_career_id, ai_gaps.get('missing_skills', []))

        # Store consolidated AI result
        ai_result = AIResult(
            user_id=current_user.id,
            assessment_id=assessment_record.id,
            career_id=ai_career_id,
            career_name=ai_career.get('career_name', 'Technology'),
            confidence=ai_career.get('confidence', confidence),
            domain_scores=json.dumps(ai_career.get('scores', {})),
            skill_gaps=json.dumps(ai_gaps.get('missing_skills', [])),
            gap_score=ai_gaps.get('gap_score', 0.0),
            placement_probability=ai_placement.get('probability', placement_prob),
            placement_factors=json.dumps(ai_placement.get('factors', {})),
            job_recommendations=json.dumps(ai_jobs),
            roadmap_data=json.dumps(ai_roadmap),
            certification_suggestions=json.dumps(ai_roadmap.get('certifications', [])),
            mentorship_scores=json.dumps(ai_mentors),
            portfolio_feedback=json.dumps(ai_portfolio),
        )
        db.session.add(ai_result)

        # Update AI-driven job recommendations in DB
        JobRecommendation.query.filter_by(user_id=current_user.id).delete()
        for job in ai_jobs[:8]:
            db.session.add(JobRecommendation(
                user_id=current_user.id,
                job_title=job['title'],
                company=job['company'],
                description=job.get('description', ''),
                required_skills=job.get('required_skills', ''),
                matching_score=round(job.get('matching_score', 0) * 100, 1),
            ))

        # Align roadmap with the newly suggested career path
        _ensure_user_career_roadmap(current_user.id, ai_career_id)
        
        db.session.commit()

        # Award gamification points
        current_user.points = (current_user.points or 0) + 10
        db.session.commit()

        logging.info(f'Assessment completed for user {current_user.username}: Tech={tech_score:.2f}, Finance={finance_score:.2f}, Healthcare={healthcare_score:.2f}, CGPA={cgpa}, Result={prediction}, AI_Career={ai_career_id}')
        return redirect(url_for('result', result=ai_career_id))

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
    query = (data.get('query') or '').strip()
    if not query:
        return jsonify({'reply': 'Please ask me something about your career!'})  

    # Build user context from profile + latest assessment
    user_profile = None
    if current_user.is_authenticated:
        profile = StudentProfile.query.filter_by(user_id=current_user.id).first()
        latest_assessment = Assessment.query.filter_by(user_id=current_user.id).order_by(Assessment.created_at.desc()).first()
        career_map = {'0': 'Technology', '1': 'Finance', '2': 'Healthcare'}
        user_profile = {
            'skills': profile.skills if profile else current_user.skills,
            'cgpa': profile.cgpa if profile else None,
            'career_path': career_map.get(str(latest_assessment.result), 'Unknown') if latest_assessment else (current_user.career_goal or None),
            'result': latest_assessment.result if latest_assessment else None,
            'education_level': current_user.education_level,
            'career_goal': current_user.career_goal,
            'interests': current_user.interests,
            'experience_level': current_user.experience_level,
        }

    if ai_service.is_available():
        reply = ai_service.chatbot_response(query, user_profile=user_profile)
        if reply:
            return jsonify({'reply': reply, 'ai_powered': True})

    # Fallback heuristic
    q = query.lower()
    if 'recommend' in q or 'career' in q:
        skills = (user_profile.get('skills') or '').split(',') if user_profile else []
        if skills and skills[0]:
            return jsonify({'reply': f"Based on your skills ({', '.join(skills[:3])}), consider careers in Data, Software Dev or Cloud. Set GROQ_API_KEY for full AI responses."})
        return jsonify({'reply': 'Add your skills in your profile and I can suggest careers. Set GROQ_API_KEY for AI-powered advice.'})
    return jsonify({'reply': "I'm your career assistant. Set GROQ_API_KEY in .env for full AI-powered responses!"})


@app.route('/api/ai-health', methods=['GET'])
def api_ai_health():
    """Lightweight AI diagnostics endpoint without exposing secrets."""
    provider = 'groq'
    model = os.getenv('GROQ_MODEL', 'llama-3.1-8b-instant')
    key_configured = bool(os.getenv('GROQ_API_KEY'))
    available = ai_service.is_available()
    status = 'ok' if available else 'degraded'

    return jsonify({
        'status': status,
        'provider': provider,
        'model': model,
        'key_configured': key_configured,
        'ai_available': available,
        'message': (
            'AI integration is active.'
            if available
            else 'AI integration unavailable. Check GROQ_API_KEY and model configuration.'
        )
    }), (200 if available else 503)


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

    if model is None:
        return jsonify({'error': 'model not loaded'}), 503

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
    resume_path = data.get('resume_path')
    user_id = data.get('user_id')

    path = None
    if resume_path:
        path = resume_path
    elif user_id:
        resume = Resume.query.filter_by(user_id=user_id).order_by(Resume.uploaded_at.desc()).first()
        if not resume:
            return jsonify({'error': 'no resume found for user'}), 404
        path = os.path.join(app.config['UPLOAD_FOLDER'], resume.filename)
    else:
        return jsonify({'error': 'resume_path or user_id required'}), 400

    analysis = analyze_resume(path)

    # Enhance with AI skill-gap analysis if available
    if ai_service.is_available():
        latest = Assessment.query.filter_by(user_id=user_id).order_by(Assessment.created_at.desc()).first() if user_id else None
        career_map = {'0': 'Technology', '1': 'Finance', '2': 'Healthcare'}
        career_path = career_map.get(str(latest.result), 'Technology') if latest else 'Technology'
        ai_gaps = ai_service.analyze_skill_gap_ai(analysis.get('found_skills', []), career_path)
        if ai_gaps:
            analysis['ai_skill_gaps'] = ai_gaps.get('gaps', [])
            analysis['ai_powered'] = True

    return jsonify(analysis)


@app.route('/roadmap_view')
def roadmap_view():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    # Determine career path from latest assessment
    latest_assessment = Assessment.query.filter_by(user_id=current_user.id).order_by(Assessment.created_at.desc()).first()
    career_map = {'0': 'Technology', '1': 'Finance', '2': 'Healthcare'}
    career_path = career_map.get(str(latest_assessment.result), 'Technology') if latest_assessment else 'Technology'

    # Get skills from profile
    profile = StudentProfile.query.filter_by(user_id=current_user.id).first()
    skills = profile.skills.split(',') if profile and profile.skills else []
    cgpa = profile.cgpa if profile else None

    # Try AI roadmap first
    if ai_service.is_available():
        ai_roadmap = ai_service.generate_roadmap_ai(career_path, skills, cgpa=cgpa)
        if ai_roadmap and ai_roadmap.get('months'):
            return render_template('roadmap.html', ai_roadmap=ai_roadmap['months'], career_path=career_path, ai_powered=True)

    # Fallback: resume-based roadmap
    resume = Resume.query.filter_by(user_id=current_user.id).order_by(Resume.uploaded_at.desc()).first()
    if not resume:
        return render_template('roadmap.html', roadmap={}, career_path=career_path, ai_powered=False)
    path = os.path.join(app.config['UPLOAD_FOLDER'], resume.filename)
    analysis = analyze_resume(path)
    return render_template('roadmap.html', roadmap=analysis.get('roadmap', {}), career_path=career_path, ai_powered=False)



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

    # AI-generated personalised explanation
    ai_explanation = None
    if ai_service.is_available():
        profile = StudentProfile.query.filter_by(user_id=current_user.id).first()
        skills = profile.skills.split(',') if profile and profile.skills else []
        cgpa = profile.cgpa if profile else None
        ai_explanation = ai_service.explain_career_result(
            career_path, confidence or 0.5, skills=skills, cgpa=cgpa
        )

    logging.info(f'User {current_user.username} completed assessment with result: {result}')
    return render_template(
        'result.html',
        result=result,
        confidence=confidence,
        placement=placement,
        aid=aid,
        career_path=career_path,
        suggested_roadmap=milestones,
        current_milestone=(roadmap.current_milestone if roadmap else 0),
        ai_explanation=ai_explanation,
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
        education_level = (request.form.get('education_level') or '').strip()
        career_goal = (request.form.get('career_goal') or '').strip()
        interests = (request.form.get('interests') or '').strip()
        experience_level = (request.form.get('experience_level') or '').strip()

        current_user.email = email

        # Persist new universal career fields
        allowed_education = {'School', 'PUC', 'Undergraduate', 'Postgraduate', 'PhD', 'Professional'}
        if education_level and education_level in allowed_education:
            current_user.education_level = education_level
        if career_goal:
            current_user.career_goal = career_goal
        if interests:
            current_user.interests = interests
        if experience_level:
            current_user.experience_level = experience_level
        if skills:
            current_user.skills = skills

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
    raw_skills = profile.skills if profile and profile.skills else ''
    skills = [s.strip() for s in raw_skills.split(',') if s and s.strip()]

    # Fetch user's latest career path
    latest_assessment = Assessment.query.filter_by(user_id=current_user.id).order_by(Assessment.created_at.desc()).first()
    career_map = {'0': 'Technology', '1': 'Finance', '2': 'Healthcare'}
    career_path = career_map.get(str(latest_assessment.result), 'Technology') if latest_assessment else 'Technology'
    cgpa = profile.cgpa if profile else None

    # Fallback seed skills so recommendations still work for new users.
    if not skills:
        default_skill_map = {
            'Technology': ['Python', 'SQL', 'Git'],
            'Finance': ['Excel', 'Financial Modeling', 'Power BI'],
            'Healthcare': ['Patient Care', 'Medical Terminology', 'Communication'],
        }
        skills = default_skill_map.get(career_path, ['Communication', 'Problem Solving'])

    # Use AI engine first: get latest AI result for career_id
    latest_ai = AIResult.query.filter_by(user_id=current_user.id).order_by(AIResult.created_at.desc()).first()
    career_id = latest_ai.career_id if latest_ai else 0
    job_data = ai_engine.match_jobs(career_id, skills)

    # Enhance with Groq AI service if available
    if ai_service.is_available():
        ai_jobs_enhanced = ai_service.generate_job_recommendations_ai(skills, career_path, cgpa=cgpa)
        if ai_jobs_enhanced:
            job_data = [{
                'title': j.get('title', 'Role'),
                'company': j.get('company', ''),
                'required_skills': j.get('required_skills', ''),
                'matching_score': j.get('match_score', 70) / 100.0,
            } for j in ai_jobs_enhanced]

    # Clear existing recommendations
    JobRecommendation.query.filter_by(user_id=current_user.id).delete()

    for job in job_data[:8]:
        recommendation = JobRecommendation(
            user_id=current_user.id,
            job_title=job['title'],
            company=job['company'],
            description=job.get('description', ''),
            required_skills=job.get('required_skills', ''),
            matching_score=round(job.get('matching_score', 0) * 100, 1),
        )
        db.session.add(recommendation)

    db.session.commit()
    current_user.points = (current_user.points or 0) + 10
    db.session.commit()
    logging.info(
        f'Job recommendations generated for user: {current_user.username} '
        f'(used_fallback_skills={not bool(raw_skills)})'
    )
    return jsonify({
        'status': 'recommendations generated',
        'count': len(job_data[:8]),
        'used_fallback_skills': not bool(raw_skills),
    })


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
        avg_score = sum(a.score for a in assessments if a.score is not None) / total_assessments
    
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
    try:
        proficiency_level = int(request.form.get('proficiency_level', 1))
    except (ValueError, TypeError):
        proficiency_level = 1
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
    
    try:
        milestone = int(request.form.get('milestone', 0))
    except (ValueError, TypeError):
        milestone = 0
    roadmap = CareerRoadmap.query.filter_by(user_id=current_user.id).first()
    
    if roadmap:
        roadmap.current_milestone = milestone
        current_user.points = (current_user.points or 0) + 30
        db.session.commit()
        logging.info(f'Career roadmap milestone updated for user: {current_user.username}')
    
    return redirect(url_for('career_roadmap'))


# ==================== AI Module: Career Recommendation ====================
@app.route('/ai-career-recommendation')
def ai_career_recommendation():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    latest_ai = AIResult.query.filter_by(user_id=current_user.id).order_by(AIResult.created_at.desc()).first()

    career_data = None
    if latest_ai:
        career_data = {
            'career_name': latest_ai.career_name,
            'career_id': latest_ai.career_id,
            'confidence': latest_ai.confidence,
            'domain_scores': json.loads(latest_ai.domain_scores) if latest_ai.domain_scores else {},
            'created_at': latest_ai.created_at.strftime('%B %d, %Y %I:%M %p') if latest_ai.created_at else '',
        }

    return render_template('ai_career_recommendation.html', user=current_user.username, career_data=career_data)


# ==================== AI Module: Skill Gap Analyzer ====================
@app.route('/ai-skill-gap')
def ai_skill_gap():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    latest_ai = AIResult.query.filter_by(user_id=current_user.id).order_by(AIResult.created_at.desc()).first()

    gap_data = None
    if latest_ai:
        missing_skills = json.loads(latest_ai.skill_gaps) if latest_ai.skill_gaps else []
        # Generate recommendations for each missing skill
        recommendations = []
        for skill in missing_skills:
            course = ai_engine.COURSE_SUGGESTIONS.get(skill, f'Search online courses for {skill}')
            recommendations.append({'skill': skill, 'course': course})

        gap_data = {
            'career_name': latest_ai.career_name,
            'missing_skills': missing_skills,
            'gap_score': latest_ai.gap_score,
            'recommendations': recommendations,
        }

    return render_template('ai_skill_gap.html', user=current_user.username, gap_data=gap_data)


# ==================== AI Module: Placement Prediction ====================
@app.route('/ai-placement-prediction')
def ai_placement_prediction():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    latest_ai = AIResult.query.filter_by(user_id=current_user.id).order_by(AIResult.created_at.desc()).first()

    placement_data = None
    if latest_ai:
        placement_data = {
            'probability': latest_ai.placement_probability,
            'factors': json.loads(latest_ai.placement_factors) if latest_ai.placement_factors else {},
            'career_name': latest_ai.career_name,
            'created_at': latest_ai.created_at.strftime('%B %d, %Y %I:%M %p') if latest_ai.created_at else '',
        }

    return render_template('ai_placement_prediction.html', user=current_user.username, placement_data=placement_data)





# ══════════════════════════════════════════════════════════════════════
#  UNIVERSAL AI CAREER NAVIGATION PLATFORM — NEW ROUTES
# ══════════════════════════════════════════════════════════════════════

# ── Helper ────────────────────────────────────────────────────────────

def _user_skills_list() -> list:
    """Return the current user's skills as a list (safe, handles None)."""
    if not current_user.is_authenticated:
        return []
    raw = current_user.skills or ''
    return [s.strip() for s in raw.split(',') if s.strip()]


def _user_interests_list() -> list:
    """Return the current user's interests as a list."""
    if not current_user.is_authenticated:
        return []
    raw = current_user.interests or ''
    return [i.strip() for i in raw.split(',') if i.strip()]


# ── Profile Update (education level, career goal, interests) ─────────

@app.route('/profile/update-career', methods=['POST'])
@login_required
def update_career_profile():
    """Update the new universal career fields on the User model."""
    education_level = request.form.get('education_level', '').strip()
    career_goal = request.form.get('career_goal', '').strip()
    interests = request.form.get('interests', '').strip()
    skills = request.form.get('skills', '').strip()
    experience_level = request.form.get('experience_level', '').strip()

    allowed_education = {'School', 'PUC', 'Undergraduate', 'Postgraduate', 'PhD', 'Professional'}
    if education_level and education_level not in allowed_education:
        return jsonify({'error': 'Invalid education_level'}), 400

    user = User.query.get(current_user.id)
    if education_level:
        user.education_level = education_level
    if career_goal:
        user.career_goal = career_goal
    if interests:
        user.interests = interests
    if skills:
        user.skills = skills
    if experience_level:
        user.experience_level = experience_level

    db.session.commit()
    return jsonify({'status': 'ok', 'message': 'Career profile updated successfully.'})


# ── Feature 1: Stream Recommendation ─────────────────────────────────

@app.route('/api/stream-recommendation', methods=['POST'])
@login_required
def api_stream_recommendation():
    if not _UNIVERSAL_MODULES_LOADED:
        return jsonify({'error': 'Service unavailable'}), 503
    data = request.get_json(silent=True) or {}
    result = stream_recommender.recommend_stream(
        favorite_subjects=data.get('favorite_subjects', []),
        interests=data.get('interests', _user_interests_list()),
        logical_reasoning_score=float(data.get('logical_reasoning_score', 5)),
        personality_traits=data.get('personality_traits', []),
    )
    return jsonify(result)


@app.route('/stream-recommendation', methods=['GET'])
@login_required
def stream_recommendation_page():
    return render_template(
        'stream_recommendation.html',
        user=current_user.username,
        education_level=current_user.education_level or 'School',
    )


# ── Feature 2: Course Recommendation ─────────────────────────────────

@app.route('/api/course-recommendation', methods=['POST'])
@login_required
def api_course_recommendation():
    if not _UNIVERSAL_MODULES_LOADED:
        return jsonify({'error': 'Service unavailable'}), 503
    data = request.get_json(silent=True) or {}
    result = course_recommender.recommend_courses(
        stream=data.get('stream', 'Science'),
        marks_percentage=float(data.get('marks_percentage', 60)),
        interests=data.get('interests', _user_interests_list()),
        skills=data.get('skills', _user_skills_list()),
    )
    return jsonify(result)


@app.route('/course-recommendation', methods=['GET'])
@login_required
def course_recommendation_page():
    return render_template(
        'course_recommendation.html',
        user=current_user.username,
        education_level=current_user.education_level or 'PUC',
    )


# ── Feature 3: College Recommendation ────────────────────────────────

@app.route('/api/college-recommendation', methods=['POST'])
@login_required
def api_college_recommendation():
    if not _UNIVERSAL_MODULES_LOADED:
        return jsonify({'error': 'Service unavailable'}), 503
    data = request.get_json(silent=True) or {}
    result = college_recommender.recommend_colleges(
        course=data.get('course', 'B.Tech'),
        location_preference=data.get('location_preference'),
        max_fees_per_year=data.get('max_fees_per_year'),
        college_type=data.get('college_type'),
    )
    return jsonify(result)


@app.route('/college-recommendation', methods=['GET'])
@login_required
def college_recommendation_page():
    return render_template(
        'college_recommendation.html',
        user=current_user.username,
    )


# ── Feature 4: Entrance Exam Guidance ────────────────────────────────

@app.route('/api/exam-guidance', methods=['POST'])
@login_required
def api_exam_guidance():
    if not _UNIVERSAL_MODULES_LOADED:
        return jsonify({'error': 'Service unavailable'}), 503
    data = request.get_json(silent=True) or {}
    career_goal = data.get('career_goal', current_user.career_goal or 'Engineering')
    result = exam_guidance.get_exam_guidance(
        career_goal=career_goal,
        education_level=data.get('education_level', current_user.education_level),
    )
    return jsonify(result)


@app.route('/exam-guidance', methods=['GET'])
@login_required
def exam_guidance_page():
    career_goal = current_user.career_goal or ''
    initial_data = None
    if _UNIVERSAL_MODULES_LOADED and career_goal:
        initial_data = exam_guidance.get_exam_guidance(
            career_goal=career_goal,
            education_level=current_user.education_level,
        )
    all_exams = exam_guidance.get_all_exams() if _UNIVERSAL_MODULES_LOADED else []
    return render_template(
        'exam_guidance.html',
        user=current_user.username,
        career_goal=career_goal,
        exam_data=initial_data,
        all_exams=all_exams,
    )


# ── Feature 6 / 7: Career Simulator & Career Twin ────────────────────

@app.route('/api/career-simulation', methods=['POST'])
@login_required
def api_career_simulation():
    if not _UNIVERSAL_MODULES_LOADED:
        return jsonify({'error': 'Service unavailable'}), 503
    data = request.get_json(silent=True) or {}
    result = career_simulator.simulate_career(
        target_career=data.get('target_career', current_user.career_goal or 'Software Engineer'),
        education_level=data.get('education_level', current_user.education_level or 'Undergraduate'),
        current_skills=data.get('skills', _user_skills_list()),
        starting_point=data.get('starting_point'),
    )
    return jsonify(result)


@app.route('/career-simulation', methods=['GET'])
@login_required
def career_simulation_page():
    return render_template(
        'career_simulation.html',
        user=current_user.username,
        career_goal=current_user.career_goal or '',
        education_level=current_user.education_level or 'Undergraduate',
    )


@app.route('/api/career-twin', methods=['POST'])
@login_required
def api_career_twin():
    if not _UNIVERSAL_MODULES_LOADED:
        return jsonify({'error': 'Service unavailable'}), 503
    data = request.get_json(silent=True) or {}
    # Pull latest assessment for domain scores if available
    latest_ai = AIResult.query.filter_by(user_id=current_user.id).order_by(
        AIResult.created_at.desc()
    ).first()
    assessment_resp = None
    if latest_ai and latest_ai.domain_scores:
        assessment_resp = {'domain_scores': json.loads(latest_ai.domain_scores)}

    result = career_twin.predict_career_twins(
        skills=data.get('skills', _user_skills_list()),
        interests=data.get('interests', _user_interests_list()),
        education_level=data.get('education_level', current_user.education_level or 'Undergraduate'),
        assessment_responses=assessment_resp,
        top_n=int(data.get('top_n', 5)),
    )
    return jsonify(result)


@app.route('/career-twin', methods=['GET'])
@login_required
def career_twin_page():
    skills = _user_skills_list()
    interests = _user_interests_list()
    twin_results = None
    if _UNIVERSAL_MODULES_LOADED and (skills or interests):
        latest_ai = AIResult.query.filter_by(user_id=current_user.id).order_by(
            AIResult.created_at.desc()
        ).first()
        assessment_resp = None
        if latest_ai and latest_ai.domain_scores:
            assessment_resp = {'domain_scores': json.loads(latest_ai.domain_scores)}
        twin_results = career_twin.predict_career_twins(
            skills=skills,
            interests=interests,
            education_level=current_user.education_level or 'Undergraduate',
            assessment_responses=assessment_resp,
        )
    return render_template(
        'career_twin.html',
        user=current_user.username,
        twin_results=twin_results,
        education_level=current_user.education_level or 'Undergraduate',
    )


# ── Feature 8: Global Skill Demand ───────────────────────────────────

@app.route('/api/skill-demand', methods=['GET'])
@login_required
def api_skill_demand():
    if not _UNIVERSAL_MODULES_LOADED:
        return jsonify({'error': 'Service unavailable'}), 503
    top_n = int(request.args.get('top_n', 10))
    result = market_analysis.get_full_market_analysis()
    result['top_skills'] = result['top_skills'][:top_n]
    return jsonify(result)


@app.route('/skill-demand', methods=['GET'])
@login_required
def skill_demand_page():
    market_data = market_analysis.get_full_market_analysis() if _UNIVERSAL_MODULES_LOADED else {}
    return render_template(
        'skill_demand.html',
        user=current_user.username,
        market_data=market_data,
    )


# ── Feature 9: AI Personal Learning Roadmap ──────────────────────────

@app.route('/api/learning-roadmap', methods=['POST'])
@login_required
def api_learning_roadmap():
    if not _UNIVERSAL_MODULES_LOADED:
        return jsonify({'error': 'Service unavailable'}), 503
    data = request.get_json(silent=True) or {}
    result = learning_engine.generate_learning_roadmap(
        career_goal=data.get('career_goal', current_user.career_goal or 'Software Engineer'),
        education_level=data.get('education_level', current_user.education_level or 'Undergraduate'),
        current_skills=data.get('skills', _user_skills_list()),
        career_switch_from=data.get('career_switch_from'),
    )
    return jsonify(result)


@app.route('/learning-roadmap', methods=['GET'])
@login_required
def learning_roadmap_page():
    career_goal = current_user.career_goal or ''
    roadmap_data = None
    if _UNIVERSAL_MODULES_LOADED and career_goal:
        roadmap_data = learning_engine.generate_learning_roadmap(
            career_goal=career_goal,
            education_level=current_user.education_level or 'Undergraduate',
            current_skills=_user_skills_list(),
        )
    return render_template(
        'learning_roadmap.html',
        user=current_user.username,
        career_goal=career_goal,
        roadmap_data=roadmap_data,
    )


# ── Feature 10: Resume / Profile Builder ─────────────────────────────

@app.route('/resume-builder', methods=['GET', 'POST'])
@login_required
def resume_builder():
    resume_draft = None
    linkedin_tips = None
    portfolio_tips = None

    if request.method == 'POST':
        name = request.form.get('name', current_user.username)
        email = request.form.get('email', current_user.email) if hasattr(current_user, 'email') else ''
        phone = request.form.get('phone', '')
        career_goal = request.form.get('career_goal', current_user.career_goal or 'Software Engineer')
        education_level = request.form.get('education_level', current_user.education_level or 'Undergraduate')
        skills_raw = request.form.get('skills', current_user.skills or '')
        skills = [s.strip() for s in skills_raw.split(',') if s.strip()]

        if _UNIVERSAL_MODULES_LOADED:
            resume_draft = generate_resume_draft(
                name=name,
                email=email,
                phone=phone,
                education_level=education_level,
                career_goal=career_goal,
                skills=skills,
            )
            linkedin_tips = generate_linkedin_suggestions(
                name=name,
                career_goal=career_goal,
                skills=skills,
                education_level=education_level,
            )
            portfolio_tips = generate_portfolio_recommendations(
                career_goal=career_goal,
                skills=skills,
                education_level=education_level,
            )

    return render_template(
        'resume_builder.html',
        user=current_user.username,
        resume_draft=resume_draft,
        linkedin_tips=linkedin_tips,
        portfolio_tips=portfolio_tips,
        career_goal=current_user.career_goal or '',
        education_level=current_user.education_level or 'Undergraduate',
        skills=current_user.skills or '',
    )


# ── Feature 11: Career Opportunity Map ───────────────────────────────

@app.route('/career-map', methods=['GET'])
@login_required
def career_map_page():
    career_name = request.args.get('career', current_user.career_goal or '')
    career_info = None
    all_careers = []
    if _UNIVERSAL_MODULES_LOADED:
        if career_name:
            career_info = career_map_service.get_career_map(career_name)
        all_careers = career_map_service.get_all_careers()
    return render_template(
        'career_map.html',
        user=current_user.username,
        career_info=career_info,
        all_careers=all_careers,
        career_name=career_name,
    )


@app.route('/api/career-map', methods=['GET'])
@login_required
def api_career_map():
    if not _UNIVERSAL_MODULES_LOADED:
        return jsonify({'error': 'Service unavailable'}), 503
    career_name = request.args.get('career', '')
    if career_name:
        result = career_map_service.get_career_map(career_name)
        if result:
            return jsonify(result)
        return jsonify({'error': f'Career not found: {career_name}'}), 404
    return jsonify({'careers': career_map_service.get_all_careers()})


# ── Feature 12: Job + Internship Finder (Extended) ───────────────────
# (Existing job-recommendations route is kept; this extends the API)

@app.route('/api/internship-finder', methods=['POST'])
@login_required
def api_internship_finder():
    """Return internship, entry-level, freelance opportunities via AI."""
    if not ai_service.is_available():
        return jsonify({'error': 'AI service unavailable'}), 503
    data = request.get_json(silent=True) or {}
    skills = data.get('skills', _user_skills_list())
    career_path = data.get('career_path', current_user.career_goal or 'Technology')
    opportunity_type = data.get('type', 'internship')  # internship, entry-level, freelance, research

    try:
        jobs = ai_service.generate_job_recommendations_ai(
            skills=skills,
            career_path=f"{career_path} ({opportunity_type})",
            cgpa=0.0,
        )
        return jsonify({
            'opportunity_type': opportunity_type,
            'career_path': career_path,
            'opportunities': jobs,
        })
    except Exception as exc:
        logging.error(f"Internship finder error: {exc}")
        return jsonify({'error': 'Failed to generate opportunities'}), 500


# ── Feature 13: Lifelong Learning / Career Switch ────────────────────

@app.route('/career-switch', methods=['GET'])
@login_required
def career_switch_page():
    return render_template(
        'career_switch.html',
        user=current_user.username,
        current_career=current_user.career_goal or '',
        education_level=current_user.education_level or 'Professional',
    )


@app.route('/api/career-switch-roadmap', methods=['POST'])
@login_required
def api_career_switch_roadmap():
    if not _UNIVERSAL_MODULES_LOADED:
        return jsonify({'error': 'Service unavailable'}), 503
    data = request.get_json(silent=True) or {}
    result = learning_engine.generate_learning_roadmap(
        career_goal=data.get('target_career', 'AI Engineer'),
        education_level=current_user.education_level or 'Professional',
        current_skills=data.get('skills', _user_skills_list()),
        career_switch_from=data.get('current_career', current_user.career_goal),
    )
    return jsonify(result)


@app.route('/logout')
def logout():
    if current_user.is_authenticated:
        logging.info(f'User logged out: {current_user.username}')
    logout_user()
    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    # Keep local developer convenience; production should use migrations.
    auto_create = os.getenv('AUTO_CREATE_DB', '1' if not IS_PRODUCTION else '0') == '1'
    if auto_create:
        with app.app_context():
            db.create_all()

    debug_mode = (os.getenv('FLASK_DEBUG', '1' if not IS_PRODUCTION else '0') == '1') and not IS_PRODUCTION
    host = os.getenv('FLASK_RUN_HOST', '127.0.0.1')
    port = int(os.getenv('FLASK_RUN_PORT', '5000'))
    app.run(host=host, port=port, debug=debug_mode)
