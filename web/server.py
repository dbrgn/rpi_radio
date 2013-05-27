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

import socket

import yaml
import netifaces
from flask import Flask, g, request, flash, url_for, redirect, render_template
from werkzeug.exceptions import BadRequest

from utils import is_valid_ipv4

CONFIG = 'config.yml'

app = Flask(__name__)


### Config parsing ###

def get_config():
    """Open and parse config file."""
    with open(CONFIG, 'r') as configfile:
        return yaml.safe_load(configfile)


def write_config(data):
    """Open and write config file."""
    with open(CONFIG, 'w') as configfile:
        yaml.safe_dump(data, configfile)


@app.before_request
def before_request():
    g.config = get_config()


@app.context_processor
def add_ip_addr():
    addr = netifaces.ifaddresses('wlan0')
    if socket.AF_INET in addr:
        return {'ip': addr[socket.AF_INET][0]['addr']}
    elif socket.AF_INET6 in addr:
        return {'ip': addr[socket.AF_INET6][0]['addr']}


### Views ###

@app.route('/')
def home():
    return redirect(url_for('dashboard'))


@app.route('/dashboard/')
def dashboard():
    return render_template('dashboard.html')


@app.route('/config/wlan/', methods=['GET', 'POST'])
def config_wlan():
    error = False
    config = g.config.get('wlan')

    if request.method == 'POST':

        # Process and validate data
        connection_type = request.form.get('type')
        if connection_type == 'dhcp':
            config = {'type': 'dhcp'}
        elif connection_type == 'static':
            config = {
                'type': 'static',
                'ip': request.form.get('ip'),
                'netmask': request.form.get('netmask'),
                'gateway': request.form.get('gateway'),
            }
            if not is_valid_ipv4(config['ip']):
                flash('Ungültige IP Adresse.', 'error')
                error = True
            if not is_valid_ipv4(config['netmask']):
                flash('Ungültige Netzmaske.', 'error')
                error = True
            if not is_valid_ipv4(config['gateway']):
                flash('Ungültiger Standardgateway.', 'error')
                error = True
        else:
            raise BadRequest('Invalid connection type.')

        # Persist data if no errors occured
        if not error:
            g.config['wlan'] = config
            write_config(g.config)
            flash('Konfiguration erfolgreich gespeichert.', 'success')
            config = get_config()['wlan']  # Refresh config to make sure everything worked

    return render_template('config_wlan.html', config=config)


@app.route('/config/radio/', methods=['GET', 'POST'])
def config_radio():
    return render_template('config_radio.html', config=g.config.get('radio'))


@app.route('/config/alarm/', methods=['GET', 'POST'])
def config_alarm():
    return render_template('config_alarm.html', config=g.config.get('alarm'))


### Dev Server ###

if __name__ == '__main__':
    app.secret_key = 'DEBUG-TODO'
    app.run(debug=True)
