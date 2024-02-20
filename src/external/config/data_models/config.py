from typing import Dict
from typing import List
from typing import TypeVar

from pydantic import BaseModel
from pydantic import RootModel

InstructionNameType = TypeVar("InstructionNameType", bound=str)


class IncomingModel(BaseModel):
    type: str
    path: str


class HttpSideEffectModel(BaseModel):
    type: str
    url: str
    method: str
    payload: Dict | None = None
    headers: Dict | None = None


class ConfigInstructionModel(BaseModel):
    incoming: IncomingModel
    side_effects: List[HttpSideEffectModel] | HttpSideEffectModel


class ConfigModel(RootModel):
    root: Dict[InstructionNameType, ConfigInstructionModel]

    def items(self):
        return self.root.items()
