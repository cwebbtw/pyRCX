from pyRCX.filtering import Filtering


class Configuration:
    _DEFAULT_CHANNEL_LOCKDOWN = 0
    _DEFAULT_CHANNEL_PREFIX = "#"
    _DEFAULT_MAX_CHANNELS_PER_USER = 10
    _DEFAULT_MAX_CHANNELS = 100
    _DEFAULT_MODES = "ntl 75"
    _DEFAULT_SERVER_NAME = "pyRCX"

    def __init__(self):
        self.channel_lockdown: int = Configuration._DEFAULT_CHANNEL_LOCKDOWN
        self.channel_prefix: str = Configuration._DEFAULT_CHANNEL_PREFIX
        self.filtering: Filtering = Filtering()
        self.default_modes: str = Configuration._DEFAULT_MODES
        self.max_channels_per_user: int = Configuration._DEFAULT_MAX_CHANNELS_PER_USER
        self.max_channels: int = Configuration._DEFAULT_MAX_CHANNELS
        self.server_name: str = Configuration._DEFAULT_SERVER_NAME
