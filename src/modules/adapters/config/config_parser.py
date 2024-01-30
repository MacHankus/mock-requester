from os.path import isfile
from pathlib import Path

import yaml
from pydantic import ValidationError
from pydantic import parse_obj_as
from loguru import logger

from modules.core.entities.config_entity import ConfigEntity
from modules.core.ports.config_parser_port import ConfigParserPort


class ConfigParser(ConfigParserPort):
    config: ConfigEntity | None = None


    def _parse(self, d: dict):
        try:
            parsed = ConfigEntity(**d)
            return parsed
        except ValidationError as e:
            logger.exception("Error while parsing file.")
            raise e

    def _parse_config_file(self, config: str):
        with open(config, "r") as stream:
            try:
                loaded = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                raise exc
        return self._parse(loaded)

    def parse_config_file(self, config_file_path) -> None:
        pathlike = Path(config_file_path)
        if not isfile(pathlike):
            raise FileNotFoundError(f"File {config_file_path} does not exist.")
        self.config = self._parse_config_file(config_file_path)
        
    def get_config(self) -> ConfigEntity:
        return self.config
