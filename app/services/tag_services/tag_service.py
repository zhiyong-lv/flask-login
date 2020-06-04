from app import db
from app.models import Tag, File, FileTag
from app.schema.file_schemas import file_schema
from app.schema.file_tag_schema import file_tag_map_schema
from app.schema.tag_schema import tag_schema
from app.services.exceptions import NotFound, BaseError
from ..base_service import BaseService


class TagService(BaseService):
    def __init__(self):
        super(TagService, self).__init__()

    def add(self, **kwargs):
        try:
            tag = tag_schema.load(kwargs, partial=("name", "creator_id"))

            tags = Tag.query.filter(
                db.and_(Tag.creator_id == kwargs.get('creator_id'), Tag.name == kwargs.get('name'))).all()
            if len(tags) == 1:
                return tag_schema.dump(tags[0])
            elif len(tags) > 1:
                raise BaseError(message="tag:{} is duplicated, and length is {}".format(tag, len(tags)))

            db.session.add(tag)
            db.session.commit()
            return tag_schema.dump(tag)
        except Exception as e:
            self._logger.exception(e)
            db.session.rollback()
            raise

    def delete(self, id, creator_id, **kwargs):
        try:
            tag = Tag.query.filter(db.and_(Tag.id == id, Tag.creator_id == creator_id)).first()
            if tag is None:
                raise NotFound(message="tag:{} is not found".format(id))

            db.session.delete(tag)
            db.session.commit()
            return tag_schema.dump(tag)
        except Exception as e:
            self._logger.exception(e)
            db.session.rollback()
            raise BaseError

    def query(self, creator_id, page=None, per_page=None, error_out=True, max_per_page=None, **kwargs):
        try:
            result = Tag.query.filter(Tag.creator_id == creator_id).paginate(page=page, per_page=per_page,
                                                                             error_out=error_out,
                                                                             max_per_page=max_per_page)
            db.session.commit()
            return result
        except Exception as e:
            db.session.rollback()
            self._logger.exception(e)
            raise BaseError

    def map_file(self, tag_id, file_uuid, **kwargs):
        try:
            file_tag = file_tag_map_schema.load({'tag_id': tag_id, 'file_uuid': file_uuid},
                                                partial=("tag_id", 'file_uuid'))

            tag = Tag.query.filter(db.and_(Tag.id == file_tag.tag_id, Tag.valid == True)).first()
            if tag is None:
                raise NotFound(message="tag:{} is not found".format(file_tag.tag_id))

            file = File.query.filter(db.and_(File.uuid == file_uuid, File.valid == True)).first()
            if file is None:
                raise NotFound(message="file:{} is not found".format(file_tag.file_uuid))

            self._logger.debug('{} type is {}'.format(file_tag, type(file_tag)))
            db.session.add(file_tag)
            db.session.commit()
            return file_tag_map_schema.dump(file_tag)
        except Exception as e:
            self._logger.exception(e)
            db.session.rollback()
            raise BaseError

    def query_file_tags(self, file_uuid, **kwargs):
        try:
            file_schema.load({'uuid': file_uuid}, partial=("uuid",))
            result = Tag.query.join(FileTag, db.and_(Tag.id == FileTag.tag_id, FileTag.file_uuid == file_uuid)).all()
            # db.session.commit()
            return result
        except Exception as e:
            # db.session.rollback()
            self._logger.exception(e)
            raise BaseError
