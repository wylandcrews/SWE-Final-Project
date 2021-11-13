import os
import pathlib
import requests
from flask import Flask, session, abort, redirect, request, render_template, url_for
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests
from flask import Flask, redirect, url_for, session, request, render_template
from flask_oauthlib.client import OAuth
import os


app = Flask("Google Login App")
app.secret_key = "Hello Fam"

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="https://127.0.0.1:5000/callback"
)


def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)  # Authorization required
        else:
            return function()

    return wrapper


@app.route("/login")
def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)


@app.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    return redirect("/protected_area")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/")
def index2():
    return "<a href='/login'><button>Login with Google</button></a> <a href='login2'><button>Login with Facebook</button></a>"


@app.route("/protected_area")
@login_is_required
def protected_area():
    return f"Hello {session['name']}! <br/> <a href='/logout'><button>Logout</button></a> <a href='index'><button>Welcome</button></a>"

@app.route("/index")
def index():
    currentWeather = session.get("currentWeather", None)
    weatherImage = session.get("weatherImage", None)
    lat_recommendation = session.get("lat_recommendation", None)
    lng_recommendation = session.get("lng_recommendation", None)

    if currentWeather != None and weatherImage != None and lat_recommendation != None and lng_recommendation != None:
        return render_template(
            "index.html",
            currentWeather=currentWeather,
            weatherImage=weatherImage,
            lat_recommendation=lat_recommendation,
            lng_recommendation=lng_recommendation
        )


SECRET_KEY = 'yay'
DEBUG = True
FACEBOOK_APP_ID = os.getenv("FACEBOOK_APP_ID")
FACEBOOK_APP_SECRET = os.getenv("FACEBOOK_APP_SECRET")

app.debug = DEBUG
app.secret_key = SECRET_KEY
oauth = OAuth()

facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=FACEBOOK_APP_ID,
    consumer_secret=FACEBOOK_APP_SECRET,
    request_token_params={'scope': 'email'}
)


@app.route('/login2')
def login2():
    return facebook.authorize(callback=url_for('facebook_authorized',
        next=request.args.get('next') or request.referrer or None,
        _external=True))


@app.route('/login/authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['oauth_token'] = (resp['access_token'], '')
    me = facebook.get('/me')
    return "Logged in as id=%s name=%s redirect=%s return <a href='/logout2'><button>Logout</button></a> <a href='index'><button>Welcome</button></a>" % \
        (me.data['id'], me.data['name'], request.args.get('next')) 


@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')

@app.route("/logout")
def logout2():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(ssl_context='adhoc')
