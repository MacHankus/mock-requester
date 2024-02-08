from dependency_injector import containers
from dependency_injector import providers

from modules.adapters.config.config_parser import ConfigParser
from modules.adapters.makers.request_maker import RequestMaker
from modules.core.services.request_service import RequestService

wiring_modules = [
    "modules.core.services.request_service",
    "modules.adapters.api.mock_router",
]


class Container(containers.DeclarativeContainer):
    request_maker = providers.Factory(RequestMaker)
    config_parser = providers.Factory(ConfigParser)
    
    request_service = providers.Factory(
        RequestService, config_parser=config_parser, request_maker=request_maker
    )
