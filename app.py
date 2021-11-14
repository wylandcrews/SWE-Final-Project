"""
Flask server file for this project
"""
import os
from dotenv import load_dotenv, find_dotenv
from flask import Flask, request, render_template, redirect, url_for, session
from flask_session import Session
from geocoder import geocode
from geolocater import geolocate
from weather import weatherAPI
from recommendation import get_recommendation

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
    """
    Defines the function for the index page.
    """
    currentWeather = session.get("currentWeather", None)
    weatherImage = session.get("weatherImage", None)
    rating = session.get("rating", None)
    place_name = session.get("place_name", None)
    place_url = session.get("place_url", None)
    photo = session.get("photo", None)
    place_id = session.get("place_id", None)

    if (
        currentWeather is not None
        and weatherImage is not None
        and rating is not None
        and place_name is not None
        and place_url is not None
        and place_id is not None
    ):
        return render_template(
            "index.html",
            currentWeather=currentWeather,
            weatherImage=weatherImage,
            rating=rating,
            place_name=place_name,
            place_url=place_url,
            photo=photo,
            place_id=place_id,
        )

    return render_template("index.html")


@app.route("/geocoder", methods=["POST"])
def geocoder():
    """
    Call geocode from geocoder.py if a user enters an address.
    """
    try:
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
        payload = get_recommendation(
            lat=lat, lng=lng, place_type=place_type, radius=radius
        )
        session["rating"] = payload.get("rating")
        session["place_name"] = payload.get("place_name")
        session["place_url"] = payload.get("url")
        session["photo"] = payload.get("photo")
        session["place_id"] = payload.get("place_id")
        return redirect(url_for("index"))
    except Exception:
        return render_template("error.html")


@app.route("/locater", methods=["POST"])
def locater():
    """
    Call geolocate from geolocater.py if user chooses current location.
    """
    try:
        lat, lng = geolocate()
        weatherResults = weatherAPI(lat, lng)
        currentWeather = weatherResults[0]
        weatherImage = weatherResults[1]
        session["currentWeather"] = currentWeather
        session["weatherImage"] = weatherImage
        # place_type and radius are hardcoded for now
        place_type = "restaurant"
        radius = 5000
        payload = get_recommendation(
            lat=lat, lng=lng, place_type=place_type, radius=radius
        )
        session["rating"] = payload.get("rating")
        session["place_name"] = payload.get("place_name")
        session["place_url"] = payload.get("url")
        session["photo"] = payload.get("photo")
        session["place_id"] = payload.get("place_id")
        return redirect(url_for("index"))
    except Exception:
        return render_template("error.html")


@app.route("/error", methods=["POST"])
def retry():
    """
    Render error.html if any exceptions occur.
    User will click a button that attempts to render index.html.
    """
    return redirect(url_for("index"))


app.run(host=os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT", 8080)), debug=True)
