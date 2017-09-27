import os
import random

#from environment_cpp import CppEnvironment
from environment_python import PythonEnvironment
from environment_c import CEnvironment


class EnvironmentManager:
    def __init__(self):
        self.environments = []
        self.dictionary = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-'
        self.env_root = os.path.join(os.getcwd(), 'backend', 'runners') + os.sep

    def make_environment(self, source, port, memory_limit):
        random_string = ''.join([self.dictionary[random.randint(0, len(self.dictionary) - 1)] for x in xrange(4)])
        found = False
        for environment in self.environments:
            if environment.solution == random_string:
                found = True
        while found:
            random_string = ''.join([self.dictionary[random.randint(0, len(self.dictionary) - 1)] for x in xrange(4)])
            found = False
            for environment in self.environments:
                if environment.solution == random_string:
                    found = True
        env = None
        if not os.path.isdir(self.env_root):
            os.mkdir(self.env_root)
        if source.endswith('.py'):
            env = PythonEnvironment(source=source, solution=self.env_root + random_string, port=port, memory_limit=memory_limit)
        #elif source.endswith('.cpp') or source.endswith('.cpp"'):
        #    env = CppEnvironment(source=source, solution=self.env_root + random_string, port=port, memory_limit=memory_limit)
        elif source.endswith('.c') or source.endswith('.c"'):
            env = CEnvironment(source=source, solution=self.env_root + random_string, port=port, memory_limit=memory_limit)

        if env is not None:
            self.environments.append(env)
            env.build()
            return env.solution
        return None

    def run(self, solution):
        for environment in self.environments:
            if environment.solution == solution:
                environment.run()

    def delete_environment(self, solution):
        for environment in self.environments:
            if environment.solution == solution:
                environment.tear_down()
