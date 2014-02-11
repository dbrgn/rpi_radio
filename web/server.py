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

import struct
import socket

import yaml
import netifaces
from werkzeug.exceptions import BadRequest
from flask import Flask, g, request, flash, url_for, redirect, render_template
from flask.ext.socketio import SocketIO, emit

import netinput
from utils import is_valid_ipv4

CONFIG = 'config.yml'

app = Flask(__name__)
app.secret_key = 'DEBUG-TODO'
socketio = SocketIO(app)


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
    else:
        return {'ip': 'Keine'}


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

        config['proto'] = request.form.get('proto')
        if config['proto'] is None:
            flash('Keinen Verschlüsselungs-Typ gewählt.')
            error = True
        config['ssid'] = request.form.get('ssid')
        config['bssid'] = request.form.get('bssid')
        config['password'] = request.form.get('password')
        config['key_mgmt'] = 'WPA-PSK'  # Only type currently supported
        if connection_type == 'dhcp':
            config['type'] = 'dhcp'
        elif connection_type == 'static':
            config.update({
                'type': 'static',
                'ip': request.form.get('ip'),
                'netmask': request.form.get('netmask'),
                'gateway': request.form.get('gateway'),
            })
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


@app.route('/simulator/', methods=['GET'])
def simulator():
    return render_template('simulator.html')


### SocketIO Endpoints ###

@socketio.on('button', namespace='/simulator')
def socketio_button(message):
    action = message.get('action')
    if not action:
        emit('error', {'reason': 'Action not provided.'})
        return

    if action in ['play', 'prev', 'next', 'menu']:
        msgtype = netinput.MessageType.button_input
        payload = netinput.ButtonInput[action]
        fmt = b'!BBBB'
    elif action in ['rotary-right', 'rotary-left']:
        msgtype = netinput.MessageType.rotary_input
        payload = 1 if action == 'rotary-right' else -1
        fmt = b'!BBBb'
    else:
        emit('error', {'reason': 'Unknown action.'})
        return

    msg = struct.pack(fmt, netinput.Magic.start, msgtype, 1, payload)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(msg, ('127.0.0.1', 4242))

    emit('success', {'action': action})


### Server ###

if __name__ == '__main__':
    socketio.run(app)
