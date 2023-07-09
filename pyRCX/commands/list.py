from typing import List

from pyRCX.commands.command import Command
from pyRCX.helpers import int_or_zero
from pyRCX.raw import Raw
from pyRCX.server_context import ServerContext
from pyRCX.user import User


class ListCommand(Command):

    def __init__(self, server_context: ServerContext,
                 raw_messages: Raw):
        self.server_context = server_context
        self.raw_messages = raw_messages

    def _yield_channels(self):
        for each in self.server_context.channel_entries:
            yield self.server_context.channel_entries[each]

    def execute(self, user: User, parameters: List[str]):
        try:
            self.raw_messages.raw(user, "321", user._nickname)
            for chanid in self._yield_channels():
                chanusers = str(len(chanid._users) - len(chanid._watch))
                if chanid.MODE_auditorium and user._nickname.lower() not in self.self.server_context.operator_entries and isOp(
                        user._nickname.lower(), chanid.channelname) == False:
                    chanusers = str((len(chanid._op) + len(chanid._owner)))

                if chanid.visible_in_list():
                    if user._nickname.lower() in chanid._users or user._nickname.lower() in self.server_context.operator_entries:
                        self.raw_messages.raw(user, "322", user._nickname,
                                         chanid.channelname, chanusers, chanid._topic)
                else:
                    if parameters[0] == "LISTX" and len(parameters) == 2:

                        if "<" in parameters[1]:
                            if len(parameters[1].split("<")) == 2:
                                lowerthanparameters = parameters[1].split("<")[1].split(",")[0]
                            if int_or_zero(chanusers) < int_or_zero(lowerthanparameters):
                                self.raw_messages.raw(user, "322", user._nickname,
                                                 chanid.channelname, chanusers,
                                                 chanid._topic)

                        elif ">" in parameters[1]:
                            if len(parameters[1].split(">")) == 2:
                                lowerthanparameters = parameters[1].split(">")[1].split(",")[0]
                            if int_or_zero(chanusers) > int_or_zero(lowerthanparameters):
                                self.raw_messages.raw(user, "322", user._nickname,
                                                 chanid.channelname, chanusers,
                                                 chanid._topic)
                        elif "R=0" == parameters[1]:
                            if chanid.MODE_registered == False:
                                self.raw_messages.raw(user, "322", user._nickname,
                                                 chanid.channelname, chanusers,
                                                 chanid._topic)

                        elif "IRCX=0" == parameters[1]:
                            if chanid.MODE_noircx:
                                self.raw_messages.raw(user, "322", user._nickname,
                                                 chanid.channelname, chanusers,
                                                 chanid._topic)

                        elif "IRCX=1" == parameters[1]:
                            if chanid.MODE_noircx == False:
                                self.raw_messages.raw(user, "322", user._nickname,
                                                 chanid.channelname, chanusers,
                                                 chanid._topic)

                        elif "R=1" == parameters[1]:
                            if chanid.MODE_registered:
                                self.raw_messages.raw(user, "322", user._nickname,
                                                 chanid.channelname, chanusers,
                                                 chanid._topic)

                        elif "N=" in parameters[1]:
                            try:
                                matchstring = parameters[1].split("=", 1)[1].lower()
                                if matchstring in chanid.channelname.lower():
                                    self.raw_messages.raw(user, "322", user._nickname,
                                                     chanid.channelname, chanusers,
                                                     chanid._topic)

                            except:
                                pass

                        elif "T=" in parameters[1]:
                            try:
                                matchstring = parameters[1].split("=", 1)[1].lower()
                                if matchstring in chanid._topic.lower():
                                    self.raw_messages.raw(user, "322", user._nickname,
                                                     chanid.channelname, chanusers,
                                                     chanid._topic)

                            except:
                                pass

                        else:
                            self.raw_messages.raw(user, "322", user._nickname,
                                             chanid.channelname, chanusers, chanid._topic)

                    else:
                        self.raw_messages.raw(user, "322", user._nickname,
                                         chanid.channelname, chanusers, chanid._topic)
        except:
            pass

        self.raw_messages.raw(user, "323", user._nickname)