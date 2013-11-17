from events import event_queue
from dispatchers import Dispatcher, ButtonDispatcher, RefreshDispatcher
from input_worker import process_input
from messages import ButtonInputMessage, RefreshMessage
from threading import Thread
import screen
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def shutdown():
    logger.info("shutdown")

#Initialize screen
first_screen = screen.ListScreen([
    (screen.DirScreen("C:/"), "C:/"),
    (screen.TextScreen("Configscreen"), "Configuration"),
    (screen.ActionScreen("Shutdown screen", shutdown), "Shutdown screen"),
    (screen.TimeScreen(), "Time"),
])

screen_manager = screen.ScreenManager(first_screen)

#Initialize dispatchers
button_dispatcher = ButtonDispatcher(screen_manager)
refresh_dispatcher = RefreshDispatcher(screen_manager)

#Attach dispatchers
dispatcher = Dispatcher()
dispatcher.attach(button_dispatcher, lambda m: isinstance(m, ButtonInputMessage))
dispatcher.attach(refresh_dispatcher, lambda m: isinstance(m, RefreshMessage))

"""
use the following numbers to emulate button input:
 3: exit to parent screen, 2: scroll up, 1: scroll down, 0: enter
"""
input_worker = Thread(target=process_input)
input_worker.start()

#Main loop: dispatching event queue
while True:
    logging.info("waiting for message. events in queue: {0}".format(event_queue.qsize()))
    message = event_queue.get()
    logging.info("dispatching message {0}".format(message))
    dispatcher.dispatch(message)
