import logging

from app import db
from app.models import Document, User
from app.schema.document_schema import doc_schema


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

    def modify_documents(self, doc_json, doc_id):
        try:
            input_doc = doc_schema.load(doc_json, partial=("title", "content"))
            doc = Document.query.filter_by(id=doc_id).with_for_update().first()
            doc.title = input_doc.title
            doc.content = input_doc.content
            db.session.commit()
            return doc
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

    def add_documents(self, json, creator_id):
        try:
            doc = doc_schema.load(json, partial=("title", "content"))
            doc.creator_id = creator_id
            # document = Document(title=doc.title, content=doc.content, creator_id=creator_id)
            db.session.add(doc)
            db.session.commit()
            return doc_schema.dump(doc)
        except Exception as e:
            self._logger.exception(e)
            # TODO: change a more suitable exception
            raise e

    def query_documents(self, page, per_page, error_out=None, max_per_page=None, creator=None, title=None):
        try:
            conditions = {}
            query = Document.query
            if title is not None:
                conditions['creator'] = creator
                query = query.filter(Document.title.like("%{title}%".format(title=title)))
            if creator is not None:
                conditions['title'] = title
                query = query.filter(User.username.like("%{username}%".format(username=creator)))
                query = query.outerjoin(User, User.id == Document.creator_id)

            return query.paginate(page=page, per_page=per_page, error_out=error_out,
                                  max_per_page=max_per_page)
        except Exception as e:
            self._logger.exception(e)
            # TODO: change a more suitable exception
            raise e
        finally:
            self._logger.debug(query)
