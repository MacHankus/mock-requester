from typing import Dict

import pytest
import yaml

from external.yaml.yaml_parser import parse_yaml_string


@pytest.mark.parametrize(
    "content",
    [
        """
first_obj:
  first_field: 1
  second_field: 2
""",
        """
first_arr:
  - 1
  - 2
""",
        """
first_value: 1 # comment
""",
    ],
)
def test_should_run_without_error(content: str):
    # Act
    d = parse_yaml_string(content)

    # Assert
    d == {"first_obj": {"first_field": 1, "second_field": 2}}


@pytest.mark.parametrize(
    "dictionary",
    [
        {"test_obj": {"test_field_1": 1}},
        {"test_arr": [1, 1, 1]},
        {"test_val": 1},
    ],
)
def test_should_return_valid_dict_from_yaml_string(dictionary: Dict):
    # Arrange
    yaml_string = yaml.dump(dictionary)

    # Act
    d = parse_yaml_string(yaml_string)

    # Assert
    assert d == dictionary
