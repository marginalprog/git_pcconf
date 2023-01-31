import sys

from PyQt5 import QtWidgets, QtCore, QtGui
from ui import untitled


class MainWindow(QtWidgets.QMainWindow, untitled.Ui_Form):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = untitled.Ui_Form()
        self.setupUi(self)

        self.insert_rb(self.tableWidget)

    def create_radioButton(self):  # Метод создания рб на виджете
        widget = QtWidgets.QWidget()
        rb = QtWidgets.QRadioButton()
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