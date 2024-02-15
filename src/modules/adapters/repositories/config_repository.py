from typing import List
from typing import Tuple

from external.config.config_data import config_data
from external.config.data_models.config import ConfigInstructionModel
from external.config.data_models.config import OutcomingHttpModel
from modules.core.entities.config_entity import ConfigInstructionEntity
from modules.core.entities.config_entity import IncomingEntity
from modules.core.entities.config_entity import OutcomingHttpEntity
from modules.core.ports.config_repository_port import ConfigRepositoryPort


class ConfigRepository(ConfigRepositoryPort):
    @staticmethod
    def _model_to_entity(
        instruction: ConfigInstructionModel,
    ) -> ConfigInstructionEntity:
        outcoming: List[OutcomingHttpEntity] | OutcomingHttpEntity | None = None
        if isinstance(instruction.outcoming, list):
            outcoming = [
                OutcomingHttpEntity(
                    type=x.type,  # type: ignore[arg-type]
                    url=x.url,
                    method=x.method,
                    payload=x.payload,
                    headers=x.headers,
                )
                for x in instruction.outcoming
            ]
        if isinstance(instruction.outcoming, OutcomingHttpModel):
            outcoming = OutcomingHttpEntity(
                type=instruction.outcoming.type,  # type: ignore[arg-type]
                url=instruction.outcoming.url,
                method=instruction.outcoming.method,
                payload=instruction.outcoming.payload,
                headers=instruction.outcoming.headers,
            )
        if outcoming is None:
            raise ValueError(
                "Outcoming section for instruction {instruction} is not valid"
            )
        return ConfigInstructionEntity(
            incoming=IncomingEntity(
                type=instruction.incoming.type,  # type: ignore[arg-type]
                path=instruction.incoming.path,
            ),
            outcoming=outcoming,
        )

    def get_instructions(self, path: str) -> List[Tuple[str, ConfigInstructionEntity]]:
        instructions = [
            (name, self._model_to_entity(instruction))
            for name, instruction in config_data.get("config", {}).items()
            if instruction.incoming.path == path
        ]
        return instructions
