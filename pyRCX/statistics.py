import logging
from typing import Dict

from pyRCX.clientbase import ClientBaseClass


class Statistics:
    """
    A class representing statistics, which maintains running counts of totals and statistics
    regarding the server. This class should be used for all types of statistics rather than
    how it currently is where calculations are all over the place.
    """

    def __init__(self, nickname_to_client_mapping_entries: Dict[str, ClientBaseClass]):
        self._nickname_to_client_mapping_entries = nickname_to_client_mapping_entries
        self._max_local = len(self._nickname_to_client_mapping_entries)

        self.logger = logging.getLogger('STATISTICS')

    def max_global_users(self) -> int:
        return self.max_local_users()

    def max_local_users(self) -> int:
        current_count = len(self._nickname_to_client_mapping_entries)
        if current_count > self._max_local:
            self._max_local = current_count

        return self._max_local

    def current_local_users(self) -> int:
        return len(self._nickname_to_client_mapping_entries)

    def current_global_users(self) -> int:
        return len(self._nickname_to_client_mapping_entries)

    def save(self):
        with open("pyRCX/database/users.dat", "w") as file:
            file.write(f"{self.max_local_users()}")

    def load(self):
        try:
            with open("pyRCX/database/users.dat", "r") as file:
                self._max_local = int(file.read().strip() or 0)
        except IOError as e:
            self.logger.warning(e)
            self._max_local = 0
