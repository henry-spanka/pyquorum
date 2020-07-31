# -*- coding: utf-8 -*-

import logging
import socket
import threading

from .handler import BaseHandler

_logger = logging.getLogger(__name__)


class UdpServer(threading.Thread):
    """UDP servers that receives messages from the network
    """

    def __init__(self, bind: str, port: int, handler: BaseHandler):
        """
        Args:
            bind (str): IP address to bind to
            port (int): Port to bind to
            handler (BaseHandler): Handler to call when a message is received
        """
        super().__init__(daemon=True)
        self.bind = bind
        self.port = port
        self.handler = handler

    def run(self):
        """Run the server
        """
        self.listen()

    def listen(self, forever=True):
        """Start listening for messages

        Args:
            forever (bool, optional): Whether the server should listen indefinitely. Defaults to True.
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind((self.bind, self.port))

        while True:
            # accept connections from outside
            data, addr = s.recvfrom(1024)  # buffer size is 1024 bytes

            if data:
                self.handler.handle(addr[0], data.decode("utf-8"))
            else:
                _logger.warning("Received invalid data from {}".format(addr))

            if not forever:
                break
