import sys
import psycopg2

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QDialog, QTableWidgetItem
from PyQt5.QtGui import QPixmap
from ui import main_interface, warningWin, acceptionWin
from ui.add import adding  # импорт файла со всеми окнами добавления
from ui.help import helping  # импорт файла со всеми окнами помощи
from ui.filter import filters  # импорт файла со всеми фильтрами
from ui.proizv import addProizvWidget  # импорт файла (виджета) добавления производителя


# Класс диалогового окна с одной кнопкой
class DialogOk(QDialog, warningWin.Ui_warningDialog):
    def __init__(self, error_win_title, error_text):
        QDialog.__init__(self)
        self.setupUi(self)
        self.setWindowTitle(error_win_title)
        self.lbErrDescription.setText(error_text)
        self.btnCancel.clicked.connect(lambda: self.close())


# Класс окна с одной кнопкой
class AcceptionWin(QDialog, acceptionWin.Ui_Dialog):
    def __init__(self, attention_win_title, attention_text):
        QDialog.__init__(self)
        self.setupUi(self)
        self.setWindowTitle(attention_win_title)
        self.lbAttDescription.setText(attention_text)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setText("Подтвердить")
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).setText("Отмена")


# Класс окна с добавлением производителя
class AddProizv(QtWidgets.QWidget, addProizvWidget.Ui_addProizvWidget):
    def __init__(self, mainwindow, text_complect, dict_proizv):
        super().__init__()
        self.setupUi(self)
        self.labelComplect.setText(text_complect)
        # mainwindow.reset_radiobutton(mainwindow.tableSklad)
        self.btnProizvSave.clicked.connect(lambda:
                                           self.create_proizv_query(mainwindow,
                                                                    text_complect,
                                                                    self.leProzivName.text(),
                                                                    dict_proizv))

    def create_proizv_query(self, mainwindow, text_complect, proizv_name, dict_proizv):
        if proizv_name == "":
            self.dialog = DialogOk("Ошибка", "Введите наименование поставщика")
            self.dialog.show()
            if self.dialog.exec():
                pass
        elif proizv_name.casefold() in str(dict_proizv.values()).casefold():
            self.dialog = DialogOk("Ошибка", "Данный поставщик уже есть в базе данных")
            self.dialog.show()
            if self.dialog.exec():
                pass
        else:
            conn = None
            cur = None
            try:
                conn = psycopg2.connect(database="confPc",
                                        user="postgres",
                                        password="2001",
                                        host="localhost",
                                        port="5432")
                cur = conn.cursor()
                match text_complect:  # Определение запроса к БД по названию переданного label
                    case "Производитель видеокарт":
                        cur.callproc('insert_proizv_videocard', [proizv_name])
                        # mainwindow.load_proizv_videocard()  # Загрузка обновлённой таблицы из БД
                    # case2 case3......

            except (Exception, psycopg2.DatabaseError) as error:
                self.dialog = DialogOk("Ошибка", error)
                self.dialog.show()

            finally:
                if conn:
                    conn.commit()
                    cur.close()
                    conn.close()
                mainwindow.load_proizv_videocard()  # Загрузка обновлённой таблицы из БД
                self.close()


class RadioButton(QtWidgets.QRadioButton):
    def __init__(self, parent=None):
        super(RadioButton, self).__init__(parent)
        self.pixmap = QPixmap("E:/pcconf/images/off.png")
        self.pixmap_pressed = QPixmap("E:/pcconf/images/on.png")

    def paintEvent(self, event):
        if self.isChecked():
            pix = self.pixmap_pressed
        else:
            pix = self.pixmap
        painter = QtGui.QPainter(self)
        painter.drawPixmap(event.rect(), pix)

    def sizeHint(self):
        return QtCore.QSize(15, 15)


