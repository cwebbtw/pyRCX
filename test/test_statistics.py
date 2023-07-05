import unittest

from pyRCX.statistics import Statistics

from unittest.mock import MagicMock


class TestStatistics(unittest.TestCase):

    def test_max_local_user_count(self):
        nickname_to_client_mapping_entries = {"christopher": MagicMock()}
        statistics = Statistics(nickname_to_client_mapping_entries)

        nickname_to_client_mapping_entries["bot"] = MagicMock()

        del nickname_to_client_mapping_entries["christopher"]

        self.assertEqual(1, statistics.max_local_users())

    def test_max_global_user_count(self):
        nickname_to_client_mapping_entries = {"christopher": MagicMock()}
        statistics = Statistics(nickname_to_client_mapping_entries)

        self.assertEqual(1, statistics.max_global_users())

    def test_current_local_user_count(self):
        nickname_to_client_mapping_entries = {"christopher": MagicMock()}
        statistics = Statistics(nickname_to_client_mapping_entries)

        self.assertEqual(1, statistics.current_local_users())

    def test_current_global_user_count(self):
        nickname_to_client_mapping_entries = {"christopher": MagicMock()}
        statistics = Statistics(nickname_to_client_mapping_entries)

        self.assertEqual(1, statistics.current_global_users())
