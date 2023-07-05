import logging
import unittest
from unittest.mock import MagicMock

from pyRCX.statistics import Statistics


class TestStatistics(unittest.TestCase):

    def setUp(self):
        logging.disable(logging.WARNING)

    def test_max_local_user_count(self):
        nickname_to_client_mapping_entries = {"christopher": MagicMock()}
        statistics = Statistics(nickname_to_client_mapping_entries, MagicMock(), MagicMock(), MagicMock(),
                                MagicMock())

        nickname_to_client_mapping_entries["bot"] = MagicMock()

        del nickname_to_client_mapping_entries["christopher"]

        self.assertEqual(1, statistics.max_local_users())

    def test_max_global_user_count(self):
        nickname_to_client_mapping_entries = {"christopher": MagicMock()}
        statistics = Statistics(nickname_to_client_mapping_entries, MagicMock(), MagicMock(), MagicMock(),
                                MagicMock())

        self.assertEqual(1, statistics.max_global_users())

    def test_current_local_user_count(self):
        nickname_to_client_mapping_entries = {"christopher": MagicMock()}
        statistics = Statistics(nickname_to_client_mapping_entries, MagicMock(), MagicMock(), MagicMock(),
                                MagicMock())

        self.assertEqual(1, statistics.current_local_users())

    def test_current_global_user_count(self):
        nickname_to_client_mapping_entries = {"christopher": MagicMock()}
        statistics = Statistics(nickname_to_client_mapping_entries, MagicMock(), MagicMock(), MagicMock(),
                                MagicMock())

        self.assertEqual(1, statistics.current_global_users())

    def test_current_online_operators(self):
        operator_entries = {"christopher": MagicMock()}
        statistics = Statistics(MagicMock(), operator_entries, MagicMock(), set(), MagicMock())

        self.assertEqual(1, statistics.current_online_operators())

    def test_current_online_operators_with_secret_operators(self):
        operator_entries = {"christopher": MagicMock()}
        secret_client_entries = {MagicMock()}
        statistics = Statistics(MagicMock(), operator_entries, MagicMock(), secret_client_entries,
                                MagicMock())

        self.assertEqual(0, statistics.current_online_operators())

    def test_current_online_operators_mismatched_calculation(self):
        operator_entries = {"christopher": MagicMock()}
        secret_client_entries = {MagicMock(), MagicMock()}
        statistics = Statistics(MagicMock(), operator_entries, MagicMock(), secret_client_entries,
                                MagicMock())

        self.assertEqual(0, statistics.current_online_operators())

    def test_current_online_users(self):
        nickname_to_client_mapping_entries = {"christopher": MagicMock()}
        statistics = Statistics(nickname_to_client_mapping_entries, MagicMock(), set(), MagicMock(),
                                MagicMock())

        self.assertEqual(1, statistics.current_online_users())

    def test_current_online_users_with_invisible_users(self):
        nickname_to_client_mapping_entries = {"christopher": MagicMock()}
        invisible_entries = {MagicMock()}
        statistics = Statistics(nickname_to_client_mapping_entries, MagicMock(), invisible_entries, MagicMock(),
                                MagicMock())

        self.assertEqual(0, statistics.current_online_users())

    def test_current_online_users_mismatched_calculation(self):
        nickname_to_client_mapping_entries = {"christopher": MagicMock()}
        invisible_entries = {MagicMock(), MagicMock()}
        statistics = Statistics(nickname_to_client_mapping_entries, MagicMock(), invisible_entries, MagicMock(),
                                MagicMock())

        self.assertEqual(0, statistics.current_online_users())

    def test_current_invisible_users(self):
        invisible_entries = {MagicMock(), MagicMock()}
        statistics = Statistics(MagicMock(), MagicMock(), invisible_entries, MagicMock(), MagicMock())

        self.assertEqual(2, statistics.current_invisible_users())

    def test_current_unknown_connections(self):
        unknown_connection_entries = {MagicMock(), MagicMock()}
        statistics = Statistics(MagicMock(), MagicMock(), MagicMock(), MagicMock(), unknown_connection_entries)

        self.assertEqual(2, statistics.current_unknown_connections())
