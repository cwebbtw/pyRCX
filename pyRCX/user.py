import logging
from abc import abstractmethod

from pyRCX.configuration import Configuration


class UserException(Exception):

    def __init__(self, message: str):
        self.message = message


class User:
    """
    Major refactor required
    """

    def __init__(self, configuration: Configuration):
        self._configuration = configuration
        self._access = []
        self._nickamount = 0
        self._nicklock = 0
        self._nickflood = 0
        self._away = ""
        self._nosendnickserv = False
        self._channels = []
        self._invites = []
        self._IRCX = False
        self._MODE_ = "+"
        self._MODE_register = False
        self._MODE_registerchat = False
        self._MODE_filter = False
        self._MODE_gag = False
        self._MODE_invisible = False
        self._MODE_inviteblock = False
        self._MODE_nowhisper = False
        self._MODE_private = False
        self._nickname = ""
        self._username = ""
        self._fullname = ""
        self._hostmask = ""
        self._hostname = ""
        self._server = self._configuration.server_name
        self._signontime = 0
        self._idletime = 0
        self._watch = []
        self.details = ["", ""]
        self._friendlyname = ""

    def has_reached_max_channels(self) -> bool:
        return len(self._channels) >= self._configuration.max_channels_per_user

    def join(self, channel):
        if not self.has_reached_max_channels():
            self._channels.append(channel)

    # TODO this should not be on the clientbase class and this needs to be
    # renamed and removed from a hierarchical sense
    @abstractmethod
    def send(self, data):
        return
