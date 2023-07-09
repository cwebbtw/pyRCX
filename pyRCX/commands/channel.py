import time
from random import random
from typing import Dict, List

from pyRCX.channel import Channel
from pyRCX.commands.command import Command
from pyRCX.configuration import Configuration
from pyRCX.operator import OperatorEntry
from pyRCX.raw import Raw
from pyRCX.server_context import ServerContext
from pyRCX.user import User


class PartCommand(Command):

    def __init__(self, server_context: ServerContext,
                 raw_messages: Raw):
        self._server_context = server_context
        self._raw_messages = raw_messages

    def execute(self, user: User, parameters: List[str]):

        for channel_name in parameters[1].split(","):
            chan = self._server_context.get_channel(channel_name)
            if chan:
                chan.part(user._nickname)
            else:
                self._raw_messages.raw(user, "403", user._nickname, channel_name)


class JoinCommand(Command):
    def __init__(self, server_context: ServerContext,
                 raw_messages: Raw):

        self._server_context = server_context
        self._configuration: Configuration = server_context.configuration
        self._raw_messages: Raw = raw_messages
        self._operator_entries: Dict[str, OperatorEntry] = server_context.operator_entries
        self._channel_entries: Dict[str, Channel] = server_context.channel_entries
        self._nickname_to_client_mapping_entries: Dict[str, User] = server_context.nickname_to_client_mapping_entries

    def execute(self, user: User, parameters: List[str]):
        for channel_name in parameters[1].split(","):

            if user.has_reached_max_channels():
                self._raw_messages.raw(user, "405", user._nickname, channel_name)
            else:
                channel = self._channel_entries.get(channel_name.lower(), None)
                if channel:
                    if channel.MODE_key != "":
                        if len(parameters) > 2:
                            if parameters[2] == channel.MODE_key:
                                channel.join(user._nickname, parameters[2])
                            elif parameters[2] == channel._prop.ownerkey:
                                if user._nickname.lower() not in channel._owner:
                                    if user._nickname.lower() not in channel._users:
                                        channel._owner.append(user._nickname.lower())

                                channel.join(user._nickname, parameters[2])

                            elif parameters[2] == channel._prop.hostkey:
                                if user._nickname.lower() not in channel._op and user._nickname.lower() not in channel._users:
                                    channel._op.append(user._nickname.lower())
                                channel.join(user._nickname, parameters[2])

                            else:
                                # send error to  user
                                self._raw_messages.raw(user, "475", user._nickname,
                                                       channel.channelname)
                                if channel.MODE_knock:
                                    for each in channel._users:  # need to check for knock mode
                                        each_channel_user = self._nickname_to_client_mapping_entries.get(each.lower(),
                                                                                                         None)
                                        if each_channel_user:
                                            each_channel_user.send(
                                                ":%s!%s@%s KNOCK %s 475\r\n" %
                                                (user._nickname, user._username, user._hostmask, channel.channelname))

                        elif user._nickname.lower() in self._operator_entries:
                            channel.join(user._nickname)

                        else:
                            # send error to  user
                            self._raw_messages.raw(user, "475", user._nickname,
                                                   channel.channelname)
                            if channel.MODE_knock:
                                for each in channel._users:  # need to check for knock mode
                                    each_channel_user = self._nickname_to_client_mapping_entries.get(each.lower(), None)
                                    each_channel_user.send(
                                        ":%s!%s@%s KNOCK %s 475\r\n" %
                                        (user._nickname, user._username, user._hostmask,
                                         channel.channelname))


                    elif len(parameters) > 2:
                        if parameters[2] == channel._prop.ownerkey:
                            if user._nickname.lower() not in channel._owner and user._nickname.lower() not in channel._users:
                                channel._owner.append(user._nickname.lower())

                        elif parameters[2] == channel._prop.hostkey:
                            if user._nickname.lower() not in channel._op and user._nickname.lower() not in channel._users:
                                channel._op.append(user._nickname.lower())

                        channel.join(user._nickname, parameters[2])
                    else:
                        channel.join(user._nickname)
                else:
                    if len(self._channel_entries) >= self._configuration.max_channels:
                        self._raw_messages.raw(user, "710", user._nickname, self._configuration.max_channels)

                    elif self._configuration.channel_lockdown == 1:
                        self._raw_messages.raw(user, "702", user._nickname)
                    else:
                        channel = Channel(self._server_context, self._raw_messages, channel_name,
                                          user._nickname)  # create
                        if channel.channelname != "":
                            self._channel_entries[channel_name.lower()] = channel

                        # if parameters[1].lower() not in createmute:
                        #     createmute[parameters[1].lower()] = self
                        #     channel = Channel(
                        #         channel_name,
                        #         self._nickname)  # create
                        #     if channel.channelname != "":
                        #         channel_entries[
                        #             channel_name.lower()] = channel
                        #
                        #     del createmute[parameters[1].lower()]
                        # else:
                        #     # TODO what in the name of concurrency was I doing?!
                        #     time.sleep(0.1)
                        #     channel = self._channel_entries.get(channel_name.lower(), None)
                        #     if channel:
                        #         channel.join(self._nickname)
