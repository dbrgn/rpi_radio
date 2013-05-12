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
