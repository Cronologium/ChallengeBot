import json
from client import Client, timeout
from ctypes import *

class XandoClient(Client):
    def __init__(self, port, username, api, dllname):
        super(XandoClient, self).__init__(port, username, api, dllname)
        self.sol_put = self.dll.put
        self.sol_put.argtypes = [type(self.api.api), POINTER(c_char_p)]

    def main(self):
        while True:
            data = self.sock.recv(1024).decode("utf-8")
            self.api.feed(json.loads(data))
            result = None
            timed_function = timeout(time_limit=1)(self.put)
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