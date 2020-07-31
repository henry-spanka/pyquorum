# -*- coding: utf-8 -*-

import pytest
from pyquorum.runner import Runner

__author__ = "Henry Spanka"
__copyright__ = "Henry Spanka"
__license__ = "mit"


def test_empty_runner():
    r = Runner(None)
    assert r.running == False
    assert r.run() == True
    assert r.running == False


def test_script_runner():
    r = Runner("./test_runner.sh")
    assert r.run() == True
    assert r.running == True
    r.stop()
    assert r.running == False


def test_script_runner_not_exists():
    r = Runner("./some_script_that_doesnt_exist.sh")
    assert r.run() == False
    assert r.running == False
    r.stop()
    assert r.running == False