class MainWindow(QtWidgets.QMainWindow, main_interface.Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Конфигуратор ПК")
        # Словари для хранения пар ключ(id производителя)-наименование производителя
        self.dict_proizv_vid_name = {}

        # Словари для хранения пар ключ(id видеокарты)-производитель(название)
        self.dict_videocard_proizv = {}
        self.dict_processor_proizv = {}
        self.dict_mother_proizv = {}
        self.dict_cool_proizv = {}
        self.dict_ram_proizv = {}
        self.dict_disk_proizv = {}
        self.dict_power_proizv = {}
        self.dict_body_proizv = {}
        # self.dict_proizv_configs = {} ??
        # Словари для хранения пар ключ(id компл.)- количество
        self.dict_videocard_kol = {}

        # Словари для хранения пар ключ(id компл.)- наименование
        self.dict_videocard_name = {}

        self.query_sklad = ""
        self.query_conf = ""

        self.dict_button_group = {}  # Словарь для хранения групп RB и таблиц, в которых они находятся
        # =============================== Надстройки вкладки "Склад"================================
        self.tableSklad.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)

        self.toolBoxNavigation.currentChanged.connect(lambda index: self.load_all_sklad(index))
        # таблицы и менять вкладки

        self.tabWidgetSklad.tabBarClicked.connect(
            lambda index: self.click_tab_sklad(self.toolBoxNavigation.currentIndex(),
                                               index, self.tabWidgetSklad))

        self.btnAdd.clicked.connect(lambda: self.tb_new_komplekt(
            self.toolBoxNavigation.currentIndex(),
            True,
            self.tableSklad.currentRow())
                                    )
        # Кнопка повтора заказа уже имеющегося (выбранного) комплектующего
        self.btnRepeat.clicked.connect(lambda: self.tb_new_komplekt(
            self.toolBoxNavigation.currentIndex(),
            False,
            self.current_sklad(
                self.tableSklad.currentRow(),
                self.tableSklad.columnCount()))
                                       )

        # По нажатии на кнопку запускается метод, который принимает выбранную вклдку ТБ и открывает нужное окно фильтра
        self.btnSkladFilter.clicked.connect(lambda: self.tb_sklad_filter(self.toolBoxNavigation.currentIndex()))

        self.load_proizv_videocard()
        self.load_all_sklad(0)  # Первоначальная загрузка всех видеокарт из бд
        # =================================Окна фильтрации комплектующих на складе=========================
        self.vidSkladFilter = filters.VideoFilter(0, self)  # Создаётся отдельный экземпляр для сохранения внесённых д-х
        # .......инициализация других окон фильтрации.......

        # =================================================================================================
        self.tableVideoProizv.setColumnWidth(0, 28)
        self.tableVideoProizv.setColumnWidth(1, 28)
        self.tableVideoProizv.setColumnWidth(2, 0)
        self.tableVideoProizv.setColumnWidth(3, 135)
        self.tableProcProizv.setColumnWidth(0, 28)
        self.tableProcProizv.setColumnWidth(1, 28)
        self.tableProcProizv.setColumnWidth(2, 0)
        self.tableProcProizv.setColumnWidth(3, 135)
        self.tableMotherProizv.setColumnWidth(0, 28)
        self.tableMotherProizv.setColumnWidth(1, 28)
        self.tableMotherProizv.setColumnWidth(2, 0)
        self.tableMotherProizv.setColumnWidth(3, 135)
        self.tableCoolProizv.setColumnWidth(0, 28)
        self.tableCoolProizv.setColumnWidth(1, 28)
        self.tableCoolProizv.setColumnWidth(2, 0)
        self.tableCoolProizv.setColumnWidth(3, 135)
        self.tableRamProizv.setColumnWidth(0, 28)
        self.tableRamProizv.setColumnWidth(1, 28)
        self.tableRamProizv.setColumnWidth(2, 0)
        self.tableRamProizv.setColumnWidth(3, 135)
        self.tableDiskProizv.setColumnWidth(0, 28)
        self.tableDiskProizv.setColumnWidth(1, 28)
        self.tableDiskProizv.setColumnWidth(2, 0)
        self.tableDiskProizv.setColumnWidth(3, 135)
        self.tablePowerProizv.setColumnWidth(0, 28)
        self.tablePowerProizv.setColumnWidth(1, 28)
        self.tablePowerProizv.setColumnWidth(2, 0)
        self.tablePowerProizv.setColumnWidth(3, 135)
        self.tableBodyProizv.setColumnWidth(0, 28)
        self.tableBodyProizv.setColumnWidth(1, 28)
        self.tableBodyProizv.setColumnWidth(2, 0)
        self.tableBodyProizv.setColumnWidth(3, 135)

        # Кнопка создания нового производителя видеокарты
        # x8 x8 x8 x8
        self.btnNewVideoProizv.clicked.connect(lambda:
                                               AddProizv(self, "Производитель видеокарт",
                                                         self.dict_proizv_vid_name).show())
        # Кнопка обновления состояния договора
        self.btnCngVideoProizv.clicked.connect(lambda: self.change_proizv(self.tableVideoProizv))
        self.tableVideoProizv.cellClicked.connect(
            lambda row, column, table=self.tableVideoProizv:
            self.cell_row(row, column, table))
        # x8 x8 x8 x8
        self.tableSklad.cellClicked.connect(
            lambda row, column, table=self.tableSklad:
            self.cell_row(row, column, table))

        # ==========================================================================================

        # =========================== Надстройки вкладки "Конфигуратор"=============================

        self.treeWidget.itemClicked.connect(lambda: self.treeNavigation())
        # ----------------------Заполнение таблиц RB---------------------------

        self.row_selected = None
        self.insert_rb(self.tableConfVideo)
        self.insert_rb(self.tableConfProc)
        self.insert_rb(self.tableConfMother)
        self.insert_rb(self.tableConfCool)
        self.insert_rb(self.tableConfRam)
        self.insert_rb(self.tableConfDisk)
        self.insert_rb(self.tableConfPower)
        self.insert_rb(self.tableConfBody)
        # ---------------------------------------------------------------------

        # ---------------------Кнопки с помощью--------------------------------
        self.vHelp = helping.VideoHelp()
        self.btnVidHelp.clicked.connect(lambda: self.vHelp.show())

        # ---------------------------------------------------------------------

        # ---------------------Кнопки с фильтрами------------------------------
        self.vidConfFilter = filters.VideoFilter(1, self)  # Создаётся отдельный экземпляр для сохранения внесённых д-х
        self.btnVidFilter.clicked.connect(lambda: self.vidConfFilter.show())

        # ---------------------------------------------------------------------

        # -----------------------Кнопка сброса сборки--------------------------
        self.btnResetConfig.clicked.connect(self.reset_all_config)
        # ---------------------------------------------------------------------

        self.table_config.setColumnWidth(0, 0)
        self.table_config.setColumnWidth(1, 170)
        self.table_config.setColumnWidth(2, 55)
        self.table_config.setColumnWidth(3, 15)
        #####
        self.tableConfVideo.setColumnWidth(0, 50)
        self.tableConfVideo.setColumnWidth(1, 40)
        self.tableConfVideo.setColumnWidth(2, 180)
        self.tableConfVideo.setColumnWidth(3, 180)

        self.tableConfVideo.cellClicked.connect(
            lambda row, column, table=self.tableConfVideo:
            self.cell_row(row, column, table))

        self.tableConfProc.cellClicked.connect(
            lambda row, column, table=self.tableConfProc:
            self.cell_row(row, column, table))

        self.tableConfMother.cellClicked.connect(
            lambda row, column, table=self.tableConfMother:
            self.cell_row(row, column, table))

        self.tableConfCool.cellClicked.connect(
            lambda row, column, table=self.tableConfCool:
            self.cell_row(row, column, table))

        self.tableConfRam.cellClicked.connect(
            lambda row, column, table=self.tableConfRam:
            self.cell_row(row, column, table))

        self.tableConfDisk.cellClicked.connect(
            lambda row, column, table=self.tableConfDisk:
            self.cell_row(row, column, table))

        self.tableConfPower.cellClicked.connect(
            lambda row, column, table=self.tableConfPower:
            self.cell_row(row, column, table))

        self.tableConfBody.cellClicked.connect(
            lambda row, column, table=self.tableConfBody:
            self.cell_row(row, column, table))

        self.video_tabs = ["RADEON", "NVIDIA", "INTEL"]  # список с названиями (принимается с БД)
        self.processor_tabs = ["INTEL", "AMD"]
        #self.fill_tabs(self.video_tabs, self.tabWidgetVideo)
        #self.fill_tabs(self.processor_tabs, self.tabWidgetProc)
        self.tabWidgetVideo.tabBarClicked.connect(lambda index: self.click_tab_conf(index, self.tabWidgetVideo))
        self.tabWidgetProc.tabBarClicked.connect(lambda index: self.click_tab_conf(index, self.tabWidgetProc))

    # Метод загрузки таблицы производителей видеокарт из БД
    def load_proizv_videocard(self):
        self.tableVideoProizv.clearSelection()
        self.tableVideoProizv.clear()
        self.dict_proizv_vid_name.clear()
        conn = None
        cur = None
        try:
            conn = psycopg2.connect(database="confPc",
                                    user="postgres",
                                    password="2001",
                                    host="localhost",
                                    port="5432")
            cur = conn.cursor()
            cur.callproc("get_proizv_videocard")
            row_count = 0
            for row in cur:
                self.tableVideoProizv.setRowCount(row_count + 1)
                # 0 столбец - radiobutton
                # 1 столбец - индикатор состояния договора
                self.tableVideoProizv.setItem(row_count, 2, QtWidgets.QTableWidgetItem(str(row[1])))
                self.dict_proizv_vid_name[row[0]] = row[2]  # Сохраняем id производителя и его имя
                self.tableVideoProizv.setItem(row_count, 3, QtWidgets.QTableWidgetItem(row[2]))
                row_count += 1

        except (Exception, psycopg2.DatabaseError) as error:
            self.dialog = DialogOk("Ошибка", error)
            self.dialog.show()

        finally:
            if conn:
                cur.close()
                conn.close()
            self.insert_existence_proizv(self.tableVideoProizv)
            self.insert_rb_sklad(self.tableVideoProizv)  # Загрузка rb для визаулизции

    # изменение состояния в таблице поставщика
    def change_proizv(self, table):
        if table.currentRow() == -1:
            err = "Выберите поставщика для изменения"
            self.dialog = DialogOk("Ошибка", err)
            self.dialog.show()
        else:
            att = "Вы действительно хотите изменить договор поставок?"
            self.dialog = AcceptionWin("Подтвердите действие", att)
            self.dialog.show()
            if self.dialog.exec():
                if table.item(table.currentRow(), 2).text() == "True":  # Перезаписываем в БД и обновляем таблицу
                    self.rewrite_proizv_videocard(False, table.item(table.currentRow(),
                                                                    3).text())

                else:
                    self.rewrite_proizv_videocard(True, table.item(table.currentRow(), 3).text())
                table.clearSelection()
                table.setCurrentCell(-1, -1)
                self.reset_radiobutton(table)
            else:
                table.clearSelection()
                table.setCurrentCell(-1, -1)
                self.reset_radiobutton(table)

    # Метод перезаписи данных о производителях видеокарты
    def rewrite_proizv_videocard(self, contract, name):
        conn = None
        cur = None
        try:
            conn = psycopg2.connect(database="confPc",
                                    user="postgres",
                                    password="2001",
                                    host="localhost",
                                    port="5432")
            cur = conn.cursor()
            cur.callproc('update_video_dogovor', [contract, name])

        except (Exception, psycopg2.DatabaseError) as error:
            self.dialog = DialogOk("Ошибка", error)
            self.dialog.show()

        finally:
            if conn:
                conn.commit()
                cur.close()
                conn.close()
            self.load_proizv_videocard()  # Загрузка обновлённой таблицы из БД

    # Метод загрузки всех видеокарт из БД с заполнением словарей (x8)
    def load_all_sklad(self, page):
        conn = None
        cur = None
        try:
            conn = psycopg2.connect(database="confPc",
                                    user="postgres",
                                    password="2001",
                                    host="localhost",
                                    port="5432")
            cur = conn.cursor()
            match page:
                case 0:
                    self.dict_videocard_kol.clear()
                    self.dict_videocard_proizv.clear()
                    self.dict_videocard_name.clear()
                    cur.callproc("get_videocard")  # Получаем данные о всех видеокартах
                    self.fill_table_sklad(page, cur)  # Заполняем таблицу
                    self.fill_tabs(page, self.tabWidgetSklad)
                    cur.callproc("get_videocard")
                    for row in cur:  # Заполняем словари данными о видеокартах
                        self.dict_videocard_proizv[row[2]] = row[3]
                        self.dict_videocard_name[row[2]] = row[4]
                        self.dict_videocard_kol[2] = row[1]

                case 1:
                    print("Заполнение таблицы процессорами")
                    self.fill_tabs(page, self.tabWidgetSklad)
                    """self.dict_processor_kol.clear()
                    self.dict_processor_proizv.clear()
                    self.dict_processor_name.clear()
                    cur.callproc("get_processors")  # Получаем данные о всех процессорах
                    self.fill_table_sklad(page, cur)  # Заполняем таблицу
                    cur.callproc("get_processors")
                    for row in cur:  # Заполняем словари данными о процессорах
                        self.dict_processor_proizv[row[2]] = row[3]
                        self.dict_processor_name[row[2]] = row[4]
                        self.dict_processor_kol[2] = row[1]"""

        except (Exception, psycopg2.DatabaseError) as error:
            self.dialog = DialogOk("Ошибка", str(error))
            self.dialog.show()

        finally:
            if conn:
                cur.close()
                conn.close()

    # Метод заполнения полей таблицы склада по фильтрующему запросу из БД
    def fill_table_sklad(self, page, cur):
        self.tableSklad.clear()
        self.tableSklad.clearSelection()
        row_count = 0
        match page:
            case 0:  # Заполнение таблицы видеокартами
                self.tableSklad.setColumnCount(17)  # Число столбцов в видеокарте
                self.tableSklad.setHorizontalHeaderLabels(["", "", "Кол-во",
                                                           "Производитель", "Название", "Произв. чипа",
                                                           "Наименов. чипа", "Объём памяти", "Тип памяти",
                                                           "Частота процессора", "Шина", "Интерфейс",
                                                           "Монитор", "Разрешение", "TDP",
                                                           "Длина", "Цена"])
                for row in cur:
                    self.tableSklad.setRowCount(row_count + 1)
                    self.insert_existence_complect(self.tableSklad, row_count, row[1])
                    self.tableSklad.setItem(row_count, 2, QtWidgets.QTableWidgetItem(str(row[0])))
                    self.tableSklad.setItem(row_count, 3, QtWidgets.QTableWidgetItem(str(row[3])))
                    self.tableSklad.setItem(row_count, 4, QtWidgets.QTableWidgetItem(str(row[4])))
                    self.tableSklad.setItem(row_count, 5, QtWidgets.QTableWidgetItem(str(row[5])))
                    self.tableSklad.setItem(row_count, 6, QtWidgets.QTableWidgetItem(str(row[6])))
                    self.tableSklad.setItem(row_count, 7, QtWidgets.QTableWidgetItem(str(row[7])))
                    self.tableSklad.setItem(row_count, 8, QtWidgets.QTableWidgetItem(str(row[8])))
                    self.tableSklad.setItem(row_count, 9, QtWidgets.QTableWidgetItem(str(row[9])))
                    self.tableSklad.setItem(row_count, 10, QtWidgets.QTableWidgetItem(str(row[10])))
                    self.tableSklad.setItem(row_count, 11, QtWidgets.QTableWidgetItem(str(row[11])))
                    self.tableSklad.setItem(row_count, 12, QtWidgets.QTableWidgetItem(str(row[12])))
                    self.tableSklad.setItem(row_count, 13, QtWidgets.QTableWidgetItem(str(row[13])))
                    self.tableSklad.setItem(row_count, 14, QtWidgets.QTableWidgetItem(str(row[14])))
                    self.tableSklad.setItem(row_count, 15, QtWidgets.QTableWidgetItem(str(row[15])))
                    self.tableSklad.setItem(row_count, 16, QtWidgets.QTableWidgetItem(str(row[16])))
                    self.insert_rb_sklad(self.tableSklad)
                    row_count += 1
                self.tableSklad.resizeColumnsToContents()
            case 1:
                print("Заполнение таблицы из БД процессоров")

    def fill_table_config(self, table):
        table.clearContents()  # хедеры оставляем, меняем только содержимое

    # Метод принимает для вставки таблицу, строку и булевое значение для индикатора
    def paste_existence(self, table, row, col, bool_):
        if bool_:
            table.setCellWidget(row, col, self.create_existence("E:/pcconf/images/have.png"))
        else:
            table.setCellWidget(row, col, self.create_existence("E:/pcconf/images/nothave.png"))

    def insert_existence_proizv(self, table):
        """
        Метод принимает на вход таблицу и построчно вызывает метод вставки индикатора наличия договора
        :param table: Таблица, в которую требуется вставить индикатор
        """
        for i in range(table.rowCount()):
            if table.item(i, 2).text() == "True":
                self.paste_existence(table, i, 1, True)
            else:
                self.paste_existence(table, i, 1, False)

        # Метод принимает на вход таблицу и заполняет столбец индикаторами

    def insert_existence_complect(self, table, row, existence):
        """
        Данный метод заполняет всю таблицу с комплектующими индикаторами наличия их на складе (при количестве > 0)
        :param table: Таблица, в которую требуется вставить индикатор
        :param row:
        :param existence:
        """
        if existence:
            self.paste_existence(table, row, 1, True)
        else:
            self.paste_existence(table, row, 1, False)

    # Чтение выбранной строки в таблце для передачи в перезаказ
    def current_sklad(self, cur_row, count_col):
        data_row = []
        if cur_row == -1:
            err = "Выберите строку для повторного заказа"
            return err
        else:
            for i in range(2, count_col):
                data_row.append(self.tableSklad.item(cur_row, i).text())
            return data_row

    # Метод, заполняющий и блокирующий поле  ввода данных lineEdit
    def block_lineedit(self, field, parameter):
        field.setText(parameter)
        field.setDisabled(True)
        field.setStyleSheet("color:gray;"
                            "padding-left: 5px;"
                            "border: 1px dotted rgb(120,120,120);")

    # # Метод, заполняющий и блокирующий поле  ввода данных comboBox
    def block_combobox(self, field, parameter):
        field.setItemText(0, parameter)
        field.setDisabled(True)
        field.setStyleSheet("QComboBox{color:gray; border: 1px dotted rgb(120,120,120); padding-left: 5px;}"
                            " QComboBox::drop-down{border: 0px;}"
                            '''QComboBox::down-arrow {
                                border-image: url("E:/pcconf/images/down-arrow-gray.png");
                                width: 17px;
                                height: 17px;
                                margin-right: 5px;}''')

    def get_list_proizvoditel(self, table):
        """
        :param table: Таблица производителей, данные которой нужно передать в окно добавления комплектующего
        :return: Список производителей, с которыми есть договор о поставках
        """
        list_proizvoditel = []
        for i in range(table.rowCount()):
            if table.item(i, 2).text() == "True":
                list_proizvoditel.append(table.item(i, 3).text())
        return list_proizvoditel

    # Очень большой метод. Сделать отдельные методы для вызова?
    def tb_new_komplekt(self, page, new_bool, row):
        """
        Метод, завязанный на выбранном в toolbox комплектующем на складе (page).
        При нажатии на кнопку добавить или изменить передается true/false (new_bool).
        Если true - добавляем новое комплектующее. Если false - создаём заказ на существующее комплектующее
        :param page: Порядковый номер выбранной в toolBox страницы на складе
        :param new_bool: Флаг. True - добавление нового комплектующего. False - создание заказа на выбранное компл.
        :param row: Строка, на которую нажал пользователь
        """
        match page:
            case 0:  # 0-9 - вкладки ToolBox (меню навигации)
                if new_bool:  # Если True - добавляем новую запись: открываем пустое окно
                    list_pr = self.get_list_proizvoditel(self.tableVideoProizv)
                    self.tableSklad.clearSelection()
                    self.reset_radiobutton(self.tableSklad)
                    self.win_add_change = adding.AddChangeVideoWindow(self, new_bool, list_pr,
                                                                      self.dict_proizv_vid_name,
                                                                      self.dict_videocard_name)
                    self.win_add_change.show()
                else:  # Есил False - изменяем выбранную запись
                    if type(row) is str:  # Если пришел не кортеж, а строка(ошибка) - вывод окна с ошибкой
                        self.dialog = DialogOk("Ошибка", row)
                        self.dialog.show()
                        if self.dialog.exec():
                            pass
                    else:  # Если пришел список - заполняем окно.
                        self.win_add_change = adding.AddChangeVideoWindow(self, new_bool, row[1],
                                                                          self.dict_proizv_vid_name,
                                                                          self.dict_videocard_name)
                        self.block_combobox(self.win_add_change.cbProizv, row[1])
                        self.block_lineedit(self.win_add_change.leFullName, row[2])
                        self.block_combobox(self.win_add_change.cbChipCreator, row[3])
                        self.block_lineedit(self.win_add_change.leChipName, row[4])
                        self.block_lineedit(self.win_add_change.leVolume, row[5])
                        self.block_lineedit(self.win_add_change.leType, row[6])
                        self.block_lineedit(self.win_add_change.leFreq, row[7])
                        self.block_lineedit(self.win_add_change.leBus, row[8])
                        self.block_combobox(self.win_add_change.cbInterface, row[9])
                        self.block_combobox(self.win_add_change.cbMonitor, row[10])
                        self.block_lineedit(self.win_add_change.leResolution, row[11])
                        self.block_lineedit(self.win_add_change.leTdp, row[12])
                        self.block_lineedit(self.win_add_change.leLength, row[13])
                        self.block_lineedit(self.win_add_change.lePrice, row[14])
                        self.win_add_change.show()
            case 1:
                if new_bool:  # Если True - добавляем новую запись: открываем пустое окно
                    self.win_add_change = adding.AddChangeVideoWindow(self, new_bool, row[1],
                                                                      self.dict_proizv_vid_name,
                                                                      self.dict_videocard_name)
                    #  self.win_add_change.radioButton = RadioButton()
                    self.win_add_change.show()
            case 2:
                if new_bool:  # Если True - добавляем новую запись: открываем пустое окно
                    self.win_add_change = adding.AddChangeVideoWindow(self, new_bool, row[1],
                                                                      self.dict_proizv_vid_name,
                                                                      self.dict_videocard_name)
                    self.win_add_change.show()
            case 3:
                if new_bool:  # Если True - добавляем новую запись: открываем пустое окно
                    self.win_add_change = adding.AddChangeVideoWindow(self, new_bool, row[1],
                                                                      self.dict_proizv_vid_name,
                                                                      self.dict_videocard_name)
                    self.win_add_change.show()
            case 4:
                if new_bool:  # Если True - добавляем новую запись: открываем пустое окно
                    self.win_add_change = adding.AddChangeVideoWindow(self, new_bool, row[1],
                                                                      self.dict_proizv_vid_name,
                                                                      self.dict_videocard_name)
                    self.win_add_change.show()
            case 5:
                if new_bool:  # Если True - добавляем новую запись: открываем пустое окно
                    self.win_add_change = adding.AddChangeVideoWindow(self, new_bool, row[1],
                                                                      self.dict_proizv_vid_name,
                                                                      self.dict_videocard_name)
                    self.win_add_change.show()
            case 6:
                if new_bool:  # Если True - добавляем новую запись: открываем пустое окно
                    self.win_add_change = adding.AddChangeVideoWindow(self, new_bool, row[1],
                                                                      self.dict_proizv_vid_name,
                                                                      self.dict_videocard_name)
                    self.win_add_change.show()
            case 7:
                if new_bool:  # Если True - добавляем новую запись: открываем пустое окно
                    self.win_add_change = adding.AddChangeVideoWindow(self, new_bool, row[1],
                                                                      self.dict_proizv_vid_name,
                                                                      self.dict_videocard_name)
                    self.win_add_change.show()

    # Метод, отвечающий за открытие окна фильтрации на складе. Принимает id вкладки ToolBox
    def tb_sklad_filter(self, page):
        match page:
            case 0:  # 0-9 - вкладки ToolBox (меню навигации)
                self.vidSkladFilter.show()  # Отображение экземпляра класса
            case 1:
                pass
                # self.vidSkladFilter.show()  # Отображение экземпляра класса
            case 2:
                pass
                # self.vidSkladFilter.show()  # Отображение экземпляра класса
            case 3:
                pass
                # self.vidSkladFilter.show()  # Отображение экземпляра класса
            case 4:
                pass
                # self.vidSkladFilter.show()  # Отображение экземпляра класса
            case 5:
                pass
                # self.vidSkladFilter.show()  # Отображение экземпляра класса
            case 6:
                pass
                # self.vidSkladFilter.show()  # Отображение экземпляра класса
            case 7:
                pass
                # self.vidSkladFilter.show()  # Отображение экземпляра класса
            case 8:
                pass
                # self.vidSkladFilter.show()  # Отображение экземпляра класса

    def send_sql_sklad(self, get_query):
        print(get_query)

    def send_sql_conf(self, get_query):
        print(get_query)

    # Метод, возвращающий из БД производителей комплектуюшего
    def get_having_proizv(self, complect):
        conn = None
        cur = None
        list_proizv = []
        try:
            conn = psycopg2.connect(database="confPc",
                                    user="postgres",
                                    password="2001",
                                    host="localhost",
                                    port="5432")
            cur = conn.cursor()
            match complect:  # Определение запроса к БД по типу комплектующего
                case "Videocard":
                    cur.callproc('get_having_videoproizv')
                    for name in cur:
                        list_proizv.append(name[0])
                case "Processor":
                    #cur.callproc('get_having_videoproizv')
                    list_proizv.append("Intel")
                    #for name in cur:
                        #list_proizv.append(name[0])
                case "Motherboard":
                    cur.callproc('get_having_videoproizv')
                    for name in cur:
                        list_proizv.append(name[0])
                case "Cooling":
                    cur.callproc('get_having_videoproizv')
                    for name in cur:
                        list_proizv.append(name[0])
                case "Ram":
                    cur.callproc('get_having_videoproizv')
                    for name in cur:
                        list_proizv.append(name[0])
                case "Disk":
                    cur.callproc('get_having_videoproizv')
                    for name in cur:
                        list_proizv.append(name[0])
                case "Power":
                    cur.callproc('get_having_videoproizv')
                    for name in cur:
                        list_proizv.append(name[0])
                case "Body":
                    cur.callproc('get_having_videoproizv')
                    for name in cur:
                        list_proizv.append(name[0])
        except (Exception, psycopg2.DatabaseError) as error:
            self.dialog = DialogOk("Ошибка", error)
            self.dialog.show()

        finally:
            if conn:
                conn.commit()
                cur.close()
                conn.close()
            list_proizv.insert(0, "Все")
            return list_proizv

    # Метод для заполнения tabWidget-ов переданными производителями
    # На складе разные page и одинаковый tab_widget (таблица скалада 1, виджет так же 1)
    # В конфигураторе передаём сюда и страницу и соответствующий виджет конфигурирования
    def fill_tabs(self, page, tab_widget):
        #if tab_widget.count() > 1:
        #    for i in range(1, tab_widget.count()):  # Удаление старых вкладок
        #        tab_widget.removeTab(i)
        tab_widget.clear()
        match page:
            case 0:
                list_names = self.get_having_proizv("Videocard")
                count_tab = len(list_names)
                for i in range(0, count_tab):  # первая вкладка должна остаться
                    tab = QtWidgets.QWidget()
                    tab_widget.addTab(tab, list_names[i])
            case 1:
                list_names = self.get_having_proizv("Processor")
                count_tab = len(list_names)
                for i in range(0, count_tab):  # первая вкладка должна остаться
                    tab = QtWidgets.QWidget()
                    tab_widget.addTab(tab, list_names[i])

    def click_tab_sklad(self, page, tab_index, tab_widget):
        conn = None
        cur = None
        tab_name = tab_widget.tabText(tab_index)
        print(tab_index)
        print(f"tab_widget.tabText(tab_index) {tab_widget.tabText(tab_index)}")
        try:
            conn = psycopg2.connect(database="confPc",
                                    user="postgres",
                                    password="2001",
                                    host="localhost",
                                    port="5432")
            cur = conn.cursor()
            match page:
                case 0:
                    if tab_name == "Все":
                        cur.callproc('get_videocard')
                        self.fill_table_sklad(page, cur)
                    else:
                        cur.callproc('get_videocard_by_name', [tab_name])
                        self.fill_table_sklad(page, cur)
                case 1:
                    if tab_name == "Все":
                        cur.callproc('get_videocard')
                        self.fill_table_sklad(page, cur)
                    else:
                        cur.callproc('get_videocard_by_name', [tab_name])
                        self.fill_table_sklad(page, cur)
                # case 2-9...

        except (Exception, psycopg2.DatabaseError) as error:
            self.dialog = DialogOk("Ошибка", error)
            self.dialog.show()

        finally:
            if conn:
                cur.close()
                conn.close()

    def click_tab_conf(self, tab_index, tab_widget):
        tab_name = tab_widget.tabText(tab_index)
        print(f"SELECT FROM TABLE WHERE FIELD1 ='{tab_name}'")

    def treeNavigation(self):
        index = self.treeWidget.currentIndex().row()
        match index:
            case 0:
                self.scrollArea.verticalScrollBar().setValue(0)
            case 1:
                self.scrollArea.verticalScrollBar().setValue(310)
            case 2:
                self.scrollArea.verticalScrollBar().setValue(620)
            case 3:
                self.scrollArea.verticalScrollBar().setValue(930)
            case 4:
                self.scrollArea.verticalScrollBar().setValue(1240)
            case 5:
                self.scrollArea.verticalScrollBar().setValue(1550)
            case 6:
                self.scrollArea.verticalScrollBar().setValue(1860)
            case 7:
                self.scrollArea.verticalScrollBar().setValue(1860)

    #  метод создания индикатора состояния комплектующего
    def create_existence(self, png_way):
        widget = QtWidgets.QWidget()
        pLayout = QtWidgets.QHBoxLayout(widget)
        pixmap = QPixmap(png_way)
        lbl = QtWidgets.QLabel()
        lbl.setPixmap(pixmap)
        pLayout.addWidget(lbl)
        pLayout.setAlignment(QtCore.Qt.AlignCenter)
        pLayout.setContentsMargins(0, 0, 0, 0)
        widget.setLayout(pLayout)
        return widget

    # Метод создания рб на виджете
    def create_radiobutton(self):
        widget = QtWidgets.QWidget()
        rb = RadioButton()
        pLayout = QtWidgets.QHBoxLayout(widget)
        pLayout.addWidget(rb)
        pLayout.setAlignment(QtCore.Qt.AlignCenter)
        pLayout.setContentsMargins(0, 0, 0, 0)
        widget.setLayout(pLayout)
        return widget, rb

    # Метод, обнуляющий собранную конфигурацию
    def reset_all_config(self):
        self.reset_radiobutton(self.tableConfVideo)
        self.reset_radiobutton(self.tableConfProc)
        self.reset_radiobutton(self.tableConfMother)
        self.reset_radiobutton(self.tableConfCool)
        self.reset_radiobutton(self.tableConfRam)
        self.reset_radiobutton(self.tableConfDisk)
        self.reset_radiobutton(self.tableConfPower)
        self.reset_radiobutton(self.tableConfBody)

    # Метод, обнуляющий RadioButton в таблице
    def reset_radiobutton(self, table):
        button_group = self.dict_button_group[table.objectName()]
        button_group.setExclusive(False)
        for i in range(table.rowCount()):
            widget = table.cellWidget(i, 0)
            if widget is not None:
                rad_but = widget.findChild(RadioButton)
                if rad_but is not None and rad_but.isChecked():
                    rad_but.setChecked(False)
        table.clearSelection()
        button_group.setExclusive(True)
        self.clear_cart(table)

    #  Метод очистки корзины (таблицы) предпросмотра заказа
    def clear_cart(self, table):
        for i in range(self.table_config.rowCount()):  # Проход по корзине и удаление строки по таблице
            if self.table_config.item(i, 0) is not None and self.table_config.item(i, 0).text() == str(table):
                self.table_config.removeRow(i)
        self.progressBar.setValue(self.table_config.rowCount())  # обновление прогрессбара

    # Метод вставки в таблицы конфигуратора рб-шек
    def insert_rb(self, table):
        row_count = table.rowCount()

        button_group = QtWidgets.QButtonGroup(self)
        button_group.setExclusive(True)

        for i in range(row_count):
            widget, radio = self.create_radiobutton()
            radio.toggled.connect(
                lambda ch, row=i: self.current_pos(ch, row, table))
            # коннект на фильтрацию в других таблицах
            table.setCellWidget(i, 0, widget)
            button_group.addButton(radio)
            button_group.setId(radio, i)
        self.dict_button_group[table.objectName()] = button_group

    # Метод вставки в таблицу склада рб-шек (без коннекторов на фильтрацию, только визуал)
    def insert_rb_sklad(self, table):
        row_count = table.rowCount()

        button_group = QtWidgets.QButtonGroup(self)
        button_group.setExclusive(True)

        for i in range(row_count):
            widget, radio = self.create_radiobutton()
            radio.toggled.connect(
                lambda ch, row=i: self.current_pos_sklad(ch, row, table))
            table.setCellWidget(i, 0, widget)
            button_group.addButton(radio)
            button_group.setId(radio, i)
        self.dict_button_group[table.objectName()] = button_group

    def cell_row(self, row, column, table):
        # print(f'\n row={row}; column={column}')
        button_group = self.dict_button_group[table.objectName()]
        rb = button_group.button(row)
        rb.click()

    def current_pos(self, ch, row, table):
        # print(f' row = {row} -- {ch}')
        if ch:
            table.selectRow(row)
            self.fill_cart(table)

    def current_pos_sklad(self, ch, row, table):
        # print(f' row = {row} -- {ch}')
        if ch:
            table.selectRow(row)

    # Метод заполнения корзины выбранных комплектующих (принимает таблицу, из которой был вызван, имя и цену)
    def fill_cart(self, table):
        name = table.item(table.currentRow(), 2).text()  # Далее - заменить на столбец с именем !!!
        price = table.item(table.currentRow(), 3).text()  # Далее - заменить на столбец с ценой!!!
        row_count = self.table_config.rowCount()
        insert_row = self.check_cart(table)
        if insert_row == -1:  # если не найдена запись
            self.table_config.setRowCount(row_count + 1)
            self.table_config.setItem(row_count, 0, QTableWidgetItem(str(table)))
            self.table_config.setItem(row_count, 1, QTableWidgetItem(name))
            self.table_config.setItem(row_count, 2, QTableWidgetItem(price))
            self.table_config.setItem(row_count, 3, QTableWidgetItem("₽"))
            # item2.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight) Выравнивание для корзины
        else:
            # дублируется вставка ид таблицы для случая пустой корзины (вставить на 0 место)
            self.table_config.setItem(insert_row, 0, QTableWidgetItem(str(table)))
            self.table_config.setItem(insert_row, 1, QTableWidgetItem(name))
            self.table_config.setItem(insert_row, 2, QTableWidgetItem(price))
            self.table_config.setItem(insert_row, 3, QTableWidgetItem("₽"))
        self.progressBar.setValue(self.table_config.rowCount())  # обновление прогрессбара

    # Метод проверки корзины на наличие выбранного типа комплектуюшего (вызывается из .fill_cart)
    def check_cart(self, table):
        if self.table_config.rowCount() == 0:  # если корзина пуста - вернуть -1
            return -1
        else:
            for i in range(self.table_config.rowCount()):
                if self.table_config.item(i, 0).text() == str(table):
                    return i
            return -1  # если не найдено записей - вернуть -1


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
