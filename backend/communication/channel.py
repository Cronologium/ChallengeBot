import Queue
from threading import Thread


class Channel:
    def __init__(self, conn, timeout):
        self.conn = conn
        self.timeout = timeout

    @staticmethod
    def receive_message(conn, q):
        message = conn.recv(1024)
        q.put(message)

    def get_message(self):
        q = Queue.Queue()
        t = Thread(target=Channel.receive_message, args=(self.conn, q))
        t.start()
        t.join(self.timeout)
        if q.empty():
            return None
        return q.get()

    def send_message(self, message):
        self.conn.sendall(message)
        return

    def close(self):
        self.conn.close()
        self.conn = None

