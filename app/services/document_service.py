import logging

from app import db
from app.models import Document, User


class DocumentService:
    def __init__(self):
        self._logger = logging.getLogger(__name__)

    def get_documents(self, doc_id):
        try:
            document = Document.query.get(doc_id)
            return document
        except Exception as e:
            self._logger.exception(e)
            # TODO: change a more suitable exception
            raise e

    def modify_documents(self, doc_id, **kwargs):
        try:
            count = Document.query.filter(Document.id == doc_id).update(kwargs)
            self._logger.debug("count is {}".format(count))
            db.session.commit()
            if count > 0:
                document = Document.query.get(doc_id)
                return document
            else:
                # TODO: change to a more sensible exception.
                raise Exception()
        except Exception as e:
            self._logger.exception(e)
            # TODO: change a more suitable exception
            raise e

    def delete_documents(self, doc_id):
        try:
            document = Document.query.get(doc_id)
            if document is not None:
                db.session.delete(document)
                db.session.commit()
            else:
                # TODO: change a more suitable exception
                raise Exception()
        except Exception as e:
            self._logger.exception(e)
            # TODO: change a more suitable exception
            raise e

    def add_documents(self, title, content, creator_id):
        try:
            document = Document(title=title, content=content, creator_id=creator_id)
            db.session.add(document)
            db.session.commit()
            return document
        except Exception as e:
            self._logger.exception(e)
            # TODO: change a more suitable exception
            raise e

    def query_documents(self, offset, limit, creator=None, title=None):
        try:
            conditions = {}
            documents_fields = [Document.id, Document.title, Document.content, Document.creator_id,
                                Document.create_time, Document.last_modify_time, Document.reversion]
            documents_key = list(field.name for field in documents_fields)
            query = Document.query.with_entities(*documents_fields)
            if title is not None:
                conditions['creator'] = creator
                query = query.filter(Document.title.like("%{title}%".format(title=title)))
            if creator is not None:
                conditions['title'] = title
                query = query.filter(User.username.like("%{username}%".format(username=creator)))

            query = query.join(User, User.id == Document.creator_id)
            documents_list = query.offset(offset - 1).limit(limit).all()

            result = {
                'documents': list(dict(zip(documents_key, doc)) for doc in documents_list),
                'conditions': conditions,
                'count': query.count(),
                'limit': limit,
                'offset': offset,
            }
            return result
        except Exception as e:
            self._logger.exception(e)
            # TODO: change a more suitable exception
            raise e
        finally:
            self._logger.debug(query)
