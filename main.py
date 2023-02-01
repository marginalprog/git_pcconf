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
        #self.ui = main_interface.Ui_MainWindow()
        self.setupUi(self)
        self.setWindowTitle("Конфигуратор ПК")
        self.pushButton.clicked.connect(lambda: print("работает"))

        testPrice = "33500"
        item = QTableWidgetItem(testPrice)
        item.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)

        self.table_config.setItem(0, 1, item)

        self.table_config.setColumnWidth(0, 170)
        self.table_config.setColumnWidth(1, 55)
        self.table_config.setColumnWidth(2, 15)

        self.tableConfVideo.setColumnWidth(0, 50)
        self.tableConfVideo.setColumnWidth(1, 40)
        self.tableConfVideo.setColumnWidth(2, 180)
        self.tableConfVideo.setColumnWidth(3, 180)
        self.tableConfVideo.cellClicked.connect(self.cell_row)
        self.row_selected = None
        self.insert_rb(self.tableConfVideo)
        ''' в дальнейшем existence будет из строк БД принимать true|false
         и вставлять соответствующее в таблицу состояние комплектующего'''
        self.existence(self.tableConfVideo, True)

    #  метод создания индикатора состояния комплектующего
    def create_existence(self, png_way):
        widget = QtWidgets.QWidget()
        pLayout = QtWidgets.QHBoxLayout(widget)
        pixmap = QPixmap(png_way)
        lbl = QtWidgets.QLabel()
        lbl.setPixmap(pixmap)
        pLayout.addWidget(lbl)
        pLayout.setAlignment(QtCore.Qt.AlignCenter)
        pLayout.setContentsMargins(0, 0, 0, 0)
        widget.setLayout(pLayout)
        return widget

    # метод заполнения ячейки с состоянием
    def existence(self, table, bool_sklad):
        row_count = table.rowCount()
        for i in range(row_count):
            if bool_sklad:
                table.setCellWidget(i, 1, self.create_existence("E:/pcconf/images/have.png"))
            else:
                table.setCellWidget(i, 1, self.create_existence("E:/pcconf/images/nothave.png"))

    # Метод создания рб на виджете
    def create_radioButton(self):
        widget = QtWidgets.QWidget()
        rb = RadioButton()
        pLayout = QtWidgets.QHBoxLayout(widget)
        pLayout.addWidget(rb)
        pLayout.setAlignment(QtCore.Qt.AlignCenter)
        pLayout.setContentsMargins(0, 0, 0, 0)
        widget.setLayout(pLayout)
        return widget, rb

    def cell_row(self, row, column):
        # print(f'\n row={row}; column={column}')
        self.row_selected = row
        rb = self.button_group.button(row)
        rb.click()

    # метод вставки в таблицу рб-шек
    def insert_rb(self, table):
        row_count = table.rowCount()

        self.button_group = QtWidgets.QButtonGroup(self)
        self.button_group.setExclusive(True)

        for i in range(row_count):
            widget, radio = self.create_radioButton()
            radio.toggled.connect(lambda ch, row=i: self.currentPos(ch, row, table))
            table.setCellWidget(i, 0, widget)

            self.button_group.addButton(radio)
            self.button_group.setId(radio, i)

    def currentPos(self, ch, row, table):
        # print(f' row = {row} -- {ch}')
        if ch:
            self.row_selected = row
            table.selectRow(row)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
