import Queue
import socket
from threading import Thread


class Channel:
    def __init__(self, port, timeout):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(('localhost', port))
        self.timeout = timeout

    @staticmethod
    def receive_message(sock, q):
        message = sock.recv(1024)
        q.put(message)

    def get_message(self):
        q = Queue.Queue()
        t = Thread(target=Channel.receive_message, args=(self.socket, q))
        t.start()
        t.join(self.timeout)
        if q.empty():
            return None
        return q.get()

    def send_message(self, message):
        self.socket.sendall(message)

    def close(self):
        self.socket.close()
        self.socket = None