import os
from flask import Flask, request, render_template, redirect, url_for, session
from flask_session import Session
from geocoder import geocode
from geolocater import geolocate
from weather import weatherAPI
from recommendation import get_recommendation
from dotenv import load_dotenv, find_dotenv

# from flask_sqlalchemy import SQLAlchemy

load_dotenv(find_dotenv())

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_KEY")
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

# Block below commented out for use once DB is set up
# Update DB URL as seen in Milestone 3
# db_url = os.getenv("DATABASE_URL")
# if db_url.startswith("postgres://"):
#    db_url = db_url.replace("postgres://", "postgresql://", 1)
# app.config["SQLALCHEMY_DATABASE_URI"] = db_url
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

Session(app)

# db = SQLAlchemy(app)


@app.route("/")
def index():
    currentWeather = session.get("currentWeather", None)
    weatherImage = session.get("weatherImage", None)
    lat_recommendation = session.get("lat_recommendation", None)
    lng_recommendation = session.get("lng_recommendation", None)
    rating = session.get("rating", None)
    place_name = session.get("place_name", None)
    place_url = session.get("place_url", None)

    if (
        currentWeather != None
        and weatherImage != None
        and lat_recommendation != None
        and lng_recommendation != None
        and rating != None
        and place_name != None
        and place_url != None
    ):
        return render_template(
            "index.html",
            currentWeather=currentWeather,
            weatherImage=weatherImage,
            lat_recommendation=lat_recommendation,
            lng_recommendation=lng_recommendation,
            rating=rating,
            place_name=place_name,
            place_url=place_url,
        )

    return render_template("index.html")


@app.route("/geocoder", methods=["POST"])
def geocoder():
    address = request.form["place"]
    lat, lng = geocode(address)
    weatherResults = weatherAPI(lat, lng)
    currentWeather = weatherResults[0]
    weatherImage = weatherResults[1]
    session["currentWeather"] = currentWeather
    session["weatherImage"] = weatherImage
    # place_type and radius are hardcoded for now
    place_type = "restaurant"
    radius = 5000
    try:
        payload = get_recommendation(
            lat=lat, lng=lng, place_type=place_type, radius=radius
        )
        session["lat_recommendation"] = payload.get("lat_recommendation")
        session["lng_recommendation"] = payload.get("lng_recommendation")
        session["rating"] = payload.get("rating")
        session["place_name"] = payload.get("place_name")
        session["place_url"] = payload.get("url")
        return redirect(url_for("index"))
    except:
        return render_template("error.html")


@app.route("/locater", methods=["POST"])
def locater():
    lat, lng = geolocate()
    weatherResults = weatherAPI(lat, lng)
    currentWeather = weatherResults[0]
    weatherImage = weatherResults[1]
    session["currentWeather"] = currentWeather
    session["weatherImage"] = weatherImage
    # place_type and radius are hardcoded for now
    place_type = "restaurant"
    radius = 5000
    try:
        payload = get_recommendation(
            lat=lat, lng=lng, place_type=place_type, radius=radius
        )
        session["lat_recommendation"] = payload.get("lat_recommendation")
        session["lng_recommendation"] = payload.get("lng_recommendation")
        session["rating"] = payload.get("rating")
        session["place_name"] = payload.get("place_name")
        session["place_url"] = payload.get("url")
        return redirect(url_for("index"))
    except:
        return render_template("error.html")


@app.route("/error", methods=["POST"])
def retry():
    return redirect(url_for("index"))


app.run(host=os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT", 8080)), debug=True)
