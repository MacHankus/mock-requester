
from typing import Dict

import yaml

from .exceptions.parsing_error import ParsingError


def parse_yaml_string(content: str) -> Dict:
    try:
        loaded = yaml.safe_load(content)
        return loaded
    except yaml.YAMLError:
        raise ParsingError("Provided yaml is not valid")