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

    def _create_outcoming_entity_from_model(
        self, model: OutcomingHttpModel
    ) -> OutcomingHttpEntity:
        return OutcomingHttpEntity(
            type=model.type,  # type: ignore[arg-type]
            url=model.url,
            method=model.method,
            payload=model.payload,
            headers=model.headers,
        )

    def _model_to_entity(
        self,
        instruction: ConfigInstructionModel,
    ) -> ConfigInstructionEntity:
        outcoming: List[OutcomingHttpEntity] | OutcomingHttpEntity | None = None
        if isinstance(instruction.outcoming, list):
            outcoming = [
                self._create_outcoming_entity_from_model(x)
                for x in instruction.outcoming
            ]
        if isinstance(instruction.outcoming, OutcomingHttpModel):
            outcoming = self._create_outcoming_entity_from_model(instruction.outcoming)
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
