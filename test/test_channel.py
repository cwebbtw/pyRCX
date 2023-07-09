import logging
import unittest
import sys
from unittest import TestCase
from unittest.mock import MagicMock

from pyRCX import server
from pyRCX.prop import Prop
from pyRCX.server_context import ServerContext


class ChannelTest(unittest.TestCase):
    """
    The class under test is horrible and needs rewriting, but it is currently broken with
    python3 so driving the behaviour with tests will recreate the correct functionality
    """

    def setUp(self):
        logging.basicConfig(stream=sys.stdout, level=logging.ERROR)

        server.statistics = MagicMock()

    def test_write_users_should_save_channel(self):
        # Given
        server_context: ServerContext = ServerContext()

        server_context.configuration.channels_database_file = "/tmp/channels.dat"

        server.server_context = server_context

        channel_information = server.Channel(server_context, MagicMock(), "#somewhere", "", "")
        channel_information.MODE_registered = True
        channel_information.MODE_private = True

        channel_information._prop = Prop("chris", None)
        channel_information._prop.onjoin = "welcome"

        server_context.channel_entries = {"#somewhere": channel_information}

        # When
        server.WriteUsers(False, True, False)

        server_context.channel_entries = {}

        # Then
        server.load_channel_history()

        expected_channel: server.Channel = server_context.channel_entries["#somewhere"]

        self.assertTrue(expected_channel.MODE_registered)
        self.assertTrue(expected_channel.MODE_private)
        self.assertEqual(expected_channel.channelname, "#somewhere")
        self.assertEqual(expected_channel._prop.onjoin, "welcome")


class TestPartCommand(TestCase):
    pass
