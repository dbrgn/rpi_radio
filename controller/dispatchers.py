import buttons
import logging

logger = logging.getLogger(__name__)


class Dispatcher(object):
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
        if message.key == buttons.exit:
            self.screen.exit()
        elif message.key == buttons.up:
            self.screen.scrollup()
        elif message.key == buttons.down:
            self.screen.scrolldown()
        elif message.key == buttons.enter:
            self.screen.enter()


class RefreshDispatcher(object):
    def __init__(self, screen):
        self.screen = screen

    def dispatch(self, message):
        logger.info("refreshing screen")
        self.screen.draw()