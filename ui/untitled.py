from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(844, 506)
        self.tableWidget = QtWidgets.QTableWidget(Form)
        self.tableWidget.setGeometry(QtCore.QRect(240, 10, 321, 151))
        self.tableWidget.setStyleSheet("QTableWidget::item:hover {\n"
"    color: white;\n"
"    background-color: red;\n"
"}      \n"
"\n"
"QTableWidget::item:selected\n"
"{\n"
"     color: white;\n"
"    background-color: green;\n"
"    \n"
"}\n"
"")
        self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget.setShowGrid(True)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(2)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(0, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(0, 2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(1, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(1, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(1, 2, item)
        self.tableWidget_2 = QtWidgets.QTableWidget(Form)
        self.tableWidget_2.setGeometry(QtCore.QRect(240, 180, 321, 151))
        self.tableWidget_2.setStyleSheet("QTableWidget::item:hover {\n"
"    color: white;\n"
"    background-color: red;\n"
"}      \n"
"\n"
"QTableWidget::item:selected\n"
"{\n"
"     color: white;\n"
"    background-color: green;\n"
"    \n"
"}\n"
"")
        self.tableWidget_2.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableWidget_2.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget_2.setShowGrid(True)
        self.tableWidget_2.setObjectName("tableWidget_2")
        self.tableWidget_2.setColumnCount(3)
        self.tableWidget_2.setRowCount(2)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setItem(0, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setItem(0, 2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setItem(1, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setItem(1, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setItem(1, 2, item)
        self.tableWidget_3 = QtWidgets.QTableWidget(Form)
        self.tableWidget_3.setGeometry(QtCore.QRect(240, 350, 321, 151))
        self.tableWidget_3.setStyleSheet("QTableWidget::item:hover {\n"
"    color: white;\n"
"    background-color: red;\n"
"}      \n"
"\n"
"QTableWidget::item:selected\n"
"{\n"
"     color: white;\n"
"    background-color: green;\n"
"    \n"
"}\n"
"")
        self.tableWidget_3.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableWidget_3.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget_3.setShowGrid(True)
        self.tableWidget_3.setObjectName("tableWidget_3")
        self.tableWidget_3.setColumnCount(3)
        self.tableWidget_3.setRowCount(2)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setItem(0, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setItem(0, 2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setItem(1, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setItem(1, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setItem(1, 2, item)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.tableWidget.setSortingEnabled(True)
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText(_translate("Form", "1"))
        item = self.tableWidget.verticalHeaderItem(1)
        item.setText(_translate("Form", "2"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Form", "0"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Form", "1"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Form", "2"))
        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        item = self.tableWidget.item(0, 1)
        item.setText(_translate("Form", "sssss"))
        item = self.tableWidget.item(0, 2)
        item.setText(_translate("Form", "xxxxxxx"))
        item = self.tableWidget.item(1, 1)
        item.setText(_translate("Form", "ttttt"))
        item = self.tableWidget.item(1, 2)
        item.setText(_translate("Form", "jjjjjj"))
        self.tableWidget.setSortingEnabled(__sortingEnabled)
        self.tableWidget_2.setSortingEnabled(True)
        item = self.tableWidget_2.verticalHeaderItem(0)
        item.setText(_translate("Form", "1"))
        item = self.tableWidget_2.verticalHeaderItem(1)
        item.setText(_translate("Form", "2"))
        item = self.tableWidget_2.horizontalHeaderItem(0)
        item.setText(_translate("Form", "New Column"))
        item = self.tableWidget_2.horizontalHeaderItem(1)
        item.setText(_translate("Form", "1"))
        item = self.tableWidget_2.horizontalHeaderItem(2)
        item.setText(_translate("Form", "2"))
        __sortingEnabled = self.tableWidget_2.isSortingEnabled()
        self.tableWidget_2.setSortingEnabled(False)
        item = self.tableWidget_2.item(0, 1)
        item.setText(_translate("Form", "1111"))
        item = self.tableWidget_2.item(0, 2)
        item.setText(_translate("Form", "2222"))
        item = self.tableWidget_2.item(1, 1)
        item.setText(_translate("Form", "33333"))
        item = self.tableWidget_2.item(1, 2)
        item.setText(_translate("Form", "44444"))
        self.tableWidget_2.setSortingEnabled(__sortingEnabled)
        self.tableWidget_3.setSortingEnabled(True)
        item = self.tableWidget_3.verticalHeaderItem(0)
        item.setText(_translate("Form", "1"))
        item = self.tableWidget_3.verticalHeaderItem(1)
        item.setText(_translate("Form", "2"))
        item = self.tableWidget_3.horizontalHeaderItem(0)
        item.setText(_translate("Form", "0"))
        item = self.tableWidget_3.horizontalHeaderItem(1)
        item.setText(_translate("Form", "1"))
        item = self.tableWidget_3.horizontalHeaderItem(2)
        item.setText(_translate("Form", "2"))
        __sortingEnabled = self.tableWidget_3.isSortingEnabled()
        self.tableWidget_3.setSortingEnabled(False)
        item = self.tableWidget_3.item(0, 1)
        item.setText(_translate("Form", "text1"))
        item = self.tableWidget_3.item(0, 2)
        item.setText(_translate("Form", "num1"))
        item = self.tableWidget_3.item(1, 1)
        item.setText(_translate("Form", "text2"))
        item = self.tableWidget_3.item(1, 2)
        item.setText(_translate("Form", "num2"))
        self.tableWidget_3.setSortingEnabled(__sortingEnabled)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
