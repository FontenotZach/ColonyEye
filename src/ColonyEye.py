########################################################################################################################
#
#   File: ColonyEye.py
#   Purpose: Driver
#
########################################################################################################################

from threading import *
from Matrix import MatrixBot
from time import sleep
from Utils import Logger
from Utils import Util

from src.Utils import DBAdapter, Util

db = DBAdapter.db(True)
db.db_init()
db.close_cursor()

util = Util.Util()

log = Logger.Logger()

T = Thread(target=util.monitor_daemon_dropbox, args=(log,))
T.daemon = True
T.start()

T_bot = Thread(target=MatrixBot.run_bot, args=(log,))
T_bot.daemon = True
T_bot.start()

T_log = Thread(target=log.log)
T_log.daemon = True
T_log.start()

while True:
    sleep(100)

