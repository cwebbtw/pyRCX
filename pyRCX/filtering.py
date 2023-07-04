from typing import List

import sys


class FilterEntry:
    """
    Represents a filter entry parsed from configuration
    """

    # TODO correct the typing as it is currently all string based
    def __init__(self, filter_type: str, filter_string: str, override_level: str):
        self.filter_type = filter_type
        self.filter_string = filter_string
        self.override = override_level


class Filtering:

    """
    Represents a filtering capability but currently the main server violates encapsulation
    as not all callers use the filter method but instead access the underlying list
    """

    def __init__(self, initial_filters: List[FilterEntry] = []):
        self._filters = initial_filters

    def add_filter(self, filter_entry: FilterEntry):
        self._filters.append(filter_entry)

    def clear_filters(self):
        self._filters.clear()

    def filter(self, text: str, filter_type: str, override_level: int):
        """
        Returns true if the text matches a given filter entry for a specific filter type but
        will not match if the override level is greater than or equal to the filter entry level
        """

        for each in self._filters:
            if override_level != 0 and override_level >= int(each.override or 0):
                return False

            if each.filter_string.lower() in text.lower() and filter_type == each.filter_type:
                return True

        return False
