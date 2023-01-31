import sys

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QDialog, QTableWidgetItem
from PyQt5.QtGui import QIcon, QPixmap
from ui import main_interface
from ui import untitled


class RadioButton(QtWidgets.QRadioButton):
    def __init__(self, parent=None):
        super(RadioButton, self).__init__(parent)
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


class MainWindow(QtWidgets.QMainWindow, main_interface.Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = main_interface.Ui_MainWindow()
        self.setupUi(self)
        self.setWindowTitle("Конфигуратор ПК")
        self.pushButton.clicked.connect(lambda: print("работает"))

        testPrice = "33500"
        item = QTableWidgetItem(testPrice)  # create the item
        item.setTextAlignment(QtCore.Qt.AlignVCenter)

        self.table_config.setItem(0, 1, item)

        self.table_config.setColumnWidth(0, 170)
        self.table_config.setColumnWidth(1, 55)
        self.table_config.setColumnWidth(2, 15)

        self.insert_rb(self.tableConfNvidia)
        self.existence(self.tableConfNvidia, True)

    def existence(self, table, bool_sklad):
        widget = QtWidgets.QWidget()
        pLayout = QtWidgets.QHBoxLayout(widget)
        row_count = table.rowCount()
        for i in range(row_count):
            if bool_sklad:
                pixmap = QPixmap("E:/pcconf/images/have.png")
                lbl = QtWidgets.QLabel()
                lbl.setPixmap(pixmap)
                pLayout.addWidget(lbl)
                pLayout.setAlignment(QtCore.Qt.AlignCenter)
                pLayout.setContentsMargins(0, 0, 0, 0)
                widget.setLayout(pLayout)
                table.setCellWidget(i, 1, widget)
            else:
                pixmap = QPixmap("E:/pcconf/images/nothave.png")
                lbl = QtWidgets.QLabel()
                lbl.setPixmap(pixmap)
                pLayout.addWidget(lbl)
                pLayout.setAlignment(QtCore.Qt.AlignCenter)
                pLayout.setContentsMargins(0, 0, 0, 0)
                widget.setLayout(pLayout)
                table.setCellWidget(i, 1, widget)

    def create_radioButton(self):  # Метод создания рб на виджете
        widget = QtWidgets.QWidget()
        rb = RadioButton()
        pLayout = QtWidgets.QHBoxLayout(widget)
        pLayout.addWidget(rb)
        pLayout.setAlignment(QtCore.Qt.AlignCenter)
        pLayout.setContentsMargins(0, 0, 0, 0)
        widget.setLayout(pLayout)
        return widget, rb

    def insert_rb(self, table):
        row_count = table.rowCount()
        for i in range(row_count):
            widget, radio = self.create_radioButton()
            radio.toggled.connect(lambda: self.currentPos(table, row_count))
            table.setCellWidget(i, 0, widget)

    def currentPos(self, table, row_count):
        rbClick = QtWidgets.qApp.focusWidget()
        index = table.indexAt(rbClick.parent().pos())
        columns = table.columnCount()
        if index.isValid():
            print(index.row(), index.column())
            table.selectRow(index.row())
            print(table.item(index.row(), 2).text())
            for i in range(row_count):
                if i != index.row():
                    widget, radio = self.create_radioButton()
                    radio.toggled.connect(lambda: self.currentPos(table, row_count))
                    table.setCellWidget(i, 0, widget)
                    # item = table.item(i, 0)
                    # item.setCheckState(False)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
