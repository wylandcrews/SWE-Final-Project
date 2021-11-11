import os, requests
from requests.api import get
from dotenv import find_dotenv, load_dotenv
import random


def get_recommendation(lat, lng, place_type, radius):
    load_dotenv(find_dotenv())
    random_number = random.randint(0, 5)
    key = os.getenv("GOOGLE_KEY")
    base_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    endpoint = f"{base_url}?location={lat},{lng}&radius={radius}&type={place_type}&opennow&key={key}"
    r = requests.get(endpoint)
    recommendation = r.json()["results"][random_number]["geometry"]["location"]
    lat_recommendation = recommendation["lat"]
    lng_recommendation = recommendation["lng"]
    return lat_recommendation, lng_recommendation
