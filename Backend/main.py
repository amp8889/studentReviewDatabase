from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'  # SQLite database file
db = SQLAlchemy(app)

# Define the Student model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    major = db.Column(db.String(100), nullable=False)
    studentID = db.Column(db.String(20), unique=True, nullable=False)
    birthdate = db.Column(db.String(10), nullable=False)
    school = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __init__(self, name, email, major, studentID, birthdate, school, password):
        self.name = name
        self.email = email
        self.major = major
        self.studentID = studentID
        self.birthdate = birthdate
        self.school = school
        self.password = password

if __name__ == '__main__':
    # Create the database and the "students" table
    db.create_all()
    app.run(debug=True)
