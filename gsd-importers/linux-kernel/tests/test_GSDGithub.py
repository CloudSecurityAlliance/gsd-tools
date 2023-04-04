import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import Mock, patch

import GSD

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

class TestGSDRepo(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @patch('GSD.GSDGithub.requests.get', side_effect=mocked_requests_get)
    def testGetNewIssues(self, mock_get):
        issues = GSD.get_new_issues('http://example.com')
        self.assertEqual(len(issues), 0)

    @patch('GSD.GSDGithub.requests.get', side_effect=mocked_requests_get)
    def testGetApprovedCan(self, mock_get):
        issues = GSD.get_approved_can_issues('http://example.com')
        self.assertEqual(len(issues), 0)
