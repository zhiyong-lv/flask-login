import datetime

from sqlalchemy.dialects.mysql import INTEGER

from app import db


class Tag(db.Model):
    id = db.Column(INTEGER(unsigned=True), autoincrement=True, primary_key=True, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    creator_id = db.Column(INTEGER(unsigned=True))
    create_time = db.Column(db.DateTime, default=datetime.datetime.now)
    last_modify_time = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    valid = db.Column(db.Boolean(), nullable=False, default=True)
    reversion = db.Column(INTEGER(unsigned=True), default=1, nullable=False)

    __tablename__ = 'tags'
    __table_args__ = (
        db.UniqueConstraint('name', 'creator_id', name='unq_idx_name_creatorId'),
    )

    def __repr__(self):
        return '<Tag {}, creator id is {}>'.format(self.name, self.creator_id)
