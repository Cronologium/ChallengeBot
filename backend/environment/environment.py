import Queue
import os
import socket
import subprocess
import threading
import time
import traceback

import psutil
import sys

class Environment(object):
    def __init__(self, source, solution, memory_limit, time_limit):
        self.source = source
        self.solution = solution
        self.memory_limit = memory_limit
        self.cmd = None
        self.write_pipe = None
        self.read_pipe = None
        self.proc = None
        self.time_limit = time_limit

    def build(self):
        pass

    def monitor(self):
        while self.proc:
            try:
                memoryUsage = psutil.Process(self.proc.pid).memory_info()[0] / float(2 ** 20)
                if memoryUsage > self.memory_limit:
                    psutil.Process(self.proc.pid).kill()
                    print "Process " + str(self.proc.pid) + " was killed due to high memory consumption.\n"
                    return
            except psutil.NoSuchProcess:
                break
            time.sleep(0.1)  # limit checks to be executed 10 times per second
        return

    def receive_message(self, message, q):
        q.put(self.read_pipe.readline())

    def interact(self, message):
        try:
            if message != '\n':
                if not message.endswith('\n'):
                    message += '\n'
                self.write_pipe.write(message)
        except Exception:
            return None
        q = Queue.Queue()
        t = threading.Thread(target=self.receive_message, args=(message, q))
        t.start()
        t.join(self.time_limit)
        if q.empty():
            return None
        return q.get()

    def run(self):
        self.proc = subprocess.Popen(self.cmd.split(' '), cwd=self.solution, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        threading.Thread(target=self.monitor, args=()).start()  # monitor memory consumption
        self.write_pipe = self.proc.stdin
        self.read_pipe = self.proc.stdout

    def tear_down(self):
        self.read_pipe = None
        self.write_pipe = None
        psutil.Process(self.proc.pid).kill()
        self.proc = None
        cmd = 'rm -r ' + self.solution
        subprocess.Popen(cmd.split(' '))
