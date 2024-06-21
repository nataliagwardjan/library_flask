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


class Status(Enum):
    AVAILABLE = "available"
    BORROW = "borrow"

    def __str__(self):
        return self.name.lower()

    def __repr__(self):
        return f"{self.__class__.__name__}.{self.name}"


class Category(Enum):
    MYSTERY = "mystery"
    THRILLER = "thriller"
    COMEDY = "comedy"
    DRAMA = "drama"
    ROMANCE = "romance"
    FANTASY = "fantasy"
    SCIENCE_FICTION = "science fiction"
    HISTORICAL_FICTION = "historical fiction"
    HORROR = "horror"
    ADVENTURE = "adventure"
    YOUNG_ADULT = "young adult"
    DYSTOPIAN = "dystopian"
    PARANORMAL = "paranormal"
    CONTEMPORARY = "contemporary"
    CHICK_LIT = "chick lit"
    GRAPHIC_NOVEL = "graphic novel"
    MYSTERY_THRILLER = "mystery thriller"
    PSYCHOLOGICAL_THRILLER = "psychological thriller"
    HISTORICAL_ROMANCE = "historical romance"
    GOTHIC = "gothic"
    SPY_FICTION = "spy fiction"
    LEGAL_THRILLER = "legal thriller"
    POLITICAL_THRILLER = "political thriller"
    CRIME = "crime"
    SUPERNATURAL = "supernatural"
    ARCHAEOLOGY = "archeology"
    PUZZLE = "puzzle"
    ACTION = "action"

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
        self.password = password if password else "aaa"
        self.roles = roles if roles else {Role.READER}

    def to_dict(self):
        return {
            "id": self._id,
            "name": self.name,
            "surname": self.surname,
            "email": self.email
        }

    @property
    def id(self):
        return self._id

    def __str__(self):
        return f"""User {self._id}: 
                {self.name} {self.surname},
                e-mail: {self.email}"""

    def __repr__(self):
        return f"{self.__class__.__name__}({self._id!r}, {self.name!r}, {self.surname!r}, {self.email!r}, P######D, {self.roles!r}"


