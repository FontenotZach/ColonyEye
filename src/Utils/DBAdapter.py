import mysql.connector
import yaml
from yaml import CLoader as Loader
import os
from CageNetwork import CageNetwork

yaml_path = os.path.join(os.getcwd(), '../config.yaml')

with open(yaml_path, 'r') as yaml_file:
    data = yaml.load(yaml_file, Loader=Loader)


mydb = mysql.connector.connect(
    host=data.get('db_specs')[0].get('host'),
    port=data.get('db_specs')[0].get('port'),
    user=data.get('db_users')[0].get('username'),
    password=data.get('db_users')[0].get('password'),
    database=data.get('db_specs')[0].get('name')
)

mycursor = mydb.cursor()

def db_init():

    try:
        mycursor.execute('CREATE TABLE colonies (colony_id VARCHAR(255), PRIMARY KEY (colony_id))')
    except:
        print('colonies table already exists')

    try:
        mycursor.execute(
            'CREATE TABLE subjects (subject_id VARCHAR(255), colony_id VARCHAR(255), rfid_num VARCHAR(255), PRIMARY KEY (subject_id), FOREIGN KEY  (colony_id) references colonies(colony_id))')
    except:
        print('subjects table already exists')

    try:
        mycursor.execute('CREATE TABLE cages (cage_id VARCHAR(255), colony_id VARCHAR(255), num_connections VARCHAR(255), PRIMARY KEY (cage_id), FOREIGN KEY (colony_id) references colonies(colony_id))')

    except:
        print('cages table already exists')

    try:
        mycursor.execute('CREATE TABLE cage_connections (connection_id VARCHAR(255), cage_source VARCHAR(255), cage_target VARCHAR(255), PRIMARY KEY (connection_id), FOREIGN KEY (cage_source) references cages(cage_id), FOREIGN KEY (cage_target) references cages(cage_id))')

    except:
        print('connections table already exists')

    try:
        mycursor.execute('CREATE TABLE events (event_id VARCHAR(255), connection_id VARCHAR(255), subject_id VARCHAR(255), datetime DATETIME, PRIMARY KEY (event_id), FOREIGN KEY (connection_id) references cage_connections(connection_id), FOREIGN KEY (subject_id) references subjects(subject_id))')

    except:
        print('events table already exists')


def add_colony_record(colony):
    mycursor.execute('INSERT INTO colonies (colony_id) VALUES (\"' + str(colony.colony_id) + '\")')


def add_subject_record(subject, colony):
    mycursor.execute('INSERT INTO subjects (subject_id, colony_id, rfid_num) VALUES (\"' + str(subject.id_label) + '\", \"' + str(colony.colony_id) + '\", \"' + str(subject.id_rfid) + '\")')


def add_cage_record(cage, colony):
    mycursor.execute('INSERT INTO cages (cage_id, colony_id, num_connections) VALUES (\"' + str(
        cage.node_id) + '\", \"' + str(colony.colony_id) + '\", \"' + str(len(cage.connections)) + '\")')


def add_connection_record(connection):
    mycursor.execute('INSERT INTO cage_connections (connection_id, cage_source, cage_target) VALUES (\"' + str(
        connection.connection_id) + '\", \"' + str(connection.cage_node_1.node_id) + '\", \"' + str(connection.cage_node_2.node_id) + '\")')


def add_event_record(event):
    mycursor.execute('INSERT INTO events (event_id, connection_id, subject_id, datetime) VALUES (\"' + str(event.event_id) + '\", \"' + str(event.unit_label) + '\", \"' + str(event.id_label) + '\", \"' + event.time.strftime('%Y-%m-%d %H:%M:%S') + '\")')


def get_colony():
    mycursor.execute('SELECT * FROM colonies')
    for a in mycursor:
        print(a)


def commit():
    mydb.commit()


def wipe():
    mycursor.execute('DROP TABLE events')
    mycursor.execute('DROP TABLE cage_connections')
    mycursor.execute('DROP TABLE cages')
    mycursor.execute('DROP TABLE subjects')
    mycursor.execute('DROP TABLE colonies')
