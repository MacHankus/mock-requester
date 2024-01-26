from abc import ABC
from abc import abstractmethod

from modules.core.entities.config_entity import ConfigEntity


class ConfigParserPort(ABC):
    @abstractmethod
    def get_config(self) -> ConfigEntity:
        pass

    @abstractmethod
    def parse_config_file(self, config_file_path) -> None:
        pass
