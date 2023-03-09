import sys

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QDialog, QTableWidgetItem
# ----------файлы интерфейса---------------
from ui.help import widgetVideoHelp


# -----------Классы окон с подсказкой-------------
class VideoHelp(QtWidgets.QWidget, widgetVideoHelp.Ui_widgetVideoHelp):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
