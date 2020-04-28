from sqlalchemy.exc import IntegrityError

from app import db
from app.models.files import File
from .exceptions import FileNotFound, FileDuplicated
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

    def add_file(self, file_name, file_size, user_id):
        try:
            file = File(uuid=str(self.uuid()), file_name=file_name, file_size=file_size, creator_id=user_id,
                        status=CREATE_STATUS.value)
            db.session.add(file)
            db.session.commit()
        except IntegrityError:
            raise FileDuplicated()
        return file.uuid

    def modify_file(self, uuid, file_name=None, file_size=None):
        file = File.query.get(uuid)
        if file is None or file.valid == False:
            # raise FileNotFound exception when file is not existed in files table or file is invalid.
            raise FileNotFound()

        if file_name is not None:
            file.file_name = file_name
        if file_size is not None:
            file.file_size = file_size

        file.reversion = file.reversion + 1
        db.session.commit()
        return file

    def get_file(self, uuid):
        files = File.query.filter(db.and_(File.uuid == uuid, File.valid == True)).all()
        if len(files) != 1:
            raise FileNotFound()
        else:
            return files[0]

    def delete(self, uuid):
        count = File.query.filter(File.uuid == uuid).delete()
        if count != 1:
            raise FileNotFound()

    def logic_delete(self, uuid):
        count = File.query.filter(db.and_(File.uuid == uuid, File.valid == True)).update({'valid': False})
        if count != 1:
            raise FileNotFound()
