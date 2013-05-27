# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

import socket


def is_valid_ipv4(address):
    try:
        socket.inet_pton(socket.AF_INET, address)
    except AttributeError:  # no inet_pton here, sorry
        try:
            socket.inet_aton(address)
        except (socket.error, TypeError):
            return False
        return address.count('.') == 3
    except (socket.error, TypeError):  # not a valid address
        return False
    return True


def is_valid_ipv6(address):
    try:
        socket.inet_pton(socket.AF_INET6, address)
    except (socket.error, TypeError):  # not a valid address
        return False
    return True
