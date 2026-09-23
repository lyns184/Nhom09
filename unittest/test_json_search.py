import unittest

from recursive_json_search import json_search
from test_data import data, key1, key2


class json_search_test(unittest.TestCase):
    """Test recursive search and role-based access control."""

    def test_search_found(self):
        """An authorized search for an existing key should return results."""
        result = json_search(key1, data, role="viewer")
        self.assertNotEqual([], result)

    def test_search_not_found(self):
        """A nonexistent key should return an empty list."""
        result = json_search(key2, data, role="viewer")
        self.assertEqual([], result)

    def test_is_a_list(self):
        """The function should always return a list."""
        result = json_search(key1, data, role="viewer")
        self.assertIsInstance(result, list)

    def test_admin_can_read_api_key(self):
        """An admin should be allowed to read apiKey."""
        result = json_search("apiKey", data, role="admin")
        self.assertEqual(
            [{"apiKey": "SNMP-COMMUNITY-STRING-7f3a9c"}],
            result,
        )

    def test_operator_cannot_read_api_key(self):
        """An operator must not be allowed to read apiKey."""
        result = json_search("apiKey", data, role="operator")
        self.assertEqual([], result)

    def test_viewer_cannot_read_api_key(self):
        """A viewer must not be allowed to read apiKey."""
        result = json_search("apiKey", data, role="viewer")
        self.assertEqual([], result)

    def test_operator_can_read_management_ip(self):
        """An operator should be allowed to read managementIpAddress."""
        result = json_search(
            "managementIpAddress",
            data,
            role="operator",
        )
        self.assertEqual(
            [{"managementIpAddress": "10.10.20.21"}],
            result,
        )

    def test_viewer_cannot_read_management_ip(self):
        """A viewer must not be allowed to read managementIpAddress."""
        result = json_search(
            "managementIpAddress",
            data,
            role="viewer",
        )
        self.assertEqual([], result)

    def test_missing_role_cannot_read_protected_field(self):
        """A missing role must not be allowed to read a protected field."""
        result = json_search("apiKey", data)
        self.assertEqual([], result)

    def test_unknown_role_cannot_read_protected_field(self):
        """An unknown role must not read a protected field."""
        result = json_search("apiKey", data, role="guest")
        self.assertEqual([], result)


if __name__ == "__main__":
    unittest.main()