# -*- coding: utf-8 -*-

from .handler import BaseHandler
import logging

import json

from .manager import QuorumManager
from .message import Message, MessageType

_logger = logging.getLogger(__name__)


class MessageReceiver(BaseHandler):
    """Handles incoming messages
    """

    def __init__(self, manager: QuorumManager):
        super().__init__()

        self.manager = manager

    def handle(self, ip: str, data: str):
        """Receives incoming messages

        Args:
            ip (str): IP address from which this message was received
            data (str): The data that was received
        """
        message = Message.fromJson(data)

        try:
            host = self.manager.getHost(ip)

            if message.type == MessageType.PING:
                self.manager.ping(host, message.data)
        except Exception:
            _logger.error("Could not handle message from {}".format(ip))
