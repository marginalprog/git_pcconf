import psycopg2
import re

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QPixmap, QIcon, QIntValidator
# ----------файлы интерфейса---------------
from ui.filter import widgetVideoFilter, widgetProcFilter
from ui.filter import widgetMotherFilter, widgetCoolFilter
from ui.filter import widgetRamFilter, widgetDiskFilter
from ui.filter import widgetPowerFilter, widgetBodyFilter

from ui import warningWin


# Класс диалогового окна с кнопкой
class DialogOk(QDialog, warningWin.Ui_warningDialog):
    def __init__(self, error_win_title, error_text):
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


# Метод, считывающий отмеченные CheckBox-ами строки из таблицы. Возвращает отмеченные строки
def get_checkboxes(table, bd_column):
    selected_parameters = []
    result_selected = ""
    for i in range(table.rowCount()):
        widget = table.cellWidget(i, 0)
        if widget is not None:
            chk_box = widget.findChild(CheckBox)
            if chk_box is not None and chk_box.isChecked():
                selected_parameters.append(table.item(i, 1).text())
    if len(selected_parameters) == 0:  # Если ничего не выбрано в таблицах фильтра
        return result_selected
    if len(selected_parameters) == 1:
        return f" {bd_column} = '{selected_parameters[0]}' "
    if len(selected_parameters) > 1:
        for i in range(len(selected_parameters)):
            if i == 0:
                result_selected += f"({bd_column} = '{selected_parameters[i]}' "
            elif i == len(selected_parameters) - 1:
                result_selected += f" OR {bd_column} = '{selected_parameters[i]}') "
            else:
                result_selected += f" OR {bd_column} = '{selected_parameters[i]}' "
    # result_selected = selected_parameters[:len(selected_parameters) - 2]  # Удаляем лишние символы
    return result_selected


# Метод, считывающий отмеченные CheckBox-ами строки из таблицы. Возвращает отмеченные строки
def get_checkboxes_concat(table, bd_column):
    selected_parameters = []
    result_selected = ""
    for i in range(table.rowCount()):
        widget = table.cellWidget(i, 0)
        if widget is not None:
            chk_box = widget.findChild(CheckBox)
            if chk_box is not None and chk_box.isChecked():
                selected_parameters.append(table.item(i, 1).text())
    if len(selected_parameters) == 0:  # Если ничего не выбрано в таблицах фильтра
        return result_selected
    if len(selected_parameters) == 1:
        return f"{bd_column} like '%' || '{selected_parameters[0]}' || '%' "
    if len(selected_parameters) > 1:
        for i in range(len(selected_parameters)):
            if i == 0:
                result_selected += f"({bd_column} like '%' || '{selected_parameters[0]}' || "
            elif i == len(selected_parameters) - 1:
                result_selected += f" '%'  || '{selected_parameters[i]}') "
            else:
                result_selected += f" '%'  || '{selected_parameters[i]}' || "
    # result_selected = selected_parameters[:len(selected_parameters) - 2]  # Удаляем лишние символы
    print(result_selected)
    return result_selected


# Метод для сравнения значений полей (принимает .text())
def checkFields(min_field, max_field):
    if min_field != "" and max_field != "":
        if int(min_field) < int(max_field):
            return int(min_field), int(max_field)
        else:
            dialog = DialogOk("Ошибка", "Максимальные значения должны быть больше минимальных")
            dialog.show()
            return -1, -1
    elif min_field == "" and max_field == "":
        return 0, 0
    elif min_field != "" and max_field == "":
        return int(min_field), 0
    elif min_field == "" and max_field != "":
        return 0, int(max_field)


# Метод генерации параметров для запроса к БД (получает значения мин. и макс. знач. введённых полей)
def check_min_max(minimum, maximum, bd_column):
    if minimum != -1:  # Если не получили флаг ошибки(-1) - выполняем запрос к БД
        if minimum == 0 and maximum == 0:  # Если пустые поля, то по цене не производим фильтрацию
            # print("Конкатенации с другими запросами не будет")
            return ""
        elif minimum != 0 and maximum == 0:
            return f"{bd_column} >= {minimum} "
        elif minimum == 0 and maximum != 0:
            return f"{bd_column} <= {maximum} "
        else:
            return f"{bd_column} >= {minimum} AND {bd_column} <= {maximum} "
    else:
        return ""


# Метод обновления значений в поле при движении слайдера
def update_field_value(field, value):
    field.setText(f"{value}")


# Метод обновления слайдера при вводе значений в поле
def update_slider_value(slider, value, field):
    if value == "":
        slider.setValue(1)
        field.clear()
    else:
        slider.setValue(int(value))


# Метод создания cb на виджете
def create_checkbox():
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


def reset_checkboxes(table):
    for i in range(table.rowCount()):
        table.clearSelection()
        widget = table.cellWidget(i, 0)
        if widget is not None:
            chk_box = widget.findChild(CheckBox)
            if chk_box is not None and chk_box.isChecked():
                chk_box.setChecked(False)


# Метод, обнуляющий значения слайдеров
def reset_sliders(slider_min, slider_max, le_min, le_max):
    slider_min.setValue(0)
    slider_max.setValue(0)
    le_min.clear()
    le_max.clear()


# Метод вставки в таблицу checkbox
def insert_cb(table):
    row_count = table.rowCount()
    for i in range(row_count):
        widget, checkbox = create_checkbox()
        checkbox.clicked.connect(
            lambda ch, row=i: current_pos(ch, row, table))
        table.setCellWidget(i, 0, widget)


def cell_row(row, column, table):
    widget = table.cellWidget(row, 0)
    if widget is not None:
        checkbox = widget.findChild(CheckBox)
        if checkbox.isChecked():
            checkbox.click()
        else:
            checkbox.click()
        table.selectRow(row)


def current_pos(ch, row, table):
    # print(f' row = {row} -- {ch}')
    table.selectRow(row)


class VideoFilter(QtWidgets.QWidget, widgetVideoFilter.Ui_WidgetVideoFilter):
    def __init__(self, tab, mainWindow):
        super().__init__()
        self.setupUi(self)
        self.mainWindow = mainWindow
        self.tab_window = tab  # Где было создано окно фильтрации - в конфигураторе или на складе
        # -------------Сигналы обновления значений в полях при движении слайдера------------
        self.sliderPriceMin.valueChanged.connect(lambda value: update_field_value(self.leMinPrice, value))
        self.sliderPriceMax.valueChanged.connect(lambda value: update_field_value(self.leMaxPrice, value))
        self.sliderTdpMin.valueChanged.connect(lambda value: update_field_value(self.leMinTdp, value))
        self.sliderTdpMax.valueChanged.connect(lambda value: update_field_value(self.leMaxTdp, value))
        self.sliderLenMin.valueChanged.connect(lambda value: update_field_value(self.leMinLen, value))
        self.sliderLenMax.valueChanged.connect(lambda value: update_field_value(self.leMaxLen, value))
        # -------------Сигналы обновления значений в слайдерах при вводе числа------------
        self.leMinPrice.textChanged.connect(
            lambda value: update_slider_value(self.sliderPriceMin, value, self.leMinPrice))
        self.leMaxPrice.textChanged.connect(
            lambda value: update_slider_value(self.sliderPriceMax, value, self.leMaxPrice))
        self.leMinTdp.textChanged.connect(
            lambda value: update_slider_value(self.sliderTdpMin, value, self.leMinTdp))
        self.leMaxTdp.textChanged.connect(
            lambda value: update_slider_value(self.sliderTdpMax, value, self.leMaxTdp))
        self.leMinLen.textChanged.connect(
            lambda value: update_slider_value(self.sliderLenMin, value, self.leMinLen))
        self.leMaxLen.textChanged.connect(
            lambda value: update_slider_value(self.sliderLenMax, value, self.leMaxLen))

        # ----------------------------------------------------------------------------------

        # -------------------Задание ограничений для полей ввода-------------------
        only_int = QIntValidator()
        only_int.setRange(0, 999999)

        two_digits_int = QIntValidator()
        two_digits_int.setRange(0, 99)

        three_digits_int = QIntValidator()
        three_digits_int.setRange(0, 999)

        six_digits_int = QIntValidator()
        six_digits_int.setRange(0, 999999)

        self.leMinPrice.setValidator(six_digits_int)
        self.leMaxPrice.setValidator(six_digits_int)
        self.leMinTdp.setValidator(three_digits_int)
        self.leMaxTdp.setValidator(three_digits_int)
        self.leMinLen.setValidator(two_digits_int)
        self.leMaxLen.setValidator(two_digits_int)
        # -------------------Задание ограничений для полей ввода-------------------

        # -------------------Установка ширины столбцов для таблиц-------------------
        self.tableProizv.setColumnWidth(0, 40)
        self.tableProizv.setColumnWidth(1, 243)
        self.tableProizv.cellClicked.connect(
            lambda row, column, table=self.tableProizv:
            cell_row(row, column, table))

        self.tableChipCreator.setColumnWidth(0, 40)
        self.tableChipCreator.setColumnWidth(1, 243)
        self.tableChipCreator.cellClicked.connect(
            lambda row, column, table=self.tableChipCreator:
            cell_row(row, column, table))

        self.tableGraphProc.setColumnWidth(0, 40)
        self.tableGraphProc.setColumnWidth(1, 243)
        self.tableGraphProc.cellClicked.connect(
            lambda row, column, table=self.tableGraphProc:
            cell_row(row, column, table))

        self.tableGaming.setColumnWidth(0, 40)
        self.tableGaming.setColumnWidth(1, 243)
        self.tableGaming.cellClicked.connect(
            lambda row, column, table=self.tableGaming:
            cell_row(row, column, table))

        self.tableVolume.setColumnWidth(0, 40)
        self.tableVolume.setColumnWidth(1, 243)
        self.tableVolume.cellClicked.connect(
            lambda row, column, table=self.tableVolume:
            cell_row(row, column, table))

        self.tableType.setColumnWidth(0, 40)
        self.tableType.setColumnWidth(1, 243)
        self.tableType.cellClicked.connect(
            lambda row, column, table=self.tableType:
            cell_row(row, column, table))

        self.tableFreq.setColumnWidth(0, 40)
        self.tableFreq.setColumnWidth(1, 243)
        self.tableFreq.cellClicked.connect(
            lambda row, column, table=self.tableFreq:
            cell_row(row, column, table))

        self.tableBus.setColumnWidth(0, 40)
        self.tableBus.setColumnWidth(1, 243)
        self.tableBus.cellClicked.connect(
            lambda row, column, table=self.tableBus:
            cell_row(row, column, table))

        self.tableInterface.setColumnWidth(0, 40)
        self.tableInterface.setColumnWidth(1, 243)
        self.tableInterface.cellClicked.connect(
            lambda row, column, table=self.tableInterface:
            cell_row(row, column, table))

        self.tableMonitor.setColumnWidth(0, 40)
        self.tableMonitor.setColumnWidth(1, 243)
        self.tableMonitor.cellClicked.connect(
            lambda row, column, table=self.tableMonitor:
            cell_row(row, column, table))

        self.tableResolution.setColumnWidth(0, 40)
        self.tableResolution.setColumnWidth(1, 243)
        self.tableResolution.cellClicked.connect(
            lambda row, column, table=self.tableResolution:
            cell_row(row, column, table))
        # ------------------------------------------------------------------

        # -----------Соединение кнопок сбосов с методом обнуления-----------
        self.btnResetAll.clicked.connect(self.resetAll)
        self.btnResetPrice.clicked.connect(
            lambda: reset_sliders(self.sliderPriceMin, self.sliderPriceMax, self.leMinPrice, self.leMaxPrice))
        self.btnResetTdp.clicked.connect(
            lambda: reset_sliders(self.sliderTdpMin, self.sliderTdpMax, self.leMinTdp, self.leMaxTdp))
        self.btnResetLen.clicked.connect(
            lambda: reset_sliders(self.sliderLenMin, self.sliderLenMax, self.leMinLen, self.leMaxLen))
        self.btnResetProizv.clicked.connect(lambda: reset_checkboxes(self.tableProizv))
        self.btnResetChipCreator.clicked.connect(lambda: reset_checkboxes(self.tableChipCreator))
        self.btnResetGraphProc.clicked.connect(lambda: reset_checkboxes(self.tableGraphProc))
        self.btnResetGaming.clicked.connect(lambda: reset_checkboxes(self.tableGaming))
        self.btnResetVolume.clicked.connect(lambda: reset_checkboxes(self.tableVolume))
        self.btnResetType.clicked.connect(lambda: reset_checkboxes(self.tableType))
        self.btnResetFreq.clicked.connect(lambda: reset_checkboxes(self.tableFreq))
        self.btnResetBus.clicked.connect(lambda: reset_checkboxes(self.tableBus))
        self.btnResetInterface.clicked.connect(lambda: reset_checkboxes(self.tableInterface))
        self.btnResetMonitor.clicked.connect(lambda: reset_checkboxes(self.tableMonitor))
        self.btnResetResolution.clicked.connect(lambda: reset_checkboxes(self.tableResolution))
        # -------------------Соединение кнопк сбосов с методом обнуления-------------------

        # Изменение положения стрелки при нажатии на вкладку фильтра
        self.toolBoxVidFilter.currentChanged.connect(self.tb_change_arrows)

        # Если выбрана вкладка склада или конфигуратора И включён индикатор "Только в наличии"
        if self.tab_window == 0 and mainWindow.rbSklad.isChecked():
            self.load_exists_parameters()
        elif self.tab_window == 0:
            self.load_all_parameters()
        elif self.tab_window == 1 and mainWindow.rbConf.isChecked():
            self.load_exists_parameters()
        elif self.tab_window == 1:
            self.load_all_parameters()

        self.btnAccept.clicked.connect(lambda: self.click_accept(mainWindow))

    def load_all_parameters(self):
        """
            Метод, загружающий параметры всех видеокарт
        """
        self.tableProizv.clear()
        self.tableChipCreator.clear()
        self.tableGraphProc.clear()
        self.tableGaming.clear()
        self.tableVolume.clear()
        self.tableType.clear()
        self.tableFreq.clear()
        self.tableBus.clear()
        self.tableInterface.clear()
        self.tableMonitor.clear()
        self.tableResolution.clear()

        conn = None
        cur = None
        try:
            conn = psycopg2.connect(database="confPc",
                                    user="postgres",
                                    password="2001",
                                    host="localhost",
                                    port="5432")
            cur = conn.cursor()

            cur.execute(" SELECT price FROM videocard ORDER BY price DESC LIMIT 1")
            for name in cur:
                self.sliderPriceMin.setRange(0, int(name[0]))
                self.sliderPriceMax.setRange(0, int(name[0]))
                self.leMaxPrice.setPlaceholderText(f"до {int(name[0])}")

            cur.execute(" SELECT tdp FROM videocard ORDER BY tdp DESC LIMIT 1")
            for name in cur:
                self.sliderTdpMin.setRange(0, int(name[0]))
                self.sliderTdpMax.setRange(0, int(name[0]))
                self.leMaxTdp.setPlaceholderText(f"до {int(name[0])}")

            cur.execute(" SELECT length FROM videocard ORDER BY length DESC LIMIT 1")
            for name in cur:
                self.sliderLenMin.setRange(0, int(name[0]))
                self.sliderLenMax.setRange(0, int(name[0]))
                self.leMaxLen.setPlaceholderText(f"до {int(name[0])}")

            cur.execute("SELECT DISTINCT name FROM proizv_videocard, videocard "
                        "WHERE proizv_videocard.id = videocard.id_proizv "
                        "ORDER BY name ASC")
            row_count = 0
            for name in cur:
                self.tableProizv.setRowCount(row_count + 1)
                self.tableProizv.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT chipcreator FROM videocard "
                        "ORDER BY chipcreator ASC")
            for name in cur:
                self.tableChipCreator.setRowCount(row_count + 1)
                self.tableChipCreator.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT chipname FROM videocard "
                        "ORDER BY chipname ASC")
            for name in cur:
                self.tableGraphProc.setRowCount(row_count + 1)
                self.tableGraphProc.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT gaming FROM videocard "
                        "ORDER BY gaming ASC")
            for name in cur:
                self.tableGaming.setRowCount(row_count + 1)
                self.tableGaming.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT vram FROM videocard "
                        "ORDER BY vram ASC")
            for name in cur:
                self.tableVolume.setRowCount(row_count + 1)
                self.tableVolume.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT typevram FROM videocard "
                        "ORDER BY typevram ASC")
            for name in cur:
                self.tableType.setRowCount(row_count + 1)
                self.tableType.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT frequency FROM videocard "
                        "ORDER BY frequency ASC")
            for name in cur:
                self.tableFreq.setRowCount(row_count + 1)
                self.tableFreq.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT bus FROM videocard "
                        "ORDER BY bus ASC")
            for name in cur:
                self.tableBus.setRowCount(row_count + 1)
                self.tableBus.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT interface FROM videocard "
                        "ORDER BY interface ASC")
            for name in cur:
                self.tableInterface.setRowCount(row_count + 1)
                self.tableInterface.setItem(row_count, 1, QtWidgets.QTableWidgetItem(name[0]))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT monitor FROM videocard "
                        "ORDER BY monitor ASC")
            for name in cur:
                self.tableMonitor.setRowCount(row_count + 1)
                self.tableMonitor.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT resolution FROM videocard "
                        "ORDER BY resolution ASC")
            for name in cur:
                self.tableResolution.setRowCount(row_count + 1)
                self.tableResolution.setItem(row_count, 1, QtWidgets.QTableWidgetItem(name[0]))
                row_count += 1

            # Заполнение таблиц кнопками CB
            self.pasteCheckBoxes()

        except (Exception, psycopg2.DatabaseError) as error:
            dialog = DialogOk("Ошибка", error)
            dialog.show()

        finally:
            if conn:
                cur.close()
                conn.close()

    def load_exists_parameters(self):
        """
            Метод, загружающий параметры имеющихся в наличии видеокарт
        """
        self.tableProizv.clear()
        self.tableChipCreator.clear()
        self.tableGaming.clear()
        self.tableGraphProc.clear()
        self.tableVolume.clear()
        self.tableType.clear()
        self.tableFreq.clear()
        self.tableBus.clear()
        self.tableInterface.clear()
        self.tableMonitor.clear()
        self.tableResolution.clear()

        conn = None
        cur = None
        try:
            conn = psycopg2.connect(database="confPc",
                                    user="postgres",
                                    password="2001",
                                    host="localhost",
                                    port="5432")
            cur = conn.cursor()

            cur.execute(" SELECT price FROM videocard WHERE exist = True ORDER BY price DESC LIMIT 1")
            for name in cur:
                self.sliderPriceMin.setRange(0, int(name[0]))
                self.sliderPriceMax.setRange(0, int(name[0]))
                self.leMaxPrice.setPlaceholderText(f"до {int(name[0])}")

            cur.execute(" SELECT tdp FROM videocard WHERE exist = True ORDER BY tdp DESC LIMIT 1")
            for name in cur:
                self.sliderTdpMin.setRange(0, int(name[0]))
                self.sliderTdpMax.setRange(0, int(name[0]))
                self.leMaxTdp.setPlaceholderText(f"до {int(name[0])}")

            cur.execute(" SELECT length FROM videocard WHERE exist = True ORDER BY length DESC LIMIT 1")
            for name in cur:
                self.sliderLenMin.setRange(0, int(name[0]))
                self.sliderLenMax.setRange(0, int(name[0]))
                self.leMaxLen.setPlaceholderText(f"до {int(name[0])}")

            cur.execute("SELECT DISTINCT name FROM proizv_videocard, videocard "
                        "WHERE proizv_videocard.id = videocard.id_proizv "
                        "AND videocard.exist = True "
                        "ORDER BY name ASC ")
            row_count = 0
            for name in cur:
                self.tableProizv.setRowCount(row_count + 1)
                self.tableProizv.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT chipcreator FROM videocard WHERE exist = True "
                        "ORDER BY chipcreator ASC")
            for name in cur:
                self.tableChipCreator.setRowCount(row_count + 1)
                self.tableChipCreator.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT chipname FROM videocard WHERE exist = True "
                        "ORDER BY chipname ASC")
            for name in cur:
                self.tableGraphProc.setRowCount(row_count + 1)
                self.tableGraphProc.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT gaming FROM videocard WHERE exist = True  "
                        "ORDER BY gaming ASC")
            for name in cur:
                self.tableGaming.setRowCount(row_count + 1)
                self.tableGaming.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT vram FROM videocard WHERE exist = True "
                        "ORDER BY vram ASC")
            for name in cur:
                self.tableVolume.setRowCount(row_count + 1)
                self.tableVolume.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT typevram FROM videocard WHERE exist = True "
                        "ORDER BY typevram ASC")
            for name in cur:
                self.tableType.setRowCount(row_count + 1)
                self.tableType.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT frequency FROM videocard WHERE exist = True "
                        "ORDER BY frequency ASC")
            for name in cur:
                self.tableFreq.setRowCount(row_count + 1)
                self.tableFreq.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT bus FROM videocard WHERE exist = True "
                        "ORDER BY bus ASC")
            for name in cur:
                self.tableBus.setRowCount(row_count + 1)
                self.tableBus.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT interface FROM videocard WHERE exist = True "
                        "ORDER BY interface ASC")
            for name in cur:
                self.tableInterface.setRowCount(row_count + 1)
                self.tableInterface.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT monitor FROM videocard WHERE exist = True "
                        "ORDER BY monitor ASC")
            for name in cur:
                self.tableMonitor.setRowCount(row_count + 1)
                self.tableMonitor.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT resolution FROM videocard WHERE exist = True "
                        "ORDER BY resolution ASC")
            for name in cur:
                self.tableResolution.setRowCount(row_count + 1)
                self.tableResolution.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            # Заполнение таблиц кнопками CB
            self.pasteCheckBoxes()

        except (Exception, psycopg2.DatabaseError) as error:
            dialog = DialogOk("Ошибка", error)
            dialog.show()

        finally:
            if conn:
                cur.close()
                conn.close()

    def tb_change_arrows(self, page):
        self.toolBoxVidFilter.setItemIcon(page, QIcon("E:/pcconf/images/up-arrow.png"))
        for i in range(self.toolBoxVidFilter.count()):
            if i != page:
                self.toolBoxVidFilter.setItemIcon(i, QIcon("E:/pcconf/images/down-arrow.png"))

    # Метод для вставки CB в таблицы
    def pasteCheckBoxes(self):
        insert_cb(self.tableProizv)
        insert_cb(self.tableChipCreator)
        insert_cb(self.tableGraphProc)
        insert_cb(self.tableGaming)
        insert_cb(self.tableVolume)
        insert_cb(self.tableType)
        insert_cb(self.tableFreq)
        insert_cb(self.tableBus)
        insert_cb(self.tableInterface)
        insert_cb(self.tableMonitor)
        insert_cb(self.tableResolution)

    # Метод, обнуляющий все поля
    def resetAll(self):
        reset_sliders(self.sliderPriceMin, self.sliderPriceMax, self.leMinPrice, self.leMaxPrice)
        reset_sliders(self.sliderTdpMin, self.sliderTdpMax, self.leMinTdp, self.leMaxTdp)
        reset_sliders(self.sliderLenMin, self.sliderLenMax, self.leMinLen, self.leMaxLen)
        reset_checkboxes(self.tableProizv)
        reset_checkboxes(self.tableChipCreator)
        reset_checkboxes(self.tableGaming)
        reset_checkboxes(self.tableGraphProc)
        reset_checkboxes(self.tableVolume)
        reset_checkboxes(self.tableType)
        reset_checkboxes(self.tableFreq)
        reset_checkboxes(self.tableBus)
        reset_checkboxes(self.tableInterface)
        reset_checkboxes(self.tableMonitor)
        reset_checkboxes(self.tableResolution)

    # Метод, срабатывающий по нажатии на кнопку и отправляющий в БД запрос на фильтрацию данных
    def click_accept(self, mainWindow):
        query = "SELECT kol, videocard.exist, videocard.id, proizv_videocard.name, fullname, gaming, " \
                "chipcreator, chipname, vram, typevram, frequency, bus, interface, monitor, " \
                "resolution, tdp, length, connvideo, kolconnvideo, price " \
                "FROM videocard, sklad_videocard, proizv_videocard " \
                "WHERE "

        min_price, max_price = checkFields(self.leMinPrice.text(), self.leMaxPrice.text())
        min_tdp, max_tdp = checkFields(self.leMinTdp.text(), self.leMaxTdp.text())
        min_len, max_len = checkFields(self.leMinLen.text(), self.leMaxLen.text())
        if min_price == -1 or min_tdp == -1 or min_len == -1:  # если не вернулось -1, то выполняем фильтрацию
            pass
        else:
            query1 = get_checkboxes(self.tableProizv, "proizv_videocard.name")
            if query1 != "":  # Если есть что добавить к запросу
                query += query1

            if query1 == "":  # Если первая таблица пустая, то добавляем к запросу без AND
                query2 = get_checkboxes(self.tableChipCreator, "chipcreator")
                query += query2
            else:
                query2 = get_checkboxes(self.tableChipCreator, "chipcreator")
                if query2 != "":  # Если есть что добавить к запросу
                    query += " AND " + query2

            if query1 == "" and query2 == "":  # Если первая таблица пустая, то добавляем к запросу без AND
                query3 = get_checkboxes(self.tableGraphProc, "chipname")
                query += query3
            else:
                query3 = get_checkboxes(self.tableGraphProc, "chipname")
                if query3 != "":  # Если есть что добавить к запросу
                    query += " AND " + query3

            if query1 == "" and query2 == "" and query3 == "":
                query4 = get_checkboxes(self.tableGaming, "gaming")
                query += query4
            else:
                query4 = get_checkboxes(self.tableGaming, "gaming")
                if query4 != "":
                    query += " AND " + query4

            if query1 == "" and query2 == "" and query3 == "" and query4 == "":
                query5 = get_checkboxes(self.tableVolume, "vram")
                query += query5
            else:
                query5 = get_checkboxes(self.tableVolume, "vram")
                if query5 != "":
                    query += " AND " + query5

            if query1 == "" and query2 == "" and query3 == "" and query4 == "" and query5 == "":
                query6 = get_checkboxes(self.tableType, "typevram")
                query += query6
            else:
                query6 = get_checkboxes(self.tableType, "typevram")
                if query6 != "":
                    query += " AND " + query6

            if query1 == "" and query2 == "" and query3 == "" and query4 == "" and query5 == "" and query6 == "":
                query7 = get_checkboxes(self.tableFreq, "frequency")
                query += query7
            else:
                query7 = get_checkboxes(self.tableFreq, "frequency")
                if query7 != "":
                    query += " AND " + query7

            if query1 == "" and query2 == "" and query3 == "" and query4 == "" and query5 == "" and query6 == "" \
                    and query7 == "":
                query8 = get_checkboxes(self.tableBus, "bus")
                query += query8
            else:
                query8 = get_checkboxes(self.tableBus, "bus")
                if query8 != "":
                    query += " AND " + query8

            if query1 == "" and query2 == "" and query3 == "" and query4 == "" and query5 == "" and query6 == "" \
                    and query7 == "" and query8 == "":
                query9 = get_checkboxes(self.tableInterface, "interface")
                query += query9
            else:
                query9 = get_checkboxes(self.tableInterface, "interface")
                if query9 != "":
                    query += " AND " + query9

            if query1 == "" and query2 == "" and query3 == "" and query4 == "" and query5 == "" and query6 == "" \
                    and query7 == "" and query8 == "" and query9 == "":
                query10 = get_checkboxes(self.tableMonitor, "monitor")
                query += query10
            else:
                query10 = get_checkboxes(self.tableMonitor, "monitor")
                if query10 != "":
                    query += " AND " + query10

            if query1 == "" and query2 == "" and query3 == "" and query4 == "" and query5 == "" and query6 == "" \
                    and query7 == "" and query8 == "" and query9 == "" and query10 == "":
                query11 = get_checkboxes(self.tableResolution, "resolution")
                query += query11
            else:
                query11 = get_checkboxes(self.tableResolution, "resolution")
                if query11 != "":
                    query += " AND " + query11

            # Вероятно, в проверке слайдеров есть лишние if
            if query1 == "" and query2 == "" and query3 == "" and query4 == "" and query5 == "" and query6 == "" \
                    and query7 == "" and query8 == "" and query9 == "" and query10 == "" and query11 == "":  # Если не выбрано ничего в таблицах
                query += check_min_max(min_price, max_price, "Price")
            else:
                if min_price != 0 or max_price != 0:
                    query += " AND " + check_min_max(min_price, max_price, "Price")

            if query1 == "" and query2 == "" and query3 == "" and query4 == "" and query5 == "" and query6 == "" \
                    and query7 == "" and query8 == "" and query9 == "" and query10 == "" and query11 == "" \
                    and (min_price == 0 and max_price == 0):
                query += check_min_max(min_tdp, max_tdp, "Tdp")
            else:
                if min_tdp != 0 or max_tdp != 0:
                    query += " AND " + check_min_max(min_tdp, max_tdp, "Tdp")

            if query1 == "" and query2 == "" and query3 == "" and query4 == "" and query5 == "" and query6 == "" \
                    and query7 == "" and query8 == "" and query9 == "" and query10 == "" and query11 == "" \
                    and (min_price == 0 and max_price == 0) and (min_tdp == 0 and max_tdp == 0):
                query += check_min_max(min_len, max_len, "Length")
            else:
                if min_len != 0 or max_len != 0:
                    query += " AND " + check_min_max(min_len, max_len, "Length")

            mainWindow.tabWidgetSklad.setCurrentIndex(0)  # Устанавливаем вкладку перед фильтрацией на 0 место

            # Если изменений в фильтрации не было, то передаём changes = False
            if query == "SELECT kol, videocard.exist, videocard.id, proizv_videocard.name, fullname, gaming, " \
                        "chipcreator, chipname, vram, typevram, frequency, bus, interface, monitor, " \
                        "resolution, tdp, length, connvideo, kolconnvideo, price " \
                        "FROM videocard, sklad_videocard, proizv_videocard " \
                        "WHERE ":

                if self.tab_window == 0:  # Если открыта вкладка "Склад", то применяем фильтры для склада
                    # Переопределяем готовым запросом
                    query = self.make_query_filter(False, mainWindow.rbSklad.isChecked())
                    mainWindow.apply_filter_sklad(query, 0)
                    self.close()
                else:  # Если открыта вкладка "Конфигуратор", то применяем фильтры для конфигуратора
                    query = self.make_query_filter(False, mainWindow.rbConf.isChecked())
                    mainWindow.apply_filter_conf(query, 0)
                    self.close()

            # Если фильтры были выбраны (начальный запрос изменился), то передаём changes = True
            else:
                if self.tab_window == 0:
                    # Дописываем финальную часть запроса (отбор по id, exist и ранжирование) для склада
                    query += self.make_query_filter(True, mainWindow.rbSklad.isChecked())
                    mainWindow.apply_filter_sklad(query, 0)
                    self.close()
                else:
                    # Дописываем финальную часть запроса (отбор по id, exist и ранжирование) для конфигуратора
                    query += self.make_query_filter(True, mainWindow.rbConf.isChecked())
                    mainWindow.apply_filter_conf(query, 0)
                    self.close()

    def make_query_filter(self, changes, having):
        if changes:  # Если есть изменения, то добавляем к запросу связывающие таблицы фильтры
            if having:  # Если отмечен переключатель наличия
                query = " AND videocard.id = sklad_videocard.id_izd AND videocard.id_proizv = proizv_videocard.id" \
                        " AND videocard.exist = True" \
                        " ORDER BY exist DESC"
                return query
            else:
                query = " AND videocard.id = sklad_videocard.id_izd AND videocard.id_proizv = proizv_videocard.id" \
                        " ORDER BY exist DESC"
                return query

        # Если фильтры не выбраны
        else:
            if having:
                query = "SELECT kol, videocard.exist, videocard.id, proizv_videocard.name, fullname, gaming, " \
                        "chipcreator, chipname, vram, typevram, frequency, bus, interface, monitor, " \
                        "resolution, tdp, length, connvideo, kolconnvideo, price " \
                        "FROM videocard, sklad_videocard, proizv_videocard " \
                        "WHERE videocard.id = sklad_videocard.id_izd " \
                        "AND videocard.id_proizv = proizv_videocard.id " \
                        "AND videocard.exist = True " \
                        "ORDER BY exist DESC "
                return query
            else:
                query = "SELECT kol, videocard.exist, videocard.id, proizv_videocard.name, fullname, gaming, " \
                        "chipcreator, chipname, vram, typevram, frequency, bus, interface, monitor, " \
                        "resolution, tdp, length, connvideo, kolconnvideo, price " \
                        "FROM videocard, sklad_videocard, proizv_videocard " \
                        "WHERE videocard.id = sklad_videocard.id_izd " \
                        "AND videocard.id_proizv = proizv_videocard.id " \
                        "ORDER BY exist DESC "
                return query


