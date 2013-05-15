# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

import contextlib


def clamp(value, minval, maxval):
    """Clamps an integer into the specified range.
    
    If it's larger than ``maxval``, the function will return ``maxval``. If
    it's smaller than ``minval``, the function will return ``minval``.
    Otherwise, the original integer will be returned.

    Args:
        value:
            The integer to clamp.
        minval:
            The minimum value.
        maxval:
            The maximum value.

    Returns:
        Integer that is between ``minval`` and ``maxval``.

    """
    return sorted((minval, int(value), maxval))[1]


@contextlib.contextmanager
def ignored(*exceptions):
    """Context manager that ignores all of the specified exceptions. This will
    be in the standard library starting with Python 3.4."""
    try:
        yield
    except exceptions:
        pass


class Observable(object):
    def __init__(self):
        self._observers = []

    def add_observer(self, observer):
        if not observer in self._observers:
            self._observers.append(observer)

    def remove_observer(self, observer):
        try:
            self._observers.remove(observer)
        except ValueError:
            pass

    def notify_observers(self):
        for observer in self._observers:
            observer.update()