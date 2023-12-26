import queue
import datetime
import os
from time import sleep


class Logger:
    def __init__(self):
        self.q = queue.Queue()
        self.f_name = os.path.join(os.getcwd(), os.path.pardir, 'Logs', 'ColonyEye_log_' + datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S') + '.txt')
        self.file = open(self.f_name, 'w')
        self.file.close()

    def push_message(self, source, message):
        self.q.put(str(source) + ' @ ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ': ' + str(message) + '\n')

    def log(self):
        while True:
            sleep(15)
            while self.q.qsize() > 0:
                try:
                    self.file = open(self.f_name, 'a')

                    out = self.q.get()
                    self.file.write(out)
                    self.file.close()
                except:
                    pass
