import os
from flask import Flask, render_template, flash, request, redirect, url_for
# Various imports for the Flask application, including extensions
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from wtforms.widgets import TextArea
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import desc
import time

# Initializing Flask app and configurations
app = Flask(__name__, static_folder="static")
## Database (switched from sqlite)##
# app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

app.config ['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:12345678@public-database.ckceiladqgeo.us-east-1.rds.amazonaws.com/our_users'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
## Login Management ##

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'f_login'
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

## User Info ##
class Users(db.Model, UserMixin):
# Various fields for Users table and related methods

    id = db.Column(db.Integer, primary_key=True) 
    username = db.Column(db.String(20), nullable=False, unique=True)
    name = db.Column(db.String(200), nullable=False) 
    email = db.Column(db.String(120), nullable=False, unique=True)
    favorite_color = db.Column(db.String(120))
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
    
## Forms ##
app.config['SECRET_KEY'] = "4x786kj4fRt98jIq"
class Posts(db.Model):
# Fields for the Posts model
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    author = db.Column(db.String(255))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    slug = db.Column(db.String(255))

class PostForm(FlaskForm):
# Form for posting content
    title = StringField("Course", validators=[DataRequired()])
    content = StringField("Content", validators=[DataRequired()], widget=TextArea())
    author = StringField("Reviewer", validators=[DataRequired()])
    slug = StringField("Rating", validators=[DataRequired()])
    submit = SubmitField("Submit")

class UserForm(FlaskForm):
# Form for user data
    name = StringField("Name", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    favorite_color = StringField("University")
    password_hash = PasswordField('Password', validators=[DataRequired(), EqualTo('password_hash2', message='passwords must match')])
    password_hash2 = PasswordField('Confirm password', validators=[DataRequired()]) # not in db, just to verify
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

with app.app_context():
    db.create_all()

## Routes ##
@app.route('/') # Root

# Starting page
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

# Register user
@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            hashed_pw = generate_password_hash(form.password_hash.data, "sha256")
            user = Users(username=form.username.data, name=form.name.data, email=form.email.data, favorite_color=form.favorite_color.data, password_hash=hashed_pw)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.username.data =''
        form.email.data = ''
        form.favorite_color.data = ''
        form.password_hash = ''
        flash("Registration completed")
    # our_users = Users.query.order_by(Users.date_added)
    return render_template("login.html", form=form)
    # return render_template("add_user.html", form=form, name=name, our_users=our_users)

# Post a review
@app.route('/add-post', methods=['GET', 'POST'])
@login_required
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Posts(title=form.title.data, content=form.content.data, author=form.author.data, slug=form.slug.data)
        form.title.data = ''
        form.content.data = ''
        form.author.data = ''
        form.slug.data = ''
        db.session.add(post)
        db.session.commit() 
        flash("Your review is now posted")
    return render_template("add_post.html", form=form)

# View all users' posts 
@app.route('/posts')
def posts():
	
    posts = Posts.query.order_by(Posts.date_posted)
    return render_template("posts.html", posts=posts)

# View a single post
@app.route('/posts/<int:id>')
def post(id):
    post = Posts.query.get_or_404(id)
    return render_template('post.html', post=post)

# Edit review
@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    post = Posts.query.get_or_404(id)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.author = form.author.data
        post.slug = form.slug.data
        post.content = form.content.data
        db.session.add(post)
        db.session.commit()
        flash("Review updated")
        return redirect(url_for('post', id=post.id))
    form.title.data = post.title
    form.author.data = post.author
    form.slug.data = post.slug
    form.content.data = post.content
    return render_template('edit_post.html', form=form)

# Delete a review
@app.route('/posts/delete/<int:id>')
@login_required
def delete_post(id):
    post_to_delete = Posts.query.get_or_404(id)
    try:
        db.session.delete(post_to_delete)
        db.session.commit()
        flash("Review deleted")
        posts = Posts.query.order_by(Posts.date_posted)
        return render_template("posts.html", posts=posts)
    except:
        flash("Deletion failed")
        posts = Posts.query.order_by(Posts.date_posted)
        return render_template("posts.html", posts=posts)

# Change Profile Info
@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.favorite_color = request.form['favorite_color']
        name_to_update.username = request.form['username']
        try:
            db.session.commit()
            flash("Profile is up to date")
            return render_template("update.html", 
                form=form,
                name_to_update = name_to_update, id=id)
        except:
            flash("Update failed")
            return render_template("update.html", 
                form=form,
                name_to_update = name_to_update,
                id=id)
    else:
        return render_template("update.html", 
                form=form,
                name_to_update = name_to_update,
                id = id)

# Delete account
@app.route('/delete/<int:id>')
@login_required
def delete(id):
    if id == current_user.id:
        user_to_delete = Users.query.get_or_404(id)
        name = None
        form = UserForm()

        try:
            db.session.delete(user_to_delete)
            db.session.commit()
            flash("User profile deleted")

            our_users = Users.query.order_by(Users.date_added)
            return render_template("add_user.html", 
            form=form,
            name=name,
            our_users=our_users)

        except:
            flash("Whoops! There was a problem deleting user, try again...")
            return render_template("add_user.html", 
            form=form, name=name,our_users=our_users)
    else:
        flash("Deletion failed")
        return redirect(url_for('dashboard'))

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

# Login / logout
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                flash("You are now logged in")
                return redirect(url_for('dashboard'))
            else:
                flash("Incorrect password")
        else:
            flash("No such user exists")

    return render_template('login.html', form=form)
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
    return render_template('dashboard.html', form=form)






# F_ADD_POST
@app.route('/f_add_post', methods=['GET', 'POST'])
@login_required
def f_add_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Posts(title=form.title.data, content=form.content.data, author=form.author.data, slug=form.slug.data)
        form.title.data = ''
        form.content.data = ''
        form.author.data = ''
        form.slug.data = ''
        db.session.add(post)
        db.session.commit() 
        flash("Your review is now posted")
    return render_template("f_add_post.html", form=form)

# F_ADD_PROFESSOR
@app.route('/user/f_addProfessor', methods=['GET', 'POST'])
def f_addProfessor():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            hashed_pw = generate_password_hash(form.password_hash.data, "sha256")
            user = Users(username=form.username.data, name=form.name.data, email=form.email.data, favorite_color=form.favorite_color.data, password_hash=hashed_pw)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.username.data =''
        form.email.data = ''
        form.favorite_color.data = ''
        form.password_hash = ''
        flash("Registration completed")
    our_users = Users.query.order_by(Users.date_added)
    return render_template("f_addProfessor.html", form=form, name=name, our_users=our_users)


# F_ADD_STUDENT
@app.route('/user/f_addStudent', methods=['GET', 'POST'])
def f_addStudent():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            hashed_pw = generate_password_hash(form.password_hash.data, "sha256")
            user = Users(username=form.username.data, name=form.name.data, email=form.email.data, favorite_color=form.favorite_color.data, password_hash=hashed_pw)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.username.data =''
        form.email.data = ''
        form.favorite_color.data = ''
        form.password_hash = ''
        flash("Registration completed")
    our_users = Users.query.order_by(Users.date_added)
    return render_template("f_addStudent.html", form=form, name=name, our_users=our_users)
    # return render_template("login.html")

# F_POSTS
@app.route('/f_posts')
def f_posts():
    posts = Posts.query.order_by(Posts.date_posted.desc())
    return render_template("f_posts.html", posts=posts)
# F_DASHBOARD
@app.route('/f_dashboard', methods=['GET', 'POST'])
@login_required
def f_dashboard():
    form = LoginForm()
    return render_template('f_dashboard.html', form=form)

# F_LOGIN
@app.route('/f_login', methods=['GET','POST'])
def f_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                flash("You are now logged in")
                return redirect(url_for('f_dashboard'))
            else:
                flash("Incorrect password")
        else:
            flash("No such user exists")
    return render_template('f_login.html', form=form)
#F_LOGOUT
@app.route('/f_logout', methods= ['GET', 'POST'])
@login_required
def f_logout():
    logout_user()
    flash("You are now logged out")
    return redirect(url_for('f_login'))

# F_DELETE
@app.route('/f_delete/<int:id>')
@login_required
def f_delete(id):
    if id == current_user.id:
        user_to_delete = Users.query.get_or_404(id)
        name = None
        form = UserForm()

        try:
            db.session.delete(user_to_delete)
            db.session.commit()
            flash("User profile deleted")

            our_users = Users.query.order_by(Users.date_added)
            return render_template("add_user.html", 
            form=form,
            name=name,
            our_users=our_users)

        except:
            flash("Whoops! There was a problem deleting user, try again...")
            return render_template("add_user.html", 
            form=form, name=name,our_users=our_users)
    else:
        flash("Deletion failed")
        return redirect(url_for('f_dashboard'))

# F_UPDATE
@app.route('/f_update/<int:id>', methods=['GET', 'POST'])
@login_required
def f_update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.favorite_color = request.form['favorite_color']
        name_to_update.username = request.form['username']
        try:
            db.session.commit()
            flash("Profile is up to date")
            return render_template("f_update.html", 
                form=form,
                name_to_update = name_to_update, id=id)
        except:
            flash("Update failed")
            return render_template("f_update.html", 
                form=form,
                name_to_update = name_to_update,
                id=id)
    else:
        return render_template("f_update.html", 
                form=form,
                name_to_update = name_to_update,
                id = id)

# F_POST
@app.route('/f_posts/<int:id>')
def f_post(id):
    post = Posts.query.get_or_404(id)
    return render_template('f_post.html', post=post)

# F_EDIT_POST
@app.route('/f_posts/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def f_edit_post(id):
    post = Posts.query.get_or_404(id)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.author = form.author.data
        post.slug = form.slug.data
        post.content = form.content.data
        db.session.add(post)
        db.session.commit()
        flash("Review updated")
        return redirect(url_for('f_post', id=post.id))
    form.title.data = post.title
    form.author.data = post.author
    form.slug.data = post.slug
    form.content.data = post.content
    return render_template('f_edit_post.html', form=form)

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

@app.route('/search', methods=['POST'])
def search():
    form = SearchForm()
    posts = Posts.query
    if form.validate_on_submit():
        post.searched = form.searched.data
        posts = posts.filter(Posts.title.like('%' + post.searched + '%'))
        posts = posts.order_by(Posts.date_posted.desc()).all()

        posts2 = Posts.query.filter(Posts.content.like('%' + post.searched + '%'))
        posts2 = posts2.order_by(Posts.date_posted.desc()).all()
        return render_template('search.html', form=form, searched=post.searched, posts=posts, posts2=posts2)
    
# F_PROFESSORS
@app.route('/f_professors')
def f_professors():
    posts = Posts.query.order_by(Posts.date_posted.desc())
    return render_template("f_professors.html", posts=posts)

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
@app.route('/f_class/<string:course>', methods = ['GET'])
def f_class(course):
    posts = Posts.query.order_by(Posts.date_posted.desc())
    return render_template("f_class.html", posts=posts, course=course)

if __name__ == '__main__':
    app.run(debug=True)
