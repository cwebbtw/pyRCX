from typing import List

from pyRCX.filtering import Filtering


class Configuration:
    _DEFAULT_CHANNEL_LOCKDOWN = 0
    _DEFAULT_CHANNEL_PREFIX = "#"
    _DEFAULT_MAX_CHANNELS_PER_USER = 10
    _DEFAULT_MAX_CHANNELS = 100
    _DEFAULT_MODES = "ntl 75"
    _DEFAULT_SERVER_NAME = "pyRCX"
    _DEFAULT_PROFANITY = []
    _DEFAULT_FLOODING_EXEMPT_COMMANDS = []

    _DEFAULT_CHANNELS_DATABASE = "database/channels.dat"
    _DEFAULT_ACCESS_DATABASE = "database/access.dat"
    _DEFAULT_USERS_DATABASE = "database/users.dat"
    _DEFAULT_NICKSERV_DATABASE = "database/nickserv.dat"

    _DEFAULT_MOTD_CONFIG = "conf/motd.conf"
    _DEFAULT_SERVER_CONFIG = "conf/pyRCX.conf"

    VERSION = "v3.0.1"

    def __init__(self):
        self.channel_lockdown: int = Configuration._DEFAULT_CHANNEL_LOCKDOWN
        self.channel_prefix: str = Configuration._DEFAULT_CHANNEL_PREFIX
        self.filtering: Filtering = Filtering()
        self.default_modes: str = Configuration._DEFAULT_MODES
        self.max_channels_per_user: int = Configuration._DEFAULT_MAX_CHANNELS_PER_USER
        self.max_channels: int = Configuration._DEFAULT_MAX_CHANNELS
        self.server_name: str = Configuration._DEFAULT_SERVER_NAME
        self.profanity_entries: List[str] = Configuration._DEFAULT_PROFANITY
        self.flooding_exempt_commands: List[str] = Configuration._DEFAULT_FLOODING_EXEMPT_COMMANDS

        self.channels_database_file: str = Configuration._DEFAULT_CHANNELS_DATABASE
        self.access_database_file: str = Configuration._DEFAULT_ACCESS_DATABASE
        self.users_database_file: str = Configuration._DEFAULT_USERS_DATABASE
        self.nickserv_database_file: str = Configuration._DEFAULT_NICKSERV_DATABASE

        self.motd_config_file: str = Configuration._DEFAULT_MOTD_CONFIG
        self.server_config_file: str = Configuration._DEFAULT_SERVER_CONFIG
