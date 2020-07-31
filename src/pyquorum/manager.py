# -*- coding: utf-8 -*-

import logging
from typing import List, Set

from .host import Host, HostStatus
from .udpclient import UdpClient

from .message import Message, MessageType

from .runner import Runner

import math

_logger = logging.getLogger(__name__)


class QuorumManager(object):
    """The manager is responsible for the master election process
    """

    def __init__(self, local: Host, hosts: List[Host], client: UdpClient, runner: Runner):
        """
        Args:
            local (Host): The local host where this instance of the manager runs
            hosts (List[Host]): Other hosts that are in the cluster
            client (UdpClient): client which can be used to send messages to other nodes
            runner (Runner): runner which runs an application on the master
        """
        super().__init__()

        self.local = local
        self.hosts = hosts
        self.client = client
        self.master = None
        self.quorum = False
        self.votes: Set[Host] = set()
        self.runner = runner

    def ping(self, host: Host, data):
        """Handles ping messages from other nodes

        Args:
            host (Host): Host which sent this message
            data ([type]): Payload of the ping message
        """
        _logger.debug("Received ping from {}".format(host.ip))

        if host.status == HostStatus.DOWN:
            _logger.warning("Host {} back online".format(host.ip))

        host.unpunish()

        if not self.quorum and data["master"] and data["master"] != self.local.ip:
            _logger.warning("Trying to join master {}".format(data["master"]))
            self.master = self.getHost(data["master"])

            if data["quorum"]:
                _logger.warning("Elected {} as master".format(data["master"]))
                self.haveQuorum()

        if data["master"] == self.local.ip:
            self.votes.add(host)
        else:
            try:
                self.votes.remove(host)
            except KeyError:
                pass

    def down(self, host: Host):
        """Called when a node leaves the cluster. Ensures that the majority of
        nodes are still online

        Args:
            host (Host): Host that left the cluster
        """
        _logger.warning("Host {} is down".format(host.ip))

        if self.master == host:
            self.lostQuorum()

    def sendKeepAlives(self):
        """Sends keepalive messages to all other nodes
        """
        for host in self.hosts:
            message = Message(MessageType.PING, {
                              'master': self.master.ip if self.master else None, 'quorum': self.quorum})

            if not self.client.send(host, message):
                host.punish()

    def getHost(self, ip: str) -> Host:
        """Get a specific host's object by ip address

        Args:
            ip (str): IP address of the host

        Raises:
            Exception: Raised if the host does not belong to the cluster

        Returns:
            Host: Returns the host object
        """
        for host in self.hosts:
            if host.ip == ip:
                return host

        raise Exception("Host not found")

    def aliveHosts(self) -> List[Host]:
        """Filter hosts which are reachable

        Returns:
            [Host]: Returns a list of reachable hosts
        """
        return [host for host in self.hosts if host.status == HostStatus.UP]

    def update(self):
        """Monitors that keepalive messages are received within a specific time frame
        and starts the master election process if quorum is lost
        """
        for host in self.hosts:
            _logger.info(host)

            # Punish host regularly.
            # keep alive messages will reset the penalty.
            if host.punish():
                self.down(host)

        # more than half of the nodes are reachable
        if len(self.aliveHosts()) + 1 > math.floor((len(self.hosts) + 1) / 2):
            if not self.quorum:
                _logger.warning("Trying to elect new master")

                lowest = True

                # find a reachable node with the lowest ip address
                for host in self.aliveHosts():
                    if QuorumManager.compareIp(host.ip, self.local.ip):
                        lowest = False
                        break

                # we should be master
                if lowest:
                    self.master = self.local

                # i am the proposed and I have more than half of the votes to be master
                if len(self.votes) + 1 > math.floor((len(self.hosts) + 1) / 2):
                    _logger.warning("Elected myself as new master with {} of {} votes".format(
                        len(self.votes) + 1, len(self.hosts) + 1))
                    self.haveQuorum()
        else:
            if self.quorum:
                # less than half of the nodes are online but we are still master
                self.lostQuorum()

    @staticmethod
    def compareIp(ip: str, ip2: str) -> bool:
        """Compares two IP addresses

        Args:
            ip (str): First ip
            ip2 (str): Second ip

        Returns:
            bool: Returns true if the first ip is lower than the second
        """
        return list(map(int, ip.split('.'))) < list(map(int, ip2.split('.')))

    def haveQuorum(self):
        """Once consensus is achieved the application will be run on the master
        """
        self.quorum = True
        _logger.warning("Have Quorum")
        if self.master == self.local:
            if not self.runner.run():
                _logger.warning(
                    "Could not run script. Check that it exists at the correct location and is executable")

    def lostQuorum(self):
        """When quorum is lost the application will be stopped on the master
        """
        self.master = None
        self.quorum = False
        self.votes = set()
        _logger.warning("Lost Quorum")
        if self.runner and self.runner.running:
            self.runner.stop()
