# -*- coding: utf-8 -*-
"""
The message types that can be sent to the event loop.
"""


class ButtonInputMessage(object):
    """A button has been pressed."""

    def __init__(self, key):
        self.key = key


class RefreshMessage(object):
    """The screen should be refreshed."""
    pass


class RotaryInputMessage(object):
    """The rotary encoder has been rotated"""

    def __init__(self, steps):
        self.steps = steps