"""
Call Google Geocoding API to turn address into lat/long
"""
import os
import requests


def geocode(address):
    """
    Return that latitude and longitude of the address the user entered
    """
    lat, lng = None, None
    key = os.getenv("GOOGLE_KEY")
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    endpoint = f"{base_url}?address={address}&key={key}"
    r = requests.get(endpoint)
    print(r)
    return results(r)


def results(r):
    try:
        results = r.json()["results"][0]
        lat = results["geometry"]["location"]["lat"]
        lng = results["geometry"]["location"]["lng"]
        return lat, lng
    except AttributeError:
        return None, None
