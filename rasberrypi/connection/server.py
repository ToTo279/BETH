import sys
import logging
import time
import socket
import signal
from typing import Union
from multiprocessing import Queue, Array
from threading import Thread

from connection.satellite_connection import SatelliteConnection
from utils.config import BUFFER_SIZE, MAX_NUMBER_OF_SATELLITES
from utils.helpers import json_decode, json_encode

root = logging.getLogger()
root.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)

class Server:
    def __init__(self, host: str, port: int, incoming_queues: list[Queue], outgoing_queues: list[Queue], satellite_arr: Array):
        signal.signal(signal.SIGINT, self.shutdown_server)
        logging.info(f"Server started on {host}:{port}")
        
        if not host or not port:
            raise ValueError("Host and port must be specified")
        
        if not incoming_queues or not outgoing_queues or len(incoming_queues+outgoing_queues) != 2*MAX_NUMBER_OF_SATELLITES:
            raise ValueError(f"Queue must be specified and have length of {2*MAX_NUMBER_OF_SATELLITES}")
        
        self.server_closed = False
        self.host = host
        self.port = port
        self.satellites: list[Union[SatelliteConnection, None]] = [None for _ in range(MAX_NUMBER_OF_SATELLITES)]
        
        self.incoming_queue = incoming_queues
        self.outgoing_queue = outgoing_queues
        self.satellites_arr = satellite_arr
        
        self.threads: list[Thread] = []
        
        self.current_connection = 0
        
        self.start_server()
        self.run()
        
    def shutdown_server(self, sig, frame):
        logging.info("Shutting down server")
        for sat in self.satellites:
            if sat:
                sat.close()
        self.server_closed = True
        self.socket.close()
        sys.exit(0)
        
    def start_server(self):
        self.socket = socket.socket()
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # TODO: remove this in production
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        self.socket.setsockopt(socket.SOL_TCP, socket.TCP_KEEPIDLE, 1)
        self.socket.setsockopt(socket.SOL_TCP, socket.TCP_KEEPINTVL, 1)
        self.socket.setsockopt(socket.SOL_TCP, socket.TCP_KEEPCNT, 3)
        self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.socket.setblocking(True)
        self.socket.bind((self.host, self.port))
        self.socket.listen(MAX_NUMBER_OF_SATELLITES)
        
    def run(self):
        monitor_thread = Thread(target=self.monitor_connections)
        monitor_thread.start()
        while not self.server_closed:
            if self.current_connection < MAX_NUMBER_OF_SATELLITES:        
                self.accept_connections()
            
    def accept_connections(self):
        conn, addr = self.socket.accept()
        time.sleep(0.01)
        # read id
        logging.info(f"New connection from {addr}")
        data = conn.recv(BUFFER_SIZE).decode('utf-8')
        if not data:
            logging.warning(f"Connection with {addr} lost")

        if data == "":
            return
        
        additional_msgs = []
        data = data.rstrip()
         
        if data.count('\r\n') > 0:
            data_arr = data.split('\r\n')
            data_arr = [line for line in data_arr if line.strip()]
            for msg in data_arr:
                if '"id"' in msg:
                    data = msg
                else:
                    additional_msgs.append(msg)

        data = json_decode(data)
        satellite_id = data.get('id', None)
        satelitte_battery = data.get('battery_status', 50)
        battery_message = {
            'command': 'satellite_status',
            'arg1': satelitte_battery
        }
        additional_msgs.append(json_encode(battery_message))

        for msg in additional_msgs:
            self.outgoing_queue[satellite_id].put_nowait(msg)
        
        logging.debug(f"Received id: {satellite_id}")
        new_sat = SatelliteConnection(conn, addr, self.incoming_queue[satellite_id], self.outgoing_queue[satellite_id])
        self.satellites_arr[satellite_id] = True
        new_sat.send('{\"result\":\"connected\"}')
        
        sender_thread = Thread(target=new_sat.send_worker, daemon=True)
        receiver_thread = Thread(target=new_sat.receive_worker, daemon=True)
        sender_thread.start()
        receiver_thread.start()
        self.threads.append(sender_thread)
        self.threads.append(receiver_thread)
        
        self.satellites[satellite_id] = new_sat
        self.current_connection += 1
        
    def monitor_connections(self):
        while True:
            for i, sat in enumerate(self.satellites):
                if sat and not sat.is_alive():
                    self.clear_queues(i)
                    self.satellites[i] = None
                    self.current_connection -= 1
                    self.satellites_arr[i] = False
                    logging.info(f"Connection with {sat.addr} lost")
            time.sleep(0.01)
            
    def clear_queues(self, index: int):
        try:
            while not self.incoming_queue[index].empty():
                self.incoming_queue[index].get()
            while not self.outgoing_queue[index].empty():
                self.outgoing_queue[index].get()
        except:
            pass