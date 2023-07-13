import logging
from typing import Dict, List

from pyRCX.channel import Channel
from pyRCX.commands.command import Command
from pyRCX.configuration import Configuration
from pyRCX.operator import OperatorEntry
from pyRCX.raw import Raw
from pyRCX.server_context import ServerContext
from pyRCX.user import User


class InviteCommand(Command):

    def __init__(self, server_context: ServerContext,
                 _raw_messages: Raw):
        self._server_context = server_context
        self._raw_messages = _raw_messages

    def execute(self, user: User, parameters: List[str]):
        if user._MODE_inviteblock:
            self._raw_messages.raw(user, "998", user.nickname, user.nickname, "*")
        else:
            channel = self._server_context.get_channel(parameters[2])
            user_to_be_invited = self._server_context.get_user(parameters[1])

            if channel is not None:
                if user.nickname.lower() in channel._users:
                    if user_to_be_invited is not None:
                        if user.nickname.lower() in channel._op or user.nickname.lower() in channel._owner:
                            if user_to_be_invited._MODE_inviteblock:
                                self._raw_messages.raw(user, "998", user.nickname,
                                                       user_to_be_invited.nickname, channel.channelname)
                            else:
                                if parameters[1].lower() in channel._users and parameters[1].lower() not in channel._watch:
                                    self._raw_messages.raw(user, "443", user.nickname,
                                                           user_to_be_invited.nickname, channel.channelname)
                                else:

                                    if not user.user_has_access_restrictions(user_to_be_invited,
                                                                         self._server_context.get_operator(
                                                                             user.nickname) is not None):
                                        self._raw_messages.raw(user, "341", user.nickname,
                                                               user_to_be_invited.nickname, channel.channelname)

                                        user_to_be_invited.send(
                                            ":%s!%s@%s INVITE %s :%s\r\n" %
                                            (user.nickname, user._username, user._hostmask,
                                             user_to_be_invited.nickname, channel.channelname))

                                        user_to_be_invited._invites.append(channel.channelname.lower())
                                    else:
                                        self._raw_messages.raw(user, "913", user.nickname, user_to_be_invited.nickname)
                        else:
                            self._raw_messages.raw(user, "482", user.nickname,
                                                   channel.channelname)
                    else:
                        self._raw_messages.raw(user, "401", user.nickname, parameters[1])
                else:
                    self._raw_messages.raw(user, "442", user.nickname, channel.channelname)
            else:
                self._raw_messages.raw(user, "403", user.nickname, parameters[2])


class KickCommand(Command):

    def __init__(self, server_context: ServerContext,
                 _raw_messages: Raw):
        self._server_context = server_context
        self._raw_messages = _raw_messages
        self._logger = logging.getLogger('COMMAND')

    def execute(self, user: User, parameters: List[str]):
        channel = self._server_context.get_channel(parameters[1])
        if channel:
            if user.nickname.lower() in channel._users:
                user_as_operator = self._server_context.get_operator(user.nickname)

                kick_message = ""
                if len(parameters) > 3:
                    kick_message = " ".join(parameters[3:])
                    kick_message = kick_message[1:] if kick_message.startswith(":") else ""

                for nickname_to_be_kicked in parameters[2].split(","):
                    if nickname_to_be_kicked in self._server_context.nickname_to_client_mapping_entries:
                        if nickname_to_be_kicked.lower() in channel._users:
                            if len(kick_message) < 128:
                                user_to_be_kicked = self._server_context.get_user(nickname_to_be_kicked)
                                if not user_to_be_kicked:
                                    self._logger.error(f"{nickname_to_be_kicked} was not found in context during kick "
                                                       f"command")
                                    continue

                                nickname_to_be_kicked_as_operator = self._server_context.get_operator(
                                    nickname_to_be_kicked)

                                if nickname_to_be_kicked_as_operator is not None and user_as_operator is None:
                                    self._raw_messages.raw(user, "481", user.nickname,
                                                           "Permission Denied - You're not a System operator")

                                elif user_to_be_kicked.nickname.lower() in self._server_context.operator_entries and user_as_operator is not None:
                                    if user_as_operator.operator_level >= nickname_to_be_kicked_as_operator.operator_level:
                                        channel.kick(user, nickname_to_be_kicked, kick_message)
                                    else:
                                        self._raw_messages.raw(user, "481", user.nickname,
                                                               "Permission Denied - Insufficient operator privileges")
                                    # operators can kick other operators but they have to be equal levels or higher
                                else:
                                    if user.nickname.lower() in channel._op:
                                        if user_to_be_kicked.nickname.lower() in channel._owner or channel.MODE_ownerkick:
                                            self._raw_messages.raw(user, "485", user.nickname, channel.channelname)
                                        else:
                                            channel.kick(user, nickname_to_be_kicked, kick_message)

                                    elif user.nickname.lower() in channel._owner:
                                        channel.kick(user, nickname_to_be_kicked, kick_message)
                                    else:
                                        if user_to_be_kicked.nickname.lower() in channel._owner:
                                            self._raw_messages.raw(user, "485", user.nickname, channel.channelname)
                                        else:
                                            self._raw_messages.raw(user, "482", user.nickname, channel.channelname)
                            else:
                                self._raw_messages.raw(user, "906", user.nickname, channel.channelname)
                        else:
                            self._raw_messages.raw(user, "441", user.nickname, channel.channelname)
                    else:
                        self._raw_messages.raw(user, "401", user.nickname, parameters[2])
            else:
                self._raw_messages.raw(user, "442", user.nickname, channel.channelname)
        else:
            self._raw_messages.raw(user, "403", user.nickname, parameters[1])


