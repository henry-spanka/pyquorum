# -*- coding: utf-8 -*-
"""
This is the entry point for the pyquorum application.
"""

import argparse
import socket
import sys
import logging
import time
import signal

from .udpserver import UdpServer
from .udpclient import UdpClient
from .host import Host
from .receiver import MessageReceiver
from .manager import QuorumManager
from .runner import Runner

from pyquorum import __version__

__author__ = "Henry Spanka"
__copyright__ = "Henry Spanka"
__license__ = "mit"

_logger = logging.getLogger(__name__)


def parse_args(args):
    """Parse command line parameters

    Args:
      args ([str]): command line parameters as list of strings

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(
        description="PyQuorum is a simple leader election algorithm written in Python.")
    parser.add_argument(
        "--version",
        action="version",
        version="pyquorum {ver}".format(ver=__version__))
    parser.add_argument(
        dest="servers",
        nargs="+",
        help="IP Address of servers running the PyQuorum application",
        type=str,
        metavar="SERVER")
    parser.add_argument(
        "-b",
        "--bind",
        dest="bind",
        help="IP to bind to",
        type=str,
        default=socket.gethostname())
    parser.add_argument(
        "-p",
        "--port",
        dest="port",
        help="Port to connect/listen to",
        type=int,
        default=51621)
    parser.add_argument(
        "-s",
        "--script",
        dest="script",
        help="Script to run on Quorum",
        type=str,
        metavar="SCRIPT")
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO)
    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG)
    return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(level=loglevel, stream=sys.stdout,
                        format=logformat, datefmt="%Y-%m-%d %H:%M:%S")


def main(args):
    """Main entry point allowing external calls

    Args:
      args ([str]): command line parameter list
    """
    args = parse_args(args)
    setup_logging(args.loglevel)

    signal.signal(signal.SIGINT, exit_handler)
    signal.signal(signal.SIGTERM, exit_handler)

    hosts = [Host(s, args.port) for s in args.servers]

    client = UdpClient(args.bind)

    runner = Runner(args.script)

    manager = QuorumManager(Host(args.bind, args.port), hosts, client, runner)
    handler = MessageReceiver(manager)

    server = UdpServer(args.bind, args.port, handler)
    server.start()

    # Main loop which will periodically send keep alive messages to other nodes
    # and update the quorum manager
    while True:
        manager.sendKeepAlives()
        time.sleep(1)

        manager.update()


def run():
    """Entry point for console_scripts
    """
    main(sys.argv[1:])


def exit_handler(sig, frame):
    """Exit handler

    Args:
        sig (Signal): signal number
        frame (Frame): stack frame
    """
    _logger.info("Shutting down")

    sys.exit(0)


if __name__ == "__main__":
    run()
