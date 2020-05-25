from marshmallow import Schema, fields, validate, EXCLUDE, post_load

from app.models import User


class UserSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Int(validate=validate.Range(min=1), dump_only=True)
    username = fields.Str(validate=validate.Length(min=1, max=80))
    password = fields.Str(validate=validate.Length(min=1, max=120), load_only=True)
    email = fields.Str(validate=validate.Length(min=1, max=120))
    active = fields.Bool(dump_only=True)
    creator = fields.Str(validate=validate.Length(min=1, max=80))

    @post_load
    def get_user(self, data, **kwargs):
        password = data.pop("password") if "password" in data else None
        user = User(**data)

        if password is not None:
            user.password = password

        return user


user_schema = UserSchema()
users_schema = UserSchema(many=True)
