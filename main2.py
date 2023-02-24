import sys

from PyQt5 import QtWidgets, QtCore
from ui import untitled


class MainWindow(QtWidgets.QMainWindow, untitled.Ui_Form):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.dict_button_group = {}

        self.tableWidget.cellClicked.connect(
            lambda row, column, table=self.tableWidget:
            self.cell_row(row, column, table))

        self.tableWidget_2.cellClicked.connect(
            lambda row, column, table=self.tableWidget_2:
            self.cell_row(row, column, table))

        self.tableWidget_3.cellClicked.connect(
            lambda row, column, table=self.tableWidget_3:
            self.cell_row(row, column, table))

        self.insert_rb(self.tableWidget)
        self.insert_rb(self.tableWidget_2)
        self.insert_rb(self.tableWidget_3)

    def create_radioButton(self):
        widget = QtWidgets.QWidget()
        rb = QtWidgets.QRadioButton()
        pLayout = QtWidgets.QHBoxLayout(widget)
        pLayout.addWidget(rb)
        pLayout.setAlignment(QtCore.Qt.AlignCenter)
        pLayout.setContentsMargins(0, 0, 0, 0)
        widget.setLayout(pLayout)
        return widget, rb

    def cell_row(self, row, column, table):
        #print(f'\n row={row}; column={column}')
        #self.row_selected = row
        #rb = self.button_group.button(row)
        button_group = self.dict_button_group[table.objectName()]
        rb = button_group.button(row)
        rb.click()

    def insert_rb(self, table):
        row_count = table.rowCount()

        button_group = QtWidgets.QButtonGroup(self)
        button_group.setExclusive(True)

        for i in range(row_count):
            widget, radio = self.create_radioButton()
            radio.toggled.connect(
                lambda ch, row=i: self.currentPos(ch, row, table))
            table.setCellWidget(i, 0, widget)

            button_group.addButton(radio)
            button_group.setId(radio, i)
        self.dict_button_group[table.objectName()] = button_group

    def currentPos(self, ch, row, table):
        # print(f' row = {row} -- {ch}')
        if ch:
            # self.row_selected = row
            table.selectRow(row)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
