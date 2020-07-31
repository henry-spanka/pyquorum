# -*- coding: utf-8 -*-

from enum import Enum
import logging

_logger = logging.getLogger(__name__)


class HostStatus(Enum):
    """Host Status interface
    """
    UP = 1
    DOWN = 2


class Host(object):
    """The Host object represents a node that runs pyquorum
    """

    def __init__(self, ip: str, port: int):
        """
        Args:
            ip (str): IP address of the node
            port (int): port of the node
        """
        super().__init__()
        self.ip = ip
        self.port = port
        self.penalty = 0
        self.status = HostStatus.DOWN

    def punish(self) -> bool:
        """Punishes a node and marks the host down if penalty > 2

        Returns:
            bool: returns true if the host was marked as down
        """
        self.penalty += 1

        if self.penalty == 3:
            self.status = HostStatus.DOWN
            return True

        return False

    def unpunish(self):
        """Unpunishes a host (marks it as up)
        """
        self.penalty = 0
        self.status = HostStatus.UP
