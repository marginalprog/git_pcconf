# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\pcconf\ui\filter\widgetVideoFilter.ui'
#
# Created by: PyQt5 UI code generator 5.15.5
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_WidgetVideoFilter(object):
    def setupUi(self, WidgetVideoFilter):
        WidgetVideoFilter.setObjectName("WidgetVideoFilter")
        WidgetVideoFilter.resize(366, 788)
        WidgetVideoFilter.setStyleSheet("QWidget\n"
"{\n"
"     background: rgb(30, 30, 30);\n"
"    color: white;\n"
"\n"
"}\n"
"")
        self.btnClose = QtWidgets.QPushButton(WidgetVideoFilter)
        self.btnClose.setGeometry(QtCore.QRect(200, 720, 121, 31))
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
        self.toolBoxVidFilter = QtWidgets.QToolBox(WidgetVideoFilter)
        self.toolBoxVidFilter.setGeometry(QtCore.QRect(30, 90, 311, 601))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolBoxVidFilter.sizePolicy().hasHeightForWidth())
        self.toolBoxVidFilter.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Montserrat Medium")
        font.setPointSize(12)
        self.toolBoxVidFilter.setFont(font)
        self.toolBoxVidFilter.setAccessibleName("")
        self.toolBoxVidFilter.setStyleSheet("QToolBox\n"
"{\n"
"    background: rgb(30, 30, 30);\n"
"    border: 1px solid red;\n"
"    margin: 1px;\n"
"    icon-size: 23px;\n"
"}\n"
"\n"
"QToolBox::tab\n"
"{\n"
"    height:250px;\n"
"    background: rgb(30, 30, 30);\n"
"    margin-left: 1px;\n"
"    left: -1px;\n"
"    color: rgb(235, 235, 235);\n"
"    border-top: 1px solid;\n"
"    border-bottom: 3px solid;\n"
"}\n"
"\n"
"QToolBox::tab:selected\n"
"{\n"
"    background-color: rgb(50, 50, 50);\n"
"    border-bottom: 2px solid  rgb(180, 0, 0);\n"
"    color: white;\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"QToolBox::tab:hover\n"
"{\n"
"    background-color: rgb(65, 65, 65);\n"
"    border-bottom: 5px solid;\n"
"    border-color: black;\n"
"}\n"
"")
        self.toolBoxVidFilter.setFrameShadow(QtWidgets.QFrame.Plain)
        self.toolBoxVidFilter.setLineWidth(0)
        self.toolBoxVidFilter.setMidLineWidth(1)
        self.toolBoxVidFilter.setObjectName("toolBoxVidFilter")
        self.Price = QtWidgets.QWidget()
        self.Price.setGeometry(QtCore.QRect(0, 0, 307, 189))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Price.sizePolicy().hasHeightForWidth())
        self.Price.setSizePolicy(sizePolicy)
        self.Price.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.Price.setSizeIncrement(QtCore.QSize(0, 0))
        self.Price.setBaseSize(QtCore.QSize(0, 200))
        self.Price.setObjectName("Price")
        self.tbFrameVideo = QtWidgets.QFrame(self.Price)
        self.tbFrameVideo.setGeometry(QtCore.QRect(0, 0, 301, 121))
        self.tbFrameVideo.setStyleSheet("")
        self.tbFrameVideo.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.tbFrameVideo.setFrameShadow(QtWidgets.QFrame.Raised)
        self.tbFrameVideo.setObjectName("tbFrameVideo")
        self.sliderPriceMin = QtWidgets.QSlider(self.tbFrameVideo)
        self.sliderPriceMin.setGeometry(QtCore.QRect(10, 70, 111, 22))
        self.sliderPriceMin.setStyleSheet("QSlider::groove:horizontal {\n"
"border: 1px solid #bbb;\n"
"background: rgb(150,150,150);\n"
"height:6px;\n"
"}\n"
"\n"
"QSlider::sub-page:horizontal {\n"
"border: 1px solid rgb(60,60,60);\n"
"background: qlineargradient(x1: 0, y1: 0,    x2: 0, y2: 1,\n"
"    stop: 0 rgb(255, 0, 0), stop: 1 rgb(91, 91, 91));\n"
"background: qlineargradient(x1: 0, y1: 0.2, x2: 1, y2: 1,\n"
"    stop: 0 rgb(60, 60,60), stop: 1 rgb(250, 0, 0));\n"
"color: rgb(144, 144, 144);\n"
"height: 6px;\n"
"}\n"
"\n"
"QSlider::add-page:horizontal {\n"
"border: 1px solid rgb(60,60,60);\n"
"background: rgb(80,80,80);\n"
"}\n"
"\n"
"QSlider::handle:horizontal {\n"
"border: 1px solid rgb(60,60,60);\n"
"background: qlineargradient(x1:0, y1:0, x2:1, y2:1,\n"
"    stop:0 rgb(80,80,80), stop:1 rgb(250,0,0));\n"
"width: 6px;\n"
"margin-top: -7px;\n"
"margin-bottom: -7px;\n"
"}\n"
"\n"
"QSlider::handle:horizontal:hover {\n"
"border: 1px solid rgb(60,60,60);\n"
"background: qlineargradient(x1:0, y1:0, x2:1, y2:1,\n"
"    stop:0 rgb(105,105,105), stop:1 rgb(250,0,0));\n"
"width: 9px;\n"
"margin-top: -7px;\n"
"margin-bottom: -7px;\n"
"}\n"
"\n"
"\n"
"QSlider::sub-page:horizontal:disabled {\n"
"background: #bbb;\n"
"border-color: #999;\n"
"}\n"
"\n"
"QSlider::add-page:horizontal:disabled {\n"
"background: #eee;\n"
"border-color: #999;\n"
"}\n"
"\n"
"QSlider::handle:horizontal:disabled {\n"
"background: #eee;\n"
"border: 1px solid #aaa;\n"
"border-radius: 4px;\n"
"}")
        self.sliderPriceMin.setProperty("value", 50)
        self.sliderPriceMin.setOrientation(QtCore.Qt.Horizontal)
        self.sliderPriceMin.setInvertedAppearance(False)
        self.sliderPriceMin.setInvertedControls(False)
        self.sliderPriceMin.setObjectName("sliderPriceMin")
        self.teMinPrice = QtWidgets.QTextEdit(self.tbFrameVideo)
        self.teMinPrice.setGeometry(QtCore.QRect(10, 20, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Montserrat Medium")
        font.setPointSize(10)
        self.teMinPrice.setFont(font)
        self.teMinPrice.setStyleSheet("QTextEdit{\n"
"    padding-left: 5px;\n"
"    border: 1px solid rgb(20,20,20);\n"
"    background-color: rgb(40,40,40);\n"
"    border-bottom: 1px solid  rgb(120,120,120);\n"
"    selection-background-color: rgb(105, 0, 0);\n"
"}\n"
"\n"
"QTextEdit:hover{\n"
"    background-color: rgb(55,55,55);\n"
"    border-bottom: 1px solid  red;\n"
"}")
        self.teMinPrice.setAutoFormatting(QtWidgets.QTextEdit.AutoNone)
        self.teMinPrice.setUndoRedoEnabled(True)
        self.teMinPrice.setReadOnly(False)
        self.teMinPrice.setOverwriteMode(False)
        self.teMinPrice.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByKeyboard|QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextBrowserInteraction|QtCore.Qt.TextEditable|QtCore.Qt.TextEditorInteraction|QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.teMinPrice.setObjectName("teMinPrice")
        self.teMaxPrice = QtWidgets.QTextEdit(self.tbFrameVideo)
        self.teMaxPrice.setGeometry(QtCore.QRect(180, 20, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Montserrat Medium")
        font.setPointSize(10)
        self.teMaxPrice.setFont(font)
        self.teMaxPrice.setStyleSheet("QTextEdit{\n"
"    padding-left: 5px;\n"
"    border: 1px solid rgb(20,20,20);\n"
"    background-color: rgb(40,40,40);\n"
"    border-bottom: 1px solid  rgb(120,120,120);\n"
"    selection-background-color: rgb(105, 0, 0);\n"
"}\n"
"\n"
"QTextEdit:hover{\n"
"    background-color: rgb(55,55,55);\n"
"    border-bottom: 1px solid  red;\n"
"}")
        self.teMaxPrice.setObjectName("teMaxPrice")
        self.line_2 = QtWidgets.QFrame(self.tbFrameVideo)
        self.line_2.setGeometry(QtCore.QRect(140, 40, 21, 20))
        self.line_2.setStyleSheet("border:0px;\n"
"border-top: 1px solid white;")
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.sliderPriceMax = QtWidgets.QSlider(self.tbFrameVideo)
        self.sliderPriceMax.setGeometry(QtCore.QRect(180, 70, 111, 22))
        self.sliderPriceMax.setStyleSheet("QSlider::groove:horizontal {\n"
"border: 1px solid #bbb;\n"
"background: rgb(150,150,150);\n"
"height:6px;\n"
"}\n"
"\n"
"QSlider::sub-page:horizontal {\n"
"border: 1px solid rgb(60,60,60);\n"
"background: qlineargradient(spread:pad, x1:0, y1:1, x2:1, y2:0, stop:0.125 rgba(66, 68, 68, 255), stop:0.426136 rgba(117, 19, 19, 255), stop:0.852273 rgba(255, 0, 0, 255));\n"
"\n"
"color: rgb(144, 144, 144);\n"
"height: 6px;\n"
"}\n"
"\n"
"QSlider::add-page:horizontal {\n"
"border: 1px solid rgb(60,60,60);\n"
"background: rgb(80,80,80);\n"
"}\n"
"\n"
"QSlider::handle:horizontal {\n"
"border: 1px solid rgb(60,60,60);\n"
"background:qlineargradient(spread:pad, x1:1, y1:1, x2:0, y2:0.057, stop:0 rgba(255, 0, 0, 255), stop:0.398876 rgba(165, 0, 0, 255), stop:0.994318 rgba(46, 48, 49, 255));\n"
"width: 6px;\n"
"margin-top: -7px;\n"
"margin-bottom: -7px;\n"
"}\n"
"\n"
"QSlider::handle:horizontal:hover {\n"
"border: 1px solid rgb(60,60,60);\n"
"background: qlineargradient(x1:0, y1:0, x2:1, y2:1,\n"
"    stop:0 rgb(105,105,105), stop:1 rgb(250,0,0));\n"
"width: 9px;\n"
"margin-top: -7px;\n"
"margin-bottom: -7px;\n"
"}\n"
"\n"
"\n"
"QSlider::sub-page:horizontal:disabled {\n"
"background: #bbb;\n"
"border-color: #999;\n"
"}\n"
"\n"
"QSlider::add-page:horizontal:disabled {\n"
"background: #eee;\n"
"border-color: #999;\n"
"}\n"
"\n"
"QSlider::handle:horizontal:disabled {\n"
"background: #eee;\n"
"border: 1px solid #aaa;\n"
"border-radius: 4px;\n"
"}")
        self.sliderPriceMax.setProperty("value", 50)
        self.sliderPriceMax.setOrientation(QtCore.Qt.Horizontal)
        self.sliderPriceMax.setInvertedAppearance(False)
        self.sliderPriceMax.setInvertedControls(False)
        self.sliderPriceMax.setObjectName("sliderPriceMax")
        icon = QtGui.QIcon.fromTheme("w")
        self.toolBoxVidFilter.addItem(self.Price, icon, "")
        self.Brand = QtWidgets.QWidget()
        self.Brand.setGeometry(QtCore.QRect(0, 0, 307, 189))
        self.Brand.setObjectName("Brand")
        self.frameBrand = QtWidgets.QFrame(self.Brand)
        self.frameBrand.setGeometry(QtCore.QRect(0, 0, 301, 181))
        self.frameBrand.setStyleSheet("")
        self.frameBrand.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameBrand.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameBrand.setObjectName("frameBrand")
        self.tableBrand = QtWidgets.QTableWidget(self.frameBrand)
        self.tableBrand.setEnabled(True)
        self.tableBrand.setGeometry(QtCore.QRect(40, 0, 241, 111))
        font = QtGui.QFont()
        font.setFamily("Montserrat Medium")
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.tableBrand.setFont(font)
        self.tableBrand.setMouseTracking(True)
        self.tableBrand.setFocusPolicy(QtCore.Qt.NoFocus)
        self.tableBrand.setAutoFillBackground(False)
        self.tableBrand.setStyleSheet("QHeaderView\n"
"{    \n"
"    background: rgb(30, 30, 30);\n"
"    color: #dddddd;\n"
"    border: 0px;\n"
"    font-size: 14px;\n"
"    min-width: 100px;    \n"
"    min-height: 30px;\n"
"}\n"
"\n"
"QHeaderView::section{\n"
"    background: rgb(30, 30, 30);\n"
"    min-width: 10px;    \n"
"    min-height: 25px;\n"
"    border: 0px solid;\n"
"    border-right: 1px solid rgb(50,50,50); \n"
"    color: #dddddd;\n"
"    font-size: 12px;\n"
"}\n"
"\n"
"QHeaderView::section:hover {\n"
"   color: white;\n"
"    background-color: rgb(80,80,80);\n"
"}\n"
"\n"
"QHeaderView::section{\n"
"    color: white;\n"
"    selection-background-color:#ffc0cb;\n"
"}\n"
"\n"
"QTableWidget QTableCornerButton::section\n"
"{\n"
"    \n"
"    background: rgb(30, 30, 30);\n"
"    border-style: solid;\n"
"    border-width: 1px;\n"
"}\n"
"\n"
"QTableWidget::item\n"
"{\n"
"     border-bottom: 1px solid rgb(60,60,60); \n"
"    border-right: 0px;\n"
"    border-left: 0px;\n"
"    border-top:0px;\n"
"}\n"
"\n"
"QTableView\n"
"{\n"
"    background: rgb(30, 30, 30);\n"
"    color: #dddddd;\n"
"    border-top: 0px;\n"
"    border-right: 0px;\n"
"    border-left: 0px;\n"
"    border-bottom: 0px;\n"
"}\n"
"\n"
"QTableWidget::item:hover {\n"
"    color: white;\n"
"    border-bottom: 1px solid rgb(180,180,180);\n"
"}      \n"
"\n"
"QTableWidget::item:selected\n"
"{\n"
"     color: white;\n"
"    border-bottom: 1px solid rgb(180,180,180);\n"
"}\n"
"\n"
"QScrollBar:vertical {\n"
"    border: none;\n"
"    background-color: #151515;\n"
"    width: 8px;\n"
"    margin: 15px 0 15px 0;\n"
"    border-radius: 0px;\n"
" }\n"
"\n"
"/*  HANDLE BAR VERTICAL */\n"
"QScrollBar::handle:vertical {    \n"
"    background-color: #151515;\n"
"    min-height: 30px;\n"
"    border-radius: 0px;\n"
"    border: 1px solid;\n"
"    border-right: 0px;\n"
"    border-color: rgb(60,60,60);\n"
"}\n"
"QScrollBar::handle:vertical:hover{    \n"
"    background-color:  rgb(50,50,50);\n"
"    border-color: rgb(60,60,60);\n"
"}\n"
"QScrollBar::handle:vertical:pressed {    \n"
"    background-color: rgb(120, 0, 2);\n"
"}\n"
"\n"
"/* BTN TOP - SCROLLBAR */\n"
"QScrollBar::sub-line:vertical {\n"
"    background-color: #151515;\n"
"    height: 15px;\n"
"    subcontrol-position: top;\n"
"    subcontrol-origin: margin;\n"
"    border: 0px;\n"
"    border-bottom: 1px solid rgb(180, 0, 0);\n"
"}\n"
"QScrollBar::sub-line:vertical:hover {    \n"
"    background-color: #575757;\n"
"    border-color: #242424;\n"
"}\n"
"QScrollBar::sub-line:vertical:pressed {    \n"
"    background-color: rgb(120, 0, 2);\n"
"}\n"
"\n"
"/* BTN BOTTOM - SCROLLBAR */\n"
"QScrollBar::add-line:vertical {\n"
"    background-color: #151515;\n"
"    height: 15px;\n"
"    subcontrol-position: bottom;\n"
"    subcontrol-origin: margin;\n"
"    border: 1px solid;\n"
"    border-color: rgb(60,60,60);\n"
"    border: 1px solid;\n"
"    border-top:1px solid rgb(180, 0, 0);\n"
"    border-right: 0px;\n"
"    border-bottom: 0px;\n"
"}\n"
"QScrollBar::add-line:vertical:hover {    \n"
"    background-color: #575757;\n"
"    border-color: #242424;\n"
"}\n"
"QScrollBar::add-line:vertical:pressed {    \n"
"    background-color: rgb(120, 0, 2);\n"
"}\n"
"/* RESET ARROW */\n"
"QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
"    background: none;\n"
"}\n"
"\n"
"QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
"    background: none;\n"
"}")
        self.tableBrand.setEditTriggers(QtWidgets.QAbstractItemView.AnyKeyPressed|QtWidgets.QAbstractItemView.EditKeyPressed|QtWidgets.QAbstractItemView.SelectedClicked)
        self.tableBrand.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableBrand.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableBrand.setShowGrid(False)
        self.tableBrand.setGridStyle(QtCore.Qt.SolidLine)
        self.tableBrand.setObjectName("tableBrand")
        self.tableBrand.setColumnCount(2)
        self.tableBrand.setRowCount(3)
        item = QtWidgets.QTableWidgetItem()
        self.tableBrand.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableBrand.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableBrand.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableBrand.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableBrand.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableBrand.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableBrand.setItem(0, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableBrand.setItem(1, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableBrand.setItem(1, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableBrand.setItem(2, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableBrand.setItem(2, 1, item)
        self.tableBrand.horizontalHeader().setVisible(False)
        self.tableBrand.horizontalHeader().setCascadingSectionResizes(True)
        self.tableBrand.horizontalHeader().setDefaultSectionSize(120)
        self.tableBrand.horizontalHeader().setHighlightSections(False)
        self.tableBrand.horizontalHeader().setMinimumSectionSize(15)
        self.tableBrand.horizontalHeader().setSortIndicatorShown(True)
        self.tableBrand.horizontalHeader().setStretchLastSection(False)
        self.tableBrand.verticalHeader().setVisible(False)
        self.tableBrand.verticalHeader().setCascadingSectionResizes(False)
        self.tableBrand.verticalHeader().setMinimumSectionSize(10)
        self.checkBox = QtWidgets.QCheckBox(self.frameBrand)
        self.checkBox.setGeometry(QtCore.QRect(40, 100, 21, 21))
        self.checkBox.setStyleSheet("QCheckBox {\n"
"    spacing: 5px;\n"
"}\n"
"\n"
"QCheckBox::indicator {\n"
"    width: 25px;\n"
"    height: 25px;\n"
"}\n"
"\n"
"QCheckBox::indicator:unchecked {\n"
"    image: url(E:/pcconf/images/unchecked.png);\n"
"}\n"
"\n"
"\n"
"QCheckBox::indicator:checked {\n"
"    image: url(E:/pcconf/images/checked.png);\n"
"}")
        self.checkBox.setText("")
        self.checkBox.setObjectName("checkBox")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("E:\\pcconf\\ui\\filter\\../../images/down-arrow.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolBoxVidFilter.addItem(self.Brand, icon, "")
        self.pageMother = QtWidgets.QWidget()
        self.pageMother.setGeometry(QtCore.QRect(0, 0, 307, 189))
        self.pageMother.setObjectName("pageMother")
        self.toolBoxVidFilter.addItem(self.pageMother, icon, "")
        self.pageCooling = QtWidgets.QWidget()
        self.pageCooling.setGeometry(QtCore.QRect(0, 0, 307, 189))
        self.pageCooling.setObjectName("pageCooling")
        self.toolBoxVidFilter.addItem(self.pageCooling, icon, "")
        self.pageRam = QtWidgets.QWidget()
        self.pageRam.setGeometry(QtCore.QRect(0, 0, 307, 189))
        self.pageRam.setObjectName("pageRam")
        self.toolBoxVidFilter.addItem(self.pageRam, icon, "")
        self.pageDisk = QtWidgets.QWidget()
        self.pageDisk.setGeometry(QtCore.QRect(0, 0, 307, 189))
        self.pageDisk.setObjectName("pageDisk")
        self.toolBoxVidFilter.addItem(self.pageDisk, icon, "")
        self.pagePower = QtWidgets.QWidget()
        self.pagePower.setGeometry(QtCore.QRect(0, 0, 307, 189))
        self.pagePower.setObjectName("pagePower")
        self.toolBoxVidFilter.addItem(self.pagePower, icon, "")
        self.pageBody = QtWidgets.QWidget()
        self.pageBody.setGeometry(QtCore.QRect(0, 0, 307, 189))
        self.pageBody.setObjectName("pageBody")
        self.toolBoxVidFilter.addItem(self.pageBody, icon, "")
        self.page = QtWidgets.QWidget()
        self.page.setGeometry(QtCore.QRect(0, 0, 307, 189))
        self.page.setObjectName("page")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("E:\\pcconf\\ui\\filter\\../../images/down-arrow.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon1.addPixmap(QtGui.QPixmap("E:\\pcconf\\ui\\filter\\../../images/down-arrow (1).png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.toolBoxVidFilter.addItem(self.page, icon1, "")
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setGeometry(QtCore.QRect(0, 0, 307, 189))
        self.page_2.setObjectName("page_2")
        self.toolBoxVidFilter.addItem(self.page_2, icon, "")
        self.page_3 = QtWidgets.QWidget()
        self.page_3.setGeometry(QtCore.QRect(0, 0, 307, 189))
        self.page_3.setObjectName("page_3")
        self.toolBoxVidFilter.addItem(self.page_3, icon, "")
        self.page_4 = QtWidgets.QWidget()
        self.page_4.setGeometry(QtCore.QRect(0, 0, 307, 189))
        self.page_4.setObjectName("page_4")
        self.toolBoxVidFilter.addItem(self.page_4, icon, "")
        self.rectangle = QtWidgets.QFrame(WidgetVideoFilter)
        self.rectangle.setGeometry(QtCore.QRect(20, 10, 61, 16))
        self.rectangle.setStyleSheet("border:0px;\n"
"background-color: rgb(180, 0, 0);\n"
"border: 1px solid rgb(180, 0, 0);")
        self.rectangle.setFrameShape(QtWidgets.QFrame.HLine)
        self.rectangle.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.rectangle.setObjectName("rectangle")
        self.lbErr = QtWidgets.QLabel(WidgetVideoFilter)
        self.lbErr.setGeometry(QtCore.QRect(40, 40, 181, 21))
        font = QtGui.QFont()
        font.setFamily("Montserrat Medium")
        font.setPointSize(12)
        self.lbErr.setFont(font)
        self.lbErr.setStyleSheet("border:0px;")
        self.lbErr.setObjectName("lbErr")
        self.line = QtWidgets.QFrame(WidgetVideoFilter)
        self.line.setGeometry(QtCore.QRect(40, 70, 181, 20))
        self.line.setStyleSheet("border:0px;\n"
"border-top: 1px solid red;")
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.btnAccept = QtWidgets.QPushButton(WidgetVideoFilter)
        self.btnAccept.setGeometry(QtCore.QRect(50, 720, 121, 31))
        font = QtGui.QFont()
        font.setFamily("Montserrat Medium")
        font.setPointSize(10)
        self.btnAccept.setFont(font)
        self.btnAccept.setStyleSheet("QPushButton{\n"
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
"}\n"
"")
        self.btnAccept.setObjectName("btnAccept")

        self.retranslateUi(WidgetVideoFilter)
        self.toolBoxVidFilter.layout().setSpacing(3)
        self.btnClose.clicked.connect(WidgetVideoFilter.close)
        QtCore.QMetaObject.connectSlotsByName(WidgetVideoFilter)

    def retranslateUi(self, WidgetVideoFilter):
        _translate = QtCore.QCoreApplication.translate
        WidgetVideoFilter.setWindowTitle(_translate("WidgetVideoFilter", "Фильтр видеокарт"))
        self.btnClose.setText(_translate("WidgetVideoFilter", "Отмена"))
        self.teMinPrice.setHtml(_translate("WidgetVideoFilter", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Montserrat Medium\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.teMinPrice.setPlaceholderText(_translate("WidgetVideoFilter", "от 1500"))
        self.teMaxPrice.setPlaceholderText(_translate("WidgetVideoFilter", "до 1500"))
        self.toolBoxVidFilter.setItemText(self.toolBoxVidFilter.indexOf(self.Price), _translate("WidgetVideoFilter", "Цена, Р"))
        self.tableBrand.setSortingEnabled(True)
        item = self.tableBrand.verticalHeaderItem(0)
        item.setText(_translate("WidgetVideoFilter", "0"))
        item = self.tableBrand.verticalHeaderItem(1)
        item.setText(_translate("WidgetVideoFilter", "1"))
        item = self.tableBrand.verticalHeaderItem(2)
        item.setText(_translate("WidgetVideoFilter", "2"))
        item = self.tableBrand.horizontalHeaderItem(0)
        item.setText(_translate("WidgetVideoFilter", "Выбор"))
        item = self.tableBrand.horizontalHeaderItem(1)
        item.setText(_translate("WidgetVideoFilter", "Название"))
        __sortingEnabled = self.tableBrand.isSortingEnabled()
        self.tableBrand.setSortingEnabled(False)
        item = self.tableBrand.item(0, 0)
        item.setText(_translate("WidgetVideoFilter", "+"))
        item = self.tableBrand.item(0, 1)
        item.setText(_translate("WidgetVideoFilter", "Gigabyte"))
        item = self.tableBrand.item(1, 0)
        item.setText(_translate("WidgetVideoFilter", "-"))
        item = self.tableBrand.item(1, 1)
        item.setText(_translate("WidgetVideoFilter", "Asus"))
        item = self.tableBrand.item(2, 0)
        item.setText(_translate("WidgetVideoFilter", "+"))
        item = self.tableBrand.item(2, 1)
        item.setText(_translate("WidgetVideoFilter", "Nvidia"))
        self.tableBrand.setSortingEnabled(__sortingEnabled)
        self.toolBoxVidFilter.setItemText(self.toolBoxVidFilter.indexOf(self.Brand), _translate("WidgetVideoFilter", "Бренд"))
        self.toolBoxVidFilter.setItemText(self.toolBoxVidFilter.indexOf(self.pageMother), _translate("WidgetVideoFilter", "Производитель процессора"))
        self.toolBoxVidFilter.setItemText(self.toolBoxVidFilter.indexOf(self.pageCooling), _translate("WidgetVideoFilter", "Графический процессор"))
        self.toolBoxVidFilter.setItemText(self.toolBoxVidFilter.indexOf(self.pageRam), _translate("WidgetVideoFilter", "Объём памяти"))
        self.toolBoxVidFilter.setItemText(self.toolBoxVidFilter.indexOf(self.pageDisk), _translate("WidgetVideoFilter", "Тип памяти"))
        self.toolBoxVidFilter.setItemText(self.toolBoxVidFilter.indexOf(self.pagePower), _translate("WidgetVideoFilter", "Частота видеочипа"))
        self.toolBoxVidFilter.setItemText(self.toolBoxVidFilter.indexOf(self.pageBody), _translate("WidgetVideoFilter", "Интерфейс подключения"))
        self.toolBoxVidFilter.setItemText(self.toolBoxVidFilter.indexOf(self.page), _translate("WidgetVideoFilter", "Количество мониторов"))
        self.toolBoxVidFilter.setItemText(self.toolBoxVidFilter.indexOf(self.page_2), _translate("WidgetVideoFilter", "Разрешение"))
        self.toolBoxVidFilter.setItemText(self.toolBoxVidFilter.indexOf(self.page_3), _translate("WidgetVideoFilter", "Тепловыделение"))
        self.toolBoxVidFilter.setItemText(self.toolBoxVidFilter.indexOf(self.page_4), _translate("WidgetVideoFilter", "Длина видеокарты"))
        self.lbErr.setText(_translate("WidgetVideoFilter", "Настройка фильтров"))
        self.btnAccept.setText(_translate("WidgetVideoFilter", "Применить"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    WidgetVideoFilter = QtWidgets.QWidget()
    ui = Ui_WidgetVideoFilter()
    ui.setupUi(WidgetVideoFilter)
    WidgetVideoFilter.show()
    sys.exit(app.exec_())
