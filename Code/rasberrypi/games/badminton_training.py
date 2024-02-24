import logging
import time
import random
from typing import Callable

from games import Game, GameHistory, GameStatus, GameMode
from games.satellite import Satellite, Incoming, Outgoing
from utils.helpers import json_decode
from utils.config import RED, GREEN, BLUE, YELLOW, LIGHT_BLUE, PINK, WHITE

# TODO: Make configurable
TIMEOUT = 10.0



class SpeedTraining(Game):
    """Badminton speed training game
    Your goal in this game is to reach the specified number of satelites as fast as possible
    
    """

    def __init__(self, satellites: list[Satellite], total_turn_count: int = 10):
        self.satellites = [i for i in satellites if i.status]
        self._status = GameStatus.NOT_STARTED
        self._history = GameHistory()
        self.total_turn_count = total_turn_count
        self.current_turn = 0
        for sat in self.satellites:
            sat.on_response = self.on_response
        self.update_interface:Callable = None
        self.cancelled = False

    def __str__(self):
        return "Badminton speed training game"

    def start(self):
        colors = [RED, GREEN, BLUE, YELLOW, LIGHT_BLUE, PINK, WHITE]
        for sat in self.satellites:
            sat.send("set_led", colors[sat.id])
        self.send_to_all("set_game", "speed")
        self.cancelled = False

    def get_status(self) -> GameStatus:
        return self._status
    
    def history(self) -> GameHistory:
        return self._history
    
    def next_step(self):
        pass

    def on_response(self, id:int, message:Incoming):
        if self._status == GameStatus.NOT_STARTED and message.command=="set_game":
            if all([sat.game_mode == "speed" for sat in self.satellites]):
                self._status = GameStatus.READY

        if self._status == GameStatus.COUNTDOWN:
            if not all([sat.history[-1].command == "start_countdown" for sat in self.satellites]): return
            self._status = GameStatus.STARTING

        if self._status == GameStatus.STARTING and message.command == "start_countdown":
            if id != 0: return
            time.sleep(1) # waits 1 second
            self._status = GameStatus.RUNNING
            sat = random.choice(self.satellites)
            sat.send("flash")
            sat.send("wait_swing", 10)
            self.update(flash=sat.id,turn=self.current_turn)
            self.current_turn += 1
            return

        if self._status == GameStatus.RUNNING:
            time.sleep(2) # waits 2 seconds
            if message.command == "wait_swing":
                message.arg1 # time taken 
                self.history().add(message.arg1, message.arg1 != TIMEOUT, id)
            
            self.update(time=message.arg1, id=id)
            
            if self.current_turn >= self.total_turn_count:
                self.stop()
                return
            sat = random.choice(self.satellites)
            sat.send("flash")
            sat.send("wait_swing", 10)
            self.update(flash=sat.id,turn=self.current_turn)
            self.current_turn += 1

        if self._status == GameStatus.STOPPED:
            if not all([sat.history[-1].command == "stop" for sat in self.satellites]): return
            self._status = GameStatus.FINISHED
            self.update(done=True)

    def run(self):
        """ GETS CALLED BY USER WHEN FINISHED SETTING UP THE SATELITES """
        if (self._status != GameStatus.READY): return 
        self.send_to_all("start_countdown", "3")
        self._status = GameStatus.COUNTDOWN

    def stop(self):
        self.send_to_all("stop")
        self._status = GameStatus.STOPPED
        
    def send_to_all(self, command: str, arg1:str = None, arg2:str=None):
        for sat in self.satellites:
            
            sat.send(command, arg1, arg2)
            
    def update(self,*args, **kwargs):
        if self.update_interface:
            self.update_interface(*args, **kwargs)
