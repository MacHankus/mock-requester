import os
import tempfile

import pytest

from ioc_container import Container
from ioc_container import wiring_modules
from settings import settings
from tests.helpers.random import get_random_string


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

    def set_value(value: str):
        settings.CONFIG_FILE_PATH = value

    yield set_value

    settings.CONFIG_FILE_PATH = default_value


@pytest.fixture(scope="session")
def ioc_container():
    container = Container()
    container.init_resources()

    container.wire(wiring_modules)

    yield container