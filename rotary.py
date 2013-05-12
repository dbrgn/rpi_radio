# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals
import time
import RPIO


PIN_A = 2
PIN_B = 3
RPIO.setmode(RPIO.BCM)


counter = 1
def callback(gpio_id, value):
    global counter
    pin_b = RPIO.input(PIN_B)
    direction = 'Right' if pin_b else 'Left'
    print('{}] Pin B: {} Direction: {}'.format(counter, pin_b, direction))
    counter += 1

RPIO.setup(PIN_A, RPIO.IN)
RPIO.setup(PIN_B, RPIO.IN)

RPIO.add_interrupt_callback(PIN_A, callback, edge='falling', debounce_timeout_ms=15)

try:
    print('Running...')
    RPIO.wait_for_interrupts()
except KeyboardInterrupt:
    print('exiting')
finally:
    print('cleaning up')
    RPIO.cleanup()
