import os
import urllib.request

import psutil


class SeverAdministrator:
    START_SERVER_COMMAND = 'sudo su minecraft -c "cd /opt/minecraft/server && java -Xmx1024M -Xms1024M -jar server.jar nogui"'

    def __init__(self, minecraft_user: str, directory: str, port: int, max_memory: int, min_memory: int):
        self.user = minecraft_user
        self.directory = directory
        self.port = port
        self.max_memory = max_memory
        self.min_memory = min_memory

    def initialize_server(self):
        self.START_SERVER_COMMAND

    @staticmethod
    def _get_minecraft_server_process_id(self):
        process_on_target_port = list(
            filter(lambda connection: connection.laddr.port == 25565, psutil.net_connections()))
        if len(process_on_target_port) > 0:
            return process_on_target_port[0].pid
        else:
            return None

    def build_directory_structure(self):
        os.makedirs(self.directory, 0o755)

    def download_server(self):
        with urllib.request.urlopen(
                "https://piston-data.mojang.com/v1/objects/c9df48efed58511cdd0213c56b9013a7b5c9ac1f/server.jar") as file:
            content = file.read().decode("utf-8")
            print(content)
