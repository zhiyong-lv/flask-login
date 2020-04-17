import logging

from flask_login import login_required
from flask_restplus import Namespace, Resource, fields, abort, reqparse

from app.services import UserService
from .parsers import generate_paginate_parser

_logger = logging.getLogger(__name__)
api = Namespace('users', description='Users related operations')

user_input = api.model('User Input', {
    'name': fields.String(required=True, description='The user name', attribute='username'),
    'email': fields.String(required=True, description='The user email'),
    'password': fields.String(required=True, description='The user password'),
})

user_output = api.model('User', {
    'name': fields.String(required=True, description='The user name', attribute='username'),
    'email': fields.String(required=True, description='The user email'),
    'id': fields.String(required=True, description='The user identifier'),
})

users_output = api.model('UserList', {
    'users': fields.List(fields.Nested(user_output)),
    'limit': fields.Integer(required=True, description='The max user count which should be returned once.'),
    'offset': fields.Integer(required=True, description='The user begin number'),
    'count': fields.Integer(required=True, description='The user count'),
})

user_parser = reqparse.RequestParser()
user_parser.add_argument('name', location='json', help='The user name')
user_parser.add_argument('email', location='json', help='The user email')
user_parser.add_argument('password', location='json', help='The user password')

paginate_parser = generate_paginate_parser('user')

user_service = UserService()


@api.route('/')
@api.response(500, 'Internal error')
@api.response(401, 'UNAUTHORIZED')
@api.response(400, 'Bad request')
class UserList(Resource):
    @api.doc('list_users', security='apikey')
    @api.expect(paginate_parser, validate=True)
    @api.marshal_list_with(users_output)
    @login_required
    def get(self):
        """List all users"""
        args = paginate_parser.parse_args()

        try:
            offset = int(args.get('offset'))
        except TypeError:
            offset = 1

        try:
            limit = int(args.get('limit'))
        except TypeError:
            limit = 20

        return user_service.query_users(offset=offset, limit=limit)

    @api.doc('create_users', security='apikey')
    @api.expect(user_input, validate=True)
    @api.marshal_with(user_output, code=201, description='User created')
    @login_required
    def post(self):
        """Creaet user"""
        args = user_parser.parse_args()
        return user_service.add_user(args['name'], args['password'], args['email'])


@api.route('/<int:id>')
@api.response(500, 'Internal error')
@api.response(400, 'Bad request')
@api.response(404, 'Not Found')
@api.response(401, 'UNAUTHORIZED')
@api.param('id', 'The user identifier')
class UserList(Resource):
    @api.doc('get_user', security='apikey')
    @api.marshal_list_with(user_output, envelope='users')
    @login_required
    def get(self, id):
        """Get user by id"""
        user = user_service.get_user(id)
        if user is None:
            abort(404)

        return user

    @api.doc('modify_user', security='apikey')
    @api.expect(user_input, validate=True)
    @api.marshal_with(user_output, code=201, description='User modified')
    @login_required
    def put(self, id):
        """Modify user"""
        args = user_parser.parse_args()
        user = user_service.modify_user(id, args)
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
