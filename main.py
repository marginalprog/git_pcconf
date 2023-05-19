import sys
import psycopg2

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QDateTime
from PyQt5.QtWidgets import QDialog, QTableWidgetItem
from PyQt5.QtGui import QPixmap
from ui import main_interface, warningWin, acceptionWin, acceptOrderWidg
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


# Класс окна с подтверждением заказа
class AcceptOrderWin(QtWidgets.QWidget, acceptOrderWidg.Ui_acceptOrderWidg):
    def __init__(self, main_window, tuple_order=None):
        super().__init__()
        self.setupUi(self)
        self.dateEdit.setDateTime(QDateTime.currentDateTime())
        self.dateEdit.setDisabled(True)
        if main_window.tableConfVideo.currentRow() != -1:
            self.previewVideo.setText(
                main_window.tableConfVideo.item(main_window.tableConfVideo.currentRow(), 2).text())
        if main_window.tableConfProc.currentRow() != -1:
            self.previewProc.setText(main_window.tableConfProc.item(main_window.tableConfProc.currentRow(), 2).text())
        if main_window.tableConfMother.currentRow() != -1:
            self.previewMother.setText(
                main_window.tableConfMother.item(main_window.tableConfMother.currentRow(), 2).text())
        if main_window.tableConfCool.currentRow() != -1:
            self.previewCool.setText(main_window.tableConfCool.item(main_window.tableConfCool.currentRow(), 2).text())
        if main_window.tableConfRam.currentRow() != -1:
            self.previewRam.setText(main_window.tableConfRam.item(main_window.tableConfRam.currentRow(), 2).text())
        if main_window.tableConfDisk.currentRow() != -1:
            self.previewDisk.setText(main_window.tableConfDisk.item(main_window.tableConfDisk.currentRow(), 2).text())
        if main_window.tableConfPower.currentRow() != -1:
            self.previewPower.setText(
                main_window.tableConfPower.item(main_window.tableConfPower.currentRow(), 2).text())
        if main_window.tableConfBody.currentRow() != -1:
            self.previewBody.setText(main_window.tableConfBody.item(main_window.tableConfBody.currentRow(), 2).text())
        self.lb_price.setText(main_window.lb_price.text())
        self.btnAcceptPurcashe.clicked.connect(
            lambda: self.create_order(tuple_order, main_window, main_window.lb_price.text()))

    def create_order(self, tuple_order, main_window, price):
        if tuple_order:
            count = 0
            for i in tuple_order[1]:
                if i > 0:
                    count += 1
            if count == 8:  # Если все 8 комплектующих содержатся в кол-ве > 0
                conn = None
                cur = None
                try:
                    conn = psycopg2.connect(database="confPc",
                                            user="postgres",
                                            password="2001",
                                            host="localhost",
                                            port="5432")
                    cur = conn.cursor()

                    cur.callproc("create_configuration", [main_window.user_id,
                                                          tuple_order[0][0],
                                                          tuple_order[0][1],
                                                          tuple_order[0][2],
                                                          tuple_order[0][3],
                                                          tuple_order[0][4],
                                                          tuple_order[0][5],
                                                          tuple_order[0][6],
                                                          tuple_order[0][7],
                                                          price,
                                                          self.dateEdit.dateTime().toString("yyyy-MM-dd")])
                    conn.commit()
                except (Exception, psycopg2.DatabaseError) as error:
                    dialog = DialogOk("Ошибка", str(error))
                    dialog.show()

                finally:
                    if conn:
                        cur.close()
                        conn.close()
                        main_window.reset_all_config()
                        main_window.reset_radiobutton(main_window.tableSklad)
                        for i in range(8):
                            main_window.load_sklad(i)
                            main_window.load_conf(i)
                        main_window.create_sklad_filter()
                        main_window.create_conf_filter()
            else:
                dialog = DialogOk("Ошибка", "Выбраны комплектующие, которых нет на складе (серый индикатор)")
                dialog.show()
                if dialog.exec():
                    pass
        else:
            dialog = DialogOk("Ошибка", "Выберите все необходимые для сборки комплектующие")
            dialog.show()
            if dialog.exec():
                pass


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
                    case "Производитель охлаждений":
                        cur.callproc('insert_proizv_cool', [proizv_name])
                        conn.commit()
                        mainwindow.load_proizv_cool()  # Загрузка обновлённой таблицы из БД
                    case "Производитель ОЗУ":
                        cur.callproc('insert_proizv_ram', [proizv_name])
                        conn.commit()
                        mainwindow.load_proizv_ram()  # Загрузка обновлённой таблицы из БД
                    case "Производитель накопителей":
                        cur.callproc('insert_proizv_disk', [proizv_name])
                        conn.commit()
                        mainwindow.load_proizv_disk()  # Загрузка обновлённой таблицы из БД
                    case "Производитель блоков питания":
                        cur.callproc('insert_proizv_power', [proizv_name])
                        conn.commit()
                        mainwindow.load_proizv_power()  # Загрузка обновлённой таблицы из БД
                    case "Производитель корпусов":
                        cur.callproc('insert_proizv_body', [proizv_name])
                        conn.commit()
                        mainwindow.load_proizv_body()
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
        self.dict_proizv_disk_name = {}
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

        # Словарь, хранящий параметры TDP Процессора, видеокарты и охлаждения  для вычисления оптимального блока питания
        self.dict_power_vid_proc_cool = {}

        # Словарь для хранения пар ключ(таблица): выбранное комплектующее
        self.dict_current = {}

        self.query_sklad = ""
        self.query_conf = ""

        self.user_id = 1  # 1 - ID администратора (работника).

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
            self.current_sklad())
                                       )

        # По нажатии на кнопку запускается метод, который принимает выбранную вклдку ТБ и открывает нужное окно фильтра
        self.btnSkladFilter.clicked.connect(lambda: self.tb_sklad_filter(self.toolBoxNavigation.currentIndex()))

        # По нажатии на кнопку наличия запускается метод, отправляющий в метод состояние кн. наличия, заказов, и вкладки
        self.rbSklad.toggled.connect(
            lambda have: self.rb_click_order_having_sklad(have, self.rbShowOrders.isChecked(),
                                                          self.toolBoxNavigation.currentIndex()))

        # По нажатии на кнопку закзаов запускается метод, отправляющий в метод having, своё состояние и ID вкладки
        self.rbShowOrders.toggled.connect(
            lambda order: self.rb_click_order_having_sklad(self.rbSklad.isChecked(), order,
                                                           self.toolBoxNavigation.currentIndex()))

        self.rbConf.toggled.connect(
            lambda have: self.rb_click_having_conf(have))

        self.load_proizv_videocard()
        self.load_proizv_processor()
        self.load_proizv_motherboard()
        self.load_proizv_cool()
        self.load_proizv_ram()
        self.load_proizv_disk()
        self.load_proizv_power()
        self.load_proizv_body()
        for i in range(8):
            self.load_sklad(i)  # Первоначальная загрузка всех параметров для словарей
        self.load_sklad(0)  # Перезагрузка и отображение в таблице склада видеокарт
        # =================================Окна фильтрации комплектующих на складе=========================
        self.vidSkladFilter = filters.VideoFilter(0, self)  # Создаётся отдельный экземпляр для сохранения внесённых д-х
        self.procSkladFilter = filters.ProcFilter(0, self)
        self.motherSkladFilter = filters.MotherFilter(0, self)
        self.coolSkladFilter = filters.CoolFilter(0, self)
        self.ramSkladFilter = filters.RamFilter(0, self)
        self.diskSkladFilter = filters.DiskFilter(0, self)
        self.powerSkladFilter = filters.PowerFilter(0, self)
        self.bodySkladFilter = filters.BodyFilter(0, self)
        self.rbSklad.toggled.connect(self.create_sklad_filter)  # Пересоздание экземпляра, если индикатор нажат

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
        self.btnNewVideoProizv.clicked.connect(lambda:
                                               AddProizv(self, "Производитель видеокарт",
                                                         self.dict_proizv_video_name).show())
        self.btnNewProcProizv.clicked.connect(lambda:
                                              AddProizv(self, "Производитель процессоров",
                                                        self.dict_proizv_proc_name).show())
        self.btnNewMotherProizv.clicked.connect(lambda:
                                                AddProizv(self, "Производитель мат. плат",
                                                          self.dict_proizv_mother_name).show())
        self.btnNewCoolProizv.clicked.connect(lambda:
                                              AddProizv(self, "Производитель охлаждений",
                                                        self.dict_proizv_cool_name).show())
        self.btnNewRamProizv.clicked.connect(lambda:
                                             AddProizv(self, "Производитель ОЗУ",
                                                       self.dict_proizv_ram_name).show())
        self.btnNewDiskProizv.clicked.connect(lambda:
                                              AddProizv(self, "Производитель накопителей",
                                                        self.dict_proizv_disk_name).show())
        self.btnNewPowerProizv.clicked.connect(lambda:
                                               AddProizv(self, "Производитель блоков питания",
                                                         self.dict_proizv_power_name).show())
        self.btnNewBodyProizv.clicked.connect(lambda:
                                              AddProizv(self, "Производитель корпусов",
                                                        self.dict_proizv_body_name).show())

        # Кнопки обновления состояния договора производителя
        self.btnCngVideoProizv.clicked.connect(lambda: self.change_proizv(self.tableVideoProizv))
        self.btnCngProcProizv.clicked.connect(lambda: self.change_proizv(self.tableProcProizv))
        self.btnCngMotherProizv.clicked.connect(lambda: self.change_proizv(self.tableMotherProizv))
        self.btnCngCoolProizv.clicked.connect(lambda: self.change_proizv(self.tableCoolProizv))
        self.btnCngRamProizv.clicked.connect(lambda: self.change_proizv(self.tableRamProizv))
        self.btnCngDiskProizv.clicked.connect(lambda: self.change_proizv(self.tableDiskProizv))
        self.btnCngPowerProizv.clicked.connect(lambda: self.change_proizv(self.tablePowerProizv))
        self.btnCngBodyProizv.clicked.connect(lambda: self.change_proizv(self.tableBodyProizv))

        self.tableVideoProizv.cellClicked.connect(
            lambda row, column, table=self.tableVideoProizv:
            self.cell_row_without_conf(row, column, table))
        self.tableProcProizv.cellClicked.connect(
            lambda row, column, table=self.tableProcProizv:
            self.cell_row_without_conf(row, column, table))
        self.tableMotherProizv.cellClicked.connect(
            lambda row, column, table=self.tableMotherProizv:
            self.cell_row_without_conf(row, column, table))
        self.tableCoolProizv.cellClicked.connect(
            lambda row, column, table=self.tableCoolProizv:
            self.cell_row_without_conf(row, column, table))
        self.tableRamProizv.cellClicked.connect(
            lambda row, column, table=self.tableRamProizv:
            self.cell_row_without_conf(row, column, table))
        self.tableDiskProizv.cellClicked.connect(
            lambda row, column, table=self.tableDiskProizv:
            self.cell_row_without_conf(row, column, table))
        self.tablePowerProizv.cellClicked.connect(
            lambda row, column, table=self.tablePowerProizv:
            self.cell_row_without_conf(row, column, table))
        self.tableBodyProizv.cellClicked.connect(
            lambda row, column, table=self.tableBodyProizv:
            self.cell_row_without_conf(row, column, table))

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
        for i in range(8):
            self.load_conf(i)
        self.fill_all_tabs_conf()
        # -----------------------------------------------------------------------------

        # ----------------------------Кнопки с помощью--------------------------------
        self.vHelp = helping.VideoHelp()
        self.pHelp = helping.ProcHelp()
        self.mHelp = helping.MotherHelp()
        self.cHelp = helping.CoolHelp()
        self.rHelp = helping.RamHelp()
        self.dHelp = helping.DiskHelp()
        self.powHelp = helping.PowerHelp()
        self.bHelp = helping.BodyHelp()

        self.btnVidHelp.clicked.connect(lambda: self.vHelp.show())
        self.btnProcHelp.clicked.connect(lambda: self.pHelp.show())
        self.btnMotherHelp.clicked.connect(lambda: self.mHelp.show())
        self.btnCoolHelp.clicked.connect(lambda: self.cHelp.show())
        self.btnRamHelp.clicked.connect(lambda: self.rHelp.show())
        self.btnDiskHelp.clicked.connect(lambda: self.dHelp.show())
        self.btnPowerHelp.clicked.connect(lambda: self.powHelp.show())
        self.btnBodyHelp.clicked.connect(lambda: self.bHelp.show())

        # ---------------------------------------------------------------------------

        # ---------------------Окна и кнопки с фильтрами------------------------
        self.vidConfFilter = filters.VideoFilter(1, self)  # Создаётся отдельный экземпляр для сохранения внесённых д-х
        self.procConfFilter = filters.ProcFilter(1, self)  # Создаётся отдельный экземпляр для сохранения внесённых д-х
        self.motherConfFilter = filters.MotherFilter(1, self)
        self.coolConfFilter = filters.CoolFilter(1, self)
        self.ramConfFilter = filters.RamFilter(1, self)
        self.diskConfFilter = filters.DiskFilter(1, self)
        self.powerConfFilter = filters.PowerFilter(1, self)
        self.bodyConfFilter = filters.BodyFilter(1, self)

        self.btnVidFilter.clicked.connect(lambda: self.vidConfFilter.show())
        self.btnProcFilter.clicked.connect(lambda: self.procConfFilter.show())
        self.btnMotherFilter.clicked.connect(lambda: self.motherConfFilter.show())
        self.btnCoolFilter.clicked.connect(lambda: self.coolConfFilter.show())
        self.btnRamFilter.clicked.connect(lambda: self.ramConfFilter.show())
        self.btnDiskFilter.clicked.connect(lambda: self.diskConfFilter.show())
        self.btnPowerFilter.clicked.connect(lambda: self.powerConfFilter.show())
        self.btnBodyFilter.clicked.connect(lambda: self.bodyConfFilter.show())
        self.rbConf.toggled.connect(self.create_conf_filter)  # Пересоздание экземпляра, если индикатор нажат

        # ---------------------------------------------------------------------

        # -----------------------Кнопка сброса сборки--------------------------
        self.btnResetConfig.clicked.connect(self.reset_all_config)
        # ---------------------------------------------------------------------

        # -----------------------Кнопки отображения хедеров--------------------------
        self.btnVideoHeader.clicked.connect(lambda: self.show_header(self.tableConfVideo, True))
        self.btnProcHeader.clicked.connect(lambda: self.show_header(self.tableConfProc, True))
        self.btnMotherHeader.clicked.connect(lambda: self.show_header(self.tableConfMother, True))
        self.btnCoolHeader.clicked.connect(lambda: self.show_header(self.tableConfCool, True))
        self.btnRamHeader.clicked.connect(lambda: self.show_header(self.tableConfRam, True))
        self.btnDiskHeader.clicked.connect(lambda: self.show_header(self.tableConfDisk, True))
        self.btnPowerHeader.clicked.connect(lambda: self.show_header(self.tableConfPower, True))
        self.btnBodyHeader.clicked.connect(lambda: self.show_header(self.tableConfBody, True))
        # ---------------------------------------------------------------------------

        # Кнопка оформления заказа
        self.order_window = AcceptOrderWin(self)
        self.btnPurcashe.clicked.connect(self.accept_order)

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
        self.tabWidgetCool.tabBarClicked.connect(lambda index: self.click_tab_conf(index, self.tabWidgetCool))
        self.tabWidgetRam.tabBarClicked.connect(lambda index: self.click_tab_conf(index, self.tabWidgetRam))
        self.tabWidgetDisk.tabBarClicked.connect(lambda index: self.click_tab_conf(index, self.tabWidgetDisk))
        self.tabWidgetPower.tabBarClicked.connect(lambda index: self.click_tab_conf(index, self.tabWidgetPower))
        self.tabWidgetBody.tabBarClicked.connect(lambda index: self.click_tab_conf(index, self.tabWidgetBody))

    def show_header(self, table, flag_btn=False):
        """
        Метод для отображения заголовков в таблицах конфигуратора. Если вызван из кнопки - видимость меняется.
        Если вызван из других методов - остаётся прежней
        :param table: таблица, в которой требуется показать заголовок
        :param flag_btn: флаг, который показывает, откуда был вызван метод
        """
        match table:
            case self.tableConfVideo:
                self.tableConfVideo.setHorizontalHeaderLabels(["", "",
                                                               "Название", "Произв. чипа",
                                                               "Наименов. чипа", "Объём памяти", "Тип памяти",
                                                               "Частота процессора", "Шина", "Интерфейс",
                                                               "Разрешение", "TDP", "Длина",
                                                               "Pin-контакты", "Кол-во pin", "Цена"])
                if flag_btn:
                    if self.btnVideoHeader.isChecked():
                        table.horizontalHeader().setVisible(self.btnVideoHeader.isChecked())
                    else:
                        for i in range(table.columnCount()):
                            table.takeHorizontalHeaderItem(i)
                        table.horizontalHeader().setVisible(False)
                else:
                    for i in range(table.columnCount()):
                        table.takeHorizontalHeaderItem(i)
                    table.horizontalHeader().setVisible(False)
            case self.tableConfProc:
                self.tableConfProc.setHorizontalHeaderLabels(["", "", "Название",
                                                              "Сокет", "Ядро", "Кол-во ядер",
                                                              "Частота процессора", "Частота ОЗУ",
                                                              "TDP", "Цена"])
                if flag_btn:
                    if self.btnProcHeader.isChecked():
                        table.horizontalHeader().setVisible(self.btnProcHeader.isChecked())
                    else:
                        for i in range(table.columnCount()):
                            table.takeHorizontalHeaderItem(i)
                        table.horizontalHeader().setVisible(False)
                else:
                    for i in range(table.columnCount()):
                        table.takeHorizontalHeaderItem(i)
                    table.horizontalHeader().setVisible(False)
            case self.tableConfMother:
                self.tableConfMother.setHorizontalHeaderLabels(["", "", "Название", "Cокет",
                                                                "Чипсет", "Формфактор", "PCI-E", "Тип ОЗУ",
                                                                "Слоты ОЗУ",
                                                                "Макс. объём ОЗУ", "Макс. частота ОЗУ", "Слоты М2",
                                                                "Разъёмы SATA", "Pin-охлаждение", "Pin-процессор",
                                                                "Кол-во pin", "Цена"])
                if flag_btn:
                    if self.btnMotherHeader.isChecked():
                        table.horizontalHeader().setVisible(self.btnMotherHeader.isChecked())
                    else:
                        for i in range(table.columnCount()):
                            table.takeHorizontalHeaderItem(i)
                        table.horizontalHeader().setVisible(False)
                else:
                    for i in range(table.columnCount()):
                        table.takeHorizontalHeaderItem(i)
                    table.horizontalHeader().setVisible(False)
            case self.tableConfCool:
                self.tableConfCool.setHorizontalHeaderLabels(["", "", "Название", "Конструкция",
                                                              "Тип охл.", "Сокеты", "Трубы", "Высота",
                                                              "Рассеиваемость", "Напряжение", "Pin-коннектор",
                                                              "Цена"])
                if flag_btn:
                    if self.btnCoolHeader.isChecked():
                        table.horizontalHeader().setVisible(self.btnCoolHeader.isChecked())
                    else:
                        for i in range(table.columnCount()):
                            table.takeHorizontalHeaderItem(i)
                        table.horizontalHeader().setVisible(False)
                else:
                    for i in range(table.columnCount()):
                        table.takeHorizontalHeaderItem(i)
                    table.horizontalHeader().setVisible(False)
            case self.tableConfRam:
                self.tableConfRam.setHorizontalHeaderLabels(["", "", "Название", "Тип",
                                                             "Объём", "Тактовая частота", "Кол-во модулей",
                                                             "CAS-Latency", "Напряжение", "Цена"])
                if flag_btn:
                    if self.btnRamHeader.isChecked():
                        table.horizontalHeader().setVisible(self.btnRamHeader.isChecked())
                    else:
                        for i in range(table.columnCount()):
                            table.takeHorizontalHeaderItem(i)
                        table.horizontalHeader().setVisible(False)
                else:
                    for i in range(table.columnCount()):
                        table.takeHorizontalHeaderItem(i)
                    table.horizontalHeader().setVisible(False)
            case self.tableConfDisk:
                self.tableConfDisk.setHorizontalHeaderLabels(["", "", "Название", "Тип", "Объём",
                                                              "Интерфейс", "Скорость чтения", "Скорость записи",
                                                              "RPM", "Цена"])
                if flag_btn:
                    if self.btnDiskHeader.isChecked():
                        table.horizontalHeader().setVisible(self.btnDiskHeader.isChecked())
                    else:
                        for i in range(table.columnCount()):
                            table.takeHorizontalHeaderItem(i)
                        table.horizontalHeader().setVisible(False)
                else:
                    for i in range(table.columnCount()):
                        table.takeHorizontalHeaderItem(i)
                    table.horizontalHeader().setVisible(False)
            case self.tableConfPower:
                self.tableConfPower.setHorizontalHeaderLabels(["", "", "Название",
                                                               "Формафактор", "Длина", "Мощность", "Сертификат",
                                                               "Основной разъём питания",
                                                               "Количество разъёмов SATA",
                                                               "Pin-процессор", "Кол-во pin", "Pin-видеокарта",
                                                               "Кол-во pin", "Цена"])
                if flag_btn:
                    if self.btnPowerHeader.isChecked():
                        table.horizontalHeader().setVisible(self.btnPowerHeader.isChecked())
                    else:
                        for i in range(table.columnCount()):
                            table.takeHorizontalHeaderItem(i)
                        table.horizontalHeader().setVisible(False)
                else:
                    for i in range(table.columnCount()):
                        table.takeHorizontalHeaderItem(i)
                    table.horizontalHeader().setVisible(False)
            case self.tableConfBody:
                self.tableConfBody.setHorizontalHeaderLabels(["", "", "Название", "Тип корпуса",
                                                              "Форм-фактор мат. платы", "Форм-фактор БП",
                                                              "Макс. длина виеокарты", "Макс. высота охлаждения",
                                                              "Макс. длина БП", "Масса", "Цвет", "Цена"])
                if flag_btn:
                    if self.btnBodyHeader.isChecked():
                        table.horizontalHeader().setVisible(self.btnBodyHeader.isChecked())
                    else:
                        for i in range(table.columnCount()):
                            table.takeHorizontalHeaderItem(i)
                        table.horizontalHeader().setVisible(False)
                else:
                    for i in range(table.columnCount()):
                        table.takeHorizontalHeaderItem(i)
                    table.horizontalHeader().setVisible(False)
        table.resizeColumnsToContents()

    def get_id_by_name(self, dict, name):
        """
        Метод вычленения ID комплектующего из словаря по имени
        :param dict: словарь с конкретным типом комплектующих
        :param name: название комплектующего
        :return: название комплектующего по ID
        """
        key_list_names = list(dict.keys())
        val_list_names = list(dict.values())

        position = val_list_names.index(name)

        return key_list_names[position]

    def make_order_dict(self):
        dict_order = {}
        list_order_id = []
        list_order_kol = []
        if self.progressBar.value() == 8:  # Если выбрано 8 комплектующих, то создаём словарь со сборкой
            id_compl = self.get_id_by_name(self.dict_video_name,
                                           self.tableConfVideo.item(self.tableConfVideo.currentRow(), 2).text())
            list_order_id.append(id_compl)
            # Словарь с id выбранных комплектующих и количеством
            list_order_kol.append(self.dict_video_kol[id_compl])

            id_compl = self.get_id_by_name(self.dict_proc_name,
                                           self.tableConfProc.item(self.tableConfProc.currentRow(), 2).text())
            list_order_id.append(id_compl)
            list_order_kol.append(self.dict_proc_kol[id_compl])

            id_compl = self.get_id_by_name(self.dict_mother_name,
                                           self.tableConfMother.item(self.tableConfMother.currentRow(), 2).text())
            list_order_id.append(id_compl)
            list_order_kol.append(self.dict_mother_kol[id_compl])

            id_compl = self.get_id_by_name(self.dict_cool_name,
                                           self.tableConfCool.item(self.tableConfCool.currentRow(), 2).text())
            list_order_id.append(id_compl)
            list_order_kol.append(self.dict_cool_kol[id_compl])

            id_compl = self.get_id_by_name(self.dict_ram_name,
                                           self.tableConfRam.item(self.tableConfRam.currentRow(), 2).text())
            list_order_id.append(id_compl)
            list_order_kol.append(self.dict_ram_kol[id_compl])

            id_compl = self.get_id_by_name(self.dict_disk_name,
                                           self.tableConfDisk.item(self.tableConfDisk.currentRow(), 2).text())
            list_order_id.append(id_compl)
            list_order_kol.append(self.dict_video_kol[id_compl])

            id_compl = self.get_id_by_name(self.dict_power_name,
                                           self.tableConfPower.item(self.tableConfPower.currentRow(), 2).text())
            list_order_id.append(id_compl)
            list_order_kol.append(self.dict_power_kol[id_compl])

            id_compl = self.get_id_by_name(self.dict_body_name,
                                           self.tableConfBody.item(self.tableConfBody.currentRow(), 2).text())
            list_order_id.append(id_compl)
            list_order_kol.append(self.dict_body_kol[id_compl])
        return list_order_id, list_order_kol

    def accept_order(self):
        """
        Переопределяет экземпляр класса окна подтверждения заказа и тем самым перезаполняет свои поля с данными
        """
        self.order_window = AcceptOrderWin(self, self.make_order_dict())
        self.order_window.show()

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
        self.procSkladFilter = filters.ProcFilter(0, self)
        self.motherSkladFilter = filters.MotherFilter(0, self)
        self.coolSkladFilter = filters.CoolFilter(0, self)
        self.ramSkladFilter = filters.RamFilter(0, self)
        self.diskSkladFilter = filters.DiskFilter(0, self)
        self.powerSkladFilter = filters.PowerFilter(0, self)
        self.bodySkladFilter = filters.BodyFilter(0, self)

    def create_conf_filter(self):
        self.vidConfFilter = filters.VideoFilter(1, self)
        self.procConfFilter = filters.ProcFilter(1, self)
        self.motherConfFilter = filters.MotherFilter(1, self)
        self.coolConfFilter = filters.CoolFilter(1, self)
        self.ramConfFilter = filters.RamFilter(1, self)
        self.diskConfFilter = filters.DiskFilter(1, self)
        self.powerConfFilter = filters.PowerFilter(1, self)
        self.bodySkladFilter = filters.BodyFilter(1, self)

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

    def load_proizv_cool(self):
        self.tableCoolProizv.clearSelection()
        self.tableCoolProizv.clear()
        self.tableCoolProizv.setRowCount(0)
        self.dict_proizv_cool_name.clear()
        conn = None
        cur = None
        try:
            conn = psycopg2.connect(database="confPc",
                                    user="postgres",
                                    password="2001",
                                    host="localhost",
                                    port="5432")
            cur = conn.cursor()
            cur.callproc("get_proizv_cool")
            row_count = 0
            for row in cur:
                self.tableCoolProizv.setRowCount(row_count + 1)
                # 0 столбец - radiobutton
                # 1 столбец - индикатор состояния договора
                self.tableCoolProizv.setItem(row_count, 2, QtWidgets.QTableWidgetItem(str(row[1])))
                self.dict_proizv_cool_name[row[0]] = row[2]  # Сохраняем id производителя и его имя
                self.tableCoolProizv.setItem(row_count, 3, QtWidgets.QTableWidgetItem(row[2]))
                row_count += 1

        except (Exception, psycopg2.DatabaseError) as error:
            dialog = DialogOk("Ошибка", error)
            dialog.show()

        finally:
            if conn:
                cur.close()
                conn.close()
            self.insert_existence_proizv(self.tableCoolProizv)
            self.insert_rb_sklad(self.tableCoolProizv)  # Загрузка rb для визаулизции

    def load_proizv_ram(self):
        self.tableRamProizv.clearSelection()
        self.tableRamProizv.clear()
        self.tableRamProizv.setRowCount(0)
        self.dict_proizv_ram_name.clear()
        conn = None
        cur = None
        try:
            conn = psycopg2.connect(database="confPc",
                                    user="postgres",
                                    password="2001",
                                    host="localhost",
                                    port="5432")
            cur = conn.cursor()
            cur.callproc("get_proizv_ram")
            row_count = 0
            for row in cur:
                self.tableRamProizv.setRowCount(row_count + 1)
                # 0 столбец - radiobutton
                # 1 столбец - индикатор состояния договора
                self.tableRamProizv.setItem(row_count, 2, QtWidgets.QTableWidgetItem(str(row[1])))
                self.dict_proizv_ram_name[row[0]] = row[2]  # Сохраняем id производителя и его имя
                self.tableRamProizv.setItem(row_count, 3, QtWidgets.QTableWidgetItem(row[2]))
                row_count += 1

        except (Exception, psycopg2.DatabaseError) as error:
            dialog = DialogOk("Ошибка", error)
            dialog.show()

        finally:
            if conn:
                cur.close()
                conn.close()
            self.insert_existence_proizv(self.tableRamProizv)
            self.insert_rb_sklad(self.tableRamProizv)  # Загрузка rb для визаулизции

    def load_proizv_disk(self):
        self.tableDiskProizv.clearSelection()
        self.tableDiskProizv.clear()
        self.tableDiskProizv.setRowCount(0)
        self.dict_proizv_disk_name.clear()
        conn = None
        cur = None
        try:
            conn = psycopg2.connect(database="confPc",
                                    user="postgres",
                                    password="2001",
                                    host="localhost",
                                    port="5432")
            cur = conn.cursor()
            cur.callproc("get_proizv_disk")
            row_count = 0
            for row in cur:
                self.tableDiskProizv.setRowCount(row_count + 1)
                # 0 столбец - radiobutton
                # 1 столбец - индикатор состояния договора
                self.tableDiskProizv.setItem(row_count, 2, QtWidgets.QTableWidgetItem(str(row[1])))
                self.dict_proizv_disk_name[row[0]] = row[2]  # Сохраняем id производителя и его имя
                self.tableDiskProizv.setItem(row_count, 3, QtWidgets.QTableWidgetItem(row[2]))
                row_count += 1

        except (Exception, psycopg2.DatabaseError) as error:
            dialog = DialogOk("Ошибка", error)
            dialog.show()

        finally:
            if conn:
                cur.close()
                conn.close()
            self.insert_existence_proizv(self.tableDiskProizv)
            self.insert_rb_sklad(self.tableDiskProizv)  # Загрузка rb для визаулизции

    def load_proizv_power(self):
        self.tablePowerProizv.clearSelection()
        self.tablePowerProizv.clear()
        self.tablePowerProizv.setRowCount(0)
        self.dict_proizv_power_name.clear()
        conn = None
        cur = None
        try:
            conn = psycopg2.connect(database="confPc",
                                    user="postgres",
                                    password="2001",
                                    host="localhost",
                                    port="5432")
            cur = conn.cursor()
            cur.callproc("get_proizv_power")
            row_count = 0
            for row in cur:
                self.tablePowerProizv.setRowCount(row_count + 1)
                # 0 столбец - radiobutton
                # 1 столбец - индикатор состояния договора
                self.tablePowerProizv.setItem(row_count, 2, QtWidgets.QTableWidgetItem(str(row[1])))
                self.dict_proizv_power_name[row[0]] = row[2]  # Сохраняем id производителя и его имя
                self.tablePowerProizv.setItem(row_count, 3, QtWidgets.QTableWidgetItem(row[2]))
                row_count += 1

        except (Exception, psycopg2.DatabaseError) as error:
            dialog = DialogOk("Ошибка", error)
            dialog.show()

        finally:
            if conn:
                cur.close()
                conn.close()
            self.insert_existence_proizv(self.tablePowerProizv)
            self.insert_rb_sklad(self.tablePowerProizv)  # Загрузка rb для визаулизции

    def load_proizv_body(self):
        self.tableBodyProizv.clearSelection()
        self.tableBodyProizv.clear()
        self.tableBodyProizv.setRowCount(0)
        self.dict_proizv_body_name.clear()
        conn = None
        cur = None
        try:
            conn = psycopg2.connect(database="confPc",
                                    user="postgres",
                                    password="2001",
                                    host="localhost",
                                    port="5432")
            cur = conn.cursor()
            cur.callproc("get_proizv_body")
            row_count = 0
            for row in cur:
                self.tableBodyProizv.setRowCount(row_count + 1)
                # 0 столбец - radiobutton
                # 1 столбец - индикатор состояния договора
                self.tableBodyProizv.setItem(row_count, 2, QtWidgets.QTableWidgetItem(str(row[1])))
                self.dict_proizv_body_name[row[0]] = row[2]  # Сохраняем id производителя и его имя
                self.tableBodyProizv.setItem(row_count, 3, QtWidgets.QTableWidgetItem(row[2]))
                row_count += 1

        except (Exception, psycopg2.DatabaseError) as error:
            dialog = DialogOk("Ошибка", error)
            dialog.show()

        finally:
            if conn:
                cur.close()
                conn.close()
            self.insert_existence_proizv(self.tableBodyProizv)
            self.insert_rb_sklad(self.tableBodyProizv)  # Загрузка rb для визаулизции

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
                        case self.tableCoolProizv:  # Перезаписываем в БД и обновляем таблицу
                            if table.item(table.currentRow(), 2).text() == "True":
                                cur.callproc('update_cool_dogovor', [False, table.item(table.currentRow(),
                                                                                       3).text()])
                            else:
                                cur.callproc('update_cool_dogovor', [True, table.item(table.currentRow(),
                                                                                      3).text()])
                            conn.commit()
                            self.load_proizv_cool()
                        case self.tableRamProizv:  # Перезаписываем в БД и обновляем таблицу
                            if table.item(table.currentRow(), 2).text() == "True":
                                cur.callproc('update_ram_dogovor', [False, table.item(table.currentRow(),
                                                                                      3).text()])
                            else:
                                cur.callproc('update_ram_dogovor', [True, table.item(table.currentRow(),
                                                                                     3).text()])
                            conn.commit()
                            self.load_proizv_ram()
                        case self.tableDiskProizv:  # Перезаписываем в БД и обновляем таблицу
                            if table.item(table.currentRow(), 2).text() == "True":
                                cur.callproc('update_disk_dogovor', [False, table.item(table.currentRow(),
                                                                                       3).text()])
                            else:
                                cur.callproc('update_disk_dogovor', [True, table.item(table.currentRow(),
                                                                                      3).text()])
                            conn.commit()
                            self.load_proizv_disk()
                        case self.tablePowerProizv:  # Перезаписываем в БД и обновляем таблицу
                            if table.item(table.currentRow(), 2).text() == "True":
                                cur.callproc('update_power_dogovor', [False, table.item(table.currentRow(),
                                                                                        3).text()])
                            else:
                                cur.callproc('update_power_dogovor', [True, table.item(table.currentRow(),
                                                                                       3).text()])
                            conn.commit()
                            self.load_proizv_power()
                        case self.tableBodyProizv:  # Перезаписываем в БД и обновляем таблицу
                            if table.item(table.currentRow(), 2).text() == "True":
                                cur.callproc('update_body_dogovor', [False, table.item(table.currentRow(),
                                                                                       3).text()])
                            else:
                                cur.callproc('update_body_dogovor', [True, table.item(table.currentRow(),
                                                                                      3).text()])
                            conn.commit()
                            self.load_proizv_body()
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
        self.rbShowOrders.setChecked(False)
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
                        self.fill_tabs_sklad(page)
                    else:
                        self.dict_video_kol.clear()
                        self.dict_video_proizv.clear()
                        self.dict_video_name.clear()
                        cur.callproc("get_all_videocard")  # Получаем данные о всех видеокартах
                        self.fill_table_sklad(page, cur)  # Заполняем таблицу
                        self.fill_tabs_sklad(page)
                        cur.callproc("get_all_videocard")
                        for row in cur:  # Заполняем словари данными о видеокартах
                            self.dict_video_kol[row[2]] = row[0]
                            self.dict_video_proizv[row[2]] = row[3]
                            self.dict_video_name[row[2]] = row[4]
                case 1:
                    if self.rbSklad.isChecked():
                        cur.callproc("get_having_processor")  # Получаем данные о имеющихся видеокартах
                        self.fill_table_sklad(page, cur)  # Заполняем таблицу
                        self.fill_tabs_sklad(page)
                    else:
                        self.dict_proc_kol.clear()
                        self.dict_proc_proizv.clear()
                        self.dict_proc_name.clear()
                        cur.callproc("get_all_processor")  # Получаем данные о всех видеокартах
                        self.fill_table_sklad(page, cur)  # Заполняем таблицу
                        self.fill_tabs_sklad(page)
                        cur.callproc("get_all_processor")
                        for row in cur:  # Заполняем словари данными о видеокартах
                            self.dict_proc_kol[row[2]] = row[0]
                            self.dict_proc_proizv[row[2]] = row[3]
                            self.dict_proc_name[row[2]] = row[4]
                case 2:
                    if self.rbSklad.isChecked():
                        cur.callproc("get_having_motherboard")  # Получаем данные о имеющихся мат.платах
                        self.fill_table_sklad(page, cur)  # Заполняем таблицу
                        self.fill_tabs_sklad(page)
                    else:
                        self.dict_mother_kol.clear()
                        self.dict_mother_proizv.clear()
                        self.dict_mother_name.clear()
                        cur.callproc("get_all_motherboard")
                        self.fill_table_sklad(page, cur)
                        self.fill_tabs_sklad(page)
                        cur.callproc("get_all_motherboard")
                        for row in cur:
                            self.dict_mother_kol[row[2]] = row[0]
                            self.dict_mother_proizv[row[2]] = row[3]
                            self.dict_mother_name[row[2]] = row[4]
                case 3:
                    if self.rbSklad.isChecked():
                        cur.callproc("get_having_cool")
                        self.fill_table_sklad(page, cur)
                        self.fill_tabs_sklad(page)
                    else:
                        self.dict_cool_kol.clear()
                        self.dict_cool_proizv.clear()
                        self.dict_cool_name.clear()
                        cur.callproc("get_all_cool")
                        self.fill_table_sklad(page, cur)
                        self.fill_tabs_sklad(page)
                        cur.callproc("get_all_cool")
                        for row in cur:
                            self.dict_cool_kol[row[2]] = row[0]
                            self.dict_cool_proizv[row[2]] = row[3]
                            self.dict_cool_name[row[2]] = row[4]
                case 4:
                    if self.rbSklad.isChecked():
                        cur.callproc("get_having_ram")
                        self.fill_table_sklad(page, cur)
                        self.fill_tabs_sklad(page)
                    else:
                        self.dict_ram_kol.clear()
                        self.dict_ram_proizv.clear()
                        self.dict_ram_name.clear()
                        cur.callproc("get_all_ram")
                        self.fill_table_sklad(page, cur)
                        self.fill_tabs_sklad(page)
                        cur.callproc("get_all_ram")
                        for row in cur:
                            self.dict_ram_kol[row[2]] = row[0]
                            self.dict_ram_proizv[row[2]] = row[3]
                            self.dict_ram_name[row[2]] = row[4]
                case 5:
                    if self.rbSklad.isChecked():
                        cur.callproc("get_having_disk")
                        self.fill_table_sklad(page, cur)
                        self.fill_tabs_sklad(page)
                    else:
                        self.dict_disk_kol.clear()
                        self.dict_disk_proizv.clear()
                        self.dict_disk_name.clear()
                        cur.callproc("get_all_disk")
                        self.fill_table_sklad(page, cur)
                        self.fill_tabs_sklad(page)
                        cur.callproc("get_all_disk")
                        for row in cur:
                            self.dict_disk_kol[row[2]] = row[0]
                            self.dict_disk_proizv[row[2]] = row[3]
                            self.dict_disk_name[row[2]] = row[4]
                case 6:
                    if self.rbSklad.isChecked():
                        cur.callproc("get_having_power")
                        self.fill_table_sklad(page, cur)
                        self.fill_tabs_sklad(page)
                    else:
                        self.dict_power_kol.clear()
                        self.dict_power_proizv.clear()
                        self.dict_power_name.clear()
                        cur.callproc("get_all_power")
                        self.fill_table_sklad(page, cur)
                        self.fill_tabs_sklad(page)
                        cur.callproc("get_all_power")
                        for row in cur:
                            self.dict_power_kol[row[2]] = row[0]
                            self.dict_power_proizv[row[2]] = row[3]
                            self.dict_power_name[row[2]] = row[4]
                case 7:
                    if self.rbSklad.isChecked():
                        cur.callproc("get_having_body")
                        self.fill_table_sklad(page, cur)
                        self.fill_tabs_sklad(page)
                    else:
                        self.dict_body_kol.clear()
                        self.dict_body_proizv.clear()
                        self.dict_body_name.clear()
                        cur.callproc("get_all_body")
                        self.fill_table_sklad(page, cur)
                        self.fill_tabs_sklad(page)
                        cur.callproc("get_all_body")
                        for row in cur:
                            self.dict_body_kol[row[2]] = row[0]
                            self.dict_body_proizv[row[2]] = row[3]
                            self.dict_body_name[row[2]] = row[4]

        except (Exception, psycopg2.DatabaseError) as error:
            dialog = DialogOk("Ошибка", str(error))
            dialog.show()

        finally:
            if conn:
                cur.close()
                conn.close()

    # Метод заполнения полей таблицы склада по фильтрующему запросу из БД
    def fill_table_sklad(self, page, cur):
        self.tableSklad.clear()
        self.tableSklad.clearSelection()
        self.tableSklad.setRowCount(0)
        self.tableSklad.setSortingEnabled(False)
        row_count = 0
        match page:
            case 0:  # Заполнение таблицы видеокартами
                if not self.rbShowOrders.isChecked():  # Если не выбрано отображение заказов
                    self.tableSklad.setColumnCount(20)  # Число столбцов в видеокарте
                    self.tableSklad.setHorizontalHeaderLabels(["", "", "Кол-во",
                                                               "Производитель", "Название", "Игровая", "Произв. чипа",
                                                               "Наименов. чипа", "Объём памяти", "Тип памяти",
                                                               "Частота процессора", "Шина", "Интерфейс",
                                                               "Монитор", "Разрешение", "TDP", "Длина",
                                                               "Pin-контакты", "Кол-во pin", "Цена"])
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
                        self.tableSklad.setItem(row_count, 17, QtWidgets.QTableWidgetItem(str(row[17])))
                        self.tableSklad.setItem(row_count, 18, QtWidgets.QTableWidgetItem(str(row[18])))
                        self.tableSklad.setItem(row_count, 19, QtWidgets.QTableWidgetItem(str(row[19])))
                        # item2.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
                        self.insert_rb_sklad(self.tableSklad)
                        row_count += 1
                else:  # Вывод зазаказнных комплектующих с количеством
                    self.tableSklad.setColumnCount(22)  # Число столбцов в видеокарте
                    self.tableSklad.setHorizontalHeaderLabels(["", "", "Кол-во(склад)", "Дата заказа",
                                                               "Кол-во(заказ)", "Производитель", "Название",
                                                               "Игровая", "Произв. чипа", "Наименов. чипа",
                                                               "Объём памяти", "Тип памяти",
                                                               "Частота процессора", "Шина", "Интерфейс",
                                                               "Монитор", "Разрешение", "TDP", "Длина",
                                                               "Pin-контакты", "Кол-во pin", "Цена"])
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
                        self.tableSklad.setItem(row_count, 17, QtWidgets.QTableWidgetItem(str(row[17])))
                        self.tableSklad.setItem(row_count, 18, QtWidgets.QTableWidgetItem(str(row[18])))
                        self.tableSklad.setItem(row_count, 19, QtWidgets.QTableWidgetItem(str(row[19])))
                        self.tableSklad.setItem(row_count, 20, QtWidgets.QTableWidgetItem(str(row[20])))
                        self.tableSklad.setItem(row_count, 21, QtWidgets.QTableWidgetItem(str(row[21])))
                        # item2.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
                        self.insert_rb_sklad(self.tableSklad)
                        row_count += 1
            case 1:
                if not self.rbShowOrders.isChecked():  # Если не выбрано отображение заказов
                    self.tableSklad.setColumnCount(17)  # Число столбцов в процессоре
                    self.tableSklad.setHorizontalHeaderLabels(["", "", "Кол-во",
                                                               "Производитель", "Название", "Игровой", "Серия",
                                                               "Сокет", "Ядро", "Кол-во ядер", "Кэш",
                                                               "Частота процессора", "Тех. проц.", "Частота ОЗУ",
                                                               "Граф. процессор", "TDP", "Цена"])
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
                        row_count += 1
                else:
                    self.tableSklad.setColumnCount(19)  # Число столбцов в процессоре
                    self.tableSklad.setHorizontalHeaderLabels(["", "", "Кол-во(склад)", "Дата заказа", "Кол-во(заказ)",
                                                               "Производитель", "Название", "Игровой", "Серия",
                                                               "Сокет", "Ядро", "Кол-во ядер", "Кэш",
                                                               "Частота процессора", "Тех. проц.", "Частота ОЗУ",
                                                               "Граф. процессор", "TDP", "Цена"])
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
                        self.tableSklad.setItem(row_count, 17, QtWidgets.QTableWidgetItem(str(row[17])))
                        self.tableSklad.setItem(row_count, 18, QtWidgets.QTableWidgetItem(str(row[18])))
                        row_count += 1
            case 2:
                if not self.rbShowOrders.isChecked():  # Если не выбрано отображение заказов
                    self.tableSklad.setColumnCount(20)  # Число столбцов в мат. плате
                    self.tableSklad.setHorizontalHeaderLabels(["", "", "Кол-во",
                                                               "Производитель", "Название", "Игровой", "Cокет",
                                                               "Чипсет", "Формфактор", "PCI-E", "Тип ОЗУ", "Слоты ОЗУ",
                                                               "Макс. объём ОЗУ", "Макс. частота ОЗУ", "Слоты М2",
                                                               "Разъёмы SATA", "Pin-охлаждение", "Pin-процессор",
                                                               "Кол-во pin", "Цена"])
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
                        self.tableSklad.setItem(row_count, 17, QtWidgets.QTableWidgetItem(str(row[17])))
                        self.tableSklad.setItem(row_count, 18, QtWidgets.QTableWidgetItem(str(row[18])))
                        self.tableSklad.setItem(row_count, 19, QtWidgets.QTableWidgetItem(str(row[19])))
                        row_count += 1
                else:
                    self.tableSklad.setColumnCount(22)  # Число столбцов в мат. плате
                    self.tableSklad.setHorizontalHeaderLabels(["", "", "Кол-во(склад)", "Дата заказа",
                                                               "Кол-во(заказ)", "Производитель", "Название",
                                                               "Игровой", "Cокет", "Чипсет", "Формфактор", "PCI-E",
                                                               "Тип ОЗУ", "Слоты ОЗУ", "Макс. объём ОЗУ",
                                                               "Макс. частота ОЗУ", "Слоты М2",
                                                               "Разъёмы SATA", "Pin-охлаждение", "Pin-процессор",
                                                               "Кол-во pin", "Цена"])
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
                        self.tableSklad.setItem(row_count, 17, QtWidgets.QTableWidgetItem(str(row[17])))
                        self.tableSklad.setItem(row_count, 18, QtWidgets.QTableWidgetItem(str(row[18])))
                        self.tableSklad.setItem(row_count, 19, QtWidgets.QTableWidgetItem(str(row[19])))
                        self.tableSklad.setItem(row_count, 20, QtWidgets.QTableWidgetItem(str(row[20])))
                        self.tableSklad.setItem(row_count, 21, QtWidgets.QTableWidgetItem(str(row[21])))
                        row_count += 1
            case 3:
                if not self.rbShowOrders.isChecked():  # Если не выбрано отображение заказов
                    self.tableSklad.setColumnCount(14)  # Число столбцов в охлаждении
                    self.tableSklad.setHorizontalHeaderLabels(["", "", "Кол-во",
                                                               "Производитель", "Название", "Конструкция",
                                                               "Тип охл.", "Сокеты", "Трубы", "Высота",
                                                               "Рассеиваемость", "Напряжение", "Pin-коннектор",
                                                               "Цена"])
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
                        row_count += 1
                else:
                    self.tableSklad.setColumnCount(16)  # Число столбцов в охлаждении
                    self.tableSklad.setHorizontalHeaderLabels(["", "", "Кол-во(склад)", "Дата заказа",
                                                                   "Кол-во(заказ)",
                                                               "Производитель", "Название", "Конструкция",
                                                               "Тип охл.", "Сокеты", "Трубы", "Высота",
                                                               "Рассеиваемость", "Напряжение", "Pin-коннектор",
                                                               "Цена"])
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
                        row_count += 1
            case 4:
                if not self.rbShowOrders.isChecked():  # Если не выбрано отображение заказов
                    self.tableSklad.setColumnCount(13)  # Число столбцов в оперативной памяти
                    self.tableSklad.setHorizontalHeaderLabels(["", "", "Кол-во",
                                                               "Производитель", "Название", "Игровой", "Тип",
                                                               "Объём", "Тактовая частота", "Кол-во модулей",
                                                               "CAS-Latency", "Напряжение", "Цена"])
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
                        row_count += 1
                else:
                    self.tableSklad.setColumnCount(15)  # Число столбцов в оперативной памяти
                    self.tableSklad.setHorizontalHeaderLabels(["", "", "Кол-во(склад)", "Дата заказа",
                                                                   "Кол-во(заказ)",
                                                               "Производитель", "Название", "Игровой", "Тип",
                                                               "Объём", "Тактовая частота", "Кол-во модулей",
                                                               "CAS-Latency", "Напряжение", "Цена"])
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
                        row_count += 1
            case 5:
                if not self.rbShowOrders.isChecked():  # Если не выбрано отображение заказов
                    self.tableSklad.setColumnCount(12)  # Число столбцов в накопителе
                    self.tableSklad.setHorizontalHeaderLabels(["", "", "Кол-во",
                                                               "Производитель", "Название", "Тип", "Объём",
                                                               "Интерфейс", "Скорость чтения", "Скорость записи",
                                                               "RPM", "Цена"])
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
                        row_count += 1
                else:
                    self.tableSklad.setColumnCount(14)  # Число столбцов в накопителе
                    self.tableSklad.setHorizontalHeaderLabels(["", "",  "Кол-во(склад)", "Дата заказа",
                                                                   "Кол-во(заказ)",
                                                               "Производитель", "Название", "Тип", "Объём",
                                                               "Интерфейс", "Скорость чтения", "Скорость записи",
                                                               "RPM", "Цена"])
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
                        row_count += 1
            case 6:
                if not self.rbShowOrders.isChecked():  # Если не выбрано отображение заказов
                    self.tableSklad.setColumnCount(16)  # Число столбцов в блоке питания
                    self.tableSklad.setHorizontalHeaderLabels(["", "", "Кол-во", "Производитель", "Название",
                                                               "Формафактор", "Длина", "Мощность", "Сертификат",
                                                               "Основной разъём питания", "Количество разъёмов SATA",
                                                               "Pin-процессор", "Кол-во pin", "Pin-видеокарта",
                                                               "Кол-во pin", "Цена"])
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
                        row_count += 1
                else:
                    self.tableSklad.setColumnCount(18)  # Число столбцов в блоке питания
                    self.tableSklad.setHorizontalHeaderLabels(["", "", "Кол-во(склад)", "Дата заказа",
                                                                   "Кол-во(заказ)", "Производитель", "Название",
                                                               "Формафактор", "Длина", "Мощность", "Сертификат",
                                                               "Основной разъём питания", "Количество разъёмов SATA",
                                                               "Pin-процессор", "Кол-во pin", "Pin-видеокарта",
                                                               "Кол-во pin", "Цена"])
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
                        self.tableSklad.setItem(row_count, 17, QtWidgets.QTableWidgetItem(str(row[17])))
                        row_count += 1
            case 7:
                if not self.rbShowOrders.isChecked():  # Если не выбрано отображение заказов
                    self.tableSklad.setColumnCount(15)  # Число столбцов в корпусеы
                    self.tableSklad.setHorizontalHeaderLabels(["", "", "Кол-во",
                                                               "Производитель", "Название", "Игровой", "Тип корпуса",
                                                               "Форм-фактор мат. платы", "Форм-фактор БП",
                                                               "Макс. длина виеокарты", "Макс. высота охлаждения",
                                                               "Макс. длина БП", "Масса", "Цвет", "Цена"])
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
                        row_count += 1
                else:
                    self.tableSklad.setColumnCount(17)  # Число столбцов в корпусеы
                    self.tableSklad.setHorizontalHeaderLabels(["", "", "Кол-во(склад)", "Дата заказа",
                                                                   "Кол-во(заказ)",
                                                               "Производитель", "Название", "Игровой", "Тип корпуса",
                                                               "Форм-фактор мат. платы", "Форм-фактор БП",
                                                               "Макс. длина виеокарты", "Макс. высота охлаждения",
                                                               "Макс. длина БП", "Масса", "Цвет", "Цена"])
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
                        row_count += 1

        self.insert_rb_sklad(self.tableSklad)
        self.tableSklad.setSortingEnabled(True)
        self.tableSklad.resizeColumnsToContents()

    # Метод загрузки всех комплектующих с БД в страницу конфигуратора
    # Вызывать после каждого обновления записей, а также при запуске
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
                    cur.callproc("get_all_videocard")
                    self.fill_table_conf(page, cur)
                case 1:
                    cur.callproc("get_all_processor")
                    self.fill_table_conf(page, cur)
                case 2:
                    cur.callproc("get_all_motherboard")
                    self.fill_table_conf(page, cur)
                case 3:
                    cur.callproc("get_all_cool")
                    self.fill_table_conf(page, cur)
                case 4:
                    cur.callproc("get_all_ram")
                    self.fill_table_conf(page, cur)
                case 5:
                    cur.callproc("get_all_disk")
                    self.fill_table_conf(page, cur)
                case 6:
                    cur.callproc("get_all_power")
                    self.fill_table_conf(page, cur)
                case 7:
                    cur.callproc("get_all_body")
                    self.fill_table_conf(page, cur)

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
                self.tableConfVideo.setColumnCount(16)  # Число столбцов в видеокарте конфигуратора
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
                    self.tableConfVideo.setItem(row_count, 9, QtWidgets.QTableWidgetItem(str(row[12])))
                    self.tableConfVideo.setItem(row_count, 10, QtWidgets.QTableWidgetItem(str(row[14])))
                    self.tableConfVideo.setItem(row_count, 11, QtWidgets.QTableWidgetItem(str(row[15])))
                    self.tableConfVideo.setItem(row_count, 12, QtWidgets.QTableWidgetItem(str(row[16])))
                    self.tableConfVideo.setItem(row_count, 13, QtWidgets.QTableWidgetItem(str(row[17])))
                    self.tableConfVideo.setItem(row_count, 14, QtWidgets.QTableWidgetItem(str(row[18])))
                    self.tableConfVideo.setItem(row_count, 15, QtWidgets.QTableWidgetItem(str(row[19])))
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
            case 2:  # Заполнение таблицы конфигуратора мат. платами
                self.tableConfMother.clear()
                self.tableConfMother.clearSelection()
                self.tableConfMother.setRowCount(0)
                self.tableConfMother.setColumnCount(17)  # Число столбцов в процессорах конфигуратора
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
                    self.tableConfMother.setItem(row_count, 13, QtWidgets.QTableWidgetItem(str(row[16])))
                    self.tableConfMother.setItem(row_count, 14, QtWidgets.QTableWidgetItem(str(row[17])))
                    self.tableConfMother.setItem(row_count, 15, QtWidgets.QTableWidgetItem(str(row[18])))
                    self.tableConfMother.setItem(row_count, 16, QtWidgets.QTableWidgetItem(str(row[19])))
                    row_count += 1
                self.insert_rb(self.tableConfMother)
                self.tableConfMother.resizeColumnsToContents()
            case 3:  # Заполнение таблицы конфигуратора охлаждением
                self.tableConfCool.clear()
                self.tableConfCool.clearSelection()
                self.tableConfCool.setRowCount(0)
                self.tableConfCool.setColumnCount(12)  # Число столбцов в процессорах конфигуратора
                for row in cur:
                    self.tableConfCool.setRowCount(row_count + 1)
                    self.insert_existence_complect(self.tableConfCool, row_count, row[1])
                    self.tableConfCool.setItem(row_count, 2, QtWidgets.QTableWidgetItem(str(row[4])))
                    self.tableConfCool.setItem(row_count, 3, QtWidgets.QTableWidgetItem(str(row[5])))
                    self.tableConfCool.setItem(row_count, 4, QtWidgets.QTableWidgetItem(str(row[6])))
                    self.tableConfCool.setItem(row_count, 5, QtWidgets.QTableWidgetItem(str(row[7])))
                    self.tableConfCool.setItem(row_count, 6, QtWidgets.QTableWidgetItem(str(row[8])))
                    self.tableConfCool.setItem(row_count, 7, QtWidgets.QTableWidgetItem(str(row[9])))
                    self.tableConfCool.setItem(row_count, 8, QtWidgets.QTableWidgetItem(str(row[10])))
                    self.tableConfCool.setItem(row_count, 9, QtWidgets.QTableWidgetItem(str(row[11])))
                    self.tableConfCool.setItem(row_count, 10, QtWidgets.QTableWidgetItem(str(row[12])))
                    self.tableConfCool.setItem(row_count, 11, QtWidgets.QTableWidgetItem(str(row[13])))
                    row_count += 1
                self.insert_rb(self.tableConfCool)
                self.tableConfCool.resizeColumnsToContents()
            case 4:  # Заполнение таблицы конфигуратора ОЗУ
                self.tableConfRam.clear()
                self.tableConfRam.clearSelection()
                self.tableConfRam.setRowCount(0)
                self.tableConfRam.setColumnCount(10)  # Число столбцов в процессорах конфигуратора
                for row in cur:
                    self.tableConfRam.setRowCount(row_count + 1)
                    self.insert_existence_complect(self.tableConfRam, row_count, row[1])
                    self.tableConfRam.setItem(row_count, 2, QtWidgets.QTableWidgetItem(str(row[4])))
                    self.tableConfRam.setItem(row_count, 3, QtWidgets.QTableWidgetItem(str(row[6])))
                    self.tableConfRam.setItem(row_count, 4, QtWidgets.QTableWidgetItem(str(row[7])))
                    self.tableConfRam.setItem(row_count, 5, QtWidgets.QTableWidgetItem(str(row[8])))
                    self.tableConfRam.setItem(row_count, 6, QtWidgets.QTableWidgetItem(str(row[9])))
                    self.tableConfRam.setItem(row_count, 7, QtWidgets.QTableWidgetItem(str(row[10])))
                    self.tableConfRam.setItem(row_count, 8, QtWidgets.QTableWidgetItem(str(row[11])))
                    self.tableConfRam.setItem(row_count, 9, QtWidgets.QTableWidgetItem(str(row[12])))
                    row_count += 1
                self.insert_rb(self.tableConfRam)
                self.tableConfRam.resizeColumnsToContents()
            case 5:  # Заполнение таблицы конфигуратора накопителями
                self.tableConfDisk.clear()
                self.tableConfDisk.clearSelection()
                self.tableConfDisk.setRowCount(0)
                self.tableConfDisk.setColumnCount(10)  # Число столбцов в процессорах конфигуратора
                for row in cur:
                    self.tableConfDisk.setRowCount(row_count + 1)
                    self.insert_existence_complect(self.tableConfDisk, row_count, row[1])
                    self.tableConfDisk.setItem(row_count, 2, QtWidgets.QTableWidgetItem(str(row[4])))
                    self.tableConfDisk.setItem(row_count, 3, QtWidgets.QTableWidgetItem(str(row[5])))
                    self.tableConfDisk.setItem(row_count, 4, QtWidgets.QTableWidgetItem(str(row[6])))
                    self.tableConfDisk.setItem(row_count, 5, QtWidgets.QTableWidgetItem(str(row[7])))
                    self.tableConfDisk.setItem(row_count, 6, QtWidgets.QTableWidgetItem(str(row[8])))
                    self.tableConfDisk.setItem(row_count, 7, QtWidgets.QTableWidgetItem(str(row[9])))
                    self.tableConfDisk.setItem(row_count, 8, QtWidgets.QTableWidgetItem(str(row[10])))
                    self.tableConfDisk.setItem(row_count, 9, QtWidgets.QTableWidgetItem(str(row[11])))
                    row_count += 1
                self.insert_rb(self.tableConfDisk)
                self.tableConfDisk.resizeColumnsToContents()
            case 6:  # Заполнение таблицы конфигуратора блока питания
                self.tableConfPower.clear()
                self.tableConfPower.clearSelection()
                self.tableConfPower.setRowCount(0)
                self.tableConfPower.setColumnCount(14)  # Число столбцов в процессорах конфигуратора
                for row in cur:
                    self.tableConfPower.setRowCount(row_count + 1)
                    self.insert_existence_complect(self.tableConfPower, row_count, row[1])
                    self.tableConfPower.setItem(row_count, 2, QtWidgets.QTableWidgetItem(str(row[4])))
                    self.tableConfPower.setItem(row_count, 3, QtWidgets.QTableWidgetItem(str(row[5])))
                    self.tableConfPower.setItem(row_count, 4, QtWidgets.QTableWidgetItem(str(row[6])))
                    self.tableConfPower.setItem(row_count, 5, QtWidgets.QTableWidgetItem(str(row[7])))
                    self.tableConfPower.setItem(row_count, 6, QtWidgets.QTableWidgetItem(str(row[8])))
                    self.tableConfPower.setItem(row_count, 7, QtWidgets.QTableWidgetItem(str(row[9])))
                    self.tableConfPower.setItem(row_count, 8, QtWidgets.QTableWidgetItem(str(row[10])))
                    self.tableConfPower.setItem(row_count, 9, QtWidgets.QTableWidgetItem(str(row[11])))
                    self.tableConfPower.setItem(row_count, 10, QtWidgets.QTableWidgetItem(str(row[12])))
                    self.tableConfPower.setItem(row_count, 11, QtWidgets.QTableWidgetItem(str(row[13])))
                    self.tableConfPower.setItem(row_count, 12, QtWidgets.QTableWidgetItem(str(row[14])))
                    self.tableConfPower.setItem(row_count, 13, QtWidgets.QTableWidgetItem(str(row[15])))
                    row_count += 1
                self.insert_rb(self.tableConfPower)
                self.tableConfPower.resizeColumnsToContents()
            case 7:  # Заполнение таблицы конфигуратора корпусов
                self.tableConfBody.clear()
                self.tableConfBody.clearSelection()
                self.tableConfBody.setRowCount(0)
                self.tableConfBody.setColumnCount(12)
                for row in cur:
                    self.tableConfBody.setRowCount(row_count + 1)
                    self.insert_existence_complect(self.tableConfBody, row_count, row[1])
                    self.tableConfBody.setItem(row_count, 2, QtWidgets.QTableWidgetItem(str(row[4])))
                    self.tableConfBody.setItem(row_count, 3, QtWidgets.QTableWidgetItem(str(row[6])))
                    self.tableConfBody.setItem(row_count, 4, QtWidgets.QTableWidgetItem(str(row[7])))
                    self.tableConfBody.setItem(row_count, 5, QtWidgets.QTableWidgetItem(str(row[8])))
                    self.tableConfBody.setItem(row_count, 6, QtWidgets.QTableWidgetItem(str(row[9])))
                    self.tableConfBody.setItem(row_count, 7, QtWidgets.QTableWidgetItem(str(row[10])))
                    self.tableConfBody.setItem(row_count, 8, QtWidgets.QTableWidgetItem(str(row[11])))
                    self.tableConfBody.setItem(row_count, 9, QtWidgets.QTableWidgetItem(str(row[12])))
                    self.tableConfBody.setItem(row_count, 10, QtWidgets.QTableWidgetItem(str(row[13])))
                    self.tableConfBody.setItem(row_count, 11, QtWidgets.QTableWidgetItem(str(row[14])))
                    row_count += 1
                self.insert_rb(self.tableConfBody)
                self.tableConfBody.resizeColumnsToContents()

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
    def current_sklad(self):
        cur_row = self.tableSklad.currentRow()
        count_col = self.tableSklad.columnCount()
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

    def block_label(self, field, x=None):
        if x:
            field.setStyleSheet("color:gray;")
        else:
            field.setStyleSheet("color:gray;"
                                "border-top: 1px dotted rgb(120,120,120);"
                                "border-bottom: 1px dotted rgb(120,120,120);")

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
        :param get_row: Строка, на которую нажал пользователь
        """
        # Если была нажата кнопка вывода заказов, то удаляем лишние 2 значения с начала списка
        # В обычном случае сюда поступает list[kol, pr_name ..].
        # С включённым заказом сюда поступает list[kol, date, kol_order, pr_name ..]. Удаление 2х эл-ов
        if self.rbShowOrders.isChecked():
            if type(row) is list:
                del row[0]
                del row[0]
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
                        win_add_change = adding.AddChangeVideoWindow(self, new_bool, list_all_pr,
                                                                     self.dict_proizv_video_name,
                                                                     self.dict_video_name)
                        self.block_lineedit(win_add_change.leKol, "")
                        win_add_change.show()
                else:  # Если false - совершаем заказ компл. на склад
                    if type(row) is str:  # Если пришел не список, а строка(ошибка) - вывод окна с ошибкой
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
                            win_add_change = adding.AddChangeVideoWindow(self, new_bool, row[1],
                                                                         self.dict_proizv_video_name,
                                                                         self.dict_video_name)
                            self.block_combobox(win_add_change.cbProizv, row[1])
                            self.block_lineedit(win_add_change.leFullName, row[2])
                            self.block_combobox(win_add_change.cbGaming, row[3])
                            self.block_combobox(win_add_change.cbChipCreator, row[4])
                            self.block_lineedit(win_add_change.leChipName, row[5])
                            self.block_lineedit(win_add_change.leVolume, row[6])
                            self.block_lineedit(win_add_change.leType, row[7])
                            self.block_lineedit(win_add_change.leFreq, row[8])
                            self.block_lineedit(win_add_change.leBus, row[9])
                            self.block_combobox(win_add_change.cbInterface, row[10])
                            self.block_combobox(win_add_change.cbMonitor, row[11])
                            self.block_combobox(win_add_change.cbResolution, row[12])
                            self.block_lineedit(win_add_change.leTdp, row[13])
                            self.block_lineedit(win_add_change.leLength, row[14])
                            self.block_combobox(win_add_change.cbPinVideo, row[15])
                            self.block_combobox(win_add_change.cbPinVideoKol, row[16])
                            self.block_lineedit(win_add_change.lePrice, row[17])
                            self.block_label(win_add_change.lbPin1)
                            self.block_label(win_add_change.lbPinX, 'x')
                            win_add_change.show()
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
                        win_add_change = adding.AddChangeProcWindow(self, new_bool, list_all_pr,
                                                                    self.dict_proizv_proc_name,
                                                                    self.dict_proc_name)
                        self.block_lineedit(win_add_change.leKol, "")
                        win_add_change.show()
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
                            win_add_change = adding.AddChangeProcWindow(self, new_bool, row[1],
                                                                        self.dict_proizv_proc_name,
                                                                        self.dict_proc_name)
                            self.block_combobox(win_add_change.cbProizv, row[1])
                            self.block_lineedit(win_add_change.leFullName, row[2])
                            self.block_combobox(win_add_change.cbGaming, row[3])
                            self.block_lineedit(win_add_change.leSeries, row[4])
                            self.block_lineedit(win_add_change.leSocket, row[5])
                            self.block_lineedit(win_add_change.leCore, row[6])
                            self.block_lineedit(win_add_change.leNcores, row[7])
                            self.block_lineedit(win_add_change.leCache, row[8])
                            self.block_lineedit(win_add_change.leFreq, row[9])
                            self.block_lineedit(win_add_change.leTechproc, row[10])
                            self.block_lineedit(win_add_change.leRamFreq, row[11])
                            self.block_lineedit(win_add_change.leGraphics, row[12])
                            self.block_lineedit(win_add_change.leTdp, row[13])
                            self.block_lineedit(win_add_change.lePrice, row[14])
                            win_add_change.show()
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
                        win_add_change = adding.AddChangeMotherWindow(self, new_bool, list_all_pr,
                                                                      self.dict_proizv_mother_name,
                                                                      self.dict_mother_name)
                        self.block_lineedit(win_add_change.leKol, "")
                        win_add_change.show()
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
                            win_add_change = adding.AddChangeMotherWindow(self, new_bool, row[1],
                                                                          self.dict_proizv_mother_name,
                                                                          self.dict_mother_name)
                            self.block_combobox(win_add_change.cbProizv, row[1])
                            self.block_lineedit(win_add_change.leFullName, row[2])
                            self.block_combobox(win_add_change.cbGaming, row[3])
                            self.block_lineedit(win_add_change.leSocket, row[4])
                            self.block_lineedit(win_add_change.leChipset, row[5])
                            self.block_combobox(win_add_change.cbFactor, row[6])
                            self.block_combobox(win_add_change.cbPcie, row[7])
                            self.block_combobox(win_add_change.cbRamType, row[8])
                            self.block_combobox(win_add_change.cbRamSlots, row[9])
                            self.block_lineedit(win_add_change.leFreqMax, row[10])
                            self.block_lineedit(win_add_change.leRamMax, row[11])
                            self.block_combobox(win_add_change.cbM2, row[12])
                            self.block_combobox(win_add_change.cbSata, row[13])
                            self.block_combobox(win_add_change.cbPinCool, row[14])
                            self.block_combobox(win_add_change.cbPinCpu, row[15])
                            self.block_combobox(win_add_change.cbPinCpuKol, row[16])
                            self.block_lineedit(win_add_change.lePrice, row[17])
                            self.block_label(win_add_change.lbPin1)
                            self.block_label(win_add_change.lbPin2)
                            self.block_label(win_add_change.lbX, 'x')
                            win_add_change.show()
            case 3:
                list_all_pr, list_exist_pr = self.get_list_proizvoditel(self.tableCoolProizv)
                if new_bool:  # Если True - добавляем новую запись: открываем пустое окно
                    self.tableSklad.clearSelection()
                    self.reset_radiobutton(self.tableSklad)
                    if self.tableCoolProizv.rowCount() == 0:  # Если нет производителей для добавления  (!=заказ)
                        dialog = DialogOk("Ошибка", "Нет производителей, чьё охлаждение можно добавить")
                        dialog.show()
                        if dialog.exec():
                            pass
                    else:  # Если таблица производителей охлаждения непустая
                        win_add_change = adding.AddChangeCoolWindow(self, new_bool, list_all_pr,
                                                                    self.dict_proizv_cool_name,
                                                                    self.dict_cool_name)
                        self.block_lineedit(win_add_change.leKol, "")
                        win_add_change.show()
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
                            win_add_change = adding.AddChangeCoolWindow(self, new_bool, row[1],
                                                                        self.dict_proizv_cool_name,
                                                                        self.dict_cool_name)
                            self.block_combobox(win_add_change.cbProizv, row[1])
                            self.block_lineedit(win_add_change.leFullName, row[2])
                            self.block_combobox(win_add_change.cbConstruction, row[3])
                            self.block_combobox(win_add_change.cbType, row[4])
                            self.block_lineedit(win_add_change.leSocket, row[5])
                            self.block_combobox(win_add_change.cbPipe, row[6])
                            self.block_lineedit(win_add_change.leHeight, row[7])
                            self.block_lineedit(win_add_change.leDisperse, row[8])
                            self.block_lineedit(win_add_change.leVoltage, row[9])
                            self.block_combobox(win_add_change.cbConnect, row[10])
                            self.block_lineedit(win_add_change.lePrice, row[11])
                            self.block_label(win_add_change.lbPin1)
                            win_add_change.show()
            case 4:
                list_all_pr, list_exist_pr = self.get_list_proizvoditel(self.tableRamProizv)
                if new_bool:  # Если True - добавляем новую запись: открываем пустое окно
                    self.tableSklad.clearSelection()
                    self.reset_radiobutton(self.tableSklad)
                    if self.tableRamProizv.rowCount() == 0:  # Если нет производителей для добавления  (!=заказ)
                        dialog = DialogOk("Ошибка", "Нет производителей, чьи ОЗУ можно добавить")
                        dialog.show()
                        if dialog.exec():
                            pass
                    else:  # Если таблица производителей охлаждения непустая
                        win_add_change = adding.AddChangeRamWindow(self, new_bool, list_all_pr,
                                                                   self.dict_proizv_ram_name,
                                                                   self.dict_ram_name)
                        self.block_lineedit(win_add_change.leKol, "")
                        win_add_change.show()
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
                            win_add_change = adding.AddChangeRamWindow(self, new_bool, row[1],
                                                                       self.dict_proizv_ram_name,
                                                                       self.dict_ram_name)
                            self.block_combobox(win_add_change.cbProizv, row[1])
                            self.block_lineedit(win_add_change.leFullName, row[2])
                            self.block_combobox(win_add_change.cbGaming, row[3])
                            self.block_combobox(win_add_change.cbRamType, row[4])
                            self.block_combobox(win_add_change.cbVolume, row[5])
                            self.block_lineedit(win_add_change.leFreq, row[6])
                            self.block_combobox(win_add_change.cbModule, row[7])
                            self.block_lineedit(win_add_change.leLatency, row[8])
                            self.block_lineedit(win_add_change.leVoltage, row[9])
                            self.block_lineedit(win_add_change.lePrice, row[10])
                            win_add_change.show()
            case 5:
                list_all_pr, list_exist_pr = self.get_list_proizvoditel(self.tableDiskProizv)
                if new_bool:  # Если True - добавляем новую запись: открываем пустое окно
                    self.tableSklad.clearSelection()
                    self.reset_radiobutton(self.tableSklad)
                    if self.tableDiskProizv.rowCount() == 0:  # Если нет производителей для добавления  (!=заказ)
                        dialog = DialogOk("Ошибка", "Нет производителей, чьи накопители можно добавить")
                        dialog.show()
                        if dialog.exec():
                            pass
                    else:  # Если таблица производителей охлаждения непустая
                        win_add_change = adding.AddChangeDiskWindow(self, new_bool, list_all_pr,
                                                                    self.dict_proizv_disk_name,
                                                                    self.dict_disk_name)
                        self.block_lineedit(win_add_change.leKol, "")
                        win_add_change.show()
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
                            win_add_change = adding.AddChangeDiskWindow(self, new_bool, row[1],
                                                                        self.dict_proizv_disk_name,
                                                                        self.dict_disk_name)
                            self.block_combobox(win_add_change.cbProizv, row[1])
                            self.block_lineedit(win_add_change.leFullName, row[2])
                            self.block_combobox(win_add_change.cbType, row[3])
                            self.block_lineedit(win_add_change.leVolume, row[4])
                            self.block_combobox(win_add_change.cbConnect, row[5])
                            self.block_lineedit(win_add_change.leRead, row[6])
                            self.block_lineedit(win_add_change.leWrite, row[7])
                            self.block_combobox(win_add_change.cbRpm, row[8])
                            self.block_lineedit(win_add_change.lePrice, row[9])
                            win_add_change.show()
            case 6:
                list_all_pr, list_exist_pr = self.get_list_proizvoditel(self.tablePowerProizv)
                if new_bool:  # Если True - добавляем новую запись: открываем пустое окно
                    self.tableSklad.clearSelection()
                    self.reset_radiobutton(self.tableSklad)
                    if self.tablePowerProizv.rowCount() == 0:  # Если нет производителей для добавления  (!=заказ)
                        dialog = DialogOk("Ошибка", "Нет производителей, чьи блоки питания можно добавить")
                        dialog.show()
                        if dialog.exec():
                            pass
                    else:  # Если таблица производителей охлаждения непустая
                        win_add_change = adding.AddChangePowerWindow(self, new_bool, list_all_pr,
                                                                     self.dict_proizv_power_name,
                                                                     self.dict_power_name)
                        self.block_lineedit(win_add_change.leKol, "")
                        win_add_change.show()
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
                            win_add_change = adding.AddChangePowerWindow(self, new_bool, row[1],
                                                                         self.dict_proizv_power_name,
                                                                         self.dict_power_name)
                            self.block_combobox(win_add_change.cbProizv, row[1])
                            self.block_lineedit(win_add_change.leFullName, row[2])
                            self.block_combobox(win_add_change.cbFPower, row[3])
                            self.block_lineedit(win_add_change.leLenPower, row[4])
                            self.block_lineedit(win_add_change.lePower, row[5])
                            self.block_combobox(win_add_change.cbCertificate, row[6])
                            self.block_combobox(win_add_change.cbPinMain, row[7])
                            self.block_lineedit(win_add_change.lePinSata, row[8])
                            self.block_combobox(win_add_change.cbPinCpu, row[9])
                            self.block_combobox(win_add_change.cbPinCpuKol, row[10])
                            self.block_combobox(win_add_change.cbPinVideo, row[11])
                            self.block_combobox(win_add_change.cbPinVideoKol, row[12])
                            self.block_lineedit(win_add_change.lePrice, row[13])
                            self.block_label(win_add_change.lbPin1)
                            self.block_label(win_add_change.lbPinX1, 'x')
                            self.block_label(win_add_change.lbPin2)
                            self.block_label(win_add_change.lbPinX2, 'x')
                            win_add_change.show()
            case 7:
                list_all_pr, list_exist_pr = self.get_list_proizvoditel(self.tableBodyProizv)
                if new_bool:  # Если True - добавляем новую запись: открываем пустое окно
                    self.tableSklad.clearSelection()
                    self.reset_radiobutton(self.tableSklad)
                    if self.tablePowerProizv.rowCount() == 0:  # Если нет производителей для добавления  (!=заказ)
                        dialog = DialogOk("Ошибка", "Нет производителей, чьи корпусы можно добавить")
                        dialog.show()
                        if dialog.exec():
                            pass
                    else:  # Если таблица производителей охлаждения непустая
                        win_add_change = adding.AddChangeBodyWindow(self, new_bool, list_all_pr,
                                                                    self.dict_proizv_body_name,
                                                                    self.dict_body_name)
                        self.block_lineedit(win_add_change.leKol, "")
                        win_add_change.show()
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
                            win_add_change = adding.AddChangeBodyWindow(self, new_bool, row[1],
                                                                        self.dict_proizv_body_name,
                                                                        self.dict_body_name)
                            self.block_combobox(win_add_change.cbProizv, row[1])
                            self.block_lineedit(win_add_change.leFullName, row[2])
                            self.block_combobox(win_add_change.cbGaming, row[3])
                            self.block_combobox(win_add_change.cbType, row[4])
                            self.block_lineedit(win_add_change.leFMother, row[5])
                            self.block_combobox(win_add_change.cbFPower, row[6])
                            self.block_lineedit(win_add_change.leLenVideo, row[7])
                            self.block_lineedit(win_add_change.leHeightCool, row[8])
                            self.block_lineedit(win_add_change.leLenPower, row[9])
                            self.block_lineedit(win_add_change.leWeight, row[10])
                            self.block_lineedit(win_add_change.leColor, row[11])
                            self.block_lineedit(win_add_change.lePrice, row[12])
                            win_add_change.show()

    # Метод, отвечающий за открытие окна фильтрации на складе. Принимает id вкладки ToolBox
    def tb_sklad_filter(self, page):
        match page:
            case 0:  # 0-9 - вкладки ToolBox (меню навигации)
                self.vidSkladFilter.show()  # Отображение экземпляра класса
            case 1:
                self.procSkladFilter.show()  # Отображение экземпляра класса
            case 2:
                self.motherSkladFilter.show()  # Отображение экземпляра класса
            case 3:
                self.coolSkladFilter.show()  # Отображение экземпляра класса
            case 4:
                self.ramSkladFilter.show()
            case 5:
                self.diskSkladFilter.show()
            case 6:
                self.powerSkladFilter.show()
            case 7:
                self.bodySkladFilter.show()  # Отображение экземпляра класса
            case 8:
                pass

    def apply_filter_sklad(self, get_query, page):
        print(get_query)
        bd_column = ""
        self.rbShowOrders.setChecked(False)  # Сбрасываем перед заполнением таблиц отображение заказов
        # В зависимости от принятого типа комплектующего задаём ключевой атрибут для фильтрующей вкладки
        match page:
            case 0:
                bd_column = "name"
            case 1:
                bd_column = "series"
            case 2:
                bd_column = "socket"
            case 3:
                bd_column = "type"
            case 4:
                bd_column = "type"
            case 5:
                bd_column = "type"
            case 6:
                bd_column = "formfactor"
            case 7:
                bd_column = "name"
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
            sklad_row = self.save_row(
                self.tableSklad)  # !!! Сохраняем строчку в фильтруемых таблицах, если они выделена!!!!
            self.fill_table_sklad(page, cur)  # page = 0-7 - порядковые идентификаторы комплектующих
            cur.execute(f"select distinct {bd_column} from({get_query}) as s1")
            list_param = []
            for name in cur:
                list_param.append(name[0])
            self.fill_tabs_configure(list_param, self.tabWidgetSklad)
            self.check_rows(sklad_row, self.tableSklad)

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
                    video_row = self.save_row(
                        self.tableConfVideo)  # !!! Сохраняем строчку в фильтруемых таблицах, если они выделена!!!!
                    self.fill_table_conf(page, cur)  # page = 0-7 - порядковые идентификаторы комплектующих
                    cur.execute(f"select distinct name from({get_query}) as s1")
                    list_name = []
                    for name in cur:
                        list_name.append(name[0])
                    self.fill_tabs_configure(list_name, self.tabWidgetVideo)
                    self.check_rows(video_row, self.tableConfVideo)
                case 1:
                    proc_row = self.save_row(
                        self.tableConfProc)  # !!! Сохраняем строчку в фильтруемых таблицах, если они выделена!!!!
                    self.fill_table_conf(page, cur)  # page = 0-7 - порядковые идентификаторы комплектующих
                    cur.execute(f"select distinct series from({get_query}) as s1")
                    list_series = []
                    for name in cur:
                        list_series.append(name[0])
                    self.fill_tabs_configure(list_series, self.tabWidgetProc)
                    self.check_rows(proc_row, self.tableConfProc)
                case 2:
                    mother_row = self.save_row(
                        self.tableConfMother)  # !!! Сохраняем строчку в фильтруемых таблицах, если они выделена!!!!
                    self.fill_table_conf(page, cur)  # page = 0-7 - порядковые идентификаторы комплектующих
                    cur.execute(f"select distinct socket from({get_query}) as s1")
                    list_socket = []
                    for name in cur:
                        list_socket.append(name[0])
                    self.fill_tabs_configure(list_socket, self.tabWidgetMother)
                    self.check_rows(mother_row, self.tableConfMother)
                case 3:
                    cool_row = self.save_row(
                        self.tableConfCool)  # !!! Сохраняем строчку в фильтруемых таблицах, если они выделена!!!!
                    self.fill_table_conf(page, cur)  # page = 0-7 - порядковые идентификаторы комплектующих
                    cur.execute(f"select distinct type from({get_query}) as s1")
                    list_type = []
                    for name in cur:
                        list_type.append(name[0])
                    self.fill_tabs_configure(list_type, self.tabWidgetCool)
                    self.check_rows(cool_row, self.tableConfCool)
                case 4:
                    ram_row = self.save_row(
                        self.tableConfRam)  # !!! Сохраняем строчку в фильтруемых таблицах, если они выделена!!!!
                    self.fill_table_conf(page, cur)  # page = 0-7 - порядковые идентификаторы комплектующих
                    cur.execute(f"select distinct type from({get_query}) as s1")
                    list_type = []
                    for name in cur:
                        list_type.append(name[0])
                    self.fill_tabs_configure(list_type, self.tabWidgetRam)
                    self.check_rows(ram_row, self.tableConfRam)
                case 5:
                    disk_row = self.save_row(
                        self.tableConfDisk)  # !!! Сохраняем строчку в фильтруемых таблицах, если они выделена!!!!
                    self.fill_table_conf(page, cur)  # page = 0-7 - порядковые идентификаторы комплектующих
                    cur.execute(f"select distinct type from({get_query}) as s1")
                    list_type = []
                    for name in cur:
                        list_type.append(name[0])
                    self.fill_tabs_configure(list_type, self.tabWidgetDisk)
                    self.check_rows(disk_row, self.tableConfDisk)
                case 6:
                    power_row = self.save_row(
                        self.tableConfPower)  # !!! Сохраняем строчку в фильтруемых таблицах, если они выделена!!!!
                    self.fill_table_conf(page, cur)  # page = 0-7 - порядковые идентификаторы комплектующих
                    cur.execute(f"select distinct formfactor from({get_query}) as s1")
                    list_ff = []
                    for name in cur:
                        list_ff.append(name[0])
                    self.fill_tabs_configure(list_ff, self.tabWidgetPower)
                    self.check_rows(power_row, self.tableConfPower)
                case 7:
                    body_row = self.save_row(
                        self.tableConfBody)  # !!! Сохраняем строчку в фильтруемых таблицах, если они выделена!!!!
                    self.fill_table_conf(page, cur)  # page = 0-7 - порядковые идентификаторы комплектующих
                    cur.execute(f"select distinct name from({get_query}) as s1")
                    list_proizv = []
                    for name in cur:
                        list_proizv.append(name[0])
                    self.fill_tabs_configure(list_proizv, self.tabWidgetBody)
                    self.check_rows(body_row, self.tableConfBody)

        except (Exception, psycopg2.DatabaseError) as error:
            dialog = DialogOk("Ошибка", error)
            dialog.show()

        finally:
            if conn:
                cur.close()
                conn.close()

    def rb_click_order_having_sklad(self, have, order, page):
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
            if self.tableSklad.currentRow() != -1:  # Если была выбрана строка, то сохраняем её и отправляе в check
                data_row = self.save_row(self.tableSklad)
            match page:  # Определение запроса к БД по типу выбранного комплектующего
                case 0:
                    if order:  # Выводим заказы, если индикатор вывода заказа нажат
                        if have:
                            cur.callproc("get_having_order_videocard")
                        else:
                            cur.callproc("get_all_order_videocard")
                    else:  # иначе - обычный фильтры по наличию
                        if have:  # Если нажат индикатор "только в наличии", то выводим либо все заказы, либо имеющиеся
                            cur.callproc("get_having_videocard")
                        else:
                            cur.callproc("get_all_videocard")
                case 1:
                    if order:  # Выводим заказы, если индикатор вывода заказа нажат
                        if have:
                            cur.callproc("get_having_order_processor")
                        else:
                            cur.callproc("get_all_order_processor")
                    else:  # иначе - обычный фильтры по наличию
                        if have:
                            cur.callproc("get_having_processor")
                        else:
                            cur.callproc("get_all_processor")
                case 2:
                    if order:  # Выводим заказы, если индикатор вывода заказа нажат
                        if have:
                            cur.callproc("get_having_order_motherboard")
                        else:
                            cur.callproc("get_all_order_motherboard")
                    else:  # иначе - обычный фильтры по наличию
                        if have:
                            cur.callproc("get_having_motherboard")
                        else:
                            cur.callproc("get_all_motherboard")
                case 3:
                    if order:  # Выводим заказы, если индикатор вывода заказа нажат
                        if have:
                            cur.callproc("get_having_order_cool")
                        else:
                            cur.callproc("get_all_order_cool")
                    else:  # иначе - обычный фильтры по наличию
                        if have:
                            cur.callproc("get_having_cool")
                        else:
                            cur.callproc("get_all_cool")
                case 4:
                    if order:  # Выводим заказы, если индикатор вывода заказа нажат
                        if have:
                            cur.callproc("get_having_order_ram")
                        else:
                            cur.callproc("get_all_order_ram")
                    else:  # иначе - обычный фильтры по наличию
                        if have:
                            cur.callproc("get_having_ram")
                        else:
                            cur.callproc("get_all_ram")
                case 5:
                    if order:  # Выводим заказы, если индикатор вывода заказа нажат
                        if have:
                            cur.callproc("get_having_order_disk")
                        else:
                            cur.callproc("get_all_order_disk")
                    else:  # иначе - обычный фильтры по наличию
                        if have:
                            cur.callproc("get_having_disk")
                        else:
                            cur.callproc("get_all_disk")
                case 6:
                    if order:  # Выводим заказы, если индикатор вывода заказа нажат
                        if have:
                            cur.callproc("get_having_order_power")
                        else:
                            cur.callproc("get_all_order_power")
                    else:  # иначе - обычный фильтры по наличию
                        if have:
                            cur.callproc("get_having_power")
                        else:
                            cur.callproc("get_all_power")
                case 7:
                    if order:  # Выводим заказы, если индикатор вывода заказа нажат
                        if have:
                            cur.callproc("get_having_order_body")
                        else:
                            cur.callproc("get_all_order_body")
                    else:  # иначе - обычный фильтры по наличию
                        if have:
                            cur.callproc("get_having_body")
                        else:
                            cur.callproc("get_all_body")

            self.fill_table_sklad(page, cur)
            self.fill_tabs_sklad(page)
            self.reset_radiobutton(self.tableSklad)
            # self.check_rows(data_row, self.tableSklad)

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
            if self.tableSklad.currentRow() != -1:  # Если была выбрана строка, то сохраняем её и отправляе в check
                data_row = self.save_row(self.tableSklad)
            match page:  # Определение запроса к БД по типу выбранного комплектующего
                case 0:
                    if have:
                        cur.callproc("get_having_videocard")
                    else:
                        cur.callproc("get_all_videocard")
                case 1:
                    if have:
                        cur.callproc("get_having_processor")
                    else:
                        cur.callproc("get_all_processor")
                case 2:
                    if have:
                        cur.callproc("get_having_motherboard")
                    else:
                        cur.callproc("get_all_motherboard")
                case 3:
                    if have:
                        cur.callproc("get_having_cool")
                    else:
                        cur.callproc("get_all_cool")
                case 4:
                    if have:
                        cur.callproc("get_having_ram")
                    else:
                        cur.callproc("get_all_ram")
                case 5:
                    if have:
                        cur.callproc("get_having_disk")
                    else:
                        cur.callproc("get_all_disk")
                case 6:
                    if have:
                        cur.callproc("get_having_power")
                    else:
                        cur.callproc("get_all_power")
                case 7:
                    if have:
                        cur.callproc("get_having_body")
                    else:
                        cur.callproc("get_all_body")

            self.fill_table_sklad(page, cur)
            self.fill_tabs_sklad(page)
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

                data_row.clear()
                if self.tableConfCool.currentRow() != -1:  # Если была выбрана строка, то сохраняем её номер
                    data_row = self.save_row(self.tableConfCool)
                cur.callproc("get_having_cool")
                self.fill_table_conf(3, cur)
                self.reset_radiobutton(self.tableConfCool)
                if self.check_rows(data_row, self.tableConfCool):
                    pass  # Ничего не выполняем, так как функция сработает еще в IF и если не вернёт True,
                    # то чистим корзину
                else:
                    self.clear_cart(self.tableConfCool)

                data_row.clear()
                if self.tableConfRam.currentRow() != -1:  # Если была выбрана строка, то сохраняем её номер
                    data_row = self.save_row(self.tableConfRam)
                cur.callproc("get_having_ram")
                self.fill_table_conf(4, cur)
                self.reset_radiobutton(self.tableConfRam)
                if self.check_rows(data_row, self.tableConfRam):
                    pass  # Ничего не выполняем, так как функция сработает еще в IF и если не вернёт True,
                    # то чистим корзину
                else:
                    self.clear_cart(self.tableConfRam)

                data_row.clear()
                if self.tableConfDisk.currentRow() != -1:  # Если была выбрана строка, то сохраняем её номер
                    data_row = self.save_row(self.tableConfDisk)
                cur.callproc("get_having_disk")
                self.fill_table_conf(5, cur)
                self.reset_radiobutton(self.tableConfDisk)
                if self.check_rows(data_row, self.tableConfDisk):
                    pass  # Ничего не выполняем, так как функция сработает еще в IF и если не вернёт True,
                    # то чистим корзину
                else:
                    self.clear_cart(self.tableConfDisk)

                data_row.clear()
                if self.tableConfPower.currentRow() != -1:  # Если была выбрана строка, то сохраняем её номер
                    data_row = self.save_row(self.tableConfPower)
                cur.callproc("get_having_power")
                self.fill_table_conf(6, cur)
                self.reset_radiobutton(self.tableConfPower)
                if self.check_rows(data_row, self.tableConfPower):
                    pass  # Ничего не выполняем, так как функция сработает еще в IF и если не вернёт True,
                    # то чистим корзину
                else:
                    self.clear_cart(self.tableConfPower)

                data_row.clear()
                if self.tableConfBody.currentRow() != -1:  # Если была выбрана строка, то сохраняем её номер
                    data_row = self.save_row(self.tableConfBody)
                cur.callproc("get_having_body")
                self.fill_table_conf(7, cur)
                self.reset_radiobutton(self.tableConfBody)
                if self.check_rows(data_row, self.tableConfBody):
                    pass  # Ничего не выполняем, так как функция сработает еще в IF и если не вернёт True,
                    # то чистим корзину
                else:
                    self.clear_cart(self.tableConfBody)

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

                data_row.clear()
                if self.tableConfCool.currentRow() != -1:  # Если была выбрана строка, то сохраняем её номер
                    data_row = self.save_row(self.tableConfCool)
                cur.callproc("get_all_cool")
                self.fill_table_conf(3, cur)
                self.reset_radiobutton(self.tableConfCool)
                if self.check_rows(data_row, self.tableConfCool):
                    pass  # Ничего не выполняем, так как функция сработает еще в IF и если не вернёт True,
                    # то чистим корзину
                else:
                    self.clear_cart(self.tableConfCool)

                data_row.clear()
                if self.tableConfRam.currentRow() != -1:  # Если была выбрана строка, то сохраняем её номер
                    data_row = self.save_row(self.tableConfRam)
                cur.callproc("get_all_ram")
                self.fill_table_conf(4, cur)
                self.reset_radiobutton(self.tableConfRam)
                if self.check_rows(data_row, self.tableConfRam):
                    pass  # Ничего не выполняем, так как функция сработает еще в IF и если не вернёт True,
                    # то чистим корзину
                else:
                    self.clear_cart(self.tableConfRam)

                data_row.clear()
                if self.tableConfDisk.currentRow() != -1:  # Если была выбрана строка, то сохраняем её номер
                    data_row = self.save_row(self.tableConfDisk)
                cur.callproc("get_all_disk")
                self.fill_table_conf(5, cur)
                self.reset_radiobutton(self.tableConfDisk)
                if self.check_rows(data_row, self.tableConfDisk):
                    pass  # Ничего не выполняем, так как функция сработает еще в IF и если не вернёт True,
                    # то чистим корзину
                else:
                    self.clear_cart(self.tableConfDisk)

                data_row.clear()
                if self.tableConfPower.currentRow() != -1:  # Если была выбрана строка, то сохраняем её номер
                    data_row = self.save_row(self.tableConfPower)
                cur.callproc("get_all_power")
                self.fill_table_conf(6, cur)
                self.reset_radiobutton(self.tableConfPower)
                if self.check_rows(data_row, self.tableConfPower):
                    pass  # Ничего не выполняем, так как функция сработает еще в IF и если не вернёт True,
                    # то чистим корзину
                else:
                    self.clear_cart(self.tableConfPower)

                data_row.clear()
                if self.tableConfBody.currentRow() != -1:  # Если была выбрана строка, то сохраняем её номер
                    data_row = self.save_row(self.tableConfBody)
                cur.callproc("get_all_body")
                self.fill_table_conf(7, cur)
                self.reset_radiobutton(self.tableConfBody)
                if self.check_rows(data_row, self.tableConfBody):
                    pass  # Ничего не выполняем, так как функция сработает еще в IF и если не вернёт True,
                    # то чистим корзину
                else:
                    self.clear_cart(self.tableConfBody)
            self.fill_all_tabs_conf()

        except (Exception, psycopg2.DatabaseError) as error:
            dialog = DialogOk("Ошибка", error)
            dialog.show()

        finally:
            if conn:
                cur.close()
                conn.close()

    # Метод, возвращающий из БД основные фильтрующие параметры (вкладки над таблицами)
    def get_tabs(self, complect, have):
        conn = None
        cur = None
        list_parameters = []
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
                            list_parameters.append(name[0])
                    else:
                        cur.callproc('get_inbase_videoproizv')
                        for name in cur:
                            list_parameters.append(name[0])
                case "Processor":
                    if have:
                        cur.callproc('get_having_procseries')
                        for name in cur:
                            list_parameters.append(name[0])
                    else:
                        cur.callproc('get_inbase_procseries')
                        for name in cur:
                            list_parameters.append(name[0])
                case "Motherboard":
                    if have:
                        cur.callproc('get_having_mothersocket')
                        for name in cur:
                            list_parameters.append(name[0])
                    else:
                        cur.callproc('get_inbase_mothersocket')
                        for name in cur:
                            list_parameters.append(name[0])
                case "Cool":
                    if have:
                        cur.callproc('get_having_cooltype')
                        for name in cur:
                            list_parameters.append(name[0])
                    else:
                        cur.callproc('get_inbase_cooltype')
                        for name in cur:
                            list_parameters.append(name[0])
                case "Ram":
                    if have:
                        cur.callproc('get_having_ramtype')
                        for name in cur:
                            list_parameters.append(name[0])
                    else:
                        cur.callproc('get_inbase_ramtype')
                        for name in cur:
                            list_parameters.append(name[0])
                case "Disk":
                    if have:
                        cur.callproc('get_having_disktype')
                        for name in cur:
                            list_parameters.append(name[0])
                    else:
                        cur.callproc('get_inbase_disktype')
                        for name in cur:
                            list_parameters.append(name[0])
                case "Power":
                    if have:
                        cur.callproc('get_having_powerfactor')
                        for name in cur:
                            list_parameters.append(name[0])
                    else:
                        cur.callproc('get_inbase_powerfactor')
                        for name in cur:
                            list_parameters.append(name[0])
                case "Body":
                    if have:
                        cur.callproc('get_having_bodyproizv')
                        for name in cur:
                            list_parameters.append(name[0])
                    else:
                        cur.callproc('get_inbase_bodyproizv')
                        for name in cur:
                            list_parameters.append(name[0])

        except (Exception, psycopg2.DatabaseError) as error:
            dialog = DialogOk("Ошибка", error)
            dialog.show()

        finally:
            if conn:
                conn.commit()
                cur.close()
                conn.close()
            return list_parameters

    # Метод для заполнения tabWidget-ов переданными производителями (есть похожий метод из-за индикатора наличия)
    def fill_tabs_sklad(self, page):
        list_names = []
        if self.tabWidgetSklad.count() > 1:
            for i in range(self.tabWidgetSklad.count() - 1):  # Удаление старых вкладок
                self.tabWidgetSklad.removeTab(1)
        # tab_widget.clear()
        match page:
            case 0:
                list_names = self.get_tabs("Videocard", self.rbSklad.isChecked())
            case 1:
                list_names = self.get_tabs("Processor", self.rbSklad.isChecked())
            case 2:
                list_names = self.get_tabs("Motherboard", self.rbSklad.isChecked())
            case 3:
                list_names = self.get_tabs("Cool", self.rbSklad.isChecked())
            case 4:
                list_names = self.get_tabs("Ram", self.rbSklad.isChecked())
            case 5:
                list_names = self.get_tabs("Disk", self.rbSklad.isChecked())
            case 6:
                list_names = self.get_tabs("Power", self.rbSklad.isChecked())
            case 7:
                list_names = self.get_tabs("Body", self.rbSklad.isChecked())

        count_tab = len(list_names)

        for i in range(0, count_tab):  # первая вкладка должна остаться
            tab = QtWidgets.QWidget()
            self.tabWidgetSklad.addTab(tab, list_names[i])

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

        list_names = self.get_tabs("Cool", self.rbConf.isChecked())
        count_tab = len(list_names)
        for i in range(0, count_tab):
            tab = QtWidgets.QWidget()
            self.tabWidgetCool.addTab(tab, list_names[i])

        list_names = self.get_tabs("Ram", self.rbConf.isChecked())
        count_tab = len(list_names)
        for i in range(0, count_tab):
            tab = QtWidgets.QWidget()
            self.tabWidgetRam.addTab(tab, list_names[i])

        list_names = self.get_tabs("Disk", self.rbConf.isChecked())
        count_tab = len(list_names)
        for i in range(0, count_tab):
            tab = QtWidgets.QWidget()
            self.tabWidgetDisk.addTab(tab, list_names[i])

        list_names = self.get_tabs("Power", self.rbConf.isChecked())
        count_tab = len(list_names)
        for i in range(0, count_tab):
            tab = QtWidgets.QWidget()
            self.tabWidgetPower.addTab(tab, list_names[i])

        list_names = self.get_tabs("Body", self.rbConf.isChecked())
        count_tab = len(list_names)
        for i in range(0, count_tab):
            tab = QtWidgets.QWidget()
            self.tabWidgetBody.addTab(tab, list_names[i])

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
                list_names = self.get_tabs("Cool", self.rbConf.isChecked())
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
                list_names = self.get_tabs("Body", self.rbConf.isChecked())
                tab_widget = self.tabWidgetBody

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
                    if tab_name == "Все" and self.rbSklad.isChecked():  # Если нажата вкладка "все" и фильтр наличия
                        if self.rbShowOrders.isChecked():  # Если нажаты заказы
                            cur.callproc('get_having_order_videocard')
                        else:
                            cur.callproc('get_having_videocard')
                    elif tab_name == "Все":
                        if self.rbShowOrders.isChecked():  # Если нажаты заказы
                            cur.callproc('get_all_order_videocard')
                        else:
                            cur.callproc('get_all_videocard')
                    else:
                        if self.rbSklad.isChecked():
                            if self.rbShowOrders.isChecked():  # Если нажаты заказы
                                cur.callproc('get_having_order_videocard_by_name', [tab_name])
                            else:
                                cur.callproc('get_having_videocard_by_name', [tab_name])
                        else:
                            if self.rbShowOrders.isChecked():  # Если нажаты заказы
                                cur.callproc('get_order_videocard_by_name', [tab_name])
                            else:
                                cur.callproc('get_videocard_by_name', [tab_name])

                case 1:
                    if self.tableSklad.currentRow() != -1:  # Если была выбрана строка, то сохраняем её номер
                        data_row = self.save_row(self.tableSklad)
                    if tab_name == "Все" and self.rbSklad.isChecked():
                        if self.rbShowOrders.isChecked():  # Если нажаты заказы
                            cur.callproc('get_having_order_processor')
                        else:
                            cur.callproc('get_having_processor')
                    elif tab_name == "Все":
                        if self.rbShowOrders.isChecked():  # Если нажаты заказы
                            cur.callproc('get_all_order_processor')
                        else:
                            cur.callproc('get_all_processor')
                    else:
                        if self.rbSklad.isChecked():
                            if self.rbShowOrders.isChecked():  # Если нажаты заказы
                                cur.callproc('get_having_order_processor_by_series', [tab_name])
                            else:
                                cur.callproc('get_having_processor_by_series', [tab_name])
                        else:
                            if self.rbShowOrders.isChecked():  # Если нажаты заказы
                                cur.callproc('get_order_processor_by_series', [tab_name])
                            else:
                                cur.callproc('get_processor_by_series', [tab_name])

                case 2:
                    if self.tableSklad.currentRow() != -1:  # Если была выбрана строка, то сохраняем её номер
                        data_row = self.save_row(self.tableSklad)
                    if tab_name == "Все" and self.rbSklad.isChecked():
                        if self.rbShowOrders.isChecked():  # Если нажаты заказы
                            cur.callproc('get_having_order_motherboard')
                        else:
                            cur.callproc('get_having_motherboard')
                    elif tab_name == "Все":
                        if self.rbShowOrders.isChecked():  # Если нажаты заказы
                            cur.callproc('get_all_order_motherboard')
                        else:
                            cur.callproc('get_all_motherboard')
                    else:
                        if self.rbSklad.isChecked():
                            if self.rbShowOrders.isChecked():  # Если нажаты заказы
                                cur.callproc('get_having_order_motherboard_by_socket', [tab_name])
                            else:
                                cur.callproc('get_having_motherboard_by_socket', [tab_name])
                        else:
                            if self.rbShowOrders.isChecked():  # Если нажаты заказы
                                cur.callproc('get_order_motherboard_by_socket', [tab_name])
                            else:
                                cur.callproc('get_motherboard_by_socket', [tab_name])

                case 3:
                    if self.tableSklad.currentRow() != -1:  # Если была выбрана строка, то сохраняем её номер
                        data_row = self.save_row(self.tableSklad)
                    if tab_name == "Все" and self.rbSklad.isChecked():
                        if self.rbShowOrders.isChecked():  # Если нажаты заказы
                            cur.callproc('get_having_order_cool')
                        else:
                            cur.callproc('get_having_cool')
                    elif tab_name == "Все":
                        if self.rbShowOrders.isChecked():  # Если нажаты заказы
                            cur.callproc('get_all_order_cool')
                        else:
                            cur.callproc('get_all_cool')
                    else:
                        if self.rbSklad.isChecked():
                            if self.rbShowOrders.isChecked():  # Если нажаты заказы
                                cur.callproc('get_having_order_cool_by_type', [tab_name])
                            else:
                                cur.callproc('get_having_cool_by_type', [tab_name])
                        else:
                            if self.rbShowOrders.isChecked():  # Если нажаты заказы
                                cur.callproc('get_order_cool_by_type', [tab_name])
                            else:
                                cur.callproc('get_cool_by_type', [tab_name])

                case 4:
                    if self.tableSklad.currentRow() != -1:  # Если была выбрана строка, то сохраняем её номер
                        data_row = self.save_row(self.tableSklad)
                    if tab_name == "Все" and self.rbSklad.isChecked():
                        if self.rbShowOrders.isChecked():  # Если нажаты заказы
                            cur.callproc('get_having_order_ram')
                        else:
                            cur.callproc('get_having_ram')
                    elif tab_name == "Все":
                        if self.rbShowOrders.isChecked():  # Если нажаты заказы
                            cur.callproc('get_all_order_ram')
                        else:
                            cur.callproc('get_all_ram')
                    else:
                        if self.rbSklad.isChecked():
                            if self.rbShowOrders.isChecked():  # Если нажаты заказы
                                cur.callproc('get_having_order_ram_by_type', [tab_name])
                            else:
                                cur.callproc('get_having_ram_by_type', [tab_name])
                        else:
                            if self.rbShowOrders.isChecked():  # Если нажаты заказы
                                cur.callproc('get_order_ram_by_type', [tab_name])
                            else:
                                cur.callproc('get_ram_by_type', [tab_name])

                case 5:
                    if self.tableSklad.currentRow() != -1:  # Если была выбрана строка, то сохраняем её номер
                        data_row = self.save_row(self.tableSklad)
                    if tab_name == "Все" and self.rbSklad.isChecked():
                        if self.rbShowOrders.isChecked():  # Если нажаты заказы
                            cur.callproc('get_having_order_disk')
                        else:
                            cur.callproc('get_having_disk')
                    elif tab_name == "Все":
                        if self.rbShowOrders.isChecked():  # Если нажаты заказы
                            cur.callproc('get_all_order_disk')
                        else:
                            cur.callproc('get_all_disk')
                    else:
                        if self.rbSklad.isChecked():
                            if self.rbShowOrders.isChecked():  # Если нажаты заказы
                                cur.callproc('get_having_order_disk_by_type', [tab_name])
                            else:
                                cur.callproc('get_having_disk_by_type', [tab_name])
                        else:
                            if self.rbShowOrders.isChecked():  # Если нажаты заказы
                                cur.callproc('get_order_disk_by_type', [tab_name])
                            else:
                                cur.callproc('get_disk_by_type', [tab_name])

                case 6:
                    if self.tableSklad.currentRow() != -1:  # Если была выбрана строка, то сохраняем её номер
                        data_row = self.save_row(self.tableSklad)
                    if tab_name == "Все" and self.rbSklad.isChecked():
                        if self.rbShowOrders.isChecked():  # Если нажаты заказы
                            cur.callproc('get_having_order_power')
                        else:
                            cur.callproc('get_having_power')
                    elif tab_name == "Все":
                        if self.rbShowOrders.isChecked():  # Если нажаты заказы
                            cur.callproc('get_all_order_power')
                        else:
                            cur.callproc('get_all_power')
                    else:
                        if self.rbSklad.isChecked():
                            if self.rbShowOrders.isChecked():  # Если нажаты заказы
                                cur.callproc('get_having_order_power_by_factor', [tab_name])
                            else:
                                cur.callproc('get_having_power_by_factor', [tab_name])
                        else:
                            if self.rbShowOrders.isChecked():  # Если нажаты заказы
                                cur.callproc('get_order_power_by_factor', [tab_name])
                            else:
                                cur.callproc('get_power_by_factor', [tab_name])

                case 7:
                    if self.tableSklad.currentRow() != -1:  # Если была выбрана строка, то сохраняем её номер
                        data_row = self.save_row(self.tableSklad)
                    if self.tableSklad.currentRow() != -1:  # Если была выбрана строка, то сохраняем её номер
                        data_row = self.save_row(self.tableSklad)
                    if tab_name == "Все" and self.rbSklad.isChecked():
                        if self.rbShowOrders.isChecked():  # Если нажаты заказы
                            cur.callproc('get_having_order_body')
                        else:
                            cur.callproc('get_having_body')
                    elif tab_name == "Все":
                        if self.rbShowOrders.isChecked():  # Если нажаты заказы
                            cur.callproc('get_all_order_body')
                        else:
                            cur.callproc('get_all_body')
                    else:
                        if self.rbSklad.isChecked():
                            if self.rbShowOrders.isChecked():  # Если нажаты заказы
                                cur.callproc('get_having_order_body_by_name', [tab_name])
                            else:
                                cur.callproc('get_having_body_by_name', [tab_name])
                        else:
                            if self.rbShowOrders.isChecked():  # Если нажаты заказы
                                cur.callproc('get_order_body_by_name', [tab_name])
                            else:
                                cur.callproc('get_body_by_name', [tab_name])

            self.fill_table_sklad(page, cur)
            self.reset_radiobutton(self.tableSklad)
            self.check_rows(data_row, self.tableSklad)

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
                    elif tab_name == "Все":
                        cur.callproc('get_all_videocard')
                    else:
                        if self.rbConf.isChecked():
                            cur.callproc('get_having_videocard_by_name', [tab_name])
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
                    elif tab_name == "Все":
                        cur.callproc('get_all_processor')
                    else:
                        if self.rbConf.isChecked():
                            cur.callproc('get_having_processor_by_series', [tab_name])
                        else:
                            cur.callproc('get_processor_by_series', [tab_name])

                    self.fill_table_conf(1, cur)
                    self.reset_radiobutton(self.tableConfProc)
                    self.check_rows(data_row, self.tableConfProc)  # Проверяем строку и выделяем её

                case self.tabWidgetMother:
                    if self.tableConfMother.currentRow() != -1:  # Если была выбрана строка, то сохраняем её номер
                        data_row = self.save_row(self.tableConfMother)
                    if tab_name == "Все" and self.rbConf.isChecked():
                        cur.callproc('get_having_motherboard')
                    elif tab_name == "Все":
                        cur.callproc('get_all_motherboard')
                    else:
                        if self.rbConf.isChecked():
                            cur.callproc('get_having_motherboard_by_socket', [tab_name])
                        else:
                            cur.callproc('get_motherboard_by_socket', [tab_name])

                    self.fill_table_conf(2, cur)
                    self.reset_radiobutton(self.tabWidgetMother)
                    self.check_rows(data_row, self.tableConfMother)  # Проверяем строку и выделяем её

                case self.tabWidgetCool:
                    if self.tableConfCool.currentRow() != -1:  # Если была выбрана строка, то сохраняем её номер
                        data_row = self.save_row(self.tableConfCool)

                    if tab_name == "Все" and self.rbConf.isChecked():
                        cur.callproc('get_having_cool')

                    elif tab_name == "Все":
                        cur.callproc('get_all_cool')
                    else:
                        if self.rbConf.isChecked():
                            cur.callproc('get_having_cool_by_type', [tab_name])
                        else:
                            cur.callproc('get_cool_by_type', [tab_name])

                    self.fill_table_conf(3, cur)
                    self.reset_radiobutton(self.tableConfCool)
                    self.check_rows(data_row, self.tableConfCool)  # Проверяем строку и выделяем её

                case self.tabWidgetRam:
                    if self.tableConfRam.currentRow() != -1:  # Если была выбрана строка, то сохраняем её номер
                        data_row = self.save_row(self.tableConfRam)

                    if tab_name == "Все" and self.rbConf.isChecked():
                        cur.callproc('get_having_ram')
                    elif tab_name == "Все":
                        cur.callproc('get_all_ram')
                    else:
                        if self.rbConf.isChecked():
                            cur.callproc('get_having_ram_by_type', [tab_name])
                        else:
                            cur.callproc('get_ram_by_type', [tab_name])

                    self.fill_table_conf(4, cur)
                    self.reset_radiobutton(self.tableConfRam)
                    self.check_rows(data_row, self.tableConfRam)  # Проверяем строку и выделяем её

                case self.tabWidgetDisk:
                    if self.tableConfDisk.currentRow() != -1:  # Если была выбрана строка, то сохраняем её номер
                        data_row = self.save_row(self.tableConfDisk)

                    if tab_name == "Все" and self.rbConf.isChecked():
                        cur.callproc('get_having_disk')
                    elif tab_name == "Все":
                        cur.callproc('get_all_disk')
                    else:
                        if self.rbConf.isChecked():
                            cur.callproc('get_having_disk_by_type', [tab_name])
                        else:
                            cur.callproc('get_disk_by_type', [tab_name])

                    self.fill_table_conf(5, cur)
                    self.reset_radiobutton(self.tableConfDisk)
                    self.check_rows(data_row, self.tableConfDisk)  # Проверяем строку и выделяем её

                case self.tabWidgetPower:
                    if self.tableConfPower.currentRow() != -1:  # Если была выбрана строка, то сохраняем её номер
                        data_row = self.save_row(self.tableConfPower)

                    if tab_name == "Все" and self.rbConf.isChecked():
                        cur.callproc('get_having_power')
                    elif tab_name == "Все":
                        cur.callproc('get_all_power')
                    else:
                        if self.rbConf.isChecked():
                            cur.callproc('get_having_power_by_factor', [tab_name])
                        else:
                            cur.callproc('get_power_by_factor', [tab_name])
                    self.fill_table_conf(6, cur)
                    self.reset_radiobutton(self.tableConfPower)
                    self.check_rows(data_row, self.tableConfPower)  # Проверяем строку и выделяем её

                case self.tabWidgetBody:
                    if self.tableConfBody.currentRow() != -1:  # Если была выбрана строка, то сохраняем её номер
                        data_row = self.save_row(self.tableConfBody)

                    if tab_name == "Все" and self.rbConf.isChecked():
                        cur.callproc('get_having_body')
                    elif tab_name == "Все":
                        cur.callproc('get_all_body')
                    else:
                        if self.rbConf.isChecked():
                            cur.callproc('get_having_body_by_name', [tab_name])
                        else:
                            cur.callproc('get_body_by_name', [tab_name])

                    self.fill_table_conf(7, cur)
                    self.reset_radiobutton(self.tableConfBody)
                    self.check_rows(data_row, self.tableConfBody)  # Проверяем строку и выделяем её

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
                    if table.objectName() in self.dict_power_vid_proc_cool:
                        self.dict_power_vid_proc_cool.pop(table.objectName())
                    if table.objectName() in self.dict_current:
                        self.dict_current.pop(table.objectName())
                    self.show_header(self.tableConfVideo)
                    self.btnVideoHeader.setChecked(False)

                case self.tableConfProc:
                    self.load_conf(1)
                    if table.objectName() in self.dict_power_vid_proc_cool:
                        self.dict_power_vid_proc_cool.pop(table.objectName())
                    if table.objectName() in self.dict_current:
                        self.dict_current.pop(table.objectName())
                    self.show_header(self.tableConfProc)
                    self.btnProcHeader.setChecked(False)

                case self.tableConfMother:
                    self.load_conf(2)
                    if table.objectName() in self.dict_current:
                        self.dict_current.pop(table.objectName())
                    self.show_header(self.tableConfMother)
                    self.btnMotherHeader.setChecked(False)

                case self.tableConfCool:
                    self.load_conf(3)
                    if table.objectName() in self.dict_power_vid_proc_cool:
                        self.dict_power_vid_proc_cool.pop(table.objectName())
                    if table.objectName() in self.dict_current:
                        self.dict_current.pop(table.objectName())
                    self.show_header(self.tableConfCool)
                    self.btnCoolHeader.setChecked(False)

                case self.tableConfRam:
                    self.load_conf(4)
                    if table.objectName() in self.dict_current:
                        self.dict_current.pop(table.objectName())
                    self.show_header(self.tableConfRam)
                    self.btnRamHeader.setChecked(False)

                case self.tableConfDisk:
                    self.load_conf(5)
                    if table.objectName() in self.dict_current:
                        self.dict_current.pop(table.objectName())
                    self.show_header(self.tableConfDisk)
                    self.btnDiskHeader.setChecked(False)

                case self.tableConfPower:
                    self.load_conf(6)
                    if table.objectName() in self.dict_current:
                        self.dict_current.pop(table.objectName())
                    self.show_header(self.tableConfPower)
                    self.btnPowerHeader.setChecked(False)

                case self.tableConfBody:
                    self.load_conf(7)
                    if table.objectName() in self.dict_current:
                        self.dict_current.pop(table.objectName())
                    self.show_header(self.tableConfBody)
                    self.btnBodyHeader.setChecked(False)

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
                        table.selectRow(i)
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
                        table.selectRow(i)
                        self.fill_cart(table)
            button_group.setExclusive(True)
            self.configure(table)

    def current_pos_sklad(self, ch, row, table):
        # print(f' row = {row} -- {ch}')
        # if ch:
        # table.selectRow(row)
        pass

    def current_pos(self, ch, row, table):  # Если добавить хедеры в конфигуратор и дать возможность ранжирования,
        # if ch:
        # table.selectRow(row)
        # self.fill_cart(table)
        pass

    def configure_video(self):
        query = "SELECT kol, videocard.exist, videocard.id, proizv_videocard.name, fullname, gaming, " \
                "chipcreator, chipname, vram, typevram, frequency, bus, interface, monitor, " \
                "resolution, tdp, length, connvideo, kolconnvideo, price " \
                "FROM videocard, sklad_videocard, proizv_videocard " \
                "WHERE videocard.id = sklad_videocard.id_izd " \
                "AND videocard.id_proizv = proizv_videocard.id "

        if self.tableConfMother.objectName() in self.dict_current:
            mother_row = self.dict_current[self.tableConfMother.objectName()]
            query += f" AND interface = '{mother_row[4]}' "
        if self.tableConfPower.objectName() in self.dict_current:
            power_row = self.dict_current[self.tableConfPower.objectName()]
            sum_video_connector = int(power_row[9]) * int(power_row[10])  # Коннекторы видеокарты
            query += f" AND connvideo*kolconnvideo <= '{sum_video_connector}' "
        if self.tableConfBody.objectName() in self.dict_current:
            body_row = self.dict_current[self.tableConfBody.objectName()]
            query += f" AND length <= '{body_row[4]}' "

        if self.rbConf.isChecked():
            query += " AND videocard.exist = True"

        query += " ORDER BY videocard.exist DESC "
        return query

    def configure_proc(self):
        query = "SELECT sklad_processor.kol, processor.exist, processor.id, proizv_processor.name, " \
                "fullname, gaming, series, socket, core, ncores, cache, frequency, techproc, " \
                "ramfreq, graphics, tdp, price " \
                "FROM processor, sklad_processor, proizv_processor " \
                "WHERE processor.id = sklad_processor.id_izd AND processor.id_proizv = proizv_processor.id "

        if self.tableConfMother.objectName() in self.dict_current:
            mother_row = self.dict_current[self.tableConfMother.objectName()]
            query += f" AND socket like '%' || '{mother_row[1]}' || '%'  "
        if self.tableConfCool.objectName() in self.dict_current:
            cool_row = self.dict_current[self.tableConfCool.objectName()]
            query += f" AND '{cool_row[3]}' like concat('%', socket, '%') " \
                     f" AND tdp*100/{cool_row[6]} >= 65 " \
                     f" AND tdp*100/{cool_row[6]} <= 90 "
        if self.tableConfRam.objectName() in self.dict_current:
            ram_row = self.dict_current[self.tableConfRam.objectName()]
            query += f" AND ramfreq >= '{ram_row[3]}' "

        if self.rbConf.isChecked():
            query += " AND processor.exist = True "

        query += " ORDER BY processor.exist DESC "
        return query

    def configure_mother(self):
        query = "SELECT sklad_motherboard.kol, motherboard.exist, motherboard.id, " \
                "proizv_motherboard.name, fullname, gaming, socket, chipset, formfactor, pcie, " \
                "memorytype, memoryslot, memorymax, memoryfreqmax, m2, sata, " \
                "conncool, connproc, kolconnproc,  price " \
                "FROM motherboard, sklad_motherboard, proizv_motherboard  " \
                "WHERE motherboard.id = sklad_motherboard.id_izd " \
                "AND motherboard.id_proizv = proizv_motherboard.id "

        # проверка влияющих на мат. плату таблиц для конкатенации запроса
        if self.tableConfVideo.objectName() in self.dict_current:
            vid_row = self.dict_current[self.tableConfVideo.objectName()]
            query += f" AND pcie = '{vid_row[7]}' "
        if self.tableConfProc.objectName() in self.dict_current:
            proc_row = self.dict_current[self.tableConfProc.objectName()]
            query += f" AND socket = '{proc_row[1]}' "
        if self.tableConfCool.objectName() in self.dict_current:
            cool_row = self.dict_current[self.tableConfCool.objectName()]
            query += f" AND '{cool_row[3]}' like concat('%', socket, '%') " \
                     f" AND conncool >= '{cool_row[8]}' "
        if self.tableConfRam.objectName() in self.dict_current:
            ram_row = self.dict_current[self.tableConfRam.objectName()]
            query += f" AND memorytype = '{ram_row[1]}' " \
                     f" AND memorymax >= {ram_row[2]} " \
                     f" AND memoryfreqmax >= {ram_row[3]} "
        if self.tableConfPower.objectName() in self.dict_current:
            power_row = self.dict_current[self.tableConfPower.objectName()]
            sum_proc_connector = int(power_row[7]) * int(power_row[8])  # Коннекторы процессора
            query += f" AND connproc*kolconnproc <= '{sum_proc_connector}' "
        if self.tableConfBody.objectName() in self.dict_current:
            body_row = self.dict_current[self.tableConfBody.objectName()]
            query += f" AND '{body_row[2]}' like concat('%', formfactor, '%') "

        if self.rbConf.isChecked():
            query += " AND motherboard.exist = True "

        query += " ORDER BY exist DESC "
        return query

    def configure_cool(self):
        query = "SELECT sklad_cool.kol, cool.exist, cool.id, proizv_cool.name, " \
                "fullname, construction, type, socket, heatpipe, " \
                "height, disperse, voltage, conncool, price " \
                "FROM cool, sklad_cool, proizv_cool " \
                "WHERE cool.id = sklad_cool.id_izd AND cool.id_proizv = proizv_cool.id "

        if self.tableConfProc.objectName() in self.dict_current:
            proc_row = self.dict_current[self.tableConfProc.objectName()]
            query += f" AND socket like '%' || '{proc_row[1]}' || '%' " \
                     f" AND {proc_row[6]}*100/disperse >= 65 " \
                     f" AND {proc_row[6]}*100/disperse <= 89 "
        if self.tableConfMother.objectName() in self.dict_current:
            mother_row = self.dict_current[self.tableConfMother.objectName()]
            query += f" AND socket like '%' || '{mother_row[1]}' || '%' " \
                     f" AND conncool >= '{mother_row[11]}' "
        if self.tableConfBody.objectName() in self.dict_current:
            body_row = self.dict_current[self.tableConfBody.objectName()]
            query += f" AND height <= '{body_row[5]}' "

        if self.rbConf.isChecked():
            query += " AND cool.exist = TRUE "

        query += " ORDER BY cool.exist DESC "
        return query

    def configure_ram(self):
        query = "SELECT sklad_ram.kol, ram.exist, ram.id, proizv_ram.name, " \
                "fullname, gaming, type, volume, frequency, " \
                "complect, latency, voltage, price " \
                "FROM ram, sklad_ram, proizv_ram " \
                "WHERE ram.id = sklad_ram.id_izd AND ram.id_proizv = proizv_ram.id "

        if self.tableConfProc.objectName() in self.dict_current:
            proc_row = self.dict_current[self.tableConfProc.objectName()]
            query += f" AND frequency <= '{proc_row[5]}' "
        if self.tableConfMother.objectName() in self.dict_current:
            mother_row = self.dict_current[self.tableConfMother.objectName()]
            query += f" AND type = '{mother_row[5]}' " \
                     f" AND volume <= '{mother_row[7]}' " \
                     f" AND frequency <= '{mother_row[8]}' "

        if self.rbConf.isChecked():
            query += "AND ram.exist = TRUE "

        query += " ORDER BY ram.exist DESC "
        return query

    def configure_power(self):
        query = "SELECT sklad_power.kol, power.exist, power.id, proizv_power.name, " \
                "fullname, formfactor, length, power, certificate, pinmain, " \
                "pinsata, connproc, kolconnproc, connvideo, kolconnvideo, price " \
                "FROM power, sklad_power, proizv_power " \
                "WHERE power.id = sklad_power.id_izd AND power.id_proizv = proizv_power.id "

        # проверка влияющих на мат. плату таблиц для конкатенации запроса
        power_sum = sum(self.dict_power_vid_proc_cool.values())  # Сумма потреблений в ваттах

        if self.tableConfVideo.objectName() in self.dict_current:
            vid_row = self.dict_current[self.tableConfVideo.objectName()]
            query += f" AND connvideo*kolconnvideo >= {int(vid_row[11]) * int(vid_row[12])} "
        if self.tableConfMother.objectName() in self.dict_current:
            mother_row = self.dict_current[self.tableConfMother.objectName()]
            query += f" AND connproc*kolconnproc >= {int(mother_row[12]) * int(mother_row[13])} "
        if self.tableConfBody.objectName() in self.dict_current:
            # sum_video_connector = int(saved_row[9]) * int(saved_row[10])  # Коннекторы видеокарты
            body_row = self.dict_current[self.tableConfBody.objectName()]
            query += f" AND formfactor = '{body_row[3]}' " \
                     f" AND length <= '{body_row[6]}' "

        if len(self.dict_power_vid_proc_cool) == 3:  # Если выбрано  3 элемента, то добавляем доп.
            # параметры в запрос-конфигуратор (поиск по оптимальной мощности)
            query += f" AND {power_sum}*100/power >= 50 " \
                     f" AND {power_sum}*100/power <= 80 "

        if self.rbConf.isChecked():
            query += " AND power.exist = TRUE "

        query += " ORDER BY power.exist DESC "
        return query

    def configure_body(self):
        query = "SELECT sklad_body.kol, body.exist, body.id, proizv_body.name, " \
                "fullname, gaming, type, ffmother, ffpower, " \
                "lengthvideo, heightcool, lengthpower, weight, color, price " \
                "FROM body, sklad_body, proizv_body " \
                "WHERE body.id = sklad_body.id_izd AND body.id_proizv = proizv_body.id "

        if self.tableConfVideo.objectName() in self.dict_current:
            vid_row = self.dict_current[self.tableConfVideo.objectName()]
            query += f" AND lengthvideo >= '{vid_row[10]}' "
        if self.tableConfMother.objectName() in self.dict_current:
            mother_row = self.dict_current[self.tableConfMother.objectName()]
            query += f" AND ffmother like '%' || '{mother_row[3]}' || '%'  "
        if self.tableConfCool.objectName() in self.dict_current:
            cool_row = self.dict_current[self.tableConfCool.objectName()]
            query += f" AND heightcool >= '{cool_row[5]}' "
        if self.tableConfPower.objectName() in self.dict_current:
            power_row = self.dict_current[self.tableConfPower.objectName()]
            query += f" AND ffpower like '%' || '{power_row[1]}' || '%' " \
                     f" AND lengthpower >= '{power_row[2]}' "

        if self.rbConf.isChecked():
            query += "AND body.exist = TRUE "

        query += " ORDER BY body.exist DESC "
        return query

    def configure(self, table):
        conn = None
        cur = None
        saved_row = self.save_row(
            table)  # Сохранение строки и передача параметра в качестве фильтра для запроса
        try:
            conn = psycopg2.connect(database="confPc",
                                    user="postgres",
                                    password="2001",
                                    host="localhost",
                                    port="5432")
            cur = conn.cursor()

            match table:  # В каждой таблице отпправляется своё количество запросов в БД для фильтрации
                case self.tableConfVideo:
                    mother_row = self.save_row(
                        self.tableConfMother)  # !!! Сохраняем строчку в фильтруемых таблицах, если они выделена!!!!
                    query = self.configure_mother()
                    cur.execute(query)
                    self.fill_table_conf(2, cur)
                    self.check_rows(mother_row, self.tableConfMother)
                    cur.execute(f"select distinct socket from({query}) as s1")
                    list_socket = []
                    for name in cur:
                        list_socket.append(name[0])
                    self.fill_tabs_configure(list_socket, self.tabWidgetMother)

                    power_row = self.save_row(
                        self.tableConfPower)  # !!! Сохраняем строчку в фильтруемых таблицах, если она выделена!!!!
                    # Перезаписываем в словаре для таблицы процессоров значение ТДП
                    self.dict_power_vid_proc_cool[self.tableConfVideo.objectName()] = int(saved_row[9])
                    query = self.configure_power()
                    cur.execute(query)
                    self.fill_table_conf(6, cur)
                    self.check_rows(power_row, self.tableConfPower)
                    cur.execute(f"select distinct formfactor from({query}) as s1")
                    list_ff = []
                    for name in cur:
                        list_ff.append(name[0])
                    self.fill_tabs_configure(list_ff, self.tabWidgetPower)

                    body_row = self.save_row(
                        self.tableConfBody)  # !!! Сохраняем строчку в фильтруемых таблицах, если они выделена!!!!
                    query = self.configure_body()
                    cur.execute(query)
                    self.fill_table_conf(7, cur)
                    self.check_rows(body_row, self.tableConfBody)
                    cur.execute(f"select distinct name from({query}) as s1")
                    list_proizv = []
                    for name in cur:
                        list_proizv.append(name[0])
                    self.fill_tabs_configure(list_proizv, self.tabWidgetBody)

                case self.tableConfProc:  # По выбранному процессору отсортировать мат платы и ОЗУ
                    mother_row = self.save_row(
                        self.tableConfMother)  # !!! Сохраняем строчку в фильтруемых таблицах, если они выделена!!!!
                    query = self.configure_mother()
                    cur.execute(query)
                    self.fill_table_conf(2, cur)
                    self.check_rows(mother_row, self.tableConfMother)
                    cur.execute(f"select distinct socket from({query}) as s1")
                    list_socket = []
                    for name in cur:
                        list_socket.append(name[0])
                    self.fill_tabs_configure(list_socket, self.tabWidgetMother)

                    cool_row = self.save_row(
                        self.tableConfCool)  # !!! Сохраняем строчку в фильтруемых таблицах, если они выделена!!!!
                    query = self.configure_cool()
                    cur.execute(query)
                    self.fill_table_conf(3, cur)
                    self.check_rows(cool_row, self.tableConfCool)
                    cur.execute(f"select distinct type from({query}) as s1")
                    list_type = []
                    for name in cur:
                        list_type.append(name[0])
                    self.fill_tabs_configure(list_type, self.tabWidgetCool)

                    ram_row = self.save_row(
                        self.tableConfRam)  # !!! Сохраняем строчку в фильтруемых таблицах, если они выделена!!!!
                    query = self.configure_ram()
                    cur.execute(query)
                    self.fill_table_conf(4, cur)
                    self.check_rows(ram_row, self.tableConfRam)
                    cur.execute(f"select distinct type from({query}) as s1")
                    list_type = []
                    for name in cur:
                        list_type.append(name[0])
                    self.fill_tabs_configure(list_type, self.tabWidgetRam)

                    power_row = self.save_row(
                        self.tableConfPower)  # !!! Сохраняем строчку в фильтруемых таблицах, если она выделена!!!!
                    # Перезаписываем в словаре для таблицы процессоров значение ТДП
                    self.dict_power_vid_proc_cool[self.tableConfProc.objectName()] = int(saved_row[6])
                    query = self.configure_power()
                    cur.execute(query)
                    self.fill_table_conf(6, cur)
                    self.check_rows(power_row, self.tableConfPower)
                    cur.execute(f"select distinct formfactor from({query}) as s1")
                    list_ff = []
                    for name in cur:
                        list_ff.append(name[0])
                    self.fill_tabs_configure(list_ff, self.tabWidgetPower)

                case self.tableConfMother:  # По выбранной мат. плате отсортировать процессоры и ОЗУ
                    video_row = self.save_row(
                        self.tableConfVideo)  # !!! Сохраняем строчку в фильтруемых таблицах, если они выделена!!!!
                    query = self.configure_video()
                    cur.execute(query)
                    self.fill_table_conf(0, cur)
                    self.check_rows(video_row, self.tableConfVideo)
                    cur.execute(f"select distinct name from({query}) as s1")
                    list_proizv = []
                    for name in cur:
                        list_proizv.append(name[0])
                    self.fill_tabs_configure(list_proizv, self.tabWidgetVideo)

                    proc_row = self.save_row(
                        self.tableConfProc)  # !!! Сохраняем строчку в фильтруемых таблицах, если они выделена!!!!
                    query = self.configure_proc()
                    cur.execute(query)
                    self.fill_table_conf(1, cur)
                    self.check_rows(proc_row, self.tableConfProc)
                    cur.execute(f"select distinct series from({query}) as s1")
                    list_series = []
                    for name in cur:
                        list_series.append(name[0])
                    self.fill_tabs_configure(list_series, self.tabWidgetProc)

                    cool_row = self.save_row(
                        self.tableConfCool)  # !!! Сохраняем строчку в фильтруемых таблицах, если они выделена!!!!
                    query = self.configure_cool()
                    cur.execute(query)
                    self.fill_table_conf(3, cur)
                    self.check_rows(cool_row, self.tableConfCool)
                    cur.execute(f"select distinct type from({query}) as s1")
                    list_type = []
                    for name in cur:
                        list_type.append(name[0])
                    self.fill_tabs_configure(list_type, self.tabWidgetCool)

                    ram_row = self.save_row(
                        self.tableConfRam)  # !!! Сохраняем строчку в фильтруемых таблицах, если они выделена!!!!
                    query = self.configure_ram()
                    cur.execute(query)
                    self.fill_table_conf(4, cur)
                    self.check_rows(ram_row, self.tableConfRam)
                    cur.execute(f"select distinct type from({query}) as s1")
                    list_type = []
                    for name in cur:
                        list_type.append(name[0])
                    self.fill_tabs_configure(list_type, self.tabWidgetRam)

                    power_row = self.save_row(
                        self.tableConfPower)  # !!! Сохраняем строчку в фильтруемых таблицах, если они выделена!!!!
                    query = self.configure_power()
                    cur.execute(query)
                    self.fill_table_conf(6, cur)
                    self.check_rows(power_row, self.tableConfPower)
                    cur.execute(f"select distinct formfactor from({query}) as s1")
                    list_ff = []
                    for name in cur:
                        list_ff.append(name[0])
                    self.fill_tabs_configure(list_ff, self.tabWidgetPower)

                    body_row = self.save_row(
                        self.tableConfBody)  # !!! Сохраняем строчку в фильтруемых таблицах, если они выделена!!!!
                    query = self.configure_body()
                    cur.execute(query)
                    self.fill_table_conf(7, cur)
                    self.check_rows(body_row, self.tableConfBody)
                    cur.execute(f"select distinct name from({query}) as s1")
                    list_proizv = []
                    for name in cur:
                        list_proizv.append(name[0])
                    self.fill_tabs_configure(list_proizv, self.tabWidgetBody)

                case self.tableConfCool:  # По выбранному кулеру отсортировать мат. плату, корпус и процессор
                    proc_row = self.save_row(
                        self.tableConfProc)  # !!! Сохраняем строчку в фильтруемых таблицах, если они выделена!!!!
                    query = self.configure_proc()
                    cur.execute(query)
                    self.fill_table_conf(1, cur)
                    self.check_rows(proc_row, self.tableConfProc)
                    cur.execute(f"select distinct series from({query}) as s1")
                    list_series = []
                    for name in cur:
                        list_series.append(name[0])
                    self.fill_tabs_configure(list_series, self.tabWidgetProc)

                    mother_row = self.save_row(
                        self.tableConfMother)  # !!! Сохраняем строчку в фильтруемых таблицах, если они выделена!!!!
                    query = self.configure_mother()
                    cur.execute(query)
                    self.fill_table_conf(2, cur)
                    self.check_rows(mother_row, self.tableConfMother)
                    cur.execute(f"select distinct socket from({query}) as s1")
                    list_socket = []
                    for name in cur:
                        list_socket.append(name[0])
                    self.fill_tabs_configure(list_socket, self.tabWidgetMother)

                    self.dict_power_vid_proc_cool[self.tableConfCool.objectName()] = int(saved_row[6])
                    power_row = self.save_row(
                        self.tableConfPower)  # !!! Сохраняем строчку в фильтруемых таблицах, если они выделена!!!!
                    query = self.configure_power()
                    cur.execute(query)
                    self.fill_table_conf(6, cur)
                    self.check_rows(power_row, self.tableConfPower)
                    cur.execute(f"select distinct formfactor from({query}) as s1")
                    list_ff = []
                    for name in cur:
                        list_ff.append(name[0])
                    self.fill_tabs_configure(list_ff, self.tabWidgetPower)

                    body_row = self.save_row(
                        self.tableConfBody)  # !!! Сохраняем строчку в фильтруемых таблицах, если они выделена!!!!
                    query = self.configure_body()
                    cur.execute(query)
                    self.fill_table_conf(7, cur)
                    self.check_rows(body_row, self.tableConfBody)
                    cur.execute(f"select distinct name from({query}) as s1")
                    list_proizv = []
                    for name in cur:
                        list_proizv.append(name[0])
                    self.fill_tabs_configure(list_proizv, self.tabWidgetBody)

                case self.tableConfRam:  # По выбранной ОЗУ отсортировать мат. плату и процессор
                    proc_row = self.save_row(
                        self.tableConfProc)  # !!! Сохраняем строчку в фильтруемых таблицах, если они выделена!!!!
                    query = self.configure_proc()
                    cur.execute(query)
                    self.fill_table_conf(1, cur)
                    self.check_rows(proc_row, self.tableConfProc)
                    cur.execute(f"select distinct series from({query}) as s1")
                    list_series = []
                    for name in cur:
                        list_series.append(name[0])
                    self.fill_tabs_configure(list_series, self.tabWidgetProc)

                    mother_row = self.save_row(
                        self.tableConfMother)  # !!! Сохраняем строчку в фильтруемых таблицах, если они выделена!!!!
                    query = self.configure_mother()
                    cur.execute(query)
                    self.fill_table_conf(2, cur)
                    self.check_rows(mother_row, self.tableConfMother)
                    cur.execute(f"select distinct socket from({query}) as s1")
                    list_socket = []
                    for name in cur:
                        list_socket.append(name[0])
                    self.fill_tabs_configure(list_socket, self.tabWidgetMother)

                case self.tableConfPower:  # По выбранному БП отсортировать видеокарту, процессор и корпус
                    video_row = self.save_row(
                        self.tableConfVideo)  # !!! Сохраняем строчку в фильтруемых таблицах, если они выделена!!!!
                    query = self.configure_video()
                    cur.execute(query)
                    self.fill_table_conf(0, cur)
                    self.check_rows(video_row, self.tableConfVideo)
                    cur.execute(f"select distinct name from({query}) as s1")
                    list_proizv = []
                    for name in cur:
                        list_proizv.append(name[0])
                    self.fill_tabs_configure(list_proizv, self.tabWidgetVideo)

                    mother_row = self.save_row(
                        self.tableConfMother)  # !!! Сохраняем строчку в фильтруемых таблицах, если они выделена!!!!
                    query = self.configure_mother()
                    cur.execute(query)
                    self.fill_table_conf(2, cur)
                    self.check_rows(mother_row, self.tableConfMother)
                    cur.execute(f"select distinct socket from({query}) as s1")
                    list_socket = []
                    for name in cur:
                        list_socket.append(name[0])
                    self.fill_tabs_configure(list_socket, self.tabWidgetMother)

                    body_row = self.save_row(
                        self.tableConfBody)  # !!! Сохраняем строчку в фильтруемых таблицах, если они выделена!!!!
                    query = self.configure_body()
                    cur.execute(query)
                    self.fill_table_conf(7, cur)
                    self.check_rows(body_row, self.tableConfBody)
                    cur.execute(f"select distinct name from({query}) as s1")
                    list_proizv = []
                    for name in cur:
                        list_proizv.append(name[0])
                    self.fill_tabs_configure(list_proizv, self.tabWidgetBody)

                case self.tableConfBody:  # По выбранной ОЗУ отсортировать мат. плату и процессор
                    video_row = self.save_row(
                        self.tableConfVideo)  # !!! Сохраняем строчку в фильтруемых таблицах, если они выделена!!!!
                    query = self.configure_video()
                    cur.execute(query)
                    self.fill_table_conf(0, cur)
                    self.check_rows(video_row, self.tableConfVideo)
                    cur.execute(f"select distinct name from({query}) as s1")
                    list_proizv = []
                    for name in cur:
                        list_proizv.append(name[0])
                    self.fill_tabs_configure(list_proizv, self.tabWidgetVideo)

                    mother_row = self.save_row(
                        self.tableConfMother)  # !!! Сохраняем строчку в фильтруемых таблицах, если они выделена!!!!
                    query = self.configure_mother()
                    cur.execute(query)
                    self.fill_table_conf(2, cur)
                    self.check_rows(mother_row, self.tableConfMother)
                    cur.execute(f"select distinct socket from({query}) as s1")
                    list_socket = []
                    for name in cur:
                        list_socket.append(name[0])
                    self.fill_tabs_configure(list_socket, self.tabWidgetMother)

                    cool_row = self.save_row(
                        self.tableConfCool)  # !!! Сохраняем строчку в фильтруемых таблицах, если они выделена!!!!
                    query = self.configure_cool()
                    cur.execute(query)
                    self.fill_table_conf(3, cur)
                    self.check_rows(cool_row, self.tableConfCool)
                    cur.execute(f"select distinct type from({query}) as s1")
                    list_type = []
                    for name in cur:
                        list_type.append(name[0])
                    self.fill_tabs_configure(list_type, self.tabWidgetCool)

                    power_row = self.save_row(
                        self.tableConfPower)  # !!! Сохраняем строчку в фильтруемых таблицах, если они выделена!!!!
                    query = self.configure_power()
                    cur.execute(query)
                    self.fill_table_conf(6, cur)
                    self.check_rows(power_row, self.tableConfPower)
                    cur.execute(f"select distinct formfactor from({query}) as s1")
                    list_ff = []
                    for name in cur:
                        list_ff.append(name[0])
                    self.fill_tabs_configure(list_ff, self.tabWidgetPower)

        except (Exception, psycopg2.DatabaseError) as error:
            dialog = DialogOk("Ошибка", str(error))
            dialog.show()

        finally:
            if conn:
                cur.close()
                conn.close()

    def save_row(self, table):
        index_row = -1
        data_row = []
        if table.currentRow() != -1:  # Если была выбрана строка, то сохраняем её номер
            index_row = table.currentRow()
            if table == self.tableSklad:
                data_row = self.current_sklad()
            else:
                data_row = self.current_conf(table)  # Сохранение строки
            self.dict_current[table.objectName()] = data_row  # Убрать ретёрн и оставить словарь?
            return data_row
        return []

    def check_rows(self, saved_row, table):
        checkable_row = []
        column_count = table.columnCount()
        row_count = table.rowCount()
        if saved_row:  # Если saved_row заполнена (была выбрана строка, тогда сравниваем. иначе - пропуск циклов)
            for j in range(row_count):
                for i in range(2, column_count):
                    checkable_row.append(table.item(j, i).text())
                if checkable_row == saved_row:  # Если нашли такую же строку - отмечаем её без конфигурирования
                    self.cell_row_without_conf(j, 0, table)
                    return True
                checkable_row.clear()
        # Если в отфильтрованной таблице нет выделенной ранее строки (метод не вернул true), то чистим корзину
        self.clear_cart(table)  # Метод вызывается и на складе.
        return False

    # Метод заполнения корзины выбранных комплектующих (принимает таблицу, из которой был вызван, имя и цену)
    def fill_cart(self, table):
        row_count = self.table_config.rowCount()
        name = ""
        price = ""
        price_configuration = []
        name = table.item(table.currentRow(), 2).text()
        price = table.item(table.currentRow(), table.columnCount() - 1).text()

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