class ProcFilter(QtWidgets.QWidget, widgetProcFilter.Ui_WidgetProcFilter):
    def __init__(self, tab, mainWindow):
        super().__init__()
        self.setupUi(self)
        self.mainWindow = mainWindow
        self.tab_window = tab  # Где было создано окно фильтрации - в конфигураторе или на складе
        # -------------Сигналы обновления значений в полях при движении слайдера------------
        self.sliderPriceMin.valueChanged.connect(lambda value: update_field_value(self.leMinPrice, value))
        self.sliderPriceMax.valueChanged.connect(lambda value: update_field_value(self.leMaxPrice, value))
        self.sliderTdpMin.valueChanged.connect(lambda value: update_field_value(self.leMinTdp, value))
        self.sliderTdpMax.valueChanged.connect(lambda value: update_field_value(self.leMaxTdp, value))
        # -------------Сигналы обновления значений в слайдерах при вводе числа------------
        self.leMinPrice.textChanged.connect(
            lambda value: update_slider_value(self.sliderPriceMin, value, self.leMinPrice))
        self.leMaxPrice.textChanged.connect(
            lambda value: update_slider_value(self.sliderPriceMax, value, self.leMaxPrice))
        self.leMinTdp.textChanged.connect(
            lambda value: update_slider_value(self.sliderTdpMin, value, self.leMinTdp))
        self.leMaxTdp.textChanged.connect(
            lambda value: update_slider_value(self.sliderTdpMax, value, self.leMaxTdp))
        # ----------------------------------------------------------------------------------

        # -------------------Задание ограничений для полей ввода-------------------
        only_int = QIntValidator()
        only_int.setRange(0, 999999)

        two_digits_int = QIntValidator()
        two_digits_int.setRange(0, 99)

        three_digits_int = QIntValidator()
        three_digits_int.setRange(0, 999)

        six_digits_int = QIntValidator()
        six_digits_int.setRange(0, 999999)

        self.leMinPrice.setValidator(six_digits_int)
        self.leMaxPrice.setValidator(six_digits_int)
        self.leMinTdp.setValidator(three_digits_int)
        self.leMaxTdp.setValidator(three_digits_int)
        # -------------------Задание ограничений для полей ввода-------------------

        # -------------------Установка ширины столбцов для таблиц-------------------
        self.tableProizv.setColumnWidth(0, 40)
        self.tableProizv.setColumnWidth(1, 243)
        self.tableProizv.cellClicked.connect(
            lambda row, column, table=self.tableProizv:
            cell_row(row, column, table))

        self.tableSeries.setColumnWidth(0, 40)
        self.tableSeries.setColumnWidth(1, 243)
        self.tableSeries.cellClicked.connect(
            lambda row, column, table=self.tableSeries:
            cell_row(row, column, table))

        self.tableGraphProc.setColumnWidth(0, 40)
        self.tableGraphProc.setColumnWidth(1, 243)
        self.tableGraphProc.cellClicked.connect(
            lambda row, column, table=self.tableGraphProc:
            cell_row(row, column, table))

        self.tableGaming.setColumnWidth(0, 40)
        self.tableGaming.setColumnWidth(1, 243)
        self.tableGaming.cellClicked.connect(
            lambda row, column, table=self.tableGaming:
            cell_row(row, column, table))

        self.tableSocket.setColumnWidth(0, 40)
        self.tableSocket.setColumnWidth(1, 243)
        self.tableSocket.cellClicked.connect(
            lambda row, column, table=self.tableSocket:
            cell_row(row, column, table))

        self.tableCore.setColumnWidth(0, 40)
        self.tableCore.setColumnWidth(1, 243)
        self.tableCore.cellClicked.connect(
            lambda row, column, table=self.tableCore:
            cell_row(row, column, table))

        self.tableNcores.setColumnWidth(0, 40)
        self.tableNcores.setColumnWidth(1, 243)
        self.tableNcores.cellClicked.connect(
            lambda row, column, table=self.tableNcores:
            cell_row(row, column, table))

        self.tableFreq.setColumnWidth(0, 40)
        self.tableFreq.setColumnWidth(1, 243)
        self.tableFreq.cellClicked.connect(
            lambda row, column, table=self.tableFreq:
            cell_row(row, column, table))

        self.tableCache.setColumnWidth(0, 40)
        self.tableCache.setColumnWidth(1, 243)
        self.tableCache.cellClicked.connect(
            lambda row, column, table=self.tableCache:
            cell_row(row, column, table))

        self.tableTechproc.setColumnWidth(0, 40)
        self.tableTechproc.setColumnWidth(1, 243)
        self.tableTechproc.cellClicked.connect(
            lambda row, column, table=self.tableTechproc:
            cell_row(row, column, table))

        self.tableRamFreq.setColumnWidth(0, 40)
        self.tableRamFreq.setColumnWidth(1, 243)
        self.tableRamFreq.cellClicked.connect(
            lambda row, column, table=self.tableRamFreq:
            cell_row(row, column, table))
        # ------------------------------------------------------------------

        # -----------Соединение кнопок сбосов с методом обнуления-----------
        self.btnResetAll.clicked.connect(self.resetAll)
        self.btnResetPrice.clicked.connect(
            lambda: reset_sliders(self.sliderPriceMin, self.sliderPriceMax, self.leMinPrice, self.leMaxPrice))
        self.btnResetTdp.clicked.connect(
            lambda: reset_sliders(self.sliderTdpMin, self.sliderTdpMax, self.leMinTdp, self.leMaxTdp))
        self.btnResetProizv.clicked.connect(lambda: reset_checkboxes(self.tableProizv))
        self.btnResetSeries.clicked.connect(lambda: reset_checkboxes(self.tableSeries))
        self.btnResetGaming.clicked.connect(lambda: reset_checkboxes(self.tableGaming))
        self.btnResetSocket.clicked.connect(lambda: reset_checkboxes(self.tableSocket))
        self.btnResetCore.clicked.connect(lambda: reset_checkboxes(self.tableCore))
        self.btnResetFreq.clicked.connect(lambda: reset_checkboxes(self.tableFreq))
        self.btnResetNcores.clicked.connect(lambda: reset_checkboxes(self.tableNcores))
        self.btnResetCache.clicked.connect(lambda: reset_checkboxes(self.tableCache))
        self.btnResetTechproc.clicked.connect(lambda: reset_checkboxes(self.tableTechproc))
        self.btnResetRamFreq.clicked.connect(lambda: reset_checkboxes(self.tableRamFreq))
        self.btnResetGraphProc.clicked.connect(lambda: reset_checkboxes(self.tableGraphProc))
        # -------------------Соединение кнопк сбосов с методом обнуления-------------------

        # Изменение положения стрелки при нажатии на вкладку фильтра
        self.toolBoxProcFilter.currentChanged.connect(self.tb_change_arrows)

        # Если выбрана вкладка склада или конфигуратора И включён индикатор "Только в наличии"
        if self.tab_window == 0 and mainWindow.rbSklad.isChecked():
            self.load_exists_parameters()
        elif self.tab_window == 0:
            self.load_all_parameters()
        elif self.tab_window == 1 and mainWindow.rbConf.isChecked():
            self.load_exists_parameters()
        elif self.tab_window == 1:
            self.load_all_parameters()

        self.btnAccept.clicked.connect(lambda: self.click_accept(mainWindow))

    def load_all_parameters(self):
        """
            Метод, загружающий параметры всех видеокарт
        """
        self.tableProizv.clear()
        self.tableSeries.clear()
        self.tableGraphProc.clear()
        self.tableGaming.clear()
        self.tableSocket.clear()
        self.tableCore.clear()
        self.tableNcores.clear()
        self.tableFreq.clear()
        self.tableCache.clear()
        self.tableTechproc.clear()
        self.tableRamFreq.clear()

        conn = None
        cur = None
        try:
            conn = psycopg2.connect(database="confPc",
                                    user="postgres",
                                    password="2001",
                                    host="localhost",
                                    port="5432")
            cur = conn.cursor()
            # Задание слайдерам максимального значения из имеющихся в БД данных
            cur.execute(" SELECT price FROM processor ORDER BY price DESC LIMIT 1")
            for name in cur:
                self.sliderPriceMin.setRange(0, int(name[0]))
                self.sliderPriceMax.setRange(0, int(name[0]))
                self.leMaxPrice.setPlaceholderText(f"до {int(name[0])}")

            cur.execute(" SELECT tdp FROM processor ORDER BY tdp DESC LIMIT 1")
            for name in cur:
                self.sliderTdpMin.setRange(0, int(name[0]))
                self.sliderTdpMax.setRange(0, int(name[0]))
                self.leMaxTdp.setPlaceholderText(f"до {int(name[0])}")

            cur.execute("SELECT DISTINCT name FROM proizv_processor, processor "
                        "WHERE proizv_processor.id = processor.id_proizv "
                        "ORDER BY name ASC")
            row_count = 0
            for name in cur:
                self.tableProizv.setRowCount(row_count + 1)
                self.tableProizv.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT series FROM processor "
                        "ORDER BY series ASC")
            for name in cur:
                self.tableSeries.setRowCount(row_count + 1)
                self.tableSeries.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT graphics FROM processor "
                        "ORDER BY graphics ASC")
            for name in cur:
                self.tableGraphProc.setRowCount(row_count + 1)
                self.tableGraphProc.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT gaming FROM processor "
                        "ORDER BY gaming ASC")
            for name in cur:
                self.tableGaming.setRowCount(row_count + 1)
                self.tableGaming.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT socket FROM processor "
                        "ORDER BY socket ASC")
            for name in cur:
                self.tableSocket.setRowCount(row_count + 1)
                self.tableSocket.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT core FROM processor "
                        "ORDER BY core ASC")
            for name in cur:
                self.tableCore.setRowCount(row_count + 1)
                self.tableCore.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT frequency FROM processor "
                        "ORDER BY frequency ASC")
            for name in cur:
                self.tableFreq.setRowCount(row_count + 1)
                self.tableFreq.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT ncores FROM processor "
                        "ORDER BY ncores ASC")
            for name in cur:
                self.tableNcores.setRowCount(row_count + 1)
                self.tableNcores.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT cache FROM processor "
                        "ORDER BY cache ASC")
            for name in cur:
                self.tableCache.setRowCount(row_count + 1)
                self.tableCache.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT techproc FROM processor "
                        "ORDER BY techproc ASC")
            for name in cur:
                self.tableTechproc.setRowCount(row_count + 1)
                self.tableTechproc.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT ramfreq FROM processor "
                        "ORDER BY ramfreq ASC")
            for name in cur:
                self.tableRamFreq.setRowCount(row_count + 1)
                self.tableRamFreq.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            # Заполнение таблиц кнопками CB
            self.pasteCheckBoxes()

        except (Exception, psycopg2.DatabaseError) as error:
            dialog = DialogOk("Ошибка", error)
            dialog.show()

        finally:
            if conn:
                cur.close()
                conn.close()

    def load_exists_parameters(self):
        """
            Метод, загружающий параметры имеющихся в наличии видеокарт
        """
        self.tableProizv.clear()
        self.tableSeries.clear()
        self.tableGraphProc.clear()
        self.tableGaming.clear()
        self.tableSocket.clear()
        self.tableCore.clear()
        self.tableNcores.clear()
        self.tableFreq.clear()
        self.tableCache.clear()
        self.tableTechproc.clear()
        self.tableRamFreq.clear()

        conn = None
        cur = None
        try:
            conn = psycopg2.connect(database="confPc",
                                    user="postgres",
                                    password="2001",
                                    host="localhost",
                                    port="5432")
            cur = conn.cursor()
            # Задание слайдерам максимального значения из имеющихся в БД данных
            cur.execute(" SELECT price FROM processor WHERE exist = True ORDER BY price DESC LIMIT 1")
            for name in cur:
                self.sliderPriceMin.setRange(0, int(name[0]))
                self.sliderPriceMax.setRange(0, int(name[0]))
                self.leMaxPrice.setPlaceholderText(f"до {int(name[0])}")

            cur.execute(" SELECT tdp FROM processor WHERE exist = True ORDER BY tdp DESC LIMIT 1")
            for name in cur:
                self.sliderTdpMin.setRange(0, int(name[0]))
                self.sliderTdpMax.setRange(0, int(name[0]))
                self.leMaxTdp.setPlaceholderText(f"до {int(name[0])}")

            cur.execute("SELECT DISTINCT name FROM proizv_processor, processor "
                        "WHERE proizv_processor.id = processor.id_proizv "
                        "AND processor.exist = True "
                        "ORDER BY name ASC")
            row_count = 0
            for name in cur:
                self.tableProizv.setRowCount(row_count + 1)
                self.tableProizv.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT series FROM processor WHERE exist = True "
                        "ORDER BY series ASC")
            for name in cur:
                self.tableSeries.setRowCount(row_count + 1)
                self.tableSeries.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT graphics FROM processor WHERE exist = True "
                        "ORDER BY graphics ASC")
            for name in cur:
                self.tableGraphProc.setRowCount(row_count + 1)
                self.tableGraphProc.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT gaming FROM processor WHERE exist = True "
                        "ORDER BY gaming ASC")
            for name in cur:
                self.tableGaming.setRowCount(row_count + 1)
                self.tableGaming.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT socket FROM processor WHERE exist = True "
                        "ORDER BY socket ASC")
            for name in cur:
                self.tableSocket.setRowCount(row_count + 1)
                self.tableSocket.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT core FROM processor WHERE exist = True "
                        "ORDER BY core ASC")
            for name in cur:
                self.tableCore.setRowCount(row_count + 1)
                self.tableCore.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT frequency FROM processor WHERE exist = True "
                        "ORDER BY frequency ASC")
            for name in cur:
                self.tableFreq.setRowCount(row_count + 1)
                self.tableFreq.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT ncores FROM processor WHERE exist = True "
                        "ORDER BY ncores ASC")
            for name in cur:
                self.tableNcores.setRowCount(row_count + 1)
                self.tableNcores.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT cache FROM processor WHERE exist = True "
                        "ORDER BY cache ASC")
            for name in cur:
                self.tableCache.setRowCount(row_count + 1)
                self.tableCache.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT techproc FROM processor WHERE exist = True "
                        "ORDER BY techproc ASC")
            for name in cur:
                self.tableTechproc.setRowCount(row_count + 1)
                self.tableTechproc.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT ramfreq FROM processor WHERE exist = True "
                        "ORDER BY ramfreq ASC")
            for name in cur:
                self.tableRamFreq.setRowCount(row_count + 1)
                self.tableRamFreq.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            # Заполнение таблиц кнопками CB
            self.pasteCheckBoxes()

        except (Exception, psycopg2.DatabaseError) as error:
            dialog = DialogOk("Ошибка", error)
            dialog.show()

        finally:
            if conn:
                cur.close()
                conn.close()

    def tb_change_arrows(self, page):
        self.toolBoxProcFilter.setItemIcon(page, QIcon("E:/pcconf/images/up-arrow.png"))
        for i in range(self.toolBoxProcFilter.count()):
            if i != page:
                self.toolBoxProcFilter.setItemIcon(i, QIcon("E:/pcconf/images/down-arrow.png"))

    # Метод для вставки CB в таблицы
    def pasteCheckBoxes(self):
        insert_cb(self.tableProizv)
        insert_cb(self.tableSeries)
        insert_cb(self.tableGraphProc)
        insert_cb(self.tableGaming)
        insert_cb(self.tableSocket)
        insert_cb(self.tableCore)
        insert_cb(self.tableNcores)
        insert_cb(self.tableFreq)
        insert_cb(self.tableCache)
        insert_cb(self.tableTechproc)
        insert_cb(self.tableRamFreq)

    # Метод, обнуляющий все поля
    def resetAll(self):
        reset_sliders(self.sliderPriceMin, self.sliderPriceMax, self.leMinPrice, self.leMaxPrice)
        reset_sliders(self.sliderTdpMin, self.sliderTdpMax, self.leMinTdp, self.leMaxTdp)
        reset_checkboxes(self.tableProizv)
        reset_checkboxes(self.tableSeries)
        reset_checkboxes(self.tableGraphProc)
        reset_checkboxes(self.tableGaming)
        reset_checkboxes(self.tableSocket)
        reset_checkboxes(self.tableCore)
        reset_checkboxes(self.tableNcores)
        reset_checkboxes(self.tableFreq)
        reset_checkboxes(self.tableCache)
        reset_checkboxes(self.tableTechproc)
        reset_checkboxes(self.tableRamFreq)

    # Метод, срабатывающий по нажатии на кнопку и отправляющий в БД запрос на фильтрацию данных
    def click_accept(self, mainWindow):
        query = "SELECT sklad_processor.kol, processor.exist, processor.id, proizv_processor.name, " \
                "fullname, gaming, series, socket, core, ncores, cache, frequency, techproc, ramfreq, " \
                "graphics, tdp, price " \
                "FROM processor, sklad_processor, proizv_processor " \
                "WHERE "

        min_price, max_price = checkFields(self.leMinPrice.text(), self.leMaxPrice.text())
        min_tdp, max_tdp = checkFields(self.leMinTdp.text(), self.leMaxTdp.text())
        if min_price == -1 or min_tdp == -1:  # если не вернулось -1, то выполняем фильтрацию
            pass
        else:
            query1 = get_checkboxes(self.tableProizv, "proizv_processor.name")
            if query1 != "":  # Если есть что добавить к запросу
                query += query1

            if query1 == "":  # Если первая таблица пустая, то добавляем к запросу без AND
                query2 = get_checkboxes(self.tableSeries, "series")
                query += query2
            else:
                query2 = get_checkboxes(self.tableSeries, "series")
                if query2 != "":  # Если есть что добавить к запросу
                    query += " AND " + query2

            if query1 == "" and query2 == "":  # Если первая таблица пустая, то добавляем к запросу без AND
                query3 = get_checkboxes(self.tableGraphProc, "graphics")
                query += query3
            else:
                query3 = get_checkboxes(self.tableGraphProc, "graphics")
                if query3 != "":  # Если есть что добавить к запросу
                    query += " AND " + query3

            if query1 == "" and query2 == "" and query3 == "":
                query4 = get_checkboxes(self.tableGaming, "gaming")
                query += query4
            else:
                query4 = get_checkboxes(self.tableGaming, "gaming")
                if query4 != "":
                    query += " AND " + query4

            if query1 == "" and query2 == "" and query3 == "" and query4 == "":
                query5 = get_checkboxes(self.tableSocket, "socket")
                query += query5
            else:
                query5 = get_checkboxes(self.tableSocket, "socket")
                if query5 != "":
                    query += " AND " + query5

            if query1 == "" and query2 == "" and query3 == "" and query4 == "" and query5 == "":
                query6 = get_checkboxes(self.tableCore, "core")
                query += query6
            else:
                query6 = get_checkboxes(self.tableCore, "core")
                if query6 != "":
                    query += " AND " + query6

            if query1 == "" and query2 == "" and query3 == "" and query4 == "" and query5 == "" and query6 == "":
                query7 = get_checkboxes(self.tableFreq, "frequency")
                query += query7
            else:
                query7 = get_checkboxes(self.tableFreq, "frequency")
                if query7 != "":
                    query += " AND " + query7

            if query1 == "" and query2 == "" and query3 == "" and query4 == "" and query5 == "" and query6 == "" \
                    and query7 == "":
                query8 = get_checkboxes(self.tableCache, "cache")
                query += query8
            else:
                query8 = get_checkboxes(self.tableCache, "cache")
                if query8 != "":
                    query += " AND " + query8

            if query1 == "" and query2 == "" and query3 == "" and query4 == "" and query5 == "" and query6 == "" \
                    and query7 == "" and query8 == "":
                query9 = get_checkboxes(self.tableTechproc, "techproc")
                query += query9
            else:
                query9 = get_checkboxes(self.tableTechproc, "techproc")
                if query9 != "":
                    query += " AND " + query9

            if query1 == "" and query2 == "" and query3 == "" and query4 == "" and query5 == "" and query6 == "" \
                    and query7 == "" and query8 == "" and query9 == "":
                query10 = get_checkboxes(self.tableRamFreq, "ramfreq")
                query += query10
            else:
                query10 = get_checkboxes(self.tableRamFreq, "ramfreq")
                if query10 != "":
                    query += " AND " + query10

            if query1 == "" and query2 == "" and query3 == "" and query4 == "" and query5 == "" and query6 == "" \
                    and query7 == "" and query8 == "" and query9 == "" and query10 == "":
                query11 = get_checkboxes(self.tableNcores, "ncores")
                query += query11
            else:
                query11 = get_checkboxes(self.tableNcores, "ncores")
                if query11 != "":
                    query += " AND " + query11

            # Вероятно, в проверке слайдеров есть лишние if
            if query1 == "" and query2 == "" and query3 == "" and query4 == "" and query5 == "" and query6 == "" \
                    and query7 == "" and query8 == "" and query9 == "" and query10 == "" and query11 == "":  # Если не выбрано ничего в таблицах
                query += check_min_max(min_price, max_price, "Price")
            else:
                if min_price != 0 or max_price != 0:
                    query += " AND " + check_min_max(min_price, max_price, "Price")

            if query1 == "" and query2 == "" and query3 == "" and query4 == "" and query5 == "" and query6 == "" \
                    and query7 == "" and query8 == "" and query9 == "" and query10 == "" and query11 == "" \
                    and (min_price == 0 and max_price == 0):
                query += check_min_max(min_tdp, max_tdp, "Tdp")
            else:
                if min_tdp != 0 or max_tdp != 0:
                    query += " AND " + check_min_max(min_tdp, max_tdp, "Tdp")

            mainWindow.tabWidgetSklad.setCurrentIndex(0)  # Устанавливаем вкладку перед фильтрацией на 0 место

            # Если изменений в фильтрации не было, то передаём changes = False
            if query == "SELECT sklad_processor.kol, processor.exist, processor.id, proizv_processor.name, " \
                        "fullname, gaming, series, socket, core, ncores, cache, frequency, techproc, ramfreq, " \
                        "graphics, tdp, price " \
                        "FROM processor, sklad_processor, proizv_processor " \
                        "WHERE ":

                if self.tab_window == 0:  # Если открыта вкладка "Склад", то применяем фильтры для склада
                    # Переопределяем готовым запросом
                    query = self.make_query_filter(False, mainWindow.rbSklad.isChecked())
                    mainWindow.apply_filter_sklad(query, 1)
                    self.close()
                else:  # Если открыта вкладка "Конфигуратор", то применяем фильтры для конфигуратора
                    query = self.make_query_filter(False, mainWindow.rbConf.isChecked())
                    mainWindow.apply_filter_conf(query, 1)
                    self.close()

            # Если фильтры были выбраны (начальный запрос изменился), то передаём changes = True
            else:
                if self.tab_window == 0:
                    # Дописываем финальную часть запроса (отбор по id, exist и ранжирование) для склада
                    query += self.make_query_filter(True, mainWindow.rbSklad.isChecked())
                    mainWindow.apply_filter_sklad(query, 1)
                    self.close()
                else:
                    # Дописываем финальную часть запроса (отбор по id, exist и ранжирование) для конфигуратора
                    query += self.make_query_filter(True, mainWindow.rbConf.isChecked())
                    mainWindow.apply_filter_conf(query, 1)
                    self.close()

    def make_query_filter(self, changes, having):
        if changes:  # Если есть изменения, то добавляем к запросу связывающие таблицы фильтры
            if having:  # Если отмечен переключатель наличия
                query = "AND processor.id = sklad_processor.id_izd AND processor.id_proizv = proizv_processor.id " \
                        "AND processor.exist = True " \
                        "ORDER BY processor.exist DESC "
                return query
            else:
                query = " AND processor.id = sklad_processor.id_izd AND processor.id_proizv = proizv_processor.id " \
                        " ORDER BY processor.exist DESC"
                return query

        # Если фильтры не выбраны
        else:
            if having:
                query = "SELECT sklad_processor.kol, processor.exist, processor.id, proizv_processor.name, " \
                        "fullname, gaming, series, socket, core, ncores, cache, frequency, techproc, ramfreq, " \
                        "graphics, tdp, price " \
                        "FROM processor, sklad_processor, proizv_processor " \
                        "WHERE processor.id = sklad_processor.id_izd AND processor.id_proizv = proizv_processor.id " \
                        "AND processor.exist = True " \
                        "ORDER BY processor.exist DESC "
                return query
            else:
                query = "SELECT sklad_processor.kol, processor.exist, processor.id, proizv_processor.name, " \
                        "fullname, gaming, series, socket, core, ncores, cache, frequency, techproc, ramfreq, " \
                        "graphics, tdp, price " \
                        "FROM processor, sklad_processor, proizv_processor " \
                        "WHERE processor.id = sklad_processor.id_izd AND processor.id_proizv = proizv_processor.id " \
                        "ORDER BY processor.exist DESC "
                return query


