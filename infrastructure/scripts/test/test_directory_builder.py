import shutil
from os import makedirs, path

import pytest

from server_administrator.directory_builder import DirectoryBuilder


class TestRunner:
    _ROOT_OF_TARGET_DIRECTORY = "./delete_this"
    TARGET_DIRECTORY = f"{_ROOT_OF_TARGET_DIRECTORY}/test/directory"

    @pytest.fixture(autouse=True)
    def run_after_each_test(self):
        yield  # * yield says "pause while the tests run, so everything after yield is after a tests * #
        shutil.rmtree(self._ROOT_OF_TARGET_DIRECTORY)

    def test_can_build_minecraft_directory_structure(self):
        builder = DirectoryBuilder(makedirs)

        builder.build_directory_structure(self.TARGET_DIRECTORY)
        path.exists(self.TARGET_DIRECTORY)

    def test_if_directory_already_exists_the_directory_already_exists_exception_is_suppressed(self):
        builder = DirectoryBuilder(makedirs)
        makedirs(self.TARGET_DIRECTORY)

        builder.build_directory_structure(self.TARGET_DIRECTORY)
        path.exists(self.TARGET_DIRECTORY)
