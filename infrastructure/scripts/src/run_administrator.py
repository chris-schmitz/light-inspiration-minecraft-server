import os
from os import makedirs

from server_administrator.directory_builder import DirectoryBuilder
from server_administrator.editor import EulaEditor
from server_administrator.server_administrator import ServerConfiguration, ServerAdministrator, seconds_of_sleep

if __name__ == "__main__":
    print("===> Building and launching Minecraft server <===")
    configuration = ServerConfiguration(
        directory=os.environ.get("MINECRAFT_SERVER_DIRECTORY"),
        port=os.environ.get("MINECRAFT_PORT"),
        max_memory=os.environ.get("MINECRAFT_MAX_MEMORY"),
        min_memory=os.environ.get("MINECRAFT_MIN_MEMORY")
    )
    directory_builder = DirectoryBuilder(makedirs)
    eula_editor = EulaEditor()
    administrator = ServerAdministrator(configuration, directory_builder, eula_editor, seconds_of_sleep)
    administrator.build_and_launch_server()
