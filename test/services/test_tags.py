import logging

import pytest

from app import db
from app.services.file_services.services import FileServices
from app.services.tag_services import TagService
from test import app

logger = logging.getLogger(__name__)

data = [
    ('test1.txt', 1024, ('test1', 'user',), 1, ['extend1.txt', 'extend2.txt', 'extend3.txt']),
    ('test2.txt', 2048, ('test2', 'user',), 1, []),
    ('test3.txt', 3072, ('user',), 2, ['extend1.txt', 'extend2.txt', 'extend3.txt'])
]


@pytest.fixture(scope='function', autouse=True)
def init_db():
    with app.app_context():
        logger.info("============start create all databases")
        db.create_all()
        yield
        logger.info("=============start delete all databases")
        db.drop_all()
        logger.info("=============end delete all databases")


@pytest.mark.parametrize("file_name, file_size, tags, user_id, extend_files", data)
class TestTagServices:
    def test_add_map_delete_tags(self, file_name, file_size, tags, user_id, extend_files):
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
                tag_service.delete(id=q_tag.id, creator_id=user_id)
                query_tags_after_delete = tag_service.query_file_tags(file_uuid)
                for q_tag_after_delete in query_tags_after_delete:
                    assert q_tag_after_delete.name in tags
                    assert q_tag.id != q_tag_after_delete.id

    def test_query_tags(self, file_name, file_size, tags, user_id, extend_files):
        with app.app_context():
            tag_service = TagService()
            for tag in tags:
                tag_service.add(name=tag, creator_id=user_id)
            query_tags = []
            page = 1
            per_page = 1
            while page * per_page <= len(tags):
                query_tag_pages = tag_service.query(creator_id=user_id, per_page=1, page=page)
                assert query_tag_pages.total == len(tags)
                assert query_tag_pages.page == page
                assert query_tag_pages.per_page == 1
                page = next_page = query_tag_pages.page + 1
                query_tags.extend(query_tag_pages.items)

            assert len(query_tags) == len(tags)
            for q_tag in query_tags:
                assert q_tag.name in tags

    def test_map_tags_to_multiple_files(self, file_name, file_size, tags, user_id, extend_files):
        with app.app_context():
            file_uuid_list = []
            file_service = FileServices()
            file = file_service.add_file(file_json={'file_name': file_name, 'file_size': file_size}, user_id=user_id)
            file_uuid_list.append((file.get('uuid'), file_name))

            for other_file_name in extend_files:
                file = file_service.add_file(file_json={'file_name': other_file_name, 'file_size': file_size},
                                             user_id=user_id)
                file_uuid_list.append((file.get('uuid'), other_file_name))

            tag_service = TagService()
            for tag in tags:
                tag_dto = tag_service.add(name=tag, creator_id=user_id)
                logger.debug(tag_dto)
                for file_uuid, _ in file_uuid_list:
                    tag_service.map_file(tag_id=tag_dto.get('id'), file_uuid=file_uuid)

            query_tags = []
            page = 1
            per_page = 1
            while page * per_page <= len(tags):
                query_tag_pages = tag_service.query(creator_id=user_id, per_page=per_page, page=page)
                assert query_tag_pages.total == len(tags)
                assert query_tag_pages.page == page
                assert query_tag_pages.per_page == per_page
                page = next_page = query_tag_pages.page + 1
                query_tags.extend(query_tag_pages.items)

            for query_tag in query_tags:
                results = tag_service.query_tag_files(tag_id=query_tag.id)
                logger.debug(results)

            for file_uuid, _ in file_uuid_list:
                query_tags = tag_service.query_file_tags(file_uuid)
                assert len(query_tags) == len(tags)
                for q_tag in query_tags:
                    assert q_tag.name in tags
