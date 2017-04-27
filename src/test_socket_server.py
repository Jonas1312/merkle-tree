#!/usr/bin/env python
# coding:utf-8
"""
  Purpose:  Test socket server
  Created:  27/04/2017
"""

from socket_client_server import Server


def main():
    server = Server()
    msg = None
    try:
        while msg != b'':
            msg = server.receive()
            print(msg)
    finally:
        server.close()


if __name__ == "__main__":
    main()
