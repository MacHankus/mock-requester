import json
from typing import Callable
from modules.core.entities.config_entity import (
    ConfigEntity,
    ConfigTaskEntity,
    IncomingEntity,
    OutcomingHttpEntity,
)
from modules.core.enums.config import IncomingRequestsTypeEnum, OutcomingTypeEnum
from modules.core.enums.http import HttpMethodsEnum
from tests.api.api_client import client
import yaml

from pytest_httpx import HTTPXMock

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
    target_method = HttpMethodsEnum.POST
    payload = {"a": 1}
    headers = {"Content-Type": "application/json"}

    config = ConfigEntity(
        {
            "send_it_somewhere": ConfigTaskEntity(
                incoming=IncomingEntity(
                    type=IncomingRequestsTypeEnum.HTTP, path=incoming_path
                ),
                outcoming=[
                    OutcomingHttpEntity(
                        type=OutcomingTypeEnum.HTTP.value,
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
    target_method = HttpMethodsEnum.POST
    payload = {"a": 1}
    headers = {"Content-Type": "application/json"}

    config = ConfigEntity(
        {
            "send_it_somewhere": ConfigTaskEntity(
                incoming=IncomingEntity(
                    type=IncomingRequestsTypeEnum.HTTP, path=incoming_path
                ),
                outcoming=[
                    OutcomingHttpEntity(
                        type=OutcomingTypeEnum.HTTP.value,
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
    assert request.method.upper() == target_method.value.upper()
    content_json = json.loads(request.content)
    assert content_json == payload


def test_should_send_http_request_from_settings_with_replaced_placeholders_from_body(
    set_config_file_path_in_settings: Callable, create_temp_file: Callable, httpx_mock: HTTPXMock
):
    # Arrange
    incoming_path = "incoming/path"
    target_path = "http://target/endpoint"
    target_method = HttpMethodsEnum.POST
    payload = {"a": "${main.target}"}
    body = {"main":{"target": "TEST"}}
    headers = {"Content-Type": "application/json"}

    config = ConfigEntity(
        {
            "send_it_somewhere": ConfigTaskEntity(
                incoming=IncomingEntity(
                    type=IncomingRequestsTypeEnum.HTTP, path=incoming_path
                ),
                outcoming=[
                    OutcomingHttpEntity(
                        type=OutcomingTypeEnum.HTTP.value,
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
