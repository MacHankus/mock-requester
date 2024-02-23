from typing import Dict
from typing import List
from typing import Literal

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import RootModel
from pydantic import validator

from modules.core.enums.config_enum import IncomingRequestsTypeEnum
from modules.core.enums.http import HttpMethodsEnum


class IncomingEntity(BaseModel):
    type: IncomingRequestsTypeEnum
    path: str

    model_config = ConfigDict(use_enum_values=True, validate_default=True)


class RequestResultEntity(BaseModel):
    headers: Dict | None = None
    status_code: int | None
    
    @validator('status_code', pre=True)
    def set_name(cls, val):
        return val or 204

class HttpSideEffectEntity(BaseModel):
    type: Literal["http"]
    url: str
    method: HttpMethodsEnum
    payload: Dict | None = None
    headers: Dict | None = None

    model_config = ConfigDict(use_enum_values=True, validate_default=True)


class ConfigInstructionEntity(BaseModel):
    incoming: IncomingEntity
    side_effects: List[HttpSideEffectEntity] | HttpSideEffectEntity
    request_result: RequestResultEntity | None = None


class ConfigEntity(RootModel):
    root: Dict[str, ConfigInstructionEntity]

    def items(self):
        return self.root.items()
