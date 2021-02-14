import json
import logging
import os
import tempfile

from tinydb import TinyDB, Query
from tinydb.middlewares import CachingMiddleware
from functools import reduce
import uuid

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from swagger_server.models import Student

db_dir_path = tempfile.gettempdir()
db_file_path = os.path.join(db_dir_path, "students.json")
student_db = TinyDB(db_file_path)

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://///Users/ta/Desktop/projects/Python/python-flask-server/student.db'
db = SQLAlchemy(app)


class StudentTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)

def add_student(student):
    queries = []
    query = Query()
    queries.append(query.first_name == student.first_name)
    queries.append(query.last_name == student.last_name)
    query = reduce(lambda a, b: a & b, queries)
    res = student_db.search(query)
    if res:
        return 'already exists', 409

    doc_id = student_db.insert(student.to_dict())
    student.student_id = doc_id
    return student.student_id


def get_student_by_id(student_id, subject):
    try:
        student = student_db.get(doc_id=int(student_id))
        print(student)
    except ValueError:
        return 'not found', 404
    if not student:
        raise ValueError
    student = Student.from_dict(student)

    if (subject and student.grades) and not subject in student.grades.keys():
            raise ValueError
    return student

def delete_student(student_id):
    student = student_db.get(doc_id=int(student_id))
    if not student:
        return student
    student_db.remove(doc_ids=[int(student_id)])
    return student_id
