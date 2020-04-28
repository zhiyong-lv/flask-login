import logging
import threading
from collections import namedtuple


class Status(type):
    FIELD_NAMES = 'name, value'
    FIELDS = FIELD_NAMES.replace(',', ' ').split()

    def __init__(cls, *args, **kwargs):
        cls._lock = threading.Lock()
        cls._log = logging.getLogger(__name__)
        cls._log.debug("in status init")

        cls._status_type = namedtuple('status_type', cls.FIELD_NAMES)
        cls._status_list = []
        cls._map = {}
        for field in cls.FIELDS:
            cls._map[field] = {}

        super().__init__(*args, **kwargs)

    def __call__(cls, *args, **kwargs):
        cls._log.debug("in status call")

        if len(args) != len(cls.FIELDS):
            for arg in args:
                cls._log.debug("arg is {}, type is {}".format(arg, type(arg)))
            raise TypeError("Input parameters error. {cls_name}({FIELD_NAMES})".format(cls_name=cls.__name__,
                                                                                       FIELD_NAMES=cls.FIELD_NAMES))

        instance = cls._status_type(*args)
        with cls._lock:
            cls._status_list.append(instance)
            for field in cls.FIELDS:
                cls._map[field][instance.__getattribute__(field)] = instance

        return instance

    @property
    def status_list(cls):
        return cls._status_list

    def get_status(cls, field, val):
        return cls._map[field].get(val, None)


class FileStatus(metaclass=Status):
    def __init__(self, *args):
        pass


CREATE_STATUS = FileStatus('new_create', 0)
CHECKED_STATUS = FileStatus('checked', 1)
ERROR_STATUS = FileStatus('invalid', 2)
