import psycopg2

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QPixmap, QIcon, QIntValidator
# ----------файлы интерфейса---------------
from ui.filter import widgetVideoFilter
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
        return f"{bd_column} = '{selected_parameters[0]}'"
    if len(selected_parameters) > 1:
        for i in range(len(selected_parameters)):
            if i == 0:
                result_selected += f"({bd_column} = '{selected_parameters[i]}'"
            elif i == len(selected_parameters) - 1:
                result_selected += f" OR {bd_column} = '{selected_parameters[i]}')"
            else:
                result_selected += f" OR {bd_column} = '{selected_parameters[i]}'"
    # result_selected = selected_parameters[:len(selected_parameters) - 2]  # Удаляем лишние символы
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
        self.tableProizv.setColumnWidth(1, 250)
        self.tableProizv.cellClicked.connect(
            lambda row, column, table=self.tableProizv:
            cell_row(row, column, table))

        self.tableChipCreator.setColumnWidth(0, 40)
        self.tableChipCreator.setColumnWidth(1, 250)
        self.tableChipCreator.cellClicked.connect(
            lambda row, column, table=self.tableChipCreator:
            cell_row(row, column, table))

        self.tableGraphProc.setColumnWidth(0, 40)
        self.tableGraphProc.setColumnWidth(1, 250)
        self.tableGraphProc.cellClicked.connect(
            lambda row, column, table=self.tableGraphProc:
            cell_row(row, column, table))

        self.tableGaming.setColumnWidth(0, 40)
        self.tableGaming.setColumnWidth(1, 250)
        self.tableGaming.cellClicked.connect(
            lambda row, column, table=self.tableGaming:
            cell_row(row, column, table))

        self.tableVolume.setColumnWidth(0, 40)
        self.tableVolume.setColumnWidth(1, 250)
        self.tableVolume.cellClicked.connect(
            lambda row, column, table=self.tableVolume:
            cell_row(row, column, table))

        self.tableType.setColumnWidth(0, 40)
        self.tableType.setColumnWidth(1, 250)
        self.tableType.cellClicked.connect(
            lambda row, column, table=self.tableType:
            cell_row(row, column, table))

        self.tableFreq.setColumnWidth(0, 40)
        self.tableFreq.setColumnWidth(1, 250)
        self.tableFreq.cellClicked.connect(
            lambda row, column, table=self.tableFreq:
            cell_row(row, column, table))

        self.tableBus.setColumnWidth(0, 40)
        self.tableBus.setColumnWidth(1, 250)
        self.tableBus.cellClicked.connect(
            lambda row, column, table=self.tableBus:
            cell_row(row, column, table))

        self.tableInterface.setColumnWidth(0, 40)
        self.tableInterface.setColumnWidth(1, 250)
        self.tableInterface.cellClicked.connect(
            lambda row, column, table=self.tableInterface:
            cell_row(row, column, table))

        self.tableMonitor.setColumnWidth(0, 40)
        self.tableMonitor.setColumnWidth(1, 250)
        self.tableMonitor.cellClicked.connect(
            lambda row, column, table=self.tableMonitor:
            cell_row(row, column, table))

        self.tableResolution.setColumnWidth(0, 40)
        self.tableResolution.setColumnWidth(1, 250)
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
                self.tableProizv.setItem(row_count, 1, QtWidgets.QTableWidgetItem(name[0]))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT chipcreator FROM videocard "
                        "ORDER BY chipcreator ASC")
            for name in cur:
                self.tableChipCreator.setRowCount(row_count + 1)
                self.tableChipCreator.setItem(row_count, 1, QtWidgets.QTableWidgetItem(name[0]))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT chipname FROM videocard "
                        "ORDER BY chipname ASC")
            for name in cur:
                self.tableGraphProc.setRowCount(row_count + 1)
                self.tableGraphProc.setItem(row_count, 1, QtWidgets.QTableWidgetItem(name[0]))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT gaming FROM videocard "
                        "ORDER BY gaming ASC")
            for name in cur:
                self.tableGaming.setRowCount(row_count + 1)
                self.tableGaming.setItem(row_count, 1, QtWidgets.QTableWidgetItem(name[0]))
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
                self.tableType.setItem(row_count, 1, QtWidgets.QTableWidgetItem(name[0]))
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
                self.tableProizv.setItem(row_count, 1, QtWidgets.QTableWidgetItem(name[0]))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT chipcreator FROM videocard WHERE exist = True "
                        "ORDER BY chipcreator ASC")
            for name in cur:
                self.tableChipCreator.setRowCount(row_count + 1)
                self.tableChipCreator.setItem(row_count, 1, QtWidgets.QTableWidgetItem(name[0]))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT chipname FROM videocard WHERE exist = True "
                        "ORDER BY chipname ASC")
            for name in cur:
                self.tableGraphProc.setRowCount(row_count + 1)
                self.tableGraphProc.setItem(row_count, 1, QtWidgets.QTableWidgetItem(name[0]))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT gaming FROM videocard WHERE exist = True  "
                        "ORDER BY gaming ASC")
            for name in cur:
                self.tableGaming.setRowCount(row_count + 1)
                self.tableGaming.setItem(row_count, 1, QtWidgets.QTableWidgetItem(name[0]))
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
                self.tableType.setItem(row_count, 1, QtWidgets.QTableWidgetItem(name[0]))
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
                self.tableInterface.setItem(row_count, 1, QtWidgets.QTableWidgetItem(name[0]))
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
            query1 = get_checkboxes(self.tableChipCreator, "chipcreator")
            if query1 != "":  # Если есть что добавить к запросу
                query += query1

            if query1 == "":  # Если первая таблица пустая, то добавляем к запросу без AND
                query2 = get_checkboxes(self.tableGraphProc, "chipname")
                query += query2
            else:
                query2 = get_checkboxes(self.tableGraphProc, "chipname")
                if query2 != "":  # Если есть что добавить к запросу
                    query += " AND " + query2

            if query1 == "" and query2 == "":
                query3 = get_checkboxes(self.tableGaming, "gaming")
                query += query3
            else:
                query3 = get_checkboxes(self.tableGaming, "gaming")
                if query3 != "":
                    query += " AND " + query3

            if query1 == "" and query2 == "" and query3 == "":
                query4 = get_checkboxes(self.tableVolume, "vram")
                query += query4
            else:
                query4 = get_checkboxes(self.tableVolume, "vram")
                if query4 != "":
                    query += " AND " + query4

            if query1 == "" and query2 == "" and query3 == "" and query4 == "":
                query5 = get_checkboxes(self.tableType, "typevram")
                query += query5
            else:
                query5 = get_checkboxes(self.tableType, "typevram")
                if query5 != "":
                    query += " AND " + query5

            if query1 == "" and query2 == "" and query3 == "" and query4 == "" and query5 == "":
                query6 = get_checkboxes(self.tableFreq, "frequency")
                query += query6
            else:
                query6 = get_checkboxes(self.tableFreq, "frequency")
                if query6 != "":
                    query += " AND " + query6

            if query1 == "" and query2 == "" and query3 == "" and query4 == "" and query5 == "" and query6 == "":
                query7 = get_checkboxes(self.tableBus, "bus")
                query += query7
            else:
                query7 = get_checkboxes(self.tableBus, "bus")
                if query7 != "":
                    query += " AND " + query7

            if query1 == "" and query2 == "" and query3 == "" and query4 == "" and query5 == "" and query6 == "" \
                    and query7 == "":
                query8 = get_checkboxes(self.tableInterface, "interface")
                query += query8
            else:
                query8 = get_checkboxes(self.tableInterface, "interface")
                if query8 != "":
                    query += " AND " + query8

            if query1 == "" and query2 == "" and query3 == "" and query4 == "" and query5 == "" and query6 == "" \
                    and query7 == "" and query8 == "":
                query9 = get_checkboxes(self.tableMonitor, "monitor")
                query += query9
            else:
                query9 = get_checkboxes(self.tableMonitor, "monitor")
                if query9 != "":
                    query += " AND " + query9

            if query1 == "" and query2 == "" and query3 == "" and query4 == "" and query5 == "" and query6 == "" \
                    and query7 == "" and query8 == "" and query9 == "":
                query10 = get_checkboxes(self.tableResolution, "resolution")
                query += query10
            else:
                query10 = get_checkboxes(self.tableResolution, "resolution")
                if query10 != "":
                    query += " AND " + query10

            # Вероятно, в проверке слайдеров есть лишние if
            if query1 == "" and query2 == "" and query3 == "" and query4 == "" and query5 == "" and query6 == "" \
                    and query7 == "" and query8 == "" and query9 == "" and query10 == "":  # Если не выбрано ничего в таблицах
                query += check_min_max(min_price, max_price, "Price")
            else:
                if min_price != 0 or max_price != 0:
                    query += " AND " + check_min_max(min_price, max_price, "Price")

            if query1 == "" and query2 == "" and query3 == "" and query4 == "" and query5 == "" and query6 == "" \
                    and query7 == "" and query8 == "" and query9 == "" and query10 == "" \
                    and (min_price == 0 and max_price == 0):
                query += check_min_max(min_tdp, max_tdp, "Tdp")
            else:
                if min_tdp != 0 or max_tdp != 0:
                    query += " AND " + check_min_max(min_tdp, max_tdp, "Tdp")

            if query1 == "" and query2 == "" and query3 == "" and query4 == "" and query5 == "" and query6 == "" \
                    and query7 == "" and query8 == "" and query9 == "" and query10 == "" \
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
                query = "SELECT kol, videocard.exist, videocard.id, proizv_videocard.name, fullname, gaming, "\
                        "chipcreator, chipname, vram, typevram, frequency, bus, interface, monitor, "\
                        "resolution, tdp, length, connvideo, kolconnvideo, price "\
                        "FROM videocard, sklad_videocard, proizv_videocard "\
                        "WHERE videocard.id = sklad_videocard.id_izd " \
                        "AND videocard.id_proizv = proizv_videocard.id " \
                        "ORDER BY exist DESC "
                return query
