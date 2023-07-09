import logging
import sys
import unittest

from pickle import loads
from typing import List
from unittest.mock import MagicMock

from pyRCX import access, server
from pyRCX.server_context import ServerContext


class AccessTest(unittest.TestCase):
    """
    The class under test is horrible and needs rewriting, but it is currently broken with
    python3 so driving the behaviour with tests will recreate the correct functionality

    # TODO a repository layer for persistence would be useful here for reading and writing
    """

    def setUp(self):
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

        server.statistics = MagicMock()

    def test_write_users_should_save_access(self):
        # Given
        server_context: ServerContext = ServerContext()
        server.server_context = server_context

        access_information = access.AccessInformation("#somewhere", "OWNER", "*", "a@b", 0, "tag", 2)

        server_context.server_access_entries = [access_information]

        # When
        server.WriteUsers(False, False, True)

        # Then
        with open("database/access.dat", "rb") as file:
            server_access: List[access.AccessInformation] = loads(file.read())

            self.assertEqual(server_access[0]._object, server_context.server_access_entries[0]._object)
            self.assertEqual(server_access[0]._level, server_context.server_access_entries[0]._level)
            self.assertEqual(server_access[0]._reason, server_context.server_access_entries[0]._reason)
            self.assertEqual(server_access[0]._mask, server_context.server_access_entries[0]._mask)
            self.assertEqual(server_access[0]._setby, server_context.server_access_entries[0]._setby)
            self.assertEqual(server_access[0]._setat, server_context.server_access_entries[0]._setat)
            self.assertEqual(server_access[0]._oplevel, server_context.server_access_entries[0]._oplevel)
            self.assertEqual(server_access[0]._expires, server_context.server_access_entries[0]._expires)
            self.assertEqual(server_access[0]._deleteafterexpire, server_context.server_access_entries[0]._deleteafterexpire)
