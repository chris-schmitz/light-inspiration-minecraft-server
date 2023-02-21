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
    def mock_subprocess_run(self, mocker):
        mock = MagicMock()
        mocker.patch("subprocess.run", mock)
        return mock

    @pytest.fixture(autouse=True)
    def administrator(self, mock_makedirs):
        return ServerAdministrator(
            minecraft_user="minecraft",
            directory="/opt/minecraft/server",
            port=25565,
            max_memory=1024,
            min_memory=1024,
            directory_tool=mock_makedirs
        )


class TestRunner(Fixtures):
    def test_can_build_minecraft_directory_structure(self, administrator, mock_makedirs, mock_urlretrieve):
        administrator.initialize_server()

        mock_makedirs.assert_called_with(administrator.directory, 0o755)
        assert administrator.is_initialize == True

    def test_if_directory_already_exists_the_directory_already_exists_exception_is_suppressed(self, administrator,
                                                                                              mock_makedirs,
                                                                                              mock_urlretrieve):
        mock_makedirs.side_effect = FileExistsError("Directory already exists.")

        administrator.initialize_server()

        mock_makedirs.assert_called_with(administrator.directory, 0o755)
        assert administrator.is_initialize is True

    def test_can_download_the_server_jar(self, administrator, mock_makedirs, mock_urlretrieve):
        administrator.initialize_server()

        urllib.request.urlretrieve.assert_called_with(
            url="https://piston-data.mojang.com/v1/objects/c9df48efed58511cdd0213c56b9013a7b5c9ac1f/server.jar",
            filename="/opt/minecraft/server/server.jar"
        )

    def test_if_server_is_initalized_can_perform_initial_launch(self, mocker, administrator, mock_subprocess_run,
                                                                mock_exists):
        administrator.max_memory = 4096
        administrator.min_memory = 512
        administrator.directory = "/test/directory"
        administrator.port = 5555
        administrator.user = "testuser"
        administrator.is_initialize = True
        administrator.first_launch()

        mock_subprocess_run.assert_called_with(
            [
                "/usr/bin/java",
                f'-Xmx4096M',
                f'-Xms512M',
                "-jar", "server.jar",
                "nogui"
            ],
            cwd="/test/directory"
        )

    def test_if_server_is_NOT_initalized_we_get_an_error(self, mocker, administrator, mock_subprocess_run,
                                                         mock_exists):
        administrator.is_initialize = False

        with pytest.raises(Exception) as exception:
            administrator.first_launch()

        assert str(exception.value) == "Server is not initialized"

    # TODO: break things out
    # * for each of these tests we're having to mock a lot of stuff. this seems like a good case for
    # * Breaking some of the concepts out into their own modules so they can be tested on their own and
    # * mocked out wholesale.
    def test_can_update_eula(self):
        pass
