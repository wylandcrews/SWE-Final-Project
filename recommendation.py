import os
import random
import requests
from dotenv import find_dotenv, load_dotenv


def get_recommendation(lat, lng, place_type, radius):
    load_dotenv(find_dotenv())
    payload = {}
    key = os.getenv("GOOGLE_KEY")
    base_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    endpoint = f"{base_url}?location={lat},{lng}&radius={radius}&type={place_type}&opennow&key={key}"
    r = requests.get(endpoint)
    random_number = random.randint(0, 5)
    recommendation = r.json()["results"][random_number]
    payload["rating"] = recommendation["rating"]
    payload["place_name"] = recommendation["name"]
    place_id = recommendation["place_id"]
    payload["place_id"] = place_id
    payload["url"] = get_url(place_id)
    photo_reference = recommendation["photos"][0]["photo_reference"]
    payload["photo"] = get_photo(photo_reference=photo_reference)
    return payload


def get_url(place_id):
    key = os.getenv("GOOGLE_KEY")
    base_url = "https://maps.googleapis.com/maps/api/place/details/json"
    endpoint = f"{base_url}?place_id={place_id}&fields=url&key={key}"
    r = requests.get(endpoint)
    url = r.json()["result"]["url"]
    return url


def get_photo(photo_reference):
    key = os.getenv("GOOGLE_KEY")
    endpoint = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photo_reference={photo_reference}&key={key}"
    r = requests.get(endpoint)
    if r.status_code != 200:
        return None
    else:
        f = open("static/placeImage.jpg", "wb")
        for chunk in r:
            if chunk:
                f.write(chunk)
        f.close()
        return "static/placeImage.jpg"
