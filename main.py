# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

import RPIO
from RPLCD import CharLCD

from functions import shutdown
from utils import clamp


# Pin configuration
NUMBERING_MODE = RPIO.BCM
PIN_LCD_RS = 10
PIN_LCD_RW = None
PIN_LCD_E = 7
PIN_LCD_DATA = [9, 25, 11, 8]
PIN_ROTARY_A = 2
PIN_ROTARY_B = 3

# Magic numbers
LCD_COLS = 20
LCD_ROWS = 4


def nop():
    pass


mainmenu = [
    ('Radio', nop),
    ('Shutdown', shutdown),
    ('Foo', nop),
    ('Bar', nop),
    ('Baz', nop),
]


class RotaryEncoder(object):
    def __init__(self, player):
        self.player = player
        RPIO.setup(PIN_ROTARY_B, RPIO.IN, pull_up_down=RPIO.PUD_UP, initial=RPIO.HIGH)
        RPIO.add_interrupt_callback(PIN_ROTARY_A, self.process_movement,
                edge='falling', pull_up_down=RPIO.PUD_UP,
                debounce_timeout_ms=15)

    def process_movement(self, gpio_id, value):
        pin_b = RPIO.input(PIN_ROTARY_B)
        if pin_b:  # Down
            self.player.menu_pos += 1
        else:  # Up
            self.player.menu_pos -= 1


class Player(object):
    def __init__(self, lcd):
        """Initialize hardware."""

        # LCD instance
        self.lcd = lcd

        # Position in menu
        self._menu_pos = 0

        # Load menu
        self.redraw()

    @property
    def menu_pos(self):
        return self._menu_pos

    @menu_pos.setter
    def menu_pos(self, value):
        newpos = clamp(value, 0, LCD_ROWS - 1)
        redraw_needed = self._menu_pos != newpos
        self._menu_pos = newpos
        if redraw_needed:
            self.redraw()

    def load_menu(self, menu, prefix='> ', selected='* '):
        self.lcd.clear()
        items = menu[:4]
        for i, (label, func) in enumerate(items):
            line = selected + label if i == self.menu_pos else prefix + label
            self.lcd.write_string(line[:LCD_COLS] + '\n\r')

    def redraw(self):
        self.load_menu(mainmenu)


if __name__ == '__main__':

    # Disable warnings
    RPIO.setwarnings(False)

    # Initialize LCD
    lcd = CharLCD(pin_rs=PIN_LCD_RS, pin_rw=PIN_LCD_RW, pin_e=PIN_LCD_E,
            pins_data=PIN_LCD_DATA, numbering_mode=NUMBERING_MODE)

    p = Player(lcd)
    r = RotaryEncoder(p)

    try:
        RPIO.wait_for_interrupts()
    except KeyboardInterrupt:
        print('Exiting...')
