import logging
import unittest
import sys

from pyRCX import server


class ChannelTest(unittest.TestCase):
    """
    The class under test is horrible and needs rewriting, but it is currently broken with
    python3 so driving the behaviour with tests will recreate the correct functionality
    """

    def setUp(self):
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    def test_write_users_should_save_channel(self):
        # Given
        channel_information = server.Channel("#somewhere", "", "")
        channel_information.MODE_registered = True
        channel_information.MODE_private = True

        channel_information._prop = server.Prop("chris", None)
        channel_information._prop.onjoin = "welcome"

        server.channels = {"#somewhere": channel_information}

        # When
        server.WriteUsers(False, True, False)

        server.channels = {}

        # Then
        server.settings()

        expected_channel: server.Channel = server.channels["#somewhere"]

        self.assertTrue(expected_channel.MODE_registered)
        self.assertTrue(expected_channel.MODE_private)
        self.assertEqual(expected_channel.channelname, "#somewhere")
        self.assertEqual(expected_channel._prop.onjoin, "welcome")
