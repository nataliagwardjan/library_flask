import uuid
from enum import Enum, auto


class Role(Enum):
    ADMIN = auto()
    MANAGER = auto()
    READER = auto()


class User:
    def __init__(self, user_id: uuid, name: str, surname: str, email: str, password: str):
        self._id = user_id if user_id else uuid.uuid4()
        self.name = name
        self.surname = surname
        self.email = email
        self.password = password

    @property
    def id(self):
        return self._id
