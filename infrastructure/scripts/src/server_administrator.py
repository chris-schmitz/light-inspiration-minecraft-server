import subprocess
import time
import urllib.request
from dataclasses import dataclass
from os import makedirs, path

import psutil

from directory_builder import DirectoryBuilder
from eula_editor.editor import EulaEditor


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
        time.sleep(5)
        self.eula_editor.update_state(f"{self.server_config.directory}/eula.txt")
        self._launch_jar()

    @staticmethod
    def _get_minecraft_server_process_id(self):
        process_on_target_port = list(
            filter(lambda connection: connection.laddr.port == 25565, psutil.net_connections()))
        if len(process_on_target_port) > 0:
            return process_on_target_port[0].pid
        else:
            return None

    def _download_server(self):
        urllib.request.urlretrieve(
            url="https://piston-data.mojang.com/v1/objects/c9df48efed58511cdd0213c56b9013a7b5c9ac1f/server.jar",
            filename=path.join(self.server_config.directory, "server.jar")
        )

    def _launch_jar(self):
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
