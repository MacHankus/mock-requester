from modules.adapters.makers.request_maker import RequestMaker
from modules.core.enums.http import HttpMethodsEnum
from pytest_httpx import HTTPXMock


def test_should_initialize_request_maker():
    # Act
    RequestMaker()


def test_should_get_status_code_from_response(httpx_mock: HTTPXMock):
    # Arrange
    maker = RequestMaker()
    url = "http://test-endpoint"
    method = HttpMethodsEnum.POST

    httpx_mock.add_response(status_code=200)
    # Act
    response = maker.make(url=url, method=method)

    # Assert
    assert response.status_code == 200


def test_should_get_json_from_response(httpx_mock: HTTPXMock):
    # Arrange
    maker = RequestMaker()
    url = "http://test-endpoint"
    json = {"test_param": 1}
    method = HttpMethodsEnum.POST

    httpx_mock.add_response(status_code=200)
    # Act
    response = maker.make(url=url, method=method, payload=json)

    # Assert
    assert response.payload == json


def test_should_get_cookies_from_response(httpx_mock: HTTPXMock):
    # Arrange
    maker = RequestMaker()
    url = "http://test-endpoint"
    cookies = {"test_param": "test_value"}
    method = HttpMethodsEnum.POST

    httpx_mock.add_response(
        status_code=200, headers={"set-cookie": "test_param=test_value"}
    )
    # Act
    response = maker.make(url=url, method=method)

    # Assert
    assert response.cookies == cookies


def test_should_get_headers_from_response(httpx_mock: HTTPXMock):
    # Arrange
    maker = RequestMaker()
    url = "http://test-endpoint"
    headers = {"test_param": "test_value"}
    method = HttpMethodsEnum.POST

    httpx_mock.add_response(status_code=200, headers=headers)
    # Act
    response = maker.make(url=url, method=method)

    # Assert
    assert response.headers == headers
