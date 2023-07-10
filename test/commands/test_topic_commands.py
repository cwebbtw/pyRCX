import unittest
from unittest.mock import Mock

from pyRCX.commands.channel import JoinCommand
from pyRCX.commands.topic import TopicCommand
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

        mock = Mock()
        self.server_context.get_channel(channel_name).change_topic = mock

        topic_command: TopicCommand = TopicCommand(self.server_context, self.raw_messages)
        topic_command.execute(self.user, ["TOPIC", channel_name, "Hello"])

        mock.assert_called_once_with(self.user, "Hello")
