import unittest
import sys
import os
from unittest.mock import MagicMock, patch
from geocoder import geocode
from geolocater import geolocate
from weather import weatherAPI


class GetLongitutdeTest(unittest.TestCase):
    def test_get_longitude(self):
        with patch("geocoder.requests.get") as mock_requests_get:
            mock_response = MagicMock()

            mock_response.json.side_effect = [
                {
                    "results": [
                        {
                            "geometry": {
                                "location": {
                                    "lat": "52.02085876464844",
                                    "lng": "4.363800048828125",
                                }
                            }
                        }
                    ]
                }
            ]

            mock_requests_get.return_value = mock_response

            location2 = ("lat", "lng")

            self.assertEqual(
                geocode("location2"), ("52.02085876464844", "4.363800048828125")
            )


class GetlocaterTest(unittest.TestCase):
    def test_get_locater(self):
        with patch("geolocater.requests.get") as mock_requests_get:
            mock_response = MagicMock()

            mock_response.json.side_effect = [
                {
                    "results": [
                        {
                            "location": {
                                "lat": "52.02085876464844",
                                "lng": "4.363800048828125",
                            }
                        },
                    ]
                }
            ]

            mock_requests_get.return_value = mock_response

            location3 = ("lat", "lng")

            self.assertEqual(geolocate(), (None, None))


class GetWeatherTest(unittest.TestCase):
    def test_get_locater(self):
        with patch("weather.requests.get") as mock_requests_get:
            mock_response = MagicMock()

            mock_response.json.side_effect = [
                {
                    "results": [
                        {
                            "current": {
                                "condition": {
                                    "text": "The current weather in your area is: Partly cloudy",
                                }
                            },
                        }
                    ]
                }
            ]

            mock_requests_get.return_value = mock_response

            self.assertEqual(weatherAPI("0", "0"), (None, None))


if __name__ == "__main__":
    unittest.main()
