from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Students(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True) 
    username = db.Column(db.String(20), nullable=False, unique=True)
    name = db.Column(db.String(200), nullable=False) 
    email = db.Column(db.String(120), nullable=False, unique=True)
    birthday = db.Column(db.Date, nullable=False)  # Add the birthday field
    major = db.Column(db.String(100), nullable=False)  # Add the major field
    student_id = db.Column(db.String(10), nullable=False, unique=True)  # Add the student ID field
    school_id = db.Column(db.String(10), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    
    password_hash = db.Column(db.String(128))
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Name %r>' % self.name
    
    ## User Info ##
class Professors(db.Model, UserMixin):
# Various fields for Professors table and related methods

    id = db.Column(db.Integer, primary_key=True) 
    username = db.Column(db.String(20), nullable=False, unique=True)
    name = db.Column(db.String(200), nullable=False) 
    email = db.Column(db.String(120), nullable=False, unique=True)
    birthday = db.Column(db.Date, nullable=False)  # Add the birthday field
    teacher_id = db.Column(db.String(10), nullable=False, unique=True)  # Add the student ID field
    school_id = db.Column(db.String(10), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    
    password_hash = db.Column(db.String(128))
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Name %r>' % self.name

    
with app.app_context():
    db.create_all()