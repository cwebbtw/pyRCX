import logging
import unittest
import sys
from unittest.mock import MagicMock, Mock, call

from pyRCX import server
from pyRCX.channel import ChannelProperties, Channel
from pyRCX.server_context import ServerContext
from pyRCX.user import User


class ChannelTest(unittest.TestCase):
    """
    The class under test is horrible and needs rewriting, but it is currently broken with
    python3 so driving the behaviour with tests will recreate the correct functionality
    """

    def setUp(self):
        self.channel = "self.channel"

        # Given
        self.server_context: ServerContext = ServerContext()
        self.server_context.configuration.channels_database_file = "/tmp/channels.dat"
        server.server_context = self.server_context

        self.user: User = User(self.server_context.configuration)
        self.user.nickname = "Christopher"
        self.server_context.add_user(self.user.nickname, self.user)

        logging.basicConfig(stream=sys.stdout, level=logging.ERROR)

        server.statistics = MagicMock()

    def test_write_users_should_save_channel(self):

        channel_information = Channel(self.server_context, MagicMock(), "self.channel", "", "")
        channel_information.MODE_registered = True
        channel_information.MODE_private = True

        channel_information._prop = ChannelProperties("chris", None)
        channel_information._prop.onjoin = "welcome"

        self.server_context.channel_entries = {"self.channel": channel_information}

        # When
        server.WriteUsers(False, True, False)

        self.server_context.channel_entries = {}

        # Then
        server.load_channel_history()

        expected_channel: server.Channel = self.server_context.channel_entries["self.channel"]

        self.assertTrue(expected_channel.MODE_registered)
        self.assertTrue(expected_channel.MODE_private)
        self.assertEqual(expected_channel.channelname, "self.channel")
        self.assertEqual(expected_channel._prop.onjoin, "welcome")

    def test_can_change_ownerkey_property(self):
        channel_information = Channel(self.server_context, MagicMock(), "self.channel", "", "")
        channel_information.MODE_optopic = False
        channel_information.join(self.user.nickname)

        mock = Mock()
        self.user.send = mock

        channel_information.change_topic(self.user, ":This is my new topic")
        mock.assert_called_once_with(f":{self.user.nickname}!{self.user._username}@{self.user._hostmask} TOPIC {self.channel} :This is my new topic\r\n")

        mock.reset_mock()

        channel_information.change_topic(self.user, "This is my new topic")
        mock.assert_called_once_with(
            f":{self.user.nickname}!{self.user._username}@{self.user._hostmask} TOPIC {self.channel} :This\r\n")

