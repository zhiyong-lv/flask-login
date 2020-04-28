import datetime

from sqlalchemy.dialects.mysql import TINYINT, BIGINT, INTEGER

from app import db


class File(db.Model):
    uuid = db.Column(db.String(50), primary_key=True, nullable=False)
    file_name = db.Column(db.String(200), nullable=False)
    file_size = db.Column(BIGINT(unsigned=True), nullable=False)
    status = db.Column(TINYINT(unsigned=True), nullable=False, default=0)
    valid = db.Column(db.Boolean(), nullable=False, default=True)
    creator_id = db.Column(INTEGER(unsigned=True))
    create_time = db.Column(db.DateTime, default=datetime.datetime.now)
    last_modify_time = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    reversion = db.Column(INTEGER(unsigned=True), default=1, nullable=False)

    __tablename__ = 'files'
    __table_args__ = (
        db.UniqueConstraint('file_name', 'creator_id', name='unq_idx_fileName_creatorId'),
    )

    def __repr__(self):
        return '<File {}, size is {}>'.format(self.file_name, self.file_size)
