import logging
import unittest
import sys

from pyRCX import main

class NickServTest(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

        self.mock_client = main.ClientConnecting(None, ["a"], None)
        self.mock_client._username = "~ABCDE0123456789"
        self.mock_client._nickname = "sample_nickname"

    def test_register_creates_registered_nickname(self):
        email = "email@email.com"

        parameters = ["NICKSERV", "REGISTER", "password", email]
        message_type = "PRIVMSG"

        main.Nickserv_function(self.mock_client, parameters, message_type)

        nickserv_entry = main.Nickserv[self.mock_client._nickname]

        self.assertEqual(nickserv_entry._email, email)