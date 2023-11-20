import os
import sys
from dropbox import Dropbox
from dropbox import DropboxOAuth2FlowNoRedirect

folder_path = '/ColonyRack_data/'
APP_KEY = "d7tqkcps28kfnas"
APP_SECRET = "0lpipnnl5nkg5ne"

auth_flow = DropboxOAuth2FlowNoRedirect(APP_KEY, APP_SECRET)

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

with Dropbox(oauth2_access_token=oauth_result.access_token) as dropbox_client:
    dropbox_client.users_get_current_account()
    print("Successfully set up client!")

#     print(str(type(dbx)))
#
# DROPBOX_TOKEN = 'sl.BpWTb9D_3M72uiUKbi2t0pCvavxkVW-sQbXGNLIkT1QHJfz8z5TcmZzKBZM12JgzYFmtI6gvYgLwV6YYZDi2dzx_sr-Q-VTu2Mvjd0G_oMDdB4CtGdjVNJox5-Xt7m-uPQKOa-Rr73IoCjelpQZN'
# dropbox_client = Dropbox(DROPBOX_TOKEN)
# folder_path = '/ColonyRack_data/'
#
# print(str(type(dropbox_client)))


def get_latest(update_time):
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
            download_path = os.path.join(os.getcwd(), "Data", "MiceData.csv"),
            path=dropbox_download_path)
    elif 'linux' in sys.platform:
        dropbox_client.files_download_to_file(
            download_path='Data/MiceData.csv',
            path=dropbox_download_path)

    return [True, most_recent_date]
