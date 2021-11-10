import os
from flask import Flask, request, render_template, redirect, url_for, session
from flask_session import Session
from geocoder import geocode
from geolocater import geolocate
from weather import weatherAPI
from dotenv import load_dotenv, find_dotenv
#from flask_sqlalchemy import SQLAlchemy

load_dotenv(find_dotenv())

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_KEY")
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

# Block below commented out for use once DB is set up
# Update DB URL as seen in Milestone 3
#db_url = os.getenv("DATABASE_URL")
#if db_url.startswith("postgres://"):
#    db_url = db_url.replace("postgres://", "postgresql://", 1)
#app.config["SQLALCHEMY_DATABASE_URI"] = db_url
#app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

Session(app)

#db = SQLAlchemy(app)


@app.route("/")
def index():
    currentWeather = session.get("currentWeather", None)
    weatherImage = session.get("weatherImage", None)

    if currentWeather != None and weatherImage != None:
        return render_template(
            "index.html",
            currentWeather=currentWeather,
            weatherImage=weatherImage,
        )

    return render_template("index.html")


@app.route("/geocoder", methods=["POST"])
def geocoder():
    address = request.form["place"]
    lat, lng = geocode(address)
    print(lat)
    print(lng)
    weatherResults = weatherAPI(lat, lng)
    currentWeather = weatherResults[0]
    weatherImage = weatherResults[1]
    session["currentWeather"] = currentWeather
    session["weatherImage"] = weatherImage
    return redirect(url_for("index"))


@app.route("/locater", methods=["POST"])
def locater():
    lat, lng = geolocate()
    print(lat)
    print(lng)
    weatherResults = weatherAPI(lat, lng)
    currentWeather = weatherResults[0]
    weatherImage = weatherResults[1]
    session["currentWeather"] = currentWeather
    session["weatherImage"] = weatherImage
    return redirect(url_for("index"))


app.run(host=os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT", 8080)), debug=True)
