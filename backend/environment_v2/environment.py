import os
import subprocess
import threading
import time
import psutil
import sys

class Environment(object):
    def __init__(self, source, solution, port, memory_limit, id):
        self.source = source
        self.port = port
        self.solution = solution
        self.memory_limit = memory_limit
        self.id = id

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

    def netcat_run(self, cmd):
        pipe_file = os.path.join(self.solution, 'pipe')
        os.mkfifo(pipe_file)
        cmd = 'nc -l -p %d < %s | %s > %s' % (self.port, pipe_file, cmd, pipe_file)
        proc = subprocess.Popen(cmd.split(), cwd=self.solution, stdout=subprocess.PIPE)  # hide errors (we want this?)
        threading.Thread(target=self.monitor, args=(proc.pid,)).start()  # monitor memory consumption
        out, err = proc.communicate()
        rc = proc.returncode
        print '[Output]', out
        if err:
            print '[Error]', err
        print '[Return code]', rc

    def run(self):
        pass

    def tear_down(self):
        if "win" in sys.platform.lower():
            cmd = ['rd', '/S', '/Q', self.solution]
            subprocess.Popen(cmd, shell=True)
        else:
            cmd = 'rm -r ' + self.solution
            subprocess.Popen(cmd.split(' '))
