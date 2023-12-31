import logging
import time

from pyRCX.configuration import Configuration


class Statistics:
    """
    A class representing statistics, which maintains running counts of totals and statistics
    regarding the server. This class should be used for all types of statistics rather than
    how it currently is where calculations are all over the place.
    """

    server_launch = time.strftime(" :On-line since %A %B %d %H:%M:%S %Y", time.localtime())

    def __init__(self, server_context):
        self._configuration: Configuration = server_context.configuration
        self._invisible_client_entries = server_context.invisible_client_entries
        self._nickname_to_client_mapping_entries = server_context.nickname_to_client_mapping_entries
        self._operator_entries = server_context.operator_entries
        self._secret_client_entries = server_context.secret_client_entries
        self._unknown_connection_entries = server_context.unknown_connection_entries
        self._channel_entries = server_context.channel_entries
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

    def current_online_operators(self) -> int:
        total_operators_online = len(self._operator_entries) - len(self._secret_client_entries)

        if total_operators_online < 0:
            self.logger.warning(
                f"Encountered a negative value ({total_operators_online}) "
                f"for total visible operators (total={len(self._operator_entries)}, "
                f"secret={len(self._secret_client_entries)})")
            total_operators_online = 0

        return total_operators_online

    def current_online_users(self) -> int:
        total_online_users = len(self._nickname_to_client_mapping_entries) - len(self._invisible_client_entries)

        if total_online_users < 0:
            self.logger.warning(
                f"Encountered a negative value {total_online_users} "
                f"for total visible clients (total={len(self._nickname_to_client_mapping_entries)}, "
                f"invisible={len(self._invisible_client_entries)}")
            total_online_users = 0

        return total_online_users

    def current_invisible_users(self) -> int:
        return len(self._invisible_client_entries)

    def current_unknown_connections(self) -> int:
        return len(self._unknown_connection_entries)

    def current_channels(self) -> int:
        return len(self._channel_entries)

    def save(self):
        with open(self._configuration.users_database_file, "w") as file:
            file.write(f"{self.max_local_users()}")

    def load(self):
        try:
            with open(self._configuration.users_database_file, "r") as file:
                self._max_local = int(file.read().strip() or 0)
        except IOError as e:
            self.logger.info("User database not found, it will be created at save points")
            self.logger.debug(e)
            self._max_local = 0
