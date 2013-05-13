# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

import time

import RPIO

import settings
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
PIN_ROTARY_BTN = 24

# Magic numbers
LCD_COLS = 20
LCD_ROWS = 4


def nop(*args):
    pass


mainmenu = [
    ('Radio', nop),
    ('Shutdown', shutdown),
    ('Foo', nop),
    ('Bar', nop),
    ('Baz', nop),
]

submenu = [
    ('Sub1', nop),
    ('Sub2', nop),
]


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
            observer.update(self)


class MenuScreen(Observable):
    """Represents a List with menu entries"""

    def __init__(self, previous, menulist):
        super(MenuScreen, self).__init__()
        self.previous = previous
        self.menulist = menulist
        self._menu_pos = 0

    @property
    def menu_pos(self):
        return self._menu_pos

    @menu_pos.setter
    def menu_pos(self, value):
        oldpos = self._menu_pos
        newpos = clamp(value, 0, LCD_ROWS - 1)
        self._menu_pos = newpos
        if oldpos != newpos:
            print("notifying observers")
            self.notify_observers()
            """self.lcd.cursor_pos = (oldpos, 0)
            self.lcd.write_string(self.menu_prefix)
            self.lcd.cursor_pos = (newpos, 0)
            self.lcd.write_string(self.menu_selected)"""

    def redraw(self):
        print("Redrawing MenuScreen: ", id(self))
        pass


class RotaryEncoder(object):
    def __init__(self, player):
        self.player = player
        RPIO.setup(settings.ROTARY_PIN_B, RPIO.IN, pull_up_down=RPIO.PUD_UP, initial=RPIO.HIGH)
        RPIO.add_interrupt_callback(settings.ROTARY_PIN_A, self.process_movement,
                                    edge='falling', pull_up_down=RPIO.PUD_UP,
                                    debounce_timeout_ms=15)
        RPIO.add_interrupt_callback(settings.ROTARY_PIN_BUTTON, self.button_pressed,
                                    edge='falling', pull_up_down=RPIO.PUD_UP,
                                    debounce_timeout_ms=15)

    def process_movement(self, gpio_id, value):
        pin_b = RPIO.input(settings.ROTARY_PIN_B)
        if pin_b:  # Down
            self.player.scroll_down()
        else:  # Up
            self.player.scroll_up()

    def button_pressed(self, gpio_id, value):
        self.player.run_action()


class Player(object):
    def __init__(self, lcd, menu_prefix='> ', menu_selected='* '):
        """Initialize hardware."""

        # LCD instance
        self.lcd = lcd

        self.current_menu = MenuScreen(previous=None, menulist=mainmenu)
        self.current_menu.add_observer(self)

        # Position in menu
        self.menu_prefix = menu_prefix
        self.menu_selected = menu_selected
        #self._menu_pos = 0

        # Loading animation
        self.welcome()

        # Load menu
        self.redraw()

    def welcome(self):
        """Draw a loading screen."""
        lcd.clear()
        lcd.write_string('Welcome to\n\rRaspberry Pi Radio!')
        lcd.cursor_pos = (3, 0)
        lcd.write(0)
        lcd.write(0)
        time.sleep(0.5)
        for i in xrange(2, 20, 2):
            lcd.write(0)
            lcd.write(0)
            time.sleep(0.1)

    def update(self):
        self.redraw()

    def load_menu(self, menu):
        self.lcd.clear()
        self.current_menu.menulist = menu
        items = menu[:4]
        for i, (label, func) in enumerate(items):
            if i == self.current_menu.menu_pos:
                line = self.menu_selected + label
            else:
                line = self.menu_prefix + label
            self.lcd.write_string(line[:LCD_COLS] + '\n\r')

    def redraw(self):
        self.load_menu(self.current_menu.menulist)

    def run_action(self):
        item = self.current_menu[self.menu_pos]
        function = item[-1]
        function(self.lcd)

    def scroll_up(self):
        self.current_menu.menu_pos -= 1

    def scroll_down(self):
        self.current_menu.menu_pos += 1


if __name__ == '__main__':

    # Disable warnings
    RPIO.setwarnings(False)

    # Initialize LCD
    data_bus = [settings.DISPLAY_PIN_DB1, settings.DISPLAY_PIN_DB2, settings.DISPLAY_PIN_DB3, settings.DISPLAY_PIN_DB4]
    lcd = CharLCD(pin_rs=settings.DISPLAY_PIN_RS, pin_rw=settings.DISPLAY_PIN_RW, pin_e=settings.DISPLAY_PIN_E,
                  pins_data=data_bus, numbering_mode=NUMBERING_MODE)

    p = Player(lcd)
    r = RotaryEncoder(p)

    try:
        RPIO.wait_for_interrupts()
    except KeyboardInterrupt:
        print('Exiting...')

    lcd.clear()
    lcd.write_string('Goodbye!')
