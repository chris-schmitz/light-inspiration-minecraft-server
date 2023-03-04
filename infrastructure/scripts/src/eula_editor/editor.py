import re

from eula_editor.InvalidEulaException import InvalidEulaException


class EulaEditor:
    def __init__(self, eula_relative_path: str):
        self.eula_path = eula_relative_path
        self.eula_lines: list[str]
        self._read_in_eula()
        self._validate_eula()

    def requires_state_update(self) -> bool:
        eula_agreement_state = self._get_eula_agreement_state_line()

        if re.search("=\s?false", eula_agreement_state):
            return True
        else:
            return False

    def update_state(self):
        self.eula_lines[-1] = "eula = true"
        self._write_lines_to_eula_file()

    def _validate_eula(self):
        self._get_eula_agreement_state_line()

    def _get_eula_agreement_state_line(self) -> str:
        try:
            return [line for line in self.eula_lines if re.search("^eula\s?=", line)][0]
        except IndexError:
            raise InvalidEulaException

    def _read_in_eula(self):
        with open(self.eula_path, "r") as eula:
            self.eula_lines = eula.readlines()

    def _write_lines_to_eula_file(self):
        with open(self.eula_path, "w") as file:
            file.writelines(self.eula_lines)
