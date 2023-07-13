import unittest
from unittest.mock import MagicMock

from pyRCX.commands.channel import JoinCommand, PartCommand, CreateCommand
from pyRCX.raw import Raw
from pyRCX.server_context import ServerContext
from pyRCX.user import User


class ChannelCommandsTest(unittest.TestCase):

    def setUp(self):
        self.server_context: ServerContext = ServerContext()
        self.raw_messages: Raw = MagicMock()
        self.user: User = User(self.server_context.configuration)
        self.user.nickname = "Christopher"
        self.server_context.add_user(self.user.nickname, self.user)

    def test_join_should_raise_index_error_for_not_enough_parameters(self):
        join_command: JoinCommand = JoinCommand(self.server_context, self.raw_messages)

        with self.assertRaises(IndexError):
            join_command.execute(self.user, ["JOIN"])

    def test_part_should_raise_index_error_for_not_enough_parameters(self):
        part_command: PartCommand = PartCommand(self.server_context, self.raw_messages)

        with self.assertRaises(IndexError):
            part_command.execute(self.user, ["PART"])

    def test_should_join_channel(self):
        channel_name = "#SoMeWheRe1"

        join_command: JoinCommand = JoinCommand(self.server_context, self.raw_messages)
        join_command.execute(self.user, ["JOIN", channel_name])

        self.assertNotEqual(self.server_context.get_channel(channel_name), None)

    def test_should_join_multiple_channels(self):
        channel_name1 = "#SoMeWheRe1"
        channel_name2 = "#SoMeWheRe2"

        join_command: JoinCommand = JoinCommand(self.server_context, self.raw_messages)
        join_command.execute(self.user, ["JOIN", ",".join([channel_name1, channel_name2])])

        self.assertNotEqual(self.server_context.get_channel(channel_name1), None)
        self.assertNotEqual(self.server_context.get_channel(channel_name2), None)

    def test_should_part_channel(self):
        channel_name = "#SoMeWheRe1"

        join_command: JoinCommand = JoinCommand(self.server_context, self.raw_messages)
        join_command.execute(self.user, ["PART", channel_name])

        part_command: PartCommand = PartCommand(self.server_context, self.raw_messages)
        part_command.execute(self.user, ["PART", channel_name])

        self.assertEqual(self.server_context.get_channel(channel_name), None)

    def test_should_part_multiple_channels(self):
        channel_name1 = "#SoMeWheRe1"
        channel_name2 = "#SoMeWheRe2"

        join_command: JoinCommand = JoinCommand(self.server_context, self.raw_messages)
        join_command.execute(self.user, ["JOIN", ",".join([channel_name1, channel_name2])])

        part_command: PartCommand = PartCommand(self.server_context, self.raw_messages)
        part_command.execute(self.user, ["PART", ",".join([channel_name1, channel_name2])])

        self.assertEqual(self.server_context.get_channel(channel_name1), None)
        self.assertEqual(self.server_context.get_channel(channel_name2), None)

    def test_can_create_channel_with_modes(self):
        channel_name1 = "#SoMeWheRe1"
        create_command: CreateCommand = CreateCommand(self.server_context, self.raw_messages)

        create_command.execute(self.user, ["CREATE", channel_name1, "ni"])

        channel = self.server_context.get_channel(channel_name1)

        self.assertIsNotNone(channel)
        self.assertTrue(channel.MODE_inviteonly)
        self.assertTrue(channel.MODE_externalmessages)