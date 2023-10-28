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

# Initializing Flask app and configurations
app = Flask(__name__, static_folder="static")
## Database (switched from sqlite)##
# app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

app.config ['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:12345678@public-database.ckceiladqgeo.us-east-1.rds.amazonaws.com/our_users'
db = SQLAlchemy(app)
## Login Management ##

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'f_login'
# @login_manager.user_loader
# def load_user(user_id):
#     return Users.query.get(int(user_id))
@login_manager.user_loader
def load_user(user_id):
    return Students.query.get(int(user_id)) or Professors.query.get(int(user_id))

# @login_manager.user_loader
# def load_user(user_id):
#     student = Students.query.filter_by(username=user_id).first()
#     professor = Professors.query.filter_by(username=user_id).first()

#     if student:
#         return student
#     elif professor:
#         return professor
#     else:
#         return None

# class Users(db.Model, UserMixin):
# # Various fields for Students table and related methods

#     id = db.Column(db.Integer, primary_key=True) 
#     username = db.Column(db.String(20), nullable=False, unique=True)
#     name = db.Column(db.String(200), nullable=False) 
#     email = db.Column(db.String(120), nullable=False, unique=True)
#     favorite_color = db.Column(db.String(120))
#     date_added = db.Column(db.DateTime, default=datetime.utcnow)
    
#     password_hash = db.Column(db.String(128))
#     @property
#     def password(self):
#         raise AttributeError('password is not a readable attribute')
#     @password.setter
#     def password(self, password):
#         self.password_hash = generate_password_hash(password)
#     def verify_password(self, password):
#         return check_password_hash(self.password_hash, password)

#     def __repr__(self):
#         return '<Name %r>' % self.name

## Forms ##
# app.config['SECRET_KEY'] = "4x786kj4fRt98jIq"
# class Posts(db.Model):
# # Fields for the Posts model
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(255))
#     content = db.Column(db.Text)
#     author = db.Column(db.String(255))
#     date_posted = db.Column(db.DateTime, default=datetime.utcnow)
#     slug = db.Column(db.String(255))

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
    


app.config['SECRET_KEY'] = "4x786kj4fRt98jIq"
# Table for Class models
class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
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

# class PostForm(FlaskForm):
# # Form for posting content
#     title = StringField("Course", validators=[DataRequired()])
#     content = StringField("Content", validators=[DataRequired()], widget=TextArea())
#     author = StringField("Reviewer", validators=[DataRequired()])
#     slug = StringField("Rating", validators=[DataRequired()])
#     submit = SubmitField("Submit")

# class UserForm(FlaskForm):
# # Form for user data
#     name = StringField("Name", validators=[DataRequired()])
#     username = StringField("Username", validators=[DataRequired()])
#     email = StringField("Email", validators=[DataRequired()])
#     favorite_color = StringField("University")
#     password_hash = PasswordField('Password', validators=[DataRequired(), EqualTo('password_hash2', message='passwords must match')])
#     password_hash2 = PasswordField('Confirm password', validators=[DataRequired()]) # not in db, just to verify
#     submit = SubmitField("Submit")


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


#determines whether user is student or professor
def determine_user_role(username):
    # Function to determine the user's role based on the username's existence
    # in the students or professors table
    if Students.query.filter_by(username=username).first():
        return 'student'
    elif Professors.query.filter_by(username=username).first():
        return 'professor'
    return None  # Unknown role  
    


## Routes ##
@app.route('/') # Root

@app.route('/')
def index():
    first_name = "John"
    return render_template("index.html", first_name=first_name)

# Invalid route(s) or server error
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500

# Testing
@app.route('/name', methods=['GET', 'POST'])
def name():
    name = None 
    form = NamerForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ""
        flash("Submission complete")
    return render_template("name.html", name=name, form=form)

# # Register user
# @app.route('/user/add', methods=['GET', 'POST'])
# def add_user():
#     name = None
#     form = UserForm()
#     if form.validate_on_submit():
#         user = Users.query.filter_by(email=form.email.data).first()
#         if user is None:
#             hashed_pw = generate_password_hash(form.password_hash.data, "sha256")
#             user = Users(username=form.username.data, name=form.name.data, email=form.email.data, favorite_color=form.favorite_color.data, password_hash=hashed_pw)
#             db.session.add(user)
#             db.session.commit()
#         name = form.name.data
#         form.name.data = ''
#         form.username.data =''
#         form.email.data = ''
#         # form.favorite_color.data = ''
#         form.password_hash = ''
#         flash("Registration completed")
#     # our_users = Users.query.order_by(Users.date_added)
#     return render_template("login.html", form=form)
#     # return render_template("add_user.html", form=form, name=name, our_users=our_users)

