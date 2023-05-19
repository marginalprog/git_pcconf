# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\pcconf\ui\help\widgetBodyHelp.ui'
#
# Created by: PyQt5 UI code generator 5.15.5
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_widgetBodyHelp(object):
    def setupUi(self, widgetBodyHelp):
        widgetBodyHelp.setObjectName("widgetBodyHelp")
        widgetBodyHelp.resize(877, 358)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("E:\\pcconf\\ui\\help\\../../images/faq.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        widgetBodyHelp.setWindowIcon(icon)
        widgetBodyHelp.setStyleSheet("QWidget{\n"
"    background-color: rgb(30,30,30);\n"
"    color: white;\n"
"}")
        self.line_2 = QtWidgets.QFrame(widgetBodyHelp)
        self.line_2.setGeometry(QtCore.QRect(10, 220, 20, 61))
        self.line_2.setStyleSheet("border: 0px;\n"
"border-right: 1px solid rgb(210, 0, 0);")
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.btnClose = QtWidgets.QPushButton(widgetBodyHelp)
        self.btnClose.setGeometry(QtCore.QRect(370, 310, 121, 31))
        font = QtGui.QFont()
        font.setFamily("Montserrat Medium")
        font.setPointSize(10)
        self.btnClose.setFont(font)
        self.btnClose.setStyleSheet("QPushButton{\n"
"    border:1px solid rgb(70,70,70);\n"
"    background-color: rgb(40,40,40);\n"
"    color: #fffafa;\n"
"}\n"
"\n"
"QPushButton::hover\n"
"{\n"
"    border:1px;\n"
"    background-color: rgb(60,60,60);\n"
"    border-color: rgb(40,40,40);\n"
"    border-bottom: 1px solid  red;\n"
"    color: red;\n"
"}\n"
"")
        self.btnClose.setObjectName("btnClose")
        self.rectangle = QtWidgets.QFrame(widgetBodyHelp)
        self.rectangle.setGeometry(QtCore.QRect(10, 10, 61, 16))
        self.rectangle.setStyleSheet("background-color: rgb(210, 0, 0);\n"
"border: 1px solid rgb(210, 0, 0);")
        self.rectangle.setFrameShape(QtWidgets.QFrame.HLine)
        self.rectangle.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.rectangle.setObjectName("rectangle")
        self.lbHowVid = QtWidgets.QLabel(widgetBodyHelp)
        self.lbHowVid.setGeometry(QtCore.QRect(40, 30, 311, 31))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(14)
        self.lbHowVid.setFont(font)
        self.lbHowVid.setObjectName("lbHowVid")
        self.line_4 = QtWidgets.QFrame(widgetBodyHelp)
        self.line_4.setGeometry(QtCore.QRect(10, 80, 20, 111))
        self.line_4.setStyleSheet("border: 0px;\n"
"border-right: 1px solid rgb(210, 0, 0);")
        self.line_4.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.lbHowVidTxt = QtWidgets.QLabel(widgetBodyHelp)
        self.lbHowVidTxt.setGeometry(QtCore.QRect(40, 80, 821, 121))
        font = QtGui.QFont()
        font.setFamily("Montserrat Medium")
        font.setPointSize(11)
        self.lbHowVidTxt.setFont(font)
        self.lbHowVidTxt.setStyleSheet("color: rgb(220,220,220);")
        self.lbHowVidTxt.setTextFormat(QtCore.Qt.PlainText)
        self.lbHowVidTxt.setScaledContents(False)
        self.lbHowVidTxt.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignTop)
        self.lbHowVidTxt.setWordWrap(True)
        self.lbHowVidTxt.setOpenExternalLinks(False)
        self.lbHowVidTxt.setObjectName("lbHowVidTxt")
        self.lbHowVidTxt_2 = QtWidgets.QLabel(widgetBodyHelp)
        self.lbHowVidTxt_2.setGeometry(QtCore.QRect(40, 220, 821, 71))
        font = QtGui.QFont()
        font.setFamily("Montserrat Medium")
        font.setPointSize(11)
        self.lbHowVidTxt_2.setFont(font)
        self.lbHowVidTxt_2.setStyleSheet("color: rgb(220,220,220);")
        self.lbHowVidTxt_2.setTextFormat(QtCore.Qt.PlainText)
        self.lbHowVidTxt_2.setScaledContents(False)
        self.lbHowVidTxt_2.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignTop)
        self.lbHowVidTxt_2.setWordWrap(True)
        self.lbHowVidTxt_2.setOpenExternalLinks(False)
        self.lbHowVidTxt_2.setObjectName("lbHowVidTxt_2")

        self.retranslateUi(widgetBodyHelp)
        self.btnClose.clicked.connect(widgetBodyHelp.close)
        QtCore.QMetaObject.connectSlotsByName(widgetBodyHelp)

    def retranslateUi(self, widgetBodyHelp):
        _translate = QtCore.QCoreApplication.translate
        widgetBodyHelp.setWindowTitle(_translate("widgetBodyHelp", "Подобрать корпус"))
        self.btnClose.setText(_translate("widgetBodyHelp", "Закрыть"))
        self.lbHowVid.setText(_translate("widgetBodyHelp", "Как подобрать корпус?"))
        self.lbHowVidTxt.setText(_translate("widgetBodyHelp", "Корпус - представляет собой базовую несущую конструкцию, которая предназначена для последующего наполнения аппаратным обеспечением с целью создания компьютера. Часто разделяется на \"Игровой\" и \"Неигровой\" - из-за особенностей конструкции, позволяющих крепить дополнительное охлаждение в виде вентиляторов, водяное охлаждение, а также подсветку. Также на данные параметры влияет вид и дизайн корпуса."))
        self.lbHowVidTxt_2.setText(_translate("widgetBodyHelp", "При выборе корпуса прежде всего следует обратить внимание на допустимые для размещения внутри форматы блоков питания, материнских плат, а также их габариты (длина, высота). Также важным может быть факт массы и типоразмера самого корпуса."))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widgetBodyHelp = QtWidgets.QWidget()
    ui = Ui_widgetBodyHelp()
    ui.setupUi(widgetBodyHelp)
    widgetBodyHelp.show()
    sys.exit(app.exec_())