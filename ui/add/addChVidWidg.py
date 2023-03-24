# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\pcconf\ui\add\addChVidWidg.ui'
#
# Created by: PyQt5 UI code generator 5.15.5
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_addChVidWidg(object):
    def setupUi(self, addChVidWidg):
        addChVidWidg.setObjectName("addChVidWidg")
        addChVidWidg.setWindowModality(QtCore.Qt.WindowModal)
        addChVidWidg.resize(881, 603)
        font = QtGui.QFont()
        font.setFamily("Montserrat Medium")
        font.setPointSize(10)
        addChVidWidg.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("E:\\pcconf\\ui\\add\\../../images/win_add_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        addChVidWidg.setWindowIcon(icon)
        addChVidWidg.setStyleSheet("QWidget\n"
"{\n"
"    background: rgb(30, 30, 30);\n"
"    color: white;\n"
"\n"
"}\n"
"")
        self.radioButton = QtWidgets.QRadioButton(addChVidWidg)
        self.radioButton.setGeometry(QtCore.QRect(20, 40, 221, 17))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.radioButton.sizePolicy().hasHeightForWidth())
        self.radioButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Montserrat Medium")
        font.setPointSize(10)
        self.radioButton.setFont(font)
        self.radioButton.setStyleSheet("QRadioButton:hover{\n"
"    color: rgb(210,0,0);\n"
"}\n"
"\n"
"QRadioButton::indicator {\n"
"    width: 13px;\n"
"    height: 13px;\n"
"     border-image: url(\"E:/pcconf/images/off.png\") 0;\n"
"}\n"
"\n"
"QRadioButton::indicator:checked {\n"
"    width: 13px;\n"
"    height: 13px;\n"
"     border-image: url(\"E:/pcconf/images/on.png\") 0;\n"
"}\n"
"\n"
"QRadioButton::indicator:unchecked {\n"
"    width: 13px;\n"
"    height: 13px;\n"
"     border-image: url(\"E:/pcconf/images/off.png\") 0;\n"
"}")
        self.radioButton.setObjectName("radioButton")
        self.lbFullName = QtWidgets.QLabel(addChVidWidg)
        self.lbFullName.setGeometry(QtCore.QRect(20, 170, 201, 21))
        font = QtGui.QFont()
        font.setFamily("Montserrat SemiBold")
        font.setPointSize(10)
        self.lbFullName.setFont(font)
        self.lbFullName.setStyleSheet("border:0px;")
        self.lbFullName.setObjectName("lbFullName")
        self.line = QtWidgets.QFrame(addChVidWidg)
        self.line.setGeometry(QtCore.QRect(20, 70, 841, 16))
        self.line.setStyleSheet("border:0px;\n"
"border-top: 1px solid rgb(180, 0, 0);")
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.line_2 = QtWidgets.QFrame(addChVidWidg)
        self.line_2.setGeometry(QtCore.QRect(20, 330, 841, 16))
        self.line_2.setStyleSheet("border:0px;\n"
"border-top: 1px solid rgb(180, 0, 0);")
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.comBoxVidPost = QtWidgets.QComboBox(addChVidWidg)
        self.comBoxVidPost.setGeometry(QtCore.QRect(20, 120, 181, 31))
        font = QtGui.QFont()
        font.setFamily("Montserrat Medium")
        font.setPointSize(10)
        self.comBoxVidPost.setFont(font)
        self.comBoxVidPost.setStyleSheet("QComboBox{\n"
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
"    border-image: url(\"E:/pcconf/images/down-arrow (1).png\");\n"
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
        self.comBoxVidPost.setEditable(False)
        self.comBoxVidPost.setIconSize(QtCore.QSize(20, 20))
        self.comBoxVidPost.setDuplicatesEnabled(False)
        self.comBoxVidPost.setFrame(False)
        self.comBoxVidPost.setModelColumn(0)
        self.comBoxVidPost.setObjectName("comBoxVidPost")
        self.comBoxVidPost.addItem("")
        self.comBoxVidPost.addItem("")
        self.comBoxVidPost.addItem("")
        self.lbVidPost = QtWidgets.QLabel(addChVidWidg)
        self.lbVidPost.setGeometry(QtCore.QRect(20, 90, 171, 21))
        font = QtGui.QFont()
        font.setFamily("Montserrat SemiBold")
        font.setPointSize(10)
        self.lbVidPost.setFont(font)
        self.lbVidPost.setStyleSheet("border:0px;")
        self.lbVidPost.setObjectName("lbVidPost")
        self.label_3 = QtWidgets.QLabel(addChVidWidg)
        self.label_3.setGeometry(QtCore.QRect(750, 40, 111, 21))
        font = QtGui.QFont()
        font.setFamily("Montserrat SemiBold")
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("border:0px;")
        self.label_3.setObjectName("label_3")
        self.btnVidSave = QtWidgets.QPushButton(addChVidWidg)
        self.btnVidSave.setGeometry(QtCore.QRect(220, 550, 151, 31))
        font = QtGui.QFont()
        font.setFamily("Montserrat Medium")
        font.setPointSize(10)
        self.btnVidSave.setFont(font)
        self.btnVidSave.setStyleSheet("QPushButton{\n"
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
        self.btnVidSave.setObjectName("btnVidSave")
        self.btnVidCancel = QtWidgets.QPushButton(addChVidWidg)
        self.btnVidCancel.setGeometry(QtCore.QRect(460, 550, 151, 31))
        font = QtGui.QFont()
        font.setFamily("Montserrat Medium")
        font.setPointSize(10)
        self.btnVidCancel.setFont(font)
        self.btnVidCancel.setStyleSheet("QPushButton{\n"
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
        self.btnVidCancel.setAutoDefault(False)
        self.btnVidCancel.setDefault(False)
        self.btnVidCancel.setFlat(False)
        self.btnVidCancel.setObjectName("btnVidCancel")
        self.label_4 = QtWidgets.QLabel(addChVidWidg)
        self.label_4.setGeometry(QtCore.QRect(20, 250, 141, 21))
        font = QtGui.QFont()
        font.setFamily("Montserrat SemiBold")
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("border:0px;")
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(addChVidWidg)
        self.label_5.setGeometry(QtCore.QRect(170, 250, 111, 21))
        font = QtGui.QFont()
        font.setFamily("Montserrat SemiBold")
        font.setPointSize(10)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("border:0px;")
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(addChVidWidg)
        self.label_6.setGeometry(QtCore.QRect(320, 250, 161, 21))
        font = QtGui.QFont()
        font.setFamily("Montserrat SemiBold")
        font.setPointSize(10)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("border:0px;")
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(addChVidWidg)
        self.label_7.setGeometry(QtCore.QRect(20, 350, 121, 21))
        font = QtGui.QFont()
        font.setFamily("Montserrat SemiBold")
        font.setPointSize(10)
        self.label_7.setFont(font)
        self.label_7.setStyleSheet("border:0px;")
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(addChVidWidg)
        self.label_8.setGeometry(QtCore.QRect(170, 350, 111, 21))
        font = QtGui.QFont()
        font.setFamily("Montserrat SemiBold")
        font.setPointSize(10)
        self.label_8.setFont(font)
        self.label_8.setStyleSheet("border:0px;")
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(addChVidWidg)
        self.label_9.setGeometry(QtCore.QRect(320, 350, 111, 21))
        font = QtGui.QFont()
        font.setFamily("Montserrat SemiBold")
        font.setPointSize(10)
        self.label_9.setFont(font)
        self.label_9.setStyleSheet("border:0px;")
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(addChVidWidg)
        self.label_10.setGeometry(QtCore.QRect(640, 350, 111, 21))
        font = QtGui.QFont()
        font.setFamily("Montserrat SemiBold")
        font.setPointSize(10)
        self.label_10.setFont(font)
        self.label_10.setStyleSheet("border:0px;")
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(addChVidWidg)
        self.label_11.setGeometry(QtCore.QRect(470, 350, 161, 21))
        font = QtGui.QFont()
        font.setFamily("Montserrat SemiBold")
        font.setPointSize(10)
        self.label_11.setFont(font)
        self.label_11.setStyleSheet("border:0px;")
        self.label_11.setObjectName("label_11")
        self.label_12 = QtWidgets.QLabel(addChVidWidg)
        self.label_12.setGeometry(QtCore.QRect(20, 440, 111, 21))
        font = QtGui.QFont()
        font.setFamily("Montserrat SemiBold")
        font.setPointSize(10)
        self.label_12.setFont(font)
        self.label_12.setStyleSheet("border:0px;")
        self.label_12.setObjectName("label_12")
        self.label_13 = QtWidgets.QLabel(addChVidWidg)
        self.label_13.setGeometry(QtCore.QRect(170, 440, 111, 21))
        font = QtGui.QFont()
        font.setFamily("Montserrat SemiBold")
        font.setPointSize(10)
        self.label_13.setFont(font)
        self.label_13.setStyleSheet("border:0px;")
        self.label_13.setObjectName("label_13")
        self.line_3 = QtWidgets.QFrame(addChVidWidg)
        self.line_3.setGeometry(QtCore.QRect(20, 430, 841, 16))
        self.line_3.setStyleSheet("border:0px;\n"
"border-top: 1px solid rgb(180, 0, 0);")
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.comBoxVidInterface = QtWidgets.QComboBox(addChVidWidg)
        self.comBoxVidInterface.setGeometry(QtCore.QRect(20, 380, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Montserrat Medium")
        font.setPointSize(10)
        self.comBoxVidInterface.setFont(font)
        self.comBoxVidInterface.setStyleSheet("QComboBox{\n"
"    background-color: rgb(40,40,40);\n"
"    border: 1px;\n"
"    border-bottom: 1px solid rgb(120,120,120);\n"
"    padding-left: 5px;\n"
"}\n"
"\n"
"QComboBox:hover{\n"
"    background-color: rgb(55,55,55);\n"
"    border-bottom: 1px solid red;\n"
"}\n"
"\n"
"QComboBox::drop-down{\n"
"border: 0px;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"border-image: url(\"E:/pcconf/images/down-arrow (2).png\");\n"
"width: 17px;\n"
"height: 17px;\n"
"margin-right: 5px;\n"
"}\n"
"\n"
"QComboBox::down-arrow:on {\n"
"    border-image: url(\"E:/pcconf/images/down-arrow (3).png\");\n"
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
        self.comBoxVidInterface.setIconSize(QtCore.QSize(20, 20))
        self.comBoxVidInterface.setDuplicatesEnabled(False)
        self.comBoxVidInterface.setFrame(True)
        self.comBoxVidInterface.setModelColumn(0)
        self.comBoxVidInterface.setObjectName("comBoxVidInterface")
        self.comBoxVidInterface.addItem("")
        self.comBoxVidInterface.addItem("")
        self.comBoxVidInterface.addItem("")
        self.comBoxVidInterface.addItem("")
        self.comBoxVidMonitor = QtWidgets.QComboBox(addChVidWidg)
        self.comBoxVidMonitor.setGeometry(QtCore.QRect(170, 380, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Montserrat Medium")
        font.setPointSize(10)
        self.comBoxVidMonitor.setFont(font)
        self.comBoxVidMonitor.setStyleSheet("QComboBox{\n"
"    background-color: rgb(40,40,40);\n"
"    border: 1px;\n"
"    border-bottom: 1px solid rgb(120,120,120);\n"
"    padding-left: 5px;\n"
"}\n"
"\n"
"QComboBox:hover{\n"
"    background-color: rgb(55,55,55);\n"
"    border-bottom: 1px solid red;\n"
"}\n"
"\n"
"QComboBox::drop-down{\n"
"border: 0px;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"border-image: url(\"E:/pcconf/images/down-arrow (2).png\");\n"
"width: 17px;\n"
"height: 17px;\n"
"margin-right: 5px;\n"
"}\n"
"\n"
"QComboBox::down-arrow:on {\n"
"    border-image: url(\"E:/pcconf/images/down-arrow (3).png\");\n"
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
        self.comBoxVidMonitor.setIconSize(QtCore.QSize(20, 20))
        self.comBoxVidMonitor.setDuplicatesEnabled(False)
        self.comBoxVidMonitor.setFrame(True)
        self.comBoxVidMonitor.setModelColumn(0)
        self.comBoxVidMonitor.setObjectName("comBoxVidMonitor")
        self.comBoxVidMonitor.addItem("")
        self.comBoxVidMonitor.addItem("")
        self.comBoxVidMonitor.addItem("")
        self.comBoxVidMonitor.addItem("")
        self.lbChip = QtWidgets.QLabel(addChVidWidg)
        self.lbChip.setGeometry(QtCore.QRect(320, 170, 171, 21))
        font = QtGui.QFont()
        font.setFamily("Montserrat SemiBold")
        font.setPointSize(10)
        self.lbChip.setFont(font)
        self.lbChip.setStyleSheet("border:0px;")
        self.lbChip.setObjectName("lbChip")
        self.comBoxVideoSelect = QtWidgets.QComboBox(addChVidWidg)
        self.comBoxVideoSelect.setGeometry(QtCore.QRect(320, 120, 181, 31))
        font = QtGui.QFont()
        font.setFamily("Montserrat Medium")
        font.setPointSize(10)
        self.comBoxVideoSelect.setFont(font)
        self.comBoxVideoSelect.setStyleSheet("QComboBox{\n"
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
"    border-image: url(\"E:/pcconf/images/down-arrow (1).png\");\n"
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
        self.comBoxVideoSelect.setEditable(False)
        self.comBoxVideoSelect.setIconSize(QtCore.QSize(20, 20))
        self.comBoxVideoSelect.setDuplicatesEnabled(False)
        self.comBoxVideoSelect.setFrame(False)
        self.comBoxVideoSelect.setModelColumn(0)
        self.comBoxVideoSelect.setObjectName("comBoxVideoSelect")
        self.comBoxVideoSelect.addItem("")
        self.comBoxVideoSelect.addItem("")
        self.comBoxVideoSelect.addItem("")
        self.rectangle = QtWidgets.QFrame(addChVidWidg)
        self.rectangle.setGeometry(QtCore.QRect(20, 10, 61, 16))
        self.rectangle.setStyleSheet("border:0px;\n"
"background-color: rgb(180, 0, 0);\n"
"border: 1px solid rgb(180, 0, 0);")
        self.rectangle.setFrameShape(QtWidgets.QFrame.HLine)
        self.rectangle.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.rectangle.setObjectName("rectangle")
        self.leVidChip = QtWidgets.QLineEdit(addChVidWidg)
        self.leVidChip.setGeometry(QtCore.QRect(320, 200, 291, 31))
        font = QtGui.QFont()
        font.setFamily("Montserrat Medium")
        font.setPointSize(10)
        self.leVidChip.setFont(font)
        self.leVidChip.setStyleSheet("QLineEdit{\n"
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
        self.leVidChip.setObjectName("leVidChip")
        self.leVidName = QtWidgets.QLineEdit(addChVidWidg)
        self.leVidName.setGeometry(QtCore.QRect(20, 200, 261, 31))
        font = QtGui.QFont()
        font.setFamily("Montserrat Medium")
        font.setPointSize(10)
        self.leVidName.setFont(font)
        self.leVidName.setStyleSheet("QLineEdit{\n"
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
        self.leVidName.setObjectName("leVidName")
        self.leVidVolue = QtWidgets.QLineEdit(addChVidWidg)
        self.leVidVolue.setGeometry(QtCore.QRect(20, 280, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Montserrat Medium")
        font.setPointSize(10)
        self.leVidVolue.setFont(font)
        self.leVidVolue.setStyleSheet("QLineEdit{\n"
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
        self.leVidVolue.setObjectName("leVidVolue")
        self.leVidType = QtWidgets.QLineEdit(addChVidWidg)
        self.leVidType.setGeometry(QtCore.QRect(170, 280, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Montserrat Medium")
        font.setPointSize(10)
        self.leVidType.setFont(font)
        self.leVidType.setStyleSheet("QLineEdit{\n"
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
        self.leVidType.setObjectName("leVidType")
        self.leVidFreq = QtWidgets.QLineEdit(addChVidWidg)
        self.leVidFreq.setGeometry(QtCore.QRect(320, 280, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Montserrat Medium")
        font.setPointSize(10)
        self.leVidFreq.setFont(font)
        self.leVidFreq.setStyleSheet("QLineEdit{\n"
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
        self.leVidFreq.setObjectName("leVidFreq")
        self.leVidKol = QtWidgets.QLineEdit(addChVidWidg)
        self.leVidKol.setGeometry(QtCore.QRect(20, 470, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Montserrat Medium")
        font.setPointSize(10)
        self.leVidKol.setFont(font)
        self.leVidKol.setStyleSheet("QLineEdit{\n"
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
        self.leVidKol.setObjectName("leVidKol")
        self.leVidPrice = QtWidgets.QLineEdit(addChVidWidg)
        self.leVidPrice.setGeometry(QtCore.QRect(170, 470, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Montserrat Medium")
        font.setPointSize(10)
        self.leVidPrice.setFont(font)
        self.leVidPrice.setStyleSheet("QLineEdit{\n"
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
        self.leVidPrice.setObjectName("leVidPrice")
        self.leVidResolution = QtWidgets.QLineEdit(addChVidWidg)
        self.leVidResolution.setGeometry(QtCore.QRect(320, 380, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Montserrat Medium")
        font.setPointSize(10)
        self.leVidResolution.setFont(font)
        self.leVidResolution.setStyleSheet("QLineEdit{\n"
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
        self.leVidResolution.setInputMask("")
        self.leVidResolution.setObjectName("leVidResolution")
        self.leVidTdp = QtWidgets.QLineEdit(addChVidWidg)
        self.leVidTdp.setGeometry(QtCore.QRect(470, 380, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Montserrat Medium")
        font.setPointSize(10)
        self.leVidTdp.setFont(font)
        self.leVidTdp.setStyleSheet("QLineEdit{\n"
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
        self.leVidTdp.setInputMask("")
        self.leVidTdp.setPlaceholderText("")
        self.leVidTdp.setObjectName("leVidTdp")
        self.leVidLen = QtWidgets.QLineEdit(addChVidWidg)
        self.leVidLen.setGeometry(QtCore.QRect(640, 380, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Montserrat Medium")
        font.setPointSize(10)
        self.leVidLen.setFont(font)
        self.leVidLen.setStyleSheet("QLineEdit{\n"
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
        self.leVidLen.setInputMask("")
        self.leVidLen.setPlaceholderText("")
        self.leVidLen.setObjectName("leVidLen")
        self.line_4 = QtWidgets.QFrame(addChVidWidg)
        self.line_4.setGeometry(QtCore.QRect(20, 520, 841, 16))
        self.line_4.setStyleSheet("border:0px;\n"
"border-top: 1px solid rgb(180, 0, 0);")
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.radioButton.raise_()
        self.lbFullName.raise_()
        self.line.raise_()
        self.line_2.raise_()
        self.comBoxVidPost.raise_()
        self.lbVidPost.raise_()
        self.label_3.raise_()
        self.btnVidSave.raise_()
        self.btnVidCancel.raise_()
        self.label_4.raise_()
        self.label_6.raise_()
        self.label_7.raise_()
        self.label_8.raise_()
        self.label_9.raise_()
        self.label_10.raise_()
        self.label_11.raise_()
        self.label_12.raise_()
        self.label_13.raise_()
        self.line_3.raise_()
        self.label_5.raise_()
        self.comBoxVidInterface.raise_()
        self.comBoxVidMonitor.raise_()
        self.lbChip.raise_()
        self.comBoxVideoSelect.raise_()
        self.rectangle.raise_()
        self.leVidChip.raise_()
        self.leVidName.raise_()
        self.leVidVolue.raise_()
        self.leVidType.raise_()
        self.leVidFreq.raise_()
        self.leVidKol.raise_()
        self.leVidPrice.raise_()
        self.leVidResolution.raise_()
        self.leVidTdp.raise_()
        self.leVidLen.raise_()
        self.line_4.raise_()

        self.retranslateUi(addChVidWidg)
        QtCore.QMetaObject.connectSlotsByName(addChVidWidg)

    def retranslateUi(self, addChVidWidg):
        _translate = QtCore.QCoreApplication.translate
        addChVidWidg.setWindowTitle(_translate("addChVidWidg", "Добавление"))
        self.radioButton.setText(_translate("addChVidWidg", "Товар доступен на складе???"))
        self.lbFullName.setText(_translate("addChVidWidg", "Наименование видеокарты"))
        self.comBoxVidPost.setItemText(0, _translate("addChVidWidg", "Gigabyte"))
        self.comBoxVidPost.setItemText(1, _translate("addChVidWidg", "Asus"))
        self.comBoxVidPost.setItemText(2, _translate("addChVidWidg", "Nvidia"))
        self.lbVidPost.setText(_translate("addChVidWidg", "Поставщик"))
        self.label_3.setText(_translate("addChVidWidg", "Видеокарта"))
        self.btnVidSave.setText(_translate("addChVidWidg", "Сохранить"))
        self.btnVidCancel.setText(_translate("addChVidWidg", "Отмена"))
        self.label_4.setText(_translate("addChVidWidg", "Объём памяти [Мб]"))
        self.label_5.setText(_translate("addChVidWidg", "Тип памяти"))
        self.label_6.setText(_translate("addChVidWidg", "Частота памяти [МГц]"))
        self.label_7.setText(_translate("addChVidWidg", "Тип интерфейса"))
        self.label_8.setText(_translate("addChVidWidg", "Мониторы"))
        self.label_9.setText(_translate("addChVidWidg", "Разрешение"))
        self.label_10.setText(_translate("addChVidWidg", "Длина [см]"))
        self.label_11.setText(_translate("addChVidWidg", "Тепловыделение (TDP)"))
        self.label_12.setText(_translate("addChVidWidg", "Количество"))
        self.label_13.setText(_translate("addChVidWidg", "Цена [руб.]"))
        self.comBoxVidInterface.setItemText(0, _translate("addChVidWidg", "PCI-E 2.0"))
        self.comBoxVidInterface.setItemText(1, _translate("addChVidWidg", "PCI-E 3.0"))
        self.comBoxVidInterface.setItemText(2, _translate("addChVidWidg", "PCI-E 4.0"))
        self.comBoxVidInterface.setItemText(3, _translate("addChVidWidg", "PCI-E 5.0"))
        self.comBoxVidMonitor.setItemText(0, _translate("addChVidWidg", "1"))
        self.comBoxVidMonitor.setItemText(1, _translate("addChVidWidg", "2"))
        self.comBoxVidMonitor.setItemText(2, _translate("addChVidWidg", "3"))
        self.comBoxVidMonitor.setItemText(3, _translate("addChVidWidg", "4"))
        self.lbChip.setText(_translate("addChVidWidg", "Наименование чипа"))
        self.comBoxVideoSelect.setItemText(0, _translate("addChVidWidg", "Новая"))
        self.comBoxVideoSelect.setItemText(1, _translate("addChVidWidg", "в1"))
        self.comBoxVideoSelect.setItemText(2, _translate("addChVidWidg", "в2"))
        self.leVidResolution.setPlaceholderText(_translate("addChVidWidg", "1920x1080"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    addChVidWidg = QtWidgets.QWidget()
    ui = Ui_addChVidWidg()
    ui.setupUi(addChVidWidg)
    addChVidWidg.show()
    sys.exit(app.exec_())
