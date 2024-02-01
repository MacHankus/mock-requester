from pydantic import ValidationError
from external.yaml.yaml_parser import parse_yaml_string
from external.yaml.exceptions.parsing_error import ParsingError
from settings import settings
from .data_models.config import ConfigModel
from .exceptions.data_corrupted_error import DataCorruptedError

config_data: ConfigModel = {}


def load_config():
    global config_data
    try:
        config_data = parse_yaml_string(settings.CONFIG_FILE_PATH)
        ConfigModel.model_validate(config_data)
    except ParsingError:
        raise DataCorruptedError("Data is not valid")
    except ValidationError:
        raise DataCorruptedError("Data is not valid")
