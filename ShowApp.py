import json
import os
from datetime import date

from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout,
    QLineEdit, QSpinBox, QPushButton,
    QTableWidget, QTableWidgetItem,
    QLabel, QDialog
)

from Show import Show


class ShowApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Show Planner")

        self.shows = []
        self.editing_show = None

        self.init_ui()
        self.load_shows()
        self.refresh_table()

    # ================= UI =================
    def init_ui(self):
        main_layout = QHBoxLayout()
        left_layout = QVBoxLayout()

        # BUTTON
        self.add_btn = QPushButton("Add Show")
        self.add_btn.clicked.connect(self.open_panel)

        # TABLE
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Show Name", "Episodes", "Minutes/Ep",
            "Hours/Day", "Days Left", "Completed", "Edit"
        ])
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)

        left_layout.addWidget(self.table)
        left_layout.addWidget(self.add_btn)

        # ================= SIDE PANEL =================
        self.side_panel = QWidget()
        self.side_panel.setFixedWidth(300)

        panel_layout = QVBoxLayout()

        self.name_input = QLineEdit()

        self.episodes_input = QSpinBox()
        self.episodes_input.setRange(1, 10000)

        self.minutes_input = QSpinBox()
        self.minutes_input.setRange(1, 180)

        self.hours_input = QSpinBox()
        self.hours_input.setRange(1, 24)

        self.submit_btn = QPushButton("Submit")
        self.submit_btn.clicked.connect(self.create_show)

        self.delete_btn = QPushButton("Delete Show")
        self.delete_btn.clicked.connect(self.delete_show)
        self.delete_btn.hide()

        self.close_btn = QPushButton("Close")
        self.close_btn.clicked.connect(self.side_panel.hide)

        panel_layout.addWidget(QLabel("Show Name"))
        panel_layout.addWidget(self.name_input)

        panel_layout.addWidget(QLabel("Episodes"))
        panel_layout.addWidget(self.episodes_input)

        panel_layout.addWidget(QLabel("Minutes per Episode"))
        panel_layout.addWidget(self.minutes_input)

        panel_layout.addWidget(QLabel("Hours per Day"))
        panel_layout.addWidget(self.hours_input)

        panel_layout.addWidget(self.submit_btn)
        panel_layout.addWidget(self.delete_btn)
        panel_layout.addWidget(self.close_btn)

        self.side_panel.setLayout(panel_layout)
        self.side_panel.hide()

        main_layout.addLayout(left_layout)
        main_layout.addWidget(self.side_panel)

        self.setLayout(main_layout)

    # ================= PANEL =================
    def open_panel(self):
        self.editing_show = None

        self.name_input.clear()
        self.episodes_input.setValue(1)
        self.minutes_input.setValue(30)
        self.hours_input.setValue(1)

        self.submit_btn.setText("Submit")
        self.delete_btn.hide()

        self.side_panel.show()

    def create_show(self):
        name = self.name_input.text()
        episodes = self.episodes_input.value()
        minutes = self.minutes_input.value()
        hours = self.hours_input.value()

        if not name:
            return

        if self.editing_show:
            self.editing_show.name = name
            self.editing_show.number_of_episodes = episodes
            self.editing_show.minutes_per_episode = minutes
            self.editing_show.hours_per_day = hours

            if self.editing_show.days_completed >= self.editing_show.total_days:
                self.completed_show(self.editing_show)

            self.editing_show = None

        else:
            show = Show(name, episodes, hours, minutes)
            self.shows.append(show)

        self.refresh_table()
        self.save_shows()
        self.side_panel.hide()

    # ================= TABLE =================
    def refresh_table(self):
        if len(self.shows) == 0:
            self.table.hide()
            return
        else:
            self.table.show()

        today = date.today().isoformat()
        self.table.setRowCount(len(self.shows))

        for row, show in enumerate(self.shows):
            self.table.setItem(row, 0, QTableWidgetItem(show.name))
            self.table.setItem(row, 1, QTableWidgetItem(str(show.number_of_episodes)))
            self.table.setItem(row, 2, QTableWidgetItem(str(show.minutes_per_episode)))
            self.table.setItem(row, 3, QTableWidgetItem(str(show.hours_per_day)))
            self.table.setItem(row, 4, QTableWidgetItem(str(show.days_remaining)))

            # COMPLETE BUTTON
            btn = QPushButton("Completed")

            if show.last_completed_date == today:
                btn.setText("Done")
                btn.setEnabled(False)
                btn.setStyleSheet("color: #4caf50; font-weight: bold;")
            else:
                btn.setStyleSheet("color: #f44336; font-weight: bold;")

            btn.clicked.connect(lambda _, s=show: self.complete_day(s))
            self.table.setCellWidget(row, 5, btn)

            # EDIT BUTTON
            edit_btn = QPushButton("Edit")
            edit_btn.clicked.connect(lambda _, s=show: self.edit_show(s))
            self.table.setCellWidget(row, 6, edit_btn)

    # ================= COMPLETE =================
    def complete_day(self, show):
        today = date.today().isoformat()

        if show.last_completed_date == today:
            return

        if show.days_remaining > 0:
            show.days_completed += 1
            show.last_completed_date = today

            if show.days_completed >= show.total_days:
                self.completed_show(show)

            self.refresh_table()
            self.save_shows()

    def completed_show(self, show):
        dialog = QDialog(self)
        dialog.setWindowTitle("Show Completed 🎉")
        dialog.setFixedSize(300, 150)

        layout = QVBoxLayout()
        label = QLabel(f"🎉 Great job!\n\nYou finished:\n{show.name}")
        label.setAlignment(Qt.AlignCenter)

        layout.addWidget(label)
        dialog.setLayout(layout)

        QTimer.singleShot(5000, dialog.accept)
        dialog.exec_()

        self.shows.remove(show)
        self.refresh_table()
        self.save_shows()

    # ================= EDIT =================
    def edit_show(self, show):
        self.editing_show = show

        self.name_input.setText(show.name)
        self.episodes_input.setValue(show.number_of_episodes)
        self.minutes_input.setValue(show.minutes_per_episode)
        self.hours_input.setValue(show.hours_per_day)

        self.submit_btn.setText("Update Show")
        self.delete_btn.show()

        self.side_panel.show()

    def delete_show(self):
        if self.editing_show:
            self.shows.remove(self.editing_show)
            self.editing_show = None

            self.refresh_table()
            self.save_shows()
            self.side_panel.hide()

    # ================= STORAGE =================
    def save_shows(self):
        data = []

        for show in self.shows:
            data.append({
                "name": show.name,
                "number_of_episodes": show.number_of_episodes,
                "hours_per_day": show.hours_per_day,
                "minutes_per_episode": show.minutes_per_episode,
                "days_completed": show.days_completed,
                "last_completed_date": show.last_completed_date
            })

        with open("shows.json", "w") as f:
            json.dump(data, f, indent=4)

    def load_shows(self):
        if not os.path.exists("shows.json"):
            return

        self.shows.clear()

        with open("shows.json", "r") as f:
            data = json.load(f)

        for item in data:
            show = Show(
                item["name"],
                item["number_of_episodes"],
                item["hours_per_day"],
                item["minutes_per_episode"]
            )
            show.days_completed = item["days_completed"]
            show.last_completed_date = item.get("last_completed_date")

            self.shows.append(show)

    def closeEvent(self, event):
        self.save_shows()
        event.accept()