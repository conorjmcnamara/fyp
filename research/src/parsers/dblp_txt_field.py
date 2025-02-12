from enum import Enum


class DblpTxtField(Enum):
    ID = "#index"
    TITLE = "#*"
    YEAR = "#t"
    AUTHORS = "#@"
    ABSTRACT = "#!"
    VENUE = "#c"
    REFERENCE = "#%"
