import subprocess
import time
import urllib.request
from dataclasses import dataclass
from os import path

from server_administrator.directory_builder import DirectoryBuilder
from server_administrator.editor import EulaEditor


def seconds_of_sleep(seconds: int):
    time.sleep(seconds)


@dataclass
class ServerConfiguration:
    def __init__(self, directory, port, max_memory, min_memory):
        self.directory = directory
        self.port = port
        self.max_memory = max_memory
        self.min_memory = min_memory


class ServerAdministrator:

    def __init__(self, config: ServerConfiguration, builder: DirectoryBuilder, editor: EulaEditor, sleeper):
        self.server_config = config
        self.directory_builder = builder
        self.eula_editor = editor
        self.seconds_of_sleep = sleeper

    def build_and_launch_server(self):
        self.directory_builder.build_directory_structure(self.server_config.directory)
        self._download_server()
        self._launch_jar()
        self.seconds_of_sleep(5)
        self.eula_editor.update_state(f"{self.server_config.directory}/eula.txt")
        self._launch_jar()

    # TODO: yeah prob best to pull this out into it's own class
    def _download_server(self):
        urllib.request.urlretrieve(
            # ! really, this url should be parameterized, maybe pull in from an ENV var? but again, just a demo
            url="https://piston-data.mojang.com/v1/objects/c9df48efed58511cdd0213c56b9013a7b5c9ac1f/server.jar",
            filename=path.join(self.server_config.directory, "server.jar")
        )

    def _launch_jar(self):
        # ! also note that if this was a real server build'n launch util we'd be creating a new user, su-ing into that
        # ! user account, and running as the user, but again again, demo.
        subprocess.run(
            [
                "/usr/bin/java",
                f'-Xmx{self.server_config.max_memory}M',
                f'-Xms{self.server_config.min_memory}M',
                "-jar", "server.jar",
                "nogui"
            ],
            cwd=self.server_config.directory
        )
