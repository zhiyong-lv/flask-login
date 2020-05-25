from flask_restplus import Model, fields

from .commons import paginate_model

document_input = Model('Document Input', {
    'title': fields.String(required=True, description='The document title'),
    'content': fields.String(required=True, description='The document content'),
})

document_output = document_input.clone('Document', {
    'id': fields.String(required=True, description='The document identifier'),
    'creator_id': fields.String(required=True, description="The creaator's id"),
    'create_time': fields.String(required=True, description="The document create time"),
    'last_modify_time': fields.String(required=True, description="The document last update time"),
    'reversion': fields.String(required=True, description="The document reversion"),
})

documents_output = paginate_model.clone('DocumentList', {
    'items': fields.List(fields.Nested(document_output))
})
