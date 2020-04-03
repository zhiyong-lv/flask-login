from app import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    active = db.Column(db.Boolean)

    def __init__(self, username, email):
        self.username = username
        self.email = email
        self.active = False

    def is_active(self):
        return self.active

    def __repr__(self):
        return '<User {}>'.format(self.username)
