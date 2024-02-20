from unittest.mock import patch

import pytest
import yaml

from external.config.config_data import load_config
from external.config.exceptions.data_corrupted_error import DataCorruptedError
from modules.core.enums.http import HttpMethodsEnum


@pytest.fixture()
def mock_open_and_yaml_parser(request):
    with patch("builtins.open"):
        with patch("external.config.config_data.parse_yaml_string") as parse_yaml_string:
            parse_yaml_string.return_value = yaml.safe_load(request.param)
            yield


class TestLoadConfigWithCorrectConfigs:
    @pytest.mark.parametrize(
        "mock_open_and_yaml_parser",
        [
            f"""
some-instruction:
    incoming: 
        type: http
        path: "endpoint/path/example"
    outcoming:
        type: http
        url: "http://example-host/"
        method: {en.value}
    """
            for en in HttpMethodsEnum
        ],
        indirect=True,
    )
    def test_should_load_config_with_different_http_outcoming_methods(
        self, mock_open_and_yaml_parser: str
    ):
        # Act
        load_config()


class TestLoadConfigWithIncorrectConfigs:
    @pytest.mark.parametrize(
        "mock_open_and_yaml_parser",
        [
            f"""
some-instruction:
    incorrect:
        value : 1
    """
        ],
        indirect=True,
    )
    def test_should_raise_DataCorruptedError_when_wrong_config_schema(
        self, mock_open_and_yaml_parser: str
    ):
        # Act
        with pytest.raises(expected_exception=DataCorruptedError):
            load_config()
