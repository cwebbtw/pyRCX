from abc import abstractmethod

from pyRCX.configuration import Configuration

import pyRCX.access as access_helper


class UserException(Exception):

    def __init__(self, message: str):
        self.message = message


class User:
    """
    Major refactor required
    """

    def __init__(self, configuration: Configuration):
        # Public
        self.nickname = ""  # this should be None
        self.presented_password = False

        # TODO a mixture of public and private variables that need reviewing
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

    def user_has_access_restrictions(self, target_user, is_operator) -> bool:
        access_helper.CheckSelfExpiry(target_user)

        if is_operator:
            return False

        for each in target_user._access:
            if each._level == "DENY":
                ret = access_helper.MatchAccess(each._mask, self)
                if ret == 1:
                    for each_grant in target_user._access:
                        if each_grant._level == "GRANT":
                            gret = access_helper.MatchAccess(each_grant._mask, self)
                            if gret == 1:
                                return False
                    return True
        return False

    # TODO this should not be on the clientbase class and this needs to be
    # renamed and removed from a hierarchical sense
    @abstractmethod
    def send(self, data):
        return
