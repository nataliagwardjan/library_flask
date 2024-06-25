import uuid
from enum import Enum


class Role(Enum):
    ADMIN = "admin"
    LIBRARIAN = "librarian"
    READER = "reader"

    def __str__(self):
        return self.name.lower()

    def __repr__(self):
        return f"{self.__class__.__name__}.{self.name}"


class User:
    def __init__(self, user_id: uuid, name: str, surname: str, email: str, password: str, roles: set):
        self._id = user_id if user_id else uuid.uuid4()
        self.name = name
        self.surname = surname
        self.email = email
        self.password = password
        self.roles = roles if roles else {Role.READER}

    def to_dict(self):
        return {
            "id": str(self._id),
            "name": self.name,
            "surname": self.surname,
            "email": self.email,
            "roles": list(self.roles)
        }

    @property
    def id(self):
        return self._id

    def __str__(self):
        return f"User {self._id}: {self.name} {self.surname}, e-mail: {self.email}, roles: {self.roles}"

    def __repr__(self):
        return f"{self.__class__.__name__}({self._id!r}, {self.name!r}, {self.surname!r}, {self.email!r}, P######D, {self.roles!r}"
