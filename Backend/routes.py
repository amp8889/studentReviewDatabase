import os
from flask import Flask, render_template, flash, request, redirect, url_for, session, abort, Blueprint
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
from models import *
from functions import *
from forms import *


main_bp = Blueprint('main', __name__)
## Routes ##
@main_bp.route('/') # Root
def default():
    return redirect(url_for('main.f_login'))


@main_bp.route('/index') #Homepage
def index():
    reviews_table1 = Professor_Posts.query.order_by(Professor_Posts.rating.desc()).limit(5).all()
    reviews_table2 = Class_Posts.query.order_by(Class_Posts.rating.desc()).limit(5).all()
    return render_template('index.html', professor_posts=reviews_table1, class_posts=reviews_table2)


# Invalid route(s) or server error
@main_bp.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404
@main_bp.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500


@main_bp.route('/f_users_posts/delete/<string:post_type>/<int:post_id>')
@login_required
def delete_post(post_type, post_id):
    if post_type == 'class':
        post = Class_Posts.query.get(post_id)
    elif post_type == 'professor':
        post = Professor_Posts.query.get(post_id)


    # Check if the current user is the author of the post
    # Delete the post
    if post and post.student_name == current_user.name:
        # Delete the post
        db.session.delete(post)
        db.session.commit()
        # flash("Post deleted", "success")
    else:
        abort(403)

    # Redirect to the user's posts page
    return redirect(url_for('main.f_dashboard'))


@main_bp.route('/login', methods=['GET', 'POST'])
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
                # flash("You are now logged in")
                return redirect(url_for('dashboard'))
            else:
                flash("Incorrect password")
        else:
            flash("No such user exists")
    
    return render_template("login.html", form=form)

@main_bp.route('/logout', methods= ['GET', 'POST'])
@login_required
def logout():
    user_role = session.get('user_role')
    print(user_role)  # For debugging purposes
    
    # Remove user_role from the session when the user logs out
    session.pop('user_role', None)
    user_role = session.get('user_role')
    print(user_role)  # For debugging purposes
    # flash("You are now logged out")
    return redirect(url_for('main.f_login'))

# Profile
@main_bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = LoginForm()
    return render_template('dashboard', form=form)


@main_bp.route('/f_addProfessor', methods=['GET', 'POST'])
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

            # flash("Professor registration completed")
            return redirect(url_for('main.f_login'))

    return render_template("f_addProfessor.html", form=form, name=name)


    
@main_bp.route('/main.f_addstudent', methods=['GET', 'POST'])
def f_addstudent():
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

            # flash("Student registration completed")
            return redirect(url_for('main.f_login'))

    return render_template("f_addstudent.html", form=form, name=name)
    # return render_template("login.html")



# F_DASHBOARD
@main_bp.route('/f_dashboard', methods=['GET', 'POST'])
@login_required
def f_dashboard():
    form = LoginForm()
    user_role = session.get('user_role', None)
    return render_template('f_dashboard.html', form=form,user_role=user_role)


@main_bp.route('/f_login', methods=['GET', 'POST'])
def f_login():
    form = LoginForm()
    if form.validate_on_submit():
        student = Students.query.filter_by(username=form.username.data).first()
        professor = Professors.query.filter_by(username=form.username.data).first()
        if student and check_password_hash(student.password_hash, form.password.data):
            login_user(student)
            user_role = "student"
            session['user_role'] = user_role
            # flash("You are now logged in as a student")
            return redirect(url_for('main.f_dashboard', user_role=user_role))
        elif professor and check_password_hash(professor.password_hash, form.password.data):
            login_user(professor)
            user_role = "professor"
            session['user_role'] = user_role
            # flash("You are now logged in as a professor")
            return redirect(url_for('main.f_dashboard', user_role=user_role))
        else:
            flash("Incorrect username or password")
    return render_template('f_login.html', form=form)

#F_LOGOUT
@main_bp.route('/f_logout', methods= ['GET', 'POST'])
@login_required
def f_logout():
    session.pop('user_role', None)
    print(session.user_role)
    logout_user()
    # flash("You are now logged out")
    return redirect(url_for('main.f_login'))


# F_DELETE
@main_bp.route('/f_delete/<int:id>')
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
                # flash("Invalid user type")
                return redirect(url_for('some_error_route'))
        else:
            # flash("User not found")
            return redirect(url_for('some_error_route'))

        try:
            db.session.delete(user_to_delete)
            db.session.commit()
            # flash("User profile deleted")

            # Redirect to a suitable template
            return redirect(url_for('main.f_dashboard'))

        except Exception as e:
            # flash("Whoops! There was a problem deleting the user, try again...")
            return redirect(url_for('main.f_dashboard'))
    else:
        # flash("Deletion failed")
        return redirect(url_for('main.f_dashboard'))



