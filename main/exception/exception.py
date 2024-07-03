import uuid


class BasicException(Exception):
    def __init__(self, message: str = None):
        self.message = message if message else "An exception was raised"
        super().__init__(self.message)


class AlreadyExistedException(BasicException):
    def __init__(self, index: uuid = None, name: str = 'Record'):
        self.message = f"{name} with id = '{index}' has already existed." if index is not None \
            else f"{name} has already existed."
        super().__init__(self.message)


class DatabaseConnectionFailedException(BasicException):
    def __init__(self, message: str = None):
        self.message = message if message else "Database connection failed"
        super().__init__(self.message)


class DatabaseErrorException(BasicException):
    def __init__(self, message: str = None):
        self.message = message if message else "Database error"
        super().__init__(self.message)


class JSONSchemaValidateException(BasicException):
    def __init__(self, message: str = None):
        self.message = message if message else f"JSON schema is not valid"
        super().__init__(self.message)


class NotFoundException(BasicException):
    def __init__(self, index: uuid = None, name: str = 'Record'):
        self.message = f"{name} with id = '{index}' not found." if index is not None else f"{name} not found."
        super().__init__(self.message)


class QueryExecuteFailedException(BasicException):
    def __init__(self, message: str = None):
        self.message = message if message else "Query execute failed"
        super().__init__(self.message)


class WrongDataFieldsAmountException(BasicException):
    def __init__(self, message: str = None):
        self.message = message if message else f"Wrong data fields amount"
        super().__init__(self.message)


class WrongDataTypeException(BasicException):
    def __init__(self, message: str = None):
        self.message = message if message else f"Wrong data type"
        super().__init__(self.message)
