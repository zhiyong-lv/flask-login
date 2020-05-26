from sqlalchemy.dialects.mysql import INTEGER

from app import db


class FileTag(db.Model):
    '''file_tags should be a multiple to multiple relationship table'''
    id = db.Column(INTEGER(unsigned=True), autoincrement=True, primary_key=True, nullable=False)
    file_uuid = db.Column(db.String(50), nullable=False, index=True)
    tag_id = db.Column(INTEGER(unsigned=True), nullable=False, index=True)

    __tablename__ = 'file_tags'

    # __table_args__ = (
    #     db.UniqueConstraint('tag_id', 'creator_id', name='unq_idx_name_creatorId'),
    # )

    def __repr__(self):
        return '<FileTag {}, file_uuid:tag_id is {}:{}>'.format(self.id, self.file_uuid, self.tag_id)
