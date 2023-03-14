import sys

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QDialog, QTableWidgetItem
from PyQt5.QtGui import QPixmap, QIcon
# ----------файлы интерфейса---------------
from ui.filter import widgetVideoFilter


class CheckBox(QtWidgets.QCheckBox):
    def __init__(self, parent=None):
        super(CheckBox, self).__init__(parent)
        self.pixmap = QPixmap("E:/pcconf/images/unchecked.png")
        self.pixmap_pressed = QPixmap("E:/pcconf/images/checked.png")

    def paintEvent(self, event):
        if self.isChecked():
            pix = self.pixmap_pressed
        else:
            pix = self.pixmap
        painter = QtGui.QPainter(self)
        painter.drawPixmap(event.rect(), pix)

    def sizeHint(self):
        return QtCore.QSize(18, 18)


class VideoFilter(QtWidgets.QWidget, widgetVideoFilter.Ui_WidgetVideoFilter):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.sliderPriceMin.valueChanged.connect(self.updateMinPrice)
        self.sliderPriceMax.valueChanged.connect(self.updateMaxPrice)
        max_price = 34999  # Здесь должен быть запрос в бд по макс. цене видеокарт
        self.sliderPriceMin.setRange(0, max_price)
        self.sliderPriceMax.setRange(0, max_price)
        self.tableBrand.setColumnWidth(0, 20)
        self.tableBrand.setColumnWidth(1, 270)

        # Изменение положения стрелки при нажатии на вкладку фильтра
        self.toolBoxVidFilter.currentChanged.connect(self.tbChangeArrows)

        # Заполнение брендов
        self.insert_cb(self.tableBrand)

        #
        self.query = ""
        self.btnAccept.clicked.connect(self.clickAccept)

    def updateMinPrice(self, value):
        self.teMinPrice.setText(f"{value}")

    def updateMaxPrice(self, value):
        self.teMaxPrice.setText(f"{value}")

    # Метод создания рб на виджете
    def create_checkbox(self):
        widget = QtWidgets.QWidget()
        cb = CheckBox()
        cb.checkState()
        pLayout = QtWidgets.QHBoxLayout(widget)
        pLayout.addWidget(cb)
        pLayout.setAlignment(QtCore.Qt.AlignCenter)
        pLayout.setContentsMargins(0, 0, 0, 0)
        widget.setLayout(pLayout)
        return widget, cb

    # Метод вставки в таблицу checkbox
    def insert_cb(self, table):
        row_count = table.rowCount()
        for i in range(row_count):
            widget, checkbox = self.create_checkbox()
            checkbox.clicked.connect(
                lambda ch, row=i: self.currentPos(ch, row, table))
            table.setCellWidget(i, 0, widget)

    def currentPos(self, ch, row, table):
        # print(f' row = {row} -- {ch}')
        table.selectRow(row)

    def tbChangeArrows(self, page):
        self.toolBoxVidFilter.setItemIcon(page, QIcon("E:/pcconf/images/up-arrow.png"))
        for i in range(self.toolBoxVidFilter.count()):
            if i != page:
                self.toolBoxVidFilter.setItemIcon(i, QIcon("E:/pcconf/images/down-arrow.png"))

    # Метод, собирающий данные о выбранных фильтрах
    def clickAccept(self):
        widget = self.tableBrand.cellWidget(1, 0)
        if widget is not None:
            chk_box = widget.findChild(CheckBox)
            if chk_box is not None and chk_box.isChecked():
                self.query += self.tableBrand.item(0, 1).text()
        print(self.query)
