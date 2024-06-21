from enum import Enum


class Status(Enum):
    AVAILABLE = "available"
    BORROW = "borrow"

    def __str__(self):
        return self.name.lower()

    def __repr__(self):
        return f"{self.__class__.__name__}.{self.name}"
