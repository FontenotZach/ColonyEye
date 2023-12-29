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
from dropbox import DropboxOAuth2FlowNoRedirect

yaml_path = os.path.join(os.getcwd(), os.path.pardir, 'config.yaml')

with open(yaml_path, 'r') as yaml_file:
    data = yaml.load(yaml_file, Loader=Loader)

class DropboxAdapter:
     
    def __init__(self):
        self.folder_path = data.get('dropbox')[0].get('folder_path')
        self.APP_KEY = data.get('dropbox')[0].get('app_key')
        self.APP_SECRET = data.get('dropbox')[0].get('app_secret')
        
        auth_flow = DropboxOAuth2FlowNoRedirect(self.APP_KEY, self.APP_SECRET, token_access_type='offline')
        
        authorize_url = auth_flow.start()
        print("1. Go to: " + authorize_url)
        print("2. Click \"Allow\" (you might have to log in first).")
        print("3. Copy the authorization code.")
        auth_code = input("Enter the authorization code here: ").strip()
        
        try:
            self.oauth_result = auth_flow.finish(auth_code)
        except Exception as e:
            print('Error: %s' % (e,))
            exit(1)
    
    def get_previous(self, log):
        with Dropbox(app_key=self.APP_KEY, app_secret=self.APP_SECRET, oauth2_refresh_token=self.oauth_result.refresh_token) as dropbox_client:
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
    
        with Dropbox(app_key=self.APP_KEY, app_secret=self.APP_SECRET, oauth2_refresh_token=self.oauth_result.refresh_token) as dropbox_client:
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
    
        dropbox_client.files_download_to_file(download_path=os.path.join(os.getcwd(), os.path.pardir, "Data", "MiceData.csv"), path=dropbox_download_path)
        log.push_message('monitor', 'Update found: File downloaded')
    
        update.update_available = True
        update.update_time = most_recent_date
        return
    
    def get_file(self, log, file_name):
        with Dropbox(app_key=self.APP_KEY, app_secret=self.APP_SECRET, oauth2_refresh_token=self.oauth_result.refresh_token) as dropbox_client:
            dropbox_client.users_get_current_account()
            print("Successfully refreshed Dropbox client")
            log.push_message('monitor', 'Dropbox client success')
    
        dropbox_client.files_download_to_file(
            download_path=os.path.join(os.getcwd(), os.path.pardir, "Data", "MiceData.csv"), path=file_name)
        log.push_message('monitor', 'File downloaded')