from flask_restplus import Namespace, Resource, fields
from flask_restplus import reqparse

from app.services import UserService
from app.models import User

api = Namespace('users', description='Users related operations')

user = api.model('User', {
    'id': fields.String(required=False, description='The user identifier'),
    'name': fields.String(required=True, description='The user name'),
    'email': fields.String(required=True, description='The user email'),
})

user_service = UserService()

parser = reqparse.RequestParser()
parser.add_argument('name')
parser.add_argument('email')


@api.route('/')
@api.response(500, 'Internal error')
@api.response(400, 'Validation error')
class UserList(Resource):
    @api.doc('list_users')
    @api.marshal_list_with(user, envelope='users')
    def get(self):
        '''List all users'''
        return User.query.all()

    @api.doc('create_users')
    @api.expect(user, validate=True)
    @api.marshal_with(user, code=201, description='User created')
    def post(self):
        '''Creaet user'''
        args = parser.parse_args()
        return user_service.add_user(args['name'], args['email'])
