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


class VideoFilter(QtWidgets.QWidget, widgetVideoFilter.Ui_WidgetVideoFilter):
    def __init__(self, tab, mainWindow):
        super().__init__()
        self.setupUi(self)
        self.mainWindow = mainWindow
        self.tab = tab  # Где было создано окно фильтрации - в конфигураторе или на складе
        # -------------Сигналы обновления значений в полях при движении слайдера------------
        self.sliderPriceMin.valueChanged.connect(lambda value: self.update_field_value(self.leMinPrice, value))
        self.sliderPriceMax.valueChanged.connect(lambda value: self.update_field_value(self.leMaxPrice, value))
        self.sliderTdpMin.valueChanged.connect(lambda value: self.update_field_value(self.leMinTdp, value))
        self.sliderTdpMax.valueChanged.connect(lambda value: self.update_field_value(self.leMaxTdp, value))
        self.sliderLenMin.valueChanged.connect(lambda value: self.update_field_value(self.leMinLen, value))
        self.sliderLenMax.valueChanged.connect(lambda value: self.update_field_value(self.leMaxLen, value))
        # -------------Сигналы обновления значений в слайдерах при вводе числа------------
        self.leMinPrice.textChanged.connect(
            lambda value: self.update_slider_value(self.sliderPriceMin, value, self.leMinPrice))
        self.leMaxPrice.textChanged.connect(
            lambda value: self.update_slider_value(self.sliderPriceMax, value, self.leMaxPrice))
        self.leMinTdp.textChanged.connect(
            lambda value: self.update_slider_value(self.sliderTdpMin, value, self.leMinTdp))
        self.leMaxTdp.textChanged.connect(
            lambda value: self.update_slider_value(self.sliderTdpMax, value, self.leMaxTdp))
        self.leMinLen.textChanged.connect(
            lambda value: self.update_slider_value(self.sliderLenMin, value, self.leMinLen))
        self.leMaxLen.textChanged.connect(
            lambda value: self.update_slider_value(self.sliderLenMax, value, self.leMaxLen))

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
        self.tableChipCreator.setColumnWidth(0, 40)
        self.tableChipCreator.setColumnWidth(1, 250)
        self.tableGraphProc.setColumnWidth(0, 40)
        self.tableGraphProc.setColumnWidth(1, 250)
        self.tableVolume.setColumnWidth(0, 40)
        self.tableVolume.setColumnWidth(1, 250)
        self.tableType.setColumnWidth(0, 40)
        self.tableType.setColumnWidth(1, 250)
        self.tableFreq.setColumnWidth(0, 40)
        self.tableFreq.setColumnWidth(1, 250)
        self.tableBus.setColumnWidth(0, 40)
        self.tableBus.setColumnWidth(1, 250)
        self.tableInterface.setColumnWidth(0, 40)
        self.tableInterface.setColumnWidth(1, 250)
        self.tableMonitor.setColumnWidth(0, 40)
        self.tableMonitor.setColumnWidth(1, 250)
        self.tableResolution.setColumnWidth(0, 40)
        self.tableResolution.setColumnWidth(1, 250)
        # ------------------------------------------------------------------

        # -----------Соединение кнопок сбосов с методом обнуления-----------
        self.btnResetAll.clicked.connect(self.resetAll)
        self.btnResetPrice.clicked.connect(
            lambda: self.reset_sliders(self.sliderPriceMin, self.sliderPriceMax, self.leMinPrice, self.leMaxPrice))
        self.btnResetTdp.clicked.connect(
            lambda: self.reset_sliders(self.sliderTdpMin, self.sliderTdpMax, self.leMinTdp, self.leMaxTdp))
        self.btnResetLen.clicked.connect(
            lambda: self.reset_sliders(self.sliderLenMin, self.sliderLenMax, self.leMinLen, self.leMaxLen))
        self.btnResetProizv.clicked.connect(lambda: self.reset_checkboxes(self.tableProizv))
        self.btnResetChipCreator.clicked.connect(lambda: self.reset_checkboxes(self.tableChipCreator))
        self.btnResetGraphProc.clicked.connect(lambda: self.reset_checkboxes(self.tableGraphProc))
        self.btnResetVolume.clicked.connect(lambda: self.reset_checkboxes(self.tableVolume))
        self.btnResetType.clicked.connect(lambda: self.reset_checkboxes(self.tableType))
        self.btnResetFreq.clicked.connect(lambda: self.reset_checkboxes(self.tableFreq))
        self.btnResetBus.clicked.connect(lambda: self.reset_checkboxes(self.tableBus))
        self.btnResetInterface.clicked.connect(lambda: self.reset_checkboxes(self.tableInterface))
        self.btnResetMonitor.clicked.connect(lambda: self.reset_checkboxes(self.tableMonitor))
        self.btnResetResolution.clicked.connect(lambda: self.reset_checkboxes(self.tableResolution))
        # -------------------Соединение кнопк сбосов с методом обнуления-------------------

        # Изменение положения стрелки при нажатии на вкладку фильтра
        self.toolBoxVidFilter.currentChanged.connect(self.tb_change_arrows)

        self.load_all_parameters()

        self.btnAccept.clicked.connect(lambda: self.click_accept(mainWindow))

    def load_all_parameters(self):
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
                self.tableProizv.setRowCount(row_count+1)
                self.tableProizv.setItem(row_count, 1, QtWidgets.QTableWidgetItem(name[0]))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT chipcreator FROM videocard "
                        "ORDER BY chipcreator ASC")
            for name in cur:
                self.tableChipCreator.setRowCount(row_count+1)
                self.tableChipCreator.setItem(row_count, 1, QtWidgets.QTableWidgetItem(name[0]))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT chipname FROM videocard "
                        "ORDER BY chipname ASC")
            for name in cur:
                self.tableGraphProc.setRowCount(row_count+1)
                self.tableGraphProc.setItem(row_count, 1, QtWidgets.QTableWidgetItem(name[0]))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT vram FROM videocard "
                        "ORDER BY vram ASC")
            for name in cur:
                self.tableVolume.setRowCount(row_count+1)
                self.tableVolume.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT typevram FROM videocard "
                        "ORDER BY typevram ASC")
            for name in cur:
                self.tableType.setRowCount(row_count+1)
                self.tableType.setItem(row_count, 1, QtWidgets.QTableWidgetItem(name[0]))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT frequency FROM videocard "
                        "ORDER BY frequency ASC")
            for name in cur:
                self.tableFreq.setRowCount(row_count+1)
                self.tableFreq.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT bus FROM videocard "
                        "ORDER BY bus ASC")
            for name in cur:
                self.tableBus.setRowCount(row_count+1)
                self.tableBus.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT interface FROM videocard "
                        "ORDER BY interface ASC")
            for name in cur:
                self.tableInterface.setRowCount(row_count+1)
                self.tableInterface.setItem(row_count, 1, QtWidgets.QTableWidgetItem(name[0]))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT monitor FROM videocard "
                        "ORDER BY monitor ASC")
            for name in cur:
                self.tableMonitor.setRowCount(row_count+1)
                self.tableMonitor.setItem(row_count, 1, QtWidgets.QTableWidgetItem(str(name[0])))
                row_count += 1

            row_count = 0
            cur.execute("SELECT DISTINCT resolution FROM videocard "
                        "ORDER BY resolution ASC")
            for name in cur:
                self.tableResolution.setRowCount(row_count+1)
                self.tableResolution.setItem(row_count, 1, QtWidgets.QTableWidgetItem(name[0]))
                row_count += 1

            # Заполнение таблиц кнопками CB
            self.pasteCheckBoxes()

        except (Exception, psycopg2.DatabaseError) as error:
            self.dialog = DialogOk("Ошибка", error)
            self.dialog.show()

        finally:
            if conn:
                cur.close()
                conn.close()

    # Метод обновления значений в поле при движении слайдера
    def update_field_value(self, field, value):
        field.setText(f"{value}")

    # Метод обновления слайдера при вводе значений в поле
    def update_slider_value(self, slider, value, field):
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
                lambda ch, row=i: self.current_pos(ch, row, table))
            table.setCellWidget(i, 0, widget)

    def current_pos(self, ch, row, table):
        # print(f' row = {row} -- {ch}')
        table.selectRow(row)

    def tb_change_arrows(self, page):
        self.toolBoxVidFilter.setItemIcon(page, QIcon("E:/pcconf/images/up-arrow.png"))
        for i in range(self.toolBoxVidFilter.count()):
            if i != page:
                self.toolBoxVidFilter.setItemIcon(i, QIcon("E:/pcconf/images/down-arrow.png"))

    # Метод для вставки CB в таблицы
    def pasteCheckBoxes(self):
        self.insert_cb(self.tableProizv)
        self.insert_cb(self.tableChipCreator)
        self.insert_cb(self.tableGraphProc)
        self.insert_cb(self.tableVolume)
        self.insert_cb(self.tableType)
        self.insert_cb(self.tableFreq)
        self.insert_cb(self.tableBus)
        self.insert_cb(self.tableInterface)
        self.insert_cb(self.tableMonitor)
        self.insert_cb(self.tableResolution)

    # Метод, обнуляющий CheckBox-ы в таблице
    def reset_checkboxes(self, table):
        for i in range(table.rowCount()):
            table.clearSelection()
            widget = table.cellWidget(i, 0)
            if widget is not None:
                chk_box = widget.findChild(CheckBox)
                if chk_box is not None and chk_box.isChecked():
                    chk_box.setChecked(False)

    # Метод, обнуляющий значения слайдеров
    def reset_sliders(self, slider_min, slider_max, le_min, le_max):
        slider_min.setValue(0)
        slider_max.setValue(0)
        le_min.clear()
        le_max.clear()

    # Метод, обнуляющий все поля
    def resetAll(self):
        self.reset_sliders(self.sliderPriceMin, self.sliderPriceMax, self.leMinPrice, self.leMaxPrice)
        self.reset_sliders(self.sliderTdpMin, self.sliderTdpMax, self.leMinTdp, self.leMaxTdp)
        self.reset_sliders(self.sliderLenMin, self.sliderLenMax, self.leMinLen, self.leMaxLen)
        self.reset_checkboxes(self.tableProizv)
        self.reset_checkboxes(self.tableChipCreator)
        self.reset_checkboxes(self.tableGraphProc)
        self.reset_checkboxes(self.tableVolume)
        self.reset_checkboxes(self.tableType)
        self.reset_checkboxes(self.tableFreq)
        self.reset_checkboxes(self.tableBus)
        self.reset_checkboxes(self.tableInterface)
        self.reset_checkboxes(self.tableMonitor)
        self.reset_checkboxes(self.tableResolution)

    # Метод, считывающий отмеченные CheckBox-ами строки из таблицы. Возвращает отмеченные строки
    def get_checkboxes(self, table, bd_column):
        selected_parameters = ""
        for i in range(table.rowCount()):
            widget = table.cellWidget(i, 0)
            if widget is not None:
                chk_box = widget.findChild(CheckBox)
                if chk_box is not None and chk_box.isChecked():
                    selected_parameters += "'" + table.item(i, 1).text() + "' " + ", "
        if selected_parameters == "":  # Если ничего не выбрано в таблицах фильтра
            return selected_parameters
        result_selected = selected_parameters[:len(selected_parameters) - 2]  # Удаляем лишние символы
        # res_str = selected_parameters.replace
        return f"{bd_column} = {result_selected}"

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

    # Метод генерации параметров для запроса к БД (получает значения мин. и макс. знач. введённых полей)
    def check_min_max(self, minimun, maximum, bd_column):
        if minimun != -1:  # Если не получили флаг ошибки(-1) - выполняем запрос к БД
            if minimun == 0 and maximum == 0:  # Если пустые поля, то по цене не производим фильтрацию
                # print("Конкатенации с другими запросами не будет")
                return ""
            elif minimun != 0 and maximum == 0:
                return f"{bd_column} >= {minimun} "
            elif minimun == 0 and maximum != 0:
                return f"{bd_column} <= {maximum} "
            else:
                return f"{bd_column} >= {minimun} AND {bd_column} <= {maximum} "
        else:
            return ""

    # Метод, срабатывающий по нажатии на кнопку и отправляющий в БД запрос на фильтрацию данных
    def click_accept(self, mainWindow):
        query = "SELECT kol, videocard.exist, videocard.id, proizv_videocard.name, fullname, chipcreator," \
                "chipname, vram, typevram, frequency, bus, interface, monitor, resolution, tdp, length, price" \
                " FROM videocard, sklad_videocard, proizv_videocard WHERE "

        min_price, max_price = self.checkFields(self.leMinPrice.text(), self.leMaxPrice.text())
        min_tdp, max_tdp = self.checkFields(self.leMinTdp.text(), self.leMaxTdp.text())
        min_len, max_len = self.checkFields(self.leMinLen.text(), self.leMaxLen.text())
        if min_price == -1 or min_tdp == -1 or min_len == -1:  # если не вернулось -1, то выполняем фильтрацию
            pass
        else:
            query += self.check_min_max(min_price, max_price, "Price")

            if (min_price != 0 or max_price != 0) and (min_tdp != 0 or max_tdp != 0):
                query += " AND " + self.check_min_max(min_tdp, max_tdp, "Tdp")
            else:
                query += self.check_min_max(min_tdp, max_tdp, "Tdp")

            if (min_price != 0 or max_price != 0 or min_tdp != 0 or max_tdp != 0) and (min_len != 0 or max_len != 0):
                query += " AND " + self.check_min_max(min_len, max_len, "Length")
            else:
                query += self.check_min_max(min_len, max_len, "Length")

            if query == "SELECT kol, videocard.exist, videocard.id, proizv_videocard.name, fullname, chipcreator," \
                        "chipname, vram, typevram, frequency, bus, interface, monitor, resolution, tdp, length, price" \
                        " FROM videocard, sklad_videocard, proizv_videocard WHERE ":  # Если не выбран фильтр цен
                # query += self.getCheckBoxes(self.tableProizv, "")
                query1 = self.get_checkboxes(self.tableChipCreator, "chipcreator")
                query += query1
            else:  # Если выбрали - дополяем запросы с AND
                query1 = self.get_checkboxes(self.tableChipCreator, "chipcreator")
                if query1 != "":
                    query += "AND " + query1

            if query1 == "":  # Если первая таблица пустая, то добавляем к запросу без AND
                query2 = self.get_checkboxes(self.tableGraphProc, "chipname")
                query += query2
            else:
                query2 = self.get_checkboxes(self.tableGraphProc, "chipname")
                if query2 != "":  # Если есть что добавить к запросу
                    query += "AND " + query2

            if query2 == "":
                query3 = self.get_checkboxes(self.tableVolume, "vram")
                query += query3
            else:
                query3 = self.get_checkboxes(self.tableVolume, "vram")
                if query3 != "":
                    query += "AND " + query3

            if query3 == "":
                query4 = self.get_checkboxes(self.tableType, "typevram")
                query += query4
            else:
                query4 = self.get_checkboxes(self.tableType, "typevram")
                if query4 != "":
                    query += "AND " + query4

            if query4 == "":
                query5 = self.get_checkboxes(self.tableFreq, "frequency")
                query += query5
            else:
                query5 = self.get_checkboxes(self.tableFreq, "frequency")
                if query5 != "":
                    query += "AND " + query5

            if query5 == "":
                query6 = self.get_checkboxes(self.tableBus, "bus")
                query += query6
            else:
                query6 = self.get_checkboxes(self.tableFreq, "bus")
                if query6 != "":
                    query += "AND " + query6

            if query6 == "":
                query7 = self.get_checkboxes(self.tableInterface, "interface")
                query += query7
            else:
                query7 = self.get_checkboxes(self.tableInterface, "interface")
                if query7 != "":
                    query += "AND " + query7

            if query7 == "":
                query8 = self.get_checkboxes(self.tableMonitor, "monitor")
                query += query8
            else:
                query8 = self.get_checkboxes(self.tableMonitor, "monitor")
                if query8 != "":
                    query += "AND " + query8

            if query8 == "":
                query9 = self.get_checkboxes(self.tableResolution, "resolution")
                query += query9
            else:
                query9 = self.get_checkboxes(self.tableResolution, "resolution")
                if query9 != "":
                    query += "AND " + query9
            mainWindow.tabWidgetSklad.setCurrentIndex(0)  # Устанавливаем вкладку перед фильтрацией на 0 место
            if query == "SELECT kol, videocard.exist, videocard.id, proizv_videocard.name, fullname, chipcreator," \
                        "chipname, vram, typevram, frequency, bus, interface, monitor, resolution, tdp, length, price" \
                        " FROM videocard, sklad_videocard, proizv_videocard WHERE ":

                # Если ничего не выбрано (или убраны все фильтры) - выводим всё
                # (запрос для конфигуратора и склада немного отличается)
                if self.tab == 0 and mainWindow.rbSklad.isChecked():  # 0 - склад, 1 - конфигуратор
                    query = "SELECT kol, videocard.exist, videocard.id, proizv_videocard.name, fullname, chipcreator," \
                            "chipname, vram, typevram, frequency, bus, interface, monitor, resolution, tdp, length, price" \
                            " FROM videocard, sklad_videocard, proizv_videocard" \
                            " WHERE videocard.id = sklad_videocard.id_izd AND videocard.id_proizv = proizv_videocard.id" \
                            " AND videocard.exist = True" \
                            " ORDER BY exist DESC"
                    mainWindow.apply_filter_sklad(query, 0)
                    self.close()
                elif self.tab == 0:  # 0 - склад, 1 - конфигуратор
                    query = "SELECT kol, videocard.exist, videocard.id, proizv_videocard.name, fullname, chipcreator," \
                            "chipname, vram, typevram, frequency, bus, interface, monitor, resolution, tdp, length, price" \
                            " FROM videocard, sklad_videocard, proizv_videocard" \
                            " WHERE videocard.id = sklad_videocard.id_izd AND videocard.id_proizv = proizv_videocard.id" \
                            " ORDER BY exist DESC"
                    mainWindow.apply_filter_sklad(query, 0)
                    self.close()

                elif self.tab == 1 and mainWindow.rb_have_conf.isChecked():  # Иначе - вызов запросов для конфигуратора
                    query += " videocard.id = sklad_videocard.id_izd AND videocard.id_proizv = proizv_videocard.id" \
                             " AND videocard.exist = True" \
                             " ORDER BY exist DESC"
                    mainWindow.apply_filter_conf(query, 0)
                    self.close()
                elif self.tab == 1:  # Если не выбран RB "только в наличии" - вытягиваем всё
                    query += " videocard.id = sklad_videocard.id_izd AND videocard.id_proizv = proizv_videocard.id" \
                             " ORDER BY exist DESC"
                    mainWindow.apply_filter_conf(query, 0)
                    self.close()

            else:  # Если начальный запрос изменился (выбраны фильтры)
                if self.tab == 0 and mainWindow.rbSklad.isChecked():  # 0 - склад, 1 - конфигуратор
                    query += " AND videocard.id = sklad_videocard.id_izd AND videocard.id_proizv = proizv_videocard.id" \
                             " AND videocard.exist = True" \
                             " ORDER BY exist DESC"
                    mainWindow.apply_filter_sklad(query, 0)
                    self.close()
                elif self.tab == 0:
                    query += " AND videocard.id = sklad_videocard.id_izd AND videocard.id_proizv = proizv_videocard.id" \
                             " ORDER BY exist DESC"
                    mainWindow.apply_filter_sklad(query, 0)
                    self.close()

                elif self.tab == 1 and mainWindow.rb_have_conf.isChecked():
                    query += " AND videocard.id = sklad_videocard.id_izd AND videocard.id_proizv = proizv_videocard.id" \
                             " ORDER BY exist DESC"
                    mainWindow.apply_filter_conf(query, 0)
                    self.close()
                elif self.tab == 1:
                    query += " AND videocard.id = sklad_videocard.id_izd AND videocard.id_proizv = proizv_videocard.id" \
                             " ORDER BY exist DESC"
                    mainWindow.apply_filter_conf(query, 0)
                    self.close()

