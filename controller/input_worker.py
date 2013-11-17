import sys
import buttons
from events import event_queue
from messages import ButtonInputMessage, RefreshMessage


def process_input():
    while True:
        print "input: "
        input = sys.stdin.readline()
        if "3" in input:
            event_queue.put(ButtonInputMessage(buttons.exit))
        if "2" in input:
            event_queue.put(ButtonInputMessage(buttons.up))
        elif "1" in input:
            event_queue.put(ButtonInputMessage(buttons.down))
        elif "0" in input:
            event_queue.put(ButtonInputMessage(buttons.enter))
        elif "r" in input:
            event_queue.put(RefreshMessage())