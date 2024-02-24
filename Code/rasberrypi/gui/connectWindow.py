from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QPainter, QMouseEvent
from PyQt5.QtCore import Qt
from .widgets import Label, PushButton
from functools import partial


from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from mainWindow import MainWindow

class ConnectWindow(QWidget):
    def __init__(self, parent: 'MainWindow'):
        super().__init__()
        layout = QVBoxLayout()
        self.setObjectName("window")
        self.setLayout(layout)

        self.label = QLabel(self)
        self.pixmap = QPixmap("./gui/assets/logo.png")
        self.pixmap = self.pixmap.scaled(
            self.pixmap.width() // 2, self.pixmap.height() // 2
        )
        self.label.setPixmap(self.pixmap)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title = Label("Connect the Satelites:", "title")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.button = QPushButton("Done!")
        button_container = QHBoxLayout()
        button_container.addStretch()
        button_container.addWidget(self.button)

        satelites = QHBoxLayout()
        size = 60
        boxes = [QLabel() for i in range(4)]
        i = 1
        for box in boxes:
            box.setObjectName("roundRed")
            box.setMaximumSize(size, size)
            box.setMinimumSize(size, size)
            box.setAlignment(Qt.AlignmentFlag.AlignCenter)
            satelites.addWidget(box)
            satelites.addWidget(Label(f"Satelite {i}"))
            i += 1

        layout.addWidget(self.label)
        layout.addWidget(self.title)
        layout.addStretch()
        layout.addLayout(satelites, 1)
        layout.addStretch()
        layout.addLayout(button_container)
