import logging
import unittest
from unittest.mock import MagicMock

from pyRCX.server_context import ServerContext
from pyRCX.statistics import Statistics


class TestStatistics(unittest.TestCase):

    def setUp(self):
        logging.disable(logging.WARNING)

    def test_max_local_user_count(self):
        server_context: ServerContext = ServerContext()
        server_context.nickname_to_client_mapping_entries = {"christopher": MagicMock()}
        statistics = Statistics(server_context)

        server_context.nickname_to_client_mapping_entries["bot"] = MagicMock()

        del server_context.nickname_to_client_mapping_entries["christopher"]

        self.assertEqual(1, statistics.max_local_users())

    def test_max_global_user_count(self):
        server_context: ServerContext = ServerContext()
        server_context.nickname_to_client_mapping_entries = {"christopher": MagicMock()}
        statistics = Statistics(server_context)

        self.assertEqual(1, statistics.max_global_users())

    def test_current_local_user_count(self):
        server_context: ServerContext = ServerContext()
        server_context.nickname_to_client_mapping_entries = {"christopher": MagicMock()}
        statistics = Statistics(server_context)

        self.assertEqual(1, statistics.current_local_users())

    def test_current_global_user_count(self):
        server_context: ServerContext = ServerContext()
        server_context.nickname_to_client_mapping_entries = {"christopher": MagicMock()}
        statistics = Statistics(server_context)

        self.assertEqual(1, statistics.current_global_users())

    def test_current_online_operators(self):
        server_context: ServerContext = ServerContext()
        server_context.operator_entries = {"christopher": MagicMock()}
        statistics = Statistics(server_context)

        self.assertEqual(1, statistics.current_online_operators())

    def test_current_online_operators_with_secret_operators(self):
        server_context: ServerContext = ServerContext()
        server_context.operator_entries = {"christopher": MagicMock()}
        server_context.secret_client_entries = {MagicMock()}
        statistics = Statistics(server_context)

        self.assertEqual(0, statistics.current_online_operators())

    def test_current_online_operators_mismatched_calculation(self):
        server_context: ServerContext = ServerContext()
        server_context.operator_entries = {"christopher": MagicMock()}
        server_context.secret_client_entries = {MagicMock(), MagicMock()}
        statistics = Statistics(server_context)

        self.assertEqual(0, statistics.current_online_operators())

    def test_current_online_users(self):
        server_context: ServerContext = ServerContext()
        server_context.nickname_to_client_mapping_entries = {"christopher": MagicMock()}
        statistics = Statistics(server_context)

        self.assertEqual(1, statistics.current_online_users())

    def test_current_online_users_with_invisible_users(self):
        server_context: ServerContext = ServerContext()
        server_context.nickname_to_client_mapping_entries = {"christopher": MagicMock()}
        server_context.invisible_client_entries = {MagicMock()}
        statistics = Statistics(server_context)

        self.assertEqual(0, statistics.current_online_users())

    def test_current_online_users_mismatched_calculation(self):
        server_context: ServerContext = ServerContext()
        server_context.nickname_to_client_mapping_entries = {"christopher": MagicMock()}
        server_context.invisible_client_entries = {MagicMock(), MagicMock()}
        statistics = Statistics(server_context)

        self.assertEqual(0, statistics.current_online_users())

    def test_current_invisible_users(self):
        server_context: ServerContext = ServerContext()
        server_context.invisible_client_entries = {MagicMock(), MagicMock()}
        statistics = Statistics(server_context)

        self.assertEqual(2, statistics.current_invisible_users())

    def test_current_unknown_connections(self):
        server_context: ServerContext = ServerContext()
        server_context.unknown_connection_entries = {MagicMock(), MagicMock()}
        statistics = Statistics(server_context)

        self.assertEqual(2, statistics.current_unknown_connections())

    def test_current_channels(self):
        server_context: ServerContext = ServerContext()
        server_context.channel_entries = {"#somewhere": MagicMock()}
        statistics = Statistics(server_context)

        self.assertEqual(1, statistics.current_channels())
