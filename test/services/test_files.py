from faker import Faker
from pytest import raises

from app.services.file_services.exceptions import *
from app.services.file_services.file_services import FileServices
from app.services.file_services.file_status import *
from . import ModelBaseTest

logger = logging.getLogger(__name__)


class TestFileServices(ModelBaseTest):
    def test_add_file_and_get(self):
        file_services = FileServices()
        uuid = file_services.add_file(file_name="test_file", file_size=12, user_id=10)
        file = file_services.get_file(uuid=uuid)
        assert file.uuid == uuid
        assert file.valid is True
        assert file.status == CREATE_STATUS.value

    def test_add_duplicated_file(self):
        file_services = FileServices()
        file_services.add_file(file_name="test_file", file_size=12, user_id=10)
        with raises(FileDuplicated):
            file_services.add_file(file_name="test_file", file_size=12, user_id=10)

    def test_get_not_existed(self):
        file_services = FileServices()
        with raises(FileNotFound):
            file_services.get_file(uuid="123")

    def test_create_and_modify(self):
        file_services = FileServices()
        uuid = file_services.add_file(file_name="test_file", file_size=12, user_id=10)
        modified_file = file_services.modify_file(uuid=uuid, file_name="test_file2", file_size=13)
        logger.debug(modified_file)
        assert modified_file.uuid == uuid and modified_file.file_name == "test_file2" and modified_file.file_size == 13
        assert modified_file.reversion == 2

    def test_modify_not_existed(self):
        file_services = FileServices()
        with raises(FileNotFound):
            file_services.modify_file(uuid="1234", file_name="test_file2", file_size=13)

    def test_logic_delete(self):
        file_services = FileServices()
        with raises(FileNotFound):
            file_services.logic_delete(uuid="1234")

    def test_delete(self):
        file_services = FileServices()
        with raises(FileNotFound):
            file_services.delete(uuid="1234")

    def test_create_logic_delete_then_delete(self):
        file_services = FileServices()
        uuid = file_services.add_file(file_name="test_file", file_size=12, user_id=10)
        file_services.logic_delete(uuid=uuid)
        file_services.delete(uuid=uuid)

    def test_create_logic_delete_then_logic_delete(self):
        file_services = FileServices()
        uuid = file_services.add_file(file_name="test_file", file_size=12, user_id=10)
        file_services.logic_delete(uuid=uuid)
        with raises(FileNotFound):
            file_services.logic_delete(uuid=uuid)

    def test_create_delete_then_delete(self):
        file_services = FileServices()
        uuid = file_services.add_file(file_name="test_file", file_size=12, user_id=10)
        file_services.delete(uuid=uuid)
        with raises(FileNotFound):
            file_services.delete(uuid=uuid)

    def test_query(self):
        file_services = FileServices()
        faker = Faker()
        data = []
        for i in range(5000):
            file_name = faker.file_name()
            file_size = faker.pyint()
            user_id = faker.pyint()
            data.append({
                'file_name': file_name,
                "file_size": file_size,
                'user_id': user_id
            })

        file_services.batch_add_file(data)
        pagination = file_services.query()
        assert len(pagination.items) == pagination.per_page
        assert pagination.total == 5000