class MotherFilter(QtWidgets.QWidget, widgetMotherFilter.Ui_WidgetMotherFilter):
    def __init__(self, tab, mainWindow):
        super().__init__()
        self.setupUi(self)
        self.mainWindow = mainWindow
        self.tab_window = tab  # Где было создано окно фильтрации - в конфигураторе или на складе
        # -------------Сигналы обновления значений в полях при движении слайдера------------
        self.sliderPriceMin.valueChanged.connect(lambda value: update_field_value(self.leMinPrice, value))
        self.sliderPriceMax.valueChanged.connect(lambda value: update_field_value(self.leMaxPrice, value))
        # -------------Сигналы обновления значений в слайдерах при вводе числа------------
        self.leMinPrice.textChanged.connect(
            lambda value: update_slider_value(self.sliderPriceMin, value, self.leMinPrice))
        self.leMaxPrice.textChanged.connect(
            lambda value: update_slider_value(self.sliderPriceMax, value, self.leMaxPrice))
        # ----------------------------------------------------------------------------------

        # -------------------Задание ограничений для полей ввода-------------------
        only_int = QIntValidator()
        only_int.setRange(0, 999999)

        two_digits_int = QIntValidator()
        two_digits_int.setRange(0, 99)

        three_digits_int = QIntValidator()
        three_digits_int.setRange(0, 999)

        six_digits_int = QIntValidator()
        six_digits_int.setRange(0, 999999)

        self.leMinPrice.setValidator(six_digits_int)
        self.leMaxPrice.setValidator(six_digits_int)
        # -------------------Задание ограничений для полей ввода-------------------

        # -------------------Установка ширины столбцов для таблиц-------------------
        self.tableProizv.setColumnWidth(0, 40)
        self.tableProizv.setColumnWidth(1, 243)
        self.tableProizv.cellClicked.connect(
            lambda row, column, table=self.tableProizv:
            cell_row(row, column, table))

        self.tableSocket.setColumnWidth(0, 40)
        self.tableSocket.setColumnWidth(1, 243)
        self.tableSocket.cellClicked.connect(
            lambda row, column, table=self.tableSocket:
            cell_row(row, column, table))

        self.tableChipset.setColumnWidth(0, 40)
        self.tableChipset.setColumnWidth(1, 243)
        self.tableChipset.cellClicked.connect(
            lambda row, column, table=self.tableChipset:
            cell_row(row, column, table))

        self.tableGaming.setColumnWidth(0, 40)
        self.tableGaming.setColumnWidth(1, 243)
        self.tableGaming.cellClicked.connect(
            lambda row, column, table=self.tableGaming:
            cell_row(row, column, table))

        self.tableSocket.setColumnWidth(0, 40)
        self.tableSocket.setColumnWidth(1, 243)
        self.tableSocket.cellClicked.connect(
            lambda row, column, table=self.tableSocket:
            cell_row(row, column, table))

        self.tableFormFactor.setColumnWidth(0, 40)
        self.tableFormFactor.setColumnWidth(1, 243)
        self.tableFormFactor.cellClicked.connect(
            lambda row, column, table=self.tableFormFactor:
            cell_row(row, column, table))

        self.tablePcie.setColumnWidth(0, 40)
        self.tablePcie.setColumnWidth(1, 243)
        self.tablePcie.cellClicked.connect(
            lambda row, column, table=self.tablePcie:
            cell_row(row, column, table))

        self.tableRamType.setColumnWidth(0, 40)
        self.tableRamType.setColumnWidth(1, 243)
        self.tableRamType.cellClicked.connect(
            lambda row, column, table=self.tableRamType:
            cell_row(row, column, table))

        self.tableRamSlots.setColumnWidth(0, 40)
        self.tableRamSlots.setColumnWidth(1, 243)
        self.tableRamSlots.cellClicked.connect(
            lambda row, column, table=self.tableRamSlots:
            cell_row(row, column, table))

        self.tableRamVolume.setColumnWidth(0, 40)
        self.tableRamVolume.setColumnWidth(1, 243)
        self.tableRamVolume.cellClicked.connect(
            lambda row, column, table=self.tableRamVolume:
            cell_row(row, column, table))

        self.tableRamFreq.setColumnWidth(0, 40)
        self.tableRamFreq.setColumnWidth(1, 243)
        self.tableRamFreq.cellClicked.connect(
            lambda row, column, table=self.tableRamFreq:
            cell_row(row, column, table))

        self.tableSata.setColumnWidth(0, 40)
        self.tableSata.setColumnWidth(1, 243)
        self.tableSata.cellClicked.connect(
            lambda row, column, table=self.tableSata:
            cell_row(row, column, table))

        self.tablePinCool.setColumnWidth(0, 40)
        self.tablePinCool.setColumnWidth(1, 243)
        self.tablePinCool.cellClicked.connect(
            lambda row, column, table=self.tablePinCool:
            cell_row(row, column, table))
        # ------------------------------------------------------------------

        # -----------Соединение кнопок сбосов с методом обнуления-----------
        self.btnResetAll.clicked.connect(self.resetAll)
        self.btnResetPrice.clicked.connect(
            lambda: reset_sliders(self.sliderPriceMin, self.sliderPriceMax, self.leMinPrice, self.leMaxPrice))
        self.btnResetProizv.clicked.connect(lambda: reset_checkboxes(self.tableProizv))
        self.btnResetSocket.clicked.connect(lambda: reset_checkboxes(self.tableSocket))
        self.btnResetChipset.clicked.connect(lambda: reset_checkboxes(self.tableChipset))
        self.btnResetGaming.clicked.connect(lambda: reset_checkboxes(self.tableGaming))
        self.btnResetFormFactor.clicked.connect(lambda: reset_checkboxes(self.tableFormFactor))
        self.btnResetPcie.clicked.connect(lambda: reset_checkboxes(self.tablePcie))
        self.btnResetRamType.clicked.connect(lambda: reset_checkboxes(self.tableRamType))
        self.btnResetRamSlots.clicked.connect(lambda: reset_checkboxes(self.tableRamSlots))
        self.btnResetRamFreq.clicked.connect(lambda: reset_checkboxes(self.tableRamFreq))
        self.btnResetm2.clicked.connect(lambda: reset_checkboxes(self.tablem2))
        self.btnResetSata.clicked.connect(lambda: reset_checkboxes(self.tableSata))
        self.btnResetPinCool.clicked.connect(lambda: reset_checkboxes(self.tablePinCool))
        # -------------------Соединение кнопк сбосов с методом обнуления-------------------

        # Изменение положения стрелки при нажатии на вкладку фильтра
        self.toolBoxMotherFilter.currentChanged.connect(self.tb_change_arrows)

        # Если выбрана вкладка склада или конфигуратора И включён индикатор "Только в наличии"
        if self.tab_window == 0 and mainWindow.rbSklad.isChecked():
            self.load_exists_parameters()
        elif self.tab_window == 0:
            self.load_all_parameters()
        elif self.tab_window == 1 and mainWindow.rbConf.isChecked():
            self.load_exists_parameters()
        elif self.tab_window == 1:
            self.load_all_parameters()

        self.btnAccept.clicked.connect(lambda: self.click_accept(mainWindow))

    def load_all_parameters(self):
        """
            Метод, загружающий параметры всех видеокарт
        """
        self.tableProizv.clear()
        self.tableSocket.clear()
        self.tableChipset.clear()
        self.tableGaming.clear()
        self.tableFormFactor.clear()
        self.tablePcie.clear()
        self.tableRamType.clear()
        self.tableRamSlots.clear()
        self.tableRamVolume.clear()
        self.tableRamFreq.clear()
        self.tablem2.clear()
        self.tableSata.clear()
        self.tablePinCool.clear()

        conn = None
        cur = None
        try:
            conn = psycopg2.connect(database="confPc",
                                    user="postgres",
                                    password="2001",
                                    host="localhost",
                                    port="5432")
            cur = conn.cursor()
            # Задание слайдерам максимального значения из имеющихся в БД данных
            cur.execute(" SELECT price FROM processor ORDER BY price DESC LIMIT 1")
            for name in cur:
                self.sliderPriceMin.setRange(0, int(name[0]))
                self.sliderPriceMax.setRange(0, int(name[0]))
                self.leMaxPrice.setPlaceholderText(f"до {int(name[0])}")

            cur.execute("SELECT DISTINCT name FROM proizv_motherboard, motherboard "
                        "WHERE proizv_motherboard.id = motherboard.id_proizv "
                        "ORDER BY name ASC")
            row_count = 0
            for name in cur:
                self.tableProizv.setRowCount(row_count + 1)
                self.tableProizv.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT socket FROM motherboard "
                        "ORDER BY socket ASC")
            for name in cur:
                self.tableSocket.setRowCount(row_count + 1)
                self.tableSocket.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT chipset FROM motherboard "
                        "ORDER BY chipset ASC")
            for name in cur:
                self.tableChipset.setRowCount(row_count + 1)
                self.tableChipset.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT gaming FROM motherboard "
                        "ORDER BY gaming ASC")
            for name in cur:
                self.tableGaming.setRowCount(row_count + 1)
                self.tableGaming.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT formfactor FROM motherboard "
                        "ORDER BY formfactor ASC")
            for name in cur:
                self.tableFormFactor.setRowCount(row_count + 1)
                self.tableFormFactor.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT pcie FROM motherboard "
                        "ORDER BY pcie ASC")
            for name in cur:
                self.tablePcie.setRowCount(row_count + 1)
                self.tablePcie.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT memorytype FROM motherboard "
                        "ORDER BY memorytype ASC")
            for name in cur:
                self.tableRamType.setRowCount(row_count + 1)
                self.tableRamType.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT memoryslot FROM motherboard "
                        "ORDER BY memoryslot ASC")
            for name in cur:
                self.tableRamSlots.setRowCount(row_count + 1)
                self.tableRamSlots.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT memorymax FROM motherboard "
                        "ORDER BY memorymax ASC")
            for name in cur:
                self.tableRamFreq.setRowCount(row_count + 1)
                self.tableRamFreq.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT m2 FROM motherboard "
                        "ORDER BY m2 ASC")
            for name in cur:
                self.tablem2.setRowCount(row_count + 1)
                self.tablem2.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT sata FROM motherboard "
                        "ORDER BY sata ASC")
            for name in cur:
                self.tableSata.setRowCount(row_count + 1)
                self.tableSata.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT conncool FROM motherboard "
                        "ORDER BY conncool ASC")
            for name in cur:
                self.tablePinCool.setRowCount(row_count + 1)
                self.tablePinCool.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            # Заполнение таблиц кнопками CB
            self.pasteCheckBoxes()

        except (Exception, psycopg2.DatabaseError) as error:
            dialog = DialogOk("Ошибка", error)
            dialog.show()

        finally:
            if conn:
                cur.close()
                conn.close()

    def load_exists_parameters(self):
        """
            Метод, загружающий параметры имеющихся в наличии видеокарт
        """
        self.tableProizv.clear()
        self.tableSocket.clear()
        self.tableChipset.clear()
        self.tableGaming.clear()
        self.tableFormFactor.clear()
        self.tablePcie.clear()
        self.tableRamType.clear()
        self.tableRamSlots.clear()
        self.tableRamVolume.clear()
        self.tableRamFreq.clear()
        self.tablem2.clear()
        self.tableSata.clear()
        self.tablePinCool.clear()

        conn = None
        cur = None
        try:
            conn = psycopg2.connect(database="confPc",
                                    user="postgres",
                                    password="2001",
                                    host="localhost",
                                    port="5432")
            cur = conn.cursor()
            # Задание слайдерам максимального значения из имеющихся в БД данных
            cur.execute(" SELECT price FROM processor WHERE exist = True ORDER BY price DESC LIMIT 1")
            for name in cur:
                self.sliderPriceMin.setRange(0, int(name[0]))
                self.sliderPriceMax.setRange(0, int(name[0]))
                self.leMaxPrice.setPlaceholderText(f"до {int(name[0])}")

            cur.execute("SELECT DISTINCT name FROM proizv_motherboard, motherboard "
                        "WHERE proizv_motherboard.id = motherboard.id_proizv "
                        "AND motherboard.exist = True "
                        "ORDER BY name ASC")
            row_count = 0
            for name in cur:
                self.tableProizv.setRowCount(row_count + 1)
                self.tableProizv.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT socket FROM motherboard "
                        "WHERE exist = True "
                        "ORDER BY socket ASC")
            for name in cur:
                self.tableSocket.setRowCount(row_count + 1)
                self.tableSocket.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT chipset FROM motherboard "
                        "WHERE exist = True "
                        "ORDER BY chipset ASC")
            for name in cur:
                self.tableChipset.setRowCount(row_count + 1)
                self.tableChipset.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT gaming FROM motherboard "
                        "WHERE exist = True "
                        "ORDER BY gaming ASC")
            for name in cur:
                self.tableGaming.setRowCount(row_count + 1)
                self.tableGaming.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT formfactor FROM motherboard "
                        "WHERE exist = True "
                        "ORDER BY formfactor ASC")
            for name in cur:
                self.tableFormFactor.setRowCount(row_count + 1)
                self.tableFormFactor.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT pcie FROM motherboard "
                        "WHERE exist = True "
                        "ORDER BY pcie ASC")
            for name in cur:
                self.tablePcie.setRowCount(row_count + 1)
                self.tablePcie.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT memorytype FROM motherboard "
                        "WHERE exist = True "
                        "ORDER BY memorytype ASC")
            for name in cur:
                self.tableRamType.setRowCount(row_count + 1)
                self.tableRamType.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT memorymax FROM motherboard "
                        "WHERE exist = True "
                        "ORDER BY memorymax ASC")
            for name in cur:
                self.tableRamVolume.setRowCount(row_count + 1)
                self.tableRamVolume.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT memoryslot FROM motherboard "
                        "WHERE exist = True "
                        "ORDER BY memoryslot ASC")
            for name in cur:
                self.tableRamSlots.setRowCount(row_count + 1)
                self.tableRamSlots.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT memoryfreqmax FROM motherboard "
                        "WHERE exist = True "
                        "ORDER BY memoryfreqmax ASC")
            for name in cur:
                self.tableRamFreq.setRowCount(row_count + 1)
                self.tableRamFreq.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT m2 FROM motherboard "
                        "WHERE exist = True "
                        "ORDER BY m2 ASC")
            for name in cur:
                self.tablem2.setRowCount(row_count + 1)
                self.tablem2.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT sata FROM motherboard "
                        "WHERE exist = True "
                        "ORDER BY sata ASC")
            for name in cur:
                self.tableSata.setRowCount(row_count + 1)
                self.tableSata.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT conncool FROM motherboard "
                        "WHERE exist = True "
                        "ORDER BY conncool ASC")
            for name in cur:
                self.tablePinCool.setRowCount(row_count + 1)
                self.tablePinCool.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            # Заполнение таблиц кнопками CB
            self.pasteCheckBoxes()

        except (Exception, psycopg2.DatabaseError) as error:
            dialog = DialogOk("Ошибка", error)
            dialog.show()

        finally:
            if conn:
                cur.close()
                conn.close()

    def tb_change_arrows(self, page):
        self.toolBoxMotherFilter.setItemIcon(page, QIcon("E:/pcconf/images/up-arrow.png"))
        for i in range(self.toolBoxMotherFilter.count()):
            if i != page:
                self.toolBoxMotherFilter.setItemIcon(i, QIcon("E:/pcconf/images/down-arrow.png"))

    # Метод для вставки CB в таблицы
    def pasteCheckBoxes(self):
        insert_cb(self.tableProizv)
        insert_cb(self.tableSocket)
        insert_cb(self.tableChipset)
        insert_cb(self.tableGaming)
        insert_cb(self.tableFormFactor)
        insert_cb(self.tablePcie)
        insert_cb(self.tableRamType)
        insert_cb(self.tableRamVolume)
        insert_cb(self.tableRamSlots)
        insert_cb(self.tableRamFreq)
        insert_cb(self.tablem2)
        insert_cb(self.tableSata)
        insert_cb(self.tablePinCool)

    # Метод, обнуляющий все поля
    def resetAll(self):
        reset_sliders(self.sliderPriceMin, self.sliderPriceMax, self.leMinPrice, self.leMaxPrice)
        reset_checkboxes(self.tableProizv)
        reset_checkboxes(self.tableProizv)
        reset_checkboxes(self.tableSocket)
        reset_checkboxes(self.tableChipset)
        reset_checkboxes(self.tableGaming)
        reset_checkboxes(self.tableFormFactor)
        reset_checkboxes(self.tablePcie)
        reset_checkboxes(self.tableRamType)
        reset_checkboxes(self.tableRamVolume)
        reset_checkboxes(self.tableRamSlots)
        reset_checkboxes(self.tableRamFreq)
        reset_checkboxes(self.tablem2)
        reset_checkboxes(self.tableSata)
        reset_checkboxes(self.tablePinCool)

    # Метод, срабатывающий по нажатии на кнопку и отправляющий в БД запрос на фильтрацию данных
    def click_accept(self, mainWindow):
        query = "SELECT sklad_motherboard.kol, motherboard.exist, motherboard.id, proizv_motherboard.name, " \
                "fullname, gaming, socket, chipset, formfactor, pcie, " \
                "memorytype, memoryslot, memorymax, memoryfreqmax, " \
                "m2, sata, conncool, connproc, kolconnproc, price " \
                "FROM motherboard, sklad_motherboard, proizv_motherboard " \
                "WHERE "

        min_price, max_price = checkFields(self.leMinPrice.text(), self.leMaxPrice.text())
        if min_price == -1:  # если не вернулось -1, то выполняем фильтрацию
            pass
        else:
            query1 = get_checkboxes(self.tableProizv, "proizv_motherboard.name")
            if query1 != "":  # Если есть что добавить к запросу
                query += query1

            if query1 == "":  # Если первая таблица пустая, то добавляем к запросу без AND
                query2 = get_checkboxes(self.tableSocket, "socket")
                query += query2
            else:
                query2 = get_checkboxes(self.tableSocket, "socket")
                if query2 != "":  # Если есть что добавить к запросу
                    query += " AND " + query2

            if query1 == "" and query2 == "":  # Если первая таблица пустая, то добавляем к запросу без AND
                query3 = get_checkboxes(self.tableChipset, "chipset")
                query += query3
            else:
                query3 = get_checkboxes(self.tableChipset, "chipset")
                if query3 != "":  # Если есть что добавить к запросу
                    query += " AND " + query3

            if query1 == "" and query2 == "" and query3 == "":
                query4 = get_checkboxes(self.tableGaming, "gaming")
                query += query4
            else:
                query4 = get_checkboxes(self.tableGaming, "gaming")
                if query4 != "":
                    query += " AND " + query4

            if query1 == "" and query2 == "" and query3 == "" and query4 == "":
                query5 = get_checkboxes(self.tableFormFactor, "formfactor")
                query += query5
            else:
                query5 = get_checkboxes(self.tableFormFactor, "formfactor")
                if query5 != "":
                    query += " AND " + query5

            if query1 == "" and query2 == "" and query3 == "" and query4 == "" and query5 == "":
                query6 = get_checkboxes(self.tablePcie, "pcie")
                query += query6
            else:
                query6 = get_checkboxes(self.tablePcie, "pcie")
                if query6 != "":
                    query += " AND " + query6

            if query1 == "" and query2 == "" and query3 == "" and query4 == "" and query5 == "" and query6 == "":
                query7 = get_checkboxes(self.tableRamType, "memorytype")
                query += query7
            else:
                query7 = get_checkboxes(self.tableRamType, "memorytype")
                if query7 != "":
                    query += " AND " + query7

            if query1 == "" and query2 == "" and query3 == "" and query4 == "" and query5 == "" and query6 == "" \
                    and query7 == "":
                query8 = get_checkboxes(self.tableRamSlots, "memoryslot")
                query += query8
            else:
                query8 = get_checkboxes(self.tableRamSlots, "memoryslot")
                if query8 != "":
                    query += " AND " + query8

            if query1 == "" and query2 == "" and query3 == "" and query4 == "" and query5 == "" and query6 == "" \
                    and query7 == "" and query8 == "":
                query9 = get_checkboxes(self.tableRamVolume, "memorymax")
                query += query9
            else:
                query9 = get_checkboxes(self.tableRamVolume, "memorymax")
                if query9 != "":
                    query += " AND " + query9

            if query1 == "" and query2 == "" and query3 == "" and query4 == "" and query5 == "" and query6 == "" \
                    and query7 == "" and query8 == "" and query9 == "":
                query10 = get_checkboxes(self.tableRamFreq, "memoryfreqmax")
                query += query10
            else:
                query10 = get_checkboxes(self.tableRamFreq, "memoryfreqmax")
                if query10 != "":
                    query += " AND " + query10

            if query1 == "" and query2 == "" and query3 == "" and query4 == "" and query5 == "" and query6 == "" \
                    and query7 == "" and query8 == "" and query9 == "" and query10 == "":
                query11 = get_checkboxes(self.tablem2, "m2")
                query += query11
            else:
                query11 = get_checkboxes(self.tablem2, "m2")
                if query11 != "":
                    query += " AND " + query11

            if query1 == "" and query2 == "" and query3 == "" and query4 == "" and query5 == "" and query6 == "" \
                    and query7 == "" and query8 == "" and query9 == "" and query10 == "" and query11 == "":
                query12 = get_checkboxes(self.tableSata, "sata")
                query += query12
            else:
                query12 = get_checkboxes(self.tableSata, "sata")
                if query12 != "":
                    query += " AND " + query12

            if query1 == "" and query2 == "" and query3 == "" and query4 == "" and query5 == "" and query6 == "" \
                    and query7 == "" and query8 == "" and query9 == "" and query10 == "" and query11 == "" \
                    and query12 == "":
                query13 = get_checkboxes(self.tablePinCool, "conncool")
                query += query13
            else:
                query13 = get_checkboxes(self.tablePinCool, "conncool")
                if query13 != "":
                    query += " AND " + query13

            # Вероятно, в проверке слайдеров есть лишние if
            if query1 == "" and query2 == "" and query3 == "" and query4 == "" and query5 == "" and query6 == "" \
                    and query7 == "" and query8 == "" and query9 == "" and query10 == "" \
                    and query11 == "" and query12 == "" and query13 == "":  # Если не выбрано ничего в таблицах
                query += check_min_max(min_price, max_price, "Price")
            else:
                if min_price != 0 or max_price != 0:
                    query += " AND " + check_min_max(min_price, max_price, "Price")

            mainWindow.tabWidgetSklad.setCurrentIndex(0)  # Устанавливаем вкладку перед фильтрацией на 0 место

            # Если изменений в фильтрации не было, то передаём changes = False
            if query == "SELECT sklad_motherboard.kol, motherboard.exist, motherboard.id, proizv_motherboard.name, " \
                        "fullname, gaming, socket, chipset, formfactor, pcie, " \
                        "memorytype, memoryslot, memorymax, memoryfreqmax, " \
                        "m2, sata, conncool, connproc, kolconnproc, price " \
                        "FROM motherboard, sklad_motherboard, proizv_motherboard " \
                        "WHERE ":

                if self.tab_window == 0:  # Если открыта вкладка "Склад", то применяем фильтры для склада
                    # Переопределяем готовым запросом
                    query = self.make_query_filter(False, mainWindow.rbSklad.isChecked())
                    mainWindow.apply_filter_sklad(query, 2)
                    self.close()
                else:  # Если открыта вкладка "Конфигуратор", то применяем фильтры для конфигуратора
                    query = self.make_query_filter(False, mainWindow.rbConf.isChecked())
                    mainWindow.apply_filter_conf(query, 2)
                    self.close()

            # Если фильтры были выбраны (начальный запрос изменился), то передаём changes = True
            else:
                if self.tab_window == 0:
                    # Дописываем финальную часть запроса (отбор по id, exist и ранжирование) для склада
                    query += self.make_query_filter(True, mainWindow.rbSklad.isChecked())
                    mainWindow.apply_filter_sklad(query, 2)
                    self.close()
                else:
                    # Дописываем финальную часть запроса (отбор по id, exist и ранжирование) для конфигуратора
                    query += self.make_query_filter(True, mainWindow.rbConf.isChecked())
                    mainWindow.apply_filter_conf(query, 2)
                    self.close()

    def make_query_filter(self, changes, having):
        if changes:  # Если есть изменения, то добавляем к запросу связывающие таблицы фильтры
            if having:  # Если отмечен переключатель наличия
                query = "AND motherboard.id = sklad_motherboard.id_izd " \
                        "AND motherboard.id_proizv = proizv_motherboard.id " \
                        "AND motherboard.exist = True " \
                        "ORDER BY motherboard.exist DESC "
                return query
            else:
                query = "AND motherboard.id = sklad_motherboard.id_izd " \
                        "AND motherboard.id_proizv = proizv_motherboard.id " \
                        "ORDER BY motherboard.exist DESC "
                return query

        # Если фильтры не выбраны
        else:
            if having:
                query = "SELECT sklad_motherboard.kol, motherboard.exist, motherboard.id, proizv_motherboard.name, " \
                        "fullname, gaming, socket, chipset, formfactor, pcie, " \
                        "memorytype, memoryslot, memorymax, memoryfreqmax, " \
                        "m2, sata, conncool, connproc, kolconnproc, price " \
                        "FROM motherboard, sklad_motherboard, proizv_motherboard " \
                        "WHERE motherboard.id = sklad_motherboard.id_izd " \
                        "AND motherboard.id_proizv = proizv_motherboard.id " \
                        "AND motherboard.exist = True " \
                        "ORDER BY motherboard.exist DESC "
                return query
            else:
                query = "SELECT sklad_motherboard.kol, motherboard.exist, motherboard.id, proizv_motherboard.name, " \
                        "fullname, gaming, socket, chipset, formfactor, pcie, " \
                        "memorytype, memoryslot, memorymax, memoryfreqmax, " \
                        "m2, sata, conncool, connproc, kolconnproc, price " \
                        "FROM motherboard, sklad_motherboard, proizv_motherboard " \
                        "WHERE motherboard.id = sklad_motherboard.id_izd " \
                        "AND motherboard.id_proizv = proizv_motherboard.id " \
                        "ORDER BY motherboard.exist DESC "
                return query


