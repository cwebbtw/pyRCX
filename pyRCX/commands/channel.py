from datetime import time
from random import random
from typing import Dict, List


class JoinCommand:
    def __init__(self, channel_entries: Dict):
        self._channel_entries = channel_entries

    def execute(self, parameters: List[str]):

        # TODO what is even going on here?!
        _sleep = "%.4f" % (random() / 9)
        time.sleep(float(_sleep))

        iloop = 0
        while iloop < len(parameters[1].split(",")):
            if len(self._channels) >= myint(MaxChannelsPerUser):
                raw_messages.raw(self, "405", self._nickname, parameters[1].split(",")[iloop])
            else:

                chanclass = getChannelOBJ(param[1].split(",")[iloop].lower())
                if chanclass:
                    if chanclass.MODE_key != "":
                        if len(param) > 2:
                            if param[2] == chanclass.MODE_key:
                                chanclass.join(self._nickname, param[2])
                            elif param[2] == chanclass._prop.ownerkey:
                                if self._nickname.lower() not in chanclass._owner:
                                    if self._nickname.lower() not in chanclass._users:
                                        chanclass._owner.append(self._nickname.lower())

                                chanclass.join(self._nickname, param[2])

                            elif param[2] == chanclass._prop.hostkey:
                                if self._nickname.lower() not in chanclass._op and self._nickname.lower() not in chanclass._users:
                                    chanclass._op.append(self._nickname.lower())
                                chanclass.join(self._nickname, param[2])

                            else:
                                # send error to  user
                                raw_messages.raw(self, "475", self._nickname, chanclass.channelname)
                                if chanclass.MODE_knock:
                                    for each in chanclass._users:  # need to check for knock mode
                                        cclientid = getUserOBJ(each)
                                        cclientid.send(
                                            ":%s!%s@%s KNOCK %s 475\r\n" %
                                            (self._nickname, self._username, self._hostmask,
                                             chanclass.channelname))

                        elif self._nickname.lower() in operator_entries:
                            chanclass.join(self._nickname)

                        else:
                            # send error to  user
                            raw_messages.raw(self, "475", self._nickname, chanclass.channelname)
                            if chanclass.MODE_knock:
                                for each in chanclass._users:  # need to check for knock mode
                                    cclientid = getUserOBJ(each)
                                    cclientid.send(
                                        ":%s!%s@%s KNOCK %s 475\r\n" %
                                        (self._nickname, self._username, self._hostmask,
                                         chanclass.channelname))
                    elif len(param) > 2:
                        if param[2] == chanclass._prop.ownerkey:
                            if self._nickname.lower() not in chanclass._owner and self._nickname.lower() not in chanclass._users:
                                chanclass._owner.append(self._nickname.lower())

                        elif param[2] == chanclass._prop.hostkey:
                            if self._nickname.lower() not in chanclass._op and self._nickname.lower() not in chanclass._users:
                                chanclass._op.append(self._nickname.lower())

                        chanclass.join(self._nickname, param[2])
                    else:
                        chanclass.join(self._nickname)
                else:
                    if len(channel_entries) >= myint(MaxChannels):
                        raw_messages.raw(self, "710", self._nickname, MaxChannels)

                    elif ChanLockDown == 1:
                        raw_messages.raw(self, "702", self._nickname)
                    else:

                        if param[1].lower() not in createmute:
                            createmute[param[1].lower()] = self
                            chanclass = Channel(
                                param[1].split(",")[iloop],
                                self._nickname)  # create
                            if chanclass.channelname != "":
                                channel_entries[param[1].split(",")[iloop].lower()] = chanclass

                            del createmute[param[1].lower()]
                        else:
                            time.sleep(0.1)
                            chanclass = getChannelOBJ(param[1].split(",")[iloop].lower())
                            if chanclass:
                                chanclass.join(self._nickname)
            iloop += 1