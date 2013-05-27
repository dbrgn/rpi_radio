# -*- coding: utf-8 -*-
"""
Web-Frontend for RPI Radio.

Configuration variables:

- WLAN Configuration
    - DHCP or static
    - IP
    - Subnet mask
    - Gateway
- Radio stations
    - Name
    - URL
- Alarm clock
    - Multiple alarms
    - Wakeup time
    - Alarm sound
    - Snooze time?

"""
from __future__ import print_function, division, absolute_import, unicode_literals

from contextlib import closing

from flask import Flask, render_template
import yaml

CONFIG = 'config.yml'

app = Flask(__name__)


### Views ###

@app.route("/")
def home():
    return render_template('home.html')


### Dev Server ###

if __name__ == '__main__':
    app.run()