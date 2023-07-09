import unittest
from unittest.mock import MagicMock, call, Mock

from pyRCX.commands.channel import JoinCommand, PartCommand
from pyRCX.commands.list import ListCommand
from pyRCX.raw import Raw
from pyRCX.server_context import ServerContext
from pyRCX.user import User


class ListCommandsTest(unittest.TestCase):
    """
    The command tests try to drive behaviour using the commands rather
    than mocks where possible.
    """

    def setUp(self):
        self.server_context: ServerContext = ServerContext()
        self.raw_messages = Mock()
        self.user: User = User(self.server_context.configuration)
        self.user.nickname = "Christopher"
        self.server_context.add_user(self.user.nickname, self.user)

    def test_list_returns_channel(self):
        channel_name = "#SoMeWheRe1"

        join_command: JoinCommand = JoinCommand(self.server_context, self.raw_messages)
        join_command.execute(self.user, ["JOIN", channel_name])

        list_command: ListCommand = ListCommand(self.server_context, self.raw_messages)
        list_command.execute(self.user, ["LIST"])

        self.raw_messages.raw.assert_any_call(self.user, "322", self.user.nickname, channel_name, "1", "")

