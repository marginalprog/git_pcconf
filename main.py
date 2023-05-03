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
            dialog = DialogOk("Ошибка", "Введите наименование поставщика")
            dialog.show()
            if dialog.exec():
                pass
        elif proizv_name.casefold() in str(dict_proizv.values()).casefold():
            dialog = DialogOk("Ошибка", "Данный поставщик уже есть в базе данных")
            dialog.show()
            if dialog.exec():
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
                        conn.commit()
                        mainwindow.load_proizv_videocard()  # Загрузка обновлённой таблицы из БД
                    case "Производитель процессоров":
                        cur.callproc('insert_proizv_processor', [proizv_name])
                        conn.commit()
                        mainwindow.load_proizv_processor()  # Загрузка обновлённой таблицы из БД
                    case "Производитель мат. плат":
                        cur.callproc('insert_proizv_motherboard', [proizv_name])
                        conn.commit()
                        mainwindow.load_proizv_motherboard()  # Загрузка обновлённой таблицы из БД

            except (Exception, psycopg2.DatabaseError) as error:
                dialog = DialogOk("Ошибка", error)
                dialog.show()

            finally:
                if conn:
                    cur.close()
                    conn.close()
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
        # Словари для хранения пар ключ(id производителя): наименование производителя
        self.dict_proizv_video_name = {}
        self.dict_proizv_proc_name = {}
        self.dict_proizv_mother_name = {}
        self.dict_proizv_cool_name = {}
        self.dict_proizv_ram_name = {}
        self.dict_proizv_hard_name = {}
        self.dict_proizv_power_name = {}
        self.dict_proizv_body_name = {}

        # Словари для хранения пар ключ(id видеокарты): производитель(название)
        self.dict_video_proizv = {}
        self.dict_proc_proizv = {}
        self.dict_mother_proizv = {}
        self.dict_cool_proizv = {}
        self.dict_ram_proizv = {}
        self.dict_disk_proizv = {}
        self.dict_power_proizv = {}
        self.dict_body_proizv = {}
        # self.dict_proizv_configs = {} ??
        # Словари для хранения пар ключ(id компл.): количество
        self.dict_video_kol = {}
        self.dict_proc_kol = {}
        self.dict_mother_kol = {}
        self.dict_cool_kol = {}
        self.dict_ram_kol = {}
        self.dict_disk_kol = {}
        self.dict_power_kol = {}
        self.dict_body_kol = {}
        # Словари для хранения пар ключ(id компл.): наименование
        self.dict_video_name = {}
        self.dict_proc_name = {}
        self.dict_mother_name = {}
        self.dict_cool_name = {}
        self.dict_ram_name = {}
        self.dict_disk_name = {}
        self.dict_power_name = {}
        self.dict_body_name = {}

        # Словарь для хранения пар ключ(таблица): выбранное комплектующее
        self.dict_current = {}

        self.query_sklad = ""
        self.query_conf = ""

        self.price_configuration = []

        self.dict_button_group = {}  # Словарь для хранения групп RB и таблиц, в которых они находятся
        self.rbCabinet.clicked.connect(self.open_cabinet)
        self.lvCabinetMenu.setCurrentRow(0)
        self.lvCabinetMenu.clicked.connect(self.menu_cabinet)
        self.tableOrders.resizeColumnsToContents()
        # =============================== Надстройки вкладки "Склад"================================
        self.btnResetSklad.clicked.connect(lambda: self.reset_radiobutton(self.tableSklad))
        self.tableSklad.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
        self.toolBoxNavigation.currentChanged.connect(lambda index: self.load_sklad(index))
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

        # По нажатии на кнопку наличия запускается метод, отправляющий в
        self.rbSklad.toggled.connect(
            lambda have: self.rb_click_having_sklad(have, self.toolBoxNavigation.currentIndex()))

        self.rbConf.toggled.connect(
            lambda have: self.rb_click_having_conf(have))

        self.load_proizv_videocard()
        self.load_proizv_processor()
        self.load_proizv_motherboard()
        self.load_sklad(0)  # Первоначальная загрузка всех видеокарт из бд
        # =================================Окна фильтрации комплектующих на складе=========================
        self.vidSkladFilter = filters.VideoFilter(0, self)  # Создаётся отдельный экземпляр для сохранения внесённых д-х
        self.rbSklad.toggled.connect(self.create_sklad_filter)  # Пересоздание экземпляра, если индикатор нажат
        self.btnSkladFilter.clicked.connect(lambda: self.vidSkladFilter.show())

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
                                                         self.dict_proizv_video_name).show())
        self.btnNewProcProizv.clicked.connect(lambda:
                                              AddProizv(self, "Производитель процессоров",
                                                        self.dict_proizv_proc_name).show())
        self.btnNewMotherProizv.clicked.connect(lambda:
                                                AddProizv(self, "Производитель мат. плат",
                                                          self.dict_proizv_mother_name).show())
        # Кнопка обновления состояния договора
        self.btnCngVideoProizv.clicked.connect(lambda: self.change_proizv(self.tableVideoProizv))
        self.btnCngProcProizv.clicked.connect(lambda: self.change_proizv(self.tableProcProizv))
        self.btnCngMotherProizv.clicked.connect(lambda: self.change_proizv(self.tableMotherProizv))

        self.tableVideoProizv.cellClicked.connect(
            lambda row, column, table=self.tableVideoProizv:
            self.cell_row(row, column, table))
        self.tableProcProizv.cellClicked.connect(
            lambda row, column, table=self.tableProcProizv:
            self.cell_row(row, column, table))
        self.tableMotherProizv.cellClicked.connect(
            lambda row, column, table=self.tableMotherProizv:
            self.cell_row(row, column, table))
        # x8 x8 x8 x8

        self.tableSklad.cellClicked.connect(
            lambda row, column, table=self.tableSklad:
            self.cell_row_without_conf(row, column, table))

        # ==========================================================================================

        # =========================== Надстройки вкладки "Конфигуратор"=============================
        self.btnResetVideo.clicked.connect(lambda: self.click_reset_radiobutton(self.tableConfVideo))
        self.btnResetProc.clicked.connect(lambda: self.click_reset_radiobutton(self.tableConfProc))
        self.btnResetMother.clicked.connect(lambda: self.click_reset_radiobutton(self.tableConfMother))
        self.btnResetCool.clicked.connect(lambda: self.click_reset_radiobutton(self.tableConfCool))
        self.btnResetDisk.clicked.connect(lambda: self.click_reset_radiobutton(self.tableConfDisk))
        self.btnResetBody.clicked.connect(lambda: self.click_reset_radiobutton(self.tableConfBody))
        self.btnResetRam.clicked.connect(lambda: self.click_reset_radiobutton(self.tableConfRam))
        self.btnResetPower.clicked.connect(lambda: self.click_reset_radiobutton(self.tableConfPower))
        self.treeWidget.itemClicked.connect(lambda: self.treeNavigation())
        # ------------------------Заполнение таблиц при инициализации-----------------------

        self.row_selected = None
        for i in range(3):
            self.load_conf(i)
        self.fill_all_tabs_conf()
        # -----------------------------------------------------------------------------

        # ---------------------Кнопки с помощью--------------------------------
        self.vHelp = helping.VideoHelp()
        self.btnVidHelp.clicked.connect(lambda: self.vHelp.show())

        # ---------------------------------------------------------------------

        # ---------------------Кнопки с фильтрами------------------------------
        self.vidConfFilter = filters.VideoFilter(1, self)  # Создаётся отдельный экземпляр для сохранения внесённых д-х
        self.rbConf.toggled.connect(self.create_conf_filter)  # Пересоздание экземпляра, если индикатор нажат
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

        self.tabWidgetVideo.tabBarClicked.connect(lambda index: self.click_tab_conf(index, self.tabWidgetVideo))
        self.tabWidgetProc.tabBarClicked.connect(lambda index: self.click_tab_conf(index, self.tabWidgetProc))
        self.tabWidgetMother.tabBarClicked.connect(lambda index: self.click_tab_conf(index, self.tabWidgetMother))

    def open_cabinet(self):
        if self.rbCabinet.isChecked():
            self.stackedWidget.setCurrentIndex(1)
            self.line_11.hide()  # Линия-сепаратор вкладок склад\конфигуратор (элемент дизайна)
            self.rbCabinet.setText("К сборке")
        else:
            self.stackedWidget.setCurrentIndex(0)
            self.line_11.show()
            self.rbCabinet.setText("Кабинет")

    def menu_cabinet(self):
        print(self.lvCabinetMenu.currentRow())
        self.tabWidgetCabinet.setCurrentIndex(self.lvCabinetMenu.currentRow())

    def create_sklad_filter(self):
        self.vidSkladFilter = filters.VideoFilter(0, self)
        # self.procSkladFilter = filters.ProcFilter(0, self) и т.д.

    def create_conf_filter(self):
        self.vidConfFilter = filters.VideoFilter(1, self)
        # self.procSkladFilter = filters.ProcFilter(1, self) и т.д.

    # Метод загрузки таблицы производителей видеокарт из БД
    def load_proizv_videocard(self):
        self.tableVideoProizv.clearSelection()
        self.tableVideoProizv.clear()
        self.tableVideoProizv.setRowCount(0)
        self.dict_proizv_video_name.clear()
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
                self.dict_proizv_video_name[row[0]] = row[2]  # Сохраняем id производителя и его имя
                self.tableVideoProizv.setItem(row_count, 3, QtWidgets.QTableWidgetItem(row[2]))
                row_count += 1

        except (Exception, psycopg2.DatabaseError) as error:
            dialog = DialogOk("Ошибка", error)
            dialog.show()

        finally:
            if conn:
                cur.close()
                conn.close()
            self.insert_existence_proizv(self.tableVideoProizv)
            self.insert_rb_sklad(self.tableVideoProizv)  # Загрузка rb для визаулизции

    def load_proizv_processor(self):
        self.tableProcProizv.clearSelection()
        self.tableProcProizv.clear()
        self.tableProcProizv.setRowCount(0)
        self.dict_proizv_proc_name.clear()
        conn = None
        cur = None
        try:
            conn = psycopg2.connect(database="confPc",
                                    user="postgres",
                                    password="2001",
                                    host="localhost",
                                    port="5432")
            cur = conn.cursor()
            cur.callproc("get_proizv_processor")
            row_count = 0
            for row in cur:
                self.tableProcProizv.setRowCount(row_count + 1)
                # 0 столбец - radiobutton
                # 1 столбец - индикатор состояния договора
                self.tableProcProizv.setItem(row_count, 2, QtWidgets.QTableWidgetItem(str(row[1])))
                self.dict_proizv_proc_name[row[0]] = row[2]  # Сохраняем id производителя и его имя
                self.tableProcProizv.setItem(row_count, 3, QtWidgets.QTableWidgetItem(row[2]))
                row_count += 1

        except (Exception, psycopg2.DatabaseError) as error:
            dialog = DialogOk("Ошибка", error)
            dialog.show()

        finally:
            if conn:
                cur.close()
                conn.close()
            self.insert_existence_proizv(self.tableProcProizv)
            self.insert_rb_sklad(self.tableProcProizv)  # Загрузка rb для визаулизции

    def load_proizv_motherboard(self):
        self.tableMotherProizv.clearSelection()
        self.tableMotherProizv.clear()
        self.tableMotherProizv.setRowCount(0)
        self.dict_proizv_mother_name.clear()
        conn = None
        cur = None
        try:
            conn = psycopg2.connect(database="confPc",
                                    user="postgres",
                                    password="2001",
                                    host="localhost",
                                    port="5432")
            cur = conn.cursor()
            cur.callproc("get_proizv_motherboard")
            row_count = 0
            for row in cur:
                self.tableMotherProizv.setRowCount(row_count + 1)
                # 0 столбец - radiobutton
                # 1 столбец - индикатор состояния договора
                self.tableMotherProizv.setItem(row_count, 2, QtWidgets.QTableWidgetItem(str(row[1])))
                self.dict_proizv_mother_name[row[0]] = row[2]  # Сохраняем id производителя и его имя
                self.tableMotherProizv.setItem(row_count, 3, QtWidgets.QTableWidgetItem(row[2]))
                row_count += 1

        except (Exception, psycopg2.DatabaseError) as error:
            dialog = DialogOk("Ошибка", error)
            dialog.show()

        finally:
            if conn:
                cur.close()
                conn.close()
            self.insert_existence_proizv(self.tableMotherProizv)
            self.insert_rb_sklad(self.tableMotherProizv)  # Загрузка rb для визаулизции

    # изменение состояния в таблице поставщика
    def change_proizv(self, table):
        if table.currentRow() == -1:
            err = "Выберите поставщика для изменения"
            dialog = DialogOk("Ошибка", err)
            dialog.show()
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
                att = "Вы действительно хотите изменить договор поставок?"
                dialog = AcceptionWin("Подтвердите действие", att)
                dialog.show()
                if dialog.exec():
                    match table:
                        case self.tableVideoProizv:  # Перезаписываем в БД и обновляем таблицу
                            if table.item(table.currentRow(), 2).text() == "True":
                                cur.callproc('update_video_dogovor', [False, table.item(table.currentRow(),
                                                                                        3).text()])
                            else:
                                cur.callproc('update_video_dogovor', [True, table.item(table.currentRow(),
                                                                                       3).text()])
                            conn.commit()
                            self.load_proizv_videocard()

                        case self.tableProcProizv:  # Перезаписываем в БД и обновляем таблицу
                            if table.item(table.currentRow(), 2).text() == "True":
                                cur.callproc('update_proc_dogovor', [False, table.item(table.currentRow(),
                                                                                       3).text()])
                            else:
                                cur.callproc('update_proc_dogovor', [True, table.item(table.currentRow(),
                                                                                      3).text()])
                            conn.commit()
                            self.load_proizv_processor()
                        case self.tableMotherProizv:  # Перезаписываем в БД и обновляем таблицу
                            if table.item(table.currentRow(), 2).text() == "True":
                                cur.callproc('update_mother_dogovor', [False, table.item(table.currentRow(),
                                                                                         3).text()])
                            else:
                                cur.callproc('update_mother_dogovor', [True, table.item(table.currentRow(),
                                                                                        3).text()])
                            conn.commit()
                            self.load_proizv_motherboard()
                self.reset_radiobutton(table)

            except (Exception, psycopg2.DatabaseError) as error:
                dialog = DialogOk("Ошибка", error)
                dialog.show()

            finally:
                if conn:
                    cur.close()
                    conn.close()

    # Метод загрузки всех видеокарт из БД с заполнением словарей
    # Вызывать после каждого обновления записей, а также при запуске#################################################
    def load_sklad(self, page):
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
                    if self.rbSklad.isChecked():
                        cur.callproc("get_having_videocard")  # Получаем данные о имеющихся видеокартах
                        self.fill_table_sklad(page, cur)  # Заполняем таблицу
                        self.fill_tabs_sklad(page, self.tabWidgetSklad)
                    else:
                        self.dict_video_kol.clear()
                        self.dict_video_proizv.clear()
                        self.dict_video_name.clear()
                        cur.callproc("get_all_videocard")  # Получаем данные о всех видеокартах
                        self.fill_table_sklad(page, cur)  # Заполняем таблицу
                        self.fill_tabs_sklad(page, self.tabWidgetSklad)
                        cur.callproc("get_all_videocard")
                        for row in cur:  # Заполняем словари данными о видеокартах
                            self.dict_video_kol[row[2]] = row[1]
                            self.dict_video_proizv[row[2]] = row[3]
                            self.dict_video_name[row[2]] = row[4]
                case 1:
                    if self.rbSklad.isChecked():
                        cur.callproc("get_having_processor")  # Получаем данные о имеющихся видеокартах
                        self.fill_table_sklad(page, cur)  # Заполняем таблицу
                        self.fill_tabs_sklad(page, self.tabWidgetSklad)
                    else:
                        self.dict_proc_kol.clear()
                        self.dict_proc_proizv.clear()
                        self.dict_proc_name.clear()
                        cur.callproc("get_all_processor")  # Получаем данные о всех видеокартах
                        self.fill_table_sklad(page, cur)  # Заполняем таблицу
                        self.fill_tabs_sklad(page, self.tabWidgetSklad)
                        cur.callproc("get_all_processor")
                        for row in cur:  # Заполняем словари данными о видеокартах
                            self.dict_proc_kol[row[2]] = row[1]
                            self.dict_proc_proizv[row[2]] = row[3]
                            self.dict_proc_name[row[2]] = row[4]
                case 2:
                    if self.rbSklad.isChecked():
                        cur.callproc("get_having_motherboard")  # Получаем данные о имеющихся мат.платах
                        self.fill_table_sklad(page, cur)  # Заполняем таблицу
                        self.fill_tabs_sklad(page, self.tabWidgetSklad)
                    else:
                        self.dict_video_kol.clear()
                        self.dict_video_proizv.clear()
                        self.dict_video_name.clear()
                        cur.callproc("get_all_motherboard")  # Получаем данные о всех видеокартах
                        self.fill_table_sklad(page, cur)  # Заполняем таблицу
                        self.fill_tabs_sklad(page, self.tabWidgetSklad)
                        cur.callproc("get_all_motherboard")
                        for row in cur:  # Заполняем словари данными о видеокартах
                            self.dict_mother_kol[row[2]] = row[1]
                            self.dict_mother_proizv[row[2]] = row[3]
                            self.dict_mother_name[row[2]] = row[4]
        except (Exception, psycopg2.DatabaseError) as error:
            dialog = DialogOk("Ошибка", str(error))
            dialog.show()

        finally:
            if conn:
                cur.close()
                conn.close()

    # Метод заполнения полей таблицы склада по фильтрующему запросу из БД
    def fill_table_sklad(self, page, cur):
        index_row = -1
        """if self.tableSklad.currentRow() != -1:  # Если была выбрана строка, то сохраняем её номер
            index_row = self.tableSklad.currentRow()"""
        self.tableSklad.clear()
        self.tableSklad.clearSelection()
        self.tableSklad.setRowCount(0)
        self.tableSklad.setSortingEnabled(False)
        row_count = 0
        match page:
            case 0:  # Заполнение таблицы видеокартами

                self.tableSklad.setColumnCount(18)  # Число столбцов в видеокарте
                self.tableSklad.setHorizontalHeaderLabels(["", "", "Кол-во",
                                                           "Производитель", "Название", "Игровая", "Произв. чипа",
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
                    if row[5]:
                        self.tableSklad.setItem(row_count, 5, QtWidgets.QTableWidgetItem("Да"))
                    else:
                        self.tableSklad.setItem(row_count, 5, QtWidgets.QTableWidgetItem("Нет"))
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
                    self.tableSklad.setItem(row_count, 17, QtWidgets.QTableWidgetItem(str(row[17])))
                    # item2.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
                    self.insert_rb_sklad(self.tableSklad)
                    row_count += 1
            case 1:
                self.tableSklad.setColumnCount(17)  # Число столбцов в процессоре
                self.tableSklad.setHorizontalHeaderLabels(["", "", "Кол-во",
                                                           "Производитель", "Название", "Игровой", "Серия",
                                                           "Сокет", "Ядро", "Кол-во ядер", "Кэш",
                                                           "Частота процессора", "Тех. проц.", "Шина",
                                                           "Граф. процессор", "TDP", "Цена"])
                for row in cur:
                    self.tableSklad.setRowCount(row_count + 1)
                    self.insert_existence_complect(self.tableSklad, row_count, row[1])
                    self.tableSklad.setItem(row_count, 2, QtWidgets.QTableWidgetItem(str(row[0])))
                    self.tableSklad.setItem(row_count, 3, QtWidgets.QTableWidgetItem(str(row[3])))
                    self.tableSklad.setItem(row_count, 4, QtWidgets.QTableWidgetItem(str(row[4])))
                    if row[5]:
                        self.tableSklad.setItem(row_count, 5, QtWidgets.QTableWidgetItem("Да"))
                    else:
                        self.tableSklad.setItem(row_count, 5, QtWidgets.QTableWidgetItem("Нет"))
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
                    row_count += 1
            case 2:
                self.tableSklad.setColumnCount(16)  # Число столбцов в видеокарте
                self.tableSklad.setHorizontalHeaderLabels(["", "", "Кол-во",
                                                           "Производитель", "Название", "Игровой", "Cокет",
                                                           "Чипсет", "Формфактор", "Тип ОЗУ", "Слоты ОЗУ",
                                                           "Макс. объём ОЗУ", "Макс. частота ОЗУ", "Слоты М2",
                                                           "Разъёмы SATA", "Цена"])
                for row in cur:
                    self.tableSklad.setRowCount(row_count + 1)
                    self.insert_existence_complect(self.tableSklad, row_count, row[1])
                    self.tableSklad.setItem(row_count, 2, QtWidgets.QTableWidgetItem(str(row[0])))
                    self.tableSklad.setItem(row_count, 3, QtWidgets.QTableWidgetItem(str(row[3])))
                    self.tableSklad.setItem(row_count, 4, QtWidgets.QTableWidgetItem(str(row[4])))
                    if row[5]:
                        self.tableSklad.setItem(row_count, 5, QtWidgets.QTableWidgetItem("Да"))
                    else:
                        self.tableSklad.setItem(row_count, 5, QtWidgets.QTableWidgetItem("Нет"))
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
                    row_count += 1
        self.insert_rb_sklad(self.tableSklad)
        self.tableSklad.setSortingEnabled(True)
        """if index_row < self.tableSklad.rowCount() and index_row != -1:
            self.cell_row(index_row, 0, self.tableSklad)  # Отмечаем строку кнопкой и выделением
            self.tableSklad.selectRow(index_row)"""
        self.tableSklad.resizeColumnsToContents()

    # Метод загрузки всех комплектующих с БД в страницу конфигуратора
    # Вызывать после каждого обновления записей, а также при запуске##################################################
    def load_conf(self, page):
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
                    cur.callproc("get_all_videocard")  # Получаем данные о всех видеокартах
                    self.fill_table_conf(page, cur)  # Заполняем таблицу
                case 1:
                    cur.callproc("get_all_processor")  # Получаем данные о всех процессорах
                    self.fill_table_conf(page, cur)  # Заполняем таблицу
                case 2:
                    cur.callproc("get_all_motherboard")  # Получаем данные о всех процессорах
                    self.fill_table_conf(page, cur)  # Заполняем таблицу

        except (Exception, psycopg2.DatabaseError) as error:
            dialog = DialogOk("Ошибка", str(error))
            dialog.show()

        finally:
            if conn:
                cur.close()
                conn.close()

    def check_radiobutton(self, table, bd_column):
        if self.tableConfVideo.currentRow() != -1:
            return self.tableConfVideo.currentRow()

    # Метод заполнения таблиц во вкладке конфигуратора
    def fill_table_conf(self, type_, cur):
        row_count = 0
        match type_:
            case 0:  # Заполнение таблицы видеокартами
                self.tableConfVideo.clear()
                self.tableConfVideo.clearSelection()
                self.tableConfVideo.setRowCount(0)
                self.tableConfVideo.setColumnCount(13)  # Число столбцов в видеокарте конфигуратора
                for row in cur:
                    self.tableConfVideo.setRowCount(row_count + 1)
                    self.insert_existence_complect(self.tableConfVideo, row_count, row[1])
                    self.tableConfVideo.setItem(row_count, 2, QtWidgets.QTableWidgetItem(str(row[4])))
                    # self.tableConfVideo.setItem(row_count, 3, QtWidgets.QTableWidgetItem(str(row[5])))
                    self.tableConfVideo.setItem(row_count, 3, QtWidgets.QTableWidgetItem(str(row[6])))
                    self.tableConfVideo.setItem(row_count, 4, QtWidgets.QTableWidgetItem(str(row[7])))
                    self.tableConfVideo.setItem(row_count, 5, QtWidgets.QTableWidgetItem(str(row[8])))
                    self.tableConfVideo.setItem(row_count, 6, QtWidgets.QTableWidgetItem(str(row[9])))
                    self.tableConfVideo.setItem(row_count, 7, QtWidgets.QTableWidgetItem(str(row[10])))
                    self.tableConfVideo.setItem(row_count, 8, QtWidgets.QTableWidgetItem(str(row[11])))
                    self.tableConfVideo.setItem(row_count, 9, QtWidgets.QTableWidgetItem(str(row[14])))
                    self.tableConfVideo.setItem(row_count, 10, QtWidgets.QTableWidgetItem(str(row[15])))
                    self.tableConfVideo.setItem(row_count, 11, QtWidgets.QTableWidgetItem(str(row[16])))
                    self.tableConfVideo.setItem(row_count, 12, QtWidgets.QTableWidgetItem(str(row[17])))
                    row_count += 1
                self.insert_rb(self.tableConfVideo)
                self.tableConfVideo.resizeColumnsToContents()
            case 1:  # Заполнение таблицы конфигуратора процессорами
                self.tableConfProc.clear()
                self.tableConfProc.clearSelection()
                self.tableConfProc.setRowCount(0)
                self.tableConfProc.setColumnCount(10)  # Число столбцов в процессорах конфигуратора
                for row in cur:
                    self.tableConfProc.setRowCount(row_count + 1)
                    self.insert_existence_complect(self.tableConfProc, row_count, row[1])
                    self.tableConfProc.setItem(row_count, 2, QtWidgets.QTableWidgetItem(str(row[4])))
                    self.tableConfProc.setItem(row_count, 3, QtWidgets.QTableWidgetItem(str(row[7])))
                    self.tableConfProc.setItem(row_count, 4, QtWidgets.QTableWidgetItem(str(row[8])))
                    self.tableConfProc.setItem(row_count, 5, QtWidgets.QTableWidgetItem(str(row[9])))

                    self.tableConfProc.setItem(row_count, 6, QtWidgets.QTableWidgetItem(str(row[11])))

                    self.tableConfProc.setItem(row_count, 7, QtWidgets.QTableWidgetItem(str(row[13])))

                    self.tableConfProc.setItem(row_count, 8, QtWidgets.QTableWidgetItem(str(row[15])))
                    self.tableConfProc.setItem(row_count, 9, QtWidgets.QTableWidgetItem(str(row[16])))
                    row_count += 1
                self.insert_rb(self.tableConfProc)
                self.tableConfProc.resizeColumnsToContents()
            case 2:  # Заполнение таблицы конфигуратора процессорами
                self.tableConfMother.clear()
                self.tableConfMother.clearSelection()
                self.tableConfMother.setRowCount(0)
                self.tableConfMother.setColumnCount(13)  # Число столбцов в процессорах конфигуратора
                for row in cur:
                    self.tableConfMother.setRowCount(row_count + 1)
                    self.insert_existence_complect(self.tableConfMother, row_count, row[1])
                    self.tableConfMother.setItem(row_count, 2, QtWidgets.QTableWidgetItem(str(row[4])))
                    self.tableConfMother.setItem(row_count, 3, QtWidgets.QTableWidgetItem(str(row[6])))
                    self.tableConfMother.setItem(row_count, 4, QtWidgets.QTableWidgetItem(str(row[7])))
                    self.tableConfMother.setItem(row_count, 5, QtWidgets.QTableWidgetItem(str(row[8])))
                    self.tableConfMother.setItem(row_count, 6, QtWidgets.QTableWidgetItem(str(row[9])))
                    self.tableConfMother.setItem(row_count, 7, QtWidgets.QTableWidgetItem(str(row[10])))
                    self.tableConfMother.setItem(row_count, 8, QtWidgets.QTableWidgetItem(str(row[11])))
                    self.tableConfMother.setItem(row_count, 9, QtWidgets.QTableWidgetItem(str(row[12])))
                    self.tableConfMother.setItem(row_count, 10, QtWidgets.QTableWidgetItem(str(row[13])))
                    self.tableConfMother.setItem(row_count, 11, QtWidgets.QTableWidgetItem(str(row[14])))
                    self.tableConfMother.setItem(row_count, 12, QtWidgets.QTableWidgetItem(str(row[15])))
                    row_count += 1
                self.insert_rb(self.tableConfMother)
                self.tableConfMother.resizeColumnsToContents()

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
        if table.rowCount() > 0:
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
            err = "Выберите комплектующее (строку) для создания заказа"
            return err
        else:
            for i in range(2, count_col):
                data_row.append(self.tableSklad.item(cur_row, i).text())
            return data_row

    # Чтение выбранной строки в таблце для передачи в перезаказ
    def current_conf(self, table):
        data_row = []
        column_count = table.columnCount()
        current_row = table.currentRow()
        for i in range(2, column_count):
            data_row.append(table.item(current_row, i).text())
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
        :return: Список всех производителей; список производителей, с которыми есть договор о поставках
        """
        list_all_proizvoditel = []
        list_exist_proizvoditel = []
        for i in range(table.rowCount()):
            list_all_proizvoditel.append(table.item(i, 3).text())

        for i in range(table.rowCount()):
            if table.item(i, 2).text() == "True":
                list_exist_proizvoditel.append(table.item(i, 3).text())
        return list_all_proizvoditel, list_exist_proizvoditel

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
                list_all_pr, list_exist_pr = self.get_list_proizvoditel(self.tableVideoProizv)
                if new_bool:  # Если True - добавляем новую запись: открываем пустое окно
                    self.tableSklad.clearSelection()
                    self.reset_radiobutton(self.tableSklad)
                    if self.tableVideoProizv.rowCount() == 0:  # Если нет производителей для добавления карты (!=заказ)
                        dialog = DialogOk("Ошибка", "Нет производителей, чьи видеокарты можно добавить")
                        dialog.show()
                        if dialog.exec():
                            pass
                    else:  # Если таблица производителей видеокарты непустая
                        self.win_add_change = adding.AddChangeVideoWindow(self, new_bool, list_all_pr,
                                                                          self.dict_proizv_video_name,
                                                                          self.dict_video_name)
                        self.block_lineedit(self.win_add_change.leKol, "")
                        self.win_add_change.show()
                else:  # Есил False - изменяем выбранную запись
                    if type(row) is str:  # Если пришел не кортеж, а строка(ошибка) - вывод окна с ошибкой
                        dialog = DialogOk("Ошибка", row)
                        dialog.show()
                        if dialog.exec():
                            pass
                    else:  # Если пришел список - заполняем окно.
                        if row[1] not in list_exist_pr:  # Если пр-ль выбранной видеокарты с False договором
                            dialog = DialogOk("Ошибка", "У данного производителя нет договора о поставках")
                            dialog.show()
                            if dialog.exec():
                                pass
                        else:
                            self.win_add_change = adding.AddChangeVideoWindow(self, new_bool, row[1],
                                                                              self.dict_proizv_video_name,
                                                                              self.dict_video_name)
                            self.block_combobox(self.win_add_change.cbProizv, row[1])
                            self.block_lineedit(self.win_add_change.leFullName, row[2])
                            self.block_combobox(self.win_add_change.cbGaming, row[3])
                            self.block_combobox(self.win_add_change.cbChipCreator, row[4])
                            self.block_lineedit(self.win_add_change.leChipName, row[5])
                            self.block_lineedit(self.win_add_change.leVolume, row[6])
                            self.block_lineedit(self.win_add_change.leType, row[7])
                            self.block_lineedit(self.win_add_change.leFreq, row[8])
                            self.block_lineedit(self.win_add_change.leBus, row[9])
                            self.block_combobox(self.win_add_change.cbInterface, row[10])
                            self.block_combobox(self.win_add_change.cbMonitor, row[11])
                            self.block_combobox(self.win_add_change.cbResolution, row[12])
                            self.block_lineedit(self.win_add_change.leTdp, row[13])
                            self.block_lineedit(self.win_add_change.leLength, row[14])
                            self.block_lineedit(self.win_add_change.lePrice, row[15])
                            self.win_add_change.show()
            case 1:
                list_all_pr, list_exist_pr = self.get_list_proizvoditel(self.tableProcProizv)
                if new_bool:  # Если True - добавляем новую запись: открываем пустое окно
                    self.tableSklad.clearSelection()
                    self.reset_radiobutton(self.tableSklad)
                    if self.tableProcProizv.rowCount() == 0:  # Если нет производителей для добавления проца (!=заказ)
                        dialog = DialogOk("Ошибка", "Нет производителей, чьи процессоры можно добавить")
                        dialog.show()
                        if dialog.exec():
                            pass
                    else:  # Если таблица производителей процессоров непустая
                        self.win_add_change = adding.AddChangeProcWindow(self, new_bool, list_all_pr,
                                                                         self.dict_proizv_proc_name,
                                                                         self.dict_proc_name)
                        self.block_lineedit(self.win_add_change.leKol, "")
                        self.win_add_change.show()
                else:  # Есил False - изменяем выбранную запись
                    if type(row) is str:  # Если пришел не кортеж, а строка(ошибка) - вывод окна с ошибкой
                        dialog = DialogOk("Ошибка", row)
                        dialog.show()
                        if dialog.exec():
                            pass
                    else:  # Если пришел список - заполняем окно.
                        if row[1] not in list_exist_pr:  # Если пр-ль выбранного процессора с False договором
                            dialog = DialogOk("Ошибка", "У данного производителя нет договора о поставках")
                            dialog.show()
                            if dialog.exec():
                                pass
                        else:
                            self.win_add_change = adding.AddChangeProcWindow(self, new_bool, row[1],
                                                                             self.dict_proizv_proc_name,
                                                                             self.dict_proc_name)
                            self.block_combobox(self.win_add_change.cbProizv, row[1])
                            self.block_lineedit(self.win_add_change.leFullName, row[2])
                            self.block_combobox(self.win_add_change.cbGaming, row[3])
                            self.block_lineedit(self.win_add_change.leSeries, row[4])
                            self.block_lineedit(self.win_add_change.leSocket, row[5])
                            self.block_lineedit(self.win_add_change.leCore, row[6])
                            self.block_lineedit(self.win_add_change.leNcores, row[7])
                            self.block_lineedit(self.win_add_change.leCache, row[8])
                            self.block_lineedit(self.win_add_change.leFreq, row[9])
                            self.block_lineedit(self.win_add_change.leTechproc, row[10])
                            self.block_lineedit(self.win_add_change.leRamFreq, row[11])
                            self.block_lineedit(self.win_add_change.leGraphics, row[12])
                            self.block_lineedit(self.win_add_change.leTdp, row[13])
                            self.block_lineedit(self.win_add_change.lePrice, row[14])
                            self.win_add_change.show()
            case 2:
                list_all_pr, list_exist_pr = self.get_list_proizvoditel(self.tableMotherProizv)
                if new_bool:  # Если True - добавляем новую запись: открываем пустое окно
                    self.tableSklad.clearSelection()
                    self.reset_radiobutton(self.tableSklad)
                    if self.tableMotherProizv.rowCount() == 0:  # Если нет производителей для добавления платы (!=заказ)
                        dialog = DialogOk("Ошибка", "Нет производителей, чьи мат. платы можно добавить")
                        dialog.show()
                        if dialog.exec():
                            pass
                    else:  # Если таблица производителей материнок непустая
                        self.win_add_change = adding.AddChangeMotherWindow(self, new_bool, list_all_pr,
                                                                           self.dict_proizv_mother_name,
                                                                           self.dict_mother_name)
                        self.block_lineedit(self.win_add_change.leKol, "")
                        self.win_add_change.show()
                else:  # Есил False - изменяем выбранную запись
                    if type(row) is str:  # Если пришел не кортеж, а строка(ошибка) - вывод окна с ошибкой
                        dialog = DialogOk("Ошибка", row)
                        dialog.show()
                        if dialog.exec():
                            pass
                    else:  # Если пришел список - заполняем окно.
                        if row[1] not in list_exist_pr:  # Если пр-ль выбранного процессора с False договором
                            dialog = DialogOk("Ошибка", "У данного производителя нет договора о поставках")
                            dialog.show()
                            if dialog.exec():
                                pass
                        else:
                            self.win_add_change = adding.AddChangeMotherWindow(self, new_bool, row[1],
                                                                               self.dict_proizv_mother_name,
                                                                               self.dict_mother_name)
                            self.block_combobox(self.win_add_change.cbProizv, row[1])
                            self.block_lineedit(self.win_add_change.leFullName, row[2])
                            self.block_combobox(self.win_add_change.cbGaming, row[3])
                            self.block_lineedit(self.win_add_change.leSocket, row[4])
                            self.block_lineedit(self.win_add_change.leChipset, row[5])
                            self.block_combobox(self.win_add_change.cbFactor, row[6])
                            self.block_combobox(self.win_add_change.cbRamType, row[7])
                            self.block_combobox(self.win_add_change.cbRamSlots, row[8])
                            self.block_lineedit(self.win_add_change.leFreqMax, row[9])
                            self.block_lineedit(self.win_add_change.leRamMax, row[10])
                            self.block_combobox(self.win_add_change.cbM2, row[11])
                            self.block_combobox(self.win_add_change.cbSata, row[12])
                            self.block_lineedit(self.win_add_change.lePrice, row[13])
                            self.win_add_change.show()
            case 3:
                if new_bool:  # Если True - добавляем новую запись: открываем пустое окно
                    self.win_add_change = adding.AddChangeVideoWindow(self, new_bool, row[1],
                                                                      self.dict_proizv_cool_name,
                                                                      self.dict_cool_name)
                    self.win_add_change.show()
            case 4:
                if new_bool:  # Если True - добавляем новую запись: открываем пустое окно
                    self.win_add_change = adding.AddChangeVideoWindow(self, new_bool, row[1],
                                                                      self.dict_proizv_ram_name,
                                                                      self.dict_ram_name)
                    self.win_add_change.show()
            case 5:
                if new_bool:  # Если True - добавляем новую запись: открываем пустое окно
                    self.win_add_change = adding.AddChangeVideoWindow(self, new_bool, row[1],
                                                                      self.dict_proizv_hard_name,
                                                                      self.dict_disk_name)
                    self.win_add_change.show()
            case 6:
                if new_bool:  # Если True - добавляем новую запись: открываем пустое окно
                    self.win_add_change = adding.AddChangeVideoWindow(self, new_bool, row[1],
                                                                      self.dict_proizv_power_name,
                                                                      self.dict_power_name)
                    self.win_add_change.show()
            case 7:
                if new_bool:  # Если True - добавляем новую запись: открываем пустое окно
                    self.win_add_change = adding.AddChangeVideoWindow(self, new_bool, row[1],
                                                                      self.dict_proizv_body_name,
                                                                      self.dict_body_name)
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

    def apply_filter_sklad(self, get_query, page):
        print(get_query)
        conn = None
        cur = None
        try:
            conn = psycopg2.connect(database="confPc",
                                    user="postgres",
                                    password="2001",
                                    host="localhost",
                                    port="5432")
            cur = conn.cursor()
            cur.execute(get_query)
            match page:
                case 0:
                    self.fill_table_sklad(page, cur)
                case 1:
                    self.fill_table_sklad(page, cur)
                case 2:
                    self.fill_table_sklad(page, cur)
        except (Exception, psycopg2.DatabaseError) as error:
            dialog = DialogOk("Ошибка", error)
            dialog.show()

        finally:
            if conn:
                cur.close()
                conn.close()

    def apply_filter_conf(self, get_query, page):
        print(get_query)
        conn = None
        cur = None
        try:
            conn = psycopg2.connect(database="confPc",
                                    user="postgres",
                                    password="2001",
                                    host="localhost",
                                    port="5432")
            cur = conn.cursor()
            cur.execute(get_query)
            match page:
                case 0:
                    self.fill_table_conf(page, cur)
                case 1:
                    self.fill_table_conf(page, cur)
                case 2:
                    self.fill_table_conf(page, cur)
        except (Exception, psycopg2.DatabaseError) as error:
            dialog = DialogOk("Ошибка", error)
            dialog.show()

        finally:
            if conn:
                cur.close()
                conn.close()

    def rb_click_having_sklad(self, have, page):
        conn = None
        cur = None
        data_row = []
        try:
            conn = psycopg2.connect(database="confPc",
                                    user="postgres",
                                    password="2001",
                                    host="localhost",
                                    port="5432")
            cur = conn.cursor()
            if self.tableSklad.currentRow() != -1:  # Если была выбрана строка, то сохраняем её номер
                data_row = self.save_row(self.tableSklad)
            match page:  # Определение запроса к БД по типу комплектующего

                case 0:

                    if have:
                        cur.callproc("get_having_videocard")
                        self.fill_table_sklad(page, cur)
                        self.fill_tabs_sklad(page, self.tabWidgetSklad)
                    else:
                        cur.callproc("get_all_videocard")
                        self.fill_table_sklad(page, cur)
                        self.fill_tabs_sklad(page, self.tabWidgetSklad)
                case 1:
                    if have:
                        cur.callproc("get_having_processor")
                        self.fill_table_sklad(page, cur)
                        self.fill_tabs_sklad(page, self.tabWidgetSklad)
                    else:
                        cur.callproc("get_all_processor")
                        self.fill_table_sklad(page, cur)
                        self.fill_tabs_sklad(page, self.tabWidgetSklad)
                case 2:
                    if have:
                        cur.callproc("get_having_motherboard")
                        self.fill_table_sklad(page, cur)
                        self.fill_tabs_sklad(page, self.tabWidgetSklad)
                    else:
                        cur.callproc("get_all_motherboard")
                        self.fill_table_sklad(page, cur)
                        self.fill_tabs_sklad(page, self.tabWidgetSklad)
                case 3:
                    pass
                case 4:
                    pass
                case 5:
                    pass
                case 6:
                    pass
                case 7:
                    pass
            self.reset_radiobutton(self.tableSklad)
            self.check_rows(data_row, self.tableSklad)

        except (Exception, psycopg2.DatabaseError) as error:
            dialog = DialogOk("Ошибка", error)
            dialog.show()

        finally:
            if conn:
                cur.close()
                conn.close()

    def rb_click_having_conf(self, have):
        conn = None
        cur = None
        data_row = []
        try:
            conn = psycopg2.connect(database="confPc",
                                    user="postgres",
                                    password="2001",
                                    host="localhost",
                                    port="5432")
            cur = conn.cursor()
            if have:
                if self.tableConfVideo.currentRow() != -1:  # Если была выбрана строка, то сохраняем её номер
                    data_row = self.save_row(self.tableConfVideo)
                cur.callproc("get_having_videocard")
                self.fill_table_conf(0, cur)
                self.reset_radiobutton(self.tableConfVideo)
                if self.check_rows(data_row, self.tableConfVideo):
                    pass  # Ничего не выполняем, так как функция сработает еще в IF и если не вернёт True,
                    # то чистим корзину
                else:
                    self.clear_cart(self.tableConfVideo)

                data_row.clear()
                if self.tableConfProc.currentRow() != -1:  # Если была выбрана строка, то сохраняем её номер
                    data_row = self.save_row(self.tableConfProc)
                cur.callproc("get_having_processor")
                self.fill_table_conf(1, cur)
                self.reset_radiobutton(self.tableConfProc)
                if self.check_rows(data_row, self.tableConfProc):
                    pass  # Ничего не выполняем, так как функция сработает еще в IF и если не вернёт True,
                    # то чистим корзину
                else:
                    self.clear_cart(self.tableConfProc)

                data_row.clear()
                if self.tableConfMother.currentRow() != -1:  # Если была выбрана строка, то сохраняем её номер
                    data_row = self.save_row(self.tableConfMother)
                cur.callproc("get_having_motherboard")
                self.fill_table_conf(2, cur)
                self.reset_radiobutton(self.tableConfMother)
                if self.check_rows(data_row, self.tableConfMother):
                    pass  # Ничего не выполняем, так как функция сработает еще в IF и если не вернёт True,
                    # то чистим корзину
                else:
                    self.clear_cart(self.tableConfMother)

                # И другие функции заполнения
            else:
                if self.tableConfVideo.currentRow() != -1:  # Если была выбрана строка, то сохраняем её номер
                    data_row = self.save_row(self.tableConfVideo)
                cur.callproc("get_all_videocard")
                self.fill_table_conf(0, cur)
                self.reset_radiobutton(self.tableConfVideo)
                if self.check_rows(data_row, self.tableConfVideo):
                    pass  # Ничего не выполняем, так как функция сработает еще в IF и если не вернёт True,
                    # то чистим корзину
                else:
                    self.clear_cart(self.tableConfVideo)

                data_row.clear()
                if self.tableConfProc.currentRow() != -1:  # Если была выбрана строка, то сохраняем её номер
                    data_row = self.save_row(self.tableConfProc)
                cur.callproc("get_all_processor")
                self.fill_table_conf(1, cur)
                self.reset_radiobutton(self.tableConfProc)
                if self.check_rows(data_row, self.tableConfProc):
                    pass  # Ничего не выполняем, так как функция сработает еще в IF и если не вернёт True,
                    # то чистим корзину
                else:
                    self.clear_cart(self.tableConfProc)

                data_row.clear()
                if self.tableConfMother.currentRow() != -1:  # Если была выбрана строка, то сохраняем её номер
                    data_row = self.save_row(self.tableConfMother)
                cur.callproc("get_all_motherboard")
                self.fill_table_conf(2, cur)
                self.reset_radiobutton(self.tableConfMother)
                if self.check_rows(data_row, self.tableConfMother):
                    pass  # Ничего не выполняем, так как функция сработает еще в IF и если не вернёт True,
                    # то чистим корзину
                else:
                    self.clear_cart(self.tableConfMother)

            self.fill_all_tabs_conf()

            # И другие функции заполнения
            # self.reset_all_config()

        except (Exception, psycopg2.DatabaseError) as error:
            dialog = DialogOk("Ошибка", error)
            dialog.show()

        finally:
            if conn:
                cur.close()
                conn.close()

    # Метод, возвращающий из БД производителей комплектуюшего
    def get_tabs(self, complect, have):
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
                    if have:
                        cur.callproc('get_having_videoproizv')
                        for name in cur:
                            list_proizv.append(name[0])
                    else:
                        cur.callproc('get_inbase_videoproizv')
                        for name in cur:
                            list_proizv.append(name[0])
                case "Processor":
                    if have:
                        cur.callproc('get_having_procseries')
                        for name in cur:
                            list_proizv.append(name[0])
                    else:
                        cur.callproc('get_inbase_procseries')
                        for name in cur:
                            list_proizv.append(name[0])
                case "Motherboard":
                    if have:
                        cur.callproc('get_having_mothersocket')
                        for name in cur:
                            list_proizv.append(name[0])
                    else:
                        cur.callproc('get_inbase_mothersocket')
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
            dialog = DialogOk("Ошибка", error)
            dialog.show()

        finally:
            if conn:
                conn.commit()
                cur.close()
                conn.close()
            return list_proizv

    # Метод для заполнения tabWidget-ов переданными производителями (есть похожий метод из-за индикатора наличия)
    def fill_tabs_sklad(self, page, tab_widget):
        if tab_widget.count() > 1:
            for i in range(tab_widget.count() - 1):  # Удаление старых вкладок
                tab_widget.removeTab(1)
        # tab_widget.clear()
        match page:
            case 0:
                if self.rbSklad.isChecked():
                    list_names = self.get_tabs("Videocard", True)
                    count_tab = len(list_names)
                    for i in range(0, count_tab):  # первая вкладка должна остаться
                        tab = QtWidgets.QWidget()
                        tab_widget.addTab(tab, list_names[i])
                else:
                    list_names = self.get_tabs("Videocard", False)
                    count_tab = len(list_names)
                    for i in range(0, count_tab):  # первая вкладка должна остаться
                        tab = QtWidgets.QWidget()
                        tab_widget.addTab(tab, list_names[i])
            case 1:
                if self.rbSklad.isChecked():
                    list_names = self.get_tabs("Processor", True)
                    count_tab = len(list_names)
                    for i in range(0, count_tab):  # первая вкладка должна остаться
                        tab = QtWidgets.QWidget()
                        tab_widget.addTab(tab, list_names[i])
                else:
                    list_names = self.get_tabs("Processor", False)
                    count_tab = len(list_names)
                    for i in range(0, count_tab):  # первая вкладка должна остаться
                        tab = QtWidgets.QWidget()
                        tab_widget.addTab(tab, list_names[i])
            case 2:
                if self.rbSklad.isChecked():
                    list_names = self.get_tabs("Motherboard", True)
                    count_tab = len(list_names)
                    for i in range(0, count_tab):  # первая вкладка должна остаться
                        tab = QtWidgets.QWidget()
                        tab_widget.addTab(tab, list_names[i])
                else:
                    list_names = self.get_tabs("Motherboard", False)
                    count_tab = len(list_names)
                    for i in range(0, count_tab):  # первая вкладка должна остаться
                        tab = QtWidgets.QWidget()
                        tab_widget.addTab(tab, list_names[i])

    def fill_tabs_configure(self, list_names, tab_widget):
        """
        Заполняет зависимые от выбранного комплектующего (при срабатывании методов, завязанных на нажатии по комплект.)
        таблицы вкладками, подходящими по выбранному компоненту. Например, заполняет вкладки мат.плат, если выбран проц.
        :param list_names: список вкладок, которыми необходимо заполнить надтабличный фильтр
        :param tab_widget: табвиджет, с которым требуется провести действия
        :return:
        """
        if tab_widget.count() > 1:
            for i in range(tab_widget.count() - 1):  # Удаление старых вкладок
                tab_widget.removeTab(1)
        count_tab = len(list_names)
        for i in range(0, count_tab):  # первая вкладка должна остаться
            tab = QtWidgets.QWidget()
            tab_widget.addTab(tab, list_names[i])

    def fill_all_tabs_conf(self):
        if self.tabWidgetVideo.count() > 1:
            for i in range(self.tabWidgetVideo.count() - 1):  # Удаление старых вкладок
                self.tabWidgetVideo.removeTab(1)
        if self.tabWidgetProc.count() > 1:
            for i in range(self.tabWidgetProc.count() - 1):
                self.tabWidgetProc.removeTab(1)
        if self.tabWidgetMother.count() > 1:
            for i in range(self.tabWidgetMother.count() - 1):
                self.tabWidgetMother.removeTab(1)
        if self.tabWidgetCool.count() > 1:
            for i in range(self.tabWidgetCool.count() - 1):
                self.tabWidgetCool.removeTab(1)
        if self.tabWidgetRam.count() > 1:
            for i in range(self.tabWidgetRam.count() - 1):
                self.tabWidgetRam.removeTab(1)
        if self.tabWidgetDisk.count() > 1:
            for i in range(self.tabWidgetDisk.count() - 1):
                self.tabWidgetDisk.removeTab(1)
        if self.tabWidgetPower.count() > 1:
            for i in range(self.tabWidgetPower.count() - 1):
                self.tabWidgetPower.removeTab(1)
        if self.tabWidgetBody.count() > 1:
            for i in range(self.tabWidgetBody.count() - 1):
                self.tabWidgetBody.removeTab(1)

        list_names = self.get_tabs("Videocard", self.rbConf.isChecked())
        count_tab = len(list_names)
        for i in range(0, count_tab):
            tab = QtWidgets.QWidget()
            self.tabWidgetVideo.addTab(tab, list_names[i])

        list_names = self.get_tabs("Processor", self.rbConf.isChecked())
        count_tab = len(list_names)
        for i in range(0, count_tab):
            tab = QtWidgets.QWidget()
            self.tabWidgetProc.addTab(tab, list_names[i])

        list_names = self.get_tabs("Motherboard", self.rbConf.isChecked())
        count_tab = len(list_names)
        for i in range(0, count_tab):
            tab = QtWidgets.QWidget()
            self.tabWidgetMother.addTab(tab, list_names[i])

    # Метод заполнения одного табвиджета
    def fill_one_tab(self, table):
        """
        Заполняет один tabwidget вкладками.
        Данный метод в частности вызывается из кнопки обновления таблицы, поэтому он принимает таблицу, по ней
        определяет надлежащий tabwidget и передаёт его циклу в конце метода
        :param table: таблица, для которой было вызвано обновление и над которой нужно обновить вкладки
        """
        list_names = []
        tab_widget = ""
        match table:
            case self.tableConfVideo:
                if self.tabWidgetVideo.count() > 1:
                    for i in range(self.tabWidgetVideo.count() - 1):  # Удаление старых вкладок
                        self.tabWidgetVideo.removeTab(1)
                list_names = self.get_tabs("Videocard", self.rbConf.isChecked())
                tab_widget = self.tabWidgetVideo

            case self.tableConfProc:
                if self.tabWidgetProc.count() > 1:
                    for i in range(self.tabWidgetProc.count() - 1):
                        self.tabWidgetProc.removeTab(1)
                list_names = self.get_tabs("Processor", self.rbConf.isChecked())
                tab_widget = self.tabWidgetProc

            case self.tableConfMother:
                if self.tabWidgetMother.count() > 1:
                    for i in range(self.tabWidgetMother.count() - 1):
                        self.tabWidgetMother.removeTab(1)
                list_names = self.get_tabs("Motherboard", self.rbConf.isChecked())
                tab_widget = self.tabWidgetMother

            case self.tableConfCool:
                if self.tabWidgetCool.count() > 1:
                    for i in range(self.tabWidgetCool.count() - 1):
                        self.tabWidgetCool.removeTab(1)
                list_names = self.get_tabs("Cooling", self.rbConf.isChecked())
                tab_widget = self.tabWidgetCool

            case self.tableConfRam:
                if self.tabWidgetRam.count() > 1:
                    for i in range(self.tabWidgetRam.count() - 1):
                        self.tabWidgetRam.removeTab(1)
                list_names = self.get_tabs("Ram", self.rbConf.isChecked())
                tab_widget = self.tabWidgetRam

            case self.tableConfDisk:
                if self.tabWidgetDisk.count() > 1:
                    for i in range(self.tabWidgetDisk.count() - 1):
                        self.tabWidgetDisk.removeTab(1)
                list_names = self.get_tabs("Disk", self.rbConf.isChecked())
                tab_widget = self.tabWidgetDisk

            case self.tableConfPower:
                if self.tabWidgetPower.count() > 1:
                    for i in range(self.tabWidgetPower.count() - 1):
                        self.tabWidgetPower.removeTab(1)
                list_names = self.get_tabs("Power", self.rbConf.isChecked())
                tab_widget = self.tabWidgetPower

            case self.tableConfBody:
                if self.tabWidgetBody.count() > 1:
                    for i in range(self.tabWidgetBody.count() - 1):
                        self.tabWidgetBody.removeTab(1)
                list_names = self.get_tabs("Motherboard", self.rbConf.isChecked())
                tab_widget = self.tabWidgetMother

        count_tab = len(list_names)
        for i in range(0, count_tab):
            tab = QtWidgets.QWidget()
            tab_widget.addTab(tab, list_names[i])

    def click_tab_sklad(self, page, tab_index, tab_widget):
        conn = None
        cur = None
        tab_name = tab_widget.tabText(tab_index)
        data_row = []
        try:
            conn = psycopg2.connect(database="confPc",
                                    user="postgres",
                                    password="2001",
                                    host="localhost",
                                    port="5432")
            cur = conn.cursor()
            match page:
                case 0:
                    if self.tableSklad.currentRow() != -1:  # Если была выбрана строка, то сохраняем её номер
                        data_row = self.save_row(self.tableSklad)
                    if tab_name == "Все" and self.rbSklad.isChecked():
                        cur.callproc('get_having_videocard')
                        self.fill_table_sklad(page, cur)
                    elif tab_name == "Все":
                        cur.callproc('get_all_videocard')
                        self.fill_table_sklad(page, cur)
                    else:
                        cur.callproc('get_videocard_by_name', [tab_name])
                        self.fill_table_sklad(page, cur)
                    self.reset_radiobutton(self.tableSklad)
                    self.check_rows(data_row, self.tableSklad)
                case 1:
                    if self.tableSklad.currentRow() != -1:  # Если была выбрана строка, то сохраняем её номер
                        data_row = self.save_row(self.tableSklad)
                    if tab_name == "Все" and self.rbSklad.isChecked():
                        cur.callproc('get_having_processor')
                        self.fill_table_sklad(page, cur)
                    elif tab_name == "Все":
                        cur.callproc('get_all_processor')
                        self.fill_table_sklad(page, cur)
                    else:
                        cur.callproc('get_processor_by_series', [tab_name])
                        self.fill_table_sklad(page, cur)
                    self.reset_radiobutton(self.tableSklad)
                    self.check_rows(data_row, self.tableSklad)
                case 2:
                    if self.tableSklad.currentRow() != -1:  # Если была выбрана строка, то сохраняем её номер
                        data_row = self.save_row(self.tableSklad)
                    if tab_name == "Все" and self.rbSklad.isChecked():
                        cur.callproc('get_having_motherboard')
                        self.fill_table_sklad(page, cur)
                    elif tab_name == "Все":
                        cur.callproc('get_all_motherboard')
                        self.fill_table_sklad(page, cur)
                    else:
                        cur.callproc('get_motherboard_by_socket', [tab_name])
                        self.fill_table_sklad(page, cur)
                    self.reset_radiobutton(self.tableSklad)
                    self.check_rows(data_row, self.tableSklad)
                # case 3-9...

            # Можно потом изменить чтобы при клике по вкладке если комплектующее в наличии не сбрасывалось
            # выделение
        except (Exception, psycopg2.DatabaseError) as error:
            dialog = DialogOk("Ошибка", error)
            dialog.show()

        finally:
            if conn:
                cur.close()
                conn.close()

    def click_tab_conf(self, tab_index, tab_widget):
        conn = None
        cur = None
        tab_name = tab_widget.tabText(tab_index)
        try:
            conn = psycopg2.connect(database="confPc",
                                    user="postgres",
                                    password="2001",
                                    host="localhost",
                                    port="5432")
            cur = conn.cursor()
            index_row = -1
            data_row = []
            match tab_widget:
                case self.tabWidgetVideo:
                    if self.tableConfVideo.currentRow() != -1:  # Если была выбрана строка, то сохраняем её номер
                        data_row = self.save_row(self.tableConfVideo)

                    if tab_name == "Все" and self.rbConf.isChecked():
                        cur.callproc('get_having_videocard')
                        self.fill_table_conf(0, cur)
                        self.reset_radiobutton(self.tableConfVideo)
                        # Можно потом изменить чтобы при клике по вкладке если комплектующее в наличии не сбрасывалось
                        # выделение
                    elif tab_name == "Все":
                        cur.callproc('get_all_videocard')
                        self.fill_table_conf(0, cur)
                        self.reset_radiobutton(self.tableConfVideo)
                    else:
                        cur.callproc('get_videocard_by_name', [tab_name])
                        self.fill_table_conf(0, cur)
                        self.reset_radiobutton(self.tableConfVideo)

                    self.check_rows(data_row, self.tableConfVideo)  # Проверяем строку и выделяем её
                case self.tabWidgetProc:  # Здесь так же 3 условия, но для процессора
                    if self.tableConfProc.currentRow() != -1:  # Если была выбрана строка, то сохраняем её номер
                        data_row = self.save_row(self.tableConfProc)

                    if tab_name == "Все" and self.rbConf.isChecked():
                        cur.callproc('get_having_processor')
                        self.fill_table_conf(1, cur)
                        self.reset_radiobutton(self.tabWidgetProc)
                        # Можно потом изменить чтобы при клике по вкладке если комплектующее в наличии не сбрасывалось
                        # выделение
                    elif tab_name == "Все":
                        cur.callproc('get_all_processor')
                        self.fill_table_conf(1, cur)
                        self.reset_radiobutton(self.tabWidgetProc)
                    else:
                        cur.callproc('get_processor_by_series', [tab_name])
                        self.fill_table_conf(1, cur)
                        self.reset_radiobutton(self.tabWidgetProc)

                    self.check_rows(data_row, self.tableConfProc)  # Проверяем строку и выделяем её

                case self.tabWidgetMother:  # Здесь так же 3 условия, но для процессора
                    if self.tableConfMother.currentRow() != -1:  # Если была выбрана строка, то сохраняем её номер
                        data_row = self.save_row(self.tableConfMother)

                    if tab_name == "Все" and self.rbConf.isChecked():
                        cur.callproc('get_having_motherboard')
                        self.fill_table_conf(2, cur)
                        self.reset_radiobutton(self.tabWidgetMother)
                        # Можно потом изменить чтобы при клике по вкладке если комплектующее в наличии не сбрасывалось
                        # выделение
                    elif tab_name == "Все":
                        cur.callproc('get_all_motherboard')
                        self.fill_table_conf(2, cur)
                        self.reset_radiobutton(self.tabWidgetMother)
                    else:
                        cur.callproc('get_motherboard_by_socket', [tab_name])
                        self.fill_table_conf(2, cur)
                        self.reset_radiobutton(self.tabWidgetMother)

                    self.check_rows(data_row, self.tableConfMother)  # Проверяем строку и выделяем её
                # case 2-9...

        except (Exception, psycopg2.DatabaseError) as error:
            dialog = DialogOk("Ошибка", error)
            dialog.show()

        finally:
            if conn:
                cur.close()
                conn.close()

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
        widget.setStyleSheet("background-color: transparent;")
        return widget

    # Метод создания рб на виджете
    def create_radiobutton(self):
        widget = QtWidgets.QWidget()
        rb = RadioButton()
        pLayout = QtWidgets.QHBoxLayout(widget)
        pLayout.addWidget(rb)
        pLayout.setAlignment(QtCore.Qt.AlignCenter)
        pLayout.setContentsMargins(0, 0, 0, 0)
        widget.setStyleSheet("background-color: transparent;")
        widget.setLayout(pLayout)
        return widget, rb

    # Метод, обнуляющий собранную конфигурацию
    def reset_all_config(self):
        self.click_reset_radiobutton(self.tableConfVideo)
        self.click_reset_radiobutton(self.tableConfProc)
        self.click_reset_radiobutton(self.tableConfMother)
        self.click_reset_radiobutton(self.tableConfCool)
        self.click_reset_radiobutton(self.tableConfRam)
        self.click_reset_radiobutton(self.tableConfDisk)
        self.click_reset_radiobutton(self.tableConfPower)
        self.click_reset_radiobutton(self.tableConfBody)
        self.lb_price.setText("000 000")

    # Метод, обнуляющий RadioButton в таблице
    def reset_radiobutton(self, table):
        if table.objectName() in self.dict_button_group:  # Если пара таблица-группа были добавлены
            button_group = self.dict_button_group[table.objectName()]
            button_group.setExclusive(False)
            for i in range(table.rowCount()):
                widget = table.cellWidget(i, 0)
                if widget is not None:
                    rad_but = widget.findChild(RadioButton)
                    if rad_but is not None and rad_but.isChecked():
                        rad_but.setChecked(False)
            table.clearSelection()
            table.setCurrentCell(-1, -1)
            button_group.setExclusive(True)

    # Метод, обнуляющий RadioButton в таблице по клику на кнопку
    def click_reset_radiobutton(self, table):
        if table.objectName() in self.dict_button_group:  # Если пара таблица-группа были добавлены
            button_group = self.dict_button_group[table.objectName()]
            button_group.setExclusive(False)
            for i in range(table.rowCount()):
                widget = table.cellWidget(i, 0)
                if widget is not None:
                    rad_but = widget.findChild(RadioButton)
                    if rad_but is not None and rad_but.isChecked():
                        rad_but.setChecked(False)
            table.clearSelection()
            table.setCurrentCell(-1, -1)
            button_group.setExclusive(True)
            self.fill_one_tab(table)
            match table:  # Перезаполнение таблицы новыми записями
                case self.tableConfVideo:
                    self.load_conf(0)
                case self.tableConfProc:
                    self.load_conf(1)
                case self.tableConfMother:
                    self.load_conf(2)
                case self.tableConfCool:
                    self.load_conf(3)
                case self.tableConfRam:
                    self.load_conf(4)
                case self.tableConfDisk:
                    self.load_conf(5)
                case self.tableConfPower:
                    self.load_conf(6)
                case self.tableConfBody:
                    self.load_conf(7)
            self.clear_cart(table)

    #  Метод очистки всей корзины (таблицы) предпросмотра заказа
    def clear_cart(self, table):
        price_configuration = []
        for i in range(self.table_config.rowCount()):  # Проход по корзине и удаление строки по таблице
            if self.table_config.item(i, 0) is not None and self.table_config.item(i, 0).text() == str(table):
                self.table_config.removeRow(i)
        self.progressBar.setValue(self.table_config.rowCount())  # обновление прогрессбара
        for row in range(self.table_config.rowCount()):
            price_configuration.append(int(self.table_config.item(row, 2).text()))
        if sum(price_configuration) == 0:
            self.lb_price.setText("000 000")
        else:
            self.lb_price.setText(str(sum(price_configuration)))

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
            """radio.toggled.connect(
                lambda ch, row=i: self.current_pos_sklad(ch, row, table))"""
            table.setCellWidget(i, 0, widget)
            button_group.addButton(radio)
            button_group.setId(radio, i)
        self.dict_button_group[table.objectName()] = button_group

    def cell_row_without_conf(self, row, column, table):
        if table.objectName() in self.dict_button_group:  # Если пара таблица-группа были добавлены
            button_group = self.dict_button_group[table.objectName()]
            button_group.setExclusive(False)
            for i in range(table.rowCount()):
                widget = table.cellWidget(i, 0)
                if widget is not None:
                    radio_but = widget.findChild(RadioButton)
                    if radio_but is not None and radio_but.isChecked():
                        radio_but.setChecked(False)
                    if i == row:
                        radio_but.setChecked(True)
            button_group.setExclusive(True)

    def cell_row(self, row, column, table):
        # print(f'\n row={row}; column={column}')
        if table.objectName() in self.dict_button_group:  # Если пара таблица-группа были добавлены
            button_group = self.dict_button_group[table.objectName()]

            # Способ переключения RB по нахождению в словарю (за каждой кнопкой своя строка)
            # rb = button_group.button(row)
            # rb.click()

            # Способ переключения RB по поиску его в кликнутой строке
            button_group.setExclusive(False)
            for i in range(table.rowCount()):
                widget = table.cellWidget(i, 0)
                if widget is not None:
                    radio_but = widget.findChild(RadioButton)
                    if radio_but is not None and radio_but.isChecked():
                        radio_but.setChecked(False)
                    if i == row:
                        radio_but.setChecked(True)
            button_group.setExclusive(True)
            self.configure(table)

    def current_pos(self, ch, row, table):
        if ch:
            table.selectRow(row)
            self.fill_cart(table)

    def configure(self, table):
        conn = None
        cur = None
        saved_row = self.save_row(
            table)  # Сохранение строки в словарь по таблице для повторного выделения (если попала под фильтр)
        try:
            conn = psycopg2.connect(database="confPc",
                                    user="postgres",
                                    password="2001",
                                    host="localhost",
                                    port="5432")
            cur = conn.cursor()

            match table:  # В каждой таблице отпправляется своё количество запросов в БД для фильтрации
                case self.tableConfVideo:
                    if self.rbConf.isChecked():
                        pass
                    else:
                        pass
                case self.tableConfProc:  # По выбранному процессору отсортировать мат платы и ОЗУ
                    if self.rbConf.isChecked():
                        pass
                    else:
                        mother_row = self.save_row(
                            self.tableConfMother)  # !!! Сохраняем строчку в фильтруемых таблицах, если они выделена!!!!
                        cur.execute("SELECT sklad_motherboard.kol, motherboard.exist, motherboard.id, "
                                    "proizv_motherboard.name, fullname, gaming, socket, chipset, formfactor, "
                                    "memorytype, memoryslot, memorymax, memoryfreqmax, m2, sata, price "
                                    "FROM motherboard, sklad_motherboard, proizv_motherboard "
                                    "WHERE motherboard.id = sklad_motherboard.id_izd "
                                    "AND motherboard.id_proizv = proizv_motherboard.id "
                                    f"AND socket = '{saved_row[1]}' "
                                    "ORDER BY exist DESC")
                        self.fill_table_conf(2, cur)
                        self.check_rows(mother_row, self.tableConfMother)
                        cur.execute("select distinct socket from( "
                                    "SELECT sklad_motherboard.kol, motherboard.exist, motherboard.id, "
                                    "proizv_motherboard.name, fullname, gaming, socket, chipset, formfactor, "
                                    "memorytype, memoryslot, memorymax, memoryfreqmax, m2, sata, price "
                                    "FROM motherboard, sklad_motherboard, proizv_motherboard "
                                    "WHERE motherboard.id = sklad_motherboard.id_izd "
                                    "AND motherboard.id_proizv = proizv_motherboard.id "
                                    f"AND socket = '{saved_row[1]}' "
                                    "ORDER BY exist DESC) as s1")
                        list_proizv = []
                        for name in cur:
                            list_proizv.append(name[0])
                        self.fill_tabs_configure(list_proizv, self.tabWidgetMother)
                case self.tableConfMother:  # По выбранной мат. плате отсортировать процессоры и ОЗУ
                    if self.rbConf.isChecked():
                        pass
                    else:
                        proc_row = self.save_row(
                            self.tableConfProc)  # !!! Сохраняем строчку в фильтруемых таблицах, если они выделена!!!!
                        cur.execute("SELECT sklad_processor.kol, processor.exist, processor.id, proizv_processor.name, "
                                    "fullname, gaming, series, socket, core, ncores, cache, frequency, techproc, "
                                    "ramfreq, graphics, tdp, price "
                                    "FROM processor, sklad_processor, proizv_processor "
                                    "WHERE processor.id = sklad_processor.id_izd "
                                    "AND processor.id_proizv = proizv_processor.id "
                                    f"AND socket = '{saved_row[1]}'"
                                    "ORDER BY exist DESC")
                        self.fill_table_conf(1, cur)
                        self.check_rows(proc_row, self.tableConfProc)
                        cur.execute("select distinct series from( "
                                    "SELECT sklad_processor.kol, processor.exist, processor.id, proizv_processor.name, "
                                    "fullname, gaming, series, socket, core, ncores, cache, frequency, techproc, "
                                    "ramfreq, graphics, tdp, price "
                                    "FROM processor, sklad_processor, proizv_processor "
                                    "WHERE processor.id = sklad_processor.id_izd "
                                    "AND processor.id_proizv = proizv_processor.id "
                                    f"AND socket = '{saved_row[1]}' "
                                    "ORDER BY exist DESC) as s1")
                        list_proizv = []
                        for name in cur:
                            list_proizv.append(name[0])
                        self.fill_tabs_configure(list_proizv, self.tabWidgetProc)

            # self.fill_tabs_conf()  # нужны отдельные функции заполнения табов по выбранному комплектующему
            # (можно здесь же сделать объединение с большим запросом с SELECT proizvname\сокет и тп DISTINCT) и заполнить табы
        except (Exception, psycopg2.DatabaseError) as error:
            dialog = DialogOk("Ошибка", str(error))
            dialog.show()

        finally:
            if conn:
                cur.close()
                conn.close()

    def save_row(self, table):
        index_row = -1
        if table.currentRow() != -1:  # Если была выбрана строка, то сохраняем её номер
            index_row = table.currentRow()
            data_row = self.current_conf(table)  # Сохранение строки
            self.dict_current[table.objectName()] = data_row  # Убрать ретёрн и оставить словарь?
            """match table:
                case self.tableConfVideo:
                    self.dict_current_video[table.objectName()] = data_row"""
            return data_row
        return []

    def check_rows(self, saved_row, table):
        checkable_row = []
        column_count = table.columnCount()
        row_count = table.rowCount()
        for j in range(row_count):
            for i in range(2, column_count):
                checkable_row.append(table.item(j, i).text())
            if checkable_row == saved_row:  # Если нашли такую же строку - отмечаем её без конфигурирования
                self.cell_row_without_conf(j, 0, table)
                return True
            checkable_row.clear()
        # Если в отфильтрованной таблице нет выделенной ранее строки (метод не вернул true), то чистим корзину
        self.clear_cart(table)
        return False

    def current_pos_sklad(self, ch, row, table):
        # print(f' row = {row} -- {ch}')
        if ch:
            table.selectRow(row)

    # Метод заполнения корзины выбранных комплектующих (принимает таблицу, из которой был вызван, имя и цену)
    def fill_cart(self, table):
        row_count = self.table_config.rowCount()
        name = ""
        price = ""
        price_configuration = []
        match table:  # Определяем имя и цену для записи в корзину по кликнутной таблице
            case self.tableConfVideo:
                name = table.item(table.currentRow(), 2).text()
                price = table.item(table.currentRow(), 12).text()
            case self.tableConfProc:
                name = table.item(table.currentRow(), 2).text()
                price = table.item(table.currentRow(), 9).text()
            case self.tableConfMother:
                name = table.item(table.currentRow(), 2).text()
                price = table.item(table.currentRow(), 12).text()
            # case.............

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
        for row in range(self.table_config.rowCount()):
            price_configuration.append(int(self.table_config.item(row, 2).text()))
        if sum(price_configuration) == 0:
            self.lb_price.setText("000 000")
        else:
            self.lb_price.setText(str(sum(price_configuration)))

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
