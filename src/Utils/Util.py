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
from src.Utils import DropboxAdapter
from src.Utils import Logger
from flask import current_app


class Util:

    def __init__(self, dropbox):
        self.update = Update.Update(False, 0, True, 0)   # Is there an update, what time was the update made, is it the first pass (hardcoded)
        self.dropbox = dropbox

    def monitor_daemon_dropbox(self, log):

        from src.Utils import DropboxAdapter

        thread_id = 'Data Manager'

        log.push_message(thread_id, 'daemon running')

        random.seed()

        loop_count = 0

        while True:

            data_clean = DataClean.DataClean()

            log.push_message(thread_id, 'Task Start:')

            log.push_message(thread_id, 'Fetching Dropbox data...')
            self.dropbox.get_latest(self.update, log)

            last_check = datetime.datetime.now()

            log.push_message(thread_id, 'Most recent file timestamp:')
            log.push_message(thread_id, self.update.update_time.strftime('%m/%d/%y %H:%M:%S'))
            log.push_message(thread_id, 'Data fetch complete.')

            if self.update.update_available:

                log.push_message(thread_id, 'Cleaning data...')
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

                log.push_message(thread_id, 'Writing out to DB')
                data_clean.to_database(self.update, log)

                log.push_message(thread_id, 'Checking mice activity...')
                data_clean.generate_report(self.update, log)
                log.push_message(thread_id, '\nFinished activity check.')
                # mouse_of_the_hour(DataClean.mouse_list)

                log.push_message(thread_id, '\n\nTask complete, sleeping 1 hr...')

                if loop_count % 12 == 0:
                    data_clean.calc_metrics(log)
                loop_count += 1
            else:
                log.push_message(thread_id, 'No update, sleeping...')
            log.push_message('monitor', 'sleeping until next hour')



            while (datetime.datetime.now() - last_check).total_seconds() < 3600:
                time.sleep(10)

    def mouse_of_the_hour(self, mouse_list, data_clean):
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

    def to_console(self, thread_id, message):
        print(str(thread_id) + ' @ ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ': ' + message)

    def write_historic_data(self, log):

        from Utils import DropboxAdapter

        files = self.dropbox.get_previous(log)

        for file in files:

            log.push_message('historical_file_writer', 'Processing file ' + str(file))

            self.dropbox.get_file(log, file)

            h_update = Update.Update(True, 0, True, 0)

            data_clean = DataClean.DataClean()

            data_clean.clean(log)
            data_clean.populate_mouse_obj(log)
            for mouse in data_clean.mouse_list:
                mouse.sort_events()
            data_clean.read_colony_track_files(log)

            data_clean.to_database(h_update, log)

        log.push_message('historical_file_writer', 'Processed ' + str(len(files)) + ' files')

        log.exit()
        exit()

