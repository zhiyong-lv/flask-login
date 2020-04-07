from flask_restplus import Api

from .home import api as ns_homepage
from .users import api as ns_users

api = Api(
    title='Flasky',
    version='1.0',
    description='Flasky is a wiki, and easy to use',
    # All API metadatas
)

api.add_namespace(ns_users)
api.add_namespace(ns_homepage)
