import logging

from flask import session, current_app, request
from flask.helpers import total_seconds
from flask_login import AUTH_HEADER_NAME
from flask_restplus import Namespace, Resource
from flask_restplus import abort

from app import login_manager
from .models.sessions import session_json
from .service_util import user_service

_logger = logging.getLogger(__name__)
api = Namespace('sessions', description='Users related operations')
api.models[session_json.name] = session_json


@login_manager.user_loader
def load_user(userid):
    return user_service.get_user(userid)


@login_manager.request_loader
def load_request(request):
    user = None
    header_name = current_app.config.get('AUTH_HEADER_NAME', AUTH_HEADER_NAME)
    if header_name in request.headers:
        token = request.headers.get(header_name)
        header, payload = token.split(" ", 1)
        if header != "flasky_token":
            return None
        max_age = total_seconds(current_app.permanent_session_lifetime)
        session_interface = current_app.session_interface
        data = session_interface.get_signing_serializer(current_app).loads(payload, max_age=max_age)
        _logger.debug("token is: {token}, data is {data}".format(token=token, data=data))
        has_user_id = 'user_id' in data
        if has_user_id:
            return user_service.get_user(data.get('user_id'))
    return user


@api.route('/')
@api.response(500, 'Internal error')
@api.response(400, 'Bad request')
class Session(Resource):
    @api.doc('create_session', security=None)
    @api.expect(session_json, validate=True)
    def post(self):
        """Creaet session"""
        try:
            if user_service.verify_user(request.json):
                session_interface = current_app.session_interface
                payload = session_interface.get_signing_serializer(current_app).dumps(dict(session))
                return {"payload": payload}
            else:
                abort(400)
        except Exception as e:
            _logger.exception(e)
            abort(500)
