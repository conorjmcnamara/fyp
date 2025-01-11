from enum import Enum


class DblpTxtField(Enum):
    ID = "#index"
    TITLE = "#*"
    AUTHORS = "#@"
    YEAR = "#t"
    ABSTRACT = "#!"
    VENUE = "#c"
    REFERENCE = "#%"
