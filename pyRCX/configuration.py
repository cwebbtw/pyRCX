from typing import List, Dict

from pyRCX.filtering import Filtering
from pyRCX.operator import OperatorEntry


class Configuration:

    # Default channel configuration
    _DEFAULT_CHANNEL_LOCKDOWN = 0
    _DEFAULT_CHANNEL_PREFIX = "#"
    _DEFAULT_MAX_CHANNELS_PER_USER = 10
    _DEFAULT_MAX_CHANNELS = 100
    _DEFAULT_MODES = "ntl 75"

    _DEFAULT_SERVER_NAME = "pyRCXServ01"
    _DEFAULT_NETWORK_NAME = "pyRCXNet"

    _DEFAULT_DISABLED_FUNCTIONALITY = {}
    _DEFAULT_PROFANITY: List[str] = []
    _DEFAULT_FLOODING_EXEMPT_COMMANDS: List[str] = []

    _DEFAULT_UNENCRYPTED_PORTS: List[int] = [6667]

    _DEFAULT_SERVER_ADMIN_NAME = "pyRCX Admin"
    _DEFAULT_SERVER_ADMIN_ORGANISATION = "pyRCX Administration Group"

    # This value will be overriden if a value in the config is specified
    # Production servers should not leave the operator line (o:line) value empty
    _DEFAULT_OPERATOR_LINES: List[OperatorEntry] = [OperatorEntry("admin", "password", "aoAO", None)]

    # Flat database files - no high availability or redundancy
    _DEFAULT_CHANNELS_DATABASE = "database/channels.dat"
    _DEFAULT_ACCESS_DATABASE = "database/access.dat"
    _DEFAULT_USERS_DATABASE = "database/users.dat"
    _DEFAULT_NICKSERV_DATABASE = "database/nickserv.dat"

    # Configuration properties that can be overriden if required
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
        self.network_name: str = Configuration._DEFAULT_NETWORK_NAME
        self.operator_lines: List[OperatorEntry] = Configuration._DEFAULT_OPERATOR_LINES
        self.profanity_entries: List[str] = Configuration._DEFAULT_PROFANITY
        self.disabled_functionality: Dict[str, int] = Configuration._DEFAULT_DISABLED_FUNCTIONALITY
        self.flooding_exempt_commands: List[str] = Configuration._DEFAULT_FLOODING_EXEMPT_COMMANDS
        self.server_admin_name: str = Configuration._DEFAULT_SERVER_ADMIN_NAME
        self.server_admin_organisation: str = Configuration._DEFAULT_SERVER_ADMIN_ORGANISATION
        self.unencrypted_ports: List[int] = Configuration._DEFAULT_UNENCRYPTED_PORTS

        self.channels_database_file: str = Configuration._DEFAULT_CHANNELS_DATABASE
        self.access_database_file: str = Configuration._DEFAULT_ACCESS_DATABASE
        self.users_database_file: str = Configuration._DEFAULT_USERS_DATABASE
        self.nickserv_database_file: str = Configuration._DEFAULT_NICKSERV_DATABASE

        self.motd_config_file: str = Configuration._DEFAULT_MOTD_CONFIG
        self.server_config_file: str = Configuration._DEFAULT_SERVER_CONFIG
