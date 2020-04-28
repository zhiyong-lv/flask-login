from flask_restplus import Api

from .documents import api as ns_homepage
from .sessions import api as ns_sessions
from .users import api as ns_users
from .files import api as ns_files

authorizations = {
    'token': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

api = Api(
    title='Flasky',
    version='1.0',
    description='Flasky is a wiki, and easy to use',
    authorizations=authorizations,
    # All API metadatas
)

api.add_namespace(ns_sessions)
api.add_namespace(ns_users)
api.add_namespace(ns_homepage)
api.add_namespace(ns_files)
