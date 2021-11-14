import os
import requests


def geolocate():
    lat, lng = None, None
    key = os.getenv("GOOGLE_KEY")
    base_url = "https://www.googleapis.com/geolocation/v1/geolocate"
    endpoint = f"{base_url}?key={key}"
    r = requests.post(endpoint)
    results = r.json()["location"]
    lat = results["lat"]
    lng = results["lng"]
    return lat, lng
