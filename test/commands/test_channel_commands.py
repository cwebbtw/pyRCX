import unittest
from unittest.mock import MagicMock

from pyRCX.commands.channel import JoinCommand, PartCommand
from pyRCX.raw import Raw
from pyRCX.server_context import ServerContext
from pyRCX.user import User


class ChannelCommandsTest(unittest.TestCase):

    def setUp(self):
        self.server_context: ServerContext = ServerContext()
        self.raw_messages: Raw = MagicMock()
        self.user: User = User(self.server_context.configuration)
        self.user._nickname = "Christopher"
        self.server_context.add_user(self.user._nickname, self.user)

    def test_should_join_channel(self):
        channel_name = "#SoMeWheRe1"

        join_command: JoinCommand = JoinCommand(self.server_context, self.raw_messages)
        join_command.execute(self.user, [channel_name])

        self.assertNotEqual(self.server_context.get_channel(channel_name), None)

    def test_should_join_multiple_channels(self):
        channel_name1 = "#SoMeWheRe1"
        channel_name2 = "#SoMeWheRe2"

        join_command: JoinCommand = JoinCommand(self.server_context, self.raw_messages)
        join_command.execute(self.user, [",".join([channel_name1, channel_name2])])

        self.assertNotEqual(self.server_context.get_channel(channel_name1), None)
        self.assertNotEqual(self.server_context.get_channel(channel_name2), None)

    def test_should_part_channel(self):
        channel_name = "#SoMeWheRe1"

        join_command: JoinCommand = JoinCommand(self.server_context, self.raw_messages)
        join_command.execute(self.user, [channel_name])

        part_command: PartCommand = PartCommand(self.server_context, self.raw_messages)
        part_command.execute(self.user, [channel_name])

        self.assertEqual(self.server_context.get_channel(channel_name), None)

    def test_should_part_multiple_channels(self):
        channel_name1 = "#SoMeWheRe1"
        channel_name2 = "#SoMeWheRe2"

        parameters = [",".join([channel_name1, channel_name2])]

        join_command: JoinCommand = JoinCommand(self.server_context, self.raw_messages)
        join_command.execute(self.user, parameters)

        part_command: PartCommand = PartCommand(self.server_context, self.raw_messages)
        part_command.execute(self.user, parameters)

        self.assertEqual(self.server_context.get_channel(channel_name1), None)
        self.assertEqual(self.server_context.get_channel(channel_name2), None)