# Post a review
# @app.route('/add-post', methods=['GET', 'POST'])
# @login_required
# def add_post():
#     form = PostForm()
#     if form.validate_on_submit():
#         post = Posts(title=form.title.data, content=form.content.data, author=form.author.data, slug=form.slug.data)
#         form.title.data = ''
#         form.content.data = ''
#         form.author.data = ''
#         form.slug.data = ''
#         db.session.add(post)
#         db.session.commit() 
#         flash("Your review is now posted")
#     return render_template("add_post.html", form=form)

# # View all users' posts 
# @app.route('/posts')
# def posts():
#     posts = Posts.query.order_by(Posts.date_posted)
#     return render_template("posts.html", posts=posts)

# # View a single post
# @app.route('/posts/<int:id>')
# def post(id):
#     post = Posts.query.get_or_404(id)
#     return render_template('post.html', post=post)

# Edit review
# @app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
# @login_required
# def edit_post(id):
#     post = Posts.query.get_or_404(id)
#     form = PostForm()
#     if form.validate_on_submit():
#         post.title = form.title.data
#         post.author = form.author.data
#         post.slug = form.slug.data
#         post.content = form.content.data
#         db.session.add(post)
#         db.session.commit()
#         flash("Review updated")
#         return redirect(url_for('post', id=post.id))
#     form.title.data = post.title
#     form.author.data = post.author
#     form.slug.data = post.slug
#     form.content.data = post.content
#     return render_template('edit_post.html', form=form)

# # Delete a review
# @app.route('/posts/delete/<int:id>')
# @login_required
# def delete_post(id):
#     post_to_delete = Posts.query.get_or_404(id)
#     try:
#         db.session.delete(post_to_delete)
#         db.session.commit()
#         flash("Review deleted")
#         posts = Posts.query.order_by(Posts.date_posted)
#         return render_template("posts.html", posts=posts)
#     except:
#         flash("Deletion failed")
#         posts = Posts.query.order_by(Posts.date_posted)
#         return render_template("posts.html", posts=posts)
from flask import abort

@app.route('/f_users_posts/delete/<string:post_type>/<int:post_id>')
@login_required
def delete_post(post_type, post_id):
    # Ensure post_type is either 'class' or 'professor' to determine which type of post to delete
    print(post_type)
    print(post_id)
    if post_type == 'class':
        print("classssew")
        post = Class_Posts.query.get(post_id)
        print(post)
    elif post_type == 'professor':
        print("prof")
        post = Professor_Posts.query.get(post_id)
        print(post)


    # Check if the current user is the author of the post
    # Delete the post
    if post and post.student_name == current_user.name:
        # Delete the post
        db.session.delete(post)
        db.session.commit()
        flash("Post deleted", "success")
    else:
        abort(403)

    # Redirect to the user's posts page
    return redirect(url_for('f_dashboard'))



# Change Profile Info
# @app.route('/update/<int:id>', methods=['GET', 'POST'])
# @login_required
# def update(id):
#     form = UserForm()
#     name_to_update = Users.query.get_or_404(id)
#     if request.method == "POST":
#         name_to_update.name = request.form['name']
#         name_to_update.email = request.form['email']
#         name_to_update.favorite_color = request.form['favorite_color']
#         name_to_update.username = request.form['username']
#         try:
#             db.session.commit()
#             flash("Profile is up to date")
#             return render_template("update.html", 
#                 form=form,
#                 name_to_update = name_to_update, id=id)
#         except:
#             flash("Update failed")
#             return render_template("update.html", 
#                 form=form,
#                 name_to_update = name_to_update,
#                 id=id)
#     else:
#         return render_template("update.html", 
#                 form=form,
#                 name_to_update = name_to_update,
#                 id = id)

# Delete account
# @app.route('/delete/<int:id>')
# @login_required
# def delete(id):
#     if id == current_user.id:
#         user_to_delete = Users.query.get_or_404(id)
#         name = None
#         form = UserForm()

