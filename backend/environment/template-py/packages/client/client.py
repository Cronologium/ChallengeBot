import functools
import socket
from threading import Thread
from time import sleep

def timeout(time_limit):
    def deco(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            res = [Exception('function [%s] timeout [%s seconds] exceeded!' % (func.__name__, time_limit))]

            def new_func():
                try:
                    res[0] = func(*args, **kwargs)
                except Exception as e:
                    res[0] = e
            t = Thread(target=new_func)
            t.daemon = True
            try:
                t.start()
                t.join(time_limit)
            except Exception as je:
                print("error starting thread")
                raise je
            ret = res[0]
            if isinstance(ret, BaseException):
                raise ret
            return ret
        return wrapper
    return deco

class Client(object):
    def __init__(self, port, username, Solution, api, required_functions=[]):
        self.api = api
        self.required_functions = required_functions
        self.sock = None
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.success = False
        self._connect()
        if self.success is True:
            self.username = username
            self.sock.sendall(self.username)
            self.sol = None
            self._create_solution(Solution)

    def _create_solution(self, Solution):
        timed_function = timeout(time_limit=0.1)(Solution)
        try:
            self._check(Solution)
            self.sol = timed_function()
        except Exception as ex:
            self.sock.recv(1024).decode("utf-8")
            self.sock.sendall("None")
            print(ex)

    def _connect(self):
        for x in xrange(30):  # 3s of trying should be enough
            try:
                self.sock.connect(("localhost", self.port))
            except socket.error as e:
                self.sock.close()
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sleep(0.1)
                continue
            self.success = True
            break

    def _check(self, Class):
        pass

    def main(self):
        pass