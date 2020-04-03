from app import db
from app.models.users import User


class UserService:
    def __init__(self):
        pass

    def add_user(self, name, email):
        user = User(username=name, email=email)
        db.session.add(user)
        db.session.commit()
