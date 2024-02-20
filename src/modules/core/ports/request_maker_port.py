from abc import ABC
from abc import abstractmethod
from typing import Dict

from modules.core.entities.side_effect_result_entity import SideEffectResultEntity
from modules.core.enums.http import HttpMethodsEnum


class RequestMakerPort(ABC):
    @abstractmethod
    def make(
        self,
        url: str,
        method: HttpMethodsEnum,
        json: Dict | None = None,
        headers: Dict | None = None,
        params: Dict | None = None,
    ) -> SideEffectResultEntity:
        pass