class PartCommand(Command):

    def __init__(self, server_context: ServerContext,
                 raw_messages: Raw):
        self._server_context = server_context
        self._raw_messages = raw_messages

    def execute(self, user: User, parameters: List[str]):

        for channel_name in parameters[1].split(","):
            chan = self._server_context.get_channel(channel_name)
            if chan:
                chan.part(user.nickname)
            else:
                self._raw_messages.raw(user, "403", user.nickname, channel_name)


class CreateCommand(Command):
    def __init__(self, server_context: ServerContext,
                 raw_messages: Raw):
        self._server_context = server_context
        self._raw_messages = raw_messages

    def execute(self, user: User, parameters: List[str]):
        if parameters[1].lower() in self._server_context.channel_entries:
            self._raw_messages.raw(user, "705", user.nickname, parameters[1])

        elif user.has_reached_max_channels():
            self._raw_messages.raw(user, "405", user.nickname, parameters[1])

        elif len(self._server_context.channel_entries) >= self._server_context.configuration.max_channels:
            self._raw_messages.raw(user, "710", user.nickname, self._server_context.configuration.max_channels)

        else:
            creation_modes = " ".join(parameters[2:])

            if len(parameters) == 2:
                creation_modes = "0"

            if user.nickname.lower() in self._server_context.operator_entries:
                creation_modes = creation_modes.replace("r", "").replace("e", "")

            else:
                creation_modes = creation_modes.replace(
                    "r", "").replace(
                    "N", "").replace(
                    "A", "").replace(
                    "a", "").replace(
                    "d", "").replace(
                    "e", "")

            created_channel = Channel(
                self._server_context,
                self._raw_messages,
                parameters[1],
                user.nickname, creation_modes)

            self._server_context.add_channel(parameters[1], created_channel)


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
                self._raw_messages.raw(user, "405", user.nickname, channel_name)
            else:
                channel = self._channel_entries.get(channel_name.lower(), None)
                if channel:
                    if channel.MODE_key != "":
                        if len(parameters) > 2:
                            if parameters[2] == channel.MODE_key:
                                channel.join(user.nickname, parameters[2])

                            elif parameters[2] == channel._prop.ownerkey:
                                if user.nickname.lower() not in channel._owner:
                                    if user.nickname.lower() not in channel._users:
                                        channel._owner.append(user.nickname.lower())

                                channel.join(user.nickname, parameters[2])

                            elif parameters[2] == channel._prop.hostkey:
                                if user.nickname.lower() not in channel._op and user.nickname.lower() not in channel._users:
                                    channel._op.append(user.nickname.lower())

                                channel.join(user.nickname, parameters[2])

                            else:
                                # send error to  user
                                self._raw_messages.raw(user, "475", user.nickname, channel.channelname)
                                if channel.MODE_knock:
                                    for each in channel._users:  # need to check for knock mode
                                        each_channel_user = self._nickname_to_client_mapping_entries.get(each.lower(),
                                                                                                         None)
                                        if each_channel_user:
                                            each_channel_user.send(
                                                ":%s!%s@%s KNOCK %s 475\r\n" %
                                                (user.nickname, user._username, user._hostmask, channel.channelname))

                        elif user.nickname.lower() in self._operator_entries:
                            channel.join(user.nickname)

                        else:
                            # send error to  user
                            self._raw_messages.raw(user, "475", user.nickname, channel.channelname)
                            if channel.MODE_knock:
                                for each in channel._users:  # need to check for knock mode
                                    each_channel_user = self._nickname_to_client_mapping_entries.get(each.lower(), None)
                                    each_channel_user.send(
                                        ":%s!%s@%s KNOCK %s 475\r\n" %
                                        (user.nickname, user._username, user._hostmask,
                                         channel.channelname))


                    elif len(parameters) > 2:
                        if parameters[2] == channel._prop.ownerkey:
                            if user.nickname.lower() not in channel._owner and user.nickname.lower() not in channel._users:
                                channel._owner.append(user.nickname.lower())

                        elif parameters[2] == channel._prop.hostkey:
                            if user.nickname.lower() not in channel._op and user.nickname.lower() not in channel._users:
                                channel._op.append(user.nickname.lower())

                        channel.join(user.nickname, parameters[2])
                    else:
                        channel.join(user.nickname)
                else:
                    if len(self._channel_entries) >= self._configuration.max_channels:
                        self._raw_messages.raw(user, "710", user.nickname, self._configuration.max_channels)

                    elif self._configuration.channel_lockdown == 1:
                        self._raw_messages.raw(user, "702", user.nickname)
                    else:
                        channel = Channel(self._server_context, self._raw_messages, channel_name, user.nickname)
                        if channel.channelname != "":
                            self._server_context.add_channel(channel_name, channel)
