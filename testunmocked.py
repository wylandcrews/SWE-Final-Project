import unittest
import sys
import os

from geocoder import results
from geolocater import result


INPUT = "INPUT"
EXPECTED_OUTPUT = "EXPECTED_OUTPUT"


class Testresults(unittest.TestCase):
    def setUp(self):
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
        for test in self.success_test_params:
            self.assertEqual(results(test[INPUT]), test[EXPECTED_OUTPUT])


class Testresults2(unittest.TestCase):
    def setUp(self):
        self.success_test_params = [
            {
                INPUT: {},
                EXPECTED_OUTPUT: (None, None),
            },
            {
                INPUT: {"1 Hacker Way, Menlo Park, California"},
                EXPECTED_OUTPUT: ("37.4843369", "-122.1476151"),
            },
        ]

    def test_geolocater_data(self):
        for test in self.success_test_params:
            self.assertEqual(result(test[INPUT]), test[EXPECTED_OUTPUT])


if __name__ == "__main__":
    unittest.main()
