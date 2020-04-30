from marshmallow import Schema, fields, validate, EXCLUDE, pre_load, post_load, post_dump

from app.models import File
from app.services.file_services.file_status import FileStatus


class FileSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    uuid = fields.UUID(dump_only=True)
    file_name = fields.Str(validate=validate.Length(min=1, max=200))
    file_size = fields.Int(validate=validate.Range(min=1, max=10 * 1024 * 1024 * 1024))
    status = fields.Int(dump_only=True)
    valid = fields.Bool(dump_only=True)
    creator_id = fields.Int(dump_only=True)
    create_time = fields.DateTime(dump_only=True)
    last_modify_time = fields.DateTime(dump_only=True)
    reversion = fields.Int(validate=validate.Range(min=1))

    @pre_load
    def process_file(self, data, **kwargs):
        status_name = data.get("status", None)
        if status_name is not None and status_name in FileStatus.field_list('name'):
            status_value = FileStatus.get_status('name', status_name).value
            data["status"] = status_value
        return data

    @post_load
    def make_file(self, data, **kwargs):
        return File(**data)

    @post_dump
    def format_file(self, data, **kwargs):
        status_value = data.get("status", None)
        if status_value is not None and status_value in FileStatus.field_list('value'):
            status_name = FileStatus.get_status('value', status_value).name
            data["status"] = status_name
        return data


file_schema = FileSchema()
files_schema = FileSchema(many=True)
