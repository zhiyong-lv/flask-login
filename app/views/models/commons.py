from flask_restplus import Model, fields
from flask_restplus.reqparse import RequestParser

paginate = RequestParser()
paginate.add_argument('page', location='args', type=int, help='The page begin number')
paginate.add_argument('per_page', location='args', type=int, help='The number in every page')

paginate_model = Model('pageinate', {
    'per_page': fields.Integer(required=True, description='Count per page', example=20),
    'page': fields.Integer(required=True, description='Current page number', example=1),
    'total': fields.Integer(required=True, description='The document total count', example=10),
})
