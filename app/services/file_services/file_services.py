from sqlalchemy.exc import IntegrityError

from app import db
from app.models.files import File
from app.schema import file_schema
from .exceptions import FileNotFound, FileDuplicated, FileBaseError
from .file_status import CREATE_STATUS
from ..base_service import BaseService

VALID = True
INVALID = False


class FileServices(BaseService):
    def __init__(self):
        """File Service will record all files in database.
        After real file was uploaded to cloud. File service will update file's status according to checking result.

        """
        super(FileServices, self).__init__()

    def add_file(self, file_json, user_id):
        try:
            file = file_schema.load(file_json, partial=("file_name", "file_size"))
            file = File(uuid=str(self.uuid()), file_name=file.file_name, file_size=file.file_size, creator_id=user_id,
                        status=CREATE_STATUS.value)
            db.session.add(file)
            db.session.commit()
            return file_schema.dump(file)
        except IntegrityError:
            raise FileDuplicated
        except Exception:
            raise FileBaseError

    def batch_add_file(self, files):
        try:
            db.session.bulk_save_objects(
                File(uuid=str(self.uuid()), file_name=file['file_name'], file_size=file['file_size'],
                     creator_id=file['user_id'],
                     status=CREATE_STATUS.value) for file in files
            )
            db.session.commit()
        except IntegrityError:
            raise FileDuplicated
        except Exception:
            raise FileBaseError

    def modify_file(self, uuid, file_json):
        file = file_schema.load(file_json)
        reversion, file_name, file_size = file.reversion, file.file_name, file.file_size
        num = File.query.filter(db.and_(File.uuid == uuid, File.valid == True, File.reversion == reversion)).update(
            {File.file_name: file_name, File.file_size: file_size, File.reversion: reversion + 1})
        db.session.commit()

        if num != 1:
            raise FileNotFound

        return file_schema.dump(File.query.get(uuid))

    def get_file(self, uuid):
        file = File.query.filter(db.and_(File.uuid == uuid, File.valid == True)).first()
        if file is None:
            raise FileNotFound()
        else:
            return file_schema.dump(file)

    def delete(self, uuid):
        count = File.query.filter(File.uuid == uuid).delete()
        if count != 1:
            raise FileNotFound()

    def logic_delete(self, uuid):
        count = File.query.filter(db.and_(File.uuid == uuid, File.valid == True)).update({'valid': False})
        if count != 1:
            raise FileNotFound()

    def query(self, page=None, per_page=None, error_out=True, max_per_page=None):
        return File.query.filter(File.valid == True).paginate(page=page, per_page=per_page, error_out=error_out,
                                                              max_per_page=max_per_page)
