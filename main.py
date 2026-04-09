import sys
from PyQt5.QtWidgets import QApplication, QTabWidget
from TaskApp import TaskApp
from ShowApp import ShowApp

if __name__ == "__main__":
    app = QApplication(sys.argv)

    tabs = QTabWidget()
    tabs.addTab(TaskApp(), "Tasks")
    tabs.addTab(ShowApp(), "Shows")

    tabs.setWindowTitle("Planner")
    tabs.resize(1000, 600)
    tabs.showMaximized()  # optional

    sys.exit(app.exec_())