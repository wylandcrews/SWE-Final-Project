import unittest
import sys
import os
from unittest.mock import MagicMock, patch
from geocoder import geocode
from geolocater import geolocate
from weather import weatherAPI
from recommendation import get_url


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
    def test_get_weather(self):
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


class GeturlTest(unittest.TestCase):
    def test_get_url(self):
        with patch("recommendation.requests.get") as mock_requests_get:
            mock_response = MagicMock()

            mock_response.json.side_effect = [
                {
                    "result": [
                        {
                            "url": "https://www.google.com/maps/dir/33.7528125,-84.3924299/1+Hacker+Way,+Menlo+Park,+CA+94025/@33.524186,-121.3685211,4z/data=!3m1!4b1!4m9!4m8!1m1!4e1!1m5!1m1!1s0x808fbb7219a03223:0xac647fa2410be2a4!2m2!1d-122.148053!2d37.4843511",
                        }
                    ]
                }
            ]

            mock_requests_get.return_value = mock_response

            self.assertEqual(
                get_url("ChIJtYuu0V25j4ARwu5e4wwRYgE"),
                (
                    "https://www.google.com/maps/dir/33.7528125,-84.3924299/1+Hacker+Way,+Menlo+Park,+CA+94025/@33.524186,-121.3685211,4z/data=!3m1!4b1!4m9!4m8!1m1!4e1!1m5!1m1!1s0x808fbb7219a03223:0xac647fa2410be2a4!2m2!1d-122.148053!2d37.4843511"
                ),
            )


if __name__ == "__main__":
    unittest.main()
