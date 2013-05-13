# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

import time

import RPIO

import settings
from RPLCD import CharLCD

from menuscreen import MenuScreen

from functions import shutdown
from utils import clamp


# Pin configuration
NUMBERING_MODE = RPIO.BCM


def nop(*args):
    pass


# (Text, function, next MenuScreen)
submenu = [
    ('Station 1', nop, None),
    ('Hauraki', nop, None),
]

mainmenu = [
    ('Radio', nop, MenuScreen(previous=None, menulist=submenu)),
    ('Shutdown', shutdown, None),
    ('Foo', nop, None),
    ('Bar', nop, None),
    ('Baz', nop, None),
]


class MenuEntry(object):
    def __init__(self, action, menu_screen):
        self.action = action
        self.menu_screen = menu_screen


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

        RPIO.add_interrupt_callback(settings.BUTTON_PIN_BACK, self.button_back_pressed, edge='falling',
                                    pull_up_down=RPIO.PUD_UP,
                                    debounce_timeout_ms=15)

    def process_movement(self, gpio_id, value):
        pin_b = RPIO.input(settings.ROTARY_PIN_B)
        if pin_b:  # Down
            self.player.scroll_down()
        else:  # Up
            self.player.scroll_up()

    def button_pressed(self, gpio_id, value):
        self.player.run_action()

    def button_back_pressed(self, gpio_id, value):
        print("back button pressed")
        self.player.back()


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
        for i, (label, func, menulist) in enumerate(items):
            if i == self.current_menu.menu_pos:
                line = self.menu_selected + label
            else:
                line = self.menu_prefix + label
            self.lcd.write_string(line[:settings.LCD_COLS] + '\n\r')

    def redraw(self):
        self.load_menu(self.current_menu.menulist)

    def run_action(self):
        item = self.current_menu.menulist[self.current_menu.menu_pos]

        function = item[-2]
        function(self.lcd)
        new_menu = item[-1]
        if new_menu is not None:  # If a MenuScreen is registered
            self.current_menu.remove_observer(self)
            self.current_menu = item[-1]
            self.current_menu.add_observer(self)

        #Update Screen with submenu
        self.redraw()

    def scroll_up(self):
        self.current_menu.menu_pos -= 1

    def scroll_down(self):
        self.current_menu.menu_pos += 1

    def back(self):
        self.current_menu.remove_observer(self)
        if self.current_menu.previous is None:  #Already on the Root level
            self.current_menu = MenuScreen(previous=None, menulist=mainmenu)
        self.current_menu.add_observer(self)
        self.redraw()


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
