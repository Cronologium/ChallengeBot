import os
import socket
import subprocess
import threading
import time
import traceback

import psutil
import sys

class Environment(object):
    def __init__(self, source, solution, port, memory_limit):
        self.source = source
        self.port = port
        self.solution = solution
        self.memory_limit = memory_limit
        self.cmd = None
        self.write_pipe = None
        self.read_pipe = None


    def build(self):
        pass

    def monitor(self, pid):
        while True:
            try:
                memoryUsage = psutil.Process(pid).memory_info()[0] / float(2 ** 20)
                if memoryUsage > self.memory_limit:
                    psutil.Process(pid).kill()
                    print "Process " + str(pid) + " was killed due to high memory consumption.\n"
                    return
            except psutil.NoSuchProcess:
                break
            time.sleep(0.1)  # limit checks to be executed 10 times per second
        return

    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('localhost', self.port))
        s.listen(1)
        connection = s.accept()[0]

        print 'Connection from port %d accepted!' % self.port

        proc = subprocess.Popen(self.cmd.split(' '), cwd=self.solution, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        threading.Thread(target=self.monitor, args=(proc.pid,)).start()  # monitor memory consumption
        self.write_pipe = proc.stdin
        self.read_pipe = proc.stdout

        try:
            while True:
                server_output = connection.recv(1024)
                print 'Incoming...', server_output
                if server_output != '\n':
                    if server_output == '$exit\n':
                        psutil.Process(proc.pid).kill()
                        break
                    self.write_pipe.write(server_output)

                server_input = self.read_pipe.readline()

                print 'Outgoing...', server_input
                connection.sendall(server_input)
        except Exception:
            print traceback.format_exc()
        finally:
            connection.close()
            s.close()

    def tear_down(self):
        cmd = 'rm -r ' + self.solution
        subprocess.Popen(cmd.split(' '))
