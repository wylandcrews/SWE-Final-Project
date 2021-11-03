import os
from flask import Flask, request, render_template, redirect, url_for
from geocoder import geocode

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_KEY")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/geocoder", methods=["POST"])
def geocoder():
    address = request.form['place']
    lat, lng = geocode(address)
    print(lat)
    print(lng)
    return redirect(url_for("index"))

app.run(
    host=os.getenv('IP', '0.0.0.0'),
    port=int(os.getenv('PORT', 8080)),
    debug=True
)