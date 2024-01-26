from modules.adapters.config.config_parser import ConfigParser
from tests.helpers.random import get_random_string
import pytest


def test_should_raise_file_not_found():
    # Arrange
    config_file_path = get_random_string()
    
    # Assert
    with pytest.raises(expected_exception=FileNotFoundError):
        cp = ConfigParser()
        cp.parse_config_file(config_file_path)
    
def test_should_parse_config_file_correctly(create_temp_file):
    # Arrange
    yaml_content= """
send_it_somewhere:
  incoming: 
    type: http
    path: /incoming/path
  outcoming:
    type: http
    url: http://target/endpoint
    method: post
    payload: {"a": 1}
    headers: 
      Content-Type: application/json
    """
    config_file_path = create_temp_file(yaml_content)
    
    # Assert
    cp = ConfigParser()
    cp.parse_config_file(config_file_path)