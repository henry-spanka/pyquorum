# -*- coding: utf-8 -*-

from __future__ import annotations

from .handler import BaseHandler
import logging
from enum import Enum

import json

_logger = logging.getLogger(__name__)


class MessageType(Enum):
    """Enum of message types used in communication between nodes
    """
    PING = 1


class Message(object):
    """Represents a message sent to nodes
    """

    def __init__(self, t: MessageType, data):
        self.type = t
        self.data = data

    def toJson(self) -> str:
        """Converts a message to its json representation

        Returns:
            str: string representation of the message
        """
        return json.dumps({'type': self.type.value, 'data': json.dumps(self.data)})

    @staticmethod
    def fromJson(data: str) -> Message:
        """Converts a string to a message object

        Args:
            data (str): string representation of the message

        Returns:
            Message: converted message object
        """
        d = json.loads(data)

        return Message(MessageType(d["type"]), json.loads(d["data"]))
