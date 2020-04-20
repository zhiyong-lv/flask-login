import logging

from flask_login import login_required, current_user
from flask_restplus import Namespace, Resource, fields, abort, reqparse

from app.services import DocumentService
from .parsers import generate_paginate_parser, generate_document_input_parser

_logger = logging.getLogger(__name__)

api = Namespace('documents', path='/documents', description='Home Page')
document_service = DocumentService()
paginate_parser = generate_paginate_parser('document')
document_input_parser = generate_document_input_parser()

document_reversion_parser = reqparse.RequestParser()
document_reversion_parser.add_argument('reversion', location='args', help='The document reversion')

document_input = api.model('Document Input', {
    'title': fields.String(required=True, description='The document title'),
    'content': fields.String(required=True, description='The document content'),
}, mask='title,content')
document_output = api.model('Document', {
    'title': fields.String(required=True, description='The document title'),
    'content': fields.String(required=True, description='The document content'),
    'id': fields.String(required=True, description='The document identifier'),
    'creator_id': fields.String(required=True, description="The creaator's id"),
    'create_time': fields.String(required=True, description="The document create time"),
    'last_modify_time': fields.String(required=True, description="The document last update time"),
    'reversion': fields.String(required=True, description="The document reversion"),
})
documents_output = api.model('DocumentList', {
    'documents': fields.Nested(document_output),
    'limit': fields.Integer(required=True, description='The max document count which should be returned once.'),
    'offset': fields.Integer(required=True, description='The document begin number'),
    'count': fields.Integer(required=True, description='The document count'),
})


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
        args = paginate_parser.parse_args()
        try:
            offset = int(args.get('offset'))
        except TypeError:
            offset = 1

        try:
            limit = int(args.get('limit'))
        except TypeError:
            limit = 20
        documents = document_service.query_documents(offset=offset, limit=limit)
        _logger.debug(documents)
        return documents

    @api.doc('create_document', security='apikey')
    @api.expect(document_input, validate=True)
    @api.marshal_with(document_output)
    @login_required
    def post(self):
        """Create a new documents"""
        args = document_input_parser.parse_args()
        document = document_service.add_documents(title=args.get('title'), content=args.get('content'),
                                                  creator_id=current_user.id)
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
        args = document_input_parser.parse_args()
        _logger.debug(args)
        document = document_service.modify_documents(doc_id=doc_id,
                                                     title=args.get('title'),
                                                     content=args.get('content'))
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
