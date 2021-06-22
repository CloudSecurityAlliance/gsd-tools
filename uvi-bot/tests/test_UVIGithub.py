import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import Mock, patch

import UVI

class FakeResponse:

    def __init__(self):
        pass

    def raise_for_status(self):
        pass

    def json(self):
        return []

# This method will be used by the mock to replace requests.get
def mocked_requests_get(*args, **kwargs):
    # Same as above
    return FakeResponse()

class TestUVIRepo(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @patch('UVI.UVIGithub.requests.get', side_effect=mocked_requests_get)
    def testGetNewIssues(self, mock_get):
        issues = UVI.get_new_issues('http://example.com')
        self.assertEqual(len(issues), 0)

    @patch('UVI.UVIGithub.requests.get', side_effect=mocked_requests_get)
    def testGetApprovedCan(self, mock_get):
        issues = UVI.get_approved_can_issues('http://example.com')
        self.assertEqual(len(issues), 0)
