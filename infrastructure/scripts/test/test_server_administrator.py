import urllib
from unittest.mock import MagicMock

import pytest

from infrastructure.scripts.src.server_administrator import ServerAdministrator


class Fixtures:
    @pytest.fixture
    def mock_makedirs(self, mocker):
        mock = MagicMock()
        mocker.patch("infrastructure.scripts.src.server_administrator.makedirs", mock)
        return mock

    # ! Note what's happening here
    # - We're creating a mock object
    # - we're replacing the object at the end of the path with that mock.
    # * This by itself is enough to faciltat
    @pytest.fixture
    def mock_exists(self, mocker):
        mock = MagicMock()
        mocker.patch("os.path.exists", mock)
        return mock

    @pytest.fixture
    def mock_urlretrieve(self, mocker):
        mock = MagicMock()
        mocker.patch("urllib.request.urlretrieve", mock)

    @pytest.fixture
    def mock_subprocess_call(self, mocker):
        mock = MagicMock()
        mocker.patch("subprocess.call", mock)
        return mock

    @pytest.fixture(autouse=True)
    def administrator(self):
        return ServerAdministrator(minecraft_user="minecraft", directory="/opt/minecraft/server", port=25565,
                                   max_memory=1024, min_memory=1024)


class TestRunner(Fixtures):
    def test_can_build_minecraft_directory_structure(self, administrator, mock_makedirs):
        administrator.initialize_server()

        mock_makedirs.assert_called_with(administrator.directory, 0o755)

    def test_if_directory_already_exists_the_directory_already_exists_exception_is_suppressed(self, administrator,
                                                                                              mock_makedirs):
        mock_makedirs.side_effect = Exception("Directory already exists.")

        administrator.initialize_server()

        mock_makedirs.assert_called_with(administrator.directory, 0o755)

    def test_can_download_the_server_jar(self, administrator, mock_makedirs, mock_urlretrieve):
        administrator.initialize_server()

        urllib.request.urlretrieve.assert_called_with(
            url="https://piston-data.mojang.com/v1/objects/c9df48efed58511cdd0213c56b9013a7b5c9ac1f/server.jar",
            filename="/opt/minecraft/server/server.jar"
        )

    def test_can_perform_initial_launch(self, administrator, mock_subprocess_call, mock_exists):
        administrator.first_launch()

        # ? Is this the best way of handling this idea?
        # ? is it worth even checking for the eula considering we're having to fake out it's creation??
        mock_subprocess_call.assert_called_with(
            f"{administrator.directory}/java -Xmx2048M -Xms1024M -jar server.jar nogui"
        )
        mock_exists.assert_called_with("/opt/minecraft/server/eula.txt")
