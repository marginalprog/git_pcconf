# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\pcconf\ui\help\widgetVideoHelp.ui'
#
# Created by: PyQt5 UI code generator 5.15.5
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_widgetVideoHelp(object):
    def setupUi(self, widgetVideoHelp):
        widgetVideoHelp.setObjectName("widgetVideoHelp")
        widgetVideoHelp.setWindowModality(QtCore.Qt.NonModal)
        widgetVideoHelp.resize(899, 645)
        font = QtGui.QFont()
        font.setFamily("Montserrat Medium")
        font.setPointSize(10)
        widgetVideoHelp.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("E:\\pcconf\\ui\\help\\../../images/faq.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        widgetVideoHelp.setWindowIcon(icon)
        widgetVideoHelp.setStyleSheet("QWidget{\n"
"    background-color: rgb(30,30,30);\n"
"    color: white;\n"
"}")
        self.lbHowVid = QtWidgets.QLabel(widgetVideoHelp)
        self.lbHowVid.setGeometry(QtCore.QRect(40, 30, 281, 31))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(14)
        self.lbHowVid.setFont(font)
        self.lbHowVid.setObjectName("lbHowVid")
        self.lbHowVidTxt = QtWidgets.QLabel(widgetVideoHelp)
        self.lbHowVidTxt.setGeometry(QtCore.QRect(40, 80, 821, 191))
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
        self.rectangle = QtWidgets.QFrame(widgetVideoHelp)
        self.rectangle.setGeometry(QtCore.QRect(10, 10, 61, 16))
        self.rectangle.setStyleSheet("background-color: rgb(210, 0, 0);\n"
"border: 1px solid rgb(210, 0, 0);")
        self.rectangle.setFrameShape(QtWidgets.QFrame.HLine)
        self.rectangle.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.rectangle.setObjectName("rectangle")
        self.lbNvidia = QtWidgets.QLabel(widgetVideoHelp)
        self.lbNvidia.setGeometry(QtCore.QRect(40, 290, 151, 31))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(13)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.lbNvidia.setFont(font)
        self.lbNvidia.setObjectName("lbNvidia")
        self.lbGeForce = QtWidgets.QLabel(widgetVideoHelp)
        self.lbGeForce.setGeometry(QtCore.QRect(40, 340, 381, 241))
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
        self.lbRadeon = QtWidgets.QLabel(widgetVideoHelp)
        self.lbRadeon.setGeometry(QtCore.QRect(490, 350, 381, 211))
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
        self.lbAmd = QtWidgets.QLabel(widgetVideoHelp)
        self.lbAmd.setGeometry(QtCore.QRect(490, 290, 151, 31))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(13)
        self.lbAmd.setFont(font)
        self.lbAmd.setObjectName("lbAmd")
        self.btnClose = QtWidgets.QPushButton(widgetVideoHelp)
        self.btnClose.setGeometry(QtCore.QRect(390, 600, 121, 31))
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
        self.line = QtWidgets.QFrame(widgetVideoHelp)
        self.line.setGeometry(QtCore.QRect(10, 340, 20, 231))
        self.line.setStyleSheet("border: 0px;\n"
"border-right: 1px solid rgb(210, 0, 0);")
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.line_2 = QtWidgets.QFrame(widgetVideoHelp)
        self.line_2.setGeometry(QtCore.QRect(10, 190, 20, 81))
        self.line_2.setStyleSheet("border: 0px;\n"
"border-right: 1px solid rgb(210, 0, 0);")
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.line_3 = QtWidgets.QFrame(widgetVideoHelp)
        self.line_3.setGeometry(QtCore.QRect(460, 340, 20, 231))
        self.line_3.setStyleSheet("border: 0px;\n"
"border-right: 1px solid rgb(210, 0, 0);")
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.line_4 = QtWidgets.QFrame(widgetVideoHelp)
        self.line_4.setGeometry(QtCore.QRect(10, 80, 20, 81))
        self.line_4.setStyleSheet("border: 0px;\n"
"border-right: 1px solid rgb(210, 0, 0);")
        self.line_4.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.lbHowVid.raise_()
        self.lbHowVidTxt.raise_()
        self.rectangle.raise_()
        self.lbNvidia.raise_()
        self.lbRadeon.raise_()
        self.lbAmd.raise_()
        self.btnClose.raise_()
        self.line.raise_()
        self.line_2.raise_()
        self.lbGeForce.raise_()
        self.line_3.raise_()
        self.line_4.raise_()

        self.retranslateUi(widgetVideoHelp)
        self.btnClose.clicked.connect(widgetVideoHelp.close)
        QtCore.QMetaObject.connectSlotsByName(widgetVideoHelp)

    def retranslateUi(self, widgetVideoHelp):
        _translate = QtCore.QCoreApplication.translate
        widgetVideoHelp.setWindowTitle(_translate("widgetVideoHelp", "Подобрать видеокарту"))
        self.lbHowVid.setText(_translate("widgetVideoHelp", "Как подобрать видеокарту?"))
        self.lbHowVidTxt.setText(_translate("widgetVideoHelp", "Видеокарта – это устройство, преобразующее графический образ, хранящийся как содержимое памяти компьютера (или самого адаптера), в форму, пригодную для дальнейшего вывода на экран монитора.\n"
"Наша компания предоставляет видеокарты с чипами от NVIDIA GeForce и AMD Radeon.\n"
"\n"
"При выборе видеокарты в первую очередь следует обратить внимание на её поколение, так как от этого зависит современность технологий, которые были применены и внедрены при производстве.\n"
"Далее - выбирается оптимальный вариант по цене и справочным данным: объём памяти, разъём интерфейса, частота ядра памяти и пр."))
        self.lbNvidia.setText(_translate("widgetVideoHelp", "NVIDIA GeForce"))
        self.lbGeForce.setText(_translate("widgetVideoHelp", "NVIDIA является лидером в разработке видеокарт, технологий и инновационных решений. \n"
"Из последних достижений такие передовые технологии, как: \n"
"-NVIDIA RTX. Аппаратное ускорение трассировки лучей, в работающее и впервые появившееся на видеокартах NVIDIA; \n"
"-NVIDIA DLSS. Высокотехнологичный апскейлинг из более низкого разрешения  до 4K с применением нейросетей.\n"
"Так, если требуется инновационная производительность и использование новейших технолгий, то следует выбирать продукты от NVIDIA"))
        self.lbRadeon.setText(_translate("widgetVideoHelp", "Продукцию AMD относят к более бюджетным вариантам. Большинство прорывов в области архитектуры графических процессоров остаётся за NVIDIA. Однако не всем пользователям необходимы последние инновационные технологии, плюс ко всему, часто AMD Radeon выигрывает в производительности у аналогов Nvidia. \n"
"Так, если нет необходимости в самых последних графичских инновациях, а бюджет ограничен, то, часто без потери производительности, следует выбирать продукты от AMD."))
        self.lbAmd.setText(_translate("widgetVideoHelp", "AMD Radeon"))
        self.btnClose.setText(_translate("widgetVideoHelp", "Закрыть"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widgetVideoHelp = QtWidgets.QWidget()
    ui = Ui_widgetVideoHelp()
    ui.setupUi(widgetVideoHelp)
    widgetVideoHelp.show()
    sys.exit(app.exec_())
