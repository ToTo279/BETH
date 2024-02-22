from multiprocessing import Queue
from socket import socket
import queue
import logging

from utils.config import BUFFER_SIZE
from utils.helpers import is_json


class SatelliteConnection:
    def __init__(self, connection: socket, addr: tuple, incoming_queue: Queue, outgoing_queue: Queue):
        self.conn = connection
        self.addr = addr
        self.id = ""
        self.incoming_queue = incoming_queue
        self.outgoing_queue = outgoing_queue
        self._is_alive = True
        
    def send(self, data: str):
        if not data or not self.is_alive() or is_json(data) == False:
            return
        try:
            self.conn.send(data.encode('utf-8'))
        except (BrokenPipeError, ConnectionResetError):
            self._is_alive = False
            self.close()
        
    def receive(self):
        try:
            return self.conn.recv(BUFFER_SIZE).decode('utf-8')
        except OSError as e:
            if e.errno == 9:
                self._is_alive = False
                self.close()
            else:
                raise e
    
    def close(self):
        self.conn.close()
        
    def is_alive(self):
        return self._is_alive
    
    def receive_worker(self):
        while self.is_alive():
            try:
                data = self.receive()
            except (TimeoutError, ConnectionResetError):
                self._is_alive = False
                self.close()
                break

            if not data:
                self._is_alive = False
                self.close()
                break
            if data == "" or data == "\r\n" or data == "\0":
                continue
            data = data.strip().replace("\n", "").replace("\r", "").replace("\t", "")
            self.outgoing_queue.put(data)
    
    def send_worker(self):
        while self.is_alive():
            try:
                data = self.incoming_queue.get(timeout=0.3)
            except queue.Empty:
                continue
            if not data or is_json(data) == False:
                continue
            self.send(data)
            