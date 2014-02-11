# -*- coding: utf-8 -*-
"""
Protocol to send events to the Raspberry Pi.
"""
from __future__ import print_function, division, absolute_import, unicode_literals

from flufl.enum import Enum


class Magic(Enum):
    start = 42


class MessageType(Enum):
    button_input = 0
    rotary_input = 1


class ButtonInput(Enum):
    menu = 0
    play = 1
    next = 2
    prev = 3
