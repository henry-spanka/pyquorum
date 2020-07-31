# -*- coding: utf-8 -*-

import pytest
from pyquorum.udpserver import UdpServer

__author__ = "Henry Spanka"
__copyright__ = "Henry Spanka"
__license__ = "mit"


def test_server(mocker, caplog):
    h = mocker.MagicMock()

    sock = mocker.patch("socket.socket.recvfrom")
    sock.return_value = (bytes("test", "utf-8"), ("127.0.0.2", 10000))

    s = UdpServer("127.0.0.1", 10000, h)
    s.listen(False)

    sock.assert_called_once()
    h.handle.assert_called_once()
