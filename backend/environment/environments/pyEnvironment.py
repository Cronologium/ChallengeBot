import sys

import time

from environment import Environment

import os
import subprocess
import threading


class PythonEnvironment(Environment):
    def __init__(self, source, solution, port):
        super(PythonEnvironment, self).__init__(source, solution, port)
        self.dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'template-py-v2', '.')

    def build(self):
        DEVNULL = open(os.devnull, 'wb')
        os.mkdir(self.solution)

        p = None
        if "win" in sys.platform.lower():
            cmd = ['xcopy', self.dir_path, self.solution, '/E', '/I']
            p = subprocess.Popen(cmd, stdout=DEVNULL, shell=True)
        else:
            cmd = ['cp', '-r', self.dir_path, self.solution]
            p = subprocess.Popen(cmd, stdout=DEVNULL)
        p.wait()
        if "win" in sys.platform.lower():
            cmd = ['copy', self.source, os.path.join(self.solution, 'solution', 'solution.py')]
            p = subprocess.Popen(cmd, stdout=DEVNULL, shell=True)
        else:
            cmd = ['cp', self.source, os.path.join(self.solution, 'solution', 'solution.py')]
            p = subprocess.Popen(cmd, stdout=DEVNULL)
        p.wait()

    def run(self, memory_limit, user, id):
        DEVNULL = open(os.devnull, 'wb')
        if "win" in sys.platform.lower():
            cmd = ['py', '-2', 'main.py', str(self.port), user]
            proc = subprocess.Popen(cmd, cwd=self.solution, shell=True)  # hide errors (we want this?)
        else:
            cmd = 'python main.py ' + str(self.port) + ' ' + user + ' ' + str(id)
            #print cmd, self.source
            proc = subprocess.Popen(cmd.split(), cwd=self.solution, stdout=subprocess.PIPE)  # hide errors (we want this?)
        threading.Thread(target=self.monitor, args=(proc.pid, memory_limit,)).start()  # monitor memory consumption
        out, err = proc.communicate()
        print out, err
