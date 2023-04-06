import sys

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QDialog, QTableWidgetItem
# ----------файлы интерфейса---------------
from ui.add import addChVidWidg


# Класс окна с добавлением\редактированием видеокарты
class AddChangeVideoWindow(QtWidgets.QWidget, addChVidWidg.Ui_addChVidWidg):
    def __init__(self, new_bool):
        super().__init__()
        self.setupUi(self)
        self.btnVidCancel.clicked.connect(lambda: self.close())
        if new_bool:
            self.setWindowTitle("Создание заказа")
        else:
            self.setWindowTitle("Повторный заказ")
