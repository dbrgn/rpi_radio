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

from flask import Flask, url_for, redirect, render_template
import yaml

CONFIG = 'config.yml'

app = Flask(__name__)


### Views ###

@app.route('/')
def home():
    return redirect(url_for('dashboard'))


@app.route('/dashboard/')
def dashboard():
    return render_template('dashboard.html')


@app.route('/config/wlan/')
def config_wlan():
    return render_template('config_wlan.html')


@app.route('/config/radio/')
def config_radio():
    return render_template('config_radio.html')


@app.route('/config/alarm/')
def config_alarm():
    return render_template('config_alarm.html')


### Dev Server ###

if __name__ == '__main__':
    app.run()
