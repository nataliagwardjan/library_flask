import uuid

from main.exception.basic_exception import BasicException


class AlreadyExistedException(BasicException):
    def __init__(self, index: uuid = None, name: str = 'Record'):
        self.message = f"{name} with id = '{index}' has already existed." if index is not None \
            else f"{name} has already existed."
        super().__init__(self.message)
