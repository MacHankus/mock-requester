from dependency_injector import containers
from dependency_injector import providers

from modules.adapters.makers.request_maker import RequestMaker
from modules.adapters.repositories.config_repository import ConfigRepository
from modules.core.services.request_service import RequestService

wiring_modules = [
    "modules.core.services.request_service",
    "modules.adapters.api.mock_router",
]


class Container(containers.DeclarativeContainer):
    request_maker = providers.Factory(RequestMaker)
    config_repository = providers.Factory(ConfigRepository)
    request_service = providers.Factory(
        RequestService, config_repository=config_repository, request_maker=request_maker
    )
