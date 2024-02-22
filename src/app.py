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
from .Utils import DropboxAdapter as dropbox_adapter

app = Flask(__name__)
app.secret_key = 'HD*WhdfwF2341F@rqwfWJ'

yaml_path = os.path.join(os.getcwd(), 'config.yaml')
with open(yaml_path, 'r') as yaml_file:
    data = yaml.load(yaml_file, Loader=Loader)

REDIRECT_URI = "http://localhost:5000/dropbox-auth-finish"
dropbox = dropbox_adapter.DropboxAdapter(REDIRECT_URI)


# with app.app_context():
#     current_app.logger.info('Running backend startup')
#     ColonyEye.run_backend()
    

@app.route('/')
def index():
    if 'dropbox_access_token' in session:
        current_app.logger.warn(session.get('dropbox_access_token'))
    else:
        current_app.logger.warn('No keys currently')
    return render_template('index.html')

@app.route('/start')
def start():
    current_app.logger.info('Starting monitor app')
    ColonyEye.run_backend(dropbox=dropbox)
    return redirect(url_for('index')) 


@app.route('/dropbox-auth-start')
def dropbox_auth_start():

    authorize_url = dropbox.auth_start(session)
    return redirect(authorize_url)


@app.route('/dropbox-auth-finish')
def dropbox_auth_finish():
    
    access_token = dropbox.auth_finish(session, request.args)
    session['dropbox_access_token'] = access_token
    return redirect(url_for('index')) 


