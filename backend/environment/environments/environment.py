import os
import subprocess
import time
import psutil
import sys

class Environment(object):
    def __init__(self, source, solution, port):
        self.source = source
        self.port = port
        self.solution = solution

    def build(self):
        pass

    def monitor(self, pid, memory_limit):
        while True:
            try:
                memoryUsage = psutil.Process(pid).memory_info()[0] / float(2 ** 20)
                if memoryUsage > memory_limit:
                    psutil.Process(pid).kill()
                    print "Process " + str(pid) + " was killed due to high memory consumption.\n"
                    return
            except psutil.NoSuchProcess:
                break
            time.sleep(0.1)  # limit checks to be executed 10 times per second
        return

    def run(self, memory_limit, user, id):
        pass

    def tear_down(self):
        if "win" in sys.platform.lower():
            cmd = ['rd', '/S', '/Q', self.solution]
            subprocess.Popen(cmd, shell=True)
        else:
            cmd = 'rm -r ' + self.solution
            subprocess.Popen(cmd.split(' '))