class CoolFilter(QtWidgets.QWidget, widgetCoolFilter.Ui_WidgetCoolFilter):
    def __init__(self, tab, mainWindow):
        super().__init__()
        self.setupUi(self)
        self.mainWindow = mainWindow
        self.tab_window = tab  # Где было создано окно фильтрации - в конфигураторе или на складе
        # -------------Сигналы обновления значений в полях при движении слайдера------------
        self.sliderPriceMin.valueChanged.connect(lambda value: update_field_value(self.leMinPrice, value))
        self.sliderPriceMax.valueChanged.connect(lambda value: update_field_value(self.leMaxPrice, value))
        self.sliderHeightMin.valueChanged.connect(lambda value: update_field_value(self.leMinHeight, value))
        self.sliderHeightMax.valueChanged.connect(lambda value: update_field_value(self.leMaxHeight, value))
        self.sliderDisperseMin.valueChanged.connect(lambda value: update_field_value(self.leMinDisperse, value))
        self.sliderDisperseMax.valueChanged.connect(lambda value: update_field_value(self.leMaxDisperse, value))
        # -------------Сигналы обновления значений в слайдерах при вводе числа------------
        self.leMinPrice.textChanged.connect(
            lambda value: update_slider_value(self.sliderPriceMin, value, self.leMinPrice))
        self.leMaxPrice.textChanged.connect(
            lambda value: update_slider_value(self.sliderPriceMax, value, self.leMaxPrice))
        self.leMinHeight.textChanged.connect(
            lambda value: update_slider_value(self.sliderHeightMin, value, self.leMinHeight))
        self.leMaxHeight.textChanged.connect(
            lambda value: update_slider_value(self.sliderHeightMax, value, self.leMaxHeight))
        self.leMinDisperse.textChanged.connect(
            lambda value: update_slider_value(self.sliderDisperseMin, value, self.leMinDisperse))
        self.leMaxDisperse.textChanged.connect(
            lambda value: update_slider_value(self.sliderDisperseMax, value, self.leMaxDisperse))
        # ----------------------------------------------------------------------------------

        # -------------------Задание ограничений для полей ввода-------------------
        only_int = QIntValidator()
        only_int.setRange(0, 999999)

        two_digits_int = QIntValidator()
        two_digits_int.setRange(0, 99)

        three_digits_int = QIntValidator()
        three_digits_int.setRange(0, 999)

        six_digits_int = QIntValidator()
        six_digits_int.setRange(0, 999999)

        self.leMinPrice.setValidator(six_digits_int)
        self.leMaxPrice.setValidator(six_digits_int)
        self.leMinHeight.setValidator(two_digits_int)
        self.leMaxHeight.setValidator(two_digits_int)
        self.leMinDisperse.setValidator(three_digits_int)
        self.leMaxDisperse.setValidator(three_digits_int)
        # -------------------Задание ограничений для полей ввода-------------------

        # -------------------Установка ширины столбцов для таблиц-------------------
        self.tableProizv.setColumnWidth(0, 40)
        self.tableProizv.setColumnWidth(1, 243)
        self.tableProizv.cellClicked.connect(
            lambda row, column, table=self.tableProizv:
            cell_row(row, column, table))

        self.tableConstr.setColumnWidth(0, 40)
        self.tableConstr.setColumnWidth(1, 243)
        self.tableConstr.cellClicked.connect(
            lambda row, column, table=self.tableConstr:
            cell_row(row, column, table))

        self.tableSocket.setColumnWidth(0, 40)
        self.tableSocket.setColumnWidth(1, 243)
        self.tableSocket.cellClicked.connect(
            lambda row, column, table=self.tableSocket:
            cell_row(row, column, table))

        self.tableType.setColumnWidth(0, 40)
        self.tableType.setColumnWidth(1, 243)
        self.tableType.cellClicked.connect(
            lambda row, column, table=self.tableType:
            cell_row(row, column, table))

        self.tablePipe.setColumnWidth(0, 40)
        self.tablePipe.setColumnWidth(1, 243)
        self.tablePipe.cellClicked.connect(
            lambda row, column, table=self.tablePipe:
            cell_row(row, column, table))

        self.tablePinCool.setColumnWidth(0, 40)
        self.tablePinCool.setColumnWidth(1, 243)
        self.tablePinCool.cellClicked.connect(
            lambda row, column, table=self.tablePinCool:
            cell_row(row, column, table))

        # ------------------------------------------------------------------

        # -----------Соединение кнопок сбосов с методом обнуления-----------
        self.btnResetAll.clicked.connect(self.resetAll)
        self.btnResetPrice.clicked.connect(
            lambda: reset_sliders(self.sliderPriceMin, self.sliderPriceMax, self.leMinPrice, self.leMaxPrice))
        self.btnResetHeight.clicked.connect(
            lambda: reset_sliders(self.sliderHeightMin, self.sliderHeightMax, self.leMinHeight, self.leMaxHeight))
        self.btnResetDisperse.clicked.connect(
            lambda: reset_sliders(self.sliderDisperseMin, self.sliderDisperseMax, self.leMinDisperse,
                                  self.leMaxDisperse))
        self.btnResetProizv.clicked.connect(lambda: reset_checkboxes(self.tableProizv))
        self.btnResetConstr.clicked.connect(lambda: reset_checkboxes(self.tableConstr))
        self.btnResetSocket.clicked.connect(lambda: reset_checkboxes(self.tableSocket))
        self.btnResetType.clicked.connect(lambda: reset_checkboxes(self.tableType))
        self.btnResetPipe.clicked.connect(lambda: reset_checkboxes(self.tablePipe))
        self.btnResetPinCool.clicked.connect(lambda: reset_checkboxes(self.tablePinCool))
        # -------------------Соединение кнопк сбосов с методом обнуления-------------------

        # Изменение положения стрелки при нажатии на вкладку фильтра
        self.toolBoxCoolFilter.currentChanged.connect(self.tb_change_arrows)

        # Если выбрана вкладка склада или конфигуратора И включён индикатор "Только в наличии"
        if self.tab_window == 0 and mainWindow.rbSklad.isChecked():
            self.load_exists_parameters()
        elif self.tab_window == 0:
            self.load_all_parameters()
        elif self.tab_window == 1 and mainWindow.rbConf.isChecked():
            self.load_exists_parameters()
        elif self.tab_window == 1:
            self.load_all_parameters()

        self.btnAccept.clicked.connect(lambda: self.click_accept(mainWindow))

    def load_all_parameters(self):
        """
            Метод, загружающий параметры всех видеокарт
        """
        self.tableProizv.clear()
        self.tableConstr.clear()
        self.tableSocket.clear()
        self.tableType.clear()
        self.tablePipe.clear()
        self.tablePinCool.clear()

        conn = None
        cur = None
        try:
            conn = psycopg2.connect(database="confPc",
                                    user="postgres",
                                    password="2001",
                                    host="localhost",
                                    port="5432")
            cur = conn.cursor()

            cur.execute(" SELECT price FROM cool ORDER BY price DESC LIMIT 1")
            for name in cur:
                self.sliderPriceMin.setRange(0, int(name[0]))
                self.sliderPriceMax.setRange(0, int(name[0]))
                self.leMaxPrice.setPlaceholderText(f"до {int(name[0])}")

            cur.execute(" SELECT disperse FROM cool ORDER BY disperse DESC LIMIT 1")
            for name in cur:
                self.sliderDisperseMin.setRange(0, int(name[0]))
                self.sliderDisperseMax.setRange(0, int(name[0]))
                self.leMaxDisperse.setPlaceholderText(f"до {int(name[0])}")

            cur.execute(" SELECT height FROM cool ORDER BY height DESC LIMIT 1")
            for name in cur:
                self.sliderHeightMin.setRange(0, int(name[0]))
                self.sliderHeightMax.setRange(0, int(name[0]))
                self.leMaxHeight.setPlaceholderText(f"до {int(name[0])}")

            cur.execute("SELECT DISTINCT name FROM proizv_cool, cool "
                        "WHERE proizv_cool.id = cool.id_proizv "
                        "ORDER BY name ASC")
            row_count = 0
            for name in cur:
                self.tableProizv.setRowCount(row_count + 1)
                self.tableProizv.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT construction FROM cool "
                        "ORDER BY construction ASC")
            for name in cur:
                self.tableConstr.setRowCount(row_count + 1)
                self.tableConstr.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            count = 0  # Счётчик уникальных записей в словаре
            dict_sockets = {}  # словарь, куда будут сохраняться сокеты как ключи (ключи не повторяются)
            cur.execute("SELECT DISTINCT socket FROM cool "
                        "ORDER BY socket ASC")
            for name in cur:
                str_name = str(name)
                # Преобразуем кортеж в строку и удаляем лишние символы, чтобы можно было сделать split списка по ',',
                # а затем записать результаты разбиения кортежа в фильтрующую таблицу
                str_name = re.sub('[^A-Za-z_0-9,+-]', '', str_name)
                str_name = str_name[:-1] + ''  # Удаляем последний символ
                list_name = str_name.split(',')  # Создаём из кортежа список и из списка заполняем таблицы сокетами
                for i in list_name:
                    dict_sockets[i] = count  # Если такой сокет уже есть - он не добавится снова в словарь
                    count += 1
            sockets = sorted(dict_sockets)  # Сортируем словарь (возвращает отсортированный список ключей)
            row_count = 0
            for elem in sockets:
                self.tableSocket.setRowCount(row_count + 1)
                self.tableSocket.setItem(row_count, 1, QtWidgets.QTableWidgetItem(elem))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT type FROM cool "
                        "ORDER BY type ASC")
            for name in cur:
                self.tableType.setRowCount(row_count + 1)
                self.tableType.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT heatpipe FROM cool "
                        "ORDER BY heatpipe ASC")
            for name in cur:
                self.tablePipe.setRowCount(row_count + 1)
                self.tablePipe.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT conncool FROM cool "
                        "ORDER BY conncool ASC")
            for name in cur:
                self.tablePinCool.setRowCount(row_count + 1)
                self.tablePinCool.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            # Заполнение таблиц кнопками CB
            self.pasteCheckBoxes()

        except (Exception, psycopg2.DatabaseError) as error:
            dialog = DialogOk("Ошибка", error)
            dialog.show()

        finally:
            if conn:
                cur.close()
                conn.close()

    def load_exists_parameters(self):
        """
            Метод, загружающий параметры имеющихся в наличии видеокарт
        """
        self.tableProizv.clear()
        self.tableConstr.clear()
        self.tableSocket.clear()
        self.tableType.clear()
        self.tablePipe.clear()
        self.tablePinCool.clear()

        conn = None
        cur = None
        try:
            conn = psycopg2.connect(database="confPc",
                                    user="postgres",
                                    password="2001",
                                    host="localhost",
                                    port="5432")
            cur = conn.cursor()

            cur.execute(" SELECT price FROM cool WHERE exist = TRUE ORDER BY price DESC LIMIT 1")
            for name in cur:
                self.sliderPriceMin.setRange(0, int(name[0]))
                self.sliderPriceMax.setRange(0, int(name[0]))
                self.leMaxPrice.setPlaceholderText(f"до {int(name[0])}")

            cur.execute(" SELECT disperse FROM cool WHERE exist = TRUE ORDER BY disperse DESC LIMIT 1")
            for name in cur:
                self.sliderDisperseMin.setRange(0, int(name[0]))
                self.sliderDisperseMax.setRange(0, int(name[0]))
                self.leMaxDisperse.setPlaceholderText(f"до {int(name[0])}")

            cur.execute(" SELECT height FROM cool WHERE exist = TRUE ORDER BY height DESC LIMIT 1")
            for name in cur:
                self.sliderHeightMin.setRange(0, int(name[0]))
                self.sliderHeightMax.setRange(0, int(name[0]))
                self.leMaxHeight.setPlaceholderText(f"до {int(name[0])}")

            cur.execute("SELECT DISTINCT name FROM proizv_cool, cool "
                        "WHERE proizv_cool.id = cool.id_proizv "
                        "AND cool.exist = True "
                        "ORDER BY name ASC")
            row_count = 0
            for name in cur:
                self.tableProizv.setRowCount(row_count + 1)
                self.tableProizv.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT construction FROM cool "
                        "WHERE exist = True "
                        "ORDER BY construction ASC")
            for name in cur:
                self.tableConstr.setRowCount(row_count + 1)
                self.tableConstr.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT socket FROM cool "
                        "WHERE exist = True "
                        "ORDER BY socket ASC")
            for name in cur:
                self.tableSocket.setRowCount(row_count + 1)
                self.tableSocket.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT type FROM cool "
                        "WHERE exist = True "
                        "ORDER BY type ASC")
            for name in cur:
                self.tableType.setRowCount(row_count + 1)
                self.tableType.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT heatpipe FROM cool "
                        "WHERE exist = True "
                        "ORDER BY heatpipe ASC")
            for name in cur:
                self.tablePipe.setRowCount(row_count + 1)
                self.tablePipe.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT conncool FROM cool "
                        "WHERE exist = True "
                        "ORDER BY conncool ASC")
            for name in cur:
                self.tablePinCool.setRowCount(row_count + 1)
                self.tablePinCool.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            # Заполнение таблиц кнопками CB
            self.pasteCheckBoxes()

        except (Exception, psycopg2.DatabaseError) as error:
            dialog = DialogOk("Ошибка", error)
            dialog.show()

        finally:
            if conn:
                cur.close()
                conn.close()

    def tb_change_arrows(self, page):
        self.toolBoxCoolFilter.setItemIcon(page, QIcon("E:/pcconf/images/up-arrow.png"))
        for i in range(self.toolBoxCoolFilter.count()):
            if i != page:
                self.toolBoxCoolFilter.setItemIcon(i, QIcon("E:/pcconf/images/down-arrow.png"))

    # Метод для вставки CB в таблицы
    def pasteCheckBoxes(self):
        insert_cb(self.tableProizv)
        insert_cb(self.tableConstr)
        insert_cb(self.tableSocket)
        insert_cb(self.tableType)
        insert_cb(self.tablePipe)
        insert_cb(self.tablePinCool)

    # Метод, обнуляющий все поля
    def resetAll(self):
        reset_sliders(self.sliderPriceMin, self.sliderPriceMax, self.leMinPrice, self.leMaxPrice)
        reset_sliders(self.sliderDisperseMin, self.sliderDisperseMax, self.leMinDisperse, self.leMaxDisperse)
        reset_sliders(self.sliderHeightMin, self.sliderHeightMax, self.leMinHeight, self.leMaxHeight)
        reset_checkboxes(self.tableProizv)
        reset_checkboxes(self.tableConstr)
        reset_checkboxes(self.tableSocket)
        reset_checkboxes(self.tableType)
        reset_checkboxes(self.tablePipe)
        reset_checkboxes(self.tablePinCool)

    # Метод, срабатывающий по нажатии на кнопку и отправляющий в БД запрос на фильтрацию данных
    def click_accept(self, mainWindow):
        query = "SELECT sklad_cool.kol, cool.exist, cool.id, proizv_cool.name, " \
                "fullname, construction, type, socket, heatpipe, " \
                "height, disperse, voltage, conncool, price " \
                "FROM cool, sklad_cool, proizv_cool " \
                "WHERE "

        min_price, max_price = checkFields(self.leMinPrice.text(), self.leMaxPrice.text())
        min_disperse, max_disperse = checkFields(self.leMinDisperse.text(), self.leMaxDisperse.text())
        min_height, max_height = checkFields(self.leMinHeight.text(), self.leMaxHeight.text())
        if min_price == -1 or min_disperse == -1 or min_height == -1:  # если не вернулось -1, то выполняем фильтрацию
            pass
        else:
            query1 = get_checkboxes(self.tableProizv, "proizv_cool.name")
            if query1 != "":  # Если есть что добавить к запросу
                query += query1

            if query1 == "":  # Если первая таблица пустая, то добавляем к запросу без AND
                query2 = get_checkboxes(self.tableConstr, "construction")
                query += query2
            else:
                query2 = get_checkboxes(self.tableConstr, "construction")
                if query2 != "":  # Если есть что добавить к запросу
                    query += " AND " + query2

            if query1 == "" and query2 == "":  # Если первая таблица пустая, то добавляем к запросу без AND
                query3 = get_checkboxes_concat(self.tableSocket, "socket")
                query += query3
            else:
                query3 = get_checkboxes_concat(self.tableSocket, "socket")
                if query3 != "":  # Если есть что добавить к запросу
                    query += " AND " + query3

            if query1 == "" and query2 == "" and query3 == "":
                query4 = get_checkboxes(self.tableType, "type")
                query += query4
            else:
                query4 = get_checkboxes(self.tableType, "type")
                if query4 != "":
                    query += " AND " + query4

            if query1 == "" and query2 == "" and query3 == "" and query4 == "":
                query5 = get_checkboxes(self.tablePipe, "pipe")
                query += query5
            else:
                query5 = get_checkboxes(self.tablePipe, "pipe")
                if query5 != "":
                    query += " AND " + query5

            if query1 == "" and query2 == "" and query3 == "" and query4 == "" and query5 == "":
                query6 = get_checkboxes(self.tablePinCool, "conncool")
                query += query6
            else:
                query6 = get_checkboxes(self.tablePinCool, "conncool")
                if query6 != "":
                    query += " AND " + query6

            # Вероятно, в проверке слайдеров есть лишние if
            if query1 == "" and query2 == "" and query3 == "" and query4 == "" and query5 == "" and query6 == "":  # Если не выбрано ничего в таблицах
                query += check_min_max(min_price, max_price, "Price")
            else:
                if min_price != 0 or max_price != 0:
                    query += " AND " + check_min_max(min_price, max_price, "Price")

            if query1 == "" and query2 == "" and query3 == "" and query4 == "" and query5 == "" and query6 == "" \
                    and (min_price == 0 and max_price == 0):
                query += check_min_max(min_disperse, max_disperse, "disperse")
            else:
                if min_disperse != 0 or max_disperse != 0:
                    query += " AND " + check_min_max(min_disperse, max_disperse, "disperse")

            if query1 == "" and query2 == "" and query3 == "" and query4 == "" and query5 == "" and query6 == "" \
                    and (min_price == 0 and max_price == 0) and (min_disperse == 0 and max_disperse == 0):
                query += check_min_max(min_height, max_height, "height")
            else:
                if min_height != 0 or min_height != 0:
                    query += " AND " + check_min_max(min_height, max_height, "height")

            mainWindow.tabWidgetSklad.setCurrentIndex(0)  # Устанавливаем вкладку перед фильтрацией на 0 место

            # Если изменений в фильтрации не было, то передаём changes = False
            if query == "SELECT sklad_cool.kol, cool.exist, cool.id, proizv_cool.name, " \
                        "fullname, construction, type, socket, heatpipe, " \
                        "height, disperse, voltage, conncool, price " \
                        "FROM cool, sklad_cool, proizv_cool " \
                        "WHERE ":

                if self.tab_window == 0:  # Если открыта вкладка "Склад", то применяем фильтры для склада
                    # Переопределяем готовым запросом
                    query = self.make_query_filter(False, mainWindow.rbSklad.isChecked())
                    mainWindow.apply_filter_sklad(query, 3)
                    self.close()
                else:  # Если открыта вкладка "Конфигуратор", то применяем фильтры для конфигуратора
                    query = self.make_query_filter(False, mainWindow.rbConf.isChecked())
                    mainWindow.apply_filter_conf(query, 3)
                    self.close()

            # Если фильтры были выбраны (начальный запрос изменился), то передаём changes = True
            else:
                if self.tab_window == 0:
                    # Дописываем финальную часть запроса (отбор по id, exist и ранжирование) для склада
                    query += self.make_query_filter(True, mainWindow.rbSklad.isChecked())
                    mainWindow.apply_filter_sklad(query, 3)
                    self.close()
                else:
                    # Дописываем финальную часть запроса (отбор по id, exist и ранжирование) для конфигуратора
                    query += self.make_query_filter(True, mainWindow.rbConf.isChecked())
                    mainWindow.apply_filter_conf(query, 3)
                    self.close()

    def make_query_filter(self, changes, having):
        if changes:  # Если есть изменения, то добавляем к запросу связывающие таблицы фильтры
            if having:  # Если отмечен переключатель наличия
                query = " AND cool.id = sklad_cool.id_izd AND cool.id_proizv = proizv_cool.id" \
                        " AND cool.exist = True" \
                        " ORDER BY cool.exist DESC"
                return query
            else:
                query = " AND cool.id = sklad_cool.id_izd AND cool.id_proizv = proizv_cool.id" \
                        " ORDER BY cool.exist DESC"
                return query

        # Если фильтры не выбраны
        else:
            if having:
                query = "SELECT sklad_cool.kol, cool.exist, cool.id, proizv_cool.name, " \
                        "fullname, construction, type, socket, heatpipe, " \
                        "height, disperse, voltage, conncool, price " \
                        "FROM cool, sklad_cool, proizv_cool " \
                        "WHERE cool.id = sklad_cool.id_izd AND cool.id_proizv = proizv_cool.id " \
                        " AND cool.exist = True" \
                        " ORDER BY cool.exist DESC"
                return query
            else:
                query = "SELECT sklad_cool.kol, cool.exist, cool.id, proizv_cool.name, " \
                        "fullname, construction, type, socket, heatpipe, " \
                        "height, disperse, voltage, conncool, price " \
                        "FROM cool, sklad_cool, proizv_cool " \
                        "WHERE cool.id = sklad_cool.id_izd AND cool.id_proizv = proizv_cool.id " \
                        "ORDER BY cool.exist DESC"
                return query


