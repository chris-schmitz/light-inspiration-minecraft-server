import urllib
from unittest.mock import MagicMock, create_autospec, Mock

import pytest

from server_administrator.server_administrator import ServerAdministrator, ServerConfiguration


class Fixtures:

    @pytest.fixture
    def mock_seconds_of_sleep(self):
        return Mock()

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
    def mock_directory_builder(self):
        from server_administrator.directory_builder import DirectoryBuilder
        mock_builder = create_autospec(DirectoryBuilder)
        return mock_builder("")

    @pytest.fixture
    def mock_eula_editor(self):
        from server_administrator.editor import EulaEditor
        mock_editor = create_autospec(EulaEditor)
        return mock_editor("")

    @pytest.fixture(autouse=True)
    def administrator(self, mock_directory_builder, server_configuration, mock_eula_editor, mock_seconds_of_sleep):
        return ServerAdministrator(
            config=server_configuration,
            builder=mock_directory_builder,
            editor=mock_eula_editor,
            sleeper=mock_seconds_of_sleep
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

    # Todo: consider abstracting
    def test_can_download_the_server_jar(self, administrator, mock_urlretrieve, mock_eula_editor, mock_subprocess_run):
        administrator.build_and_launch_server()

        urllib.request.urlretrieve.assert_called_with(
            url="https://piston-data.mojang.com/v1/objects/c9df48efed58511cdd0213c56b9013a7b5c9ac1f/server.jar",
            filename="/opt/minecraft/server/server.jar"
        )

    def test_can_correctly_launch_minecraft_jar(self, mock_directory_builder, mock_eula_editor,
                                                mock_subprocess_run, mock_seconds_of_sleep, mock_urlretrieve):
        config = ServerConfiguration(
            minecraft_user="anyuser",
            max_memory=4096,
            min_memory=512,
            directory="/test/directory",
            port=5555,
        )
        administrator = ServerAdministrator(config, mock_directory_builder, mock_eula_editor, mock_seconds_of_sleep)

        administrator.build_and_launch_server()

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

    # * I'm not actually sure the best way of spelling out this logic in a test other than this.
    # * the basic idea is that with the minecraft server we launch the jar once, the jar creates (amongst other things)
    # * the end user license agreement (the eula we need to modify) and then the jar's process exits asking you to
    # * update the eula. once it's updated we can launch the jar again and the server will run.
    # * It feels like in the spirit of "tests as documentation" we'd do something like assert the first call, then the
    # * eula update, then the second call in that order, but I don't know if that's actually possible.
    def test_can_update_eula(self, administrator, mock_eula_editor, mock_urlretrieve, mock_subprocess_run):
        administrator.build_and_launch_server()

        assert mock_subprocess_run.call_count == 2
        mock_eula_editor.update_state.assert_called_with("/opt/minecraft/server/eula.txt")
