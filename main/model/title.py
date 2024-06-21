from enum import Enum


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
