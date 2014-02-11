# -*- coding: utf-8 -*-
"""
Everything related to the event queue.
"""
import logging
import Queue

logger = logging.getLogger(__name__)


# The main event queue instance.
event_queue = Queue.Queue()


class EventLoop(object):
    """The main event loop, used to dispatch events."""
    def __init__(self, dispatcher):
        """
        Args:
            dispatcher:
                The main dispatcher that can handle all the event types. It
                should provide a ``dispatch(message)`` method.

        """
        self.dispatcher = dispatcher

    def run(self):
        """
        Run event loop until interrupted.
        
        The call to ``run()`` is blocking, and can be interrupted using a
        ``KeyboardInterrupt`` exception (SIGINT / Ctrl+C).
        
        """
        while True:
            logging.info('Waiting for message. events in queue: {0}'.format(event_queue.qsize()))
            try:
                # hack: http://stackoverflow.com/q/212797/284318
                logging.debug("pre get")
                message = event_queue.get(timeout=1000)
                logging.debug("post get")
            except Queue.Empty:
                logging.debug("queue empty")
                pass
            except KeyboardInterrupt:
                return
            else:
                logging.info('Dispatching message {0!r}'.format(message))
                self.dispatcher.dispatch(message)
