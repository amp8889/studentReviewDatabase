import os
from flask import Flask, render_template, flash, request, redirect, url_for, session, abort
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
from routes import main_bp


#  Initializing Flask app and configurations
app = Flask(__name__, static_folder="static")

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:TRZFxAXg015C7lg@ipro2.ckceiladqgeo.us-east-1.rds.amazonaws.com/our_users'
app.config['SECRET_KEY'] = "4x786kj4fRt98jIq"
db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(main_bp)
#

with app.app_context():
    db.create_all()

## Login Management ##
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'main.f_login'



@login_manager.user_loader
def load_user(user_id):
    return Students.query.get(int(user_id)) or Professors.query.get(int(user_id))

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

@app.route('/test-500')
def test_500():
    raise Exception("This is a test exception for a 500 error.")

@app.errorhandler(500)
def internal_server_error(e):
    # You can log the error here if you like
    # log.exception('An internal server error occurred.')
    return render_template('500.html'), 500



if __name__ == '__main__':
    app.run(debug=False)
