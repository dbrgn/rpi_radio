# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

from subprocess import call

def shutdown(lcd):
    lcd.clear()
    lcd.write_string('Goodbye.')
    call('sudo init 0', shell=True)
