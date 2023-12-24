########################################################################################################################
#
#   File: RfidDevice.py
#   Purpose: Tracks RFID devices in ColonyRack
#
########################################################################################################################

class RfidDevice:
    def __init__(self, id, id_label, unit_label, event_duration, sense_duration):
        self.id = id
        self.id_label = id_label
        self.unit_label = unit_label
        self.event_duration = event_duration
        self.sense_duration = sense_duration

