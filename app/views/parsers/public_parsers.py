from flask_restplus import reqparse


def generate_paginate_parser(name):
    paginate_parser = reqparse.RequestParser()
    paginate_parser.add_argument('offset', location='args', help='The {name} begin number'.format(name=name))
    paginate_parser.add_argument('limit', location='args',
                                 help='The max {name} count which should be returned once'.format(name=name))
    return paginate_parser
