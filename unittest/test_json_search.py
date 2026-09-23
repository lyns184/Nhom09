# Fill the Python code in this file
import unittest

from recursive_json_search import json_search
from test_data import data, key1, key2


class json_search_test(unittest.TestCase):
    """Test the json_search function in recursive_json_search.py."""

    def test_search_found(self):
        """An existing key should return a non-empty list."""
        result = json_search(key1, data)
        self.assertNotEqual([], result)

    def test_search_not_found(self):
        """A nonexistent key should return an empty list."""
        result = json_search(key2, data)
        self.assertEqual([], result)

    def test_is_a_list(self):
        """The function should return a list."""
        result = json_search(key1, data)
        self.assertIsInstance(result, list)


if __name__ == "__main__":
    unittest.main()