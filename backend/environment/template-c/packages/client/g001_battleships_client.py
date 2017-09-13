import json
import traceback

from copy import deepcopy

import sys

from client import Client, timeout
from ctypes import *

class BattleshipsClient(Client):
    def __init__(self, port, username, api, dllname):
        super(BattleshipsClient, self).__init__(port, username, api, dllname)
        self.sol_put = self.dll.put
        self.sol_shoot = self.dll.shoot
        self.sol_put.argtypes = [type(self.api.api), POINTER(c_char_p)]
        self.sol_shoot.argtypes = [type(self.api.api), POINTER(c_char_p)]

    def main(self):
        for i in range(5):
            data = self.sock.recv(1024).decode("utf-8")
            self.api.feed(json.loads(data))
            result = None
            timed_function = timeout(time_limit=1)(self.put)
            try:
                result = timed_function()
            except Exception as ex:
                print traceback.format_exc()
            self.sock.sendall(result if result else "None")

        while True:
            data = self.sock.recv(1024).decode("utf-8")
            self.api.feed(json.loads(data))
            result = None
            timed_function = timeout(time_limit=1)(self.shoot)
            try:
                result = timed_function()
            except Exception as ex:
                print(ex)
            self.sock.sendall(result if result else "None")


    @timeout(1)  # 1 second timeout
    def put(self):
        empty_string = c_char_p('')
        address = pointer(empty_string)
        self.sol_put(self.api.get_data(), address)
        return address.contents.value

    @timeout(1)  # 1 second timeout
    def shoot(self):
        empty_string = c_char_p('')
        address = pointer(empty_string)
        self.sol_shoot(self.api.get_data(), address)
        return address.contents.value