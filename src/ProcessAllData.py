########################################################################################################################
#
#   File: ProcessAllData.py
#   Purpose: Driver
#
########################################################################################################################

from threading import *
from Matrix import MatrixBot
from time import sleep
from Utils import Logger
from src.Utils import DBAdapter, Util

db = DBAdapter.db(True)

db.wipe()

db.db_init()

db.close_cursor()

util = Util.Util()

log = Logger.Logger()

T = Thread(target=util.write_historic_data, args=(log,))
T.daemon = True
T.start()

T_log = Thread(target=log.log)
T_log.daemon = True
T_log.start()

while T.is_alive():
    sleep(60)
