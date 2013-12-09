# -*- coding: utf-8 -*-
"""
Main file, project entry point.
"""
import logging
from threading import Thread

import events
import screen
from dispatchers import DispatcherManager, ButtonDispatcher, RefreshDispatcher
from input_worker import process_input
from messages import ButtonInputMessage, RefreshMessage

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def shutdown():
    logger.info("shutdown")

# Initialize screen
first_screen = screen.ListScreen([
    (screen.DirScreen("/home/"), "/home/"),
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

# Use the following numbers to emulate button input:
# 3: exit to parent screen, 2: scroll up, 1: scroll down, 0: enter
input_worker = Thread(target=process_input)
input_worker.setDaemon(True)
input_worker.start()

# Main event loop
loop = events.EventLoop(dispatcher)
loop.run()
print '\nGoodbye.'
