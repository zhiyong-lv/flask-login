import logging

from flask import request
from flask_login import login_required
from flask_restplus import Namespace, Resource, abort

from app.services import UserService
from .models.commons import paginate
from .models.users import user_input, user_output, users_output, user_basic

user_service = UserService()

_logger = logging.getLogger(__name__)
api = Namespace('users', description='Users related operations')
api.models[user_input.name] = user_input
api.models[user_output.name] = user_output
api.models[users_output.name] = users_output


@api.route('/')
@api.response(500, 'Internal error')
@api.response(401, 'UNAUTHORIZED')
@api.response(400, 'Bad request')
class UserList(Resource):
    @api.doc('list_users', security='apikey')
    @api.expect(paginate, validate=True)
    @api.marshal_with(users_output)
    @login_required
    # @cache.cached()
    def get(self):
        """List all users"""
        args = paginate.parse_args()
        return user_service.query_users(**args)

    @api.doc('create_users', security='apikey')
    @api.expect(user_input, validate=True)
    @api.marshal_with(user_output, code=201, description='User created')
    @login_required
    def post(self):
        """Creaet user"""
        return user_service.add_user(request.json)


@api.route('/<int:id>')
@api.response(500, 'Internal error')
@api.response(400, 'Bad request')
@api.response(404, 'Not Found')
@api.response(401, 'UNAUTHORIZED')
@api.param('id', 'The user identifier')
class UserList(Resource):
    @api.doc('get_user', security='apikey')
    @api.marshal_with(user_output)
    @login_required
    def get(self, id):
        """Get user by id"""
        user = user_service.get_user(id)
        if user is None:
            abort(404)

        return user

    @api.doc('modify_user', security='apikey')
    @api.expect(user_basic, validate=True)
    @api.marshal_with(user_output, code=200, description='User modified')
    @login_required
    def put(self, id):
        """Modify user"""
        # args = user_parser.parse_args()
        user = user_service.modify_user(id, request.json)
        if user is None:
            abort(404)

        return user

    @api.doc('delete_user', security='apikey')
    @login_required
    def delete(self, id):
        """Delete user by id"""
        user = user_service.delete_user(id)
        if user is None:
            abort(404)
