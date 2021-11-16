"""
Favorite Place Module
"""
import os
import requests
from dotenv import find_dotenv, load_dotenv
from recommendation import get_url


def favorite_details(place_id):
    """
    Get name, Maps URL, photo, and rating of user's favorite place
    """
    load_dotenv(find_dotenv())
    details = {}
    key = os.getenv("GOOGLE_KEY")
    details["url"] = get_url(place_id=place_id)
    base_url = "https://maps.googleapis.com/maps/api/place/details/json"
    endpoint = f"{base_url}?place_id={place_id}&key={key}"
    r = requests.get(endpoint)
    results = r.json()["result"]
    details["name"] = results["name"]
    details["rating"] = results["rating"]
    photo_ref = results["photos"][0]["photo_reference"]
    details["photo"] = favorite_photo(photo_ref=photo_ref)
    return details


def favorite_photo(photo_ref):
    """
    Get photo of user's favorite place
    """
    key = os.getenv("GOOGLE_KEY")
    endpoint = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photo_reference={photo_ref}&key={key}"
    r = requests.get(endpoint)
    if r.status_code != 200:
        return None
    else:
        f = open("static/favoriteImage.jpg", "wb")
        for chunk in r:
            if chunk:
                f.write(chunk)
        f.close()
        return "static/favoriteImage.jpg"
