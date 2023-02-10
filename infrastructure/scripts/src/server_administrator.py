import subprocess
import urllib.request
from os import makedirs, path

import psutil


class ServerAdministrator:
    START_SERVER_COMMAND = 'sudo su minecraft -c "cd /opt/minecraft/server && java -Xmx1024M -Xms1024M -jar server.jar nogui"'

    def __init__(self, minecraft_user: str, directory: str, port: int, max_memory: int, min_memory: int):
        self.user = minecraft_user
        self.directory = directory
        self.port = port
        self.max_memory = max_memory
        self.min_memory = min_memory

    def initialize_server(self):
        self._build_directory_structure()
        self._download_server()

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

    def _build_directory_structure(self):
        try:
            makedirs(self.directory, 0o755)
        except Exception as e:
            if str(e) != "Directory already exists.":
                raise e

    def _download_server(self):
        urllib.request.urlretrieve(
            url="https://piston-data.mojang.com/v1/objects/c9df48efed58511cdd0213c56b9013a7b5c9ac1f/server.jar",
            filename=path.join(self.directory, "server.jar")
        )

    def first_launch(self):
        subprocess.call("java -Xmx2048M -Xms1024M -jar server.jar nogui")


if __name__ == "__main__":
    administrator = ServerAdministrator("minecraft", "/Users/cschmitz/Desktop/deleteme/", 12345, 1024, 1024)
    administrator.initialize_server()
