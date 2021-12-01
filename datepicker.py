"""
Call Weather API to get weather for input date
"""
from logging import error
import os
import requests


def dateChooser(date, lat, lng):
    """
    Return the weather and weather icon for forecast date
    """
    location = str(lat) + "," + str(lng)
    key = os.getenv("WEATHER_API")
    base_url = "http://api.weatherapi.com/v1/forecast.json?"
    endpoint = f"{base_url}key={key}&q={location}&days=10&aqi=no&alerts=no"
    responsejson = requests.get(endpoint)
    results = responsejson.json()
    listcomp = []

    for i in range(10):
        try:
            listcomp.append(results["forecast"]["forecastday"][i]["date"])
            listcomp.append(
                results["forecast"]["forecastday"][i]["day"]["condition"]["text"]
            )
            listcomp.append(
                results["forecast"]["forecastday"][i]["day"]["condition"]["icon"]
            )
        except Exception:
            pass

    index = listcomp.index(date)
    currentWeather = listcomp[index + 1]
    currentWeatherIcon = listcomp[index + 2]
    currentWeatherIcon = (results["current"]["condition"]["icon"]).replace("//", "")
    return currentWeather, "https://" + currentWeatherIcon
