
from typing import Dict
import yaml

from modules.core.exceptions.parsing_error import ParsingError

def parse_yaml_string(content: str) -> Dict:
    try:
        loaded = yaml.safe_load(content)
        return loaded
    except yaml.YAMLError as exc:
        raise ParsingError("Provided yaml is not valid")