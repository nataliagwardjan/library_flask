from main.const.global_const import EXCEPTION_HANDLE, ALREADY_EXISTED, DATABASE_CONNECTION_FAILED, \
    JSON_SCHEMA_VALIDATION_FAILED, QUERY_EXECUTE_FAILED, NOT_FOUND, VALUE_ERROR, RECORD_NOT_REMOVE, \
    RECORD_NOT_ADD, RECORD_NOT_GET, RECORD_NOT_UPDATE, DATABASE_ERROR


class BasicException(Exception):
    def __init__(self, exception_type: str = EXCEPTION_HANDLE, message: str = "An exception was raised."):
        self.exception_type = exception_type
        self.message = message
        super().__init__(self.exception_type, self.message)


class AlreadyExistedException(BasicException):
    def __init__(self, exception_type: str = ALREADY_EXISTED, message: str = "Record has already existed."):
        self.exception_type = exception_type
        self.message = message
        super().__init__(self.exception_type, self.message)


class DatabaseConnectionFailedException(BasicException):
    def __init__(self, exception_type: str = DATABASE_CONNECTION_FAILED, message: str = "Database connection failed."):
        self.exception_type = exception_type
        self.message = message
        super().__init__(self.exception_type, self.message)


class DatabaseErrorException(BasicException):
    def __init__(self, exception_type: str = DATABASE_ERROR, message: str = "Database error."):
        self.exception_type = exception_type
        self.message = message
        super().__init__(self.exception_type, self.message)


class JSONSchemaValidateException(BasicException):
    def __init__(self, exception_type: str = JSON_SCHEMA_VALIDATION_FAILED, message: str = "JSON schema is not valid."):
        self.exception_type = exception_type
        self.message = message
        super().__init__(self.exception_type, self.message)


class NotFoundException(BasicException):
    def __init__(self, exception_type: str = NOT_FOUND, message: str = "Record not found."):
        self.exception_type = exception_type
        self.message = message
        super().__init__(self.exception_type, self.message)


class QueryExecuteFailedException(BasicException):
    def __init__(self, exception_type: str = QUERY_EXECUTE_FAILED, message: str = "Query execute failed."):
        self.exception_type = exception_type
        self.message = message
        super().__init__(self.exception_type, self.message)


class NotGetException(BasicException):
    def __init__(self, exception_type: str = RECORD_NOT_GET,
                 message: str = "Data cannot be got from database."):
        self.exception_type = exception_type
        self.message = message
        super().__init__(self.exception_type, self.message)


class NotAddException(BasicException):
    def __init__(self, exception_type: str = RECORD_NOT_ADD, message: str = "Record cannot be added to database."):
        self.exception_type = exception_type
        self.message = message
        super().__init__(self.exception_type, self.message)


class NotUpdateException(BasicException):
    def __init__(self, exception_type: str = RECORD_NOT_UPDATE, message: str = "Record cannot be updated to database."):
        self.exception_type = exception_type
        self.message = message
        super().__init__(self.exception_type, self.message)


class NotDeleteException(BasicException):
    def __init__(self, exception_type: str = RECORD_NOT_REMOVE, message: str = None):
        self.exception_type = exception_type
        self.message = message if message else "Record cannot be removed to database."
        super().__init__(self.exception_type, self.message)


class ValueException(BasicException):
    def __init__(self, exception_type: str = VALUE_ERROR, message: str = None):
        self.exception_type = exception_type
        self.message = message if message else "Invalid object or missing attribute."
        super().__init__(self.exception_type, self.message)