@main_bp.route('/f_update/<int:id>', methods=['GET', 'POST'])
@login_required
def f_update(id):
    # Determine user_type based on the id
    user_to_update = Students.query.get(int(id))
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
            # flash("Invalid user type")
            return redirect(url_for('some_error_route'))
    else:
        # flash("User not found")
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
            # flash("Profile is up to date")
            return redirect(url_for('main.f_dashboard'))
        except Exception as e:
            flash("Update failed: " + str(e))
    
    return render_template("f_update.html", form=form, user_to_update=user_to_update, id=id, user_type=user_type)


@main_bp.route('/edit_post/<post_type>/<int:id>', methods=['GET', 'POST'])
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
        # flash("Invalid post type")
        return redirect(url_for('main.f_dashboard'))

    if form.validate_on_submit():
        if post_type == 'class':
            post.professor_name = form.professor_name.data
        elif post_type == 'professor':
            post.class_name = form.class_name.data
        post.rating = form.rating.data
        post.content = form.review_content.data
        db.session.commit()
        # flash("Review updated")
        return redirect(url_for('main.f_dashboard'))

    is_professor_review = (post_type == 'professor')
    return render_template('f_edit_post.html', form=form, is_professor_review=is_professor_review)

@main_bp.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

@main_bp.route('/ourmission')
def ourMission():
    return render_template('ourMission.html')

@main_bp.route('/contactus')
def contactUs():
    return render_template('contactUs.html')

@main_bp.route('/futureplans')
def futurePlans():
    return render_template('futurePlans.html')

# F_HELP
@main_bp.route('/f_help')
def f_help():
    return render_template('f_help.html')


#SEARCH
@main_bp.context_processor
def base():
    form = SearchForm()
    return dict(form=form)


class SearchForm(FlaskForm):
    searched = StringField("Searched", validators=[DataRequired()])
    submit = SubmitField("Submit")


from sqlalchemy import or_

@main_bp.route('/search', methods=['POST'])
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
    
    results = [{'id': professor.id, 'name': professor.name, 'type': 'Professor', 'description': professor.description} for professor in professor_results]
    results.extend([{'id': course.id, 'name': course.name, 'type': 'Course', 'description':course.description, 'class_name': course.class_name} for course in class_results])

    return render_template('search.html', form=form, searched=search_query, results=results)

    

@main_bp.route('/f_professors', defaults={'professor_name': None, 'searched': None})
@main_bp.route('/f_professors/<professor_name>/<searched>', methods=['GET', 'POST'])
def f_professors(professor_name,searched):
    form = ProfessorReviewForm()
    search_boolean = False
    if searched == "True": 
        search_boolean = True
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

        #  Save the review to the database or perform other necessary actions
        # You can create a Review model and save the review data to the database here
        reviews = Professor_Posts.query.filter_by(professor_name=professor_name).all()
        
    else:
        description = None  # Set to None for a blank page
        reviews = []
        
    professors = Professor.query.order_by(Professor.id)
    return render_template('f_professors.html', prof_description=description, professor_name=professor_name, form=form, reviews=reviews, professors=professors,searched=search_boolean)

    
@main_bp.route('/f_class', defaults={'course_name': None, 'searched': None})
@main_bp.route('/f_class/<course_name>/<searched>', methods=['GET', 'POST'])
def f_class(course_name,searched):
    form = ClassReviewForm()
    search_boolean = False
    if searched == "True": 
        search_boolean = True
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
        course_list = Class.query.order_by(Class.id)

        return render_template('f_class.html', course_description=description, course_name=course_name, form=form, reviews=reviews,course_list=course_list,searched=search_boolean)


    else:
        description = None  # Set to None for a blank page
        course_list = Class.query.order_by(Class.id)    
        reviews = []
        return render_template('f_class.html', course_description=description, course_name=course_name, form=form,reviews=reviews, course_list=course_list,searched=search_boolean)

@main_bp.route('/f_users_posts/<username>')
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
        # flash('User not found', 'danger')
        return redirect(url_for('main.index'))  # Redirect to the homepage or another appropriate page

@main_bp.route('/addProfessor', methods=['GET', 'POST'])
@login_required
def addProfessor():
    form = addProfessorForm()
    if form.validate_on_submit():
            professor = Professor(
                name=form.name.data,
                description=form.description.data,
            )
            db.session.add(professor)
            db.session.commit()

            form.name.data = ''
            form.description.data = ''
            return redirect(url_for('main.addProfessor'))

    return render_template("addProfessor.html", form=form)


@login_required
@main_bp.route('/addClass', methods=['GET', 'POST'])
def addClass():
    form = addClassForm()
    if form.validate_on_submit():
            c = Class(
                name=form.name.data,
                description=form.description.data,
                class_name=form.class_name.data
            )
            db.session.add(c)
            db.session.commit()

            form.name.data = ''
            form.description.data = ''
            form.class_name.data = ''
            return redirect(url_for('main.addClass'))

    return render_template("addClass.html", form=form)

# @main_bp.before_request
# def before_request():
#     if not current_user.is_authenticated and request.endpoint != 'main.f_login':
#         return redirect(url_for('main.f_login'))
    # else:
    #     # Log the user out automatically
    #     f_logout()
