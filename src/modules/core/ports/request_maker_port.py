from abc import ABC
from abc import abstractmethod
from typing import Dict

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
    ) -> None:
        pass
