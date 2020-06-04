import logging

import pytest

from app import db
from app.services.file_services.services import FileServices
from app.services.tag_services import TagService
from test import app

logger = logging.getLogger(__name__)

data = [
    ('test1.txt', 1024, ('test1', 'user',), 1),
    ('test2.txt', 2048, ('test2', 'user',), 1),
    ('test3.txt', 3072, ('user',), 2)
]


@pytest.fixture(scope='class', autouse=True)
def init_db():
    with app.app_context():
        logger.info("============start create all databases")
        db.create_all()
        yield
        logger.info("=============start delete all databases")
        db.drop_all()
        logger.info("=============end delete all databases")


@pytest.mark.parametrize("file_name, file_size, tags, user_id", data)
class TestTagServices:
    def test_add_tags(self, file_name, file_size, tags, user_id):
        with app.app_context():
            file_service = FileServices()
            file = file_service.add_file(file_json={'file_name': file_name, 'file_size': file_size}, user_id=user_id)
            file_uuid = file.get('uuid')
            logger.debug(file)

            tag_service = TagService()
            for tag in tags:
                tag_dto = tag_service.add(name=tag, creator_id=user_id)
                logger.debug(tag_dto)
                tag_service.map_file(tag_id=tag_dto.get('id'), file_uuid=file_uuid)

            query_tags = tag_service.query_file_tags(file_uuid)
            assert len(query_tags) == len(tags)
            for q_tag in query_tags:
                assert q_tag.name in tags
