from unittest.mock import Mock

from modules.core.entities.config_entity import ConfigInstructionEntity
from modules.core.entities.config_entity import HttpSideEffectEntity
from modules.core.entities.config_entity import IncomingEntity
from modules.core.enums.config_enum import IncomingRequestsTypeEnum
from modules.core.enums.config_enum import OutcomingTypeEnum
from modules.core.enums.http import HttpMethodsEnum
from modules.core.services.request_service import RequestService
from tests.helpers.random import get_random_string


def test_should_initialize_sesrvice():
    # Act
    RequestService(config_repository=Mock(), request_maker=Mock())


def test_should_not_call_request_maker_when_no_instructions_found():
    # Arrange
    path = "some/test/endpoint/path"
    body = {}
    config_repository_mock = Mock()
    config_repository_mock.get_instructions.return_value = []

    request_maker_mock = Mock()
    request_maker_mock.make = Mock()

    service = RequestService(
        config_repository=config_repository_mock, request_maker=request_maker_mock
    )

    # Act

    service.make_request(path=path, body=body)

    # Assert

    request_maker_mock.make.assert_not_called()


def test_should_call_request_maker_once_when_instruction_has_one_outcoming_object():
    # Arrange
    path = "some/test/endpoint/path"
    body = {}
    config_repository_mock = Mock()
    config_repository_mock.get_instructions.return_value = [
        (
            "some-instruction-name",
            ConfigInstructionEntity(
                incoming=IncomingEntity(type=IncomingRequestsTypeEnum.HTTP, path=path),
                side_effects=HttpSideEffectEntity(
                    type=OutcomingTypeEnum.HTTP.value,
                    url=get_random_string(),
                    method=HttpMethodsEnum.GET,
                ),
            ),
        )
    ]

    request_maker_mock = Mock()
    request_maker_mock.make = Mock()

    service = RequestService(
        config_repository=config_repository_mock, request_maker=request_maker_mock
    )

    # Act

    service.make_request(path=path, body=body)

    # Assert

    request_maker_mock.make.assert_called_once()


def test_should_call_request_maker_twice_when_instruction_has_two_outcoming_objects():
    # Arrange
    path = "some/test/endpoint/path"
    body = {}
    config_repository_mock = Mock()
    config_repository_mock.get_instructions.return_value = [
        (
            "some-instruction-name",
            ConfigInstructionEntity(
                incoming=IncomingEntity(type=IncomingRequestsTypeEnum.HTTP, path=path),
                side_effects=[
                    HttpSideEffectEntity(
                        type=OutcomingTypeEnum.HTTP.value,
                        url=get_random_string(),
                        method=HttpMethodsEnum.GET,
                    ),
                    HttpSideEffectEntity(
                        type=OutcomingTypeEnum.HTTP.value,
                        url=get_random_string(),
                        method=HttpMethodsEnum.GET,
                    ),
                ],
            ),
        )
    ]

    request_maker_mock = Mock()
    request_maker_mock.make = Mock()

    service = RequestService(
        config_repository=config_repository_mock, request_maker=request_maker_mock
    )

    # Act

    service.make_request(path=path, body=body)

    # Assert

    assert request_maker_mock.make.call_count == 2
