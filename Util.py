import datetime
import time
import random
import ColonyTrackAdapter
import DropboxAdapter
import DataClean
import CTMetrics


def excel_time_to_unix_2(fh):
    res = (fh - 25569.0) * 86400.0 + 21600              # convert to Berlin time
    dt = datetime.datetime.fromtimestamp(int(res))
    return dt


def monitor_daemon():
    update = [False, 0]
    random.seed()
    while True:
        print('Task Start:')

        print('Fetching Dropbox data...')
        update = DropboxAdapter.get_latest(update[1])
        print('Most recent file timestamp:')
        print(update[1].strftime('%m/%d/%y %H:%M:%S'))
        print('Data fetch complete.')

        if update[0]:

            print('Cleaning data...')
            DataClean.clean()
            DataClean.populate_mouse_obj()
            for mouse in DataClean.mouse_list:
                mouse.sort_events()

            print('Checking mice activity...')
            for mouse in DataClean.mouse_list:
                print()
                print('Checking on mouse ' + str(mouse.id_label))
                if not mouse.is_active(update[1]):
                    print('Mouse ' + str(mouse.id_label) + ' is not active')
                    # print('\tlast active time: ' + mouse.event_list[0].strftime("%m/%d/%Y, %H:%M:%S"))

                else:
                    print('Mouse ' + str(mouse.id_label) + ' is active')
                    # print('\tlast active time: ' + mouse.event_list[0].strftime("%m/%d/%Y, %H:%M:%S"))
            print('\nFinished activity check.')

            print('\nGetting ColonyTrack metrics...')
            ct_data_pointer = None
            try:
                ColonyTrackAdapter.checkout_data(ct_data_pointer)
            except:
                print('ColonyTrack error.')
            print('Finished calculating ColonyTrack metrics.')

            print('\nMouse of the hour:')
            lucky_mouse = DataClean.mouse_list[random.randint(1, len(DataClean.mouse_list) - 1)]
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

            print('\n\nTask complete, sleeping 1 hr...')
        else:
            print('No update, sleeping...')
        time.sleep(3600)
