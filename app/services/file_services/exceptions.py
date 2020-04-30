class FileBaseException(Exception):
    def __init__(self, message, code):
        self._msg = message
        self._code = code

    @property
    def message(self):
        return self._msg

    @property
    def code(self):
        return self.code


class FileNotFound(FileBaseException):
    def __init__(self, message=None, code=None):
        message = message if message is not None else "File is not found"
        code = code if code is not None else 404
        super().__init__(message, code)


class FileReversionError(FileBaseException):
    def __init__(self, message=None, code=None):
        message = message if message is not None else "File's reversion error"
        code = code if code is not None else 400
        super().__init__(message, code)


class FileDuplicated(FileBaseException):
    def __init__(self, message=None, code=None):
        message = message if message is not None else "File is duplicated"
        code = code if code is not None else 400
        super().__init__(message, code)

class FileInValid(FileBaseException):
    def __init__(self, message=None, code=None):
        message = message if message is not None else "File is invalid"
        code = code if code is not None else 400
        super().__init__(message, code)

class FileBaseError(FileBaseException):
    def __init__(self, message=None, code=None):
        message = message if message is not None else "Internal Error"
        code = code if code is not None else 500
        super().__init__(message, code)

