from __future__ import annotations
import sys
from typing import *
from PyQt5.QtWidgets import *

from gui.connectWindow import ConnectWindow
from gui.selectGameWindow import SelectGameWindow
from gui.mainMenu import MainMenu
from gui.speedGameWindow import speedGameWindow
from gui.widgets import *
from gui.debugWIndow import DebugWindow
from gui.logsWindow import logsWindow

from utils.config import FULL_SCREEN

from multiprocessing import Queue
from games.satellite import Satellite
from ctypes import c_bool

class Windows:
    windows = {}
    current = "connect"

    @classmethod
    def start_windows(cls, main:MainWindow):
        cls.windows = {"connect": ConnectWindow(main), 
                       "gameSelect": SelectGameWindow(main), 
                       "mainMenu": MainMenu(main),
                       "reaction": speedGameWindow(main),
                       "logs": logsWindow(main),
                       "debug": DebugWindow(main)
                       }

    @classmethod
    def get_current_window(cls)->QWidget:
        return cls.windows[cls.current]
    
    @classmethod
    def get_window(cls, label:str)->QWidget:
        return cls.windows[label]

    @classmethod
    def set_window(cls, label=None, index=None):
        if not any([label, index]):
            raise ValueError("At least label xor index need to be defined")
        elif label and label in cls.windows:
            cls.current = label
        elif index and index > 0 and index < len(cls.windows):
            cls.current = list(cls.windows.keys())[index]
        else:
            raise ValueError(
                f"Values provided are invalid:\nWindows:{cls.windows}\nLabel:{label}\nIndex:{index}"
            )


class MainWindow(QWidget):
    def __init__(self, incoming: List[Queue], outgoing: List[Queue], satellites: List[c_bool]):
        super().__init__()

        # Configure Window Size
        self.setWindowTitle("Bad Milton")
        self.setFixedSize(800, 480)
        self.setGeometry(100, 100, 800, 480)
        self.setObjectName("mainWindow")
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.satellites = [
            Satellite(i, outgoing[i], incoming[i], satellites) for i in range(len(satellites))
        ]

        # Load Stylesheet
        with open("./gui/styles", "r") as f:
            self.setStyleSheet(f.read())

        # configure windwos
        Windows.start_windows(self)
        Windows.set_window(label="mainMenu")

        layout = QVBoxLayout()
        topper = TopMenu(self)
        lower = QHBoxLayout()

        self.central_widget = QStackedWidget()
        
        layout.addLayout(topper)
        layout.addLayout(lower)
        lower.addWidget(self.central_widget)

        self.setLayout(layout)
        
        #self.setCentralWidget(self.central_widget)
        self.central_widget.addWidget(Windows.get_current_window())
        
        if FULL_SCREEN == 1:
            self.showFullScreen()
            # self.showMaximized()
        else:
            self.show()

    def reload_syles(self):
        with open("./gui/styles", "r") as f:
            self.setStyleSheet(f.read())


    def getWindow(self, label: str) -> QWidget:
        return Windows.get_window(label)

    def setWindow(self, window: str):
        # Test if this part is creating a stack of widgets
        # -> Does not create! Great!
        Windows.set_window(label=window)
        self.central_widget.addWidget(Windows.get_current_window())
        self.central_widget.setCurrentWidget(Windows.get_current_window())

    def n_connected(self)->int:
        return sum([1 for i in self.satellites if i.status])



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
