# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\pcconf\ui\warningWin.ui'
#
# Created by: PyQt5 UI code generator 5.15.5
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_warningDialog(object):
    def setupUi(self, warningDialog):
        warningDialog.setObjectName("warningDialog")
        warningDialog.resize(340, 181)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("E:\\pcconf\\ui\\../images/warning.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        warningDialog.setWindowIcon(icon)
        warningDialog.setStyleSheet("QWidget\n"
"{\n"
"     background: rgb(25, 25, 25);\n"
"    color: white;\n"
"\n"
"}\n"
"")
        self.line = QtWidgets.QFrame(warningDialog)
        self.line.setGeometry(QtCore.QRect(10, 70, 321, 20))
        self.line.setStyleSheet("border:0px;\n"
"border-top: 1px solid rgb(180, 0, 0);")
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.lbErr = QtWidgets.QLabel(warningDialog)
        self.lbErr.setGeometry(QtCore.QRect(10, 40, 61, 21))
        font = QtGui.QFont()
        font.setFamily("Montserrat SemiBold")
        font.setPointSize(10)
        self.lbErr.setFont(font)
        self.lbErr.setStyleSheet("border:0px;")
        self.lbErr.setObjectName("lbErr")
        self.lbErrDescription = QtWidgets.QLabel(warningDialog)
        self.lbErrDescription.setGeometry(QtCore.QRect(10, 80, 321, 31))
        font = QtGui.QFont()
        font.setFamily("Montserrat Medium")
        font.setPointSize(10)
        self.lbErrDescription.setFont(font)
        self.lbErrDescription.setStyleSheet("border:0px;")
        self.lbErrDescription.setAlignment(QtCore.Qt.AlignCenter)
        self.lbErrDescription.setWordWrap(True)
        self.lbErrDescription.setObjectName("lbErrDescription")
        self.rectangle = QtWidgets.QFrame(warningDialog)
        self.rectangle.setGeometry(QtCore.QRect(10, 10, 61, 16))
        self.rectangle.setStyleSheet("border:0px;\n"
"background-color: rgb(180, 0, 0);\n"
"border: 1px solid rgb(180, 0, 0);")
        self.rectangle.setFrameShape(QtWidgets.QFrame.HLine)
        self.rectangle.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.rectangle.setObjectName("rectangle")
        self.btnCancel = QtWidgets.QPushButton(warningDialog)
        self.btnCancel.setGeometry(QtCore.QRect(110, 140, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Montserrat Medium")
        font.setPointSize(10)
        self.btnCancel.setFont(font)
        self.btnCancel.setStyleSheet("QPushButton{\n"
"    background-color: rgb(40,40,40);\n"
"    color: #fffafa;\n"
"}\n"
"\n"
"QPushButton::hover\n"
"{\n"
"    color: red;\n"
"    background-color: rgb(50,50,50);\n"
"    border-bottom: 1px solid red;\n"
"}\n"
"")
        self.btnCancel.setObjectName("btnCancel")
        self.line_2 = QtWidgets.QFrame(warningDialog)
        self.line_2.setGeometry(QtCore.QRect(10, 120, 321, 20))
        self.line_2.setStyleSheet("border:0px;\n"
"border-top: 1px solid rgb(180, 0, 0);")
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.line.raise_()
        self.lbErrDescription.raise_()
        self.lbErr.raise_()
        self.rectangle.raise_()
        self.btnCancel.raise_()
        self.line_2.raise_()

        self.retranslateUi(warningDialog)
        QtCore.QMetaObject.connectSlotsByName(warningDialog)

    def retranslateUi(self, warningDialog):
        _translate = QtCore.QCoreApplication.translate
        warningDialog.setWindowTitle(_translate("warningDialog", "Dialog"))
        self.lbErr.setText(_translate("warningDialog", "Ошибка"))
        self.lbErrDescription.setText(_translate("warningDialog", "[Описание ошибки]"))
        self.btnCancel.setText(_translate("warningDialog", "Отмена"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    warningDialog = QtWidgets.QDialog()
    ui = Ui_warningDialog()
    ui.setupUi(warningDialog)
    warningDialog.show()
    sys.exit(app.exec_())