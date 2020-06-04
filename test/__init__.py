import logging
import sys

from app import create_app
from app.config import Config

logging.basicConfig(
    stream=sys.stdout,
    format="%(asctime)s - %(threadName)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)s - %(message)s",
    level=logging.DEBUG
)

logger = logging.getLogger(__name__)

logger.debug("start create app")
assert Config.DATABASE_NAME == 'test_flask_login_unittest'
app = create_app()
