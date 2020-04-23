import logging

from flask_login import login_user

from app import db, cache
from app.models import User


class UserService:

    def __init__(self):
        self._logger = logging.getLogger(__name__)

    @cache.memoize()
    def query_users(self, offset, limit):
        import time
        time.sleep(5)
        return {
            'users': User.query.offset(offset - 1).limit(limit).all(),
            'count': User.query.count(),
            'limit': limit,
            'offset': offset,
        }

    def add_user(self, name, password, email):
        user = User(username=name, email=email)
        user.password = password
        db.session.add(user)
        db.session.commit()
        return user


    @cache.memoize()
    def get_user(self, id):
        import time
        time.sleep(5)
        return User.query.get(id)

    def get_users_by_name(self, name):
        return User.query.filter_by(username=name).first()

    def verify_user(self, name, password):
        user = User.query.filter_by(username=name).first()
        if user is not None and user.verify(password):
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
            user.name = update_data['name']
            user.password = update_data['password']
            user.name = update_data['email']
            db.session.add(user)
            db.session.commit()
        return user

    def delete_user(self, id):
        user = User.query.get(id)
        if user is not None:
            db.session.delete(user)
            db.session.commit()
        return user
