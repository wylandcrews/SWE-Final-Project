import os
from flask import Flask, request, render_template, redirect, url_for, session
from flask_session import Session
from geocoder import geocode
from geolocater import geolocate
from weather import weatherAPI


app = Flask(__name__)
app.secret_key = os.getenv("FLASK_KEY")
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)


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
