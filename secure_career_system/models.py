from datetime import datetime
try:
    from flask_login import UserMixin
except Exception:
    class UserMixin:
        pass

from .extensions import db, login_manager, bcrypt


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), default='student')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_locked = db.Column(db.Boolean, default=False)
    failed_logins = db.Column(db.Integer, default=0)
    last_failed_at = db.Column(db.DateTime)
    points = db.Column(db.Integer, default=0)
    badges = db.Column(db.Text)

    def set_password(self, password: str):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password: str) -> bool:
        return bcrypt.check_password_hash(self.password_hash, password)


class StudentProfile(db.Model):
    __tablename__ = 'student_profiles'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    cgpa = db.Column(db.Float)
    skills = db.Column(db.Text)
    academic_records = db.Column(db.Text)
    # encrypted academic field (store base64 or encrypted string)
    academic_records_encrypted = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Assessment(db.Model):
    __tablename__ = 'assessments'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    responses = db.Column(db.Text)
    result = db.Column(db.String(255))
    score = db.Column(db.Float)
    confidence = db.Column(db.Float)
    placement_prob = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Appointment(db.Model):
    __tablename__ = 'appointments'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    counsellor_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    scheduled_at = db.Column(db.DateTime)
    status = db.Column(db.String(50), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class CounsellorNote(db.Model):
    __tablename__ = 'counsellor_notes'
    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id'), nullable=False)
    counsellor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    note = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Resume(db.Model):
    __tablename__ = 'resumes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    filename = db.Column(db.String(255))
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)


class AuditLog(db.Model):
    __tablename__ = 'audit_logs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    action = db.Column(db.String(255))
    ip_address = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# Feature 1: Profile Enhancements - Certifications and Badges
class Certification(db.Model):
    __tablename__ = 'certifications'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    issuer = db.Column(db.String(255))
    issue_date = db.Column(db.DateTime)
    expiry_date = db.Column(db.DateTime)
    credential_url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# Feature 2: Notifications
class Notification(db.Model):
    __tablename__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text)
    notification_type = db.Column(db.String(50))  # 'appointment', 'assessment', 'achievement', etc.
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# Feature 3: Career Roadmap
class CareerRoadmap(db.Model):
    __tablename__ = 'career_roadmaps'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    career_path = db.Column(db.String(255), nullable=False)
    current_milestone = db.Column(db.Integer, default=0)
    roadmap_data = db.Column(db.Text)  # JSON format with milestones
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# Feature 4: Skill Matching - Job Recommendations
class JobRecommendation(db.Model):
    __tablename__ = 'job_recommendations'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    job_title = db.Column(db.String(255), nullable=False)
    company = db.Column(db.String(255))
    description = db.Column(db.Text)
    required_skills = db.Column(db.Text)  # Comma-separated
    matching_score = db.Column(db.Float)  # 0-100
    source_url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# Feature 5: Portfolio
class PortfolioItem(db.Model):
    __tablename__ = 'portfolio_items'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(100))  # 'project', 'achievement', 'publication'
    media_url = db.Column(db.String(500))  # Link to project/image
    github_url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# Feature 6: Mentorship
class Mentor(db.Model):
    __tablename__ = 'mentors'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    expertise = db.Column(db.Text)  # Comma-separated skills/domains
    bio = db.Column(db.Text)
    availability = db.Column(db.String(100))  # 'available', 'limited', 'unavailable'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', backref=db.backref('mentor_profile', uselist=False))


class MentorshipConnection(db.Model):
    __tablename__ = 'mentorship_connections'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    mentor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(50), default='pending')  # 'pending', 'active', 'completed'
    request_date = db.Column(db.DateTime, default=datetime.utcnow)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    student = db.relationship('User', foreign_keys=[student_id], backref='student_mentorships')
    mentor = db.relationship('User', foreign_keys=[mentor_id], backref='mentor_mentorships')


# Feature 7: Progress Tracking
class SkillProgress(db.Model):
    __tablename__ = 'skill_progress'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    skill_name = db.Column(db.String(255), nullable=False)
    proficiency_level = db.Column(db.Integer, default=1)  # 1-5
    progress_percentage = db.Column(db.Float, default=0)  # 0-100
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
