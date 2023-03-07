import os
import re

import pytest

from server_administrator.InvalidEulaException import InvalidEulaException
from server_administrator.editor import EulaEditor


# * Note: EULA == End User License Agreement
# * It's a text file that mojang creates the first time the server launches
class TestRunner:
    EULA_FILE_PATH = "./resources/eula.txt"

    @pytest.fixture(autouse=True)
    def before_and_after_each(self, request):
        if 'disable_auto_use_setting' in request.keywords:
            yield
        else:
            yield
            os.remove(self.EULA_FILE_PATH)

    def test_can_update_eula_state(self):
        self.create_eula_file(["eula = false"])
        editor = EulaEditor()

        editor.update_state(self.EULA_FILE_PATH)

        with open(self.EULA_FILE_PATH) as eula:
            last_line = eula.readlines()[-1]
            assert re.match("^eula\s?=\s?true", last_line)

    def test_if_file_is_not_valid_eula_expect_exception(self):
        self.create_eula_file(["some text that isn't the eula state"])

        with pytest.raises(InvalidEulaException):
            editor = EulaEditor()
            editor.update_state(self.EULA_FILE_PATH)

    @pytest.mark.disable_auto_use_setting
    def test_exception_raised_if_file_doesnt_exist(self):
        with pytest.raises(FileNotFoundError):
            editor = EulaEditor()
            editor.update_state("/some/path/that/is/not/the/eula/file")

    def test_can_update_eula_if_state_is_not_on_last_line(self):
        self.create_eula_file([
            "eula = false\n",
            "and another line after"
        ])
        editor = EulaEditor()

        editor.update_state(self.EULA_FILE_PATH)

        with open(self.EULA_FILE_PATH) as eula:
            lines = eula.readlines()
            pattern = re.compile("^eula\s?=\s?")
            state_line = list(filter(pattern.match, lines))
            assert len(state_line) == 1
            assert re.match("^eula\s?=\s?true", state_line[0])

    def create_eula_file(self, additional_lines: list[str]):
        with open(self.EULA_FILE_PATH, "w") as eula:
            eula.writelines([
                                "# By changing the setting below to TRUE you are indicating your agreement to our EULA (https://aka.ms/MinecraftEULA).\n",
                                "# Mon Feb 27 07:22:28 CST 2023\n",
                            ]
                            + additional_lines)
