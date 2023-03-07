import re
from typing import List

from InvalidEulaException import InvalidEulaException


class StateLineInformation:
    def __init__(self, state_line: str, line_index_in_file: int):
        self.text = state_line
        self.line_index_in_file = line_index_in_file


class EulaEditor:
    def update_state(self, path: str):
        lines = self._read_in_eula(path)
        updated_lines = self._set_eula_state_to_true(lines)
        self._write_lines_to_eula_file(path, updated_lines)

    def _set_eula_state_to_true(self, lines):
        state_line = self._get_eula_agreement_state_line(lines)
        state_line.text = "eula = true"
        lines[state_line.line_index_in_file] = state_line.text
        return lines

    @staticmethod
    def _get_eula_agreement_state_line(lines: List[str]) -> StateLineInformation:
        state_line_info = None
        for index, line in enumerate(lines):
            if re.search("^eula\s?=", line):
                state_line_info = StateLineInformation(line, index)

        if state_line_info is not None:
            return state_line_info
        else:
            raise InvalidEulaException

    @staticmethod
    def _read_in_eula(path: str) -> List[str]:
        with open(path, "r") as eula:
            return eula.readlines()

    @staticmethod
    def _write_lines_to_eula_file(path: str, lines: List[str]):
        with open(path, "w") as file:
            file.writelines(lines)
