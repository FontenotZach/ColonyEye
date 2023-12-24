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

mouse_events = []
rfid_devices = []
cage_network = None
mouse_list = []
update_time = 0


def populate_mouse_obj():

    temp_list = []

    for event in mouse_events:
        if event.id_label not in temp_list and event.id_label != '' and event.id_label != 'none':
            event_list = []
            m = Mouse(event.id_label, event.id_rfid, event_list)
            m.add_event(event)
            mouse_list.append(m)
            temp_list.append(event.id_label)
        else:
            pos = temp_list.index(event.id_label)
            mouse_list[pos].add_event(event)


def clean():
    raw_data = pd.read_csv(os.path.join(os.getcwd(), os.path.pardir, "Data", "MiceData.csv"), encoding='utf-16', delimiter=';')

    for row in raw_data.iterrows():
        if row[1].get('DateTime') == '#ID-Device':
            r1 = RfidDevice(row[1].get('IdRFID'), row[1].get('IdLabel'), row[1].get('unitLabel'), row[1].get('eventDuration'), row[1].get('sense1duration'))
            rfid_devices.append(r1)
        elif row[1].get('DateTime') != '':
            m1 = MouseEvent(row[1].get('DateTime'), row[1].get('IdRFID'), row[1].get('IdLabel'), row[1].get('unitLabel'), row[1].get('eventDuration'), row[1].get('senseRFIDrecords'), row[1].get('MsgValue1'))
            mouse_events.append(m1)


def read_colony_track_files():
    read_cages()


def read_cages():
    global cage_network
    raw_data = pd.read_csv(os.path.join(os.getcwd(), os.path.pardir, "ColonyTrackFiles", "CageNetwork.tsv"),
                           delimiter='\t')

    grouped = raw_data.groupby("Source").head(1000)
    temp = []
    cage_list = []

    for ind in grouped.index:

        node_source = None
        node_dest = None
        connection_id = grouped['Link'][ind]

        if grouped['Source'][ind] not in temp:
            temp.append(grouped['Source'][ind])
            connections_source = []
            node_source = CageNode(grouped['Source'][ind], connections_source)
            cage_list.append(node_source)
        else:
            index = temp.index(grouped['Source'][ind])
            node_source = cage_list[index]

        if grouped['Target'][ind] not in temp:
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

    cage_network = CageNetwork(cage_list)


def to_database():
    try:
        DBAdapter.add_colony_record(cage_network)
    except mysql.connector.errors.IntegrityError:
        None

    for node in cage_network.nodes:
        try:
            DBAdapter.add_cage_record(node, cage_network)
        except mysql.connector.errors.IntegrityError:
            None
        for connection in node.connections:
            try:
                DBAdapter.add_connection_record(connection)
            except mysql.connector.errors.IntegrityError:
                None

    for mouse in mouse_list:
        try:
            DBAdapter.add_subject_record(mouse, cage_network)
        except mysql.connector.errors.IntegrityError:
            None

    # TODO improve time complexity
    for event in mouse_events:
        try:
            DBAdapter.add_event_record(event)
        except mysql.connector.errors.IntegrityError:
            None

    DBAdapter.commit()

