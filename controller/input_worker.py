# -*- coding: utf-8 -*-
"""
A worker thread that listens for user input via keyboard.
This is only used for debugging purposes.
"""

import logging
import struct

from messages import ButtonInputMessage, RotaryInputMessage
from events import event_queue
from message_types import ROTARY_INPUT, BUTTON_INPUT

logger = logging.getLogger(__name__)


def process_frame(message_type, data):
    """Port represents the device, from which frames are read. Has to prive read(), read(num) methods"""

    logger.info("frame received")

    if message_type == BUTTON_INPUT:
        payload = struct.unpack("!" + "B" * len(data), data)
        event_queue.put(ButtonInputMessage(payload[0]))
    if message_type == ROTARY_INPUT:
        payload = struct.unpack("!" + "b" * len(data), data)
        event_queue.put(RotaryInputMessage(payload[0]))

    logger.info("Payload: {0}, Queue Size: {1}".format(payload[0], event_queue.qsize()))