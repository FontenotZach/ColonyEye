########################################################################################################################
#
#   File: ColonyEye.py
#   Purpose: Driver
#
########################################################################################################################

from threading import *
from Matrix import MatrixBot
from time import sleep

from src.Utils import DBAdapter, Util
#DBAdapter.wipe()
DBAdapter.db_init()


T = Thread(target=Util.monitor_daemon_dropbox)
T.daemon = True
T.start()

T_bot = Thread(target=MatrixBot.run_bot)
T_bot.daemon = True
T_bot.start()

while True:
    sleep(100)

