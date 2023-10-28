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
from models import Students, Professors, Class, Professor


def get_class_description(course_name):
    class_info = Class.query.filter_by(name=course_name).first()
    if class_info:
        return class_info.description
    else:
        return "Class description not found"
    
def get_prof_description(prof_name):
    prof_info = Professor.query.filter_by(name=prof_name).first()
    if prof_info:
        return prof_info.description
    else:
        return "Professor description not found"


#determines whether user is student or professor
def determine_user_role(username):
    # Function to determine the user's role based on the username's existence
    # in the students or professors table
    if Students.query.filter_by(username=username).first():
        return 'student'
    elif Professors.query.filter_by(username=username).first():
        return 'professor'
    return None  # Unknown role  
    