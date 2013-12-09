# -*- coding: utf-8 -*-
"""
A worker thread that listens for user input via keyboard.
This is only used for debugging purposes.
"""
import thread

import buttons
from events import event_queue
from messages import ButtonInputMessage, RefreshMessage


def process_input():
    def print_help():
        print 'Press one of the following keys:'
        print '  u: Up'
        print '  d: Down'
        print '  e: Enter'
        print '  m: Menu / Back'
        print '  r: Refresh'
        print '  q: Quit this test loop'
    print_help()
    while True:
        command = raw_input('input: ').strip()
        if command == 'u':
            event_queue.put(ButtonInputMessage(buttons.up))
        elif command == 'd':
            event_queue.put(ButtonInputMessage(buttons.down))
        elif command == 'e':
            event_queue.put(ButtonInputMessage(buttons.enter))
        elif command == 'm':
            event_queue.put(ButtonInputMessage(buttons.exit))
        elif command == 'r':
            event_queue.put(RefreshMessage())
        elif command == 'q':
            thread.interrupt_main()
        else:
            print_help()
