from main.exception.basic_exception import BasicException


class WrongDataTypeException(BasicException):
    def __init__(self, message: str = None):
        self.message = message if message else f"Wrong data type"
        super().__init__(self.message)
