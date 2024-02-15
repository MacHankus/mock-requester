from typing import Dict
from typing import List
from typing import TypeVar

from dependency_injector.wiring import Provide
from dependency_injector.wiring import inject
from loguru import logger

from modules.adapters.replacers.replacer import crawler
from modules.core.entities.config_entity import ConfigInstructionEntity
from modules.core.enums.config_enum import IncomingRequestsTypeEnum
from modules.core.exceptions.service_unavailable_error import ServiceUnavailableError
from modules.core.ports.config_repository_port import ConfigRepositoryPort
from modules.core.ports.request_maker_port import RequestMakerPort
from modules.core.ports.request_service_port import RequestServicePort

RequestsToRun = TypeVar("RequestsToRun")


class RequestService(RequestServicePort):
    @inject
    def __init__(
        self,
        config_repository: ConfigRepositoryPort = Provide["config_repository"],
        request_maker: RequestMakerPort = Provide["request_maker"],
    ):
        self.config_repository = config_repository
        self.request_maker = request_maker

    def make_request(self, path: str, body: Dict) -> None:
        logger.info(f"Running request for config name: {path}")
        for key, instruction in self.config_repository.get_instructions(path=path):
            self._run_request_for_config_task(
                config_instruction=instruction, config_name=key, body=body
            )

    def _requests_to_run(
        self, requests_to_run: RequestsToRun | List[RequestsToRun]
    ) -> List[RequestsToRun]:
        if isinstance(requests_to_run, list):
            requests_to_run = requests_to_run
        else:
            requests_to_run = [requests_to_run]

        return requests_to_run

    def _run_request_for_config_task(
        self, config_instruction: ConfigInstructionEntity, config_name: str, body: Dict
    ) -> None:
        logger.info(
            f"Config with name: {config_name} is configured for path: {config_instruction.incoming.path}"
        )

        requests_to_run = self._requests_to_run(config_instruction.outcoming)

        for idx, request_to_run in enumerate(requests_to_run):
            if request_to_run.type == IncomingRequestsTypeEnum.HTTP:
                crawler(request_to_run.payload, body)
                try:
                    logger.info(f"Request[{idx}] is starting...")
                    self.request_maker.make(
                        url=request_to_run.url,
                        method=request_to_run.method,
                        payload=request_to_run.payload,
                        headers=request_to_run.headers,
                    )
                except ServiceUnavailableError:
                    logger.info(f"Error while doing request ({request_to_run})")
