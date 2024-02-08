from abc import ABC
from abc import abstractmethod
from typing import Dict
from typing import List
from typing import Tuple

from modules.core.entities.config_entity import ConfigInstructionEntity


class ConfigRepositoryPort(ABC):

    @abstractmethod
    def get_instructions(self, path: str) -> List[Tuple[str, ConfigInstructionEntity]]:
        pass
