import json
from client import Client, timeout

class BattleshipsClient(Client):
    def __init__(self, port, username, Solution, api):
        super(BattleshipsClient, self).__init__(port, username, Solution, api, ['put', 'shoot'])

    def main(self):
        for i in range(5):
            data = self.sock.recv(1024).decode("utf-8")
            self.api.feed(json.loads(data))
            result = None
            timed_function = timeout(time_limit=1)(self.put)
            try:
                result = timed_function()
            except Exception as ex:
                print(ex)
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
        return self.sol.put(self.api.get_data())

    @timeout(1)  # 1 second timeout
    def shoot(self):
        return self.sol.shoot(self.api.get_data())