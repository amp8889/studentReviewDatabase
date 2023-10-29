import os
from flask import Flask, render_template, flash, request, redirect, url_for, session
# Various imports for the Flask application, including extensions
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError, SelectField,TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from wtforms.widgets import TextArea
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import desc
from sqlalchemy.orm import relationship
import time
db = SQLAlchemy()

class Students(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True) 
    username = db.Column(db.String(20), nullable=False, unique=True)
    name = db.Column(db.String(200), nullable=False,index=True) 
    email = db.Column(db.String(120), nullable=False, unique=True)
    birthday = db.Column(db.Date, nullable=False)  # Add the birthday field
    major = db.Column(db.String(100), nullable=False)  # Add the major field
    student_id = db.Column(db.String(10), nullable=False, unique=True)  # Add the student ID field
    school_id = db.Column(db.String(10), nullable=False)
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

    id = db.Column(db.Integer, primary_key=True,autoincrement=True) 
    username = db.Column(db.String(20), nullable=False, unique=True)
    name = db.Column(db.String(200), nullable=False) 
    email = db.Column(db.String(120), nullable=False, unique=True)
    birthday = db.Column(db.Date, nullable=False)  # Add the birthday field
    teacher_id = db.Column(db.String(10), nullable=False, unique=True)  # Add the student ID field
    school_id = db.Column(db.String(10), nullable=False) 
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
    



# Table for Class models
class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    class_name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    # posts = db.relationship('Class_Posts', backref='course', lazy=True)



#Table for Professor models
class Professor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    # posts = db.relationship('Professor_Posts', backref='professor', lazy=True)



class Class_Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    class_name = db.Column(db.String(255))
    content = db.Column(db.Text)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    professor_name = db.Column(db.String(255))
    rating = db.Column(db.String(255))
    student_name = db.Column(db.String(200), db.ForeignKey('students.name'))


    
class Professor_Posts(db.Model):
# Fields for the Professor Review model
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    professor_name = db.Column(db.String(255))
    class_name = db.Column(db.String(255))
    content = db.Column(db.Text)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    rating = db.Column(db.String(255))
    student_name = db.Column(db.String(200), db.ForeignKey('students.name'))
    