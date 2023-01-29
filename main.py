import sys

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QDialog, QTableWidgetItem
from PyQt5.QtGui import QIcon, QPixmap
from ui import main_interface
from ui import untitled


class RadioButton(QtWidgets.QRadioButton):
    def __init__(self, parent=None):
        super(RadioButton, self).__init__(parent)
        self.pixmap = QPixmap("E:\pcconf\images\off.png")
        self.pixmap_pressed = QPixmap("E:\pcconf\images\on.png")
        #self.setText('rb0')

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
        self.setWindowTitle('Конфигуратор ПК')
        self.pushButton.clicked.connect(lambda: print('работает'))

        testPrice = "33500"
        item = QTableWidgetItem(testPrice)  # create the item
        item.setTextAlignment(QtCore.Qt.AlignVCenter)

        self.table_config.setItem(0, 1, item)

        self.table_config.setColumnWidth(0, 170)
        self.table_config.setColumnWidth(1, 55)
        self.table_config.setColumnWidth(2, 15)

        for i in range(self.tableConfNvidia.rowCount()):
            self.insert_rb(i, self.tableConfNvidia)



    def create_radioButton(self,):  # Метод создания рб на виджете
        widget = QtWidgets.QWidget()
        rb = RadioButton()
        pLayout = QtWidgets.QHBoxLayout(widget)
        pLayout.addWidget(rb)
        pLayout.setAlignment(QtCore.Qt.AlignCenter)
        pLayout.setContentsMargins(0, 0, 0, 0)
        #pRadioButton.setStyleSheet('border-image: url("E:/pcconf/images/closed.png") 0;')
        widget.setLayout(pLayout)
        return widget, rb

    def insert_rb(self, row_id, table):
        row_count = table.rowCount()
        col_count = table.columnCount()
        widget, radio = self.create_radioButton()
        radio.toggled.connect(lambda: self.currentPos(table, row_count))

        table.setCellWidget(row_id, 0, widget)

    def currentPos(self, table, row_count):
        rbClick = QtWidgets.qApp.focusWidget()
        index = table.indexAt(rbClick.parent().pos())
        if index.isValid():
            print(index.row(), index.column())
            for i in range(row_count):
               if i != index.row():
                    widget, radio = self.create_radioButton()
                    radio.toggled.connect(lambda: self.currentPos(table, row_count))
                    table.setCellWidget(i, 0, widget)
                    #item = table.item(i, 0)
                    #item.setCheckState(False)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()