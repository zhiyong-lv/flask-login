import logging

from flask_testing import TestCase

from app import create_app, db
from app.config import Config

# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
logger = logging.getLogger(__name__)


class ModelBaseTest(TestCase):
    def create_app(self):
        assert Config.DATABASE_NAME == 'test_flask_login_unittest'
        return create_app()

    def setUp(self):
        logger.debug("create all table")
        db.drop_all()
        db.create_all()

    def tearDown(self):
        logger.debug("drop all table")
        db.session.remove()
        db.drop_all()
