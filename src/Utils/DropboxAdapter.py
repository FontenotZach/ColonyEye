########################################################################################################################
#
#   File: DropboxAdapter.py
#   Purpose: Communicates with Dropbox cloud file storage
#
########################################################################################################################

import os
import yaml
from yaml import CLoader as Loader
from dropbox import Dropbox
from dropbox import DropboxOAuth2Flow

yaml_path = os.path.join(os.getcwd(), 'config.yaml')

with open(yaml_path, 'r') as yaml_file:
    data = yaml.load(yaml_file, Loader=Loader)

class DropboxAdapter:
     
    def __init__(self, REDIRECT_URI):
        self.folder_path = data.get('dropbox')[0].get('folder_path')
        self.APP_KEY = data.get('dropbox')[0].get('app_key')
        self.APP_SECRET = data.get('dropbox')[0].get('app_secret')     
        self.access_token = ''  
        self.refresh_token = ''
        self.REDIRECT_URI = REDIRECT_URI 

    def auth_start(self, session):
        auth_flow = DropboxOAuth2Flow(consumer_key=self.APP_KEY, consumer_secret=self.APP_SECRET, redirect_uri=self.REDIRECT_URI, session=session, csrf_token_session_key='dropbox-auth-csrf-token', token_access_type='offline')
        authorize_url = auth_flow.start()  
        return authorize_url

    def auth_finish(self, session, args):
        auth_flow = DropboxOAuth2Flow(consumer_key=self.APP_KEY, consumer_secret=self.APP_SECRET, redirect_uri=self.REDIRECT_URI, session=session, csrf_token_session_key='dropbox-auth-csrf-token', token_access_type='offline')
        oauth_result = auth_flow.finish(args)
        self.access_token = oauth_result.access_token
        self.refresh_token = oauth_result.refresh_token
        return self.access_token
        
    def get_previous(self, log):
        with Dropbox(app_key=self.APP_KEY, app_secret=self.APP_SECRET, oauth2_refresh_token=self.refresh_token) as dropbox_client:
            dropbox_client.users_get_current_account()
            print("Successfully refreshed Dropbox client")
            log.push_message('monitor', 'Dropbox client success')
    
        file_list = dropbox_client.files_list_folder(self.folder_path)
        csv_files = []
    
        for entry in file_list.entries:
            if entry.name.lower().endswith('.csv'):
                csv_files.append(self.folder_path + entry.name)
    
        return csv_files
    
    def get_latest(self, update, log):
    
        with Dropbox(app_key=self.APP_KEY, app_secret=self.APP_SECRET, oauth2_refresh_token=self.refresh_token) as dropbox_client:
            dropbox_client.users_get_current_account()
            print("Successfully refreshed Dropbox client")
            log.push_message('monitor', 'Dropbox client success')
    
        file_list = dropbox_client.files_list_folder(self.folder_path)
        most_current_file = file_list.entries[0].name
        most_recent_date = file_list.entries[0].server_modified
    
        for entry in file_list.entries:
            if entry.name.lower().endswith('.csv'):
                if entry.server_modified > most_recent_date:
                    most_recent_date = entry.server_modified
                    most_current_file = entry.name
    
        log.push_message('monitor', 'Found most recent file in dropbox: ' + str(most_current_file))
    
        dropbox_download_path = self.folder_path + most_current_file
    
        if most_recent_date == update.update_time:
            update.update_available = False
            log.push_message('monitor', 'No update available')
            return
    
        dropbox_client.files_download_to_file(download_path=os.path.join(os.getcwd(), "Data", "MiceData.csv"), path=dropbox_download_path)
        log.push_message('monitor', 'Update found: File downloaded')
    
        update.update_available = True
        update.update_time = most_recent_date
        return
    
    def get_file(self, log, file_name):
        with Dropbox(app_key=self.APP_KEY, app_secret=self.APP_SECRET, oauth2_refresh_token=self.refresh_token) as dropbox_client:
            dropbox_client.users_get_current_account()
            print("Successfully refreshed Dropbox client")
            log.push_message('monitor', 'Dropbox client success')
    
        dropbox_client.files_download_to_file(
            download_path=os.path.join(os.getcwd(), "Data", "MiceData.csv"), path=file_name)
        log.push_message('monitor', 'File downloaded')
