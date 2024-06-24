from main.exception.basic_exception import BasicException


class WrongDataFieldsAmountException(BasicException):
    def __init__(self, message: str = None):
        self.message = message if message else f"Wrong data fields amount"
        super().__init__(self.message)
