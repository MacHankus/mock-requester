from abc import ABC
from abc import abstractmethod
from typing import Dict

from modules.core.entities.config_entity import RequestResultEntity


class RequestServicePort(ABC):
    @abstractmethod
    def make_request(self, path: str, body: Dict) -> RequestResultEntity | None:
        pass
