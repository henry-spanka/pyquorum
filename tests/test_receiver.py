# -*- coding: utf-8 -*-

import pytest
from pyquorum.receiver import MessageReceiver
from pyquorum.message import Message, MessageType
from pyquorum.host import Host

__author__ = "Henry Spanka"
__copyright__ = "Henry Spanka"
__license__ = "mit"


def test_receiver(mocker, caplog):
    host = Host("127.0.0.2", 10000)
    m = mocker.MagicMock()
    m.getHost.return_value = host

    r = MessageReceiver(m)
    r.handle("127.0.0.2", Message(MessageType.PING, {
             'master': None, 'quorum': False}).toJson())

    m.getHost.assert_called_once()
    m.ping.assert_called_with(host, {'master': None, 'quorum': False})

    assert not caplog.text


def test_invalid_receiver(mocker, caplog):
    host = Host("127.0.0.2", 10000)
    m = mocker.MagicMock()
    m.getHost.side_effect = Exception

    r = MessageReceiver(m)
    r.handle("127.0.0.2", Message(MessageType.PING, {
             'master': None, 'quorum': False}).toJson())

    m.getHost.assert_called_once()
    m.ping.assert_not_called()

    assert "Could not handle message from 127.0.0.2" in caplog.text
