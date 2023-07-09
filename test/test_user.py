import unittest
from unittest.mock import MagicMock

from pyRCX.configuration import Configuration
from pyRCX.user import User


class TestUser(unittest.TestCase):

    def test_user_can_join_channels(self):
        configuration: Configuration = Configuration()
        configuration.max_channels_per_user = 2

        user: User = User(configuration)
        self.assertFalse(user.has_reached_max_channels())

        user.join(MagicMock())
        user.join(MagicMock())

        self.assertTrue(user.has_reached_max_channels())
