import os
import requests


def geocode(address):
    lat, lng = None, None
    key = os.getenv("GOOGLE_KEY")
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    endpoint = f"{base_url}?address={address}&key={key}"
    r = requests.get(endpoint)
    results = r.json()["results"][0]
    lat = results["geometry"]["location"]["lat"]
    lng = results["geometry"]["location"]["lng"]
    return lat, lng
