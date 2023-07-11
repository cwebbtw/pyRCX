from typing import Dict, Set, List, Any

from pyRCX.nickserv import NickServEntry
from pyRCX.configuration import Configuration
from pyRCX.operator import OperatorEntry
from pyRCX.user import User


class ServerContext:

    def __init__(self):
        # This class is doing too much for an object
        from pyRCX.channel import Channel
        from pyRCX.access import AccessInformation

        self.operator_entries: Dict[str, OperatorEntry] = {}
        self.nickname_to_client_mapping_entries: Dict[str, User] = {}
        self.channel_entries: Dict[str, Channel] = {}
        self.invisible_client_entries: Set[User] = set()
        self.secret_client_entries: Set[User] = set()
        self.unknown_connection_entries: Set[User] = set()
        self.nickserv_entries: Dict[str, NickServEntry] = {}
        self.server_access_entries: List[AccessInformation] = []
        self.configuration: Configuration = Configuration()

        self.currently_active_listeners: Dict[int, Any] = {}

    def add_channel(self, channel_name, channel):
        self.channel_entries[channel_name.lower()] = channel

    def remove_channel(self, channel_name: str):
        return self.channel_entries.pop(channel_name.lower(), None)

    def get_channel(self, channel: str):
        return self.channel_entries.get(channel.lower(), None)

    def add_user(self, nickname: str, user: User):
        self.nickname_to_client_mapping_entries[nickname.lower()] = user

    def get_user(self, nickname: str) -> User:
        return self.nickname_to_client_mapping_entries.get(nickname.lower(), None)

    def get_operator(self, nickname: str) -> OperatorEntry:
        return self.operator_entries.get(nickname.lower(), None)
