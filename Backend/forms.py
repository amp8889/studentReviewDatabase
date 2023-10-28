from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo
from wtforms.widgets import TextArea

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