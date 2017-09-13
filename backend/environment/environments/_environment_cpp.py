from environment import Environment

import sys
import os
import subprocess
import threading


class CppEnvironment(Environment):
    def __init__(self, source, solution, port):
        super(CppEnvironment, self).__init__(source, solution, port)

    def build(self):
        os.mkdir(self.solution)

        DEVNULL = open(os.devnull, 'wb')
        proc = None
        if "win" in sys.platform.lower():
            cmd = ['xcopy', 'client-template-cpp\windows\*', self.solution, '/s', '/i']
            proc = subprocess.Popen(cmd, stdout=DEVNULL, shell=True)
        else:
            cmd = ['cp', '-r', 'client-template-cpp/linux/.', self.solution]
            proc = subprocess.Popen(cmd, stdout=DEVNULL)
        proc.wait()

        if "win" in sys.platform.lower():
            cmd = ['xcopy', self.source, os.path.join(self.solution, '_g001_battleships.cpp')]
            proc = subprocess.Popen(cmd, stdout=DEVNULL, shell=True)
        else:
            cmd = ['cp', self.source, os.path.join(self.solution, '_g001_battleships.cpp')]
            proc = subprocess.Popen(cmd, stdout=DEVNULL)
        proc.wait()

        if "win" in sys.platform.lower():
            buildCmd = ['g++', '-std=gnu++11', 'Utils.h', 'Utils.cpp', 'Solution.h', 'ClientSolution.h',
                        '_g001_battleships.cpp', 'Client.h', 'Client.cpp', 'Source.cpp', '-lws2_32', '-o', 'Client.exe']
            proc = subprocess.Popen(buildCmd, cwd=self.solution, stdout=DEVNULL, shell=True)  # hide errors (we want this?)
        else:
            buildCmd = ['g++', '-std=gnu++11', 'Utils.h', 'Utils.cpp', 'Solution.h', 'ClientSolution.h',
                        '_g001_battleships.cpp', 'Client.h', 'Client.cpp', 'Source.cpp', '-o', 'Client.out']
            proc = subprocess.Popen(buildCmd, cwd=self.solution, stdout=DEVNULL)  # hide errors (we want this?)
        proc.wait()

    def run(self, memory_limit, user, id):

        DEVNULL = open(os.devnull, 'wb')
        if "win" in sys.platform.lower():
            executable = os.path.join(self.solution, "Client.exe")
            runCmd = [executable, str(self.port), user]
            proc = subprocess.Popen(runCmd, cwd=self.solution, stdout=DEVNULL)  # hide errors (we want this?)
        else:
            runCmd = ['./Client.out', str(self.port), user]
            print runCmd
            proc = subprocess.Popen(runCmd, cwd=self.solution, stdout=DEVNULL)  # hide errors (we want this?)
        threading.Thread(target=self.monitor, args=(proc.pid, memory_limit,)).start()  # monitor memory consumption
        proc.wait()
