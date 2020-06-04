from faker import Faker
from pytest import raises, mark, fixture

from app import db
from app.services.exceptions import *
from app.services.file_services.file_status import *
from app.services.file_services.services import FileServices
from test import app

logger = logging.getLogger(__name__)

data_of_create_and_modify = [
    ('test1.txt', 1024),
    ('test2.txt', 2048),
    ('test3.txt', 3072)
]


@fixture(scope='function', autouse=True)
def init_db():
    with app.app_context():
        logger.info("============start create all databases")
        db.create_all()
        yield
        logger.info("=============start delete all databases")
        db.drop_all()
        logger.info("=============end delete all databases")


class TestFileServices():
    def test_create_and_modify(self):
        with app.app_context():
            file_services = FileServices()
            file = file_services.add_file({'file_name': "test_file", 'file_size': 12}, user_id=10)
            logger.debug(file)
            uuid = file.get('uuid')
            reversion = file.get('reversion')
            modified_file = file_services.modify_file(uuid=uuid,
                                                      file_json={'reversion': reversion, 'file_name': 'test_file2',
                                                                 'file_size': 13})
            logger.debug(modified_file)
            assert modified_file.get('uuid') == uuid and modified_file.get(
                "file_name") == "test_file2" and modified_file.get("file_size") == 13
            assert modified_file.get('reversion') == 2

    def test_modify_not_existed(self):
        with app.app_context():
            file_services = FileServices()
            with raises(NotFound):
                file_services.modify_file(uuid="1234", file_json={'reversion': 1, 'file_name': 'test_file2',
                                                                  'file_size': 13})

    def test_add_file_and_get(self):
        with app.app_context():
            file_services = FileServices()
            uuid = file_services.add_file({'file_name': "test_file", 'file_size': 12}, user_id=10).get('uuid')
            file = file_services.get_file(uuid=uuid)
            assert file.get('uuid') == uuid
            assert file.get('valid') is True
            assert file.get('status') == CREATE_STATUS.name

    def test_add_duplicated_file(self):
        with app.app_context():
            file_services = FileServices()
            file_services.add_file({'file_name': "test_file3", 'file_size': 12}, user_id=10)
            with raises(Duplicated):
                file_services.add_file({'file_name': "test_file3", 'file_size': 12}, user_id=10)

    def test_get_not_existed(self):
        with app.app_context():
            file_services = FileServices()
            with raises(NotFound):
                file_services.get_file(uuid="123")

    def test_logic_delete(self):
        with app.app_context():
            file_services = FileServices()
            with raises(NotFound):
                file_services.logic_delete(uuid="1234")

    def test_delete(self):
        with app.app_context():
            file_services = FileServices()
            with raises(NotFound):
                file_services.delete(uuid="1234")

    def test_create_logic_delete_then_delete(self):
        with app.app_context():
            file_services = FileServices()
            uuid = file_services.add_file({'file_name': "test_file4", 'file_size': 12}, user_id=10).get('uuid')
            file_services.logic_delete(uuid=uuid)
            file_services.delete(uuid=uuid)

    def test_create_logic_delete_then_logic_delete(self):
        with app.app_context():
            file_services = FileServices()
            uuid = file_services.add_file({'file_name': "test_file5", 'file_size': 12}, user_id=10).get('uuid')
            file_services.logic_delete(uuid=uuid)
            with raises(NotFound):
                file_services.logic_delete(uuid=uuid)

    def test_create_delete_then_delete(self):
        with app.app_context():
            file_services = FileServices()
            uuid = file_services.add_file({'file_name': "test_file6", 'file_size': 12}, user_id=10).get('uuid')
            file_services.delete(uuid=uuid)
            with raises(NotFound):
                file_services.delete(uuid=uuid)

    def test_query(self):
        with app.app_context():
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
