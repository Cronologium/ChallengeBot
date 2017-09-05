import sys
from client import Client, timeout

class BattleshipsClient(Client):
    def __init__(self, port, username, Solution, api):
        super(BattleshipsClient, self).__init__(port, username, Solution, api, ['put', 'shoot'])

    def main(self):
        for i in range(5):
            data = self.sock.recv(1024).decode("utf-8")
            if data != '$exit':
                self.api.feed(data)
                result = None
                timed_function = timeout(time_limit=1)(self.put)
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
            self.api.feed(data)
            result = None
            timed_function = timeout(time_limit=1)(self.shoot)
            try:
                result = timed_function(data)
            except Exception as ex:
                print(ex)
            self.sock.sendall(result if result else "None")
            data = self.sock.recv(1024).decode("utf-8")

    @timeout(1)  # 1 second timeout
    def put(self):
        return self.sol.put_ship(self.api.get_data())

    @timeout(1)  # 1 second timeout
    def shoot(self):
        return self.shoot(self.api.get_data())