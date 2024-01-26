from typing import Dict
from typing import List
from typing import Literal

from pydantic import BaseModel

from modules.core.enums.config import IncomingRequestsTypeEnum
from modules.core.enums.http import HttpMethodsEnum


class IncomingEntity(BaseModel):
    type: IncomingRequestsTypeEnum
    path: str

    class Config:
        use_enum_values = True  # <--


class OutcomingHttpEntity(BaseModel):
    type: Literal[IncomingRequestsTypeEnum.HTTP]
    url: str
    method: HttpMethodsEnum
    payload: Dict | None = None
    headers: Dict

    class Config:
        use_enum_values = True  # <--


class ConfigTaskEntity(BaseModel):
    incoming: IncomingEntity
    outcoming: List[OutcomingHttpEntity] | OutcomingHttpEntity


class ConfigEntity(BaseModel):
    __root__: Dict[str, ConfigTaskEntity]

    def items(self):
        return self.__root__.items()
