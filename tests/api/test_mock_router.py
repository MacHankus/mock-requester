import json
from typing import Callable

import yaml
from pytest_httpx import HTTPXMock

from external.config.config_data import load_config
from external.config.data_models.config import ConfigInstructionModel
from external.config.data_models.config import ConfigModel
from external.config.data_models.config import HttpSideEffectModel
from external.config.data_models.config import IncomingModel
from modules.core.enums.config_enum import IncomingRequestsTypeEnum
from modules.core.enums.config_enum import OutcomingTypeEnum
from modules.core.enums.http import HttpMethodsEnum
from tests.api.api_client import client


def test_should_return_204():
    # Act
    response = client.post(
        url="/",
    )

    # Assert
    assert response.status_code == 204


def test_should_send_request_from_settings_with_success(
    set_config_file_path_in_settings: Callable, create_temp_file: Callable
):
    # Arrange
    incoming_path = "incoming/path"
    target_path = "http://target/endpoint"
    target_method = HttpMethodsEnum.POST.value
    payload = {"a": 1}
    headers = {"Content-Type": "application/json"}

    config = ConfigModel(
        {
            "send_it_somewhere": ConfigInstructionModel(
                incoming=IncomingModel(
                    type=IncomingRequestsTypeEnum.HTTP.value, path=incoming_path
                ),
                side_effects=[
                    HttpSideEffectModel(
                        type=OutcomingTypeEnum.HTTP.value, # type: ignore[arg-type]
                        url=target_path,
                        method=target_method,
                        payload=payload,
                        headers=headers,
                    )
                ],
            )
        }
    )
    config_dict = config.model_dump()
    yaml_content = yaml.dump(config_dict)
    config_file_path = create_temp_file(yaml_content)
    set_config_file_path_in_settings(config_file_path)
    load_config()

    # Act
    response = client.post(
        url=incoming_path,
    )

    # Assert
    assert response.status_code == 204

def test_should_send_http_request_from_settings(
    set_config_file_path_in_settings: Callable, create_temp_file: Callable, httpx_mock: HTTPXMock
):
    # Arrange
    incoming_path = "incoming/path"
    target_path = "http://target/endpoint"
    target_method = HttpMethodsEnum.POST.value
    payload = {"a": 1}
    headers = {"Content-Type": "application/json"}

    config = ConfigModel(
        {
            "send_it_somewhere": ConfigInstructionModel(
                incoming=IncomingModel(
                    type=IncomingRequestsTypeEnum.HTTP.value, path=incoming_path
                ),
                side_effects=[
                    HttpSideEffectModel(
                        type=OutcomingTypeEnum.HTTP.value, # type: ignore[arg-type]
                        url=target_path,
                        method=target_method,
                        payload=payload,
                        headers=headers,
                    )
                ],
            )
        }
    )
    config_dict = config.model_dump()
    yaml_content = yaml.dump(config_dict)
    config_file_path = create_temp_file(yaml_content)
    set_config_file_path_in_settings(config_file_path)
    load_config()

    httpx_mock.add_response(url=target_path)
    # Act
    response = client.post(
        url=incoming_path,
    )

    # Assert
    assert response.status_code == 204

    request = httpx_mock.get_request()
    assert request
    assert request.url == target_path
    assert request.method.upper() == target_method.upper()
    content_json = json.loads(request.content)
    assert content_json == payload


def test_should_send_http_request_from_settings_with_replaced_placeholders_from_body(
    set_config_file_path_in_settings: Callable, create_temp_file: Callable, httpx_mock: HTTPXMock
):
    # Arrange
    incoming_path = "incoming/path"
    target_path = "http://target/endpoint"
    target_method = HttpMethodsEnum.POST.value
    payload = {"a": "${main.target}"}
    body = {"main":{"target": "TEST"}}
    headers = {"Content-Type": "application/json"}

    config = ConfigModel(
        {
            "send_it_somewhere": ConfigInstructionModel(
                incoming=IncomingModel(
                    type=IncomingRequestsTypeEnum.HTTP.value, path=incoming_path
                ),
                side_effects=[
                    HttpSideEffectModel(
                        type=OutcomingTypeEnum.HTTP.value, # type: ignore[arg-type]
                        url=target_path,
                        method=target_method,
                        payload=payload,
                        headers=headers,
                    )
                ],
            )
        }
    )
    config_dict = config.model_dump()
    yaml_content = yaml.dump(config_dict)
    config_file_path = create_temp_file(yaml_content)
    set_config_file_path_in_settings(config_file_path)
    load_config()

    httpx_mock.add_response(url=target_path)
    # Act
    response = client.post(
        url=incoming_path, json=body
    )

    # Assert
    assert response.status_code == 204

    request = httpx_mock.get_request()
    assert request
    content_json = json.loads(request.content)
    assert content_json["a"] == body["main"]["target"]
