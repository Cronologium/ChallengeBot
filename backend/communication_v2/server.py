import Queue
import socket
from threading import Thread

from backend.communication.channel import Channel


class Server:
    def __init__(self):
        self.channels = {}
        self.in_use = False

    def connect(self, name, port, timeout):
        self.channels[name] = Channel(port, timeout)

    def cleanup(self):
        for channel_name in self.channels:
            self.close_channel(channel_name)

    def send_and_receive(self, player_name, message):
        if message is None:
            message = ''
        self.send_message(player_name, message)
        return self.channels[player_name].get_message()

    def send_message(self, player_name, message):
        if message != '':
            self.channels[player_name].send_message(message + '\n')

    def close_channel(self, player_name):
        self.channels[player_name].close()
        del self.channels[player_name]