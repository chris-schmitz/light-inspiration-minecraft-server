import subprocess
import urllib.request
from dataclasses import dataclass
from os import path, makedirs

import psutil

from directory_builder import DirectoryBuilder


@dataclass
class ServerConfiguration:
    def __init__(self, minecraft_user, directory, port, max_memory, min_memory):
        self.minecraft_user = minecraft_user
        self.directory = directory
        self.port = port
        self.max_memory = max_memory
        self.min_memory = min_memory


class ServerAdministrator:

    def __init__(self, config: ServerConfiguration, directory_builder: DirectoryBuilder):
        # TODO: consider refactor
        # * consider storing all of the configs as the server config object instead of breaking
        # * them all out into individual properties
        self.port = config.port
        self.directory = config.directory
        self.user = config.minecraft_user
        self.max_memory = config.max_memory
        self.min_memory = config.min_memory
        self.directory_builder = directory_builder
        self.is_initialize = False

    def initialize_server(self):

        self.directory_builder.build_directory_structure(self.directory)
        self._download_server()
        self.is_initialize = True

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
        if self.is_initialize:
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

        else:
            raise Exception("Server is not initialized")


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
