import os
import urllib
from unittest.mock import MagicMock

import pytest

from infrastructure.scripts.src.server_administrator import SeverAdministrator


@pytest.fixture
def mock_os(mocker):
    mkdir = MagicMock()
    mocker.patch("os.makedirs", return_value=mkdir)


@pytest.fixture
def mock_urllib(mocker):
    urlopen = MagicMock()
    mocker.patch("urllib.request.urlopen", urlopen)


def test_can_build_minecraft_directory_structure(mock_os):
    administrator = SeverAdministrator(minecraft_user="minecraft", directory="/opt/minecraft/server", port=25565,
                                       max_memory=1024, min_memory=1024)

    administrator.build_directory_structure()

    os.makedirs.assert_called_with("/opt/minecraft/server", 0o755)
    # with open("/opt/minecraft/server/eula.txt", "r") as eula:
    #     re.match("^eula=true$", eula.read())


def test_can_download_the_server_jar(mock_urllib):
    administrator = SeverAdministrator(minecraft_user="minecraft", directory="/opt/minecraft/server", port=25565,
                                       max_memory=1024, min_memory=1024)

    administrator.download_server()

    urllib.request.urlopen.assert_called_with(
        "https://piston-data.mojang.com/v1/objects/c9df48efed58511cdd0213c56b9013a7b5c9ac1f/server.jar")
