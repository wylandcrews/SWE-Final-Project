import os
from dotenv import load_dotenv, find_dotenv
import requests
from flask import url_for, session, jsonify
from flask_oauthlib.client import OAuthException

load_dotenv(find_dotenv())

# DATABASE imports
# from user import User

"""
Google OAuth Logic borrowed from:
https://github.com/lepture/flask-oauthlib/blob/master/example/google.py

Facebook OAuth Logic borrowed from:
https://github.com/lepture/flask-oauthlib/blob/master/example/facebook.py
"""

# STATIC VARIABLES
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", None)

FB_CLIENT_ID = os.getenv("FB_CLIENT_ID", None)
FB_CLIENT_SECRET = os.getenv("FB_CLIENT_SECRET", None)


class OAuthLogin:
    def __init__(self, oauth, app):
        if FB_CLIENT_ID is None or GOOGLE_CLIENT_ID is None:
            print("Please fill out env file with the appropriate variables")
            return

        self.google_client = oauth.remote_app(
            "google",
            consumer_key=GOOGLE_CLIENT_ID,
            consumer_secret=GOOGLE_CLIENT_SECRET,
            request_token_params={"scope": "email"},
            base_url="https://www.googleapis.com/oauth2/v1/",
            request_token_url=None,
            access_token_method="POST",
            access_token_url="https://accounts.google.com/o/oauth2/token",
            authorize_url="https://accounts.google.com/o/oauth2/auth",
        )

        self.meta_client = oauth.remote_app(
            "facebook",
            consumer_key=FB_CLIENT_ID,
            consumer_secret=FB_CLIENT_SECRET,
            request_token_params={"scope": "email"},
            base_url="https://graph.facebook.com",
            request_token_url=None,
            access_token_url="/oauth/access_token",
            access_token_method="GET",
            authorize_url="https://www.facebook.com/dialog/oauth",
        )

    def google_auth(self):
        """
        Google Authentication flow
        :return: flask_redirect: the request uri for google auth
        """
        return self.google_client.authorize(
            callback=url_for("login_google", _external=True)
        )

    def google_callback(self, request):
        """
        Google callback value parser
        :param request: Json data included with google resp
        :return:
        """
        resp = self.google_client.authorized_response()
        if resp is None:
            return "Access denied: reason=%s error=%s" % (
                request.args["error_reason"],
                request.args["error_description"],
            )
        session["google_token"] = (resp["access_token"], "")
        me = self.google_client.get("userinfo")
        return jsonify({"data": me.data})

    def meta_auth(self, request):
        """
        Facebook Authentication Flow
        :return: flask_redirect: the request uri for meta auth
        """
        callback = url_for(
            "login_facebook",
            next=request.args.get("next") or request.referrer or None,
            _external=True,
        )

        return self.meta_client.authorize(callback=callback)

    def meta_callback(self, request):
        """
        Facebook callback value parser
        :param request: Json data included with facebook resp
        :return: User Data
        """
        resp = self.meta_client.authorized_response()
        if resp is None:
            return "Access denied: reason=%s error=%s" % (
                request.args["error_reason"],
                request.args["error_description"],
            )
        if isinstance(resp, OAuthException):
            return "Access denied: %s" % resp.message

        session["oauth_token"] = (resp["access_token"], "")
        me = self.meta_client.get("/me")
        return "Logged in as id=%s name=%s redirect=%s" % (
            me.data["id"],
            me.data["name"],
            request.args.get("next"),
        )
