import sys

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QDialog, QTableWidgetItem
from PyQt5.QtGui import QPixmap, QIcon, QIntValidator
# ----------файлы интерфейса---------------
from ui.filter import widgetVideoFilter
from ui import warningWin


# Класс диалогового окна с кнопкой
class DialogOk(QDialog, warningWin.Ui_warningDialog):
    def __init__(self, text):
        QDialog.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("Ошибка")
        self.lbErrDescription.setText(text)
        self.btnCancel.clicked.connect(lambda: self.close())


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
        # -------------------Установка ширины столбцов для таблиц-------------------
        self.tableBrand.setColumnWidth(0, 20)
        self.tableBrand.setColumnWidth(1, 270)

        self.tableProizv.setColumnWidth(0, 20)
        self.tableProizv.setColumnWidth(1, 270)

        self.tableGraphProc.setColumnWidth(0, 20)
        self.tableGraphProc.setColumnWidth(1, 270)
        # -------------------Установка ширины столбцов для таблиц-------------------

        # -----------Соединение кнопок сбосов с методом обнуления-----------
        self.btnResetPrice.clicked.connect(lambda: self.resetSliders(self.sliderPriceMin, self.sliderPriceMax))
        self.btnResetTdp.clicked.connect(lambda: self.resetSliders(self.sliderTdpMin, self.sliderTdpMax))
        self.btnResetLen.clicked.connect(lambda: self.resetSliders(self.sliderLenMin, self.sliderLenMax))
        self.btnResetBrand.clicked.connect(lambda: self.resetCheckBoxes(self.tableBrand))
        self.btnResetProizv.clicked.connect(lambda: self.resetCheckBoxes(self.tableProizv))
        self.btnResetGraphProc.clicked.connect(lambda: self.resetCheckBoxes(self.tableGraphProc))
        # -------------------Соединение кнопк сбосов с методом обнуления-------------------

        # -------------------Задание ограничений для полей ввода-------------------
        onlyInt = QIntValidator()
        onlyInt.setRange(0, 999999)
        self.leMinPrice.setValidator(onlyInt)
        self.leMaxPrice.setValidator(onlyInt)
        self.leMinTdp.setValidator(onlyInt)
        self.leMaxTdp.setValidator(onlyInt)
        self.leMinLen.setValidator(onlyInt)
        self.leMaxLen.setValidator(onlyInt)
        # -------------------Задание ограничений для полей ввода-------------------
        # Изменение положения стрелки при нажатии на вкладку фильтра
        self.toolBoxVidFilter.currentChanged.connect(self.tbChangeArrows)

        # Заполнение таблиц кнопками CB
        self.insert_cb(self.tableBrand)
        self.insert_cb(self.tableProizv)
        self.insert_cb(self.tableGraphProc)

        #
        self.query = ""
        self.btnAccept.clicked.connect(self.clickAccept)

    # нужен общий метод!!!!!!
    def updateMinPrice(self, value):
        self.leMinPrice.setText(f"{value}")

    def updateMaxPrice(self, value):
        self.leMaxPrice.setText(f"{value}")

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

    # Метод, обнуляющий CheckBox-ы в таблице
    def resetCheckBoxes(self, table):
        for i in range(table.rowCount()):
            table.clearSelection()
            widget = table.cellWidget(i, 0)
            if widget is not None:
                chk_box = widget.findChild(CheckBox)
                if chk_box is not None and chk_box.isChecked():
                    chk_box.setChecked(False)

    # Метод, обнуляющий значения слайдеров
    def resetSliders(self, sliderMin, sliderMax):
        sliderMin.setValue(0)
        sliderMax.setValue(0)

    # Метод, считывающий отмеченные CheckBox-ами строки из таблицы. Возвращает отмеченные строки
    def getCheckBoxes(self, table):
        selected_parameters = ""
        for i in range(table.rowCount()):
            widget = table.cellWidget(i, 0)
            if widget is not None:
                chk_box = widget.findChild(CheckBox)
                if chk_box is not None and chk_box.isChecked():
                    selected_parameters += table.item(i, 1).text() + " "
        return selected_parameters

    # Метод для сравнения значений полей (принимает .text())
    def checkFields(self, min_field, max_field):
        if min_field != "" and max_field != "":
            if int(min_field) < int(max_field):
                return min_field, max_field
            else:
                self.dialog = DialogOk("Максимальные значения должны быть больше минимальных")
                self.dialog.show()
                return -1, -1
        elif min_field == "" and max_field == "":
            return 0, 0
        elif min_field != "" and max_field == "":
            return min_field, 0
        elif min_field == "" and max_field != "":
            return 0, max_field

    # метод для очистки параметров фильтрации
    # SELECT * FROM Videocard WHERE Price BETWEEN {16000} AND {18000}
    #                                     > {sss}
    # Метод, срабатывающий по нажатии на кнопку и отправляющий в БД запрос на фильтрацию данных
    def clickAccept(self):
        query = ""  # Сделать массив, который потом по порядку вбить в f-строку для запроса БД
        min_price, max_price = self.checkFields(self.leMinPrice.text(), self.leMaxPrice.text())
        min_tdp, max_tdp = self.checkFields(self.leMinTdp.text(), self.leMaxTdp.text())
        min_len, max_len = self.checkFields(self.leMinLen.text(), self.leMaxLen.text())
        if min_price != -1 and min_tdp != -1 and min_len != -1:  # Если не получили флаг ошибки(-1) - выполняем запрос к БД
            if min_price == 0 and max_price == 0:  # Если пустые поля, то по цене не производим фильтрацию
                print("Конкатенации с другими запросами не будет")
            elif min_price != 0 and max_price == 0:
                query = f"Price > {min_price}"
            elif min_price == 0 and max_price != 0:
                query = f"Price < {max_price}"
            else:
                query = f"Price BETWEEN {min_price} AND {max_price}"


            #query += f'{min_price} {max_price} {min_tdp} {max_tdp} {min_len} {max_len}'
            query += self.getCheckBoxes(self.tableBrand)
            query += self.getCheckBoxes(self.tableProizv)
            query += self.getCheckBoxes(self.tableGraphProc)
            print(query)
            self.close()

