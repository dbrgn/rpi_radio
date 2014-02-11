import serial
import logging
import threading
from controller import input_worker

logger = logging.getLogger(__name__)


class SerialInputServer(object):
    def __init__(self, port):
        self.serial_port = serial.Serial(port, 9600)

    def run(self):
        logging.info("SerialInputServer started")
        while True:
            start_marker = self.serial_port.read()
            if start_marker is not 42:
                continue
            logging.info("start marker received")
            frame_type = self.serial_port.read()
            frame_length = self.serial_port.read()
            frame_payload = self.serial_port.read(frame_length)
            raw_frame = start_marker + frame_type + frame_length + frame_payload
            threading.Thread(target=input_worker.process_frame(raw_frame))



