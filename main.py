import sys
# pip freeze > requirements.txt
# pip install -r requirements.txt
from PyQt5.QtWidgets import QApplication
from TaskApp import TaskApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TaskApp()
    window.showMaximized()
    sys.exit(app.exec_())
