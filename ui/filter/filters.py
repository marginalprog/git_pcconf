import sys

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QDialog, QTableWidgetItem
from PyQt5.QtGui import QPixmap, QIcon, QIntValidator
# ----------файлы интерфейса---------------
from ui.filter import widgetVideoFilter
from ui import warningWin


# Класс диалогового окна с кнопкой
class DialogOk(QDialog, warningWin.Ui_warningDialog):
    def __init__(self, error_win_title, error_text, parent=None):
        QDialog.__init__(self)
        self.setupUi(self)
        self.setWindowTitle(error_win_title)
        self.lbErrDescription.setText(error_text)
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
    def __init__(self, page, parent):
        super().__init__()
        self.setupUi(self)
        self.parent = parent
        self.page = page  # Где было создано окно фильтрации - в конфигураторе или на складе
        # -------------Сигналы обновления значений в полях при движении слайдера------------
        self.sliderPriceMin.valueChanged.connect(lambda value: self.updateFieldValue(self.leMinPrice, value))
        self.sliderPriceMax.valueChanged.connect(lambda value: self.updateFieldValue(self.leMaxPrice, value))
        self.sliderTdpMin.valueChanged.connect(lambda value: self.updateFieldValue(self.leMinTdp, value))
        self.sliderTdpMax.valueChanged.connect(lambda value: self.updateFieldValue(self.leMaxTdp, value))
        self.sliderLenMin.valueChanged.connect(lambda value: self.updateFieldValue(self.leMinLen, value))
        self.sliderLenMax.valueChanged.connect(lambda value: self.updateFieldValue(self.leMaxLen, value))
        # -------------Сигналы обновления значений в слайдерах при вводе числа------------
        self.leMinPrice.textChanged.connect(lambda value: self.updateSliderValue(self.sliderPriceMin, value, self.leMinPrice))
        self.leMaxPrice.textChanged.connect(lambda value: self.updateSliderValue(self.sliderPriceMax, value, self.leMaxPrice))
        self.leMinTdp.textChanged.connect(lambda value: self.updateSliderValue(self.sliderTdpMin, value, self.leMinTdp))
        self.leMaxTdp.textChanged.connect(lambda value: self.updateSliderValue(self.sliderTdpMax, value, self.leMaxTdp))
        self.leMinLen.textChanged.connect(lambda value: self.updateSliderValue(self.sliderLenMin, value, self.leMinLen))
        self.leMaxLen.textChanged.connect(lambda value: self.updateSliderValue(self.sliderLenMax, value, self.leMaxLen))
        # --------------------------------------------------------------------------------
        max_price = 34999  # Здесь должен быть запрос в бд по макс. цене видеокарт
        max_tdp = 250  # Здесь должен быть запрос в бд по макс. тдп видеокарт
        max_length = 40  # Здесь должен быть запрос в бд по макс. длине видеокарт
        self.sliderPriceMin.setRange(0, max_price)
        self.sliderPriceMax.setRange(0, max_price)
        self.sliderTdpMin.setRange(0, max_tdp)
        self.sliderTdpMax.setRange(0, max_tdp)
        self.sliderLenMin.setRange(0, max_length)
        self.sliderLenMax.setRange(0, max_length)
        # ----------------------------------------------------------------------------------

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

        # -------------------Установка ширины столбцов для таблиц-------------------
        self.tableBrand.setColumnWidth(0, 20)
        self.tableBrand.setColumnWidth(1, 270)
        self.tableProizv.setColumnWidth(0, 20)
        self.tableProizv.setColumnWidth(1, 270)
        self.tableGraphProc.setColumnWidth(0, 20)
        self.tableGraphProc.setColumnWidth(1, 270)
        self.tableVolume.setColumnWidth(0, 20)
        self.tableVolume.setColumnWidth(1, 270)
        self.tableType.setColumnWidth(0, 20)
        self.tableType.setColumnWidth(1, 270)
        self.tableFreq.setColumnWidth(0, 20)
        self.tableFreq.setColumnWidth(1, 270)
        self.tableInterface.setColumnWidth(0, 20)
        self.tableInterface.setColumnWidth(1, 270)
        self.tableMonitor.setColumnWidth(0, 20)
        self.tableMonitor.setColumnWidth(1, 270)
        self.tableResolution.setColumnWidth(0, 20)
        self.tableResolution.setColumnWidth(1, 270)
        # ------------------------------------------------------------------

        # -----------Соединение кнопок сбосов с методом обнуления-----------
        self.btnResetAll.clicked.connect(self.resetAll)
        self.btnResetPrice.clicked.connect(lambda: self.resetSliders(self.sliderPriceMin, self.sliderPriceMax, self.leMinPrice, self.leMaxPrice))
        self.btnResetTdp.clicked.connect(lambda: self.resetSliders(self.sliderTdpMin, self.sliderTdpMax, self.leMinTdp, self.leMaxTdp))
        self.btnResetLen.clicked.connect(lambda: self.resetSliders(self.sliderLenMin, self.sliderLenMax, self.leMinLen, self.leMaxLen))
        self.btnResetBrand.clicked.connect(lambda: self.resetCheckBoxes(self.tableBrand))
        self.btnResetProizv.clicked.connect(lambda: self.resetCheckBoxes(self.tableProizv))
        self.btnResetGraphProc.clicked.connect(lambda: self.resetCheckBoxes(self.tableGraphProc))
        # -------------------Соединение кнопк сбосов с методом обнуления-------------------

        # Изменение положения стрелки при нажатии на вкладку фильтра
        self.toolBoxVidFilter.currentChanged.connect(self.tbChangeArrows)

        # Заполнение таблиц кнопками CB
        self.pasteCheckBoxes()

        #
        self.btnAccept.clicked.connect(self.clickAccept)

    # Метод обновления значений в поле при движении слайдера
    def updateFieldValue(self, field, value):
        field.setText(f"{value}")

    # Метод обновления слайдера при вводе значений в поле
    def updateSliderValue(self, slider, value, field):
        if value == "":
            slider.setValue(1)
            field.clear()
        else:
            slider.setValue(int(value))

    # Метод создания cb на виджете
    def create_checkbox(self):
        widget = QtWidgets.QWidget()
        widget.setStyleSheet("background: rgb(10, 10, 10);")
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

    # Метод для вставки CB в таблицы
    def pasteCheckBoxes(self):
        self.insert_cb(self.tableBrand)
        self.insert_cb(self.tableProizv)
        self.insert_cb(self.tableGraphProc)
        self.insert_cb(self.tableVolume)
        self.insert_cb(self.tableType)
        self.insert_cb(self.tableFreq)
        self.insert_cb(self.tableInterface)
        self.insert_cb(self.tableMonitor)
        self.insert_cb(self.tableResolution)

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
    def resetSliders(self, sliderMin, sliderMax, leMin, leMax):
        sliderMin.setValue(0)
        sliderMax.setValue(0)
        leMin.clear()
        leMax.clear()

    # Метод, обнуляющий все поля
    def resetAll(self):
        self.resetSliders(self.sliderPriceMin, self.sliderPriceMax, self.leMinPrice, self.leMaxPrice)
        self.resetSliders(self.sliderTdpMin, self.sliderTdpMax, self.leMinTdp, self.leMaxTdp)
        self.resetSliders(self.sliderLenMin, self.sliderLenMax, self.leMinLen, self.leMaxLen)
        self.resetCheckBoxes(self.tableBrand)
        self.resetCheckBoxes(self.tableProizv)
        self.resetCheckBoxes(self.tableGraphProc)
        self.resetCheckBoxes(self.tableVolume)
        self.resetCheckBoxes(self.tableType)
        self.resetCheckBoxes(self.tableFreq)
        self.resetCheckBoxes(self.tableInterface)
        self.resetCheckBoxes(self.tableMonitor)
        self.resetCheckBoxes(self.tableResolution)
        print('ssss')

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
                self.dialog = DialogOk("Ошибка", "Максимальные значения должны быть больше минимальных")
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
    # Метод генерации параметров для запроса к БД (получает значения мин. и макс. знач. введённых полей)
    def checkMinMax(self, min, max, bd_table):
        if min != -1:  # Если не получили флаг ошибки(-1) - выполняем запрос к БД
            if min == 0 and max == 0:  # Если пустые поля, то по цене не производим фильтрацию
                print("Конкатенации с другими запросами не будет")
                return ""
            elif min != 0 and max == 0:
                return f"{bd_table} > {min}"
            elif min == 0 and max != 0:
                return f"{bd_table} < {max}"
            else:
                return f"{bd_table} BETWEEN {min} AND {max}"
        else:
            return ""

    # Метод, срабатывающий по нажатии на кнопку и отправляющий в БД запрос на фильтрацию данных
    def clickAccept(self):
        query = ""  # Сделать массив, который потом по порядку вбить в f-строку для запроса БД
        min_price, max_price = self.checkFields(self.leMinPrice.text(), self.leMaxPrice.text())
        min_tdp, max_tdp = self.checkFields(self.leMinTdp.text(), self.leMaxTdp.text())
        min_len, max_len = self.checkFields(self.leMinLen.text(), self.leMaxLen.text())
        # query += f'{min_price} {max_price} {min_tdp} {max_tdp} {min_len} {max_len}'
        query += self.checkMinMax(min_price, max_price, "Price") + " "
        query += self.checkMinMax(min_tdp, max_tdp, "Tdp") + " "
        query += self.checkMinMax(min_len, max_len, "Length") + " "

        query += self.getCheckBoxes(self.tableBrand)
        query += self.getCheckBoxes(self.tableProizv)
        query += self.getCheckBoxes(self.tableGraphProc)
        if self.page == 0:  # 0 - склад, 1 - конфигуратор
            self.parent.query += query
            self.parent.send_sql_sklad()
        else:
            self.parent.query += query
            self.parent.send_sql_conf()
        self.close()
