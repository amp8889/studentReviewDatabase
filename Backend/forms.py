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


class ProfessorReviewForm(FlaskForm):
    class_name = StringField('Professor Name', validators=[DataRequired()])
    rating = SelectField('Rating', choices=[('5', '5 - Excellent'), ('4', '4 - Very Good'), ('3', '3 - Average'), ('2', '2 - Poor'), ('1', '1 - Terrible')], validators=[DataRequired()])
    review_content = TextAreaField('Your Review', validators=[DataRequired()])
    submit = SubmitField('Submit Professor Review')
    
class ClassReviewForm(FlaskForm):
    professor_name = StringField('Professor Name', validators=[DataRequired()])
    rating = SelectField('Rating', choices=[('5', '5 - Excellent'), ('4', '4 - Very Good'), ('3', '3 - Average'), ('2', '2 - Poor'), ('1', '1 - Terrible')], validators=[DataRequired()])
    review_content = TextAreaField('Your Review', validators=[DataRequired()])
    submit = SubmitField('Submit Class Review')

class addProfessorForm(FlaskForm):
    name = StringField('Professor Name', validators=[DataRequired()])
    description= StringField('Description', validators=[DataRequired()])


class addClassForm(FlaskForm):
    name = StringField('Class Number(ex; CS422)', validators=[DataRequired()])
    class_name = StringField('Class Name', validators=[DataRequired()])
    description= StringField('Description', validators=[DataRequired()])
    


class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    birthday = StringField("Birthday", validators=[DataRequired()])  # Adjust field type as needed
    major = StringField("Major", validators=[DataRequired()])
    student_id = StringField("Student ID", validators=[DataRequired()])
    school_id = StringField("School ID", validators=[DataRequired()])
    password_hash = PasswordField('Password', validators=[DataRequired(), EqualTo('password_hash2', message='Passwords must match')])
    password_hash2 = PasswordField('Confirm Password', validators=[DataRequired()])  # Not in the database, just for password confirmation
    submit = SubmitField("Submit")

class ProfForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    birthday = StringField("Birthday", validators=[DataRequired()])  # Adjust field type as needed
    teacher_id = StringField("Teacher ID", validators=[DataRequired()])
    school_id = StringField("School ID", validators=[DataRequired()])
    password_hash = PasswordField('Password', validators=[DataRequired(), EqualTo('password_hash2', message='Passwords must match')])
    password_hash2 = PasswordField('Confirm Password', validators=[DataRequired()])  # Not in the database, just for password confirmation
    submit = SubmitField("Submit")
    
    
class NamerForm(FlaskForm):
# A simple form with a single field
    name = StringField("", validators=[DataRequired()])
    submit = SubmitField("Submit")

class PasswordForm(FlaskForm):
# Form to test passwords
    email = StringField("Enter your email", validators=[DataRequired()])
    password_hash = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")

class LoginForm(FlaskForm):
# Form for user login
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")