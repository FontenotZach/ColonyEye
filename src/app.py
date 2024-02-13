from flask import Flask, render_template
from flask import current_app
from flask import redirect, session, request, url_for
from flask_dance.contrib.dropbox import make_dropbox_blueprint, dropbox

import os

import yaml
from yaml import CLoader as Loader

import dropbox
from dropbox import DropboxOAuth2Flow

from . import ColonyEye

app = Flask(__name__)
app.secret_key = 'HD*WhdfwF2341F@rqwfWJ'

yaml_path = os.path.join(os.getcwd(), 'config.yaml')
with open(yaml_path, 'r') as yaml_file:
    data = yaml.load(yaml_file, Loader=Loader)


# with app.app_context():
#     current_app.logger.info('Running backend startup')
#     ColonyEye.run_backend()
    

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dropbox-auth-start')
def dropbox_auth_start():

    folder_path = data.get('dropbox')[0].get('folder_path')
    APP_KEY = data.get('dropbox')[0].get('app_key')
    APP_SECRET = data.get('dropbox')[0].get('app_secret')
    REDIRECT_URI = "http://localhost:5000/dropbox-auth-finish"

    
    auth_flow = DropboxOAuth2Flow(consumer_key=APP_KEY, consumer_secret=APP_SECRET, redirect_uri=REDIRECT_URI, session=session, csrf_token_session_key='dropbox-auth-csrf-token', token_access_type='offline')
    authorize_url = auth_flow.start()  

    current_app.logger.warn("CSRF session key: " + str(session['dropbox-auth-csrf-token']))

    return redirect(authorize_url)


@app.route('/dropbox-auth-finish')
def dropbox_auth_finish():

    APP_KEY = data.get('dropbox')[0].get('app_key')
    APP_SECRET = data.get('dropbox')[0].get('app_secret')
    REDIRECT_URI = "http://localhost:5000/dropbox-auth-finish"


    state = request.args.get('state', None)
    auth_code = request.args.get('code', None)

    current_app.logger.warn("state: " + str(state))
    current_app.logger.warn("code: " + str(auth_code))
    
    if auth_code is None:
        return "Authorization code not found in the request.", 400

    # Use the Dropbox SDK or an HTTP request to exchange the code for a token
    # Example with placeholder SDK method:
    auth_flow = DropboxOAuth2Flow(consumer_key=APP_KEY, consumer_secret=APP_SECRET, redirect_uri=REDIRECT_URI, session=session, csrf_token_session_key='dropbox-auth-csrf-token', token_access_type='offline')
    oauth_result = auth_flow.finish(request.args)
    access_token = oauth_result.access_token
    # Save the access token securely (e.g., in the session or database)
    return redirect(url_for('index'))  # Redirect to the main page or appropriate route