#         try:
#             db.session.delete(user_to_delete)
#             db.session.commit()
#             flash("User profile deleted")

#             our_users = Users.query.order_by(Users.date_added)
#             return render_template("add_user.html", 
#             form=form,
#             name=name,
#             our_users=our_users)

#         except:
#             flash("Whoops! There was a problem deleting user, try again...")
#             return render_template("add_user.html", 
#             form=form, name=name,our_users=our_users)
#     else:
#         flash("Deletion failed")
#         return redirect(url_for('dashboard'))

# Testing passwords
@app.route('/test_pw', methods=['GET', 'POST'])
def test_pw():
    email = None
    password = None
    pw_to_check = None
    passed = None
    form = PasswordForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password_hash.data
        form.email.data = ""
        form.password_hash.data = ""

        pw_to_check = Users.query.filter_by(email=email).first()

        passed = check_password_hash(pw_to_check.password_hash, password)

    return render_template("test_pw.html", email=email, password=password, pw_to_check=pw_to_check, passed=passed, form=form)

# # Login / logout
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = Users.query.filter_by(username=form.username.data).first()
#         if user:
#             if check_password_hash(user.password_hash, form.password.data):
#                 login_user(user)
#                 flash("You are now logged in")
#                 return redirect(url_for('dashboard'))
#             else:
#                 flash("Incorrect password")
#         else:
#             flash("No such user exists")

#     return render_template('login.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        role = determine_user_role(username)
        form.role.data = role 

        if role == 'student':
            user = Students.query.filter_by(username=form.username.data).first()
        elif role == 'professor':
            user = Professors.query.filter_by(username=form.username.data).first()

        if user:
            if check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                flash("You are now logged in")
                return redirect(url_for('dashboard'))
            else:
                flash("Incorrect password")
        else:
            flash("No such user exists")
    
    return render_template("login.html", form=form)

