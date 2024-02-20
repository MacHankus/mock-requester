from typing import Dict
from typing import List
from typing import TypeVar

from pydantic import BaseModel
from pydantic import RootModel

from modules.core.enums.http import HttpMethodsEnum

InstructionNameType = TypeVar("InstructionNameType", bound=str)


class IncomingModel(BaseModel):
    type: str
    path: str


class OutcomingHttpModel(BaseModel):
    type: str
    url: str
    method: HttpMethodsEnum
    payload: Dict | None = None
    headers: Dict


class ConfigInstructionModel(BaseModel):
    incoming: IncomingModel
    outcoming: List[OutcomingHttpModel] | OutcomingHttpModel


class ConfigModel(RootModel):
    root: Dict[InstructionNameType, ConfigInstructionModel]

    def items(self):
        return self.root.items()
