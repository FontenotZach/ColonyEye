import yaml
from yaml import CLoader as Loader
import os
import mysql.connector
import ColonyTrack.ColonyTrackAdapter as ct
import datetime

#

from Utils import DBAdapter

import pyttsx3
engine = pyttsx3.init() # object creation

""" RATE"""
rate = engine.getProperty('rate')   # getting details of current speaking rate
print (rate)                        #printing current voice rate
engine.setProperty('rate', 125)     # setting up new voice rate


"""VOLUME"""
volume = engine.getProperty('volume')   #getting to know current volume level (min=0 and max=1)
print (volume)                          #printing current volume level
engine.setProperty('volume',1.0)    # setting up volume level  between 0 and 1

"""VOICE"""
voices = engine.getProperty('voices')       #getting details of current voice
#engine.setProperty('voice', voices[0].id)  #changing index, changes voices. o for male
engine.setProperty('voice', voices[1].id)   #changing index, changes voices. 1 for female




db = DBAdapter.db(True)

output = db.get_connections()

db.add_message('connections', output)



engine.say("Ding ding ding")
engine.say("Ding ding ding")
engine.say("Ding ding ding")
engine.say("Ding ding ding")
engine.say("Ding ding ding")
engine.say("Ding ding ding")
engine.say("Ding ding ding")
engine.say("Ding ding ding")
engine.say("Ding ding ding")
engine.say("Ding ding ding")
engine.say("Ding ding ding")
engine.say("Ding ding ding")
engine.say("Ding ding ding")
engine.say("Ding ding ding")
engine.say("Ding ding ding")
engine.say("Ding ding ding")
engine.say("Ding ding ding")
engine.say("Ding ding ding")
engine.say("Ding ding ding")
engine.say("Ding ding ding")
engine.say("Ding ding ding")
engine.say("Ding ding ding")
engine.say("Ding ding ding")
engine.say("Ding ding ding")
engine.say("Ding ding ding")
engine.say("Ding ding ding")
engine.say("Ding ding ding")
engine.say("Ding ding ding")
engine.say("Ding ding ding")
engine.runAndWait()
engine.stop()

db.commit()
db.close_cursor()





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