class RamFilter(QtWidgets.QWidget, widgetRamFilter.Ui_WidgetRamFilter):
    def __init__(self, tab, mainWindow):
        super().__init__()
        self.setupUi(self)
        self.mainWindow = mainWindow
        self.tab_window = tab  # Где было создано окно фильтрации - в конфигураторе или на складе
        # -------------Сигналы обновления значений в полях при движении слайдера------------
        self.sliderPriceMin.valueChanged.connect(lambda value: update_field_value(self.leMinPrice, value))
        self.sliderPriceMax.valueChanged.connect(lambda value: update_field_value(self.leMaxPrice, value))
        # -------------Сигналы обновления значений в слайдерах при вводе числа------------
        self.leMinPrice.textChanged.connect(
            lambda value: update_slider_value(self.sliderPriceMin, value, self.leMinPrice))
        self.leMaxPrice.textChanged.connect(
            lambda value: update_slider_value(self.sliderPriceMax, value, self.leMaxPrice))
        # ----------------------------------------------------------------------------------

        # -------------------Задание ограничений для полей ввода-------------------
        only_int = QIntValidator()
        only_int.setRange(0, 999999)

        six_digits_int = QIntValidator()
        six_digits_int.setRange(0, 999999)

        self.leMinPrice.setValidator(six_digits_int)
        self.leMaxPrice.setValidator(six_digits_int)
        # -------------------Задание ограничений для полей ввода-------------------

        # -------------------Установка ширины столбцов для таблиц-------------------
        self.tableProizv.setColumnWidth(0, 40)
        self.tableProizv.setColumnWidth(1, 243)
        self.tableProizv.cellClicked.connect(
            lambda row, column, table=self.tableProizv:
            cell_row(row, column, table))

        self.tableType.setColumnWidth(0, 40)
        self.tableType.setColumnWidth(1, 243)
        self.tableType.cellClicked.connect(
            lambda row, column, table=self.tableType:
            cell_row(row, column, table))

        self.tableGaming.setColumnWidth(0, 40)
        self.tableGaming.setColumnWidth(1, 243)
        self.tableGaming.cellClicked.connect(
            lambda row, column, table=self.tableGaming:
            cell_row(row, column, table))

        self.tableVolume.setColumnWidth(0, 40)
        self.tableVolume.setColumnWidth(1, 243)
        self.tableVolume.cellClicked.connect(
            lambda row, column, table=self.tableVolume:
            cell_row(row, column, table))

        self.tableFreq.setColumnWidth(0, 40)
        self.tableFreq.setColumnWidth(1, 243)
        self.tableFreq.cellClicked.connect(
            lambda row, column, table=self.tableFreq:
            cell_row(row, column, table))

        self.tableModule.setColumnWidth(0, 40)
        self.tableModule.setColumnWidth(1, 243)
        self.tableModule.cellClicked.connect(
            lambda row, column, table=self.tableModule:
            cell_row(row, column, table))

        self.tableLatency.setColumnWidth(0, 40)
        self.tableLatency.setColumnWidth(1, 243)
        self.tableLatency.cellClicked.connect(
            lambda row, column, table=self.tableLatency:
            cell_row(row, column, table))
        # ------------------------------------------------------------------

        # -----------Соединение кнопок сбосов с методом обнуления-----------
        self.btnResetAll.clicked.connect(self.resetAll)
        self.btnResetPrice.clicked.connect(
            lambda: reset_sliders(self.sliderPriceMin, self.sliderPriceMax, self.leMinPrice, self.leMaxPrice))
        self.btnResetProizv.clicked.connect(lambda: reset_checkboxes(self.tableProizv))
        self.btnResetType.clicked.connect(lambda: reset_checkboxes(self.tableType))
        self.btnResetGaming.clicked.connect(lambda: reset_checkboxes(self.tableGaming))
        self.btnResetVolume.clicked.connect(lambda: reset_checkboxes(self.tableVolume))
        self.btnResetFreq.clicked.connect(lambda: reset_checkboxes(self.tableFreq))
        self.btnResetModule.clicked.connect(lambda: reset_checkboxes(self.tableModule))
        self.btnResetLatency.clicked.connect(lambda: reset_checkboxes(self.tableLatency))
        # -------------------Соединение кнопк сбосов с методом обнуления-------------------

        # Изменение положения стрелки при нажатии на вкладку фильтра
        self.toolBoxRamFilter.currentChanged.connect(self.tb_change_arrows)

        # Если выбрана вкладка склада или конфигуратора И включён индикатор "Только в наличии"
        if self.tab_window == 0 and mainWindow.rbSklad.isChecked():
            self.load_exists_parameters()
        elif self.tab_window == 0:
            self.load_all_parameters()
        elif self.tab_window == 1 and mainWindow.rbConf.isChecked():
            self.load_exists_parameters()
        elif self.tab_window == 1:
            self.load_all_parameters()

        self.btnAccept.clicked.connect(lambda: self.click_accept(mainWindow))

    def load_all_parameters(self):
        """
            Метод, загружающий параметры всех видеокарт
        """
        self.tableProizv.clear()
        self.tableType.clear()
        self.tableGaming.clear()
        self.tableVolume.clear()
        self.tableFreq.clear()
        self.tableModule.clear()
        self.tableLatency.clear()

        conn = None
        cur = None
        try:
            conn = psycopg2.connect(database="confPc",
                                    user="postgres",
                                    password="2001",
                                    host="localhost",
                                    port="5432")
            cur = conn.cursor()
            # Задание слайдерам максимального значения из имеющихся в БД данных
            cur.execute(" SELECT price FROM ram ORDER BY price DESC LIMIT 1")
            for name in cur:
                self.sliderPriceMin.setRange(0, int(name[0]))
                self.sliderPriceMax.setRange(0, int(name[0]))
                self.leMaxPrice.setPlaceholderText(f"до {int(name[0])}")

            cur.execute("SELECT DISTINCT name FROM proizv_ram, ram "
                        "WHERE proizv_ram.id = ram.id_proizv "
                        "ORDER BY name ASC")
            row_count = 0
            for name in cur:
                self.tableProizv.setRowCount(row_count + 1)
                self.tableProizv.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT type FROM ram "
                        "ORDER BY type ASC")
            for name in cur:
                self.tableType.setRowCount(row_count + 1)
                self.tableType.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT gaming FROM ram "
                        "ORDER BY gaming ASC")
            for name in cur:
                self.tableGaming.setRowCount(row_count + 1)
                self.tableGaming.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT volume FROM ram "
                        "ORDER BY volume ASC")
            for name in cur:
                self.tableVolume.setRowCount(row_count + 1)
                self.tableVolume.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT frequency FROM ram "
                        "ORDER BY frequency ASC")
            for name in cur:
                self.tableFreq.setRowCount(row_count + 1)
                self.tableFreq.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT complect FROM ram "
                        "ORDER BY complect ASC")
            for name in cur:
                self.tableModule.setRowCount(row_count + 1)
                self.tableModule.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT latency FROM ram "
                        "ORDER BY latency ASC")
            for name in cur:
                self.tableLatency.setRowCount(row_count + 1)
                self.tableLatency.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            # Заполнение таблиц кнопками CB
            self.pasteCheckBoxes()

        except (Exception, psycopg2.DatabaseError) as error:
            dialog = DialogOk("Ошибка", error)
            dialog.show()

        finally:
            if conn:
                cur.close()
                conn.close()

    def load_exists_parameters(self):
        """
            Метод, загружающий параметры имеющихся в наличии видеокарт
        """
        self.tableProizv.clear()
        self.tableType.clear()
        self.tableGaming.clear()
        self.tableVolume.clear()
        self.tableFreq.clear()
        self.tableModule.clear()
        self.tableLatency.clear()

        conn = None
        cur = None
        try:
            conn = psycopg2.connect(database="confPc",
                                    user="postgres",
                                    password="2001",
                                    host="localhost",
                                    port="5432")
            cur = conn.cursor()
            # Задание слайдерам максимального значения из имеющихся в БД данных
            cur.execute(" SELECT price FROM ram WHERE exist = True ORDER BY price DESC LIMIT 1")
            for name in cur:
                self.sliderPriceMin.setRange(0, int(name[0]))
                self.sliderPriceMax.setRange(0, int(name[0]))
                self.leMaxPrice.setPlaceholderText(f"до {int(name[0])}")

            cur.execute("SELECT DISTINCT name FROM proizv_ram, ram "
                        "WHERE proizv_ram.id = ram.id_proizv "
                        "AND ram.exist = True "
                        "ORDER BY name ASC")
            row_count = 0
            for name in cur:
                self.tableProizv.setRowCount(row_count + 1)
                self.tableProizv.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT type FROM ram "
                        "WHERE exist = True "
                        "ORDER BY type ASC")
            for name in cur:
                self.tableType.setRowCount(row_count + 1)
                self.tableType.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT gaming FROM ram "
                        "WHERE exist = True "
                        "ORDER BY gaming ASC")
            for name in cur:
                self.tableGaming.setRowCount(row_count + 1)
                self.tableGaming.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT volume FROM ram "
                        "WHERE exist = True "
                        "ORDER BY volume ASC")
            for name in cur:
                self.tableVolume.setRowCount(row_count + 1)
                self.tableVolume.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT frequency FROM ram "
                        "WHERE exist = True "
                        "ORDER BY frequency ASC")
            for name in cur:
                self.tableFreq.setRowCount(row_count + 1)
                self.tableFreq.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT complect FROM ram "
                        "WHERE exist = True "
                        "ORDER BY complect ASC")
            for name in cur:
                self.tableModule.setRowCount(row_count + 1)
                self.tableModule.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT latency FROM ram "
                        "WHERE exist = True "
                        "ORDER BY latency ASC")
            for name in cur:
                self.tableLatency.setRowCount(row_count + 1)
                self.tableLatency.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            # Заполнение таблиц кнопками CB
            self.pasteCheckBoxes()

        except (Exception, psycopg2.DatabaseError) as error:
            dialog = DialogOk("Ошибка", error)
            dialog.show()

        finally:
            if conn:
                cur.close()
                conn.close()

    def tb_change_arrows(self, page):
        self.toolBoxRamFilter.setItemIcon(page, QIcon("E:/pcconf/images/up-arrow.png"))
        for i in range(self.toolBoxRamFilter.count()):
            if i != page:
                self.toolBoxRamFilter.setItemIcon(i, QIcon("E:/pcconf/images/down-arrow.png"))

    # Метод для вставки CB в таблицы
    def pasteCheckBoxes(self):
        insert_cb(self.tableProizv)
        insert_cb(self.tableType)
        insert_cb(self.tableGaming)
        insert_cb(self.tableVolume)
        insert_cb(self.tableFreq)
        insert_cb(self.tableModule)
        insert_cb(self.tableLatency)

    # Метод, обнуляющий все поля
    def resetAll(self):
        reset_sliders(self.sliderPriceMin, self.sliderPriceMax, self.leMinPrice, self.leMaxPrice)
        reset_checkboxes(self.tableProizv)
        reset_checkboxes(self.tableType)
        reset_checkboxes(self.tableGaming)
        reset_checkboxes(self.tableVolume)
        reset_checkboxes(self.tableFreq)
        reset_checkboxes(self.tableModule)
        reset_checkboxes(self.tableLatency)

    # Метод, срабатывающий по нажатии на кнопку и отправляющий в БД запрос на фильтрацию данных
    def click_accept(self, mainWindow):
        query = "SELECT sklad_ram.kol, ram.exist, ram.id, proizv_ram.name, " \
                "fullname, gaming, type, volume, frequency, " \
                "complect, latency, voltage, price " \
                "FROM ram, sklad_ram, proizv_ram " \
                "WHERE "

        min_price, max_price = checkFields(self.leMinPrice.text(), self.leMaxPrice.text())
        if min_price == -1:  # если не вернулось -1, то выполняем фильтрацию
            pass
        else:
            query1 = get_checkboxes(self.tableProizv, "proizv_ram.name")
            if query1 != "":  # Если есть что добавить к запросу
                query += query1

            if query1 == "":  # Если первая таблица пустая, то добавляем к запросу без AND
                query2 = get_checkboxes(self.tableType, "type")
                query += query2
            else:
                query2 = get_checkboxes(self.tableType, "type")
                if query2 != "":  # Если есть что добавить к запросу
                    query += " AND " + query2

            if query1 == "" and query2 == "":  # Если первая таблица пустая, то добавляем к запросу без AND
                query3 = get_checkboxes(self.tableGaming, "gaming")
                query += query3
            else:
                query3 = get_checkboxes(self.tableGaming, "gaming")
                if query3 != "":  # Если есть что добавить к запросу
                    query += " AND " + query3

            if query1 == "" and query2 == "" and query3 == "":
                query4 = get_checkboxes(self.tableVolume, "volume")
                query += query4
            else:
                query4 = get_checkboxes(self.tableVolume, "volume")
                if query4 != "":
                    query += " AND " + query4

            if query1 == "" and query2 == "" and query3 == "" and query4 == "":
                query5 = get_checkboxes(self.tableFreq, "frequency")
                query += query5
            else:
                query5 = get_checkboxes(self.tableFreq, "frequency")
                if query5 != "":
                    query += " AND " + query5

            if query1 == "" and query2 == "" and query3 == "" and query4 == "" and query5 == "":
                query6 = get_checkboxes(self.tableModule, "complect")
                query += query6
            else:
                query6 = get_checkboxes(self.tableModule, "complect")
                if query6 != "":
                    query += " AND " + query6

            if query1 == "" and query2 == "" and query3 == "" and query4 == "" and query5 == "" and query6 == "":
                query7 = get_checkboxes(self.tableLatency, "latency")
                query += query7
            else:
                query7 = get_checkboxes(self.tableLatency, "latency")
                if query7 != "":
                    query += " AND " + query7

            # Вероятно, в проверке слайдеров есть лишние if
            if query1 == "" and query2 == "" and query3 == "" and query4 == "" and query5 == "" and query6 == "" \
                    and query7 == "":  # Если не выбрано ничего в таблицах
                query += check_min_max(min_price, max_price, "Price")
            else:
                if min_price != 0 or max_price != 0:
                    query += " AND " + check_min_max(min_price, max_price, "Price")

            mainWindow.tabWidgetSklad.setCurrentIndex(0)  # Устанавливаем вкладку перед фильтрацией на 0 место

            # Если изменений в фильтрации не было, то передаём changes = False
            if query == "SELECT sklad_ram.kol, ram.exist, ram.id, proizv_ram.name, " \
                        "fullname, gaming, type, volume, frequency, " \
                        "complect, latency, voltage, price " \
                        "FROM ram, sklad_ram, proizv_ram " \
                        "WHERE ":

                if self.tab_window == 0:  # Если открыта вкладка "Склад", то применяем фильтры для склада
                    # Переопределяем готовым запросом
                    query = self.make_query_filter(False, mainWindow.rbSklad.isChecked())
                    mainWindow.apply_filter_sklad(query, 4)
                    self.close()
                else:  # Если открыта вкладка "Конфигуратор", то применяем фильтры для конфигуратора
                    query = self.make_query_filter(False, mainWindow.rbConf.isChecked())
                    mainWindow.apply_filter_conf(query, 4)
                    self.close()

            # Если фильтры были выбраны (начальный запрос изменился), то передаём changes = True
            else:
                if self.tab_window == 0:
                    # Дописываем финальную часть запроса (отбор по id, exist и ранжирование) для склада
                    query += self.make_query_filter(True, mainWindow.rbSklad.isChecked())
                    mainWindow.apply_filter_sklad(query, 4)
                    self.close()
                else:
                    # Дописываем финальную часть запроса (отбор по id, exist и ранжирование) для конфигуратора
                    query += self.make_query_filter(True, mainWindow.rbConf.isChecked())
                    mainWindow.apply_filter_conf(query, 4)
                    self.close()

    def make_query_filter(self, changes, having):
        if changes:  # Если есть изменения, то добавляем к запросу связывающие таблицы фильтры
            if having:  # Если отмечен переключатель наличия
                query = "AND ram.id = sklad_ram.id_izd " \
                        "AND ram.id_proizv = proizv_ram.id " \
                        "AND ram.exist = True " \
                        "ORDER BY ram.exist DESC "
                return query
            else:
                query = "AND ram.id = sklad_ram.id_izd " \
                        "AND ram.id_proizv = proizv_ram.id " \
                        "ORDER BY ram.exist DESC "
                return query

        # Если фильтры не выбраны
        else:
            if having:
                query = "SELECT sklad_ram.kol, ram.exist, ram.id, proizv_ram.name, " \
                        "fullname, gaming, type, volume, frequency, " \
                        "complect, latency, voltage, price " \
                        "FROM ram, sklad_ram, proizv_ram " \
                        "WHERE ram.id = sklad_ram.id_izd " \
                        "AND ram.id_proizv = proizv_ram.id " \
                        "AND ram.exist = True " \
                        "ORDER BY ram.exist DESC "
                return query
            else:
                query = "SELECT sklad_ram.kol, ram.exist, ram.id, proizv_ram.name, " \
                        "fullname, gaming, type, volume, frequency, " \
                        "complect, latency, voltage, price " \
                        "FROM ram, sklad_ram, proizv_ram " \
                        "WHERE ram.id = sklad_ram.id_izd " \
                        "AND ram.id_proizv = proizv_ram.id " \
                        "ORDER BY ram.exist DESC "
                return query


