from main.exception.basic_exception import BasicException


class JSONSchemaValidateException(BasicException):
    def __init__(self, message: str = None):
        self.message = message if message else f"JSON schema is not valid"
        super().__init__(self.message)
