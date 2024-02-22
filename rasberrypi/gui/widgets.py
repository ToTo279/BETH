from time import sleep
from typing import TYPE_CHECKING, Callable, List, Tuple
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtCore import Qt, QCoreApplication, QTimer
from utils.config import MAX_NUMBER_OF_SATELLITES
from games.satellite import Satellite
if TYPE_CHECKING:
    from mainWindow import MainWindow

class RoundLabel(QLabel):
    def __init__(self, text=None, type: str = None, parent=None):
        super().__init__(text=text, parent=parent)
        self.setObjectName(type)
        self.setStyleSheet(self._get_default_style())
    def _get_default_style(self):
        return """
            border-radius:20px;
            background-color:#a7a7a7;
            font-weight: bold;
            color: white;
            font-size: 12px;
            qproperty-alignment: AlignCenter;
            line-height: 50px;
            text-align: center;
        """
    def set_background_color(self, color):
        style = self._get_default_style()
        style += f"background-color: {color};"
        try:
            self.setStyleSheet(style)
        except Exception as e:
            print(f"Error parsing stylesheet of object: {e}")

class Label(QLabel):
    def __init__(self, text=None, type: str = None, parent=None):
        super().__init__(text=text, parent=parent)
        self.setObjectName(type)
        #self.setAutoFillBackground(True)

class PushButton(QPushButton):
    def __init__(self, text=None, parent=None, command: Callable = None, type=None):
        super().__init__(text=text, parent=parent)
        self.setObjectName(type)
        if command:
            self.clicked.connect(command)

class TopMenu(QHBoxLayout):
    def __init__(self, main: 'MainWindow', circle_size=60):
        super().__init__()
        self.circle_size = circle_size
        self.satelites: List[Satellite] = main.satellites

        self.sat_displays: Tuple[QLabel, Label] = []
        for i in range(len(self.satelites)):
            sat = QLabel(text=f"{i+1}")
            sat.setStyleSheet("""
                border-radius:30px;
                background-color:#fa4646;
                font-weight: bold;
                color: white;
                font-size: 22px;
                qproperty-alignment: AlignCenter;
                line-height: 50px;
                text-align: center;""")
            sat.setMinimumSize(self.circle_size, self.circle_size)
            sat.setAlignment(Qt.AlignmentFlag.AlignLeft)
            text = Label(f"100%")
            self.addWidget(sat)
            self.addWidget(text)
            self.sat_displays.append((sat, text))

        self.timer=QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(1_000)

        self.main = main

        self.quit_button = PushButton(type="round",command=self.stop)
        self.quit_button.setFixedWidth(circle_size - 20)
        self.quit_button.setIcon(QIcon("gui/assets/close.png"))
        
        self.addStretch()
        self.addWidget(self.quit_button)

    def stop(self):
        for i in self.main.satellites:
            i.stop()
        QCoreApplication.quit()

    def set_green_battery(self, circle: QLabel, text:Label, battery:str):
        circle.setStyleSheet(f"""
            border-radius:30px;
            background-color:#40b53a;
            font-weight: bold;
            color: white;
            font-size: 22px;
            qproperty-alignment: AlignCenter;
            line-height: 50px;
            text-align: center;""")
        if battery:
            text.setText(f"{battery}%")
        else:
            text.setText(f"--%")

    def set_red_battery(self, circle: QLabel, text:Label):
        circle.setStyleSheet("""
            border-radius:30px;
            background-color:#fa4646;
            font-weight: bold;
            color: white;
            font-size: 22px;
            qproperty-alignment: AlignCenter;
            line-height: 50px;
            text-align: center;""")
        text.setText(f"-")

    def update_data(self):
        for i in range(len(self.satelites)):
            sat = self.satelites[i]
            sat_circle, sat_txt = self.sat_displays[i]
            if sat.status:
                self.set_green_battery(sat_circle,sat_txt, sat.battery)
            else:
                self.set_red_battery(sat_circle,sat_txt)


class GameField(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(200)
        self.setFixedHeight(220)
        
        #
        # container:layout
        #   ->Grid1
        #     ...
        #   ->Grid4
        # 
        main_layout = QVBoxLayout()

        container = Label(type="GameField")
        layout = QVBoxLayout()
        container.setLayout(layout)
        main_layout.addWidget(container)

        b1 = Label("0",type="roundFieldYellow")
        b2 = Label("1",type="roundFieldRed")
        b3 = Label("2",type="roundFieldGreen")
        b4 = Label("3",type="roundFieldBlue")

        b1.setMinimumSize(40,40)
        b2.setMinimumSize(40,40)
        b3.setMinimumSize(40,40)
        b4.setMinimumSize(40,40)
        firstRow = QHBoxLayout()
        firstRow.addWidget(b1)
        firstRow.addStretch()
        firstRow.addWidget(b2)
        secondRow = QHBoxLayout()
        secondRow.addWidget(b3)
        secondRow.addStretch()
        secondRow.addWidget(b4)

        layout.addLayout(firstRow)
        layout.addStretch()
        layout.addLayout(secondRow)

        self.setLayout(main_layout)