@app.route('/logout', methods= ['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("You are now logged out")
    return redirect(url_for('f_login'))

# Profile
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = LoginForm()
    return render_template('dashboard', form=form)






# # F_ADD_POST
# @app.route('/f_add_post', methods=['GET', 'POST'])
# @login_required
# def f_add_post():
#     form = PostForm()
#     if form.validate_on_submit():
#         post = Posts(title=form.title.data, content=form.content.data, author=form.author.data, slug=form.slug.data)
#         form.title.data = ''
#         form.content.data = ''
#         form.author.data = ''
#         form.slug.data = ''
#         db.session.add(post)
#         db.session.commit() 
#         flash("Your review is now posted")
#     return render_template("f_add_post.html", form=form)

# # F_ADD_PROFESSOR
# @app.route('/user/f_addProfessor', methods=['GET', 'POST'])
# def f_addProfessor():
#     name = None
#     form = UserForm()
#     if form.validate_on_submit():
#         user = Users.query.filter_by(email=form.email.data).first()
#         if user is None:
#             hashed_pw = generate_password_hash(form.password_hash.data, "sha256")
#             user = Users(username=form.username.data, name=form.name.data, email=form.email.data, favorite_color=form.favorite_color.data, password_hash=hashed_pw)
#             db.session.add(user)
#             db.session.commit()
#         name = form.name.data
#         form.name.data = ''
#         form.username.data =''
#         form.email.data = ''
#         form.favorite_color.data = ''
#         form.password_hash = ''
#         flash("Registration completed")
#     our_users = Users.query.order_by(Users.date_added)
#     return render_template("f_addProfessor.html", form=form, name=name, our_users=our_users)

@app.route('/f_addProfessor', methods=['GET', 'POST'])
def f_addProfessor():
    name = None
    form = ProfForm()  # Assuming the UserForm is updated to include the necessary fields for professors

    if form.validate_on_submit():
        user = Professors.query.filter_by(email=form.email.data).first()  # Use Professors model
        if user is None:
            hashed_pw = generate_password_hash(form.password_hash.data, "sha256")
            user = Professors(
                username=form.username.data,
                name=form.name.data,
                email=form.email.data,
                birthday=form.birthday.data,  # Add the birthday field
                teacher_id=form.teacher_id.data,  # Add the teacher_id field
                school_id=form.school_id.data,
                password_hash=hashed_pw
            )
            db.session.add(user)
            db.session.commit()

            name = form.name.data
            form.name.data = ''
            form.username.data = ''
            form.email.data = ''
            form.birthday.data = ''
            form.teacher_id.data = ''
            form.school_id.data = ''
            form.password_hash.data = ''

            flash("Professor registration completed")
            return redirect(url_for('f_login'))

    return render_template("f_addProfessor.html", form=form, name=name)


# F_ADD_STUDENT
# @app.route('/user/f_addStudent', methods=['GET', 'POST'])
# def f_addStudent():
#     name = None
#     form = UserForm()
#     if form.validate_on_submit():
#         user = Users.query.filter_by(email=form.email.data).first()
#         if user is None:
#             hashed_pw = generate_password_hash(form.password_hash.data, "sha256")
#             user = Users(username=form.username.data, name=form.name.data, email=form.email.data, favorite_color=form.favorite_color.data, password_hash=hashed_pw)
#             db.session.add(user)
#             db.session.commit()
#         name = form.name.data
#         form.name.data = ''
#         form.username.data =''
#         form.email.data = ''
#         form.favorite_color.data = ''
#         form.password_hash = ''
#         flash("Registration completed")
#     our_users = Users.query.order_by(Users.date_added)
#     return render_template("f_addStudent.html", form=form, name=name, our_users=our_users)
    # return render_template("login.html")
    
@app.route('/f_addStudent', methods=['GET', 'POST'])
def f_addStudent():
    name = None
    form = UserForm()  # Assuming the UserForm is updated to include the necessary fields for students

    if form.validate_on_submit():
        user = Students.query.filter_by(email=form.email.data).first()  # Use Students model
        if user is None:
            hashed_pw = generate_password_hash(form.password_hash.data, "sha256")
            user = Students(
                username=form.username.data,
                name=form.name.data,
                email=form.email.data,
                birthday=form.birthday.data,  # Add the birthday field
                major=form.major.data,  # Add the major field
                student_id=form.student_id.data,
                school_id=form.school_id.data,
                password_hash=hashed_pw
            )
            db.session.add(user)
            db.session.commit()

            name = form.name.data
            form.name.data = ''
            form.username.data = ''
            form.email.data = ''
            form.birthday.data = ''
            form.major.data = ''
            form.student_id.data = ''
            form.school_id.data = ''
            form.password_hash.data = ''

            flash("Student registration completed")
            return redirect(url_for('f_login'))

    return render_template("f_addStudent.html", form=form, name=name)
    # return render_template("login.html")

# # F_POSTS
# @app.route('/f_posts')
# def f_posts():
#     posts = Posts.query.order_by(Posts.date_posted.desc())
#     return render_template("f_posts.html", posts=posts)


# F_DASHBOARD
@app.route('/f_dashboard', methods=['GET', 'POST'])
@login_required
def f_dashboard():
    form = LoginForm()
    user_role = session.get('user_role', None)
    return render_template('f_dashboard.html', form=form,user_role=user_role)

# # F_LOGIN
# @app.route('/f_login', methods=['GET','POST'])
# def f_login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = Users.query.filter_by(username=form.username.data).first()
#         if user:
#             if check_password_hash(user.password_hash, form.password.data):
#                 login_user(user)
#                 flash("You are now logged in")
#                 return redirect(url_for('f_dashboard'))
#             else:
#                 flash("Incorrect password")
#         else:
#             flash("No such user exists")
#     return render_template('f_login.html', form=form)
# @app.route('/f_login', methods=['GET', 'POST'])
# def f_login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         student = Students.query.filter_by(username=form.username.data).first()
#         professor = Professors.query.filter_by(username=form.username.data).first()
#         user_role = "student" if Students.query.filter_by(username=form.username.data).first() else "professor"
#         session['user_role'] = user_role
#         print(user_role)
#         if student and check_password_hash(student.password_hash, form.password.data):
#             login_user(student)
#             flash("You are now logged in as a student")
#             return redirect(url_for('f_dashboard'))
#         elif professor and check_password_hash(professor.password_hash, form.password.data):
#             login_user(professor)
#             flash("You are now logged in as a professor")
#             return redirect(url_for('f_dashboard'))
#         else:
#             flash("Incorrect username or password")

#     return render_template('f_login.html', form=form)
@app.route('/f_login', methods=['GET', 'POST'])
def f_login():
    form = LoginForm()
    if form.validate_on_submit():
        student = Students.query.filter_by(username=form.username.data).first()
        professor = Professors.query.filter_by(username=form.username.data).first()
        if student and check_password_hash(student.password_hash, form.password.data):
            login_user(student)
            user_role = "student"
            session['user_role'] = user_role
            print(user_role)
            flash("You are now logged in as a student")
            return redirect(url_for('f_dashboard', user_role=user_role))
        elif professor and check_password_hash(professor.password_hash, form.password.data):
            login_user(professor)
            user_role = "professor"
            session['user_role'] = user_role
            print(user_role)
            flash("You are now logged in as a professor")
            return redirect(url_for('f_dashboard', user_role=user_role))
        else:
            flash("Incorrect username or password")
    return render_template('f_login.html', form=form)

#F_LOGOUT
@app.route('/f_logout', methods= ['GET', 'POST'])
@login_required
def f_logout():
    logout_user()
    flash("You are now logged out")
    return redirect(url_for('f_login'))

# # F_DELETE
# @app.route('/f_delete/<int:id>')
# @login_required
# def f_delete(id):
#     if id == current_user.id:
#         user_to_delete = Users.query.get_or_404(id)
#         name = None
#         form = UserForm()

#         try:
#             db.session.delete(user_to_delete)
#             db.session.commit()
#             flash("User profile deleted")

#             our_users = Users.query.order_by(Users.date_added)
#             return render_template("add_user.html", 
#             form=form,
#             name=name,
#             our_users=our_users)

#         except:
#             flash("Whoops! There was a problem deleting user, try again...")
#             return render_template("add_user.html", 
#             form=form, name=name,our_users=our_users)
#     else:
#         flash("Deletion failed")
#         return redirect(url_for('f_dashboard'))
# F_DELETE
# F_DELETE
@app.route('/f_delete/<int:id>')
@login_required
def f_delete(id):
    if id == current_user.id:
        # Determine user_type based on the id
        user_to_delete = Students.query.get(id)
        if user_to_delete is None:
            user_to_delete = Professors.query.get(id)

        if user_to_delete:
            # Determine user type and select the appropriate form
            if isinstance(user_to_delete, Students):
                user_type = 'student'
                user_id = user_to_delete.id
                form = UserForm()
            elif isinstance(user_to_delete, Professors):
                user_id = user_to_delete.id
                user_type = 'professor'
                form = ProfForm()
            else:
                flash("Invalid user type")
                return redirect(url_for('some_error_route'))
        else:
            flash("User not found")
            return redirect(url_for('some_error_route'))

        try:
            db.session.delete(user_to_delete)
            db.session.commit()
            flash("User profile deleted")

            # Redirect to a suitable template
            return redirect(url_for('f_dashboard'))

        except Exception as e:
            flash("Whoops! There was a problem deleting the user, try again...")
            return redirect(url_for('f_dashboard'))
    else:
        flash("Deletion failed")
        return redirect(url_for('f_dashboard'))


# F_UPDATE
# @app.route('/f_update/<int:id>', methods=['GET', 'POST'])
# @login_required
# def f_update(id):
#     form = UserForm()
#     name_to_update = Users.query.get_or_404(id)
#     if request.method == "POST":
#         name_to_update.name = request.form['name']
#         name_to_update.email = request.form['email']
#         name_to_update.favorite_color = request.form['favorite_color']
#         name_to_update.username = request.form['username']
#         try:
#             db.session.commit()
#             flash("Profile is up to date")
#             return render_template("f_update.html", 
#                 form=form,
#                 name_to_update = name_to_update, id=id)
#         except:
#             flash("Update failed")
#             return render_template("f_update.html", 
#                 form=form,
#                 name_to_update = name_to_update,
#                 id=id)
#     else:
#         return render_template("f_update.html", 
#                 form=form,
#                 name_to_update = name_to_update,
#                 id = id)
# Update route for both students and professors

@app.route('/f_update/<int:id>', methods=['GET', 'POST'])
@login_required
def f_update(id):
    # Determine user_type based on the id
    user_to_update = Students.query.get(int(id))
    print(user_to_update)
    if user_to_update is None:
        user_to_update = Professors.query.get(int(id))

    if user_to_update:
        if isinstance(user_to_update, Students):
            user_type = 'student'
            user_id = user_to_update.id
            form = UserForm()
        elif isinstance(user_to_update, Professors):
            user_id = user_to_update.id
            user_type = 'professor'
            form = ProfForm()
        else:
            flash("Invalid user type")
            return redirect(url_for('some_error_route'))
    else:
        flash("User not found")
        return redirect(url_for('some_error_route'))

    if request.method == "POST":
        try:
            if user_type == 'student':
                # Update user information for students
                user_to_update.name = form.name.data
                user_to_update.email = form.email.data
                user_to_update.school_id = form.school_id.data
                user_to_update.username = form.username.data
                user_to_update.student_id = form.student_id.data
                user_to_update.major = form.major.data
            elif user_type == 'professor':
                # Update user information for professors
                user_to_update.name = form.name.data
                user_to_update.email = form.email.data
                user_to_update.teacher_id = form.teacher_id.data
                user_to_update.username = form.username.data
                user_to_update.school_id = form.school_id.data

            db.session.commit()
            flash("Profile is up to date")
            return redirect(url_for('f_dashboard'))
        except Exception as e:
            flash("Update failed: " + str(e))
    
    return render_template("f_update.html", form=form, user_to_update=user_to_update, id=id, user_type=user_type)







# F_POST
@app.route('/f_posts/<int:id>')
def f_post(id):
    post = Posts.query.get_or_404(id)
    return render_template('f_post.html', post=post)

# F_EDIT_POST
# @app.route('/f_posts/edit/<int:id>', methods=['GET', 'POST'])
# @login_required
# def f_edit_post(id):
#     post = Posts.query.get_or_404(id)
#     form = PostForm()
#     if form.validate_on_submit():
#         post.title = form.title.data
#         post.author = form.author.data
#         post.slug = form.slug.data
#         post.content = form.content.data
#         db.session.add(post)
#         db.session.commit()
#         flash("Review updated")
#         return redirect(url_for('f_post', id=post.id))
#     form.title.data = post.title
#     form.author.data = post.author
#     form.slug.data = post.slug
#     form.content.data = post.content
#     return render_template('f_edit_post.html', form=form)
# Edit and update a review (class or professor)
# Edit and update a review (class or professor)
@app.route('/edit_post/<post_type>/<int:id>', methods=['GET', 'POST'])
def f_edit_post(post_type, id):
    post = None

    if post_type == 'class':
        is_professor_review = False
        post = Class_Posts.query.get_or_404(id)
        form = ClassReviewForm()
    elif post_type == 'professor':
        is_professor_review = True
        post = Professor_Posts.query.get_or_404(id)
        form = ProfessorReviewForm()
    else:
        flash("Invalid post type")
        return redirect(url_for('f_dashboard'))

    if form.validate_on_submit():
        if post_type == 'class':
            post.professor_name = form.professor_name.data
        elif post_type == 'professor':
            post.class_name = form.class_name.data
        post.rating = form.rating.data
        post.content = form.review_content.data
        db.session.commit()
        flash("Review updated")
        return redirect(url_for('f_dashboard'))

    is_professor_review = (post_type == 'professor')
    return render_template('f_edit_post.html', form=form, is_professor_review=is_professor_review)



# F_HELP
@app.route('/f_help')
def f_help():
    return render_template('f_help.html')


#SEARCH
@app.context_processor
def base():
    form = SearchForm()
    return dict(form=form)


class SearchForm(FlaskForm):
    searched = StringField("Searched", validators=[DataRequired()])
    submit = SubmitField("Submit")

# @app.route('/search', methods=['POST'])
# def search():
#     form = SearchForm()
#     posts = Posts.query
#     if form.validate_on_submit():
#         post.searched = form.searched.data
#         posts = posts.filter(Posts.title.like('%' + post.searched + '%'))
#         posts = posts.order_by(Posts.date_posted.desc()).all()

#         posts2 = Posts.query.filter(Posts.content.like('%' + post.searched + '%'))
#         posts2 = posts2.order_by(Posts.date_posted.desc()).all()
#         return render_template('search.html', form=form, searched=post.searched, posts=posts, posts2=posts2)
from sqlalchemy import or_

@app.route('/search', methods=['POST'])
def search():
    form = SearchForm()
    search_query = form.searched.data
    professor_results = Professor.query.filter(or_(
        Professor.name.like(f'%{search_query}%'),
    )).all()
    
    class_results = Class.query.filter(or_(
        Class.name.like(f'%{search_query}%'),
        Class.description.like(f'%{search_query}%')
    )).all()
    
    results = [{'id': professor.id, 'name': professor.name, 'type': 'Professor'} for professor in professor_results]
    results.extend([{'id': course.id, 'name': course.name, 'type': 'Course'} for course in class_results])

    return render_template('search.html', form=form, searched=search_query, results=results)

    
# # F_PROFESSORS
# @app.route('/f_professors')
# def f_professors():
#     posts = Posts.query.order_by(Posts.date_posted.desc())
#     return render_template("f_professors.html", posts=posts)
@app.route('/f_professors', defaults={'professor_name': None})
@app.route('/f_professors/<professor_name>', methods=['GET', 'POST'])
def f_professors(professor_name):
    form = ProfessorReviewForm()
    if professor_name is not None:
        # Retrieve the class description based on the course_name
        description = get_prof_description(professor_name)
        if form.validate_on_submit():
            class_name = form.class_name.data
            rating = form.rating.data
            review_content = form.review_content.data
            student = current_user.name
            new_post = Professor_Posts(
                    class_name=class_name,
                    professor_name=professor_name,
                    rating=rating,
                    content=review_content,
                    student_name=student  # Associate the review with the current student
                )
            db.session.add(new_post)
            db.session.commit()
            form.class_name.data = ''
            form.rating.data = ''
            form.review_content.data = ''

        # Save the review to the database or perform other necessary actions
        # You can create a Review model and save the review data to the database here
        reviews = Professor_Posts.query.filter_by(professor_name=professor_name).all()
        
    else:
        description = None  # Set to None for a blank page
        reviews = []

    return render_template('f_professors.html', prof_description=description, professor_name=professor_name, form=form, reviews=reviews)

# F_POST_DELETE
@app.route('/posts/f_post_delete/<int:id>')
@login_required
def f_post_delete(id):
    post_to_delete = Posts.query.get_or_404(id)
    try:
        db.session.delete(post_to_delete)
        db.session.commit()
        flash("Review deleted")
        posts = Posts.query.order_by(Posts.date_posted)
        return render_template("f_posts.html", posts=posts)
    except:
        flash("Deletion failed")
        posts = Posts.query.order_by(Posts.date_posted)
        return render_template("f_posts.html", posts=posts)

# F_CLASS
# @app.route('/f_class/<string:course>', methods = ['GET'])
# def f_class(course):
#     posts = Posts.query.order_by(Posts.date_posted.desc())
#     return render_template("f_class.html", posts=posts, course=course)
from flask_login import current_user

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
    
    
@app.route('/f_class', defaults={'course_name': None})
@app.route('/f_class/<course_name>', methods=['GET', 'POST'])
def f_class(course_name):
    form = ClassReviewForm()
    if course_name is not None:
        # Retrieve the class description based on the course_name
        description = get_class_description(course_name)
        if form.validate_on_submit():
            professor_name = form.professor_name.data
            rating = form.rating.data
            review_content = form.review_content.data
            student = current_user.name
            new_post = Class_Posts(
                    class_name=course_name,
                    professor_name=professor_name,
                    rating=rating,
                    content=review_content,
                    student_name=student  # Associate the review with the current student
                )
            db.session.add(new_post)
            db.session.commit()
            form.professor_name.data = ''
            form.rating.data = ''
            form.review_content.data = ''

        # Save the review to the database or perform other necessary actions
        # You can create a Review model and save the review data to the database here
        reviews = Class_Posts.query.filter_by(class_name=course_name).all()


    else:
        description = None  # Set to None for a blank page
        reviews = []

    return render_template('f_class.html', course_description=description, course_name=course_name, form=form, reviews=reviews)

@app.route('/f_users_posts/<username>')
@login_required  # Requires the user to be logged in
def f_users_posts(username):
    # Query the database to get the user's posts from both tables
    user = Students.query.filter_by(username=username).first()
    if user:
        class_posts = Class_Posts.query.filter_by(student_name=user.name).all()
        professor_posts = Professor_Posts.query.filter_by(student_name=user.name).all()
        return render_template('f_users_posts.html', user=user, class_posts=class_posts, professor_posts=professor_posts)
    else:
        # Handle the case when the user doesn't exist
        flash('User not found', 'danger')
        return redirect(url_for('index'))  # Redirect to the homepage or another appropriate page




with app.app_context():
    db.create_all()

if __name__ == '__main__':
    migrate = Migrate(app, db)

    app.run(debug=True)
