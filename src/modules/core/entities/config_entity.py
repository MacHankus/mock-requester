from typing import Dict
from typing import List
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, RootModel

from modules.core.enums.config import IncomingRequestsTypeEnum, OutcomingTypeEnum
from modules.core.enums.http import HttpMethodsEnum


class IncomingEntity(BaseModel):
    type: IncomingRequestsTypeEnum
    path: str

    model_config = ConfigDict(use_enum_values=True, validate_default=True)


class OutcomingHttpEntity(BaseModel):
    type: Literal[OutcomingTypeEnum.HTTP.value]
    url: str
    method: HttpMethodsEnum
    payload: Dict | None = None
    headers: Dict = Field(default_factory=lambda: {})

    model_config = ConfigDict(use_enum_values=True, validate_default=True)


class ConfigInstructionEntity(BaseModel):
    incoming: IncomingEntity
    outcoming: List[OutcomingHttpEntity] | OutcomingHttpEntity


class ConfigEntity(RootModel):
    root: Dict[str, ConfigInstructionEntity]

    def items(self):
        return self.root.items()
