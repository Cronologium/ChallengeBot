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

        proc = None

        elf_name = self.source[:-2] + '.elf'
        if not os.path.isfile(elf_name):
            obj_name = self.source[:-2] + '.o'

            cmd = ['gcc', '-c', '-fPIC', self.source , '-o', obj_name]
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
            out, err = proc.communicate()
            if err:
                raise RuntimeError("Compilation failed for " + self.source + "\n" + err)

            cmd = ['gcc', '-o', elf_name, '-fPIC', obj_name]
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
            out, err = proc.communicate()
            if err:
                raise RuntimeError("Linking error for " + self.source + "\n" + err)

            os.remove(obj_name)

        cmd = ['cp', elf_name, os.path.join(self.solution, 'solution')]
        proc = subprocess.Popen(cmd, stdout=DEVNULL)
        proc.wait()


    def run(self):
        cmd = './solution'
        self.netcat_run(cmd)

