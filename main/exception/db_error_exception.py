from main.exception.basic_exception import BasicException


class DatabaseErrorException(BasicException):
    def __init__(self, message: str = None):
        self.message = message if message else "Database error"
        super().__init__(self.message)
