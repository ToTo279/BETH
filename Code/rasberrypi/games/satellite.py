from ctypes import c_bool
from enum import Enum
from multiprocessing import Array, Queue
from queue import Empty as EmptyQueue
from threading import Thread
from dataclasses import dataclass
from typing import Callable, List, Union
from utils.helpers import json_encode, json_decode
from time import sleep

@dataclass
class Message:
    command: str
    arg1: str = None
    arg2: str = None


class Incoming(Message):
    pass


class Outgoing(Message):
    pass


class Satellite:
    def __init__(self, id: int, incoming_queue: Queue, outgoing_queue: Queue, status_array: Array = None):
        self.id:int = id
        self.incoming_queue = incoming_queue
        self.outgoing_queue = outgoing_queue
        self.status_array = status_array

        self.history_size = 30
        self.history: List[Message] = []

        self.on_response: Callable[[int, Incoming], None] = None

        self.game_mode:str = None
        self.battery:str = None
        self.status:bool = False

        self.running = True
        self.thread = Thread(target=self.loop)
        self.thread.start()

    def send(self, command, arg1 = None, arg2 = None):
        data = {"command":command, "arg1":arg1, "arg2":arg2}
        self.history.append(Outgoing(**data))
        self.history = self.history[-self.history_size :]
        self.outgoing_queue.put_nowait(json_encode(data))

    def handle_data(self, data: Incoming):
        if data.command == "set_game":
            self.game_mode = data.arg1
        if data.command == "satellite_status":
            self.battery = data.arg1

            
    def last_cmd(self)->Message:
        return self.history[-1]

    def stop(self):
        self.running = False

    def loop(self):
        while self.running:
            if self.status_array:
                self.status = bool(self.status_array[:][self.id])
            try:
                data = self.incoming_queue.get(timeout=0.3)
            except EmptyQueue:
                continue
            if not data: continue
            if len(data) == 0: continue
            data = json_decode(data)
            data = Incoming(**data)
            self.history.append(data)
            self.history = self.history[-self.history_size :]
            self.handle_data(data)
            if self.on_response:
                self.on_response(self.id, data)

if __name__ == "__main__":
    command = "teste"
    arg1 = 10
    arg2 = None
    data = {"command":command, "arg1":arg1, "arg2":None}
    print(Outgoing(**data))