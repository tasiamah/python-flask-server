from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://///Users/ta/Desktop/projects/Python/python-flask-server/student.db'
db = SQLAlchemy(app)


class StudentTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
