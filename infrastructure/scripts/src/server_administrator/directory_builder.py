class DirectoryBuilder:

    def __init__(self, directory_tool):
        self.makedirs = directory_tool

    def build_directory_structure(self, directory):
        try:
            self.makedirs(directory, 0o755)
        except FileExistsError as e:
            pass
