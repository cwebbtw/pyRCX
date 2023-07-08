from typing import Dict, Set

from pyRCX.configuration import Configuration
from pyRCX.operator import OperatorEntry
from pyRCX.user import User


class ServerContext:
    def __init__(self):
        self.operator_entries: Dict[str, OperatorEntry] = {}
        self.nickname_to_client_mapping_entries: Dict[str, User] = {}
        self.channel_entries: Dict = {}
        self.invisible_client_entries: Set[User] = set()
        self.secret_client_entries: Set[User] = set()
        self.unknown_connection_entries: Set[User] = set()
        self.configuration: Configuration = Configuration()
