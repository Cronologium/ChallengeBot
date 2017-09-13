from environment import Environment

import sys
import os
import subprocess
import threading


class CEnvironment(Environment):
    def __init__(self, source, solution, port):
        super(CEnvironment, self).__init__(source, solution, port)
        self.dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'template-c', '.')

    def build(self):
        os.mkdir(self.solution)
        DEVNULL = open(os.devnull, 'wb')

        p = None
        if "win" in sys.platform.lower():
            cmd = ['xcopy', self.dir_path, self.solution, '/E', '/I']
            p = subprocess.Popen(cmd, stdout=DEVNULL, shell=True)
        else:
            cmd = ['cp', '-r', self.dir_path, self.solution]
            p = subprocess.Popen(cmd, stdout=DEVNULL)
        p.wait()

        proc = None
        if "win" in sys.platform.lower():
            raise NotImplementedError
        else:
            dll_name = self.source[:-2] + '.so'
            if not os.path.isfile(dll_name):
                obj_name = self.source[:-2] + '.o'

                cmd = ['gcc', '-c', '-fPIC', self.source , '-o', obj_name]
                proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
                out, err = proc.communicate()
                if err:
                    raise RuntimeError("Compilation failed for " + self.source + "\n" + err)

                cmd = ['gcc', '-shared', '-o', dll_name, '-fPIC', obj_name]
                proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
                out, err = proc.communicate()
                if err:
                    raise RuntimeError("Linking error for " + self.source + "\n" + err)

                os.remove(obj_name)

            cmd = ['cp', dll_name, os.path.join(self.solution, 'solution.so')]
            proc = subprocess.Popen(cmd, stdout=DEVNULL)
        proc.wait()

        '''
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
        '''

    def run(self, memory_limit, user, id):
        DEVNULL = open(os.devnull, 'wb')
        if "win" in sys.platform.lower():
            cmd = ['py', '-2', 'main.py', str(self.port), user]
            proc = subprocess.Popen(cmd, cwd=self.solution, shell=True)  # hide errors (we want this?)
        else:
            cmd = 'python main.py ' + str(self.port) + ' ' + user + ' ' + str(id)
            proc = subprocess.Popen(cmd.split(), cwd=self.solution, stdout=subprocess.PIPE)  # hide errors (we want this?)
        threading.Thread(target=self.monitor, args=(proc.pid, memory_limit,)).start()  # monitor memory consumption
        out, err = proc.communicate()
        rc = proc.returncode
        print '[Output]', out
        if err:
            print '[Error]', err
        print '[Return code]', rc
