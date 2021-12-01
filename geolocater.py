"""
Call Google Geolocation API to obtain user's current location
"""
import os
import requests


def geolocate():
    """
    Return the latitude and longitude of the user's current location
    """
    lat, lng = None, None
    key = os.getenv("GOOGLE_KEY")
    base_url = "https://www.googleapis.com/geolocation/v1/geolocate"
    endpoint = f"{base_url}?key={key}"
    r = requests.post(endpoint)

    try:
        results = r.json()["location"]
        lat = results["lat"]
        lng = results["lng"]
        return lat, lng
    except KeyError:
        return None, None
