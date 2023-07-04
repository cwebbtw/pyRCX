import unittest

from pyRCX.filtering import *


class FilteringTest(unittest.TestCase):
    """
    Filtering looks after the behaviours of what is allowed and what is not for
    a given type of entity
    """

    def test_filter_entry_is_matched(self):
        filtering = Filtering()
        filtering.add_filter(FilterEntry("type1", "sysop", 0))

        self.assertTrue(filtering.filter("sysop", "type1", 0))
        self.assertFalse(filtering.filter("christopher", "type1", 0))

    def test_filter_entry_can_be_overriden(self):
        filtering = Filtering()
        filtering.add_filter(FilterEntry("type1", "sysop", 2))

        self.assertTrue(filtering.filter("sysop", "type1", 0))
        self.assertTrue(filtering.filter("sysop", "type1", 1))
        self.assertFalse(filtering.filter("sysop", "type1", 2))
        self.assertFalse(filtering.filter("sysop", "type1", 3))
