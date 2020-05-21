import logging

from flask import request
from flask_login import login_required, current_user
from flask_restplus import Namespace, Resource, abort

from app.services import FileServices
from app.services.file_services.exceptions import FileNotFound
from .models.commons import paginate as paginate_parser
from .models.files import file_input, files_output, file_output

_logger = logging.getLogger(__name__)

api = Namespace('files', path='/files', description='File Management')
file_service = FileServices()

api.models[file_input.name] = file_input
api.models[file_output.name] = file_output
api.models[files_output.name] = files_output


@api.route('/')
@api.response(500, 'Internal error')
@api.response(404, 'Not Found')
@api.response(400, 'Validation error')
@api.response(401, 'UNAUTHORIZED')
class Fils(Resource):
    @api.doc('query_files', security='apikey')
    @api.expect(paginate_parser, validate=True)
    @api.marshal_with(files_output)
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
    @api.response(201, 'CREATED', file_output)
    @login_required
    def post(self):
        """Create a new file"""
        document = file_service.add_file(request.json, user_id=current_user.id)
        return document, 201


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
        try:
            file = file_service.modify_file(uuid, request.json)
            return file
        except FileNotFound:
            abort(404)

    @api.doc('delete_file', security='apikey')
    @login_required
    def delete(self, uuid):
        try:
            file_service.logic_delete(uuid)
        except FileNotFound:
            abort(404)
