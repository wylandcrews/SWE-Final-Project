"""
Obtain the current weather at a specific latitude and longitude
"""
import os
import requests


def weatherAPI(lat, lng):
    """
    Call the Weather API to retrieve current weather and a respective icon
    """
    location = str(lat) + "," + str(lng)
    key = os.getenv("WEATHER_API")
    base_url = "http://api.weatherapi.com/v1/current.json?"
    endpoint = f"{base_url}key={key}&q={location}&aqi=no"
    responsejson = requests.get(endpoint)
    results = responsejson.json()
    currentWeather = results["current"]["condition"]["text"]
    currentWeatherIcon = (results["current"]["condition"]["icon"]).replace("//", "")
    return currentWeather, "https://" + currentWeatherIcon
