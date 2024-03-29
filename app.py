"""
Flask server file for this project
"""
import os
from datetime import date
import flask
from flask import Flask, request, render_template, redirect, url_for, session
from dotenv import load_dotenv, find_dotenv
from flask_oauthlib.client import OAuth
from flask_login import (
    LoginManager,
    login_required,
    current_user,
    login_user,
    logout_user,
    UserMixin,
)
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd
from flask_session import Session
from favorite_place import favorite_details
from geocoder import geocode
from geolocater import geolocate
from weather import weatherAPI
from recommendation import get_recommendation
from auth import OAuthLogin
from datepicker import dateChooser

load_dotenv(find_dotenv())

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_KEY")
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

login_manager = LoginManager()
login_manager.init_app(app)

oauth_client = OAuthLogin(OAuth(app), app)

# Block below commented out for use once DB is set up
# Update DB URL as seen in Milestone 3
db_url = os.getenv("DATABASE_URL")
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


Session(app)

db = SQLAlchemy(app)


class userCredentials(UserMixin, db.Model):
    """
    userCredentials class contains fields for a user's username, email, and password.
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150))
    email = db.Column(db.String(200))
    password = db.Column(db.String(250))
    userProfilePicture = db.Column(db.String(250))

    def __repr__(self):
        """
        Return self
        """
        return f"<userCredentials {self.username}>"

    def get_username(self):
        """
        Return username
        """
        return self.username

    def set_password(self, password):
        """
        Return password
        """
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """
        Check input password against database password for validation
        """
        return check_password_hash(self.password, password)


class savedSearches(db.Model):
    """
    Saved searches database that will store saved place_id's separated by commas.
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False)
    savedplaces = db.Column(db.String(1000), nullable=False)

    def __repr__(self):
        return f"<savedSearches {self.username}>"


db.create_all()


@login_manager.user_loader
def load_user(user_name):
    """
    User loader method
    """
    return userCredentials.query.get(user_name)


