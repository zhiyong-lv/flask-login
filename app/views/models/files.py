from flask_restplus import Model, fields
from .commons import paginate_model

file_input = Model('File Input', {
    'file_name': fields.String(required=True, description='The file name', example='test.zip'),
    'file_size': fields.Integer(required=True, description='The file size', example=100),
    'reversion': fields.Integer(description='The file reversion', example=1),
}, mask='file_name,file_size,reversion')

file_output = file_input.clone('File', {
    'uuid': fields.String(required=True, description='The file uuid and the unique identifier of file',
                          example="12345678-1234-5678-1234-567812345678"),
    'status': fields.String(required=True, description='The file status', example="new_create"),
    'creator_id': fields.Integer(required=True, description="The creaator's id", example=1),
    'create_time': fields.DateTime(required=True, description="The document create time", example=""),
    'last_modify_time': fields.String(required=True, description="The document last update time"),
})

files_output = paginate_model.clone('FileList', {
    'items': fields.List(fields.Nested(file_output))
})
