from subprocess import Popen, PIPE, STDOUT
import threading
from time import sleep
from os import O_NONBLOCK, read
from fcntl import fcntl, F_GETFL, F_SETFL
from configparser import *
from naomigame import *

'''
A job sends a game to the NetDIMM. Each job has an accosiated process (based on tiforce_tools) that sends a game's data over the network to the NetDIMM. A transfer is started with the start() method. Status of the transfer can be checked with finished().
'''

class Job:

    def __init__(self, game=None):
        self._game = game
        self._process = None
        self._status = 0
        self._message = "Ready"
        self._thread = None

    def start(self):
        '''
        start the data transfer thread to send a game to the NetDIMM.
        '''
        self._thread = threading.Thread(target=self._watch)
        self._thread.start()

    def _watch(self):
        # TODO: use mutex?
        # start uploading game from a sub process
        game_path = self._game.filename
        self._message = "Uploading {}...".format(game_path)
        # "-u" option is used to skip buffering of stdout of the sub process
        #self._process = Popen(["python3", "-u", "triforcetools.py", "192.168.1.2", game_path], shell=False, stderr=PIPE)
        self._process = Popen(["python3", "-u", "test.py", str(self._game.size)], shell=False, stderr=PIPE)
        
        # set the O_NONBLOCK flag to the process stderr
        flags = fcntl(self._process.stderr, F_GETFL) # get current flags
        fcntl(self._process.stderr, F_SETFL, flags | O_NONBLOCK)
        
        # watch the progression of the upload task
        while True:
            if self._process.poll() is None:
                # still running so get progression
                output = self._process.stderr.readline()
                if output is not None and len(output) != 0:
                    try:
                        address = int(output, 16)
                    except ValueError:
                        continue # skip this invalid output
                    progression = int(address * 100 / self._game.size)
                    self._message = "LOADING {}%".format(progression)
            else:
                # finished
                # TODO check return code
                self._message = "Ready"
                break;
            sleep(0.1)

    def finished(self):
        '''
        Return value: True if there is no process associated with the job or the associated process has ended.
        '''
        # TODO review this
        if self._process == None:
            return True
        if self._process.poll() == None:
            return False
        
        return True

    def status(self):
        return self._status

    def message(self):
        return self._message