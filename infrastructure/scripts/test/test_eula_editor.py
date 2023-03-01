import os
import re

import pytest


# TODO: move out to src exception
class InvalidEulaException(Exception):
    pass


# TODO: move out to src module
class EulaEditor:
    def __init__(self, eula_relative_path: str):
        self.eula_path = eula_relative_path
        self.eula_lines: list[str]
        self._read_in_eula()
        self._validate_eula()

    def _validate_eula(self):
        self._get_eula_agreement_state_line()

    def requires_edit(self) -> bool:
        eula_agreement_state = self._get_eula_agreement_state_line()

        if re.search("=\s?false", eula_agreement_state):
            return True
        else:
            return False

    def _get_eula_agreement_state_line(self) -> str:
        try:
            return [line for line in self.eula_lines if re.search("^eula\s?=", line)][0]
        except IndexError:
            raise InvalidEulaException

    def _read_in_eula(self):
        with open(self.eula_path, "r") as eula:
            self.eula_lines = eula.readlines()


class TestRunner:
    EULA_FILE_PATH = "./resources/eula.txt"

    @pytest.fixture
    def before_and_after_each(self):
        yield
        os.remove(self.EULA_FILE_PATH)

    def test_can_confirm_eula_needs_update(self):
        self.create_eula_file(["eula = false"])

        editor = EulaEditor(self.EULA_FILE_PATH)

        assert editor.requires_edit() is True

    def test_if_file_is_not_valid_eula_expect_exception(self):
        self.create_eula_file(["some text that isn't the eula state"])

        with pytest.raises(InvalidEulaException):
            EulaEditor(self.EULA_FILE_PATH)

    @pytest.mark.skip(reason="next test")
    def test_can_update_eula_state(self):
        pass

    def create_eula_file(self, additional_lines: list[str]):
        with open(self.EULA_FILE_PATH, "w") as eula:
            eula.writelines([
                                "# By changing the setting below to TRUE you are indicating your agreement to our EULA (https://aka.ms/MinecraftEULA).\n",
                                "# Mon Feb 27 07:22:28 CST 2023\n",
                            ]
                            + additional_lines)
