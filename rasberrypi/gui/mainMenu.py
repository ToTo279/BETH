import typing
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget
from .widgets import *

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from mainWindow import MainWindow

class MainMenu(QWidget):
    def __init__(self, parent: 'MainWindow' = None) -> None:
        super().__init__()
        layout = QVBoxLayout()
        
        layout.addWidget(Label("B.E.T.H.", type="title_big"))
        layout.addWidget(Label("Badminton Equipment for Training and Health", type="subtitle"))
        b1 = PushButton("Start")
        b2 = PushButton("Protokolle")
        b3 = PushButton("Status")
        bottom = QHBoxLayout()

        play_action = lambda: parent.setWindow("gameSelect")
        b1.clicked.connect(play_action)
        b2.clicked.connect(lambda:(parent.setWindow("logs"), parent.getWindow("logs").refresh_list()))
        b3.clicked.connect(lambda:parent.setWindow("debug"))

        layout.addWidget(b1)
        layout.addWidget(b2)
        layout.addWidget(b3)
        layout.addStretch()
        layout.addLayout(bottom)
        
        user_button = PushButton()
        user_button.setIcon(QIcon("gui/assets/user.png"))
        user_button.setMaximumWidth(80)
        
        bottom.addStretch()
        bottom.addWidget(user_button)
        
        self.setLayout(layout)


