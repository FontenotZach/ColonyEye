########################################################################################################################
#
#   File: DBAdapter.py
#   Purpose: Communicates with MySQL database
#
########################################################################################################################
import datetime
import mysql.connector
import yaml
from yaml import CLoader as Loader
import os

yaml_path = os.path.join(os.getcwd(), os.path.pardir, 'config.yaml')

with open(yaml_path, 'r') as yaml_file:
    data = yaml.load(yaml_file, Loader=Loader)


mydb = mysql.connector.connect(
    host=data.get('db_specs')[0].get('host'),
    port=data.get('db_specs')[0].get('port'),
    user=data.get('db_users')[0].get('username'),
    password=data.get('db_users')[0].get('password'),
    database=data.get('db_specs')[0].get('name')
)

mycursor = mydb.cursor(buffered=True)


def db_init():
    try:
        mycursor.execute('CREATE TABLE colonies (colony_id VARCHAR(255), PRIMARY KEY (colony_id))')
    except:
        db_error('init error: colonies table creation')

    try:
        mycursor.execute(
            'CREATE TABLE subjects (subject_id VARCHAR(255), colony_id VARCHAR(255), rfid_num VARCHAR(255), PRIMARY KEY (subject_id), FOREIGN KEY  (colony_id) references colonies(colony_id))')
    except:
        db_error('init error: reports table subjects')

    try:
        mycursor.execute('CREATE TABLE cages (cage_id VARCHAR(255), colony_id VARCHAR(255), num_connections VARCHAR(255), PRIMARY KEY (cage_id), FOREIGN KEY (colony_id) references colonies(colony_id))')

    except:
        db_error('init error: cages table creation')

    try:
        mycursor.execute('CREATE TABLE cage_connections (connection_id VARCHAR(255), cage_source VARCHAR(255), cage_target VARCHAR(255), PRIMARY KEY (connection_id), FOREIGN KEY (cage_source) references cages(cage_id), FOREIGN KEY (cage_target) references cages(cage_id))')

    except:
        db_error('init error: cage_connections table creation')

    try:
        mycursor.execute('CREATE TABLE events (event_id VARCHAR(255), connection_id VARCHAR(255), subject_id VARCHAR(255), datetime DATETIME, PRIMARY KEY (event_id), FOREIGN KEY (connection_id) references cage_connections(connection_id), FOREIGN KEY (subject_id) references subjects(subject_id))')

    except:
        db_error('init error: events table creation')

    try:
        mycursor.execute('CREATE TABLE reports (subject_id VARCHAR(255), datetime DATETIME, last_connection VARCHAR(255), PRIMARY KEY (subject_id), FOREIGN KEY (last_connection) references cage_connections(connection_id))')

    except:
        db_error('init error: reports table creation')


def add_colony_record(colony):
    try:
        mycursor.execute('INSERT INTO colonies (colony_id) VALUES (\"' + str(colony.colony_id) + '\")')
    except:
        pass


def add_subject_record(subject, colony):
    try:
        mycursor.execute('INSERT INTO subjects (subject_id, colony_id, rfid_num) VALUES (\"' + str(subject.id_label) + '\", \"' + str(colony.colony_id) + '\", \"' + str(subject.id_rfid) + '\")')
    except:
        pass

def add_cage_record(cage, colony):
    try:
        mycursor.execute('INSERT INTO cages (cage_id, colony_id, num_connections) VALUES (\"' + str(
            cage.node_id) + '\", \"' + str(colony.colony_id) + '\", \"' + str(len(cage.connections)) + '\")')
    except:
        pass

def add_connection_record(connection):
    try:
        mycursor.execute('INSERT INTO cage_connections (connection_id, cage_source, cage_target) VALUES (\"' + str(
            connection.connection_id) + '\", \"' + str(connection.cage_node_1.node_id) + '\", \"' + str(connection.cage_node_2.node_id) + '\")')
    except:
        pass

def add_report(subject, time, last):

    mycursor.execute('INSERT INTO reports (subject_id, datetime, last_connection) VALUES (\"' + str(subject) + '\", \"' + time + '\" , \"' + str(last) + '\")')


def add_event_record(event):
    try:
        mycursor.execute('INSERT INTO events (event_id, connection_id, subject_id, datetime) VALUES (\"' + str(event.event_id) + '\", \"' + str(event.unit_label) + '\", \"' + str(event.id_label) + '\", \"' + event.time.strftime('%Y-%m-%d %H:%M:%S') + '\")')
    except:
        pass


def get_report():
    output = 'Subject activity data (descending time since last activity):\n'
    output += 'Subject:\t\tLast Activity (UTC):\n'
    mycursor.execute('SELECT * from reports ORDER BY datetime DESC')
    result = mycursor.fetchall()
    for report in result:
        output += str(report[0]) + '\t\t' + report[1].strftime('%Y-%m-%d %H:%M:%S') + '\t\t' + str(report[2]) + '\n'

    return output


def get_connections():
    output = 'Connection data:\n'
    output += 'Source:\t\tDestination:\n'
    mycursor.execute('SELECT * from connections')
    result = mycursor.fetchall()
    for connection in result:
        output += str(connection[1]) + '\t\t' + str(connection[2]) + '\n'

    return output



def get_inactive():
    # try:
    output = 'Data for inactive subjects (last activity >6 hours ago):\n'
    output += 'Subject:\t\tLast Activity (UTC):\n'
    mycursor.execute('SELECT * from reports ORDER BY datetime DESC')
    result = mycursor.fetchall()
    for report in result:
        if (report[1] - datetime.datetime.now()).total_seconds() > 6 * 3600:
            output += str(report[0]) + '\t\t' + report[1].strftime('%Y-%m-%d %H:%M:%S') + '\n'

    return output
    # except:
    #     db_error('get_inactive() error')


def commit():
    mydb.commit()


def wipe():
    mycursor.execute('DROP TABLE events')
    mycursor.execute('DROP TABLE reports')
    mycursor.execute('DROP TABLE cage_connections')
    mycursor.execute('DROP TABLE cages')
    mycursor.execute('DROP TABLE subjects')
    mycursor.execute('DROP TABLE colonies')


def clear_reports():
    try:
        mycursor.execute('DELETE * FROM reports')
    except:
        db_error('clear_reports() error')


def db_error(message):
    print('DB Error @ ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ': ' + message)
