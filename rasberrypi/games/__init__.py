from time import time
from abc import ABCMeta, abstractmethod
from enum import Enum
import json
import os

class GameStatus(Enum):
    """ Enum for game status """
    NOT_STARTED = 0
    READY = 1
    RUNNING = 2
    STOPPED = 3
    FINISHED = 4
    ERROR = 5
    UNKNOWN = 6
    COUNTDOWN = 7
    STARTING = 8

GameMode = Enum('GameMode', ['NONE', 'SPEED'])

class GameHistory:
    def __init__(self):
        self._history: list[dict] = []

    def add(self, score: int, success: bool, satellite_id: int):
        self._history.append({
            "score": score,
            "timestamp": time(),
            "success": success,
            "satellite_id": satellite_id
        })

    def get(self) -> list[dict]:
        return self._history

    def get_last(self) -> dict:
        if len(self._history) == 0:
            return None
        return self._history[-1]

    def get_last_success(self) -> dict:
        for i in range(len(self._history) - 1, -1, -1):
            if self._history[i]["success"]:
                return self._history[i]
        return None
    
    def save_game(self):
        if len(self._history) == 0: return
        filename = 'game_history_' + str(time())
        data = []
        for i in self._history:
            data.append({
                "score":i["score"],
                'timestamp':i['timestamp'],
                'success': i['success'],
                'satellite_id':i['satellite_id']
            })
        if not os.path.exists(f"./storage"):
            os.mkdir(f"./storage")
        with open(f"./storage/{filename}.json", 'w') as f:
            json.dump(data, f)




class Game(metaclass=ABCMeta):
    """Interface for all games"""

    """ Starts the game """
    @abstractmethod
    def start(self): raise NotImplementedError
    
    """ Stops/cancels the game """
    @abstractmethod
    def stop(self): raise NotImplementedError
    
    """ Iterates to the next step of the game """
    @abstractmethod
    def next_step(self): raise NotImplementedError
    
    """ Runs the game """
    @abstractmethod
    def run(self): raise NotImplementedError
    
    """ Returns Status of the game """
    @abstractmethod
    def get_status(self) -> GameStatus: raise NotImplementedError

    """ Returns history of the game """
    @abstractmethod
    def history(self) -> GameHistory: raise NotImplementedError
