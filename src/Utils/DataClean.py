########################################################################################################################
#
#   File: DataClean.py
#   Purpose: Parsing and packaging of data based on ColonyRack file format
#
########################################################################################################################

import pandas as pd
from src.ColonyRackObjs.MouseEvent import MouseEvent
from src.ColonyRackObjs.RfidDevice import RfidDevice
from src.ColonyRackObjs.CageNode import CageNode
from src.ColonyRackObjs.CageConnection import CageConnection
from src.ColonyRackObjs.CageNetwork import CageNetwork
from src.Utils import DBAdapter
from src.ColonyRackObjs.Mouse import Mouse
import sys
import os
import mysql.connector
import datetime

class DataClean:
    
    def __init__(self):
        self.mouse_events = []
        self.sorted_events = []
        self.rfid_devices = []
        self.cage_network = None
        self.mouse_list = []
        self.update_time = 0
    
    
    def populate_mouse_obj(self, log):
    
        temp_list = []
        count = 0
    
        log.push_message('monitor', 'Subject population start')
    
        for event in self.mouse_events:
            count += 1
            if event.id_label not in temp_list and event.id_label != '' and event.id_label != 'none':
                event_list = []
                m = Mouse(event.id_label, event.id_rfid, event_list)
                m.add_event(event)
                self.mouse_list.append(m)
                temp_list.append(event.id_label)
            else:
                pos = temp_list.index(event.id_label)
                self.mouse_list[pos].add_event(event)
    
        log.push_message('monitor', 'Subject population stop')
    
    
    def clean(self, log):
        raw_data = pd.read_csv(os.path.join(os.getcwd(), os.path.pardir, "Data", "MiceData.csv"), encoding='utf-16', delimiter=';')
    
        for row in raw_data.iterrows():
            if row[1].get('DateTime') == '#ID-Device':
                r1 = RfidDevice(row[1].get('IdRFID'), row[1].get('IdLabel'), row[1].get('unitLabel'), row[1].get('eventDuration'), row[1].get('sense1duration'))
                self.rfid_devices.append(r1)
            elif row[1].get('DateTime') != '':
                m1 = MouseEvent(row[1].get('DateTime'), row[1].get('IdRFID'), row[1].get('IdLabel'), row[1].get('unitLabel'), row[1].get('eventDuration'), row[1].get('senseRFIDrecords'), row[1].get('MsgValue1'))
                self.mouse_events.append(m1)
    
        log.push_message('monitor', 'Event sort start')
        self.sorted_events = sorted(self.mouse_events, key=lambda x: x.time, reverse=True)
        log.push_message('monitor', 'Event sort stop')
    
    
    # TODO This function should eventually handle cage quality
    def read_colony_track_files(self, log):
        self.read_cages(log)
        #read_cage_quality(log)
    
    
    def read_cages(self, log):
        raw_data = pd.read_csv(os.path.join(os.getcwd(), os.path.pardir, "ColonyTrackFiles", "CageNetwork.tsv"),
                               delimiter='\t')
    
        grouped = raw_data.groupby("Source").head(1000)
        temp = []
        cage_list = []
    
        count = 0
    
        for ind in grouped.index:
    
            node_source = None
            node_dest = None
            connection_id = grouped['Link'][ind]
    
            if grouped['Source'][ind] not in temp:
                count += 1
                temp.append(grouped['Source'][ind])
                connections_source = []
                node_source = CageNode(grouped['Source'][ind], connections_source)
                cage_list.append(node_source)
            else:
                index = temp.index(grouped['Source'][ind])
                node_source = cage_list[index]
    
            if grouped['Target'][ind] not in temp:
                count += 1
                temp.append(grouped['Target'][ind])
                connections_source = []
                node_dest = CageNode(grouped['Target'][ind], connections_source)
                cage_list.append(node_dest)
            else:
                index = temp.index(grouped['Target'][ind])
                node_dest = cage_list[index]
    
            connection = CageConnection(node_source, node_dest, connection_id)
            node_source.add_connection(connection)
            node_dest.add_connection(connection)
    
        log.push_message('monitor', 'read_cages() found ' + str(count) + ' connections')
    
        self.cage_network = CageNetwork(cage_list)
    
    
    def to_database(self, update, log):
    
        db = DBAdapter.db(True)
    
        count = 0
        connection_count = 0
    
        db.add_colony_record(self.cage_network)
        log.push_message('monitor', 'B added cage network record')
    
        for node in self.cage_network.nodes:
            db.add_cage_record(node, self.cage_network)
            count += 1
        for node in self.cage_network.nodes:
            for connection in node.connections:
                db.add_connection_record(connection)
                connection_count += 1
    
    
        log.push_message('monitor', 'DB processed ' + str(count) + ' cage records and ' + str(connection_count) + ' connection records')
    
        count = 0
        for mouse in self.mouse_list:
            db.add_subject_record(mouse, self.cage_network)
            count += 1
            pass
    
        log.push_message('monitor', 'DB processed ' + str(count) + ' subject records')
    
        count = 0
        # TODO improve time complexity
        if update.first_pass:
            for event in self.sorted_events:
                db.add_event_record(event)
                count += 1
                if count > 10:
                    break
    
            update.previous_update_time = update.update_time
            update.first_pass = False
        else:
            for event in self.sorted_events:
                if event.time > update.previous_update_time:
                    db.add_event_record(event)
                    count += 1
                else:
                    break
            update.previous_update_time = update.update_time
        log.push_message('monitor', 'DB processed ' + str(count) + ' event records')
    
        db.commit()
        db.close_cursor()
        log.push_message('monitor', 'DB committed')

    def generate_report(self, update, log):
        count = 0

        db = DBAdapter.db(True)

        db.clear_reports()

        for mouse in self.mouse_list:
            count += 1
            db.add_report(mouse.id_label, mouse.event_list[0].time.strftime('%Y-%m-%d %H:%M:%S'),
                          mouse.event_list[0].unit_label)

        log.push_message('monitor', 'generate_report() wrote ' + str(count) + ' reports to DB')

        db.commit()

        db.close_cursor()
    
