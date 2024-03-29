# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\pcconf\ui\help\widgetMotherHelp.ui'
#
# Created by: PyQt5 UI code generator 5.15.5
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_widgetMotherHelp(object):
    def setupUi(self, widgetMotherHelp):
        widgetMotherHelp.setObjectName("widgetMotherHelp")
        widgetMotherHelp.resize(896, 386)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("E:\\pcconf\\ui\\help\\../../images/faq.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        widgetMotherHelp.setWindowIcon(icon)
        widgetMotherHelp.setStyleSheet("QWidget{\n"
"    background-color: rgb(30,30,30);\n"
"    color: white;\n"
"}")
        self.lbHowVid = QtWidgets.QLabel(widgetMotherHelp)
        self.lbHowVid.setGeometry(QtCore.QRect(40, 30, 361, 31))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(14)
        self.lbHowVid.setFont(font)
        self.lbHowVid.setObjectName("lbHowVid")
        self.lbHowVidTxt = QtWidgets.QLabel(widgetMotherHelp)
        self.lbHowVidTxt.setGeometry(QtCore.QRect(40, 80, 821, 91))
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
        self.rectangle = QtWidgets.QFrame(widgetMotherHelp)
        self.rectangle.setGeometry(QtCore.QRect(20, 10, 61, 16))
        self.rectangle.setStyleSheet("background-color: rgb(210, 0, 0);\n"
"border: 1px solid rgb(210, 0, 0);")
        self.rectangle.setFrameShape(QtWidgets.QFrame.HLine)
        self.rectangle.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.rectangle.setObjectName("rectangle")
        self.line_4 = QtWidgets.QFrame(widgetMotherHelp)
        self.line_4.setGeometry(QtCore.QRect(10, 80, 20, 81))
        self.line_4.setStyleSheet("border: 0px;\n"
"border-right: 1px solid rgb(210, 0, 0);")
        self.line_4.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.lbHowVidTxt_2 = QtWidgets.QLabel(widgetMotherHelp)
        self.lbHowVidTxt_2.setGeometry(QtCore.QRect(40, 190, 821, 131))
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
        self.line_2 = QtWidgets.QFrame(widgetMotherHelp)
        self.line_2.setGeometry(QtCore.QRect(10, 190, 20, 131))
        self.line_2.setStyleSheet("border: 0px;\n"
"border-right: 1px solid rgb(210, 0, 0);")
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.btnClose = QtWidgets.QPushButton(widgetMotherHelp)
        self.btnClose.setGeometry(QtCore.QRect(390, 340, 121, 31))
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

        self.retranslateUi(widgetMotherHelp)
        self.btnClose.clicked.connect(widgetMotherHelp.close)
        QtCore.QMetaObject.connectSlotsByName(widgetMotherHelp)

    def retranslateUi(self, widgetMotherHelp):
        _translate = QtCore.QCoreApplication.translate
        widgetMotherHelp.setWindowTitle(_translate("widgetMotherHelp", "Подобрать мат. плату"))
        self.lbHowVid.setText(_translate("widgetMotherHelp", "Как подобрать материнскую плату?"))
        self.lbHowVidTxt.setText(_translate("widgetMotherHelp", "Материнская плата — печатная плата, которая связывает все комплектующие компьютера между собой и питает их. Она выполняет множество процессов и объединяет все компоненты ПК в единую систему. От параметров материнской платы зависит то, насколько производительными будут другие компоненты системы, и получится ли их вообще установить в ПК."))
        self.lbHowVidTxt_2.setText(_translate("widgetMotherHelp", "При выборе материнской платы следует обратить внимание на: \n"
"-сокет (разъём под процессор), \n"
"-чипсет (набор микросхем, раскрывающий работу процессора, ОЗУ и периферии), \n"
"-версия PCI-e (от неё зависит КПД видеокарты), \n"
"-тип и количество слотов, максимальный объём и частота оперативной памяти (данные параметры ограничиваются шинами материнской платы)."))
        self.btnClose.setText(_translate("widgetMotherHelp", "Закрыть"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widgetMotherHelp = QtWidgets.QWidget()
    ui = Ui_widgetMotherHelp()
    ui.setupUi(widgetMotherHelp)
    widgetMotherHelp.show()
    sys.exit(app.exec_())
