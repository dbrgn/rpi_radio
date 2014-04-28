# -*- coding: utf-8 -*-
"""
Protocol to send events to the Raspberry Pi.
"""
from __future__ import print_function, division, absolute_import, unicode_literals

from flufl.enum import Enum


class Magic(Enum):
    start = 0x02
    stop = 0x03


class MessageType(Enum):
    rotary_input = 0x30
    button_input = 0x31
    analog = 0x32
    brightness = 0x33
    shutdown = 0x7f


class ButtonInput(Enum):
    select = 0x30
    menu = 0x31
    play = 0x32
    next = 0x33
    prev = 0x34
    power = 0x35


class RotaryInput(Enum):
    left = 0x2d
    right = 0x2b


class ButtonState(Enum):
    released = 0x30
    pressed = 0x31


def push_button(button, state):
    tpl = b'{start}{type}{button}{state}{stop}'
    return tpl.format(start=Magic.start.value, stop=Magic.stop.value,
                      type=MessageType.button_input.value,
                      button=button.value, state=state.value)


def rotate_encoder(direction, steps):
    tpl = b'{start}{type}{direction}{steps}{stop}'
    return tpl.format(start=Magic.start.value, stop=Magic.stop.value,
                      type=MessageType.rotary_input.value,
                      direction=direction.value, steps=steps)
