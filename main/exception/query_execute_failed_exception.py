from main.exception.basic_exception import BasicException


class QueryExecuteFailedException(BasicException):
    def __init__(self, message: str = None):
        self.message = message if message else "Query execute failed"
        super().__init__(self.message)
