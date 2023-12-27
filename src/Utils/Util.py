########################################################################################################################
#
#   File: Util.py
#   Purpose: Daemon function + misc methods
#
########################################################################################################################

import datetime
import time
import random
from src.Utils import DataClean
from src.Utils import DBAdapter
from src.Utils import Update


update = Update.Update(False, 0, True, 0)   # Is there an update, what time was the update made, is it the first pass (hardcoded)


def excel_time_to_unix_2(fh):
    res = (fh - 25569.0) * 86400.0 + 21600              # convert to UTC
    dt = datetime.datetime.fromtimestamp(int(res))
    return dt


def monitor_daemon_dropbox(log):

    from src.Utils import DropboxAdapter

    thread_id = 'Data Manager'

    log.push_message('monitor', 'daemon running')

    data_clean = DataClean.DataClean()

    random.seed()
    global update
    while True:
        to_console(thread_id, 'Task Start:')

        to_console(thread_id, 'Fetching Dropbox data...')
        DropboxAdapter.get_latest(update, log)
        to_console(thread_id, 'Most recent file timestamp:')
        to_console(thread_id, update.update_time.strftime('%m/%d/%y %H:%M:%S'))
        to_console(thread_id, 'Data fetch complete.')

        if update.update_available:

            to_console(thread_id, 'Cleaning data...')
            data_clean.clean(log)
            data_clean.populate_mouse_obj(log)
            for mouse in data_clean.mouse_list:
                mouse.sort_events()
            data_clean.read_colony_track_files(log)

            # TODO: implement ColonyTrack
            # to_console(thread_id, '\nGetting ColonyTrack metrics...')
            # #try:
            #     ColonyTrackAdapter.checkout_data()
            # #except:
            #     to_console(thread_id, 'ColonyTrack error.')
            # to_console(thread_id, 'Finished calculating ColonyTrack metrics.')

            to_console(thread_id, 'Writing out to DB')
            data_clean.to_database(update, log)

            to_console(thread_id, 'Checking mice activity...')
            data_clean.generate_report(update, log)
            to_console(thread_id, '\nFinished activity check.')
            # mouse_of_the_hour(DataClean.mouse_list)

            to_console(thread_id, '\n\nTask complete, sleeping 1 hr...')
        else:
            to_console(thread_id, 'No update, sleeping...')
        log.push_message('monitor', 'sleeping until next hour')
        time.sleep(3600)


def mouse_of_the_hour(mouse_list, data_clean):
    print('\nMouse of the hour:')
    lucky_mouse = data_clean.mouse_list[random.randint(1, len(mouse_list) - 1)]
    print('\nData from mouse #' + str(lucky_mouse.id_label) + '...')
    print('\tRFID chip ' + str(lucky_mouse.id_rfid))
    print('\tEvents:')
    most_recent_count = 0
    for event in lucky_mouse.event_list:
        print('\t\tMouse ' + str(event.id_label) + ' moved through ' + str(
            event.unit_label) + ' at time ' + event.time.strftime('%m/%d/%y %H:%M:%S'))
        most_recent_count = most_recent_count + 1
        if most_recent_count > 10:
            break


def to_console(thread_id, message):
    print(str(thread_id) + ' @ ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ': ' + message)