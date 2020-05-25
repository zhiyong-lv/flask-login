from marshmallow import Schema, fields, validate, EXCLUDE, post_load

from app.models import Document


class DocumentSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Int(validate=validate.Range(min=1), dump_only=True)
    title = fields.Str(validate=validate.Length(min=1, max=80))
    content = fields.Str(validate=validate.Length(min=1))
    creator_id = fields.Int(validate=validate.Range(min=1), dump_only=True)
    create_time = fields.DateTime(dump_only=True)
    last_modify_time = fields.DateTime(dump_only=True)
    reversion = fields.Int(validate=validate.Range(min=1), dump_only=True)

    @post_load
    def get_user(self, data, **kwargs):
        return Document(**data)


doc_schema = DocumentSchema()
docs_schema = DocumentSchema(many=True)
