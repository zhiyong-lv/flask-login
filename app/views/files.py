import logging

from flask_login import login_required, current_user
from flask_restplus import Namespace, Resource, fields, abort, reqparse

from app.services import FileServices
from app.services.file_services.exceptions import FileNotFound

_logger = logging.getLogger(__name__)

api = Namespace('files', path='/files', description='File Management')
file_service = FileServices()
paginate_parser = reqparse.RequestParser()
paginate_parser.add_argument('page', location='args', help='The page begin number')
paginate_parser.add_argument('per_page', location='args', help='The number in every page')

file_input = api.model('File Input', {
    'file_name': fields.String(required=True, description='The file name'),
    'file_size': fields.String(required=True, description='The file size'),
    'reversion': fields.String(description='The file reversion'),
}, mask='file_name,file_size,reversion')

file_input_parser = reqparse.RequestParser()
file_input_parser.add_argument('file_name', location='json', help='The file name')
file_input_parser.add_argument('file_size', location='json', help='The file size')
file_input_parser.add_argument('reversion', location='json', help='The reversion number')

file_output = api.model('File', {
    'uuid': fields.String(required=True, description='The file uuid and the unique identifier of file'),
    'file_name': fields.String(required=True, description='The file name'),
    'file_size': fields.String(required=True, description='The file size'),
    'status': fields.String(required=True, description='The file status'),
    'creator_id': fields.String(required=True, description="The creaator's id"),
    'create_time': fields.String(required=True, description="The document create time"),
    'last_modify_time': fields.String(required=True, description="The document last update time"),
    'reversion': fields.String(required=True, description="The document reversion"),
})
files_output = api.model('FileList', {
    'items': fields.Nested(file_output),
    'per_page': fields.Integer(required=True, description='The max document count which should be returned once.'),
    'page': fields.Integer(required=True, description='The file page begin number'),
    'total': fields.Integer(required=True, description='The document total count'),
})


@api.route('/')
@api.response(500, 'Internal error')
@api.response(400, 'Validation error')
@api.response(401, 'UNAUTHORIZED')
class Fils(Resource):
    @api.doc('query_files', security='apikey')
    @api.expect(paginate_parser, validate=True)
    @api.marshal_list_with(files_output)
    @login_required
    def get(self):
        """Query files"""
        args = paginate_parser.parse_args()
        try:
            page = int(args.get('page'))
        except TypeError:
            page = 1

        try:
            per_page = int(args.get('per_page'))
        except TypeError:
            per_page = 20
        files = file_service.query(page=page, per_page=per_page)
        return files

    @api.doc('create_file', security='apikey')
    @api.expect(file_input, validate=True)
    @api.marshal_with(file_output)
    @login_required
    def post(self):
        """Create a new file"""
        args = file_input_parser.parse_args()
        document = file_service.add_file(file_size=args.get('file_size'), file_name=args.get('file_name'),
                                         user_id=current_user.id)
        return document


@api.route('/<string:uuid>')
@api.response(500, 'Internal error')
@api.response(400, 'Validation error')
@api.response(401, 'UNAUTHORIZED')
@api.response(404, 'Not Found')
class Document(Resource):
    @api.doc('get_file', security='apikey')
    @api.marshal_with(file_output)
    @login_required
    def get(self, uuid):
        try:
            file = file_service.get_file(uuid)
            return file
        except FileNotFound:
            abort(404)

    @api.doc('modify_file', security='apikey')
    @api.expect(file_input, validate=True)
    @api.marshal_with(file_output)
    @login_required
    def put(self, uuid):
        args = file_input_parser.parse_args()
        _logger.debug(args)
        try:
            # TODO: reversion is not equal to current reversion value, still could modify file.
            file = file_service.modify_file(uuid=uuid,
                                            reversion=args.get('reversion'),
                                            file_name=args.get('file_name'),
                                            file_size=args.get('file_size'))
            return file
        except FileNotFound:
            abort(404)

    @api.doc('delete_file', security='apikey')
    @login_required
    def delete(self, uuid):
        try:
            file_service.logic_delete(uuid)
        # TODO: Change exception to a more suitable Exception
        except FileNotFound:
            abort(404)
