from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password_hash = db.Column(db.String(120))
    email = db.Column(db.String(120), unique=True)
    active = db.Column(db.Boolean)
    creator = db.Column(db.String(80))

    def __init__(self, username=None, email=None):
        self.username = username
        self.email = email
        self.active = False

    @property
    def password(self):
        # TODO: Change Exception to another more suitable exception.
        raise Exception()

    @password.setter
    def password(self, pw):
        self.password_hash = generate_password_hash(pw)

    def verify(self, pw):
        '''verify input password'''
        return check_password_hash(self.password_hash, pw)

    @property
    def is_active(self):
        return self.active

    def __repr__(self):
        return '<User {}>'.format(self.username)
