from flask_restplus import Model, fields
from .commons import paginate_model

user_basic = Model('User', {
    'username': fields.String(required=True, description='The user name', attribute='username'),
    'email': fields.String(required=True, description='The user email'),
})

user_input = user_basic.clone('User Input', {
    'password': fields.String(required=True, description='The user password'),
})

user_output = user_basic.clone('User', {
    'id': fields.String(required=True, description='The user identifier'),
})

users_output = paginate_model.clone('Users', {
    'items': fields.List(fields.Nested(user_output))
})
