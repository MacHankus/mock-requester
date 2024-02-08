from typing import Dict

from pydantic import ValidationError

from external.yaml.exceptions.parsing_error import ParsingError
from external.yaml.yaml_parser import parse_yaml_string
from settings import settings

from .data_models.config import ConfigModel
from .exceptions.data_corrupted_error import DataCorruptedError

config_data: Dict = {
    "config":ConfigModel({})
    }


def load_config():
    global config_data
    try:
        with open(settings.CONFIG_FILE_PATH) as content:
            parsed = parse_yaml_string(content)
            config_data["config"] = ConfigModel.model_validate(parsed)
    except ParsingError:
        raise DataCorruptedError("Data is not valid")
    except ValidationError:
        raise DataCorruptedError("Data is not valid")
