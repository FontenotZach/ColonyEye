import pandas as pd
from MouseEvent import MouseEvent
from RfidDevice import RfidDevice
from Mouse import Mouse
import sys
import os

mouse_events = []
rfid_devices = []
mouse_list = []
update_time = 0


def populate_mouse_obj():

    temp_list = []

    for event in mouse_events:
        if event.id_label not in temp_list:
            event_list = []
            m = Mouse(event.id_label, event.id_rfid, event_list)
            m.add_event(event)
            mouse_list.append(m)
            temp_list.append(event.id_label)
        else:
            pos = temp_list.index(event.id_label)
            mouse_list[pos].add_event(event)





def clean():
    if 'win32' in sys.platform:
        raw_data = pd.read_csv(os.path.join(os.getcwd(), "Data", "MiceData.csv"), encoding='utf-16', delimiter=';')

    elif 'linux' in sys.platform:
        raw_data = pd.read_csv('Data/MiceData.csv', encoding='utf-16', delimiter=';')
    else:
        # cannot read data error
        exit()

    for row in raw_data.iterrows():
        if row[1].get('DateTime') == '#ID-Device':
            r1 = RfidDevice(row[1].get('IdRFID'), row[1].get('IdLabel'), row[1].get('unitLabel'), row[1].get('eventDuration'), row[1].get('sense1duration'))
            rfid_devices.append(r1)
        elif row[1].get('DateTime') != 'nan':
            m1 = MouseEvent(row[1].get('DateTime'), row[1].get('IdRFID'), row[1].get('IdLabel'), row[1].get('unitLabel'), row[1].get('eventDuration'), row[1].get('senseRFIDrecords'), row[1].get('MsgValue1'))
            mouse_events.append(m1)
