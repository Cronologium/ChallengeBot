import sys

import time

from environment import Environment

import os
import subprocess
import threading


class PythonEnvironment(Environment):
    def __init__(self, source, solution, memory_limit, time_limit):
        super(PythonEnvironment, self).__init__(source, solution, memory_limit, time_limit)
        self.cmd = 'python solution.py'

    def build(self):
        DEVNULL = open(os.devnull, 'wb')
        os.mkdir(self.solution)

        p = None

        cmd = ['cp', self.source, os.path.join(self.solution, 'solution.py')]
        p = subprocess.Popen(cmd, stdout=DEVNULL)
        p.wait()
