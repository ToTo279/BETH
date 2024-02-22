from __future__ import annotations
from threading import Thread
import typing
from PyQt5 import QtCore
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *
from .widgets import *
from games.badminton_training import SpeedTraining
from .consts import *
from games.satellite import Satellite
from PyQt5.QtCore import pyqtSlot, pyqtSignal

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from mainWindow import MainWindow


class speedGameWindow(QWidget):
    def __init__(self, parent: 'MainWindow' = None) -> None:
        super().__init__()
        self.settingsWindow = settingsWindow(self)
        self.endGameWindow = None
        self.inGameWindow = None

        self.main = parent
        layout = QVBoxLayout()
        self.center = QStackedWidget()
        self.turns = 0
        
        layout.addWidget(self.center)
        self.center.addWidget(self.settingsWindow)
        self.center.setCurrentWidget(self.settingsWindow)
        self.setLayout(layout)

    def get_turns(self)->int:
        return self.turns

    def get_satelites(self)->List[Satellite]:
        """Returns the list of satellites that are currently connected"""
        return [i for i in self.main.satellites if i.status]
    
    def get_game(self)->SpeedTraining:
        if self.game: return self.game
        return None

    def go_back(self):
        self.main.setWindow("gameSelect")
        if self.inGameWindow:
            self.center.removeWidget(self.inGameWindow)
            self.center.setCurrentWidget(self.settingsWindow)
            self.inGameWindow = None
        if self.endGameWindow:
            self.center.removeWidget(self.endGameWindow)
            self.center.setCurrentWidget(self.settingsWindow)
            self.endGameWindow = None

    def start_game(self):
        if self.main.n_connected() == 0: return
        # Starts the game, sending messages to the satellites
        self.turns = int(self.settingsWindow.count.text())
        self.game = SpeedTraining(self.main.satellites, self.turns)
        self.inGameWindow = inGameWindow(self)
        self.inGameWindow.game_ended_signal.connect(self.end_game)
        self.game.update_interface = self.inGameWindow.update
        self.center.addWidget(self.inGameWindow)
        self.center.setCurrentWidget(self.inGameWindow)
        self.game.start()
        
    @pyqtSlot()
    def end_game(self):
        if self.endGameWindow: return
        self.endGameWindow = endGameWindow(self)
        self.center.addWidget(self.endGameWindow)
        self.center.setCurrentWidget(self.endGameWindow)


class inGameWindow(QWidget):
    game_ended_signal = pyqtSignal()
    def __init__(self, main: speedGameWindow):
        super().__init__()
        self.gridLayout = QGridLayout()
        self.gridLayout.setSpacing(0)
        self.gridLayout.setContentsMargins(0,0,0,0)

        layout = QHBoxLayout()
        left = QVBoxLayout()
        right = QVBoxLayout()
        layout.addLayout(left)
        #layout.addStretch()
        layout.addLayout(right)

        self.countdown_layout = QVBoxLayout()
        self.countdown_label = Label("3")
        self.countdown_timer = QTimer()
        self.countdown_timer.setInterval(1000)
        self.countdown_timer.timeout.connect(self.update_countdown_screen)
        
        self.countdown_label.setObjectName("countdownLabel")
        self.countdown_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.countdown_layout.addWidget(self.countdown_label)
        self.countdown_layout.addStretch()
        self.countdown_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.countdown_label.setVisible(False)

        self.main = main
        self.satelites = main.get_satelites()
        self.indicators = [RoundLabel(str(i+1)) for i in range(len(self.satelites))]
        self.times = [Label("0.0s") for i in range(len(self.satelites))]
        self.start_stop_button = PushButton("Start", command=self.start)

        for i in range(len(self.indicators)):
            indicator = self.indicators[i]
            time = self.times[i]
            time.setMargin(10)
            hbox = QHBoxLayout()
            indicator.setFixedSize(40,40)
            hbox.addWidget(indicator)
            hbox.addWidget(time)
            left.addLayout(hbox)

        t1 = Label("Runde", type="title_big")
        self.round = Label("0", type="big")
        t1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.round.setAlignment(Qt.AlignmentFlag.AlignCenter)
        right.addWidget(t1)
        right.addWidget(self.round)
        right.addStretch()
        buttons_box = QHBoxLayout()
        self.back_button = PushButton("Back", command=self.main.go_back)
        right.addLayout(buttons_box)
        buttons_box.addWidget(self.back_button)
        buttons_box.addWidget(self.start_stop_button)

        self.gridLayout.addLayout(layout, 0, 0, 1, 1)
        self.gridLayout.addLayout(self.countdown_layout, 0, 0, 1, 1)
        self.setLayout(self.gridLayout)

    def start(self):
        self.back_button.hide()
        self.start_countdown_screen()
        self.start_stop_button.setText("Stop")
        self.start_stop_button.clicked.disconnect()
        self.start_stop_button.clicked.connect(self.stop)
        self.main.get_game().run()

    def start_countdown_screen(self):
        self.countdown_label.setVisible(True)
        self.countdown_timer.start()

    def update_countdown_screen(self):
        countdown_text = self.countdown_label.text()
        countdown_text = int(countdown_text)-1
        if countdown_text == -1:
            self.countdown_label.setVisible(False)
            self.countdown_timer.stop()
            return
        self.countdown_label.setText(str(countdown_text))

    def stop(self):
        game = self.main.get_game()
        if not game: return
        game.cancelled = True
        game.stop()

    def finished(self):
        # game finished without interruptions
        self.main.get_game().history().save_game()
        self.game_ended_signal.emit()

    def update(self, *args, **kwargs):
        if "time" in kwargs and "id" in kwargs:
            id:int = kwargs["id"]
            time:float = kwargs["time"]
            self.times[id].setText(f"{time}s")
            self.blink(id)
            #self.indicators[id].set_background_color("#a7a7a7")

        if "flash" in kwargs:
            id:int = kwargs["flash"]
            self.indicators[id].set_background_color("#f4f72f")

        if "turn" in kwargs:
            self.round.setText(str(kwargs["turn"]))
        if "done" in kwargs:
            self.finished()

    def blink(self, id:int):
        rLabel = self.indicators[id]
        rLabel.set_background_color("#46fa55")
        Thread(
            target=lambda:(sleep(0.3), rLabel.set_background_color("#a7a7a7"))
            ).start()


