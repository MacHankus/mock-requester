from typing import Dict
from typing import List
from typing import TypeVar

from dependency_injector.wiring import Provide
from dependency_injector.wiring import inject
from loguru import logger

from modules.adapters.replacers.replacer import replace_placeholder
from modules.adapters.replacers.replacer import replacer
from modules.core.entities.config_entity import ConfigInstructionEntity
from modules.core.entities.config_entity import RequestResultEntity
from modules.core.entities.side_effect_result_entity import SideEffectResultEntity
from modules.core.enums.config_enum import IncomingRequestsTypeEnum
from modules.core.exceptions.service_unavailable_error import ServiceUnavailableError
from modules.core.ports.config_repository_port import ConfigRepositoryPort
from modules.core.ports.request_maker_port import RequestMakerPort
from modules.core.ports.request_service_port import RequestServicePort

SideEffect = TypeVar("SideEffect")


class RequestService(RequestServicePort):
    @inject
    def __init__(
        self,
        config_repository: ConfigRepositoryPort = Provide["config_repository"],
        request_maker: RequestMakerPort = Provide["request_maker"],
    ):
        self.config_repository = config_repository
        self.request_maker = request_maker

    def make_request(self, path: str, body: Dict) -> RequestResultEntity | None:
        logger.info(f"Running request for config name: {path}")
        for key, instruction in self.config_repository.get_instructions(path=path):
            self._run_request_for_config_task(
                config_instruction=instruction, config_name=key, body=body
            )
            return instruction.request_result
        return None

    def _prepare_side_effect(
        self, requests_to_run: SideEffect | List[SideEffect]
    ) -> List[SideEffect]:
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

        requests_to_run = self._prepare_side_effect(config_instruction.side_effects)
        replacers = {
            "BODY": body,
        }

        for idx, request_to_run in enumerate(requests_to_run):
            if request_to_run.type == IncomingRequestsTypeEnum.HTTP:
                replacer(request_to_run.payload, replacers)
                request_to_run.url = replace_placeholder(request_to_run.url, replacers)
                try:
                    logger.info(f"Request[{idx}] is starting...")
                    side_effect_result: SideEffectResultEntity = (
                        self.request_maker.make(
                            url=request_to_run.url,
                            method=request_to_run.method,
                            payload=request_to_run.payload,
                            headers=request_to_run.headers,
                        )
                    )
                    replacers[f"SIDE_EFFECT[{idx}]"] = side_effect_result.model_dump()
                except ServiceUnavailableError:
                    logger.info(f"Error while doing request ({request_to_run})")
