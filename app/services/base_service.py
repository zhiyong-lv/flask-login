import logging
import threading
import time
import uuid
from contextlib import contextmanager
from functools import wraps

# singleton instance, default value.
sentinel = object()


class BaseService(object):
    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._service_lock = threading.Lock()
        self._uuid_func = uuid.uuid1

    def uuid(self, *args, **kwargs):
        return self._uuid_func()

    def timethis(self, func):
        @wraps(func)
        def _wrapper(*args, **kwargs):
            start = time.perf_counter()
            r = func(args, kwargs)
            end = time.perf_counter()
            self._logger.debug(f"{func.__module__}.{func.__name__} : {end - start}")
            return r

        return _wrapper

    @contextmanager
    def timeblock(self, label):
        start = time.perf_counter()
        try:
            yield
        finally:
            end = time.perf_counter()
            self._logger.debug(f"{label} : {end - start}")
