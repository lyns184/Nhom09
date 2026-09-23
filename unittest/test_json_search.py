import unittest
from recursive_json_search import *
from test_data import *


class json_search_test(unittest.TestCase):
    '''test module to test search function in recursive_json_search.py'''

    def test_search_found(self):
        '''key should be found, return list should not be empty'''
        self.assertTrue([] != json_search(key1, data, role="viewer"))

    def test_search_not_found(self):
        '''key should not be found, should return an empty list'''
        self.assertTrue([] == json_search(key2, data))

    def test_is_a_list(self):
        '''Should return a list'''
        self.assertIsInstance(json_search(key1, data, role="viewer"), list)

    def test_admin_can_read_api_key(self):
        '''admin should be allowed to read apiKey'''
        self.assertTrue([] != json_search("apiKey", data, role="admin"))

    def test_operator_cannot_read_api_key(self):
        '''operator should not be allowed to read apiKey'''
        self.assertEqual([], json_search("apiKey", data, role="operator"))

    def test_viewer_cannot_read_api_key(self):
        '''viewer should not be allowed to read apiKey'''
        self.assertEqual([], json_search("apiKey", data, role="viewer"))

    def test_operator_can_read_management_ip_address(self):
        '''operator should be allowed to read managementIpAddress'''
        self.assertTrue([] != json_search("managementIpAddress", data, role="operator"))

    def test_viewer_cannot_read_management_ip_address(self):
        '''viewer should not be allowed to read managementIpAddress'''
        self.assertEqual([], json_search("managementIpAddress", data, role="viewer"))

    def test_viewer_can_read_issue_summary(self):
        '''viewer should be allowed to read issueSummary'''
        self.assertTrue([] != json_search("issueSummary", data, role="viewer"))

    def test_missing_role_cannot_read_protected_field(self):
        '''missing role should not be allowed to read a protected field'''
        self.assertEqual([], json_search("apiKey", data))

    def test_unknown_role_cannot_read_protected_field(self):
        '''unknown role should not be allowed to read a protected field'''
        self.assertEqual([], json_search("apiKey", data, role="auditor"))


if __name__ == '__main__':
    unittest.main()
