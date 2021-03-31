#!/usr/bin/env python
#  -*- coding: utf-8 -*-
"""
Copyright (c) 2020 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.

This sample script leverages the Flask web service micro-framework
(see http://flask.pocoo.org/).  By default the web server will be reachable at
port 5000 you can change this default if desired (see `flask_app.run(...)`).
ngrok (https://ngrok.com/) can be used to tunnel traffic back to your server
if your machine sits behind a firewall: i.e. ‘./ngrok http 5000’
Additional Webex Teams webhook details can be found here:
https://developer.webex.com/webhooks-explained.html

"""


# Use future for Python v2 and v3 compatibility
from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)
from builtins import *


__author__ = ""
__author_email__ = ""
__copyright__ = ""
__license__ = "Cisco"

from requests_oauthlib import OAuth2Session
from flask import Flask, request, redirect, session, url_for, render_template
import requests
import os
import json

from webexteamssdk import WebexTeamsAPI, Webhook
import sys


from urllib.parse import urljoin

#initialize variabes for URLs
#REDIRECT_URL must match what is in the integration
REDIRECT_URI = 'http://0.0.0.0:5000/callback'

from config import CLIENT_SECRET, CLIENT_ID
AUTHORIZATION_BASE_URL = 'https://api.ciscospark.com/v1/authorize'
TOKEN_URL = 'https://api.ciscospark.com/v1/access_token'
SCOPE = 'spark:all'


os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
# Initialize the environment
# Create the web application instance
flask_app = Flask(__name__)
flask_app.secret_key = os.urandom(24)

#api = WebexTeamsAPI(access_token=TEST_TEAMS_ACCESS_TOKEN)
api = None



@flask_app.route("/")
def login():
    """Step 1: User Authorization.
    Redirect the user/resource owner to the OAuth provider (i.e. Webex Teams)
    using a URL with a few key OAuth parameters.
    """

    teams = OAuth2Session(CLIENT_ID, scope=SCOPE, redirect_uri=REDIRECT_URI)
    authorization_url, state = teams.authorization_url(AUTHORIZATION_BASE_URL)

    # State is used to prevent CSRF, keep this for later.

    session['oauth_state'] = state
    return redirect(authorization_url)

# Step 2: User authorization, this happens on the provider.

@flask_app.route("/callback", methods=["GET"])
def callback():
    """
    Step 3: Retrieving an access token.
    The user has been redirected back from the provider to your registered
    callback URL. With this redirection comes an authorization code included
    in the redirect URL. We will use that to obtain an access token.
    """
    print("Client ID: ",CLIENT_ID)
    print("Client secret: ",CLIENT_SECRET)

    auth_code = OAuth2Session(CLIENT_ID, state=session['oauth_state'], redirect_uri=REDIRECT_URI)
    token = auth_code.fetch_token(TOKEN_URL, client_secret=CLIENT_SECRET,
                                  authorization_response=request.url)

    """
    At this point you can fetch protected resources but lets save
    the token and show how this is done from a persisted token
    """

    session['oauth_token'] = token
    return redirect(url_for('.started'))

@flask_app.route("/started", methods=["GET"])
def started():

    # Use returned token to make Teams API for list of spaces
    global api
    teams_token = session['oauth_token']
    # Create the Webex Teams API connection object
    api = WebexTeamsAPI(access_token=teams_token['access_token'])
    theResult=api.people.me()
    print("TheResult calling api.people.me(): ",theResult)

    return ("""<!DOCTYPE html>
               <html lang="en">
                   <head>
                       <meta charset="UTF-8">
                       <title>Webex Teams message re-director served via Flask</title>
                   </head>
               <body>
               <p>
               <strong>Welcome """+theResult.displayName+""" , you have been propertly authenticated!</strong>
               </p>
               Your Webex Person ID is """+theResult.id+""" and the access token for you to use with your code derived from
               this sample is stored in session['oauth_token'] .  
               </body>
               </html>
            """)



# Start the Flask web server
if __name__ == '__main__':
    flask_app.run(host='0.0.0.0', port=5000)