import os, requests
from requests.api import get
from dotenv import find_dotenv, load_dotenv
import random


def get_recommendation(lat, lng, place_type, radius):
    load_dotenv(find_dotenv())
    payload = {}
    random_number = random.randint(0, 5)
    key = os.getenv("GOOGLE_KEY")
    base_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    endpoint = f"{base_url}?location={lat},{lng}&radius={radius}&type={place_type}&opennow&key={key}"
    r = requests.get(endpoint)
    recommendation = r.json()["results"][random_number]
    payload["lat_recommendation"] = recommendation["geometry"]["location"]["lat"]
    payload["lng_recommendation"] = recommendation["geometry"]["location"]["lng"]
    payload["rating"] = recommendation["rating"]
    payload["place_name"] = recommendation["name"]
    place_id = recommendation["place_id"]
    payload["url"] = get_url(place_id)
    return payload

def get_url(place_id):
    key = os.getenv("GOOGLE_KEY")
    base_url = "https://maps.googleapis.com/maps/api/place/details/json"
    endpoint = f"{base_url}?place_id={place_id}&fields=url&key={key}"
    r = requests.get(endpoint)
    url = r.json()["result"]["url"]
    return url