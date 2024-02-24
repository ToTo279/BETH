from PyQt5.QtWidgets import *
from gui.widgets import *
from threading import Thread
from time import sleep

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from gui.mainWindow import MainWindow

class DebugWindow(QWidget):
    def __init__(self, parent: 'MainWindow') -> None:
        super().__init__()
        layout = QVBoxLayout()
        bottom = QHBoxLayout()

        for i in parent.satellites:
            i.on_response = self.update_data


        self.main = parent
        self.messages = []
        
        back = PushButton("Back")
        back.setFixedHeight(60)
        back.clicked.connect(lambda:parent.setWindow("mainMenu"))
        
        self.text = Label("\n".join([f"Teste{1}" for i in range(30)]), type="console")
        self.text.setWordWrap(True)
        self.text.setAlignment(Qt.AlignmentFlag.AlignTop)

        bottom.addWidget(back)
        bottom.addStretch()

        layout.addWidget(self.text)
        layout.addLayout(bottom)

        self.setLayout(layout)

    def update_data(self, id:int, data:dict):
        self.messages.append(f"<{id}> {data}")
        if len(self.messages) > 13:
            self.messages = self.messages[-13:]
        self.text.setText("\n".join(self.messages))

        