class DiskFilter(QtWidgets.QWidget, widgetDiskFilter.Ui_WidgetDiskFilter):
    def __init__(self, tab, mainWindow):
        super().__init__()
        self.setupUi(self)
        self.mainWindow = mainWindow
        self.tab_window = tab  # Где было создано окно фильтрации - в конфигураторе или на складе
        # -------------Сигналы обновления значений в полях при движении слайдера------------
        self.sliderPriceMin.valueChanged.connect(lambda value: update_field_value(self.leMinPrice, value))
        self.sliderPriceMax.valueChanged.connect(lambda value: update_field_value(self.leMaxPrice, value))
        self.sliderReadMin.valueChanged.connect(lambda value: update_field_value(self.leMinRead, value))
        self.sliderReadMax.valueChanged.connect(lambda value: update_field_value(self.leMaxRead, value))
        self.sliderWriteMin.valueChanged.connect(lambda value: update_field_value(self.leMinWrite, value))
        self.sliderWriteMax.valueChanged.connect(lambda value: update_field_value(self.leMaxWrite, value))
        # -------------Сигналы обновления значений в слайдерах при вводе числа------------
        self.leMinPrice.textChanged.connect(
            lambda value: update_slider_value(self.sliderPriceMin, value, self.leMinPrice))
        self.leMaxPrice.textChanged.connect(
            lambda value: update_slider_value(self.sliderPriceMax, value, self.leMaxPrice))
        self.leMinRead.textChanged.connect(
            lambda value: update_slider_value(self.sliderReadMin, value, self.leMinRead))
        self.leMaxRead.textChanged.connect(
            lambda value: update_slider_value(self.sliderReadtMax, value, self.leMaxRead))
        self.leMinWrite.textChanged.connect(
            lambda value: update_slider_value(self.sliderWriteMin, value, self.leMinWrite))
        self.leMaxWrite.textChanged.connect(
            lambda value: update_slider_value(self.sliderWriteMax, value, self.leMaxWrite))
        # ----------------------------------------------------------------------------------

        # -------------------Задание ограничений для полей ввода-------------------
        only_int = QIntValidator()
        only_int.setRange(0, 999999)

        five_digits_int = QIntValidator()
        five_digits_int.setRange(0, 9999)

        six_digits_int = QIntValidator()
        six_digits_int.setRange(0, 999999)

        self.leMinPrice.setValidator(six_digits_int)
        self.leMaxPrice.setValidator(six_digits_int)
        self.leMinRead.setValidator(five_digits_int)
        self.leMaxRead.setValidator(five_digits_int)
        self.leMinWrite.setValidator(five_digits_int)
        self.leMaxWrite.setValidator(five_digits_int)
        # -------------------Задание ограничений для полей ввода-------------------

        # -------------------Установка ширины столбцов для таблиц-------------------
        self.tableProizv.setColumnWidth(0, 40)
        self.tableProizv.setColumnWidth(1, 243)
        self.tableProizv.cellClicked.connect(
            lambda row, column, table=self.tableProizv:
            cell_row(row, column, table))

        self.tableType.setColumnWidth(0, 40)
        self.tableType.setColumnWidth(1, 243)
        self.tableType.cellClicked.connect(
            lambda row, column, table=self.tableType:
            cell_row(row, column, table))

        self.tableVolume.setColumnWidth(0, 40)
        self.tableVolume.setColumnWidth(1, 243)
        self.tableVolume.cellClicked.connect(
            lambda row, column, table=self.tableVolume:
            cell_row(row, column, table))

        self.tableRpm.setColumnWidth(0, 40)
        self.tableRpm.setColumnWidth(1, 243)
        self.tableRpm.cellClicked.connect(
            lambda row, column, table=self.tableRpm:
            cell_row(row, column, table))

        # ------------------------------------------------------------------

        # -----------Соединение кнопок сбосов с методом обнуления-----------
        self.btnResetAll.clicked.connect(self.resetAll)
        self.btnResetPrice.clicked.connect(
            lambda: reset_sliders(self.sliderPriceMin, self.sliderPriceMax, self.leMinPrice, self.leMaxPrice))
        self.btnResetRead.clicked.connect(
            lambda: reset_sliders(self.sliderReadMin, self.sliderReadMax, self.leMinRead, self.leMaxRead))
        self.btnResetWrite.clicked.connect(
            lambda: reset_sliders(self.sliderWriteMin, self.sliderWriteMax, self.leMinWrite,
                                  self.leMaxWrite))
        self.btnResetProizv.clicked.connect(lambda: reset_checkboxes(self.tableProizv))
        self.btnResetType.clicked.connect(lambda: reset_checkboxes(self.tableType))
        self.btnResetVolume.clicked.connect(lambda: reset_checkboxes(self.tableVolume))
        self.btnResetRpm.clicked.connect(lambda: reset_checkboxes(self.tableRpm))
        # -------------------Соединение кнопк сбосов с методом обнуления-------------------

        # Изменение положения стрелки при нажатии на вкладку фильтра
        self.toolBoxDiskFilter.currentChanged.connect(self.tb_change_arrows)

        # Если выбрана вкладка склада или конфигуратора И включён индикатор "Только в наличии"
        if self.tab_window == 0 and mainWindow.rbSklad.isChecked():
            self.load_exists_parameters()
        elif self.tab_window == 0:
            self.load_all_parameters()
        elif self.tab_window == 1 and mainWindow.rbConf.isChecked():
            self.load_exists_parameters()
        elif self.tab_window == 1:
            self.load_all_parameters()

        self.btnAccept.clicked.connect(lambda: self.click_accept(mainWindow))

    def load_all_parameters(self):
        """
            Метод, загружающий параметры всех видеокарт
        """
        self.tableProizv.clear()
        self.tableType.clear()
        self.tableVolume.clear()
        self.tableRpm.clear()

        conn = None
        cur = None
        try:
            conn = psycopg2.connect(database="confPc",
                                    user="postgres",
                                    password="2001",
                                    host="localhost",
                                    port="5432")
            cur = conn.cursor()

            cur.execute(" SELECT price FROM disk ORDER BY price DESC LIMIT 1")
            for name in cur:
                self.sliderPriceMin.setRange(0, int(name[0]))
                self.sliderPriceMax.setRange(0, int(name[0]))
                self.leMaxPrice.setPlaceholderText(f"до {int(name[0])}")

            cur.execute(" SELECT read FROM disk ORDER BY read DESC LIMIT 1")
            for name in cur:
                self.sliderReadMin.setRange(0, int(name[0]))
                self.sliderReadMax.setRange(0, int(name[0]))
                self.leMaxRead.setPlaceholderText(f"до {int(name[0])}")

            cur.execute(" SELECT write FROM disk ORDER BY write DESC LIMIT 1")
            for name in cur:
                self.sliderWriteMin.setRange(0, int(name[0]))
                self.sliderWriteMax.setRange(0, int(name[0]))
                self.leMaxWrite.setPlaceholderText(f"до {int(name[0])}")

            cur.execute("SELECT DISTINCT name FROM proizv_disk, disk "
                        "WHERE proizv_disk.id = disk.id_proizv "
                        "ORDER BY name ASC")
            row_count = 0
            for name in cur:
                self.tableProizv.setRowCount(row_count + 1)
                self.tableProizv.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT type FROM disk "
                        "ORDER BY type ASC")
            for name in cur:
                self.tableType.setRowCount(row_count + 1)
                self.tableType.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT volume FROM disk "
                        "ORDER BY volume ASC")
            for name in cur:
                self.tableVolume.setRowCount(row_count + 1)
                self.tableVolume.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT rpm FROM disk "
                        "ORDER BY rpm ASC")
            for name in cur:
                self.tableRpm.setRowCount(row_count + 1)
                self.tableRpm.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            # Заполнение таблиц кнопками CB
            self.pasteCheckBoxes()

        except (Exception, psycopg2.DatabaseError) as error:
            dialog = DialogOk("Ошибка", error)
            dialog.show()

        finally:
            if conn:
                cur.close()
                conn.close()

    def load_exists_parameters(self):
        """
            Метод, загружающий параметры имеющихся в наличии видеокарт
        """
        self.tableProizv.clear()
        self.tableType.clear()
        self.tableVolume.clear()
        self.tableRpm.clear()

        conn = None
        cur = None
        try:
            conn = psycopg2.connect(database="confPc",
                                    user="postgres",
                                    password="2001",
                                    host="localhost",
                                    port="5432")
            cur = conn.cursor()

            cur.execute(" SELECT price FROM disk WHERE exist = True ORDER BY price DESC LIMIT 1")
            for name in cur:
                self.sliderPriceMin.setRange(0, int(name[0]))
                self.sliderPriceMax.setRange(0, int(name[0]))
                self.leMaxPrice.setPlaceholderText(f"до {int(name[0])}")

            cur.execute(" SELECT read FROM disk WHERE exist = True ORDER BY read DESC LIMIT 1")
            for name in cur:
                self.sliderReadMin.setRange(0, int(name[0]))
                self.sliderReadMax.setRange(0, int(name[0]))
                self.leMaxRead.setPlaceholderText(f"до {int(name[0])}")

            cur.execute(" SELECT write FROM disk WHERE exist = True ORDER BY write DESC LIMIT 1")
            for name in cur:
                self.sliderWriteMin.setRange(0, int(name[0]))
                self.sliderWriteMax.setRange(0, int(name[0]))
                self.leMaxWrite.setPlaceholderText(f"до {int(name[0])}")

            cur.execute("SELECT DISTINCT name FROM proizv_disk, disk "
                        "WHERE proizv_disk.id = disk.id_proizv "
                        "AND disk.exist = True "
                        "ORDER BY name ASC")
            row_count = 0
            for name in cur:
                self.tableProizv.setRowCount(row_count + 1)
                self.tableProizv.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT type FROM disk "
                        "WHERE exist = True "
                        "ORDER BY type ASC")
            for name in cur:
                self.tableType.setRowCount(row_count + 1)
                self.tableType.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT volume FROM disk "
                        "WHERE exist = True "
                        "ORDER BY volume ASC")
            for name in cur:
                self.tableVolume.setRowCount(row_count + 1)
                self.tableVolume.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT rpm FROM disk "
                        "WHERE exist = True "
                        "ORDER BY rpm ASC")
            for name in cur:
                self.tableRpm.setRowCount(row_count + 1)
                self.tableRpm.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            # Заполнение таблиц кнопками CB
            self.pasteCheckBoxes()

        except (Exception, psycopg2.DatabaseError) as error:
            dialog = DialogOk("Ошибка", error)
            dialog.show()

        finally:
            if conn:
                cur.close()
                conn.close()

    def tb_change_arrows(self, page):
        self.toolBoxDiskFilter.setItemIcon(page, QIcon("E:/pcconf/images/up-arrow.png"))
        for i in range(self.toolBoxDiskFilter.count()):
            if i != page:
                self.toolBoxDiskFilter.setItemIcon(i, QIcon("E:/pcconf/images/down-arrow.png"))

    # Метод для вставки CB в таблицы
    def pasteCheckBoxes(self):
        insert_cb(self.tableProizv)
        insert_cb(self.tableType)
        insert_cb(self.tableVolume)
        insert_cb(self.tableRpm)

    # Метод, обнуляющий все поля
    def resetAll(self):
        reset_sliders(self.sliderPriceMin, self.sliderPriceMax, self.leMinPrice, self.leMaxPrice)
        reset_sliders(self.sliderReadMin, self.sliderReadMax, self.leMinRead, self.leMaxRead)
        reset_sliders(self.sliderWriteMin, self.sliderWriteMax, self.leMinWrite, self.leMaxWrite)
        reset_checkboxes(self.tableProizv)
        reset_checkboxes(self.tableType)
        reset_checkboxes(self.tableVolume)
        reset_checkboxes(self.tableRpm)

    # Метод, срабатывающий по нажатии на кнопку и отправляющий в БД запрос на фильтрацию данных
    def click_accept(self, mainWindow):
        query = "SELECT sklad_disk.kol, disk.exist, disk.id, proizv_disk.name, " \
                "fullname, type, volume, connect, read, write, rpm, price " \
                "FROM disk, sklad_disk, proizv_disk " \
                "WHERE "

        min_price, max_price = checkFields(self.leMinPrice.text(), self.leMaxPrice.text())
        min_read, max_read = checkFields(self.leMinRead.text(), self.leMaxRead.text())
        min_write, max_write = checkFields(self.leMinWrite.text(), self.leMaxWrite.text())
        if min_price == -1 or min_read == -1 or min_write == -1:  # если не вернулось -1, то выполняем фильтрацию
            pass
        else:
            query1 = get_checkboxes(self.tableProizv, "proizv_disk.name")
            if query1 != "":  # Если есть что добавить к запросу
                query += query1

            if query1 == "":  # Если первая таблица пустая, то добавляем к запросу без AND
                query2 = get_checkboxes(self.tableType, "type")
                query += query2
            else:
                query2 = get_checkboxes(self.tableType, "type")
                if query2 != "":  # Если есть что добавить к запросу
                    query += " AND " + query2

            if query1 == "" and query2 == "":  # Если первая таблица пустая, то добавляем к запросу без AND
                query3 = get_checkboxes(self.tableVolume, "volume")
                query += query3
            else:
                query3 = get_checkboxes(self.tableVolume, "volume")
                if query3 != "":  # Если есть что добавить к запросу
                    query += " AND " + query3

            if query1 == "" and query2 == "" and query3 == "":
                query4 = get_checkboxes(self.tableRpm, "rpm")
                query += query4
            else:
                query4 = get_checkboxes(self.tableRpm, "rpm")
                if query4 != "":
                    query += " AND " + query4

            # Вероятно, в проверке слайдеров есть лишние if
            if query1 == "" and query2 == "" and query3 == "" and query4 == "":  # Если не выбрано ничего в таблицах
                query += check_min_max(min_price, max_price, "Price")
            else:
                if min_price != 0 or max_price != 0:
                    query += " AND " + check_min_max(min_price, max_price, "Price")

            if query1 == "" and query2 == "" and query3 == "" and query4 == "" \
                    and (min_price == 0 and max_price == 0):
                query += check_min_max(min_read, max_read, "read")
            else:
                if min_read != 0 or max_read != 0:
                    query += " AND " + check_min_max(min_read, max_read, "read")

            if query1 == "" and query2 == "" and query3 == "" and query4 == "" \
                    and (min_price == 0 and max_price == 0) and (min_read == 0 and max_read == 0):
                query += check_min_max(min_write, max_write, "write")
            else:
                if min_write != 0 or max_write != 0:
                    query += " AND " + check_min_max(min_write, max_write, "write")

            mainWindow.tabWidgetSklad.setCurrentIndex(0)  # Устанавливаем вкладку перед фильтрацией на 0 место

            # Если изменений в фильтрации не было, то передаём changes = False
            if query == "SELECT sklad_disk.kol, disk.exist, disk.id, proizv_disk.name, " \
                        "fullname, type, volume, connect, read, write, rpm, price " \
                        "FROM disk, sklad_disk, proizv_disk " \
                        "WHERE ":

                if self.tab_window == 0:  # Если открыта вкладка "Склад", то применяем фильтры для склада
                    # Переопределяем готовым запросом
                    query = self.make_query_filter(False, mainWindow.rbSklad.isChecked())
                    mainWindow.apply_filter_sklad(query, 5)
                    self.close()
                else:  # Если открыта вкладка "Конфигуратор", то применяем фильтры для конфигуратора
                    query = self.make_query_filter(False, mainWindow.rbConf.isChecked())
                    mainWindow.apply_filter_conf(query, 5)
                    self.close()

            # Если фильтры были выбраны (начальный запрос изменился), то передаём changes = True
            else:
                if self.tab_window == 0:
                    # Дописываем финальную часть запроса (отбор по id, exist и ранжирование) для склада
                    query += self.make_query_filter(True, mainWindow.rbSklad.isChecked())
                    mainWindow.apply_filter_sklad(query, 5)
                    self.close()
                else:
                    # Дописываем финальную часть запроса (отбор по id, exist и ранжирование) для конфигуратора
                    query += self.make_query_filter(True, mainWindow.rbConf.isChecked())
                    mainWindow.apply_filter_conf(query, 5)
                    self.close()

    def make_query_filter(self, changes, having):
        if changes:  # Если есть изменения, то добавляем к запросу связывающие таблицы фильтры
            if having:  # Если отмечен переключатель наличия
                query = " AND disk.id = sklad_disk.id_izd AND disk.id_proizv = proizv_disk.id " \
                        " AND disk.exist = True " \
                        " ORDER BY disk.exist DESC"
                return query
            else:
                query = " AND disk.id = sklad_disk.id_izd AND disk.id_proizv = proizv_disk.id " \
                        " ORDER BY disk.exist DESC"
                return query

        # Если фильтры не выбраны
        else:
            if having:
                query = "SELECT sklad_disk.kol, disk.exist, disk.id, proizv_disk.name, " \
                        "fullname, type, volume, connect, read, write, rpm, price " \
                        "FROM disk, sklad_disk, proizv_disk " \
                        "WHERE disk.id = sklad_disk.id_izd AND disk.id_proizv = proizv_disk.id " \
                        "AND disk.exist = True " \
                        "ORDER BY disk.exist DESC"
                return query
            else:
                query = "SELECT sklad_disk.kol, disk.exist, disk.id, proizv_disk.name, " \
                        "fullname, type, volume, connect, read, write, rpm, price " \
                        "FROM disk, sklad_disk, proizv_disk " \
                        "WHERE disk.id = sklad_disk.id_izd AND disk.id_proizv = proizv_disk.id " \
                        "ORDER BY disk.exist DESC"
                return query


