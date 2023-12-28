import yaml
from yaml import CLoader as Loader
import os
import mysql.connector
import src.ColonyTrack.ColonyTrackAdapter as ct
import datetime

#

from src.Utils import DBAdapter

db = DBAdapter.db(True)

print(db.get_report())



# ct.checkout_data()
# ct.to_df()



# c1 = CageNode('abc', [])
# c2 = CageNode('123', [])
#
# net = CageNetwork([])
#
# net.add_node(c1)
# net.add_node(c2)
#
# c = CageConnection(c1, c2, 'abc')
#
# c1.add_connection(c)
# c2.add_connection(c)
#
# m = Mouse('hello', 'hiii', [])
# e = MouseEvent(42000, 'hiii', 'hello', 'abc', '123', '123', '123')
#
# m.add_event(e)
#
# DBAdapter.add_cage_record(c1, net)
# DBAdapter.add_cage_record(c2, net)
# DBAdapter.add_connection_record(c)
#
# DBAdapter.add_subject_record(m, net)
# DBAdapter.add_event_record(e)



