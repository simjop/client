from enum import Enum, auto


class SymbolType(Enum):
    """
    1   -
    2a  / a
    2b  / b
    3   |
    4a  \ a
    4b  \ b
    """

    LINE_1 = auto()
    LINE_2a = auto()
    LINE_2b = auto()
    LINE_3 = auto()
    LINE_4a = auto()
    LINE_4b = auto()


class SymbolMode(Enum):
    DEFAULT = auto()
    HELPER = auto()
