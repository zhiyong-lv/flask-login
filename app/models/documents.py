import datetime

from sqlalchemy.dialects.mysql import LONGTEXT

from app import db


class Document(db.Model):
    __tablename__ = 'documents'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True)
    content = db.Column(LONGTEXT)
    creator_id = db.Column(db.Integer)
    create_time = db.Column(db.DateTime, default=datetime.datetime.now)
    last_modify_time = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    reversion = db.Column(db.Integer, default=1)

    def __repr__(self):
        return '<Document {}>'.format(self.title)
