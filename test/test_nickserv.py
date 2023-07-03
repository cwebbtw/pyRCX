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
        client = main.ClientConnecting(None, ["details1"], None)
        client._username = "~ABCDE0123456789"
        client._nickname = "sample_nickname1"

        email = "email1@email.com"

        parameters = ["NICKSERV", "REGISTER", "password", email]
        message_type = "PRIVMSG"

        # When
        main.Nickserv_function(client, parameters, message_type)

        nickserv_entry = main.Nickserv[client._nickname]

        # Then
        self.assertEqual(nickserv_entry._email, email)

    def test_group_groups_nicknames(self):

        # Given
        group_owner_nickname = "sample_nickname2"

        client = main.ClientConnecting(None, ["details2"], None)
        client._username = "~ABCDE0123456789"
        client._nickname = group_owner_nickname

        parameters = ["NICKSERV", "REGISTER", "password", "email2@email.com"]
        message_type = "PRIVMSG"

        main.Nickserv_function(client, parameters, message_type)

        client._nickname = "sample_nickname3"

        parameters = ["NICKSERV", "GROUP", group_owner_nickname, "password"]

        # When
        main.Nickserv_function(client, parameters, message_type)

        nickserv_entry = main.Nickserv[group_owner_nickname]

        # Then
        self.assertEqual(nickserv_entry._groupnick, [client._nickname])

    def test_identify_registered_nickname(self):

        # Given
        client = main.ClientConnecting(None, ["details3"], None)
        client._username = "~ABCDE0123456789"
        client._nickname = "sample_nickname4"

        parameters = ["NICKSERV", "REGISTER", "password", "email3@email.com"]
        message_type = "PRIVMSG"

        main.Nickserv_function(client, parameters, message_type)

        client = main.ClientConnecting(None, ["details3"], None)
        client._username = "~ABCDE0123456789"
        client._nickname = "sample_nickname4"

        parameters = ["NICKSERV", "IDENTIFY", "password"]

        # When
        main.Nickserv_function(client, parameters, message_type)

        # Then
        self.assertTrue(client._MODE_register)

    def test_identify_registered_nickname_with_invalid_password(self):

        # Given
        client = main.ClientConnecting(None, ["details3"], None)
        client._username = "~ABCDE0123456789"
        client._nickname = "sample_nickname4"

        parameters = ["NICKSERV", "REGISTER", "password", "email3@email.com"]
        message_type = "PRIVMSG"

        main.Nickserv_function(client, parameters, message_type)

        client = main.ClientConnecting(None, ["details3"], None)
        client._username = "~ABCDE0123456789"
        client._nickname = "sample_nickname4"

        parameters = ["NICKSERV", "IDENTIFY", "wrongpassword"]

        # When
        main.Nickserv_function(client, parameters, message_type)

        # Then
        self.assertFalse(client._MODE_register)
