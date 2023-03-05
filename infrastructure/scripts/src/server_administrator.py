import subprocess
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
        # TODO: consider refactor
        # * consider storing all of the configs as the server config object instead of breaking
        # * them all out into individual properties
        self.directory_builder = directory_builder
        self.eula_editor = eula_editor

        self.port = config.port
        self.directory = config.directory
        self.user = config.minecraft_user
        self.max_memory = config.max_memory
        self.min_memory = config.min_memory

    # TODO: consider refactor or rename
    # ? Should this really be an initialization?? is there going to be some condition outside
    # ? of this where we'd decide to do anything other than launching the server outside of a
    # ? raised exception that would blow everything up anyway??
    # * I feel like we can come back and refactor this to be "build and run server" or just "launch"
    # * or something like that. Any deviation from launching would just be an exception that we'd be
    # * looking to the error logs to troubleshoot anyway
    def initialize_server(self):
        self.directory_builder.build_directory_structure(self.directory)
        self._download_server()
        self.first_launch()
        self.eula_editor.update_state(f"{self.directory}/eula.txt")
        # self.full_launch()

    def start_server(self):
        #     ! fire the command
        pass

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
            filename=path.join(self.directory, "server.jar")
        )

    def first_launch(self):
        subprocess.run(
            [
                "/usr/bin/java",
                f'-Xmx{self.max_memory}M',
                f'-Xms{self.min_memory}M',
                "-jar", "server.jar",
                "nogui"
            ],
            cwd=self.directory
        )


if __name__ == "__main__":
    config = ServerConfiguration(
        minecraft_user="minecraft",
        directory="/Users/cschmitz/Desktop/opt/minecraft/server",
        port=25565,
        max_memory=2048,
        min_memory=1024)
    directory_builder = DirectoryBuilder(makedirs)
    administrator = ServerAdministrator(config, directory_builder)
    administrator.initialize_server()
    administrator.first_launch()
