from typing import Callable

from external.config.config_data import load_config
from modules.adapters.repositories.config_repository import ConfigRepository


def test_should_return_instruction_when_correct_data_in_repository(
    set_config_file_path_in_settings: Callable, create_temp_file: Callable
):
    # Arrange
    incoming_path = "endpoint/path/example"
    valid_yaml_config = f"""
some-instruction:
  incoming: 
    type: http
    path: {incoming_path}
  side_effects:
    type: http
    url: "http://example-host/"
    method: post
    payload:     
      field: 1
      field_2: 2
    headers: 
      Content-Type: application/json
"""
    temp_file_path = create_temp_file(valid_yaml_config)
    set_config_file_path_in_settings(temp_file_path)

    config_repository = ConfigRepository()
    load_config()
    # Act

    instructions = config_repository.get_instructions(incoming_path)

    # Assert
    assert len(instructions) == 1


def test_should_return_instruction_when_correct_data_in_repository_with_proper_values(
    set_config_file_path_in_settings: Callable, create_temp_file: Callable
):
    # Arrange
    incoming_path = "endpoint/path/example"
    instruction_name = "some-instruction"
    side_effects_url = "http://example-host/"
    valid_yaml_config = f"""
{instruction_name}:
  incoming: 
    type: http
    path: {incoming_path}
  side_effects:
    type: http
    url: "{side_effects_url}"
    method: post
    payload:     
      field: 1
      field_2: 2
    headers: 
      Content-Type: application/json
"""
    temp_file_path = create_temp_file(valid_yaml_config)
    set_config_file_path_in_settings(temp_file_path)

    config_repository = ConfigRepository()
    load_config()
    # Act

    instructions = config_repository.get_instructions(incoming_path)

    # Assert
    assert len(instructions) == 1

    instruction_name, instruction = instructions[0]

    assert instruction_name == instruction_name
    assert not isinstance(instruction.side_effects, list)
    assert instruction.side_effects.url == side_effects_url
