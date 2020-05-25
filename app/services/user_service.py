import logging

from flask_login import login_user

from app import db, cache
from app.models import User
from app.schema.user_schema import user_schema


class UserService:

    def __init__(self):
        self._logger = logging.getLogger(__name__)

    @cache.memoize()
    def query_users(self, page=None, per_page=None, error_out=True, max_per_page=None):
        return User.query.paginate(page=page, per_page=per_page, error_out=error_out,
                                   max_per_page=max_per_page)

    def add_user(self, user_json):
        user = user_schema.load(user_json, partial=("username", "email", "password"))
        db.session.add(user)
        db.session.commit()
        return user

    @cache.memoize()
    def get_user(self, id):
        return User.query.get(id)

    def get_users_by_name(self, name):
        return User.query.filter_by(username=name).first()

    def verify_user(self, session_json):
        input_user = user_schema.load(session_json, partial=("email",))
        user = User.query.filter_by(username=input_user.username).first()
        if user is not None and user.verify(session_json['password']):
            return login_user(user)
        else:
            self._logger.info("user({name}'s password is not correct)".format(name=name))
            return False

    def modify_user(self, id, update_data):
        user = User.query.get(id)
        if user is not None:
            print("user is not None when modify user")
            self._logger.info(
                "user is not None when modify user, user#{id} input is {data}".format(id=id, data=update_data))

            new_user = user_schema.load(update_data, partial=("username", "email"))
            user.name = new_user.username
            user.email = new_user.email
            db.session.add(user)
            db.session.commit()
        return user

    def delete_user(self, id):
        user = User.query.get(id)
        if user is not None:
            db.session.delete(user)
            db.session.commit()
        return user
