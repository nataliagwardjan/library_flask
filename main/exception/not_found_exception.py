import uuid

from main.exception.basic_exception import BasicException


class NotFoundException(BasicException):
    def __init__(self, index: uuid = None, name: str = 'Record'):
        self.message = f"{name} with id = '{index}' not found." if index is not None else f"{name} not found."
        super().__init__(self.message)
