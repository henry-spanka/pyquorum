# -*- coding: utf-8 -*-

import pytest
from pyquorum.manager import QuorumManager
from pyquorum.host import Host, HostStatus

__author__ = "Henry Spanka"
__copyright__ = "Henry Spanka"
__license__ = "mit"


def make_manager():
    return QuorumManager(Host("127.0.0.1", 10000), {}, None, None)


def make_manager_hosts():
    return QuorumManager(Host("127.0.0.1", 10000), {Host("127.0.0.2", 10000), Host("127.0.0.3", 10000)}, None, None)


def make_host():
    return Host("127.0.0.2", 10000)


def test_ping(mocker, caplog):
    m = make_manager()
    host = make_host()

    spy = mocker.spy(host, 'unpunish')
    m.ping(host, {'master': None, 'quorum': False})

    spy.assert_called_once()
    assert host.status == HostStatus.UP
    assert host.penalty == 0
    assert "Host 127.0.0.2 back online" in caplog.text


def test_ping_master(mocker, caplog):
    m = make_manager_hosts()
    host = m.getHost("127.0.0.2")

    m.ping(host, {'master': '127.0.0.2', 'quorum': False})
    assert host.status == HostStatus.UP
    assert m.master == host
    assert "Trying to join master 127.0.0.2" in caplog.text


def test_ping_master_quorum(mocker, caplog):
    m = make_manager_hosts()
    host = m.getHost("127.0.0.2")

    spy = mocker.spy(m, 'haveQuorum')

    m.ping(host, {'master': '127.0.0.2', 'quorum': True})
    assert host.status == HostStatus.UP
    assert m.master == host
    assert "Elected 127.0.0.2 as master" in caplog.text
    spy.assert_called_once()


def test_ping_master_no_quorum(mocker, caplog):
    m = make_manager_hosts()
    host = m.getHost("127.0.0.2")

    m.master = host

    spy = mocker.spy(m, 'haveQuorum')
    m.ping(host, {'master': '127.0.0.2', 'quorum': False})
    assert host.status == HostStatus.UP
    assert m.master == m.getHost("127.0.0.2")
    assert "Trying to join master 127.0.0.2" in caplog.text
    spy.assert_not_called()


def test_host_down(mocker, caplog):
    m = make_manager_hosts()
    host = m.getHost("127.0.0.2")

    spy = mocker.spy(m, 'lostQuorum')

    m.down(host)

    assert "Host 127.0.0.2 is down" in caplog.text
    spy.assert_not_called()


def test_master_down(mocker, caplog):
    m = make_manager_hosts()
    host = m.getHost("127.0.0.2")
    m.master = host

    spy = mocker.spy(m, 'lostQuorum')

    m.down(host)

    assert "Host 127.0.0.2 is down" in caplog.text
    spy.assert_called_once()


def test_invalid_host_exception():
    m = make_manager_hosts()
    with pytest.raises(Exception):
        m.getHost("255.255.255.255")


def test_keepalive(mocker):
    punish = mocker.patch('pyquorum.host.Host.punish')

    m = make_manager_hosts()

    m.client = mocker.MagicMock()
    m.client.send.return_value = True

    m.sendKeepAlives()

    for host in m.hosts:
        m.client.send.assert_called()
        punish.assert_not_called()


def test_keepalive_fail(mocker):
    punish = mocker.patch('pyquorum.host.Host.punish')
    m = make_manager_hosts()

    m.client = mocker.MagicMock()
    m.client.send.return_value = False

    m.sendKeepAlives()

    for host in m.hosts:
        m.client.send.assert_called()
        punish.assert_called()


def test_elect_master(mocker, caplog):
    m = make_manager_hosts()
    host1 = m.getHost("127.0.0.2")
    host2 = m.getHost("127.0.0.3")

    host1.status = HostStatus.UP
    host2.status = HostStatus.UP
    m.votes = set({host1, host2})
    m.master = m.local
    m.quorum = False

    stub = mocker.patch.object(m, 'haveQuorum')

    m.update()
    stub.assert_called_once()

    assert "Elected myself as new master with 3 of 3 votes" in caplog.text


def test_elect_master_2votes(mocker, caplog):
    m = make_manager_hosts()
    host1 = m.getHost("127.0.0.2")
    host2 = m.getHost("127.0.0.3")

    host1.status = HostStatus.UP
    host2.status = HostStatus.UP
    m.votes = set({host1})
    m.master = m.local
    m.quorum = False

    stub = mocker.patch.object(m, 'haveQuorum')

    m.update()
    stub.assert_called_once()

    assert "Elected myself as new master with 2 of 3 votes" in caplog.text
