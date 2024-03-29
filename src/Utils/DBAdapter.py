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
import time

yaml_path = os.path.join(os.getcwd(), 'config.yaml')

with open(yaml_path, 'r') as yaml_file:
    data = yaml.load(yaml_file, Loader=Loader)


class db:

    def __init__(self, buffer):

        connected = False

        while (not connected):
            try:
                self.mydb = mysql.connector.connect(
                    host=os.environ.get('DB_HOST', 'db'),  # Default to 'localhost' if not set
                    port=os.environ.get('DB_PORT', '3306'),
                    user=os.environ.get('DB_USER', 'user'),  # Default user
                    password=os.environ.get('DB_PASSWORD', 'password'),  # Default password
                    database=os.environ.get('MYSQL_DATABASE', 'mydatabase')  # Default database name
                )
                connected = True
            except mysql.connector.errors.DatabaseError:
                time.sleep(10)

        self.my_cursor = self.mydb.cursor(buffered=buffer)

        self.connection_report = 'No connections data at this time, please check back later.'

    def db_init(self):
        try:
            self.my_cursor.execute('CREATE TABLE colonies (colony_id VARCHAR(255), PRIMARY KEY (colony_id))')
        except:
            self.db_error('init error: colonies table creation')
    
        try:
            self.my_cursor.execute(
                'CREATE TABLE subjects (subject_id VARCHAR(255), colony_id VARCHAR(255), rfid_num VARCHAR(255), PRIMARY KEY (subject_id), FOREIGN KEY  (colony_id) references colonies(colony_id))')
        except:
            self.db_error('init error: reports table subjects')
    
        try:
            self.my_cursor.execute('CREATE TABLE cages (cage_id VARCHAR(255), colony_id VARCHAR(255), num_connections VARCHAR(255), PRIMARY KEY (cage_id), FOREIGN KEY (colony_id) references colonies(colony_id))')
    
        except:
            self.db_error('init error: cages table creation')
    
        try:
            self.my_cursor.execute('CREATE TABLE cage_connections (connection_id VARCHAR(255), cage_source VARCHAR(255), cage_target VARCHAR(255), PRIMARY KEY (connection_id), FOREIGN KEY (cage_source) references cages(cage_id), FOREIGN KEY (cage_target) references cages(cage_id))')
    
        except:
            self.db_error('init error: cage_connections table creation')
    
        try:
            self.my_cursor.execute('CREATE TABLE events (event_id VARCHAR(255), connection_id VARCHAR(255), subject_id VARCHAR(255), datetime DATETIME, PRIMARY KEY (event_id), FOREIGN KEY (connection_id) references cage_connections(connection_id), FOREIGN KEY (subject_id) references subjects(subject_id))')
    
        except:
            self.db_error('init error: events table creation')
    
        try:
            self.my_cursor.execute('CREATE TABLE reports (subject_id VARCHAR(255), datetime DATETIME, last_cage VARCHAR(255), PRIMARY KEY (subject_id), FOREIGN KEY (last_cage) references cages(cage_id))')

        except:
            self.db_error('init error: reports table creation')

        try:
            self.my_cursor.execute('CREATE TABLE messages (message_id VARCHAR(255), datetime DATETIME, content TEXT)')
        except:
            self.db_error('init error: messages table creation')

    def add_colony_record(self, colony):
        try:
            self.my_cursor.execute('INSERT INTO colonies (colony_id) VALUES (\"' + str(colony.colony_id) + '\")')
        except mysql.connector.errors.IntegrityError:
            pass
    
    def add_subject_record(self, subject, colony):
        try:
            self.my_cursor.execute('INSERT INTO subjects (subject_id, colony_id, rfid_num) VALUES (\"' + str(subject.id_label) + '\", \"' + str(colony.colony_id) + '\", \"' + str(subject.id_rfid) + '\")')
        except mysql.connector.errors.IntegrityError:
            pass
    
    def add_cage_record(self, cage, colony):
        try:
            self.my_cursor.execute('INSERT INTO cages (cage_id, colony_id, num_connections) VALUES (\"' + str(
                cage.node_id) + '\", \"' + str(colony.colony_id) + '\", \"' + str(len(cage.connections)) + '\")')
        except mysql.connector.errors.IntegrityError:
            pass
    
    def add_connection_record(self, connection):
        try:
            self.my_cursor.execute('INSERT INTO cage_connections (connection_id, cage_source, cage_target) VALUES (\"' + str(
                connection.connection_id) + '\", \"' + str(connection.cage_node_1.node_id) + '\", \"' + str(connection.cage_node_2.node_id) + '\")')
        except mysql.connector.errors.IntegrityError:
            pass
    
    def add_report(self, subject, time, last):
        try:
            self.my_cursor.execute('INSERT INTO reports (subject_id, datetime, last_cage) VALUES (\"' + str(subject) + '\", \"' + time + '\" , \"' + str(last.node_id) + '\")')
        except mysql.connector.errors.IntegrityError as e:
            print(e)

    def add_event_record(self, event):
        try:
            self.my_cursor.execute('INSERT INTO events (event_id, connection_id, subject_id, datetime) VALUES (\"' + str(event.event_id) + '\", \"' + str(event.unit_label) + '\", \"' + str(event.id_label) + '\", \"' + event.time.strftime('%Y-%m-%d %H:%M:%S') + '\")')
        except mysql.connector.errors.IntegrityError:
            pass

    def add_message(self, message_id, content):
        try:
            query = 'DELETE FROM messages WHERE message_id = %s'

            self.my_cursor.execute(query, (message_id,))

            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            self.my_cursor.execute('INSERT INTO messages (message_id, datetime, content) VALUES (\"' + str(message_id) + '\", \"' + str(now) + '\", \"' + str(content) + '\")')
        except Exception as e:
            print(e)

    def get_message(self, message_id):
        output = ''
        try:
            self.my_cursor.execute('SELECT * FROM messages WHERE message_id = \"' + str(message_id) + '\"')
            result = self.my_cursor.fetchone()

            output = result[2]
        except Exception as e:
            print(e)

        if output == '':
            output = 'Could not retrieve message.'

        return output
    
    def get_report(self):
        output = 'Subject activity data (descending time since last activity):\n'
        output += 'Subject:\t\tLast Activity (UTC):\t\tLast Cage\n'
        self.my_cursor.execute('SELECT * from reports ORDER BY datetime DESC')
        result = self.my_cursor.fetchall()
        if len(result) == 0:
            output = 'No reports at this time.'
        else:
            for report in result:
                if str(report[0]) == 'nan':
                    output += 'control' + '\t\t' + report[1].strftime('%Y-%m-%d %H:%M:%S') + '\t\t' + str(report[2]) + '\n'
                else:
                    output += str(report[0]) + '\t\t' + report[1].strftime('%Y-%m-%d %H:%M:%S') + '\t\t' + str(report[2]) + '\n'

        return output

    def get_connections(self):
        output = 'Connection data (RFID):\n'
        output += 'Connection:\t\tPath:\t\t\t\tUsage: total (in last 10 days)\n'
        self.my_cursor.execute('SELECT * from cage_connections')
        result = self.my_cursor.fetchall()
        if len(result) == 0:
            output = 'No reports at this time.'
        else:
            for connection in result:
                query = "SELECT * FROM events WHERE connection_id = %s"
                self.my_cursor.execute(query, (connection[0],))

                result_events = self.my_cursor.fetchall()

                recent_usage = 0

                for event in result_events:

                    now = datetime.datetime.now()
                    event_time = event[3]

                    delta = (now - event_time).total_seconds()

                    if delta < (3600 * 240):
                        recent_usage += 1

                output += str(connection[0]) + '\t\t\t' + str(connection[1]) + ' to ' + str(connection[2]) + '  \t' + str(len(result_events)) + '  (' + str(recent_usage) + ')\n'

        return output

    def get_inactive(self):
        output = 'Data for inactive subjects (last activity >6 hours ago):\n'
        output += 'Subject:\t\tLast Activity (UTC): \t\tLast Cage:\n'
        self.my_cursor.execute('SELECT * from reports ORDER BY datetime DESC')
        result = self.my_cursor.fetchall()

        inactive_count = 0

        if len(result) == 0:
            output = 'No reports at this time.'
        else:
            for report in result:
                if (datetime.datetime.now() - report[1]).total_seconds() > (6 * 3600):
                    inactive_count += 1
                    if str(report[0]) == 'nan':
                        output += 'control' + '\t\t' + report[1].strftime('%Y-%m-%d %H:%M:%S') + '\t\t' + str(report[2]) + '\n'
                    else:
                        output += str(report[0]) + '\t\t' + report[1].strftime('%Y-%m-%d %H:%M:%S') + '\t\t' + str(report[2]) + '\n'

        if inactive_count == 0:
            output = 'All mice are active in the last 6 hours.'

        return output

    def commit(self):
        self.mydb.commit()

    def wipe(self):
        try:
            self.my_cursor.execute('DROP TABLE events')
        except:
            pass
        try:
            self.my_cursor.execute('DROP TABLE reports')
        except:
            pass
        try:
            self.my_cursor.execute('DROP TABLE cage_connections')
        except:
            pass
        try:
            self.my_cursor.execute('DROP TABLE cages')
        except:
            pass
        try:
            self.my_cursor.execute('DROP TABLE subjects')
        except:
            pass
        try:
            self.my_cursor.execute('DROP TABLE colonies')
        except:
            pass

    def clear_reports(self):
        try:
            self.my_cursor.execute('DROP TABLE reports')

            self.my_cursor.execute('CREATE TABLE reports (subject_id VARCHAR(255), datetime DATETIME, last_cage VARCHAR(255), PRIMARY KEY (subject_id), FOREIGN KEY (last_cage) references cages(cage_id))')

        except mysql.connector.errors.IntegrityError:
            self.db_error('clear_reports() error')

    def db_error(self, message):
        print('DB Error @ ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ': ' + message)

    def close_cursor(self):
        self.my_cursor.close()
        self.mydb.close()

    def refresh_cursor(self, buffer):
        try:
            self.mydb = mysql.connector.connect(
                host=os.environ.get('MYSQL_HOST', 'db'),  # Default to 'localhost' if not set
                port=os.environ.get('MYSQL_PORT', '3306'),
                user=os.environ.get('MYSQL_USER', 'user'),  # Default user
                password=os.environ.get('MYSQL_PASSWORD', 'password'),  # Default password
                database=os.environ.get('MYSQL_DATABASE', 'mydatabase')  # Default database name
            )
            connected = True
        except mysql.connector.errors.DatabaseError:
            time.sleep(10)

        self.my_cursor = self.mydb.cursor(buffered=buffer)
