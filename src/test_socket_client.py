#!/usr/bin/env python
# coding:utf-8
"""
  Purpose:  Test socket client
  Created:  27/04/2017
"""

from socket_client_server import Client
from time import sleep


def main():
    client = Client()
    for i in range(5):
        client.send("Msg numero {}".format(i))
        sleep(1)
    client.close()


if __name__ == "__main__":
    main()
