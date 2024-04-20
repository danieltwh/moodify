from flask import Flask, request, jsonify, session, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from extensions import db, login_manager, app




@login_manager.user_loader
def user_loader(id):
    return User.query.get(id)

class User(db.Model, UserMixin):
    __tablename__='users'
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    firstname = db.Column(db.String(80), nullable=False)
    lastname = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    salt = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    # 0 for Admin, 1 for Data Dcientise, 2 or Data Engineers, 3 for DevOps Engineers
    # 4 for Business Analytics, 5 for Project Managers
    role = db.Column(db.String(80), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    github_id = db.Column(db.String(80), default=None)
    github_credentials = db.Column(db.String(150), default=None)


    def __repr__(self):
        return '<User %r>' % self.firstname

    def __init__(self, firstname, lastname, email, salt, password, role, date_created, github_id, github_credentials):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.salt = salt
        self.password = password
        self.role = role
        self.date_created = date_created
        self.github_id = github_id
        self.github_credentials = github_credentials


    def serialize(self):
        return {
            "id": self.id,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,
            "salt": self.salt, 
            "password": self.password,
            "role": self.role,
            "date_created": self.date_created,
            "github_id" : self.github_id,
            "github_credentials" : self.github_credentials,
        }
