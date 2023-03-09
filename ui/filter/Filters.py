import sys

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QDialog, QTableWidgetItem
from PyQt5.QtGui import QPixmap
# ----------файлы интерфейса---------------
from ui.filter import widgetVideoFilter


class CheckBox(QtWidgets.QRadioButton):
    def __init__(self, parent=None):
        super(CheckBox, self).__init__(parent)
        self.pixmap = QPixmap("E:/pcconf/images/off.png")
        self.pixmap_pressed = QPixmap("E:/pcconf/images/on.png")

    def paintEvent(self, event):
        if self.isChecked():
            pix = self.pixmap_pressed
        else:
            pix = self.pixmap
        painter = QtGui.QPainter(self)
        painter.drawPixmap(event.rect(), pix)

    def sizeHint(self):
        return QtCore.QSize(15, 15)


class VideoFilter(QtWidgets.QWidget, widgetVideoFilter.Ui_WidgetVideoFilter):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
