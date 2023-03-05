import urllib
from unittest.mock import MagicMock, create_autospec

import pytest

from infrastructure.scripts.src.server_administrator import ServerAdministrator, ServerConfiguration


class Fixtures:
    @pytest.fixture
    def mock_directory_builder(self, mocker):
        mock = MagicMock()
        mocker.patch("directory_builder.DirectoryBuilder", mock)
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

    @pytest.fixture
    def mock_eula_editor(self):
        from eula_editor.editor import EulaEditor
        mock_editor = create_autospec(EulaEditor)
        return mock_editor("")

    @pytest.fixture(autouse=True)
    def administrator(self, mock_directory_builder, server_configuration, mock_eula_editor):
        return ServerAdministrator(
            config=server_configuration,
            directory_builder=mock_directory_builder,
            eula_editor=mock_eula_editor
        )

    @pytest.fixture
    def server_configuration(self):
        return ServerConfiguration(
            minecraft_user="minecraft",
            directory="/opt/minecraft/server",
            port=25565,
            max_memory=1024,
            min_memory=1024,
        )


class TestRunner(Fixtures):

    # todo: consider abstracting
    def test_can_download_the_server_jar(self, administrator, mock_urlretrieve, mock_eula_editor, mock_subprocess_run):
        administrator.initialize_server()

        urllib.request.urlretrieve.assert_called_with(
            url="https://piston-data.mojang.com/v1/objects/c9df48efed58511cdd0213c56b9013a7b5c9ac1f/server.jar",
            filename="/opt/minecraft/server/server.jar"
        )

    def test_if_server_is_initalized_can_perform_initial_launch(self, administrator, mock_subprocess_run):
        administrator.max_memory = 4096
        administrator.min_memory = 512
        administrator.directory = "/test/directory"
        administrator.port = 5555
        administrator.user = "testuser"
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

    def test_if_server_is_NOT_initalized_we_get_an_error(self, administrator, mock_subprocess_run):
        mock_subprocess_run.side_effect = Exception("Server is not initialized")
        with pytest.raises(Exception) as exception:
            administrator.first_launch()

        assert str(exception.value) == "Server is not initialized"

    def test_can_update_eula(self, administrator, mock_eula_editor, mock_urlretrieve, mock_subprocess_run, mocker):
        administrator.initialize_server()

        mock_eula_editor.update_state.assert_called_with("/opt/minecraft/server/eula.txt")
