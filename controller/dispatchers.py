# -*- coding: utf-8 -*-
"""
Dispatchers are used to handle specific events.
"""
import logging

import buttons

logger = logging.getLogger(__name__)


class DispatcherManager(object):
    """Class that handles all dispatchers.

    Dispatcher instances can be attached to the dispatcher manager with a
    selector function. If the selector function returns ``True``, the
    dispatcher is called.

    """
    def __init__(self):
        self.dispatchers = []

    def attach(self, dispatcher, interest_function):
        self.dispatchers.append((dispatcher, interest_function))

    def dispatch(self, message):
        for dispatcher, interest_function in self.dispatchers:
            if interest_function(message) is True:
                dispatcher.dispatch(message)


class ButtonDispatcher(object):
    def __init__(self, screen):
        self.screen = screen

    def dispatch(self, message):
        logger.info("got message: {0} key: {1}".format(message, message.key))
        if message.key == buttons.MENU:
            logger.info('MENU')
        elif message.key == buttons.PLAY:
            logger.info('PLAY')
        elif message.key == buttons.NEXT:
            logger.info('NEXT')
        elif message.key == buttons.PREVIOUS:
            logger.info('PREVIOUS')
        elif message.key == buttons.ROTARY:
            logger.info('ROTARY')
            self.screen.enter()


class RefreshDispatcher(object):
    def __init__(self, screen):
        self.screen = screen

    def dispatch(self, message):
        logger.info("refreshing screen")
        self.screen.draw()
