from flask_restplus import reqparse, fields


def generate_document_input_parser():
    document_input_parser = reqparse.RequestParser()
    document_input_parser.add_argument('title', location='json', help='The document title')
    document_input_parser.add_argument('content', location='json', help='The document content')
    return document_input_parser


def generate_document_output_model(api):
    pass
    # document_output = api.model('Document', {
    #     'title': fields.String(required=True, description='The document title'),
    #     'content': fields.String(required=True, description='The document content'),
    #     'id': fields.String(required=True, description='The document identifier'),
    #     'creator_id': fields.String(required=True, description="The creaator's id"),
    #     'create_time': fields.String(required=True, description="The document create time"),
    #     'last_modify_time': fields.String(required=True, description="The document last update time"),
    #     'reversion': fields.String(required=True, description="The document reversion"),
    # })
    # return document_output


def generate_documents_output_model(api, document):
    pass
    # documents_output = api.model('DocumentList', {
    #     'documents': fields.List(fields.Nested(document)),
    #     'limit': fields.Integer(required=True, description='The max document count which should be returned once.'),
    #     'offset': fields.Integer(required=True, description='The document begin number'),
    #     'count': fields.Integer(required=True, description='The document count'),
    # })
    # return documents_output
