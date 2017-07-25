import socket
import sys

from time import sleep
from threading import Thread
import functools

HOST = 'localhost'


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


class Client:
    def __init__(self, Solution, port, user):
        self.sock = None
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.success = False
        self.hidden_connect()
        if self.success is True:
            self.user = user
            self.sock.sendall(self.user)
            self.sol = None
            self.create_solution(Solution)

    def create_solution(self, Solution):
        timed_function = timeout(time_limit=0.1)(Solution)
        try:
            self.sol = timed_function()
        except Exception as ex:
            self.sock.recv(1024).decode("utf-8")
            self.sock.sendall("None")
            print(ex)

    def hidden_connect(self):
        for x in xrange(30):  # 3s of trying should be enough
            try:
                self.sock.connect((HOST, self.port))
            except socket.error as e:
                self.sock.close()
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sleep(0.1)
                continue
            self.success = True
            break

    def hidden_main(self):
        for i in range(5):
            data = self.sock.recv(1024).decode("utf-8")
            if data != '$exit':
                result = None
                timed_function = timeout(time_limit=1)(self.put_ship)
                try:
                    result = timed_function(data)
                except Exception as ex:
                    print(ex)
                self.sock.sendall(result if result else "None")
            else:
                print("Kicked :(")
                sys.exit(0)

        data = self.sock.recv(1024).decode("utf-8")
        while data != '$exit':
            result = None
            timed_function = timeout(time_limit=1)(self.shoot)
            try:
                result = timed_function(data)
            except Exception as ex:
                print(ex)
            self.sock.sendall(result if result else "None")
            data = self.sock.recv(1024).decode("utf-8")

    @timeout(1)  # 1 second timeout
    def put_ship(self, server_command):
        return self.sol.put_ship(server_command)

    @timeout(1)  # 1 second timeout
    def shoot(self, server_command):
        return self.sol.shoot(server_command)
