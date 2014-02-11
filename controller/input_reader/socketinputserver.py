import socket
import logging
import threading
import struct
from controller import input_worker

logger = logging.getLogger(__name__)


class SocketInputServer():
    def __init__(self, port):
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.port = port

    def run(self):
        try:
            self.serversocket.bind(("0.0.0.0", self.port))
            logger.info("SocketInputServer started")

            while 1:
                data, address = self.serversocket.recvfrom(257)
                logger.info("Network connection opened to {0!r} ".format(address))
                logger.info("payload: {0!r}".format(data))
                start_marker = data[0]
                if ord(start_marker) != 42:
                    continue

                message_type, message_length = struct.unpack("!BB", data[1:3])
                payload = data[3:message_length + 3]
                threading.Thread(target=input_worker.process_frame(message_type, payload))

        finally:
            self.serversocket.close()