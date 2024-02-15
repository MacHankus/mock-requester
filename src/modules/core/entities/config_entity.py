from typing import Dict
from typing import List
from typing import Literal

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field
from pydantic import RootModel

from modules.core.enums.config_enum import IncomingRequestsTypeEnum
from modules.core.enums.http import HttpMethodsEnum


class IncomingEntity(BaseModel):
    type: IncomingRequestsTypeEnum
    path: str

    model_config = ConfigDict(use_enum_values=True, validate_default=True)


class OutcomingHttpEntity(BaseModel):
    type: Literal['http']
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
