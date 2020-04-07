import logging

from app import db
from app.models.users import User


class UserService:
    def __init__(self):
        self._logger = logging.getLogger()

    def query_users(self, offset, limit):
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

    def get_user(self, id):
        return User.query.get(id)

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
