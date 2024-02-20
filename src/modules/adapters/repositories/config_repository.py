from typing import List
from typing import Tuple

from external.config.config_data import config_data
from external.config.data_models.config import ConfigInstructionModel
from external.config.data_models.config import HttpSideEffectModel
from modules.core.entities.config_entity import ConfigInstructionEntity
from modules.core.entities.config_entity import HttpSideEffectEntity
from modules.core.entities.config_entity import IncomingEntity
from modules.core.enums.http import HttpMethodsEnum
from modules.core.ports.config_repository_port import ConfigRepositoryPort


class ConfigRepository(ConfigRepositoryPort):

    def _create_outcoming_entity_from_model(
        self, model: HttpSideEffectModel
    ) -> HttpSideEffectEntity:
        return HttpSideEffectEntity(
            type=model.type,  # type: ignore[arg-type]
            url=model.url,
            method=HttpMethodsEnum(model.method),
            payload=model.payload,
            headers=model.headers,
        )

    def _model_to_entity(
        self,
        instruction: ConfigInstructionModel,
    ) -> ConfigInstructionEntity:
        side_effects: List[HttpSideEffectEntity] | HttpSideEffectEntity | None = None
        if isinstance(instruction.side_effects, list):
            side_effects = [
                self._create_outcoming_entity_from_model(x)
                for x in instruction.side_effects
            ]
        if isinstance(instruction.side_effects, HttpSideEffectModel):
            side_effects = self._create_outcoming_entity_from_model(instruction.side_effects)
        if side_effects is None:
            raise ValueError(
                "Outcoming section for instruction {instruction} is not valid"
            )
        return ConfigInstructionEntity(
            incoming=IncomingEntity(
                type=instruction.incoming.type,  # type: ignore[arg-type]
                path=instruction.incoming.path,
            ),
            side_effects=side_effects,
        )

    def get_instructions(self, path: str) -> List[Tuple[str, ConfigInstructionEntity]]:
        instructions = [
            (name, self._model_to_entity(instruction))
            for name, instruction in config_data.get("config", {}).items()
            if instruction.incoming.path == path
        ]
        return instructions