class PowerFilter(QtWidgets.QWidget, widgetPowerFilter.Ui_WidgetPowerFilter):
    def __init__(self, tab, mainWindow):
        super().__init__()
        self.setupUi(self)
        self.mainWindow = mainWindow
        self.tab_window = tab  # Где было создано окно фильтрации - в конфигураторе или на складе
        # -------------Сигналы обновления значений в полях при движении слайдера------------
        self.sliderPriceMin.valueChanged.connect(lambda value: update_field_value(self.leMinPrice, value))
        self.sliderPriceMax.valueChanged.connect(lambda value: update_field_value(self.leMaxPrice, value))
        self.sliderPowerMin.valueChanged.connect(lambda value: update_field_value(self.leMinPower, value))
        self.sliderPowerMax.valueChanged.connect(lambda value: update_field_value(self.leMaxPower, value))
        self.sliderLenMin.valueChanged.connect(lambda value: update_field_value(self.leMinLen, value))
        self.sliderLenMax.valueChanged.connect(lambda value: update_field_value(self.leMaxLen, value))
        # -------------Сигналы обновления значений в слайдерах при вводе числа------------
        self.leMinPrice.textChanged.connect(
            lambda value: update_slider_value(self.sliderPriceMin, value, self.leMinPrice))
        self.leMaxPrice.textChanged.connect(
            lambda value: update_slider_value(self.sliderPriceMax, value, self.leMaxPrice))
        self.leMinPower.textChanged.connect(
            lambda value: update_slider_value(self.sliderPowerMin, value, self.leMinPower))
        self.leMaxPower.textChanged.connect(
            lambda value: update_slider_value(self.sliderPowerMax, value, self.leMaxPower))
        self.leMinLen.textChanged.connect(
            lambda value: update_slider_value(self.sliderLenMin, value, self.leMinLen))
        self.leMaxLen.textChanged.connect(
            lambda value: update_slider_value(self.sliderLenMax, value, self.leMaxLen))
        # ----------------------------------------------------------------------------------

        # -------------------Задание ограничений для полей ввода-------------------
        only_int = QIntValidator()
        only_int.setRange(0, 999999)
        three_digits_int = QIntValidator()
        three_digits_int.setRange(0, 999)

        four_digits_int = QIntValidator()
        four_digits_int.setRange(0, 9999)

        six_digits_int = QIntValidator()
        six_digits_int.setRange(0, 999999)

        self.leMinPrice.setValidator(six_digits_int)
        self.leMaxPrice.setValidator(six_digits_int)
        self.leMinPower.setValidator(four_digits_int)
        self.leMaxPower.setValidator(four_digits_int)
        self.leMinLen.setValidator(three_digits_int)
        self.leMaxLen.setValidator(three_digits_int)
        # -------------------Задание ограничений для полей ввода-------------------

        # -------------------Установка ширины столбцов для таблиц-------------------
        self.tableProizv.setColumnWidth(0, 40)
        self.tableProizv.setColumnWidth(1, 243)
        self.tableProizv.cellClicked.connect(
            lambda row, column, table=self.tableProizv:
            cell_row(row, column, table))

        self.tableFormFactor.setColumnWidth(0, 40)
        self.tableFormFactor.setColumnWidth(1, 243)
        self.tableFormFactor.cellClicked.connect(
            lambda row, column, table=self.tableFormFactor:
            cell_row(row, column, table))

        self.tableCert.setColumnWidth(0, 40)
        self.tableCert.setColumnWidth(1, 243)
        self.tableCert.cellClicked.connect(
            lambda row, column, table=self.tableCert:
            cell_row(row, column, table))

        self.tablePinmain.setColumnWidth(0, 40)
        self.tablePinmain.setColumnWidth(1, 243)
        self.tablePinmain.cellClicked.connect(
            lambda row, column, table=self.tablePinmain:
            cell_row(row, column, table))

        # ------------------------------------------------------------------

        # -----------Соединение кнопок сбосов с методом обнуления-----------
        self.btnResetAll.clicked.connect(self.resetAll)
        self.btnResetPrice.clicked.connect(
            lambda: reset_sliders(self.sliderPriceMin, self.sliderPriceMax, self.leMinPrice, self.leMaxPrice))
        self.btnResetPower.clicked.connect(
            lambda: reset_sliders(self.sliderPowerMin, self.sliderPowerMax, self.leMinPower, self.leMaxPower))
        self.btnResetLen.clicked.connect(
            lambda: reset_sliders(self.sliderLenMin, self.sliderLenMax, self.leMinLen,
                                  self.leMaxLen))
        self.btnResetProizv.clicked.connect(lambda: reset_checkboxes(self.tableProizv))
        self.btnResetFormFactor.clicked.connect(lambda: reset_checkboxes(self.tableFormFactor))
        self.btnResetCert.clicked.connect(lambda: reset_checkboxes(self.tableCert))
        self.btnResetPinmain.clicked.connect(lambda: reset_checkboxes(self.tablePinmain))
        # -------------------Соединение кнопк сбосов с методом обнуления-------------------

        # Изменение положения стрелки при нажатии на вкладку фильтра
        self.toolBoxPowerFilter.currentChanged.connect(self.tb_change_arrows)

        # Если выбрана вкладка склада или конфигуратора И включён индикатор "Только в наличии"
        if self.tab_window == 0 and mainWindow.rbSklad.isChecked():
            self.load_exists_parameters()
        elif self.tab_window == 0:
            self.load_all_parameters()
        elif self.tab_window == 1 and mainWindow.rbConf.isChecked():
            self.load_exists_parameters()
        elif self.tab_window == 1:
            self.load_all_parameters()

        self.btnAccept.clicked.connect(lambda: self.click_accept(mainWindow))

    def load_all_parameters(self):
        """
            Метод, загружающий параметры всех видеокарт
        """
        self.tableProizv.clear()
        self.tableFormFactor.clear()
        self.tableCert.clear()
        self.tablePinmain.clear()

        conn = None
        cur = None
        try:
            conn = psycopg2.connect(database="confPc",
                                    user="postgres",
                                    password="2001",
                                    host="localhost",
                                    port="5432")
            cur = conn.cursor()

            cur.execute(" SELECT price FROM power ORDER BY price DESC LIMIT 1")
            for name in cur:
                self.sliderPriceMin.setRange(0, int(name[0]))
                self.sliderPriceMax.setRange(0, int(name[0]))
                self.leMaxPrice.setPlaceholderText(f"до {int(name[0])}")

            cur.execute(" SELECT power.power FROM power ORDER BY power DESC LIMIT 1")
            for name in cur:
                self.sliderPowerMin.setRange(0, int(name[0]))
                self.sliderPowerMax.setRange(0, int(name[0]))
                self.leMaxPower.setPlaceholderText(f"до {int(name[0])}")

            cur.execute(" SELECT length FROM power ORDER BY length DESC LIMIT 1")
            for name in cur:
                self.sliderLenMin.setRange(0, int(name[0]))
                self.sliderLenMax.setRange(0, int(name[0]))
                self.leMaxLen.setPlaceholderText(f"до {int(name[0])}")

            cur.execute("SELECT DISTINCT name FROM proizv_power, power "
                        "WHERE proizv_power.id = power.id_proizv "
                        "ORDER BY name ASC")
            row_count = 0
            for name in cur:
                self.tableProizv.setRowCount(row_count + 1)
                self.tableProizv.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT formfactor FROM power "
                        "ORDER BY formfactor ASC")
            for name in cur:
                self.tableFormFactor.setRowCount(row_count + 1)
                self.tableFormFactor.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT certificate FROM power "
                        "ORDER BY certificate ASC")
            for name in cur:
                self.tableCert.setRowCount(row_count + 1)
                self.tableCert.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT pinmain FROM power "
                        "ORDER BY pinmain ASC")
            for name in cur:
                self.tablePinmain.setRowCount(row_count + 1)
                self.tablePinmain.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            # Заполнение таблиц кнопками CB
            self.pasteCheckBoxes()

        except (Exception, psycopg2.DatabaseError) as error:
            dialog = DialogOk("Ошибка", error)
            dialog.show()

        finally:
            if conn:
                cur.close()
                conn.close()

    def load_exists_parameters(self):
        """
            Метод, загружающий параметры имеющихся в наличии видеокарт
        """
        self.tableProizv.clear()
        self.tableFormFactor.clear()
        self.tableCert.clear()
        self.tablePinmain.clear()

        conn = None
        cur = None
        try:
            conn = psycopg2.connect(database="confPc",
                                    user="postgres",
                                    password="2001",
                                    host="localhost",
                                    port="5432")
            cur = conn.cursor()

            cur.execute(" SELECT price FROM power WHERE exist = True ORDER BY price DESC LIMIT 1")
            for name in cur:
                self.sliderPriceMin.setRange(0, int(name[0]))
                self.sliderPriceMax.setRange(0, int(name[0]))
                self.leMaxPrice.setPlaceholderText(f"до {int(name[0])}")

            cur.execute(" SELECT power.power FROM power WHERE exist = True ORDER BY power DESC LIMIT 1")
            for name in cur:
                self.sliderPowerMin.setRange(0, int(name[0]))
                self.sliderPowerMax.setRange(0, int(name[0]))
                self.leMaxPower.setPlaceholderText(f"до {int(name[0])}")

            cur.execute(" SELECT length FROM power WHERE exist = True ORDER BY length DESC LIMIT 1")
            for name in cur:
                self.sliderLenMin.setRange(0, int(name[0]))
                self.sliderLenMax.setRange(0, int(name[0]))
                self.leMaxLen.setPlaceholderText(f"до {int(name[0])}")

            cur.execute("SELECT DISTINCT name FROM proizv_power, power "
                        "WHERE proizv_power.id = power.id_proizv "
                        "AND power.exist = True "
                        "ORDER BY name ASC")
            row_count = 0
            for name in cur:
                self.tableProizv.setRowCount(row_count + 1)
                self.tableProizv.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT formfactor FROM power "
                        "WHERE exist = True "
                        "ORDER BY formfactor ASC")
            for name in cur:
                self.tableFormFactor.setRowCount(row_count + 1)
                self.tableFormFactor.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT certificate FROM power "
                        "WHERE exist = True "
                        "ORDER BY certificate ASC")
            for name in cur:
                self.tableCert.setRowCount(row_count + 1)
                self.tableCert.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT pinmain FROM power "
                        "WHERE exist = True "
                        "ORDER BY pinmain ASC")
            for name in cur:
                self.tablePinmain.setRowCount(row_count + 1)
                self.tablePinmain.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            # Заполнение таблиц кнопками CB
            self.pasteCheckBoxes()

        except (Exception, psycopg2.DatabaseError) as error:
            dialog = DialogOk("Ошибка", error)
            dialog.show()

        finally:
            if conn:
                cur.close()
                conn.close()

    def tb_change_arrows(self, page):
        self.toolBoxPowerFilter.setItemIcon(page, QIcon("E:/pcconf/images/up-arrow.png"))
        for i in range(self.toolBoxPowerFilter.count()):
            if i != page:
                self.toolBoxPowerFilter.setItemIcon(i, QIcon("E:/pcconf/images/down-arrow.png"))

    # Метод для вставки CB в таблицы
    def pasteCheckBoxes(self):
        insert_cb(self.tableProizv)
        insert_cb(self.tableFormFactor)
        insert_cb(self.tableCert)
        insert_cb(self.tablePinmain)

    # Метод, обнуляющий все поля
    def resetAll(self):
        reset_sliders(self.sliderPriceMin, self.sliderPriceMax, self.leMinPrice, self.leMaxPrice)
        reset_sliders(self.sliderPowerMin, self.sliderPowerMax, self.leMinPower, self.leMaxPower)
        reset_sliders(self.sliderLenMin, self.sliderLenMax, self.leMinLen, self.leMaxLen)
        reset_checkboxes(self.tableProizv)
        reset_checkboxes(self.tableFormFactor)
        reset_checkboxes(self.tableCert)
        reset_checkboxes(self.tablePinmain)

    # Метод, срабатывающий по нажатии на кнопку и отправляющий в БД запрос на фильтрацию данных
    def click_accept(self, mainWindow):
        query = "SELECT sklad_power.kol, power.exist, power.id, proizv_power.name, " \
                "fullname, formfactor, length, power, certificate, pinmain, " \
                "pinsata, connproc, kolconnproc, connvideo, kolconnvideo, price " \
                "FROM power, sklad_power, proizv_power " \
                "WHERE "

        min_price, max_price = checkFields(self.leMinPrice.text(), self.leMaxPrice.text())
        min_power, max_power = checkFields(self.leMinPower.text(), self.leMaxPower.text())
        min_len, max_len = checkFields(self.leMinLen.text(), self.leMaxLen.text())
        if min_price == -1 or min_power == -1 or min_len == -1:  # если не вернулось -1, то выполняем фильтрацию
            pass
        else:
            query1 = get_checkboxes(self.tableProizv, "proizv_power.name")
            if query1 != "":  # Если есть что добавить к запросу
                query += query1

            if query1 == "":  # Если первая таблица пустая, то добавляем к запросу без AND
                query2 = get_checkboxes(self.tableFormFactor, "formfactor")
                query += query2
            else:
                query2 = get_checkboxes(self.tableFormFactor, "formfactor")
                if query2 != "":  # Если есть что добавить к запросу
                    query += " AND " + query2

            if query1 == "" and query2 == "":  # Если первая таблица пустая, то добавляем к запросу без AND
                query3 = get_checkboxes(self.tableCert, "certificate")
                query += query3
            else:
                query3 = get_checkboxes(self.tableCert, "certificate")
                if query3 != "":  # Если есть что добавить к запросу
                    query += " AND " + query3

            if query1 == "" and query2 == "" and query3 == "":
                query4 = get_checkboxes(self.tablePinmain, "pinmain")
                query += query4
            else:
                query4 = get_checkboxes(self.tablePinmain, "pinmain")
                if query4 != "":
                    query += " AND " + query4

            # Вероятно, в проверке слайдеров есть лишние if
            if query1 == "" and query2 == "" and query3 == "" and query4 == "":  # Если не выбрано ничего в таблицах
                query += check_min_max(min_price, max_price, "Price")
            else:
                if min_price != 0 or max_price != 0:
                    query += " AND " + check_min_max(min_price, max_price, "Price")

            if query1 == "" and query2 == "" and query3 == "" and query4 == "" \
                    and (min_price == 0 and max_price == 0):
                query += check_min_max(min_power, max_power, "power")
            else:
                if min_power != 0 or max_power != 0:
                    query += " AND " + check_min_max(min_power, max_power, "power")

            if query1 == "" and query2 == "" and query3 == "" and query4 == "" \
                    and (min_price == 0 and max_price == 0) and (min_power == 0 and max_power == 0):
                query += check_min_max(min_len, max_len, "length")
            else:
                if min_len != 0 or max_len != 0:
                    query += " AND " + check_min_max(min_len, max_len, "length")

            mainWindow.tabWidgetSklad.setCurrentIndex(0)  # Устанавливаем вкладку перед фильтрацией на 0 место

            # Если изменений в фильтрации не было, то передаём changes = False
            if query == "SELECT sklad_power.kol, power.exist, power.id, proizv_power.name, " \
                        "fullname, formfactor, length, power, certificate, pinmain, " \
                        "pinsata, connproc, kolconnproc, connvideo, kolconnvideo, price " \
                        "FROM power, sklad_power, proizv_power " \
                        "WHERE ":

                if self.tab_window == 0:  # Если открыта вкладка "Склад", то применяем фильтры для склада
                    # Переопределяем готовым запросом
                    query = self.make_query_filter(False, mainWindow.rbSklad.isChecked())
                    mainWindow.apply_filter_sklad(query, 6)
                    self.close()
                else:  # Если открыта вкладка "Конфигуратор", то применяем фильтры для конфигуратора
                    query = self.make_query_filter(False, mainWindow.rbConf.isChecked())
                    mainWindow.apply_filter_conf(query, 6)
                    self.close()

            # Если фильтры были выбраны (начальный запрос изменился), то передаём changes = True
            else:
                if self.tab_window == 0:
                    # Дописываем финальную часть запроса (отбор по id, exist и ранжирование) для склада
                    query += self.make_query_filter(True, mainWindow.rbSklad.isChecked())
                    mainWindow.apply_filter_sklad(query, 6)
                    self.close()
                else:
                    # Дописываем финальную часть запроса (отбор по id, exist и ранжирование) для конфигуратора
                    query += self.make_query_filter(True, mainWindow.rbConf.isChecked())
                    mainWindow.apply_filter_conf(query, 6)
                    self.close()

    def make_query_filter(self, changes, having):
        if changes:  # Если есть изменения, то добавляем к запросу связывающие таблицы фильтры
            if having:  # Если отмечен переключатель наличия
                query = " AND power.id = sklad_power.id_izd AND power.id_proizv = proizv_power.id " \
                        " AND power.exist = True " \
                        " ORDER BY power.exist DESC"
                return query
            else:
                query = "AND power.id = sklad_power.id_izd AND power.id_proizv = proizv_power.id " \
                        " ORDER BY power.exist DESC"
                return query

        # Если фильтры не выбраны
        else:
            if having:
                query = "SELECT sklad_power.kol, power.exist, power.id, proizv_power.name, " \
                        "fullname, formfactor, length, power, certificate, pinmain, " \
                        "pinsata, connproc, kolconnproc, connvideo, kolconnvideo, price " \
                        "FROM power, sklad_power, proizv_power " \
                        "WHERE power.id = sklad_power.id_izd AND power.id_proizv = proizv_power.id " \
                        " AND power.exist = True " \
                        " ORDER BY power.exist DESC"
                return query
            else:
                query = "SELECT sklad_power.kol, power.exist, power.id, proizv_power.name, " \
                        "fullname, formfactor, length, power, certificate, pinmain, " \
                        "pinsata, connproc, kolconnproc, connvideo, kolconnvideo, price " \
                        "FROM power, sklad_power, proizv_power " \
                        "WHERE power.id = sklad_power.id_izd AND power.id_proizv = proizv_power.id " \
                        " ORDER BY power.exist DESC"
                return query


