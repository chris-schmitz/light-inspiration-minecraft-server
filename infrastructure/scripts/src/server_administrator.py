import subprocess
import time
import urllib.request
from dataclasses import dataclass
from os import makedirs, path

from directory_builder import DirectoryBuilder
from editor import EulaEditor


@dataclass
class ServerConfiguration:
    def __init__(self, minecraft_user, directory, port, max_memory, min_memory):
        self.minecraft_user = minecraft_user
        self.directory = directory
        self.port = port
        self.max_memory = max_memory
        self.min_memory = min_memory


class ServerAdministrator:

    def __init__(self, config: ServerConfiguration, directory_builder: DirectoryBuilder, eula_editor: EulaEditor):
        self.server_config = config
        self.directory_builder = directory_builder
        self.eula_editor = eula_editor

    def build_and_launch_server(self):
        self.directory_builder.build_directory_structure(self.server_config.directory)
        self._download_server()
        self._launch_jar()
        # TODO: consider abstracting
        # * the sleep time to a util function that gets injected so you can mock it and speed up the tests cases
        time.sleep(5)  # ! Not really the most elegant way of giving initial launch time to run, but this _is_ a demo :|
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


# TODO: move this to a stand alone launcher file
if __name__ == "__main__":
    print("===> Building and launching Minecraft server <===")
    config = ServerConfiguration(
        minecraft_user="minecraft",
        directory="/Users/cschmitz/Desktop/opt/minecraft/server",
        port=25565,
        max_memory=2048,
        min_memory=1024)
    directory_builder = DirectoryBuilder(makedirs)
    eula_editor = EulaEditor()
    administrator = ServerAdministrator(config, directory_builder, eula_editor)
    administrator.build_and_launch_server()
