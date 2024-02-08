import pytest
import tempfile
import os
from ioc_container import Container, wiring_modules

from tests.helpers.random import get_random_string
from settings import settings 

@pytest.fixture
def create_temp_file(request):
    def _wrapper(content: str):
        temp_dir = tempfile.gettempdir()
        temp_file_path = os.path.join(temp_dir, get_random_string())
        with open(temp_file_path, 'w') as f:
            f.write(content)

        def drop_file():
            os.unlink(temp_file_path)
            
        request.addfinalizer(drop_file)

        return temp_file_path

    yield _wrapper


@pytest.fixture
def set_config_file_path_in_settings():
    default_value = settings.CONFIG_FILE_PATH

    def set_value(value: bool):
        settings.CONFIG_FILE_PATH = value

    yield set_value

    settings.CONFIG_FILE_PATH = default_value


@pytest.fixture(scope="session")
def initialize_container():
    container = Container()
    container.init_resources()

    container.wire(wiring_modules)

    yield container