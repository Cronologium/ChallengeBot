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

    def make_environment(self, source, memory_limit, time_limit):
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
            env = PythonEnvironment(source=source, solution=self.env_root + random_string, memory_limit=memory_limit, time_limit=time_limit)
        #elif source.endswith('.cpp') or source.endswith('.cpp"'):
        #    env = CppEnvironment(source=source, solution=self.env_root + random_string, memory_limit=memory_limit, time_limit=time_limit)
        elif source.endswith('.c') or source.endswith('.c"'):
            env = CEnvironment(source=source, solution=self.env_root + random_string, memory_limit=memory_limit, time_limit=time_limit)

        if env is not None:
            self.environments.append(env)
            env.build()
            return random_string
        return None

    def run(self, env_id):
        solution = self.env_root + env_id
        for environment in self.environments:
            if environment.solution == solution:
                environment.run()

    def interact(self, env_id, message):
        solution = self.env_root + env_id
        if message == '$exit':
            self.delete_environment(env_id)
            return None
        for environment in self.environments:
            if environment.solution == solution:
                return environment.interact(message)

    def delete_environment(self, env_id):
        solution = self.env_root + env_id
        marked = None
        for x in xrange(len(self.environments)):
            if self.environments[x].solution == solution:
                self.environments[x].tear_down()
                marked = x
        if marked:
            if len(self.environments) > 1:
                self.environments = self.environments[:marked] + self.environments[marked+1:]
            else:
                self.environments = []
