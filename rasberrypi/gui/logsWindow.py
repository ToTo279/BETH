import os
import json
from datetime import datetime

from gui.widgets import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from gui.mainWindow import MainWindow


class logsWindow(QWidget):
    def __init__(self, parent: 'MainWindow') -> None:
        super().__init__()
        self.parent = parent

        # search in storage directory for game history files
        self.files = []
        self.file_dates = []
        
        self.list = QListWidget()
        self.list.setStyleSheet('QListView::item {height: 50px;line-height: 50px; font-size: 30px}')
        self.list.itemClicked.connect(self.open_file)
        self.list.setSpacing(5)
        self.refresh_list()
        self.__create_stats()

        main_layout = QHBoxLayout()
        left_w = QWidget()
        left = QVBoxLayout()
        right_w = QWidget()
        right = QVBoxLayout()
        main_layout.addWidget(left_w)
        main_layout.addWidget(right_w)

        left_w.setLayout(left)
        left_w.setFixedWidth(200)
        right_w.setLayout(right)


        
        form_layout = QFormLayout()
        form_layout.addRow(self.rounds_label, self.rounds_value_label)
        form_layout.addRow(self.average_time_label, self.average_time_value_label)
        form_layout.addRow(self.best_time_label, self.best_time_value_label)
        form_layout.addRow(self.worse_time_label, self.worse_time_value_label)
        form_layout.addRow(self.n_fails_label, self.n_fails_value_label)
        #form_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        left.addWidget(Label("Spiele", type="large-bold"))
        left.addWidget(self.list)

        right.addLayout(form_layout)
        right.addWidget(PushButton("Zurück", command=lambda:parent.setWindow("mainMenu")))

        self.setLayout(main_layout)

    def __create_stats(self):
        self.rounds_label = Label("Rounds:", type="large-bold")
        self.average_time_label = Label("Average Time:", type="large-bold")
        self.best_time_label = Label("Best Time:", type="large-bold")
        self.worse_time_label = Label("Worse Time:", type="large-bold")
        self.n_fails_label = Label("Number of Fails:", type="large-bold")

        self.rounds_value_label = Label(f"", type="large")
        self.average_time_value_label = Label(f"", type="large")
        self.best_time_value_label = Label(f"", type="large")
        self.worse_time_value_label = Label(f"", type="large")
        self.n_fails_value_label = Label(f"", type="large")

        self.rounds_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.average_time_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.best_time_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.worse_time_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.n_fails_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        self.rounds_value_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.average_time_value_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.best_time_value_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.worse_time_value_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.n_fails_value_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

    def open_file(self, item):
        index = self.file_dates.index(item.text())
        try:
            with open(f"./storage/{self.files[index]}","r") as f:
                history = json.load(f)
        except Exception as e:
            print(f"Exception reading file: {e}")
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

        self.rounds_value_label.setText(f"{n_round}")
        self.average_time_value_label.setText(f"{avg}s")
        self.best_time_value_label.setText(f"{min_['score']} mit Satellite {min_['satellite_id']}")
        self.worse_time_value_label.setText(f"{max_['score']} mit Satellite {max_['satellite_id']}")
        self.n_fails_value_label.setText(f"{n_failures}")

    def refresh_list(self):
        self.list.clear()
        self.files = []
        self.file_dates = []
        for file in os.listdir("./storage"):
            if file.startswith("game_history_"):
                self.files.append(file)
        
        self.files.sort(reverse=True)

        for file in self.files:
            self.file_dates.append(datetime.fromtimestamp(float(file.replace("game_history_", "").replace(".json", ""))).strftime("%d.%m.%Y %H:%M:%S"))	
        self.list.addItems(self.file_dates)
        