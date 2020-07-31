# -*- coding: utf-8 -*-

import abc


class BaseHandler(abc.ABC):
    """Base Handler interface
    """
    @abc.abstractclassmethod
    def handle(self, ip: str, message: str):
        """Handle method called by the server

        Args:
            ip (str): IP Address of the client that sent the message
            message (str): the message sent
        """
        pass
