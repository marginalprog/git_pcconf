# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\pcconf\ui\help\widgetDiskHelp.ui'
#
# Created by: PyQt5 UI code generator 5.15.5
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_widgetDiskHelp(object):
    def setupUi(self, widgetDiskHelp):
        widgetDiskHelp.setObjectName("widgetDiskHelp")
        widgetDiskHelp.resize(892, 686)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("E:\\pcconf\\ui\\help\\../../images/faq.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        widgetDiskHelp.setWindowIcon(icon)
        widgetDiskHelp.setStyleSheet("QWidget{\n"
"    background-color: rgb(30,30,30);\n"
"    color: white;\n"
"}")
        self.lbGeForce = QtWidgets.QLabel(widgetDiskHelp)
        self.lbGeForce.setGeometry(QtCore.QRect(40, 360, 381, 261))
        font = QtGui.QFont()
        font.setFamily("Montserrat Medium")
        font.setPointSize(10)
        self.lbGeForce.setFont(font)
        self.lbGeForce.setAutoFillBackground(False)
        self.lbGeForce.setStyleSheet("color: rgb(220,220,220);")
        self.lbGeForce.setTextFormat(QtCore.Qt.PlainText)
        self.lbGeForce.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignTop)
        self.lbGeForce.setWordWrap(True)
        self.lbGeForce.setObjectName("lbGeForce")
        self.line = QtWidgets.QFrame(widgetDiskHelp)
        self.line.setGeometry(QtCore.QRect(10, 360, 20, 251))
        self.line.setStyleSheet("border: 0px;\n"
"border-right: 1px solid rgb(210, 0, 0);")
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.lbHowVid = QtWidgets.QLabel(widgetDiskHelp)
        self.lbHowVid.setGeometry(QtCore.QRect(40, 30, 281, 31))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(14)
        self.lbHowVid.setFont(font)
        self.lbHowVid.setObjectName("lbHowVid")
        self.lbHowVidTxt = QtWidgets.QLabel(widgetDiskHelp)
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
        self.lbNvidia = QtWidgets.QLabel(widgetDiskHelp)
        self.lbNvidia.setGeometry(QtCore.QRect(40, 310, 151, 31))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(13)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.lbNvidia.setFont(font)
        self.lbNvidia.setObjectName("lbNvidia")
        self.rectangle = QtWidgets.QFrame(widgetDiskHelp)
        self.rectangle.setGeometry(QtCore.QRect(10, 10, 61, 16))
        self.rectangle.setStyleSheet("background-color: rgb(210, 0, 0);\n"
"border: 1px solid rgb(210, 0, 0);")
        self.rectangle.setFrameShape(QtWidgets.QFrame.HLine)
        self.rectangle.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.rectangle.setObjectName("rectangle")
        self.line_3 = QtWidgets.QFrame(widgetDiskHelp)
        self.line_3.setGeometry(QtCore.QRect(460, 360, 20, 261))
        self.line_3.setStyleSheet("border: 0px;\n"
"border-right: 1px solid rgb(210, 0, 0);")
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.line_4 = QtWidgets.QFrame(widgetDiskHelp)
        self.line_4.setGeometry(QtCore.QRect(10, 80, 20, 81))
        self.line_4.setStyleSheet("border: 0px;\n"
"border-right: 1px solid rgb(210, 0, 0);")
        self.line_4.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.lbHowVidTxt_2 = QtWidgets.QLabel(widgetDiskHelp)
        self.lbHowVidTxt_2.setGeometry(QtCore.QRect(40, 190, 821, 101))
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
        self.line_2 = QtWidgets.QFrame(widgetDiskHelp)
        self.line_2.setGeometry(QtCore.QRect(10, 190, 20, 101))
        self.line_2.setStyleSheet("border: 0px;\n"
"border-right: 1px solid rgb(210, 0, 0);")
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.lbAmd = QtWidgets.QLabel(widgetDiskHelp)
        self.lbAmd.setGeometry(QtCore.QRect(490, 310, 151, 31))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(13)
        self.lbAmd.setFont(font)
        self.lbAmd.setObjectName("lbAmd")
        self.lbRadeon = QtWidgets.QLabel(widgetDiskHelp)
        self.lbRadeon.setGeometry(QtCore.QRect(490, 360, 381, 271))
        font = QtGui.QFont()
        font.setFamily("Montserrat Medium")
        font.setPointSize(10)
        self.lbRadeon.setFont(font)
        self.lbRadeon.setAutoFillBackground(False)
        self.lbRadeon.setStyleSheet("color: rgb(220,220,220);")
        self.lbRadeon.setTextFormat(QtCore.Qt.PlainText)
        self.lbRadeon.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignTop)
        self.lbRadeon.setWordWrap(True)
        self.lbRadeon.setObjectName("lbRadeon")
        self.btnClose = QtWidgets.QPushButton(widgetDiskHelp)
        self.btnClose.setGeometry(QtCore.QRect(390, 640, 121, 31))
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

        self.retranslateUi(widgetDiskHelp)
        self.btnClose.clicked.connect(widgetDiskHelp.close)
        QtCore.QMetaObject.connectSlotsByName(widgetDiskHelp)

    def retranslateUi(self, widgetDiskHelp):
        _translate = QtCore.QCoreApplication.translate
        widgetDiskHelp.setWindowTitle(_translate("widgetDiskHelp", "Подобрать накопитель"))
        self.lbGeForce.setText(_translate("widgetDiskHelp", "Жесткие диски или HDD представляют собой типы накопителей данных, запись на которые осуществляется путем намагничивания отдельный участков пластин. Эти устройства имеют алюминиевую, стеклянную или керамическую поверхность, покрытую ферромагнетиком.\n"
"Чтобы организовать хранение информации, магнитные диски разбивают на сектора и дорожки. Совокупность вторых элементов, которые на нескольких дисках находятся друг над другом, называют цилиндрами. Скорость, при этом, может варьироваться в диапазоне 4 — 15 тыс. оборотов/минуту (rpm). Запись данных и их считывание с пластины осуществляет магнитная головка."))
        self.lbHowVid.setText(_translate("widgetDiskHelp", "Как подобрать накопитель?"))
        self.lbHowVidTxt.setText(_translate("widgetDiskHelp", "Накопитель - это  устройство для хранения информации. Используется в персональных компьютерах, ноутбуках, системах видеонаблюдения. В отличие от оперативной памяти работает медленнее, но отличается большим объемом памяти и надежностью."))
        self.lbNvidia.setText(_translate("widgetDiskHelp", "3.5 HDD"))
        self.lbHowVidTxt_2.setText(_translate("widgetDiskHelp", "При выборе накопителя нужно обратить внимание на такие параметры, как: \n"
"-тип накопителя (HDD или SSD),  \n"
"-типоразмер(2.5\" - 3.5\"); \n"
"-скорость вращения головки (в случае винчестера): \n"
"-скорость записи/чтения данных."))
        self.lbAmd.setText(_translate("widgetDiskHelp", "2.5 SSD"))
        self.lbRadeon.setText(_translate("widgetDiskHelp", "Твердотельный накопитель — компьютерное энергонезависимое немеханическое запоминающее устройство на основе микросхем памяти, альтернатива жёстким дискам (HDD). \n"
"По сравнению с традиционными жёсткими дисками твердотельные накопители имеют меньший размер и вес, являются бесшумными, а также многократно более устойчивы к повреждениям (например, при падении) и имеют гораздо бóльшую скорость производимых операций. В то же время, они имеют в несколько раз бóльшую стоимость в пересчёте на гигабайт и меньшую износостойкость (ресурс записи).\n"
"Не так просто подвергаются восстановлению данных, в отличие от HDD."))
        self.btnClose.setText(_translate("widgetDiskHelp", "Закрыть"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widgetDiskHelp = QtWidgets.QWidget()
    ui = Ui_widgetDiskHelp()
    ui.setupUi(widgetDiskHelp)
    widgetDiskHelp.show()
    sys.exit(app.exec_())