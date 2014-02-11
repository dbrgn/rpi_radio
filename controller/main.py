# -*- coding: utf-8 -*-
"""
Main file, project entry point.
"""
import logging
import threading
import socket
from os.path import expanduser

import events
import screen
from dispatchers import DispatcherManager, ButtonDispatcher, RefreshDispatcher
from input_reader import serialinputserver, socketinputserver
from messages import ButtonInputMessage, RefreshMessage

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def shutdown():
    logger.info("shutdown")

# Initialize screen
first_screen = screen.ListScreen([
    (screen.DirScreen(expanduser('~')), "Files"),
    (screen.TextScreen("Configscreen"), "Configuration"),
    (screen.ActionScreen("Shutdown screen", shutdown), "Shutdown screen"),
    (screen.TimeScreen(), "Time"),
])

screen_manager = screen.ScreenManager(first_screen)

# Initialize dispatchers
button_dispatcher = ButtonDispatcher(screen_manager)
refresh_dispatcher = RefreshDispatcher(screen_manager)

# Attach dispatchers
dispatcher = DispatcherManager()
dispatcher.attach(button_dispatcher, lambda m: isinstance(m, ButtonInputMessage))
dispatcher.attach(refresh_dispatcher, lambda m: isinstance(m, RefreshMessage))

# Start input workers
socket_input_worker = threading.Thread(target=socketinputserver.SocketInputServer(4242).run)
serial_input_worker = threading.Thread(target=serialinputserver.SerialInputServer("COM6").run)

socket_input_worker.setDaemon(True)
serial_input_worker.setDaemon(True)

socket_input_worker.start()
serial_input_worker.start()

# Main event loop
logger.info("enter main loop")
loop = events.EventLoop(dispatcher)
loop.run()
print '\nGoodbye.'
