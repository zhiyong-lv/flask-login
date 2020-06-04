from marshmallow import Schema, fields, validate, EXCLUDE, post_load

from app.models import FileTag


class FileTagSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Int(validate=validate.Range(min=0), dump_only=True)
    file_uuid = fields.UUID(required=True)
    tag_id = fields.Int(validate=validate.Range(min=0), required=True)

    @post_load
    def make_file(self, data, **kwargs):
        data['file_uuid'] = str(data['file_uuid'])
        return FileTag(**data)


file_tag_map_schema = FileTagSchema()
file_tag_maps_schema = FileTagSchema(many=True)
