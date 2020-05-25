import logging

from flask import request
from flask_login import login_required, current_user
from flask_restplus import Namespace, Resource, abort

from app.services import DocumentService
from .models.commons import paginate as paginate_parser
from .models.documents import document_input, document_output, documents_output

_logger = logging.getLogger(__name__)

api = Namespace('documents', path='/documents', description='Home Page')
api.models[document_input.name] = document_input
api.models[document_output.name] = document_output
api.models[documents_output.name] = documents_output
document_service = DocumentService()


@api.route('/')
@api.response(500, 'Internal error')
@api.response(400, 'Validation error')
@api.response(401, 'UNAUTHORIZED')
class Documents(Resource):
    @api.doc('query_documents', security='apikey')
    @api.expect(paginate_parser, validate=True)
    @api.marshal_list_with(documents_output)
    @login_required
    def get(self):
        """Query documents"""
        return document_service.query_documents(**paginate_parser.parse_args())

    @api.doc('create_document', security='apikey')
    @api.expect(document_input, validate=True)
    @api.response(201, 'CREATED', document_output)
    @login_required
    def post(self):
        """Create a new documents"""
        document = document_service.add_documents(request.json, creator_id=current_user.id)
        _logger.info(document)
        return document


@api.route('/<int:doc_id>')
@api.response(500, 'Internal error')
@api.response(400, 'Validation error')
@api.response(401, 'UNAUTHORIZED')
@api.response(404, 'Not Found')
class Document(Resource):
    @api.doc('get_document', security='apikey')
    @api.marshal_with(document_output)
    @login_required
    def get(self, doc_id):
        document = document_service.get_documents(doc_id)
        if document is None:
            abort(404)
        return document

    @api.doc('modify_document', security='apikey')
    @api.expect(document_input, validate=True)
    @api.marshal_with(document_output)
    @login_required
    def put(self, doc_id):
        document = document_service.modify_documents(request.json, doc_id=doc_id)
        if document is None:
            abort(404)
        return document

    @api.doc('delete_document', security='apikey')
    @login_required
    def delete(self, doc_id):
        try:
            document_service.delete_documents(doc_id)
        # TODO: Change exception to a more suitable Exception
        except Exception:
            abort(404)
