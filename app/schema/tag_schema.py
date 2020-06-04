from marshmallow import Schema, fields, validate, EXCLUDE, post_load

from app.models import Tag


class TagSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Int(validate=validate.Length(min=0), dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    creator_id = fields.Int(required=True)
    create_time = fields.DateTime(dump_only=True)
    last_modify_time = fields.DateTime(dump_only=True)
    valid = fields.Bool(dump_only=True)
    reversion = fields.Int(validate=validate.Range(min=1))

    @post_load
    def make_file(self, data, **kwargs):
        return Tag(**data)


tag_schema = TagSchema()
tags_schema = TagSchema(many=True)
