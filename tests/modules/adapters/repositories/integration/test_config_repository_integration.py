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
  outcoming:
    type: http
    url: "http://example-host/"
    method: post
    params: 
      param1: 1
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


class TestConfigValules:
    def test_should_return_correct_url_from_outcoming_section(
        self, set_config_file_path_in_settings: Callable, create_temp_file: Callable
    ):
        # Arrange
        incoming_path = "endpoint/path/example"
        instruction_name = "some-instruction"
        outcoming_url = "http://example-host/"
        valid_yaml_config = f"""
{instruction_name}:
  incoming: 
    type: http
    path: {incoming_path}
  outcoming:
    type: http
    url: "{outcoming_url}"
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
        assert not isinstance(instruction.outcoming, list)
        assert instruction.outcoming.url == outcoming_url

    def test_should_return_correct_params_from_outcoming_section(
        self, set_config_file_path_in_settings: Callable, create_temp_file: Callable
    ):
        # Arrange
        incoming_path = "endpoint/path/example"
        instruction_name = "some-instruction"
        outcoming_url = "http://example-host/"
        param1 = 1
        valid_yaml_config = f"""
{instruction_name}:
  incoming: 
    type: http
    path: {incoming_path}
  outcoming:
    type: http
    url: "{outcoming_url}"
    method: post
    params: 
      param1: 1
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
        assert not isinstance(instruction.outcoming, list)
        assert instruction.outcoming.params["param1"] == param1
