import Queue
import socket
from threading import Thread


class Server:
    def __init__(self, port):
        self.port = port
        self.socket = None
        self.channels = {}
        self.in_use = False

    def start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('localhost', self.port))
        self.socket.listen(5)

    def cleanup(self):
        for channel_name in self.channels:
            self.close_channel(channel_name)

    def end(self):
        self.socket.close()

    def bind_channel(self, player_name, channel):
        self.channels[player_name] = channel

    @staticmethod
    def receive_message(conn, q):
        message = conn.recv(1024)
        q.put(message)

    def get_message(self, connection):
        q = Queue.Queue()
        t = Thread(target=Server.receive_message, args=(connection, q))
        t.start()
        t.join(1)
        if q.empty():
            return None
        return q.get()

    def send_and_receive(self, player_name, message):
        if message is None:
            message = ''
        self.channels[player_name].send_message(message)
        return self.channels[player_name].get_message()

    def send_message(self, player_name, message):
        self.channels[player_name].send_message(message)

    def get_blind_message(self):
        (conn, address) = self.socket.accept()
        return conn, self.get_message(conn)

    def close_channel(self, player_name):
        self.channels[player_name].close()
        del self.channels[player_name]

