# -*- coding: utf-8 -*-

import logging
import socket

from .host import Host

from .message import Message

_logger = logging.getLogger(__name__)


class UdpClient(object):
    """UDP network client that sends messages across the network
    """

    def __init__(self, ip: str):
        """
        Args:
            ip (str): IP to listen to
        """
        super().__init__()

        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind((ip, 0))

    def send(self, host: Host, message: Message) -> bool:
        """Sends a message to the given host

        Args:
            host (Host): Host to send a message to
            message (Message): Message to send

        Returns:
            bool: Returns true if the message was sent. This does not mean that it reached the destination.
        """
        try:
            self.s.sendto(bytes(message.toJson(), "utf-8"),
                          (host.ip, host.port))
        except OSError:
            _logger.warning(
                "Failed to send healthcheck to {}:{}".format(host.ip, host.port))
            return False

        return True
