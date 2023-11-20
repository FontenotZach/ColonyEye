from threading import *
import Util
try:
    import DBAdapter
except:
    print('DBAdapter error occurred.')

T = Thread(target=Util.monitor_daemon())
T.daemon = True
T.start()


# notif mouse movmnt, rfid activity,