class BodyFilter(QtWidgets.QWidget, widgetBodyFilter.Ui_WidgetBodyFilter):
    def __init__(self, tab, mainWindow):
        super().__init__()
        self.setupUi(self)
        self.mainWindow = mainWindow
        self.tab_window = tab  # Где было создано окно фильтрации - в конфигураторе или на складе
        # -------------Сигналы обновления значений в полях при движении слайдера------------
        self.sliderPriceMin.valueChanged.connect(lambda value: update_field_value(self.leMinPrice, value))
        self.sliderPriceMax.valueChanged.connect(lambda value: update_field_value(self.leMaxPrice, value))
        self.sliderVideoLenMin.valueChanged.connect(lambda value: update_field_value(self.leMinVideoLen, value))
        self.sliderVideoLenMax.valueChanged.connect(lambda value: update_field_value(self.leMaxVideoLen, value))
        self.sliderPowerLenMin.valueChanged.connect(lambda value: update_field_value(self.leMinPowerLen, value))
        self.sliderPowerLenMax.valueChanged.connect(lambda value: update_field_value(self.leMaxPowerLen, value))
        self.sliderCoolHeightMin.valueChanged.connect(lambda value: update_field_value(self.leMinCoolHeight, value))
        self.sliderCoolHeightMax.valueChanged.connect(lambda value: update_field_value(self.leMaxCoolHeight, value))
        self.sliderWeightMin.valueChanged.connect(lambda value: update_field_value(self.leMinWeight, value))
        self.sliderWeightMax.valueChanged.connect(lambda value: update_field_value(self.leMaxWeight, value))
        # -------------Сигналы обновления значений в слайдерах при вводе числа------------
        self.leMinPrice.textChanged.connect(
            lambda value: update_slider_value(self.sliderPriceMin, value, self.leMinPrice))
        self.leMaxPrice.textChanged.connect(
            lambda value: update_slider_value(self.sliderPriceMax, value, self.leMaxPrice))
        self.leMinVideoLen.textChanged.connect(
            lambda value: update_slider_value(self.sliderVideoLenMin, value, self.leMinVideoLen))
        self.leMaxVideoLen.textChanged.connect(
            lambda value: update_slider_value(self.sliderVideoLenMax, value, self.leMaxVideoLen))
        self.leMinPowerLen.textChanged.connect(
            lambda value: update_slider_value(self.sliderPowerLenMin, value, self.leMinPowerLen))
        self.leMaxPowerLen.textChanged.connect(
            lambda value: update_slider_value(self.sliderPowerLenMax, value, self.leMaxPowerLen))
        self.leMinCoolHeight.textChanged.connect(
            lambda value: update_slider_value(self.sliderCoolHeightMin, value, self.leMinCoolHeight))
        self.leMaxCoolHeight.textChanged.connect(
            lambda value: update_slider_value(self.sliderCoolHeightMax, value, self.leMaxCoolHeight))
        self.leMinWeight.textChanged.connect(
            lambda value: update_slider_value(self.sliderWeightMin, value, self.leMinWeight))
        self.leMaxWeight.textChanged.connect(
            lambda value: update_slider_value(self.sliderWeightMax, value, self.leMaxWeight))
        # ----------------------------------------------------------------------------------

        # -------------------Задание ограничений для полей ввода-------------------
        only_int = QIntValidator()
        only_int.setRange(0, 999999)

        two_digits_int = QIntValidator()
        two_digits_int.setRange(0, 99)

        three_digits_int = QIntValidator()
        three_digits_int.setRange(0, 999)

        six_digits_int = QIntValidator()
        six_digits_int.setRange(0, 999999)

        self.leMinPrice.setValidator(six_digits_int)
        self.leMaxPrice.setValidator(six_digits_int)
        self.leMinVideoLen.setValidator(three_digits_int)
        self.leMaxVideoLen.setValidator(three_digits_int)
        self.leMinPowerLen.setValidator(three_digits_int)
        self.leMaxPowerLen.setValidator(three_digits_int)
        self.leMinCoolHeight.setValidator(three_digits_int)
        self.leMaxCoolHeight.setValidator(three_digits_int)
        self.leMinWeight.setValidator(two_digits_int)
        self.leMaxWeight.setValidator(two_digits_int)
        # -------------------Задание ограничений для полей ввода-------------------

        # -------------------Установка ширины столбцов для таблиц-------------------
        self.tableProizv.setColumnWidth(0, 40)
        self.tableProizv.setColumnWidth(1, 243)
        self.tableProizv.cellClicked.connect(
            lambda row, column, table=self.tableProizv:
            cell_row(row, column, table))

        self.tableGaming.setColumnWidth(0, 40)
        self.tableGaming.setColumnWidth(1, 243)
        self.tableGaming.cellClicked.connect(
            lambda row, column, table=self.tableGaming:
            cell_row(row, column, table))

        self.tableType.setColumnWidth(0, 40)
        self.tableType.setColumnWidth(1, 243)
        self.tableType.cellClicked.connect(
            lambda row, column, table=self.tableType:
            cell_row(row, column, table))

        self.tableFfmother.setColumnWidth(0, 40)
        self.tableFfmother.setColumnWidth(1, 243)
        self.tableFfmother.cellClicked.connect(
            lambda row, column, table=self.tableFfmother:
            cell_row(row, column, table))

        self.tableFfpower.setColumnWidth(0, 40)
        self.tableFfpower.setColumnWidth(1, 243)
        self.tableFfpower.cellClicked.connect(
            lambda row, column, table=self.tableFfpower:
            cell_row(row, column, table))

        # ------------------------------------------------------------------

        # -----------Соединение кнопок сбосов с методом обнуления-----------
        self.btnResetAll.clicked.connect(self.resetAll)
        self.btnResetPrice.clicked.connect(
            lambda: reset_sliders(self.sliderPriceMin, self.sliderPriceMax, self.leMinPrice, self.leMaxPrice))
        self.btnResetVideoLen.clicked.connect(
            lambda: reset_sliders(self.sliderVideoLenMin, self.sliderVideoLenMax, self.leMinVideoLen,
                                  self.leMaxVideoLen))
        self.btnResetPowerLen.clicked.connect(
            lambda: reset_sliders(self.sliderPowerLenMin, self.sliderPowerLenMax, self.leMinPowerLen,
                                  self.leMaxPowerLen))
        self.btnResetCoolHeight.clicked.connect(
            lambda: reset_sliders(self.sliderCoolHeightMin, self.sliderCoolHeightMax, self.leMinCoolHeight,
                                  self.leMaxCoolHeight))
        self.btnResetWeight.clicked.connect(
            lambda: reset_sliders(self.sliderWeightMin, self.sliderWeightMax, self.leMinWeight,
                                  self.leMaxWeight))

        self.btnResetProizv.clicked.connect(lambda: reset_checkboxes(self.tableProizv))
        self.btnResetGaming.clicked.connect(lambda: reset_checkboxes(self.tableGaming))
        self.btnResetType.clicked.connect(lambda: reset_checkboxes(self.tableType))
        self.btnResetFfmother.clicked.connect(lambda: reset_checkboxes(self.tableFfmother))
        self.btnResetFfpower.clicked.connect(lambda: reset_checkboxes(self.tableFfpower))
        # -------------------Соединение кнопк сбосов с методом обнуления-------------------

        # Изменение положения стрелки при нажатии на вкладку фильтра
        self.toolBoxBodyFilter.currentChanged.connect(self.tb_change_arrows)

        # Если выбрана вкладка склада или конфигуратора И включён индикатор "Только в наличии"
        if self.tab_window == 0 and mainWindow.rbSklad.isChecked():
            self.load_exists_parameters()
        elif self.tab_window == 0:
            self.load_all_parameters()
        elif self.tab_window == 1 and mainWindow.rbConf.isChecked():
            self.load_exists_parameters()
        elif self.tab_window == 1:
            self.load_all_parameters()

        self.btnAccept.clicked.connect(lambda: self.click_accept(mainWindow))

    def load_all_parameters(self):
        """
            Метод, загружающий параметры всех видеокарт
        """
        self.tableProizv.clear()
        self.tableGaming.clear()
        self.tableType.clear()
        self.tableFfmother.clear()
        self.tableFfpower.clear()

        conn = None
        cur = None
        try:
            conn = psycopg2.connect(database="confPc",
                                    user="postgres",
                                    password="2001",
                                    host="localhost",
                                    port="5432")
            cur = conn.cursor()

            cur.execute(" SELECT price FROM body ORDER BY price DESC LIMIT 1")
            for name in cur:
                self.sliderPriceMin.setRange(0, int(name[0]))
                self.sliderPriceMax.setRange(0, int(name[0]))
                self.leMaxPrice.setPlaceholderText(f"до {int(name[0])}")

            cur.execute(" SELECT lengthvideo FROM body ORDER BY lengthvideo DESC LIMIT 1")
            for name in cur:
                self.sliderVideoLenMin.setRange(0, int(name[0]))
                self.sliderVideoLenMax.setRange(0, int(name[0]))
                self.leMaxVideoLen.setPlaceholderText(f"до {int(name[0])}")

            cur.execute(" SELECT lengthpower FROM body ORDER BY lengthpower DESC LIMIT 1")
            for name in cur:
                self.sliderPowerLenMin.setRange(0, int(name[0]))
                self.sliderPowerLenMax.setRange(0, int(name[0]))
                self.leMaxPowerLen.setPlaceholderText(f"до {int(name[0])}")

            cur.execute(" SELECT heightcool FROM body ORDER BY heightcool DESC LIMIT 1")
            for name in cur:
                self.sliderCoolHeightMin.setRange(0, int(name[0]))
                self.sliderCoolHeightMax.setRange(0, int(name[0]))
                self.leMaxCoolHeight.setPlaceholderText(f"до {int(name[0])}")

            cur.execute(" SELECT weight FROM body ORDER BY weight DESC LIMIT 1")
            for name in cur:
                self.sliderWeightMin.setRange(0, int(name[0]))
                self.sliderWeightMax.setRange(0, int(name[0]))
                self.leMaxWeight.setPlaceholderText(f"до {int(name[0])}")

            cur.execute("SELECT DISTINCT name FROM proizv_body, body "
                        "WHERE proizv_body.id = body.id_proizv "
                        "ORDER BY name ASC")
            row_count = 0
            for name in cur:
                self.tableProizv.setRowCount(row_count + 1)
                self.tableProizv.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT gaming FROM body "
                        "ORDER BY gaming ASC")
            for name in cur:
                self.tableGaming.setRowCount(row_count + 1)
                self.tableGaming.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            count = 0  # Счётчик уникальных записей в словаре
            dict_sockets = {}  # словарь, куда будут сохраняться фф м.п. как ключи (ключи не повторяются)
            cur.execute("SELECT DISTINCT ffmother FROM body "
                        "ORDER BY ffmother ASC")
            for name in cur:
                str_name = str(name)
                # Преобразуем кортеж в строку и удаляем лишние символы, чтобы можно было сделать split списка по ',',
                # а затем записать результаты разбиения кортежа в фильтрующую таблицу
                str_name = re.sub('[^A-Za-z_0-9,+-]', '', str_name)
                str_name = str_name[:-1] + ''  # Удаляем последний символ
                list_name = str_name.split(',')  # Создаём из кортежа список и из списка заполняем таблицы формфакторами
                for i in list_name:
                    dict_sockets[i] = count  # Если такой сокет уже есть - он не добавится снова в словарь
                    count += 1
            sockets = sorted(dict_sockets)  # Сортируем словарь (возвращает отсортированный список ключей)
            row_count = 0
            for elem in sockets:
                self.tableFfmother.setRowCount(row_count + 1)
                self.tableFfmother.setItem(row_count, 1, QtWidgets.QTableWidgetItem(elem))
                row_count += 1

            count = 0  # Счётчик уникальных записей в словаре
            dict_sockets = {}  # словарь, куда будут сохраняться фф м.п. как ключи (ключи не повторяются)
            cur.execute("SELECT DISTINCT ffpower FROM body "
                        "ORDER BY ffpower ASC")
            for name in cur:
                str_name = str(name)
                # Преобразуем кортеж в строку и удаляем лишние символы, чтобы можно было сделать split списка по ',',
                # а затем записать результаты разбиения кортежа в фильтрующую таблицу
                str_name = re.sub('[^A-Za-z_0-9,+-]', '', str_name)
                str_name = str_name[:-1] + ''  # Удаляем последний символ
                list_name = str_name.split(',')  # Создаём из кортежа список и из списка заполняем таблицы формфакторами
                for i in list_name:
                    dict_sockets[i] = count  # Если такой сокет уже есть - он не добавится снова в словарь
                    count += 1
            sockets = sorted(dict_sockets)  # Сортируем словарь (возвращает отсортированный список ключей)
            row_count = 0
            for elem in sockets:
                self.tableFfpower.setRowCount(row_count + 1)
                self.tableFfpower.setItem(row_count, 1, QtWidgets.QTableWidgetItem(elem))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT type FROM body "
                        "ORDER BY type ASC")
            for name in cur:
                self.tableType.setRowCount(row_count + 1)
                self.tableType.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            # Заполнение таблиц кнопками CB
            self.pasteCheckBoxes()

        except (Exception, psycopg2.DatabaseError) as error:
            dialog = DialogOk("Ошибка", error)
            dialog.show()

        finally:
            if conn:
                cur.close()
                conn.close()

    def load_exists_parameters(self):
        """
            Метод, загружающий параметры имеющихся в наличии видеокарт
        """
        self.tableProizv.clear()
        self.tableGaming.clear()
        self.tableType.clear()
        self.tableFfmother.clear()
        self.tableFfpower.clear()

        conn = None
        cur = None
        try:
            conn = psycopg2.connect(database="confPc",
                                    user="postgres",
                                    password="2001",
                                    host="localhost",
                                    port="5432")
            cur = conn.cursor()

            cur.execute(" SELECT price FROM body WHERE exist = True ORDER BY price DESC LIMIT 1")
            for name in cur:
                self.sliderPriceMin.setRange(0, int(name[0]))
                self.sliderPriceMax.setRange(0, int(name[0]))
                self.leMaxPrice.setPlaceholderText(f"до {int(name[0])}")

            cur.execute(" SELECT lengthvideo FROM body WHERE exist = True ORDER BY lengthvideo DESC LIMIT 1")
            for name in cur:
                self.sliderVideoLenMin.setRange(0, int(name[0]))
                self.sliderVideoLenMax.setRange(0, int(name[0]))
                self.leMaxVideoLen.setPlaceholderText(f"до {int(name[0])}")

            cur.execute(" SELECT lengthpower FROM body WHERE exist = True ORDER BY lengthpower DESC LIMIT 1")
            for name in cur:
                self.sliderPowerLenMin.setRange(0, int(name[0]))
                self.sliderPowerLenMax.setRange(0, int(name[0]))
                self.leMaxPowerLen.setPlaceholderText(f"до {int(name[0])}")

            cur.execute(" SELECT heightcool FROM body WHERE exist = True ORDER BY heightcool DESC LIMIT 1")
            for name in cur:
                self.sliderCoolHeightMin.setRange(0, int(name[0]))
                self.sliderCoolHeightMax.setRange(0, int(name[0]))
                self.leMaxCoolHeight.setPlaceholderText(f"до {int(name[0])}")

            cur.execute(" SELECT weight FROM body WHERE exist = True ORDER BY weight DESC LIMIT 1")
            for name in cur:
                self.sliderWeightMin.setRange(0, int(name[0]))
                self.sliderWeightMax.setRange(0, int(name[0]))
                self.leMaxWeight.setPlaceholderText(f"до {int(name[0])}")

            cur.execute("SELECT DISTINCT name FROM proizv_body, body "
                        "WHERE proizv_body.id = body.id_proizv "
                        "AND body.exist = True "
                        "ORDER BY name ASC")
            row_count = 0
            for name in cur:
                self.tableProizv.setRowCount(row_count + 1)
                self.tableProizv.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT gaming FROM body "
                        "WHERE exist = True "
                        "ORDER BY gaming ASC")
            for name in cur:
                self.tableGaming.setRowCount(row_count + 1)
                self.tableGaming.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            count = 0  # Счётчик уникальных записей в словаре
            dict_sockets = {}  # словарь, куда будут сохраняться фф м.п. как ключи (ключи не повторяются)
            cur.execute("SELECT DISTINCT ffmother FROM body "
                        "WHERE exist = True "
                        "ORDER BY ffmother ASC")
            for name in cur:
                str_name = str(name)
                # Преобразуем кортеж в строку и удаляем лишние символы, чтобы можно было сделать split списка по ',',
                # а затем записать результаты разбиения кортежа в фильтрующую таблицу
                str_name = re.sub('[^A-Za-z_0-9,+-]', '', str_name)
                str_name = str_name[:-1] + ''  # Удаляем последний символ
                list_name = str_name.split(',')  # Создаём из кортежа список и из списка заполняем таблицы формфакторами
                for i in list_name:
                    dict_sockets[i] = count  # Если такой сокет уже есть - он не добавится снова в словарь
                    count += 1
            sockets = sorted(dict_sockets)  # Сортируем словарь (возвращает отсортированный список ключей)
            row_count = 0
            for elem in sockets:
                self.tableFfmother.setRowCount(row_count + 1)
                self.tableFfmother.setItem(row_count, 1, QtWidgets.QTableWidgetItem(elem))
                row_count += 1

            count = 0  # Счётчик уникальных записей в словаре
            dict_sockets = {}  # словарь, куда будут сохраняться фф м.п. как ключи (ключи не повторяются)
            cur.execute("SELECT DISTINCT ffpower FROM body "
                        "WHERE exist = True "
                        "ORDER BY ffpower ASC")
            for name in cur:
                str_name = str(name)
                # Преобразуем кортеж в строку и удаляем лишние символы, чтобы можно было сделать split списка по ',',
                # а затем записать результаты разбиения кортежа в фильтрующую таблицу
                str_name = re.sub('[^A-Za-z_0-9,+-]', '', str_name)
                str_name = str_name[:-1] + ''  # Удаляем последний символ
                list_name = str_name.split(',')  # Создаём из кортежа список и из списка заполняем таблицы формфакторами
                for i in list_name:
                    dict_sockets[i] = count  # Если такой сокет уже есть - он не добавится снова в словарь
                    count += 1
            sockets = sorted(dict_sockets)  # Сортируем словарь (возвращает отсортированный список ключей)
            row_count = 0
            for elem in sockets:
                self.tableFfpower.setRowCount(row_count + 1)
                self.tableFfpower.setItem(row_count, 1, QtWidgets.QTableWidgetItem(elem))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT type FROM body "
                        "WHERE exist = True "
                        "ORDER BY type ASC")
            for name in cur:
                self.tableType.setRowCount(row_count + 1)
                self.tableType.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            # Заполнение таблиц кнопками CB
            self.pasteCheckBoxes()

        except (Exception, psycopg2.DatabaseError) as error:
            dialog = DialogOk("Ошибка", error)
            dialog.show()

        finally:
            if conn:
                cur.close()
                conn.close()

    def tb_change_arrows(self, page):
        self.toolBoxBodyFilter.setItemIcon(page, QIcon("E:/pcconf/images/up-arrow.png"))
        for i in range(self.toolBoxBodyFilter.count()):
            if i != page:
                self.toolBoxBodyFilter.setItemIcon(i, QIcon("E:/pcconf/images/down-arrow.png"))

    # Метод для вставки CB в таблицы
    def pasteCheckBoxes(self):
        insert_cb(self.tableProizv)
        insert_cb(self.tableGaming)
        insert_cb(self.tableType)
        insert_cb(self.tableFfmother)
        insert_cb(self.tableFfpower)

    # Метод, обнуляющий все поля
    def resetAll(self):
        reset_sliders(self.sliderPriceMin, self.sliderPriceMax, self.leMinPrice, self.leMaxPrice)
        reset_sliders(self.sliderVideoLenMin, self.sliderVideoLenMax, self.leMinVideoLen, self.leMaxVideoLen)
        reset_sliders(self.sliderPowerLenMin, self.sliderPowerLenMax, self.leMinPowerLen, self.leMaxPowerLen)
        reset_sliders(self.sliderCoolHeightMin, self.sliderCoolHeightMax, self.leMinCoolHeight, self.leMaxCoolHeight)
        reset_sliders(self.sliderWeightMin, self.sliderWeightMax, self.leMinWeight, self.leMaxWeight)
        reset_checkboxes(self.tableProizv)
        reset_checkboxes(self.tableGaming)
        reset_checkboxes(self.tableType)
        reset_checkboxes(self.tableFfmother)
        reset_checkboxes(self.tableFfpower)

    # Метод, срабатывающий по нажатии на кнопку и отправляющий в БД запрос на фильтрацию данных
    def click_accept(self, mainWindow):
        query = "SELECT sklad_body.kol, body.exist, body.id, proizv_body.name, " \
                "fullname, gaming, type, ffmother, ffpower, " \
                "lengthvideo, heightcool, lengthpower, weight, color, price " \
                "FROM body, sklad_body, proizv_body " \
                "WHERE "

        min_price, max_price = checkFields(self.leMinPrice.text(), self.leMaxPrice.text())
        min_videolen, max_videolen = checkFields(self.leMinVideoLen.text(), self.leMaxVideoLen.text())
        min_powerlen, max_powerlen = checkFields(self.leMinPowerLen.text(), self.leMaxPowerLen.text())
        min_coolheight, max_coolheight = checkFields(self.leMinCoolHeight.text(), self.leMaxCoolHeight.text())
        min_weight, max_weight = checkFields(self.leMinWeight.text(), self.leMaxWeight.text())
        if min_price == -1 or min_videolen == -1 or min_powerlen == -1\
                or min_coolheight == -1 or min_weight == -1:  # если не вернулось -1, то выполняем фильтрацию
            pass
        else:
            query1 = get_checkboxes(self.tableProizv, "proizv_body.name")
            if query1 != "":  # Если есть что добавить к запросу
                query += query1

            if query1 == "":  # Если первая таблица пустая, то добавляем к запросу без AND
                query2 = get_checkboxes(self.tableGaming, "gaming")
                query += query2
            else:
                query2 = get_checkboxes(self.tableGaming, "gaming")
                if query2 != "":  # Если есть что добавить к запросу
                    query += " AND " + query2

            if query1 == "" and query2 == "":  # Если первая таблица пустая, то добавляем к запросу без AND
                query3 = get_checkboxes(self.tableType, "type")
                query += query3
            else:
                query3 = get_checkboxes(self.tableType, "type")
                if query3 != "":  # Если есть что добавить к запросу
                    query += " AND " + query3

            if query1 == "" and query2 == "" and query3 == "":
                query4 = get_checkboxes_concat(self.tableFfmother, "ffmother")
                query += query4
            else:
                query4 = get_checkboxes_concat(self.tableFfmother, "ffmother")
                if query4 != "":
                    query += " AND " + query4

            if query1 == "" and query2 == "" and query3 == "" and query4 == "":
                query5 = get_checkboxes_concat(self.tableFfpower, "ffpower")
                query += query5
            else:
                query5 = get_checkboxes_concat(self.tableFfpower, "ffpower")
                if query5 != "":
                    query += " AND " + query5

            # Вероятно, в проверке слайдеров есть лишние if
            if query1 == "" and query2 == "" and query3 == "" and query4 == "" and query5 == "":  # Если не выбрано ничего в таблицах
                query += check_min_max(min_price, max_price, "Price")
            else:
                if min_price != 0 or max_price != 0:
                    query += " AND " + check_min_max(min_price, max_price, "Price")

            if query1 == "" and query2 == "" and query3 == "" and query4 == "" and query5 == "" \
                    and (min_price == 0 and max_price == 0):
                query += check_min_max(min_videolen, max_videolen, "lengthvideo")
            else:
                if min_videolen != 0 or max_videolen != 0:
                    query += " AND " + check_min_max(min_videolen, max_videolen, "lengthvideo")

            if query1 == "" and query2 == "" and query3 == "" and query4 == "" and query5 == "" \
                    and (min_price == 0 and max_price == 0) and (min_videolen == 0 and max_videolen == 0):
                query += check_min_max(min_powerlen, max_powerlen, "lengthpower")
            else:
                if min_powerlen != 0 or max_powerlen != 0:
                    query += " AND " + check_min_max(min_powerlen, max_powerlen, "lengthpower")

            if query1 == "" and query2 == "" and query3 == "" and query4 == "" and query5 == "" \
                    and (min_price == 0 and max_price == 0) and (min_videolen == 0 and max_videolen == 0)\
                    and (min_powerlen == 0 and max_powerlen == 0):
                query += check_min_max(min_coolheight, max_coolheight, "heightcool")
            else:
                if min_powerlen != 0 or max_powerlen != 0:
                    query += " AND " + check_min_max(min_coolheight, max_coolheight, "heightcool")

            if query1 == "" and query2 == "" and query3 == "" and query4 == "" and query5 == "" \
                    and (min_price == 0 and max_price == 0) and (min_videolen == 0 and max_videolen == 0)\
                    and (min_powerlen == 0 and max_powerlen == 0) and (min_coolheight == 0 and max_coolheight == 0):
                query += check_min_max(min_weight, max_weight, "weight")
            else:
                if min_powerlen != 0 or max_powerlen != 0:
                    query += " AND " + check_min_max(min_weight, max_weight, "weight")

            mainWindow.tabWidgetSklad.setCurrentIndex(0)  # Устанавливаем вкладку перед фильтрацией на 0 место

            # Если изменений в фильтрации не было, то передаём changes = False
            if query == "SELECT sklad_body.kol, body.exist, body.id, proizv_body.name, " \
                        "fullname, gaming, type, ffmother, ffpower, " \
                        "lengthvideo, heightcool, lengthpower, weight, color, price " \
                        "FROM body, sklad_body, proizv_body " \
                        "WHERE ":

                if self.tab_window == 0:  # Если открыта вкладка "Склад", то применяем фильтры для склада
                    # Переопределяем готовым запросом
                    query = self.make_query_filter(False, mainWindow.rbSklad.isChecked())
                    mainWindow.apply_filter_sklad(query, 7)
                    self.close()
                else:  # Если открыта вкладка "Конфигуратор", то применяем фильтры для конфигуратора
                    query = self.make_query_filter(False, mainWindow.rbConf.isChecked())
                    mainWindow.apply_filter_conf(query, 7)
                    self.close()

            # Если фильтры были выбраны (начальный запрос изменился), то передаём changes = True
            else:
                if self.tab_window == 0:
                    # Дописываем финальную часть запроса (отбор по id, exist и ранжирование) для склада
                    query += self.make_query_filter(True, mainWindow.rbSklad.isChecked())
                    mainWindow.apply_filter_sklad(query, 7)
                    self.close()
                else:
                    # Дописываем финальную часть запроса (отбор по id, exist и ранжирование) для конфигуратора
                    query += self.make_query_filter(True, mainWindow.rbConf.isChecked())
                    mainWindow.apply_filter_conf(query, 7)
                    self.close()

    def make_query_filter(self, changes, having):
        if changes:  # Если есть изменения, то добавляем к запросу связывающие таблицы фильтры
            if having:  # Если отмечен переключатель наличия
                query = " AND body.id = sklad_body.id_izd AND body.id_proizv = proizv_body.id" \
                        " AND body.exist = True " \
                        " ORDER BY body.exist DESC"
                return query
            else:
                query = " AND body.id = sklad_body.id_izd AND body.id_proizv = proizv_body.id " \
                        " ORDER BY body.exist DESC"
                return query

        # Если фильтры не выбраны
        else:
            if having:
                query = "SELECT sklad_body.kol, body.exist, body.id, proizv_body.name, " \
                        "fullname, gaming, type, ffmother, ffpower, " \
                        "lengthvideo, heightcool, lengthpower, weight, color, price " \
                        "FROM body, sklad_body, proizv_body " \
                        "WHERE body.id = sklad_body.id_izd AND body.id_proizv = proizv_body.id " \
                        " AND body.exist = True" \
                        " ORDER BY body.exist DESC"
                return query
            else:
                query = "SELECT sklad_body.kol, body.exist, body.id, proizv_body.name, " \
                        "fullname, gaming, type, ffmother, ffpower, " \
                        "lengthvideo, heightcool, lengthpower, weight, color, price " \
                        "FROM body, sklad_body, proizv_body " \
                        "WHERE body.id = sklad_body.id_izd AND body.id_proizv = proizv_body.id " \
                        " ORDER BY body.exist DESC"
                return query

