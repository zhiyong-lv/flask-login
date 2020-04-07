from flask_login import login_required
from flask_restplus import Namespace, Resource

api = Namespace('homepage', description='Home Page')


@api.route('/home')
@api.response(500, 'Internal error')
@api.response(400, 'Validation error')
@api.response(401, 'unauthorized')
class Home(Resource):

    # @login_required
    @api.doc('homepage')
    def get(self):
        '''Return Home Page'''
        return 'hello world'
