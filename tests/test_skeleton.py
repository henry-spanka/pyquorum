# -*- coding: utf-8 -*-

import pytest
from pyqourum.skeleton import fib

__author__ = "Henry Spanka"
__copyright__ = "Henry Spanka"
__license__ = "mit"


def test_fib():
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(7) == 13
    with pytest.raises(AssertionError):
        fib(-10)
