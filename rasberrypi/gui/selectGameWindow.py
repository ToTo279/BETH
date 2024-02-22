from PyQt5.QtWidgets import *
from .widgets import *

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from mainWindow import MainWindow

class SelectGameWindow(QWidget):
    def __init__(self, parent:'MainWindow'):
        super().__init__()
        l_width = 230
        self.game = "reaction"
        self.main = parent


        layout = QHBoxLayout()
        left_w = QWidget()
        left = QVBoxLayout()
        right_w = QWidget()
        right = QVBoxLayout()
        layout.addWidget(left_w)
        layout.addWidget(right_w)

        left_w.setLayout(left)
        left_w.setFixedWidth(l_width)
        right_w.setLayout(right)


        self.title = Label("", "title")
        self.text = Label("")
        self.text.setWordWrap(True)


        b1 = PushButton("Reaction Time")
        b1.pressed.connect(lambda:self.change_game("reaction"))
        b2 = PushButton("Meteor")
        b2.pressed.connect(lambda:self.change_game("meteor"))


        left.addWidget(Label("Select a game!","title"))
        left.addSpacing(10)
        left.addWidget(b1)

        # left.addWidget(b2)
        left.addStretch()
        left.addWidget(PushButton("Return", command=lambda:parent.setWindow("mainMenu")))

        right.addWidget(self.title)
        right.addWidget(self.text)
        right.addStretch()
        right.addWidget(PushButton("Start Game!", command=self.start_game))

        self.change_game(self.game)

        self.setLayout(layout)

    def start_game(self):
        self.main.setWindow(self.game)

    def change_text(self, title, text):
        self.title.setText(title)
        self.text.setText(text)

    def change_game(self, game:str):
        self.game = game
        if game == "reaction":
            
            self.change_text("Reaction Training:",
                             "Try to react as fast as possible as the different satelites activate around you!")
        elif game == "meteor":
            self.change_text("Meteor",
                             "The satelites will start to light up at the same time! They go from red to yellow and then green.\n Keep track of all satelites and activate them when they turn green!")
