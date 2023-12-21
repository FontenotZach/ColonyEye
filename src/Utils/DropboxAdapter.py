import os
import sys
import yaml
from yaml import CLoader as Loader
from dropbox import Dropbox
from dropbox import DropboxOAuth2FlowNoRedirect

yaml_path = os.path.join(os.getcwd(), '../config.yaml')

with open(yaml_path, 'r') as yaml_file:
    data = yaml.load(yaml_file, Loader=Loader)

folder_path = '/ColonyRack_data/'

APP_KEY = data.get('dropbox')[0].get('app_key')
APP_SECRET = data.get('dropbox')[0].get('app_secret')

auth_flow = DropboxOAuth2FlowNoRedirect(APP_KEY, APP_SECRET, token_access_type='offline')

authorize_url = auth_flow.start()
print("1. Go to: " + authorize_url)
print("2. Click \"Allow\" (you might have to log in first).")
print("3. Copy the authorization code.")
auth_code = input("Enter the authorization code here: ").strip()

try:
    oauth_result = auth_flow.finish(auth_code)
except Exception as e:
    print('Error: %s' % (e,))
    exit(1)


def get_latest(update_time):

    with Dropbox(app_key=APP_KEY, app_secret=APP_SECRET, oauth2_refresh_token=oauth_result.refresh_token) as dropbox_client:
        dropbox_client.users_get_current_account()
        print("Successfully refreshed Dropbox client")

    file_list = dropbox_client.files_list_folder(folder_path)
    most_current_file = file_list.entries[0].name
    most_recent_date = file_list.entries[0].server_modified

    for entry in file_list.entries:
        if entry.name.lower().endswith('.csv'):
            if entry.server_modified > most_recent_date:
                most_recent_date = entry.server_modified
                most_current_file = entry.name

    dropbox_download_path = folder_path + most_current_file

    if most_recent_date == update_time:
        print('No new file to download.')
        return [False, update_time]

    if 'win32' in sys.platform:
        dropbox_client.files_download_to_file(
            download_path = os.path.join(os.getcwd(), "../Data", "MiceData.csv"),
            path=dropbox_download_path)
    elif 'linux' in sys.platform:
        dropbox_client.files_download_to_file(
            download_path='../Data/MiceData.csv',
            path=dropbox_download_path)

    return [True, most_recent_date]
