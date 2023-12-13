#!/usr/bin/env python

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest import mock

import securitylist
import json
import datetime

# This method will be used by the mock to replace requests.get
def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, status_code):
            self.status_code = status_code

            with open('src/tests/nvd.json') as fh:
                self.json_data = json.load(fh)

        def json(self):
            return self.json_data

        def raise_for_status(self):
            pass

    if args[0] == 'https://services.nvd.nist.gov/rest/json/cve/2.0/CVE-1000-0001':
        return MockResponse(200)
    elif args[0] == 'https://services.nvd.nist.gov/rest/json/cve/2.0/CVE-1000-0002':
        return MockResponse(200)

    return MockResponse(404)

class TestNVD(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_date(self, mock_get):

        timestamp = datetime.datetime.now()

        nvd = securitylist.NVD()
        nvd.get_range(None, None)

        self.assertEqual(nvd.total, 40)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_iterate(self, mock_get):

        timestamp = datetime.datetime.now()

        nvd = securitylist.NVD()
        nvd.get_range(None, None)

        self.assertEqual(nvd.total, 40)

        count = 0
        for i in nvd:
            count = count + 1

        self.assertEqual(count, 40)
