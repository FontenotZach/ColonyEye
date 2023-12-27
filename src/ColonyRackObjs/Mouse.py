########################################################################################################################
#
#   File: Mouse.py
#   Purpose: Mouse subject class
#
########################################################################################################################
import datetime


class Mouse:

    def __init__(self, id_label, id_rfid, event_list):
        self.id_label = id_label
        self.id_rfid = id_rfid
        self.event_list = event_list

    def add_event(self, event):
        self.event_list.append(event)

    def sort_events(self):
        self.event_list = sorted(self.event_list, key=lambda x: x.time, reverse=True)

    def is_active(self, update_time):
        if update_time.timestamp() - self.event_list[0].time.timestamp() > 24000:
            return False
        else:
            return True