class settingsWindow(QWidget):
    def __init__(self, main: speedGameWindow):
        super().__init__()

        self.main = main

        layout = QVBoxLayout()
        top = QHBoxLayout()
        bot = QHBoxLayout()
        left = QVBoxLayout()
        right = QVBoxLayout()
        top.addLayout(left)
        top.addLayout(right)
        layout.addLayout(top)
        layout.addLayout(bot)

        self.text = Label("Positioniere die Satellites an den richtigen Positionen rund um das Badmintom-Feld!",
                          "medium")
        self.text.setWordWrap(True)

        left.addWidget(self.text)
        left.addStretch()

        self.count = Label("10","title")
        self.count.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.up_button   = PushButton(command=lambda :self.count.setText(str(int(self.count.text())+1)))
        self.down_button = PushButton(command=lambda :self.count.setText(str(int(self.count.text())-1)) if self.count.text()!= "0" else {} )
        self.up_button.setIcon(QIcon("gui/assets/up.png"))
        self.down_button.setIcon(QIcon("gui/assets/down.png"))
        right.setAlignment(Qt.AlignmentFlag.AlignCenter)
        right.addStretch()
        right.addWidget(self.up_button)
        right.addWidget(Label("Rounds:"))
        right.addWidget(self.count)
        right.addWidget(self.down_button)
        right.addStretch()

        bot.addWidget(PushButton("Back", command=main.go_back))
        bot.addStretch()
        bot.addWidget(PushButton("Start Game!", command=main.start_game))

        self.setLayout(layout)


class endGameWindow(QWidget):
    def __init__(self, main: speedGameWindow):
        super().__init__()
        self.main = main
        history = self.main.get_game().history().get()
        
        times = [i['score'] for i in history if i['success']]
        
        n_failures = len([i for i in history if not i['success']])
        n_round = len(history)
        if len(times) == 0:
            avg = 0
        else:
            avg = round(sum(times)/len(times),2)
        try:
            max_ = max([i for i in history if i['success']], key=lambda x: x['score'])
            min_ = min([i for i in history if i['success']], key=lambda x: x['score'])
        except:
            max_ = {'score':0, 'satellite_id':0}
            min_ = {'score':0, 'satellite_id':0}


        layout = QVBoxLayout()
        

        rounds_label = Label("Rounds:", type="large-bold")
        average_time_label = Label("Average Time:", type="large-bold")
        best_time_label = Label("Best Time:", type="large-bold")
        worse_time_label = Label("Worse Time:", type="large-bold")
        n_fails_label = Label("Number of Fails:", type="large-bold")

        rounds_value_label = Label(f"{n_round}", type="large")
        average_time_value_label = Label(f"{avg}s", type="large")
        best_time_value_label = Label(f"{min_['score']} mit Satellite {min_['satellite_id']}", type="large")
        worse_time_value_label = Label(f"{max_['score']} mit Satellite {max_['satellite_id']}", type="large")
        n_fails_value_label = Label(f"{n_failures}", type="large")

        rounds_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        average_time_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        best_time_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        worse_time_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        n_fails_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        rounds_value_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        average_time_value_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        best_time_value_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        worse_time_value_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        n_fails_value_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        
        form_layout = QFormLayout()
        form_layout.addRow(rounds_label, rounds_value_label)
        form_layout.addRow(average_time_label, average_time_value_label)
        form_layout.addRow(best_time_label, best_time_value_label)
        form_layout.addRow(worse_time_label, worse_time_value_label)
        form_layout.addRow(n_fails_label, n_fails_value_label)

        form_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        
        #layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        layout.addLayout(form_layout)
        layout.addStretch()
        layout.addWidget(PushButton("Zurück", command=main.go_back))
        if main.get_game().cancelled: # This part seems strange, 
            layout.addWidget(PushButton("Speichern", command=
                                        lambda: (self.main.get_game().history().save_game(), main.go_back())))

        self.setLayout(layout)

