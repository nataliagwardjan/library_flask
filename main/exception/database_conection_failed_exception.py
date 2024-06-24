from main.exception.basic_exception import BasicException


class DatabaseConnectionFailedException(BasicException):
    def __init__(self, message: str = None):
        self.message = message if message else "Database connection failed"
        super().__init__(self.message)