@app.route("/register", methods=["GET", "POST"])
def register():
    """
    Register method that will be used for email/password login
    """
    users = userCredentials.query.all()
    userList = []
    for user in users:
        userList.append(user.username)

    if flask.request.method == "POST":
        username = flask.request.form.get("username")
        email = flask.request.form.get("email")
        password = flask.request.form.get("password")
        confirmPassword = flask.request.form.get("confirmPassword")
        userProfileImage = flask.request.form["inlineRadioOptions"]

        if password != confirmPassword:
            flask.flash("The passwords do not match.")

        elif username in userList:
            flask.flash("This username already exists, please input another username.")

        elif userProfileImage == "":
            flask.flash("Please select a profile image.")

        else:
            newUser = userCredentials(
                username=username, email=email, userProfilePicture=userProfileImage
            )
            newUser.set_password(password)
            db.session.add(newUser)
            db.session.commit()
            return flask.redirect(flask.url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Login method using email and password
    """
    users = userCredentials.query.all()
    emailList = []
    for user in users:
        emailList.append(user.email)

    if flask.request.method == "POST":
        email = flask.request.form.get("email")
        if email not in emailList:
            flask.flash("Email not found. Please register.")
            return render_template("login.html")
        password = flask.request.form.get("password")
        current = userCredentials.query.filter_by(email=email).first()
        passwordCheck = current.check_password(password)

        if passwordCheck is False:
            flask.flash("This email or password combination is incorrect.")

        else:
            login_user(current)
            return flask.redirect(flask.url_for("index"))

    return render_template("login.html")


@app.route("/login/callback/google")
def google_callback():
    """
    Google Login Callback
    """
    user_data = oauth_client.google_callback(request)
    user = userCredentials.query.filter_by(username=user_data).first()
    if user:
        pass
    else:
        user = userCredentials(username=user_data)
        db.session.add(user)
        db.session.commit()
    pass


@app.route("/login/callback/facebook")
def facebook_callback():
    """
    Facebook Login Callback
    """
    user_data = oauth_client.meta_callback(request)
    user = userCredentials.query.filter_by(username=user_data).first()
    if user:
        pass
    else:
        user = userCredentials(username=user_data)
        db.session.add(user)
        db.session.commit()
    pass


@app.route("/sso/google")
def login_google():
    """
    Use library to construct the request for Google login and provide
    scopes that let you retrieve user's profile from Google

    don't need redirect here because the function call returns a redirect
    """
    return oauth_client.google_auth()


@app.route("/sso/facebook")
def login_facebook():
    """
    Use library to construct the request for Facebook login and
    provide scopes that let you retrieve the user's profile from FB
    """

    return oauth_client.meta_auth(request)


@app.route("/")
def landing():
    """
    Render the landing page.
    """
    return render_template("landing.html")


@app.route("/index")
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

    if currentWeather is not None and weatherImage is not None:
        if (
            rating is not None
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
        else:
            return render_template(
                "index.html",
                currentWeather=currentWeather,
                weatherImage=weatherImage,
            )
    return render_template("index.html")


@app.route("/geocoder", methods=["POST"])
def geocoder():
    """
    Call geocode from geocoder.py if a user enters an address.
    """
    try:
        address = request.form["place"]
        dateInput = request.form["datePicker"]

        today = date.today().isoformat()
        dates = pd.date_range(today, periods=3, freq="D")
        next3Days = []
        for day in dates:
            next3Days.append(str(day)[0:10])
        next3Days.pop(0)

        lat, lng = geocode(address)
        session["lat"] = lat
        session["lng"] = lng

        if dateInput == today:
            weatherResults = weatherAPI(lat, lng)
            currentWeather = weatherResults[0]
            weatherImage = weatherResults[1]
            session["currentWeather"] = currentWeather
            session["weatherImage"] = weatherImage

        elif str(dateInput) in next3Days:
            weatherResults = dateChooser(dateInput, lat, lng)
            currentWeather = weatherResults[0]
            weatherImage = weatherResults[1]
            session["currentWeather"] = currentWeather
            session["weatherImage"] = weatherImage

        if "rain" in currentWeather:
            flask.flash(
                "The weather outside doesn't look so great, let's explore some indoor activites!"
            )
        else:
            flask.flash("Today's a great day for outdoor activites!")
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
        session["lat"] = lat
        session["lng"] = lng
        currentWeather = weatherResults[0]
        weatherImage = weatherResults[1]
        session["currentWeather"] = currentWeather
        session["weatherImage"] = weatherImage
        if "rain" in currentWeather:
            flask.flash(
                "The weather outside doesn't look so great, let's explore some indoor activites!"
            )
        else:
            flask.flash("Today's a great day for outdoor activites!")
        return redirect(url_for("index"))
    except Exception:
        return render_template("error.html")


@app.route("/recommend", methods=["POST"])
def recommend():
    """
    Call recommendation from get_recommendation.py to generate payload for place recommendation.
    """
    try:
        place_type = request.form["inlineRadioOptions"]
        lat = session.get("lat", None)
        lng = session.get("lng", None)
        # radius is hardcoded to 50 km for now
        radius = request.form["radius"]
        radius = int(radius) * 1610
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


@app.route("/save", methods=["POST"])
@login_required
def save_place():
    """
    Save place_id to database as user's favorite location
    """
    username = current_user.username
    place_id = session.get("place_id")
    current_row = savedSearches.query.filter_by(username=username).first()
    if current_row is not None:
        current_row.savedplaces = place_id
    else:
        db.session.add(savedSearches(username=username, savedplaces=place_id))
    db.session.commit()
    return redirect(url_for("profile"))


@app.route("/profile")
@login_required
def profile():
    """
    Render the user's profile
    """
    username = current_user.username
    userProfileImage = current_user.userProfilePicture
    current_row = savedSearches.query.filter_by(username=username).first()
    if current_row is not None:
        place_id = current_row.savedplaces
        details = favorite_details(place_id=place_id)
        fav_photo = details["photo"]
        fav_place_url = details["url"]
        fav_rating = details["rating"]
        fav_place_name = details["name"]
        return render_template(
            "profile.html",
            username=username,
            fav_photo=fav_photo,
            fav_place_url=fav_place_url,
            fav_rating=fav_rating,
            fav_place_name=fav_place_name,
            userProfileImage=userProfileImage,
        )
    else:
        return render_template(
            "profile.html",
            username=username,
            fav_place_name=None,
            userProfileImage=userProfileImage,
        )


@app.route("/error", methods=["POST"])
def retry():
    """
    Render error.html if any exceptions occur.
    User will click a button that attempts to render index.html.
    """
    return redirect(url_for("index"))


@app.route("/logout")
@login_required
def logout():
    """
    Logout method
    """
    logout_user()
    return flask.redirect(flask.url_for("index"))


@login_manager.unauthorized_handler
def unauthorized():
    """
    Redirect user to login if they are not logged in.
    """
    return redirect(url_for("login"))


app.run(
    host=os.getenv("IP", "0.0.0.0"),
    port=int(os.getenv("PORT", 8080)),
    debug=True,
)
