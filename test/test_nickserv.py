import logging
import unittest
import sys

from pyRCX import main

class NickServTest(unittest.TestCase):
    """
    NickServ manages the ownership of nicknames so that people can have a sense
    of ownership when visiting the server. This test case challenges the scenarios
    that a user will perform.
    """
        
    def setUp(self):
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
        
    def test_register_creates_registered_nickname(self):

        # Given
        mock_client = main.ClientConnecting(None, ["details1"], None)
        mock_client._username = "~ABCDE0123456789"
        mock_client._nickname = "sample_nickname1"

        email = "email1@email.com"

        parameters = ["NICKSERV", "REGISTER", "password", email]
        message_type = "PRIVMSG"

        # When
        main.Nickserv_function(mock_client, parameters, message_type)

        nickserv_entry = main.Nickserv[mock_client._nickname]

        # Then
        self.assertEqual(nickserv_entry._email, email)

    def test_group_groups_nicknames(self):

        # Given
        group_owner_nickname = "sample_nickname2"

        mock_client = main.ClientConnecting(None, ["details2"], None)
        mock_client._username = "~ABCDE0123456789"
        mock_client._nickname = group_owner_nickname

        parameters = ["NICKSERV", "REGISTER", "password", "email2@email.com"]
        message_type = "PRIVMSG"

        main.Nickserv_function(mock_client, parameters, message_type)

        mock_client._nickname = "sample_nickname3"

        parameters = ["NICKSERV", "GROUP", group_owner_nickname, "password"]

        # When
        main.Nickserv_function(mock_client, parameters, message_type)

        nickserv_entry = main.Nickserv[group_owner_nickname]

        # Then
        self.assertEqual(nickserv_entry._groupnick, [mock_client._nickname])