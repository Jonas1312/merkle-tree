#!/usr/bin/env python
# coding:utf-8
"""
  Purpose:  Socket
  Created:  27/04/2017
"""

import socket


class Client:
    """Client class."""

    def __init__(self, host="localhost", port=12800):
        """Client object constructor."""
        self.sock = socket.socket()
        self.sock.connect((host, port))
        print("Client connected to {}:{}".format(host, port))

    def send(self, data):
        if type(data) is str:
            self.sock.sendall(data.encode())
        else:
            self.sock.sendall(data)

    def close(self):
        self.sock.close()
        print("Client closed")


class Server:
    """Server class."""

    def __init__(self, port=12800):
        """Server object constructor."""
        self.sock = socket.socket()
        self.sock.bind(('', port))
        self.sock.listen(5)
        self.client, self.address = self.sock.accept()
        print("Server connected to {}".format(self.address))

    def receive(self):
        return self.client.recv(2 ** 15)

    def close(self):
        self.client.close()
        self.sock.close()
        print("Server closed")
