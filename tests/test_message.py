# -*- coding: utf-8 -*-

import pytest
from pyquorum.message import Message, MessageType

__author__ = "Henry Spanka"
__copyright__ = "Henry Spanka"
__license__ = "mit"


def test_ping_message_to_json():
    m = Message(MessageType.PING, {'master': '127.0.0.1', 'quorum': False})
    assert m.toJson(
    ) == "{\"type\": 1, \"data\": \"{\\\"master\\\": \\\"127.0.0.1\\\", \\\"quorum\\\": false}\"}"

    m = Message(MessageType.PING, {'master': '127.0.0.1', 'quorum': True})
    assert m.toJson(
    ) == "{\"type\": 1, \"data\": \"{\\\"master\\\": \\\"127.0.0.1\\\", \\\"quorum\\\": true}\"}"

    m = Message(MessageType.PING, {'master': None, 'quorum': False})
    assert m.toJson(
    ) == "{\"type\": 1, \"data\": \"{\\\"master\\\": null, \\\"quorum\\\": false}\"}"


def test_ping_message_from_json():
    m = Message.fromJson(
        "{\"type\": 1, \"data\": \"{\\\"master\\\": \\\"127.0.0.1\\\", \\\"quorum\\\": false}\"}")

    assert m.type == MessageType.PING
    assert m.data == {'master': '127.0.0.1', 'quorum': False}

    m = Message.fromJson(
        "{\"type\": 1, \"data\": \"{\\\"master\\\": \\\"127.0.0.1\\\", \\\"quorum\\\": true}\"}")

    assert m.type == MessageType.PING
    assert m.data == {'master': '127.0.0.1', 'quorum': True}

    m = Message.fromJson(
        "{\"type\": 1, \"data\": \"{\\\"master\\\": null, \\\"quorum\\\": false}\"}")

    assert m.type == MessageType.PING
    assert m.data == {'master': None, 'quorum': False}
