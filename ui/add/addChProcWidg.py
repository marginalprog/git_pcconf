# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\pcconf\ui\add\addChProcWidg.ui'
#
# Created by: PyQt5 UI code generator 5.15.5
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_addChProcWidg(object):
    def setupUi(self, addChProcWidg):
        addChProcWidg.setObjectName("addChProcWidg")
        addChProcWidg.resize(880, 603)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("E:\\pcconf\\ui\\add\\../../images/win_add_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        addChProcWidg.setWindowIcon(icon)
        addChProcWidg.setStyleSheet("QWidget\n"
"{\n"
"    background: rgb(30, 30, 30);\n"
"    color: white;\n"
"\n"
"}\n"
"")
        self.lbSocket = QtWidgets.QLabel(addChProcWidg)
        self.lbSocket.setGeometry(QtCore.QRect(500, 170, 101, 21))
        font = QtGui.QFont()
        font.setFamily("Montserrat SemiBold")
        font.setPointSize(10)
        self.lbSocket.setFont(font)
        self.lbSocket.setStyleSheet("border:0px;")
        self.lbSocket.setObjectName("lbSocket")
        self.lbFreq = QtWidgets.QLabel(addChProcWidg)
        self.lbFreq.setGeometry(QtCore.QRect(500, 250, 211, 21))
        font = QtGui.QFont()
        font.setFamily("Montserrat SemiBold")
        font.setPointSize(10)
        self.lbFreq.setFont(font)
        self.lbFreq.setStyleSheet("border:0px;")
        self.lbFreq.setObjectName("lbFreq")
        self.lbComplect = QtWidgets.QLabel(addChProcWidg)
        self.lbComplect.setGeometry(QtCore.QRect(760, 40, 101, 21))
        font = QtGui.QFont()
        font.setFamily("Montserrat SemiBold")
        font.setPointSize(12)
        self.lbComplect.setFont(font)
        self.lbComplect.setStyleSheet("border:0px;")
        self.lbComplect.setObjectName("lbComplect")
        self.line_2 = QtWidgets.QFrame(addChProcWidg)
        self.line_2.setGeometry(QtCore.QRect(20, 330, 841, 16))
        self.line_2.setStyleSheet("border:0px;\n"
"border-top: 1px solid rgb(220, 0, 0);")
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.btnSave = QtWidgets.QPushButton(addChProcWidg)
        self.btnSave.setGeometry(QtCore.QRect(250, 550, 151, 31))
        font = QtGui.QFont()
        font.setFamily("Montserrat Medium")
        font.setPointSize(10)
        self.btnSave.setFont(font)
        self.btnSave.setStyleSheet("QPushButton{\n"
"    border:1px solid rgb(70,70,70);\n"
"    background-color: rgb(35,35,35);\n"
"    color: #fffafa;\n"
"}\n"
"\n"
"QPushButton::hover\n"
"{\n"
"    border:1px;\n"
"    background-color: rgb(60,60,60);\n"
"    border-bottom: 1px solid rgb(0, 255, 8);\n"
"}\n"
"")
        self.btnSave.setObjectName("btnSave")
        self.btnCancel = QtWidgets.QPushButton(addChProcWidg)
        self.btnCancel.setGeometry(QtCore.QRect(440, 550, 151, 31))
        font = QtGui.QFont()
        font.setFamily("Montserrat Medium")
        font.setPointSize(10)
        self.btnCancel.setFont(font)
        self.btnCancel.setStyleSheet("QPushButton{\n"
"    border:1px solid rgb(70,70,70);\n"
"    background-color: rgb(35,35,35);\n"
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
        self.btnCancel.setAutoDefault(False)
        self.btnCancel.setDefault(False)
        self.btnCancel.setFlat(False)
        self.btnCancel.setObjectName("btnCancel")
        self.lbCore = QtWidgets.QLabel(addChProcWidg)
        self.lbCore.setGeometry(QtCore.QRect(20, 250, 111, 21))
        font = QtGui.QFont()
        font.setFamily("Montserrat SemiBold")
        font.setPointSize(10)
        self.lbCore.setFont(font)
        self.lbCore.setStyleSheet("border:0px;")
        self.lbCore.setObjectName("lbCore")
        self.line_4 = QtWidgets.QFrame(addChProcWidg)
        self.line_4.setGeometry(QtCore.QRect(20, 520, 841, 16))
        self.line_4.setStyleSheet("border:0px;\n"
"border-top: 1px solid rgb(220, 0, 0);")
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.line_3 = QtWidgets.QFrame(addChProcWidg)
        self.line_3.setGeometry(QtCore.QRect(20, 430, 841, 16))
        self.line_3.setStyleSheet("border:0px;\n"
"border-top: 1px solid rgb(220, 0, 0);")
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.lbGraphics = QtWidgets.QLabel(addChProcWidg)
        self.lbGraphics.setGeometry(QtCore.QRect(500, 350, 171, 21))
        font = QtGui.QFont()
        font.setFamily("Montserrat SemiBold")
        font.setPointSize(10)
        self.lbGraphics.setFont(font)
        self.lbGraphics.setStyleSheet("border:0px;")
        self.lbGraphics.setObjectName("lbGraphics")
        self.lbPrice = QtWidgets.QLabel(addChProcWidg)
        self.lbPrice.setGeometry(QtCore.QRect(170, 440, 111, 21))
        font = QtGui.QFont()
        font.setFamily("Montserrat SemiBold")
        font.setPointSize(10)
        self.lbPrice.setFont(font)
        self.lbPrice.setStyleSheet("border:0px;")
        self.lbPrice.setObjectName("lbPrice")
        self.leTdp = QtWidgets.QLineEdit(addChProcWidg)
        self.leTdp.setGeometry(QtCore.QRect(320, 380, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Montserrat Medium")
        font.setPointSize(10)
        self.leTdp.setFont(font)
        self.leTdp.setStyleSheet("QLineEdit{\n"
"    padding-left: 5px;\n"
"    border: 1px solid rgb(20,20,20);\n"
"    background-color: rgb(40,40,40);\n"
"    border-bottom: 1px solid  rgb(120,120,120);\n"
"    selection-background-color: rgb(105, 0, 0);\n"
"}\n"
"\n"
"QLineEdit:hover{\n"
"    background-color: rgb(55,55,55);\n"
"    border-bottom: 1px solid  red;\n"
"}")
        self.leTdp.setInputMask("")
        self.leTdp.setPlaceholderText("")
        self.leTdp.setObjectName("leTdp")
        self.lbProcProizv = QtWidgets.QLabel(addChProcWidg)
        self.lbProcProizv.setGeometry(QtCore.QRect(20, 90, 111, 21))
        font = QtGui.QFont()
        font.setFamily("Montserrat SemiBold")
        font.setPointSize(10)
        self.lbProcProizv.setFont(font)
        self.lbProcProizv.setStyleSheet("border:0px;")
        self.lbProcProizv.setObjectName("lbProcProizv")
        self.lbNcores = QtWidgets.QLabel(addChProcWidg)
        self.lbNcores.setGeometry(QtCore.QRect(170, 250, 141, 21))
        font = QtGui.QFont()
        font.setFamily("Montserrat SemiBold")
        font.setPointSize(10)
        self.lbNcores.setFont(font)
        self.lbNcores.setStyleSheet("border:0px;")
        self.lbNcores.setObjectName("lbNcores")
        self.lePrice = QtWidgets.QLineEdit(addChProcWidg)
        self.lePrice.setGeometry(QtCore.QRect(170, 470, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Montserrat Medium")
        font.setPointSize(10)
        self.lePrice.setFont(font)
        self.lePrice.setStyleSheet("QLineEdit{\n"
"    padding-left: 5px;\n"
"    border: 1px solid rgb(20,20,20);\n"
"    background-color: rgb(40,40,40);\n"
"    border-bottom: 1px solid  rgb(120,120,120);\n"
"    selection-background-color: rgb(105, 0, 0);\n"
"}\n"
"\n"
"QLineEdit:hover{\n"
"    background-color: rgb(55,55,55);\n"
"    border-bottom: 1px solid  red;\n"
"}")
        self.lePrice.setInputMask("")
        self.lePrice.setObjectName("lePrice")
        self.line = QtWidgets.QFrame(addChProcWidg)
        self.line.setGeometry(QtCore.QRect(20, 70, 841, 16))
        self.line.setStyleSheet("border:0px;\n"
"border-top: 1px solid rgb(220, 0, 0);")
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.rectangle = QtWidgets.QFrame(addChProcWidg)
        self.rectangle.setGeometry(QtCore.QRect(20, 10, 61, 16))
        self.rectangle.setStyleSheet("background-color: rgb(210, 0, 0);\n"
"border: 1px solid rgb(210, 0, 0);")
        self.rectangle.setFrameShape(QtWidgets.QFrame.HLine)
        self.rectangle.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.rectangle.setObjectName("rectangle")
        self.lbKol = QtWidgets.QLabel(addChProcWidg)
        self.lbKol.setGeometry(QtCore.QRect(20, 440, 121, 21))
        font = QtGui.QFont()
        font.setFamily("Montserrat SemiBold")
        font.setPointSize(10)
        self.lbKol.setFont(font)
        self.lbKol.setStyleSheet("border:0px;")
        self.lbKol.setObjectName("lbKol")
        self.leCore = QtWidgets.QLineEdit(addChProcWidg)
        self.leCore.setGeometry(QtCore.QRect(20, 280, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Montserrat Medium")
        font.setPointSize(10)
        self.leCore.setFont(font)
        self.leCore.setStyleSheet("QLineEdit{\n"
"    padding-left: 5px;\n"
"    border: 1px solid rgb(20,20,20);\n"
"    background-color: rgb(40,40,40);\n"
"    border-bottom: 1px solid  rgb(120,120,120);\n"
"    selection-background-color: rgb(105, 0, 0);\n"
"}\n"
"\n"
"QLineEdit:hover{\n"
"    background-color: rgb(55,55,55);\n"
"    border-bottom: 1px solid  red;\n"
"}")
        self.leCore.setInputMask("")
        self.leCore.setObjectName("leCore")
        self.lbDate = QtWidgets.QLabel(addChProcWidg)
        self.lbDate.setGeometry(QtCore.QRect(670, 440, 111, 21))
        font = QtGui.QFont()
        font.setFamily("Montserrat SemiBold")
        font.setPointSize(10)
        self.lbDate.setFont(font)
        self.lbDate.setStyleSheet("border:0px;")
        self.lbDate.setObjectName("lbDate")
        self.leRamFreq = QtWidgets.QLineEdit(addChProcWidg)
        self.leRamFreq.setGeometry(QtCore.QRect(320, 280, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Montserrat Medium")
        font.setPointSize(10)
        self.leRamFreq.setFont(font)
        self.leRamFreq.setStyleSheet("QLineEdit{\n"
"    padding-left: 5px;\n"
"    border: 1px solid rgb(20,20,20);\n"
"    background-color: rgb(40,40,40);\n"
"    border-bottom: 1px solid  rgb(120,120,120);\n"
"    selection-background-color: rgb(105, 0, 0);\n"
"}\n"
"\n"
"QLineEdit:hover{\n"
"    background-color: rgb(55,55,55);\n"
"    border-bottom: 1px solid  red;\n"
"}")
        self.leRamFreq.setInputMask("")
        self.leRamFreq.setObjectName("leRamFreq")
        self.lbTdp = QtWidgets.QLabel(addChProcWidg)
        self.lbTdp.setGeometry(QtCore.QRect(320, 350, 171, 21))
        font = QtGui.QFont()
        font.setFamily("Montserrat SemiBold")
        font.setPointSize(10)
        self.lbTdp.setFont(font)
        self.lbTdp.setStyleSheet("border:0px;")
        self.lbTdp.setObjectName("lbTdp")
        self.leSocket = QtWidgets.QLineEdit(addChProcWidg)
        self.leSocket.setGeometry(QtCore.QRect(500, 200, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Montserrat Medium")
        font.setPointSize(10)
        self.leSocket.setFont(font)
        self.leSocket.setStyleSheet("QLineEdit{\n"
"    padding-left: 5px;\n"
"    border: 1px solid rgb(20,20,20);\n"
"    background-color: rgb(40,40,40);\n"
"    border-bottom: 1px solid  rgb(120,120,120);\n"
"    selection-background-color: rgb(105, 0, 0);\n"
"}\n"
"\n"
"QLineEdit:hover{\n"
"    background-color: rgb(55,55,55);\n"
"    border-bottom: 1px solid  red;\n"
"}")
        self.leSocket.setObjectName("leSocket")
        self.lbRamFreq = QtWidgets.QLabel(addChProcWidg)
        self.lbRamFreq.setGeometry(QtCore.QRect(320, 250, 151, 21))
        font = QtGui.QFont()
        font.setFamily("Montserrat SemiBold")
        font.setPointSize(10)
        self.lbRamFreq.setFont(font)
        self.lbRamFreq.setStyleSheet("border:0px;")
        self.lbRamFreq.setObjectName("lbRamFreq")
        self.lbFullName = QtWidgets.QLabel(addChProcWidg)
        self.lbFullName.setGeometry(QtCore.QRect(20, 170, 221, 21))
        font = QtGui.QFont()
        font.setFamily("Montserrat SemiBold")
        font.setPointSize(10)
        self.lbFullName.setFont(font)
        self.lbFullName.setStyleSheet("")
        self.lbFullName.setObjectName("lbFullName")
        self.leFreq = QtWidgets.QLineEdit(addChProcWidg)
        self.leFreq.setGeometry(QtCore.QRect(500, 280, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Montserrat Medium")
        font.setPointSize(10)
        self.leFreq.setFont(font)
        self.leFreq.setStyleSheet("QLineEdit{\n"
"    padding-left: 5px;\n"
"    border: 1px solid rgb(20,20,20);\n"
"    background-color: rgb(40,40,40);\n"
"    border-bottom: 1px solid  rgb(120,120,120);\n"
"    selection-background-color: rgb(105, 0, 0);\n"
"}\n"
"\n"
"QLineEdit:hover{\n"
"    background-color: rgb(55,55,55);\n"
"    border-bottom: 1px solid  red;\n"
"}")
        self.leFreq.setInputMask("")
        self.leFreq.setObjectName("leFreq")
        self.leNcores = QtWidgets.QLineEdit(addChProcWidg)
        self.leNcores.setGeometry(QtCore.QRect(170, 280, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Montserrat Medium")
        font.setPointSize(10)
        self.leNcores.setFont(font)
        self.leNcores.setStyleSheet("QLineEdit{\n"
"    padding-left: 5px;\n"
"    border: 1px solid rgb(20,20,20);\n"
"    background-color: rgb(40,40,40);\n"
"    border-bottom: 1px solid  rgb(120,120,120);\n"
"    selection-background-color: rgb(105, 0, 0);\n"
"}\n"
"\n"
"QLineEdit:hover{\n"
"    background-color: rgb(55,55,55);\n"
"    border-bottom: 1px solid  red;\n"
"}")
        self.leNcores.setObjectName("leNcores")
        self.cbProizv = QtWidgets.QComboBox(addChProcWidg)
        self.cbProizv.setGeometry(QtCore.QRect(20, 120, 131, 31))
        font = QtGui.QFont()
        font.setFamily("Montserrat Medium")
        font.setPointSize(10)
        self.cbProizv.setFont(font)
        self.cbProizv.setStyleSheet("QComboBox{\n"
"    background-color: rgb(40,40,40);\n"
"    border: 1px;\n"
"    border-bottom: 1px solid red;\n"
"    padding-left: 5px;\n"
"    selection-background-color: rgb(105, 0, 0);\n"
"}\n"
"\n"
"QComboBox QListView{\n"
"    border: 1px solid red;\n"
"    padding-left: 5px;\n"
"    selection-background-color: rgb(105, 0, 0);\n"
"}\n"
"\n"
"QComboBox:hover{\n"
"    background-color: rgb(55,55,55);\n"
"}\n"
"\n"
"QComboBox::drop-down{\n"
"border: 0px;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"border-image: url(\"E:/pcconf/images/down-arrow.png\");\n"
"width: 17px;\n"
"height: 17px;\n"
"margin-right: 5px;\n"
"}\n"
"\n"
"QComboBox::down-arrow:on {\n"
"    border-image: url(\"E:/pcconf/images/up-arrow.png\");\n"
"    width: 17px;\n"
"    height: 17px;\n"
"    margin-right: 5px;\n"
"}\n"
"\n"
"QComboBox:on{\n"
"border: 2px solid rgb(100,0,0);\n"
"}\n"
"\n"
"QComboBox QAbstractItemView {\n"
"    background: rgb(250, 250, 250);\n"
"    border-width: 1px;\n"
"    border-style: solid;\n"
"    border-color: rgb(235, 235, 235);\n"
"    selection-background-color: rgb(240, 240, 240);\n"
"    selection-color: rgb(25, 25, 25);\n"
"}\n"
"")
        self.cbProizv.setEditable(False)
        self.cbProizv.setIconSize(QtCore.QSize(20, 20))
        self.cbProizv.setDuplicatesEnabled(False)
        self.cbProizv.setFrame(False)
        self.cbProizv.setModelColumn(0)
        self.cbProizv.setObjectName("cbProizv")
        self.cbProizv.addItem("")
        self.cbProizv.addItem("")
        self.leKol = QtWidgets.QLineEdit(addChProcWidg)
        self.leKol.setGeometry(QtCore.QRect(20, 470, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Montserrat Medium")
        font.setPointSize(10)
        self.leKol.setFont(font)
        self.leKol.setStyleSheet("QLineEdit{\n"
"    padding-left: 5px;\n"
"    border: 1px solid rgb(20,20,20);\n"
"    background-color: rgb(40,40,40);\n"
"    border-bottom: 1px solid  rgb(120,120,120);\n"
"    selection-background-color: rgb(105, 0, 0);\n"
"}\n"
"\n"
"QLineEdit:hover{\n"
"    background-color: rgb(55,55,55);\n"
"    border-bottom: 1px solid  red;\n"
"}")
        self.leKol.setInputMask("")
        self.leKol.setObjectName("leKol")
        self.lbSeries = QtWidgets.QLabel(addChProcWidg)
        self.lbSeries.setGeometry(QtCore.QRect(320, 170, 101, 21))
        font = QtGui.QFont()
        font.setFamily("Montserrat SemiBold")
        font.setPointSize(10)
        self.lbSeries.setFont(font)
        self.lbSeries.setStyleSheet("border:0px;")
        self.lbSeries.setObjectName("lbSeries")
        self.leFullName = QtWidgets.QLineEdit(addChProcWidg)
        self.leFullName.setGeometry(QtCore.QRect(20, 200, 261, 31))
        font = QtGui.QFont()
        font.setFamily("Montserrat Medium")
        font.setPointSize(10)
        self.leFullName.setFont(font)
        self.leFullName.setStyleSheet("QLineEdit{\n"
"    padding-left: 5px;\n"
"    border: 1px solid rgb(20,20,20);\n"
"    background-color: rgb(40,40,40);\n"
"    border-bottom: 1px solid  rgb(120,120,120);\n"
"    selection-background-color: rgb(105, 0, 0);\n"
"}\n"
"\n"
"QLineEdit:hover{\n"
"    background-color: rgb(55,55,55);\n"
"    border-bottom: 1px solid  red;\n"
"}")
        self.leFullName.setObjectName("leFullName")
        self.leTechproc = QtWidgets.QLineEdit(addChProcWidg)
        self.leTechproc.setGeometry(QtCore.QRect(20, 380, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Montserrat Medium")
        font.setPointSize(10)
        self.leTechproc.setFont(font)
        self.leTechproc.setStyleSheet("QLineEdit{\n"
"    padding-left: 5px;\n"
"    border: 1px solid rgb(20,20,20);\n"
"    background-color: rgb(40,40,40);\n"
"    border-bottom: 1px solid  rgb(120,120,120);\n"
"    selection-background-color: rgb(105, 0, 0);\n"
"}\n"
"\n"
"QLineEdit:hover{\n"
"    background-color: rgb(55,55,55);\n"
"    border-bottom: 1px solid  red;\n"
"}")
        self.leTechproc.setInputMask("")
        self.leTechproc.setPlaceholderText("")
        self.leTechproc.setObjectName("leTechproc")
        self.lbTechproc = QtWidgets.QLabel(addChProcWidg)
        self.lbTechproc.setGeometry(QtCore.QRect(20, 350, 111, 21))
        font = QtGui.QFont()
        font.setFamily("Montserrat SemiBold")
        font.setPointSize(10)
        self.lbTechproc.setFont(font)
        self.lbTechproc.setStyleSheet("border:0px;")
        self.lbTechproc.setObjectName("lbTechproc")
        self.dateEdit = QtWidgets.QDateEdit(addChProcWidg)
        self.dateEdit.setGeometry(QtCore.QRect(670, 470, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Montserrat Medium")
        font.setPointSize(11)
        self.dateEdit.setFont(font)
        self.dateEdit.setStyleSheet("QDateEdit{\n"
"    background-color: rgb(40,40,40);\n"
"    border: 1px;\n"
"    border-bottom: 1px solid rgb(120,120,120);\n"
"    padding-left: 5px;\n"
"}\n"
"QDateEdit:hover{\n"
"    background-color: rgb(55,55,55);\n"
"    border-bottom: 1px solid red;\n"
"}\n"
"QDateEdit::drop-down{\n"
"    border: 0px;\n"
"}\n"
"\n"
"QDateEdit::down-arrow {\n"
"    border-image: url(\"E:/pcconf/images/down-arrow-gray.png\");\n"
"    width: 17px;\n"
"    height: 17px;\n"
"    margin-right: 5px;\n"
"}\n"
"\n"
"QDateEdit::down-arrow:on {\n"
"    border-image: url(\"E:/pcconf/images/up-arrow-gray.png\");\n"
"    width: 17px;\n"
"    height: 17px;\n"
"    margin-right: 5px;\n"
"    border: 2px solid rgb(100,0,0)\n"
"}\n"
"\n"
"QDateEdit:on{\n"
"    border: 2px solid rgb(100,0,0);\n"
"}\n"
"\n"
"QDateEdit::up-arrow {\n"
"    border-image: url(\"E:/pcconf/images/up-arrow-gray.png\");\n"
"    width: 17px;\n"
"    height: 17px;\n"
"    margin-right: 5px;\n"
"}\n"
"\n"
"QCalendarWidget QWidget#qt_calendar_navigationbar { background-color: rgb(40,40,40); }\n"
"QCalendarWidget QToolButton {\n"
"    background: transparent;\n"
"    border: none;\n"
"    width: 70px;\n"
"    height: 25px;\n"
"    color: rgb(220,220,220);\n"
"    font-size: 14px;\n"
"    icon-size: 30px, 30px;\n"
"}\n"
"\n"
"QToolButton#qt_calendar_prevmonth {\n"
"    background: rgb(45,45,45);\n"
"    border: none;\n"
"    width: 30px;\n"
"    height: 25px;\n"
"    qproperty-icon:  url(\"E:/pcconf/images/left-arrow.png\");\n"
"    icon-size: 20px, 20px;\n"
"    border-bottom: 1px solid red;\n"
"}\n"
"QToolButton#qt_calendar_nextmonth {\n"
"    background: rgb(35,35,35);\n"
"    border: none;\n"
"    width: 30px;\n"
"    height: 25px;\n"
"    qproperty-icon:  url(\"E:/pcconf/images/right-arrow.png\");\n"
"    icon-size: 20px, 20px;\n"
"    border-bottom: 1px solid red;\n"
"}\n"
"\n"
"QCalendarWidget QMenu {\n"
"    width: 100px;\n"
"    left: 10px;\n"
"    color: white;\n"
"    font-size: 14px;\n"
"    background-color: rgb(80, 80, 80);\n"
"    selection-color: rgb(220,0,0);\n"
"}\n"
"\n"
"QCalendarWidget QSpinBox { \n"
"    width: 45px; \n"
"    font-size:14px; \n"
"    color: white; \n"
"    background: transparent;\n"
"    selection-background-color: rgb(105, 0, 0);\n"
"    selection-color: rgb(255, 255, 255);\n"
"}\n"
"QCalendarWidget QSpinBox::up-button { subcontrol-origin: border;  subcontrol-position: top right;  width:15px; height: 15px; border:1px solid rgb(30,30,30); }\n"
"QCalendarWidget QSpinBox::down-button { subcontrol-origin: border; subcontrol-position: bottom right;  width:15px;  height: 15px; border:1px solid rgb(30,30,30);}\n"
"QCalendarWidget QSpinBox::up-arrow { border-image: url(\"E:/pcconf/images/up-arrow.png\"); }\n"
"QCalendarWidget QSpinBox::down-arrow { border-image: url(\"E:/pcconf/images/down-arrow.png\");}\n"
" \n"
"/* header row */\n"
"QCalendarWidget QWidget { alternate-background-color: rgb(50, 50, 50);  border-bottom: 1px solid red; }\n"
" \n"
"/* normal days */\n"
"QCalendarWidget QAbstractItemView:enabled \n"
"{\n"
"    font-size:12px;  \n"
"    color: rgb(180, 180, 180);  \n"
"    background-color: rgb(15, 15, 15);  \n"
"    selection-background-color: rgb(64, 64, 64); \n"
"    selection-color: rgb(0, 255, 0); \n"
"    selection-border-color: red;\n"
"    height: 30px;\n"
"}\n"
" \n"
"/* days in other months */\n"
"QCalendarWidget QAbstractItemView:disabled { color: rgb(80, 80, 80); }")
        self.dateEdit.setProperty("showGroupSeparator", True)
        self.dateEdit.setMinimumDateTime(QtCore.QDateTime(QtCore.QDate(2023, 1, 1), QtCore.QTime(0, 0, 0)))
        self.dateEdit.setMaximumDate(QtCore.QDate(2030, 12, 31))
        self.dateEdit.setCalendarPopup(True)
        self.dateEdit.setDate(QtCore.QDate(2023, 1, 1))
        self.dateEdit.setObjectName("dateEdit")
        self.leSeries = QtWidgets.QLineEdit(addChProcWidg)
        self.leSeries.setGeometry(QtCore.QRect(320, 200, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Montserrat Medium")
        font.setPointSize(10)
        self.leSeries.setFont(font)
        self.leSeries.setStyleSheet("QLineEdit{\n"
"    padding-left: 5px;\n"
"    border: 1px solid rgb(20,20,20);\n"
"    background-color: rgb(40,40,40);\n"
"    border-bottom: 1px solid  rgb(120,120,120);\n"
"    selection-background-color: rgb(105, 0, 0);\n"
"}\n"
"\n"
"QLineEdit:hover{\n"
"    background-color: rgb(55,55,55);\n"
"    border-bottom: 1px solid  red;\n"
"}")
        self.leSeries.setInputMask("")
        self.leSeries.setObjectName("leSeries")
        self.leGraphics = QtWidgets.QLineEdit(addChProcWidg)
        self.leGraphics.setGeometry(QtCore.QRect(500, 380, 201, 31))
        font = QtGui.QFont()
        font.setFamily("Montserrat Medium")
        font.setPointSize(10)
        self.leGraphics.setFont(font)
        self.leGraphics.setStyleSheet("QLineEdit{\n"
"    padding-left: 5px;\n"
"    border: 1px solid rgb(20,20,20);\n"
"    background-color: rgb(40,40,40);\n"
"    border-bottom: 1px solid  rgb(120,120,120);\n"
"    selection-background-color: rgb(105, 0, 0);\n"
"}\n"
"\n"
"QLineEdit:hover{\n"
"    background-color: rgb(55,55,55);\n"
"    border-bottom: 1px solid  red;\n"
"}")
        self.leGraphics.setInputMask("")
        self.leGraphics.setPlaceholderText("")
        self.leGraphics.setObjectName("leGraphics")
        self.lbCache = QtWidgets.QLabel(addChProcWidg)
        self.lbCache.setGeometry(QtCore.QRect(170, 350, 111, 21))
        font = QtGui.QFont()
        font.setFamily("Montserrat SemiBold")
        font.setPointSize(10)
        self.lbCache.setFont(font)
        self.lbCache.setStyleSheet("border:0px;")
        self.lbCache.setObjectName("lbCache")
        self.leCache = QtWidgets.QLineEdit(addChProcWidg)
        self.leCache.setGeometry(QtCore.QRect(170, 380, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Montserrat Medium")
        font.setPointSize(10)
        self.leCache.setFont(font)
        self.leCache.setStyleSheet("QLineEdit{\n"
"    padding-left: 5px;\n"
"    border: 1px solid rgb(20,20,20);\n"
"    background-color: rgb(40,40,40);\n"
"    border-bottom: 1px solid  rgb(120,120,120);\n"
"    selection-background-color: rgb(105, 0, 0);\n"
"}\n"
"\n"
"QLineEdit:hover{\n"
"    background-color: rgb(55,55,55);\n"
"    border-bottom: 1px solid  red;\n"
"}")
        self.leCache.setInputMask("")
        self.leCache.setObjectName("leCache")
        self.cbGaming = QtWidgets.QComboBox(addChProcWidg)
        self.cbGaming.setGeometry(QtCore.QRect(500, 120, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Montserrat Medium")
        font.setPointSize(10)
        self.cbGaming.setFont(font)
        self.cbGaming.setStyleSheet("QComboBox{\n"
"    background-color: rgb(40,40,40);\n"
"    border: 1px;\n"
"    border-bottom: 1px solid rgb(120,120,120);\n"
"    padding-left: 5px;\n"
"    selection-background-color: rgb(105, 0, 0);\n"
"}\n"
"\n"
"QComboBox QListView{\n"
"    border: 1px solid red;\n"
"    padding-left: 5px;\n"
"    selection-background-color: rgb(105, 0, 0);\n"
"}\n"
"\n"
"QComboBox:hover{\n"
"    background-color: rgb(55,55,55);\n"
"    border-bottom: 1px solid red;\n"
"}\n"
"\n"
"QComboBox::down-arrow:hover {\n"
"border-image: url(\"E:/pcconf/images/down-arrow.png\");\n"
"width: 17px;\n"
"height: 17px;\n"
"margin-right: 5px;\n"
"}\n"
"\n"
"QComboBox::drop-down{\n"
"border: 0px;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"border-image: url(\"E:/pcconf/images/down-arrow-gray.png\");\n"
"width: 17px;\n"
"height: 17px;\n"
"margin-right: 5px;\n"
"}\n"
"\n"
"QComboBox::down-arrow:on {\n"
"    border-image: url(\"E:/pcconf/images/up-arrow.png\");\n"
"    width: 17px;\n"
"    height: 17px;\n"
"    margin-right: 5px;\n"
"}\n"
"\n"
"QComboBox:on{\n"
"border: 2px solid rgb(100,0,0);\n"
"}\n"
"\n"
"QComboBox QAbstractItemView {\n"
"    background: rgb(250, 250, 250);\n"
"    border-width: 1px;\n"
"    border-style: solid;\n"
"    border-color: rgb(235, 235, 235);\n"
"    selection-background-color: rgb(240, 240, 240);\n"
"    selection-color: rgb(25, 25, 25);\n"
"}\n"
"")
        self.cbGaming.setEditable(False)
        self.cbGaming.setIconSize(QtCore.QSize(20, 20))
        self.cbGaming.setDuplicatesEnabled(False)
        self.cbGaming.setFrame(False)
        self.cbGaming.setModelColumn(0)
        self.cbGaming.setObjectName("cbGaming")
        self.cbGaming.addItem("")
        self.cbGaming.addItem("")
        self.lbProcGaming = QtWidgets.QLabel(addChProcWidg)
        self.lbProcGaming.setGeometry(QtCore.QRect(500, 90, 191, 21))
        font = QtGui.QFont()
        font.setFamily("Montserrat SemiBold")
        font.setPointSize(10)
        self.lbProcGaming.setFont(font)
        self.lbProcGaming.setStyleSheet("border:0px;")
        self.lbProcGaming.setObjectName("lbProcGaming")

        self.retranslateUi(addChProcWidg)
        self.btnCancel.clicked.connect(addChProcWidg.close)
        QtCore.QMetaObject.connectSlotsByName(addChProcWidg)

    def retranslateUi(self, addChProcWidg):
        _translate = QtCore.QCoreApplication.translate
        addChProcWidg.setWindowTitle(_translate("addChProcWidg", "Form"))
        self.lbSocket.setText(_translate("addChProcWidg", "Сокет"))
        self.lbFreq.setText(_translate("addChProcWidg", "Частота процессора [МГц]"))
        self.lbComplect.setText(_translate("addChProcWidg", "Процессор"))
        self.btnSave.setText(_translate("addChProcWidg", "Сохранить"))
        self.btnCancel.setText(_translate("addChProcWidg", "Отмена"))
        self.lbCore.setText(_translate("addChProcWidg", "Ядро"))
        self.lbGraphics.setText(_translate("addChProcWidg", "Встроенная графика"))
        self.lbPrice.setText(_translate("addChProcWidg", "Цена [руб.]"))
        self.lbProcProizv.setText(_translate("addChProcWidg", "Производитель"))
        self.lbNcores.setText(_translate("addChProcWidg", "Количество ядер"))
        self.lbKol.setText(_translate("addChProcWidg", "Количество"))
        self.lbDate.setText(_translate("addChProcWidg", "Дата заказа"))
        self.lbTdp.setText(_translate("addChProcWidg", "Тепловыделение (TDP)"))
        self.lbRamFreq.setText(_translate("addChProcWidg", "Макс. частота ОЗУ"))
        self.lbFullName.setText(_translate("addChProcWidg", "Название процессора"))
        self.cbProizv.setItemText(0, _translate("addChProcWidg", "AMD"))
        self.cbProizv.setItemText(1, _translate("addChProcWidg", "Intel"))
        self.lbSeries.setText(_translate("addChProcWidg", "Серия"))
        self.lbTechproc.setText(_translate("addChProcWidg", "Техпроцесс"))
        self.lbCache.setText(_translate("addChProcWidg", "Кэш [Мб]"))
        self.cbGaming.setItemText(0, _translate("addChProcWidg", "Да"))
        self.cbGaming.setItemText(1, _translate("addChProcWidg", "Нет"))
        self.lbProcGaming.setText(_translate("addChProcWidg", "Игровое комплектующее"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    addChProcWidg = QtWidgets.QWidget()
    ui = Ui_addChProcWidg()
    ui.setupUi(addChProcWidg)
    addChProcWidg.show()
    sys.exit(app.exec_())