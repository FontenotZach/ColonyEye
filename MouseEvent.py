import Util

class MouseEvent:

    event_list = []

    def __init__(self, time, id_rfid, id_label, unit_label, event_duration, sense_rfid_records, sense_value):
        self.time = Util.excel_time_to_unix_2(float(time))
        self.id_rfid = id_rfid
        self.id_label = id_label
        self.unit_label = unit_label
        self.event_duration = event_duration
        self.sense_rfid_records = sense_rfid_records
        self.sense_value = sense_value
