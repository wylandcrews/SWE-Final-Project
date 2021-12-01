"""
Unmocked Unit Tests
"""
import unittest
import sys
import os

from geocoder import results
from recommendation import get_recommendation, get_url, get_photo
from weather import weatherAPI
from geolocater import geolocate


INPUT = "INPUT"
EXPECTED_OUTPUT = "EXPECTED_OUTPUT"


class Testresults(unittest.TestCase):
    """
    Test class
    """

    def setUp(self):
        """
        Test Constructor
        """
        self.success_test_params = [
            {
                INPUT: {},
                EXPECTED_OUTPUT: (None, None),
            },
            {
                INPUT: {"r": "<Response [200]>"},
                EXPECTED_OUTPUT: (None, None),
            },
        ]

    def test_geocoder_data(self):
        """
        Test geocoder method
        """
        for test in self.success_test_params:
            self.assertEqual(results(test[INPUT]), test[EXPECTED_OUTPUT])


if __name__ == "__main__":
    unittest.main()
