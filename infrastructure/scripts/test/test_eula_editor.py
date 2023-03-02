import os
import re

import pytest

from eula_editor.EulaEditor import EulaEditor
from eula_editor.InvalidEulaException import InvalidEulaException


# * Note: EULA == End User License Agreement
# * It's a text file that mojang creates the first time the server launches
class TestRunner:
    EULA_FILE_PATH = "./resources/eula.txt"

    @pytest.fixture(autouse=True)
    def before_and_after_each(self):
        yield
        os.remove(self.EULA_FILE_PATH)

    def test_can_confirm_eula_needs_update(self):
        self.create_eula_file(["eula = false"])

        editor = EulaEditor(self.EULA_FILE_PATH)

        assert editor.requires_state_update() is True

    def test_if_file_is_not_valid_eula_expect_exception(self):
        self.create_eula_file(["some text that isn't the eula state"])

        with pytest.raises(InvalidEulaException):
            EulaEditor(self.EULA_FILE_PATH)

    def test_can_update_eula_state(self):
        self.create_eula_file(["eula = false"])
        editor = EulaEditor(self.EULA_FILE_PATH)

        editor.update_state()

        with open(self.EULA_FILE_PATH) as eula:
            last_line = eula.readlines()[-1]
            assert re.match("^eula\s?=\s?true", last_line)

    def create_eula_file(self, additional_lines: list[str]):
        with open(self.EULA_FILE_PATH, "w") as eula:
            eula.writelines([
                                "# By changing the setting below to TRUE you are indicating your agreement to our EULA (https://aka.ms/MinecraftEULA).\n",
                                "# Mon Feb 27 07:22:28 CST 2023\n",
                            ]
                            + additional_lines)
