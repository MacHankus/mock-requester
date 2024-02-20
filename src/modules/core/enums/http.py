from enum import StrEnum
from enum import auto


class HttpMethodsEnum(StrEnum):
    POST = auto()
    GET = auto()
    PUT = auto()
    DELETE = auto()
    PATCH = auto()
