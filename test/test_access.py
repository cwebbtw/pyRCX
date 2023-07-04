import logging
import unittest
import sys

from pickle import loads
from typing import List

from pyRCX import access, server


class AccessTest(unittest.TestCase):
    """
    The class under test is horrible and needs rewriting, but it is currently broken with
    python3 so driving the behaviour with tests will recreate the correct functionality

    # TODO a repository layer for persistence would be useful here for reading and writing
    """

    def setUp(self):
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    def test_write_users_should_save_access(self):
        # Given
        access_information = access.AccessInformation("#somewhere", "OWNER", "*", "a@b", 0, "tag", 2)
        server.ServerAccess = [access_information]

        # When
        server.WriteUsers("1", "1", False, False, True)

        # Then
        with open("pyRCX/database/access.dat", "rb") as file:
            server_access: List[access.AccessInformation] = loads(file.read())

            self.assertEqual(server_access[0]._object, server.ServerAccess[0]._object)
            self.assertEqual(server_access[0]._level, server.ServerAccess[0]._level)
            self.assertEqual(server_access[0]._reason, server.ServerAccess[0]._reason)
            self.assertEqual(server_access[0]._mask, server.ServerAccess[0]._mask)
            self.assertEqual(server_access[0]._setby, server.ServerAccess[0]._setby)
            self.assertEqual(server_access[0]._setat, server.ServerAccess[0]._setat)
            self.assertEqual(server_access[0]._oplevel, server.ServerAccess[0]._oplevel)
            self.assertEqual(server_access[0]._expires, server.ServerAccess[0]._expires)
            self.assertEqual(server_access[0]._deleteafterexpire, server.ServerAccess[0]._deleteafterexpire)
