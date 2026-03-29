import json
import os
import sys
from datetime import date
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QLabel, QHBoxLayout, QLineEdit, QSpinBox,
    QTableWidget, QTableWidgetItem, QScrollArea
)
from PyQt5.QtCore import Qt


class Task:
    def __init__(self, name, total_hours, total_days):
        self.name = name
        self.total_hours = total_hours
        self.total_days = total_days
        self.days_completed = 0
        self.last_completed_date = None

    @property
    def days_remaining(self):
        return self.total_days - self.days_completed

    @property
    def hours_per_day(self):
        return self.total_hours / self.total_days if self.total_days else 0


class TaskApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Task Planner")

        self.tasks = []

        self.init_ui()
        self.load_tasks()
        self.refresh_table()
        self.editing_task = None

    def init_ui(self):
        main_layout = QHBoxLayout()

        # ================= LEFT =================
        left_layout = QVBoxLayout()

        self.add_btn = QPushButton("Add Task")
        self.add_btn.clicked.connect(self.open_add_panel)

        # TABLE
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setColumnWidth(0,300)
        self.table.setColumnWidth(1,300)
        self.table.setColumnWidth(2,300)
        self.table.setColumnWidth(3,300)
        self.table.setColumnWidth(4,300)
        self.table.setColumnWidth(5,300)
        self.table.setHorizontalHeaderLabels([
            "Task Name", "Hours/Day", "Days Left", "Days Completed", "Action", "Edit"
        ])

        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)

        left_layout.addWidget(self.table)
        left_layout.addWidget(self.add_btn)
        # ================= SIDE PANEL =================
        self.side_panel = QWidget()
        self.side_panel.setObjectName("sidePanel")
        self.side_panel.setFixedWidth(300)

        panel_layout = QVBoxLayout()

        self.name_input = QLineEdit()
        self.hours_input = QSpinBox()
        self.hours_input.setRange(1, 1000)

        self.days_input = QSpinBox()
        self.days_input.setRange(1, 365)

        self.submit_btn = QPushButton("Submit")
        self.submit_btn.clicked.connect(self.add_task_from_panel)

        self.close_btn = QPushButton("Close")
        self.close_btn.clicked.connect(self.side_panel.hide)

        panel_layout.addWidget(QLabel("Task Name"))
        panel_layout.addWidget(self.name_input)
        panel_layout.addWidget(QLabel("How many Hours per Day"))
        panel_layout.addWidget(self.hours_input)
        panel_layout.addWidget(QLabel("How many Days"))
        panel_layout.addWidget(self.days_input)
        panel_layout.addSpacing(10)
        panel_layout.addWidget(self.submit_btn)
        panel_layout.addWidget(self.close_btn)

        self.side_panel.setLayout(panel_layout)
        self.side_panel.hide()

        self.table.setSelectionMode(QTableWidget.NoSelection)
        self.table.setFocusPolicy(Qt.NoFocus)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectItems)

        # ================= MAIN =================
        main_layout.addLayout(left_layout)
        main_layout.addWidget(self.side_panel)
        self.setLayout(main_layout)


        # ================= STYLE =================
        self.setStyleSheet("""
            QWidget {
                background-color: #121212;
                color: white;
                font-size: 16px;
            }

            QTableWidget {
                background-color: #2b2b2b;
                color: white;
                gridline-color: #444;
            }

            QHeaderView::section {
                background-color: #1f1f1f;
                color: white;
                font-weight: bold;
                padding: 6px;
                border: 1px solid #444;
            }

            QTableWidget QPushButton {
                background-color: transparent;
                border: none;
                color: white;
                padding: 0px;
            }

            /* 🔹 NORMAL BUTTONS (side panel, add button) */
            QPushButton {
                background-color: #3a3a3a;
                color: white;
                border: none;
                padding: 6px;
                border-radius: 4px;
            }

            QPushButton:hover {
                background-color: #505050;
            }

            QLineEdit, QSpinBox {
                background-color: #2b2b2b;
                color: white;
                border: 1px solid #555;
                padding: 4px;
            }

            QWidget#sidePanel {
                background-color: #1a1a1a;
                border-left: 2px solid #444;
                padding: 10px;
            }
        """)

    # ================= LOGIC =================

    def open_add_panel(self):
        self.editing_task = None
        self.name_input.clear()
        self.hours_input.setValue(1)
        self.days_input.setValue(1)

        self.submit_btn.setText("Submit")  # optional UX fix

        self.side_panel.show()

    def add_task_from_panel(self):
        name = self.name_input.text()
        hours = self.hours_input.value()
        days = self.days_input.value()

        if not name:
            return

        if self.editing_task:
            self.editing_task.name = name
            self.editing_task.total_hours = hours
            self.editing_task.total_days = days

            self.editing_task = None

        else:
            task = Task(name, hours, days)
            self.tasks.append(task)

        self.refresh_table()
        self.save_tasks()

        # Reset inputs
        self.name_input.clear()
        self.hours_input.setValue(1)
        self.days_input.setValue(1)

        self.side_panel.hide()

    def refresh_table(self):
        if len(self.tasks) == 0:
            self.table.hide()
            return
        else:
            self.table.show()
        today = date.today().isoformat()
        self.table.setRowCount(len(self.tasks))

        for row, task in enumerate(self.tasks):
            self.table.setItem(row, 0, QTableWidgetItem(task.name))
            self.table.setItem(row, 1, QTableWidgetItem(f"{task.hours_per_day:.2f}"))
            self.table.setItem(row, 2, QTableWidgetItem(str(task.days_remaining)))
            self.table.setItem(row, 3, QTableWidgetItem(str(task.days_completed)))

            btn = QPushButton("Complete Day")
            if task.last_completed_date == today:
                btn.setText("Done Today")
                btn.setEnabled(False)
            btn.clicked.connect(lambda _, t=task: self.complete_day(t))
            self.table.setCellWidget(row, 4, btn)

            edit_btn = QPushButton("Edit")
            edit_btn.clicked.connect(lambda _, t=task: self.edit_task(t))
            self.table.setCellWidget(row, 5, edit_btn)

        row_count = len(self.tasks)
        row_height = self.table.verticalHeader().defaultSectionSize()
        header_height = self.table.horizontalHeader().height()
        total_height = header_height + (row_height * row_count) + 2

        # Limit max height so scrolling kicks in
        max_height = 300

        self.table.setMaximumHeight(min(total_height, max_height))

    def complete_day(self, task):
        from datetime import date
        today = date.today().isoformat()

        if task.last_completed_date == today:
            return

        if task.days_remaining > 0:
            task.days_completed += 1
            task.last_completed_date = today

            if task.days_completed >= task.total_days:
                self.tasks.remove(task)

            self.refresh_table()
            self.save_tasks()

    def save_tasks(self):
        data = []
        for task in self.tasks:
            data.append({
                "name": task.name,
                "total_hours": task.total_hours,
                "total_days": task.total_days,
                "days_completed": task.days_completed,
                "last_completed_date": task.last_completed_date
            })

        with open("tasks.json", "w") as f:
            json.dump(data, f, indent=4)

    def load_tasks(self):
        if not os.path.exists("tasks.json"):
            return

        self.tasks.clear()

        with open("tasks.json", "r") as f:
            data = json.load(f)

        for item in data:
            task = Task(
                item["name"],
                item["total_hours"],
                item["total_days"]
            )
            task.days_completed = item["days_completed"]
            task.last_completed_date = item.get("last_completed_date", None)
            self.tasks.append(task)

    def edit_task(self, task):
        self.editing_task = task
        self.submit_btn.setText("Update Task")

        self.name_input.setText(task.name)
        self.hours_input.setValue(task.total_hours)
        self.days_input.setValue(task.total_days)

        self.side_panel.show()

    def closeEvent(self, event):
        self.save_tasks()
        event.accept()

# ================= RUN =================

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TaskApp()
    window.showMaximized()
    sys.exit(app.exec_())
