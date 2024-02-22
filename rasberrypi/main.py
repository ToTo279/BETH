#!/usr/local/bin/python3.12
import os
import sys
import logging
import signal
import random
import time
from multiprocessing import Queue, Process, Array
from ctypes import c_bool

from connection.server import Server
from utils.config import MAX_NUMBER_OF_SATELLITES, TCP_IP, TCP_PORT

from gui import MainWindow, QApplication

def main():
    global server_process
    if check_arg(["-d", "--debug"]):
        try:
            logging.basicConfig(
                level=logging.DEBUG,
                handlers=[
                    logging.FileHandler("./logs/debug.log"),
                    logging.StreamHandler()
                ]
            )
            with open("./logs/debug.log", "a") as f:
                f.write("")
                f.write("")
            logging.debug("New debug session started at " + time.strftime("%d/%m/%Y %H:%M:%S"))
        except FileNotFoundError:
            os.mkdir("./logs")

    incoming_queues = [Queue() for _ in range(MAX_NUMBER_OF_SATELLITES)]
    outgoing_queues = [Queue() for _ in range(MAX_NUMBER_OF_SATELLITES)]

    satellites = Array(c_bool, [False for _ in range(MAX_NUMBER_OF_SATELLITES)])

    server_process = Process(target=Server, args=(TCP_IP, TCP_PORT, incoming_queues, outgoing_queues, satellites))
    server_process.start()

    # TODO: start GUI process

    app = QApplication(sys.argv)
    window = MainWindow(incoming_queues, outgoing_queues, satellites)
    # sys.exit(app.exec_())
    app.exec_()
    server_process.kill()


def check_arg(arg_check_for: list) -> bool:
    return any(arg in sys.argv for arg in arg_check_for)

if __name__ == "__main__":
    main()
