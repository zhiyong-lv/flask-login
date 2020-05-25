from flask_restplus import Model, fields

session_json = Model('Session Input', {
    'username': fields.String(required=True, description='The user name', attribute='username'),
    'password': fields.String(required=True, description='The user password'),
})
