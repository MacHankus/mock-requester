from typing import Dict
from typing import List

from pydantic import BaseModel
from pydantic import RootModel

from modules.core.enums.http import HttpMethodsEnum


class IncomingModel(BaseModel):
    type: str
    path: str


class OutcomingHttpModel(BaseModel):
    type: str
    url: str
    method: HttpMethodsEnum
    payload: Dict | None = None
    headers: Dict | None = None,
    params: Dict | None = None


class ConfigInstructionModel(BaseModel):
    incoming: IncomingModel
    outcoming: List[OutcomingHttpModel] | OutcomingHttpModel


class ConfigModel(RootModel):
    root: Dict[str, ConfigInstructionModel]

    def items(self):
        return self.root.items()
