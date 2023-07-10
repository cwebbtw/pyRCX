from typing import List

from pyRCX.commands.command import Command
from pyRCX.raw import Raw
from pyRCX.server_context import ServerContext
from pyRCX.user import User


class TopicCommand(Command):
    def __init__(self, server_context: ServerContext,
                 _raw_messages: Raw):
        self._server_context = server_context
        self._raw_messages = _raw_messages

    def execute(self, user: User, parameters: List[str]):
        channel = self._server_context.get_channel(parameters[1])
        if channel is None:
            self._raw_messages.raw(user, "403", user.nickname, parameters[1])
            return

        if len(parameters) == 2:
            if channel.topic_visible_for_nickname(user.nickname) and channel._topic != "":
                self._raw_messages.raw(user, "332", user.nickname, channel.channelname, channel._topic)
                self._raw_messages.raw(user, "333", user.nickname, channel.channelname,
                                       channel._topic_nick, channel._topic_time)
            else:
                self._raw_messages.raw(user, "331", user.nickname, channel.channelname)
        else:
            channel.change_topic(user, " ".join(parameters[2:]))

