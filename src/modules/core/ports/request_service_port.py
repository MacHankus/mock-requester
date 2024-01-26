from abc import ABC
from abc import abstractmethod
from typing import Dict


class RequestServicePort(ABC):
    @abstractmethod
    def make_request(self, path: str, body: Dict) -> None:
        pass
