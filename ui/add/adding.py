import psycopg2

from PyQt5 import QtWidgets
from PyQt5.QtCore import QDateTime
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QDialog
# ----------файлы интерфейса---------------
from ui import warningWin
from ui.add import addChVidWidg, addChProcWidg, addChMotherWidg, addChCoolWidg, addChRamWidg, addChDiskWidg, \
    addChPowerWidg, addChBodyWidg


# Проверяет и окрашивает название поле, если то заполнено неверно (не заполнено вовсе)
def mark_labels(line_edit, label):
    if line_edit.text() != "":  # Если верно - перезадаём стиль (меняем цвет на белый)
        label.setStyleSheet("")
        if label.text()[-1] == "*":  # Если мы меняли эту строку - удаляем 2 символа
            label.setText(label.text()[:len(label.text()) - 2])
    else:  # Если заполнено неверно - добавление * и окрашивание надписи в красный
        if label.text()[-1] != "*":  # Если не меняли строку - не добавляем "*"
            label.setText(label.text() + ' *')
            label.setStyleSheet("color: rgb(240,0,0);")


# Класс диалогового окна с одной кнопкой
class DialogOk(QDialog, warningWin.Ui_warningDialog):
    def __init__(self, error_win_title, error_text):
        QDialog.__init__(self)
        self.setupUi(self)
        self.setWindowTitle(error_win_title)
        self.lbErrDescription.setText(str(error_text))
        self.btnCancel.clicked.connect(lambda: self.close())


# Класс окна с добавлением\редактированием видеокарты
class AddChangeVideoWindow(QtWidgets.QWidget, addChVidWidg.Ui_addChVidWidg):
    def __init__(self, main_window, new_bool, list_valid_proizv, dict_proizv, dict_videocard):
        super().__init__()
        self.setupUi(self)
        if new_bool:
            self.setWindowTitle("Добавление видеокарты")
            self.dateEdit.setDisabled(True)
            self.dateEdit.setStyleSheet("QDateEdit{color:gray; border: 1px dotted rgb(120,120,120); padding-left: 5px;}"
                                        " QDateEdit::drop-down{border: 0px;}"
                                        '''QDateEdit::down-arrow {
                                        border-image: url("E:/pcconf/images/down-arrow-gray.png");
                                        width: 17px;
                                        height: 17px;
                                        margin-right: 5px;}''')
        else:
            self.setWindowTitle("Создание заказа")
        self.dateEdit.setDateTime(QDateTime.currentDateTime())
        #  временные рамки заказа?
        # Вызов метода проверки корректности заполнения полей
        self.btnSave.clicked.connect(
            lambda: self.sql_insert_videocard(new_bool, main_window, dict_proizv, dict_videocard))

        three_digits_int = QIntValidator()
        three_digits_int.setRange(0, 999)

        four_digits_int = QIntValidator()
        four_digits_int.setRange(0, 9999)

        five_digits_int = QIntValidator()
        five_digits_int.setRange(0, 99999)

        six_digits_int = QIntValidator()
        six_digits_int.setRange(0, 999999)

        self.leVolume.setValidator(five_digits_int)
        self.leBus.setValidator(four_digits_int)
        self.leFreq.setValidator(four_digits_int)
        self.leTdp.setValidator(three_digits_int)
        self.leLength.setValidator(three_digits_int)
        self.leKol.setValidator(four_digits_int)
        self.lePrice.setValidator(six_digits_int)
        self.cbProizv.clear()
        if type(list_valid_proizv) == str:  # Если передан 1 параметр в виде строки
            one_list = [list_valid_proizv]
            self.cbProizv.addItems(one_list)
        else:
            self.cbProizv.addItems(list_valid_proizv)

    # Метод отправки запроса в БД на создание записи. выдаёт ошибку, если есть пустые поля
    # Окрашивает надписи к полям, которые не заполнены (cb заполнены всегда, поэтому их не красит)
    def sql_insert_videocard(self, new_bool, main_window, dict_proizv, dict_videocard):
        conn = None
        cur = None
        try:
            conn = psycopg2.connect(database="confPc",
                                    user="postgres",
                                    password="2001",
                                    host="localhost",
                                    port="5432")
            cur = conn.cursor()
            id_pr = {i for i in dict_proizv
                     if dict_proizv[i] == self.cbProizv.currentText()}
            if new_bool:  # Если создаём новый заказ - вызываем 2 процедуры и заполняем их
                mark_labels(self.leFullName, self.lbFullName)
                mark_labels(self.leChipName, self.lbChipName)
                mark_labels(self.leVolume, self.lbVolume)
                mark_labels(self.leType, self.lbType)
                mark_labels(self.leBus, self.lbBus)
                mark_labels(self.leFreq, self.lbFreq)
                mark_labels(self.leTdp, self.lbTdp)
                mark_labels(self.leLength, self.lbLength)
                mark_labels(self.lePrice, self.lbPrice)
                if self.leFullName.text() == "" or self.leChipName.text() == "" or self.leVolume.text() == "" or \
                        self.leType.text() == "" or self.leBus.text() == "" or self.leFreq.text() == "" or \
                        self.leLength.text() == "" or self.leTdp.text() == "" or self.lePrice.text() == "":
                    dialog = DialogOk("Ошибка", "Все поля должны быть заполнены")
                    dialog.show()
                else:
                    cur.callproc('insert_videocard', [id_pr.pop(),
                                                      self.leFullName.text(),
                                                      self.cbGaming.currentText(),
                                                      self.cbChipCreator.currentText(),
                                                      self.leChipName.text(),
                                                      int(self.leVolume.text()),
                                                      self.leType.text(),
                                                      int(self.leFreq.text()),
                                                      int(self.leBus.text()),
                                                      self.cbInterface.currentText(),
                                                      int(self.cbMonitor.currentText()),
                                                      self.cbResolution.currentText(),
                                                      int(self.leTdp.text()),
                                                      int(self.leLength.text()),
                                                      int(self.cbPinVideo.currentText()),
                                                      int(self.cbPinVideoKol.currentText()),
                                                      int(self.lePrice.text())])
                    self.close()
            else:  # Если повторяем заказ - вызываем 1 процедуру и заполняем её
                mark_labels(self.leKol, self.lbKol)
                if self.leKol.text() == "" or int(self.leKol.text()) < 1:
                    dialog = DialogOk("Ошибка", "Заполните поле 'Количество' числом >= 1 ")
                    dialog.show()
                else:
                    id_izd = {i for i in dict_videocard
                              if dict_videocard[i] == self.leFullName.text()}
                    cur.callproc('insert_order_videocard', [id_izd.pop(),
                                                            int(self.leKol.text()),
                                                            self.dateEdit.dateTime().toString("yyyy-MM-dd")])
                    self.close()

        except (Exception, psycopg2.DatabaseError) as error:
            dialog = DialogOk("Ошибка", error)
            dialog.show()
        finally:
            if conn:
                conn.commit()
                cur.close()
                conn.close()
                main_window.reset_all_config()
                main_window.reset_radiobutton(main_window.tableSklad)
                main_window.load_sklad(0)  # Загрузка обновлённой таблицы Материнских плат из БД на склад
                main_window.load_conf(0)  # Загрузка обновлённой таблицы Материнских плат из БД в конфигуратор
                main_window.toolBoxNavigation.setCurrentIndex(0)
                main_window.create_sklad_filter()  # Пересоздание экземпляра класса фильтров для отображения новых данных
                main_window.create_conf_filter()  # Пересоздание экземпляра класса фильтров для отображения новых данных


# Класс окна с добавлением\редактированием процессора
class AddChangeProcWindow(QtWidgets.QWidget, addChProcWidg.Ui_addChProcWidg):
    def __init__(self, main_window, new_bool, list_valid_proizv, dict_proizv, dict_processor):
        super().__init__()
        self.setupUi(self)
        if new_bool:
            self.setWindowTitle("Добавление процессора")
            self.dateEdit.setDisabled(True)
            self.dateEdit.setStyleSheet("QDateEdit{color:gray; border: 1px dotted rgb(120,120,120); padding-left: 5px;}"
                                        " QDateEdit::drop-down{border: 0px;}"
                                        '''QDateEdit::down-arrow {
                                        border-image: url("E:/pcconf/images/down-arrow-gray.png");
                                        width: 17px;
                                        height: 17px;
                                        margin-right: 5px;}''')
        else:
            self.setWindowTitle("Создание заказа")
        self.dateEdit.setDateTime(QDateTime.currentDateTime())
        #  временные рамки заказа?
        # Вызов метода проверки корректности заполнения полей
        self.btnSave.clicked.connect(
            lambda: self.sql_insert_processor(new_bool, main_window, dict_proizv, dict_processor))

        two_digits_int = QIntValidator()
        two_digits_int.setRange(0, 99)

        three_digits_int = QIntValidator()
        three_digits_int.setRange(0, 999)

        four_digits_int = QIntValidator()
        four_digits_int.setRange(0, 9999)

        five_digits_int = QIntValidator()
        five_digits_int.setRange(0, 99999)

        six_digits_int = QIntValidator()
        six_digits_int.setRange(0, 999999)

        self.leNcores.setValidator(two_digits_int)
        self.leRamFreq.setValidator(four_digits_int)
        self.leFreq.setValidator(four_digits_int)
        self.leTdp.setValidator(three_digits_int)
        self.leKol.setValidator(four_digits_int)
        self.lePrice.setValidator(six_digits_int)
        self.cbProizv.clear()
        if type(list_valid_proizv) == str:  # Если передан 1 параметр в виде строки
            one_list = [list_valid_proizv]
            self.cbProizv.addItems(one_list)
        else:
            self.cbProizv.addItems(list_valid_proizv)

    def sql_insert_processor(self, new_bool, main_window, dict_proizv, dict_processor):
        conn = None
        cur = None
        try:
            conn = psycopg2.connect(database="confPc",
                                    user="postgres",
                                    password="2001",
                                    host="localhost",
                                    port="5432")
            cur = conn.cursor()
            id_pr = {i for i in dict_proizv
                     if dict_proizv[i] == self.cbProizv.currentText()}
            if new_bool:  # Если создаём новый заказ - вызываем 2 процедуры и заполняем их
                mark_labels(self.leFullName, self.lbFullName)
                mark_labels(self.leSeries, self.lbSeries)
                mark_labels(self.leSocket, self.lbSocket)
                mark_labels(self.leCore, self.lbCore)
                mark_labels(self.leRamFreq, self.lbRamFreq)
                mark_labels(self.leFreq, self.lbFreq)
                mark_labels(self.leCache, self.lbCache)
                mark_labels(self.leTdp, self.lbTdp)
                mark_labels(self.leTechproc, self.lbTechproc)
                mark_labels(self.leGraphics, self.lbGraphics)
                mark_labels(self.lePrice, self.lbPrice)
                if self.leFullName.text() == "" or self.leSeries.text() == "" or self.leSocket.text() == "" or \
                        self.leCore.text() == "" or self.leRamFreq.text() == "" or self.leFreq.text() == "" or \
                        self.leTechproc.text() == "" or self.leGraphics.text() == "" or self.leTdp.text() == "" \
                        or self.leCache.text() == "" or self.lePrice.text() == "":
                    dialog = DialogOk("Ошибка", "Все поля должны быть заполнены")
                    dialog.show()
                else:
                    graphics = self.leGraphics.text()
                    if graphics.lower() == "нет": graphics = "нет"  # Если ввели "Нет", то вставляем в нижнем регистре
                    cur.callproc('insert_processor', [id_pr.pop(),
                                                      self.leFullName.text(),
                                                      self.cbGaming.currentText(),
                                                      self.leSeries.text(),
                                                      self.leSocket.text(),
                                                      self.leCore.text(),
                                                      int(self.leNcores.text()),
                                                      int(self.leCache.text()),
                                                      int(self.leFreq.text()),
                                                      self.leTechproc.text(),
                                                      int(self.leRamFreq.text()),
                                                      graphics,
                                                      int(self.leTdp.text()),
                                                      int(self.lePrice.text())])
                    self.close()
            else:  # Если повторяем заказ - вызываем 1 процедуру и заполняем её
                mark_labels(self.leKol, self.lbKol)
                if self.leKol.text() == "" or int(self.leKol.text()) < 1:
                    dialog = DialogOk("Ошибка", "Заполните поле 'Количество' числом >= 1 ")
                    dialog.show()
                else:
                    id_izd = {i for i in dict_processor
                              if dict_processor[i] == self.leFullName.text()}
                    cur.callproc('insert_order_processor', [id_izd.pop(),
                                                            int(self.leKol.text()),
                                                            self.dateEdit.dateTime().toString("yyyy-MM-dd")])
                self.close()

        except (Exception, psycopg2.DatabaseError) as error:
            dialog = DialogOk("Ошибка", error)
            dialog.show()
        finally:
            if conn:
                conn.commit()
                cur.close()
                conn.close()
                main_window.reset_all_config()
                main_window.reset_radiobutton(main_window.tableSklad)
                main_window.load_sklad(1)  # Загрузка обновлённой таблицы Материнских плат из БД на склад
                main_window.load_conf(1)  # Загрузка обновлённой таблицы Материнских плат из БД в конфигуратор
                main_window.toolBoxNavigation.setCurrentIndex(1)
                main_window.create_sklad_filter()  # Пересоздание экземпляра класса фильтров для отображения новых данных
                main_window.create_conf_filter()  # Пересоздание экземпляра класса фильтров для отображения новых данных


# Класс окна с добавлением\редактированием мат. платы
class AddChangeMotherWindow(QtWidgets.QWidget, addChMotherWidg.Ui_addChMotherWidg):
    def __init__(self, main_window, new_bool, list_valid_proizv, dict_proizv, dict_motherboard):
        super().__init__()
        self.setupUi(self)
        if new_bool:
            self.setWindowTitle("Добавление материнской платы")
            self.dateEdit.setDisabled(True)
            self.dateEdit.setStyleSheet("QDateEdit{color:gray; border: 1px dotted rgb(120,120,120); padding-left: 5px;}"
                                        " QDateEdit::drop-down{border: 0px;}"
                                        '''QDateEdit::down-arrow {
                                        border-image: url("E:/pcconf/images/down-arrow-gray.png");
                                        width: 17px;
                                        height: 17px;
                                        margin-right: 5px;}''')
        else:
            self.setWindowTitle("Создание заказа")
        self.dateEdit.setDateTime(QDateTime.currentDateTime())
        #  временные рамки заказа?
        # Вызов метода проверки корректности заполнения полей
        self.btnSave.clicked.connect(
            lambda: self.sql_insert_mother(new_bool, main_window, dict_proizv, dict_motherboard))

        three_digits_int = QIntValidator()
        three_digits_int.setRange(0, 999)

        four_digits_int = QIntValidator()
        four_digits_int.setRange(0, 9999)
        six_digits_int = QIntValidator()
        six_digits_int.setRange(0, 999999)

        self.leRamMax.setValidator(three_digits_int)
        self.leFreqMax.setValidator(four_digits_int)
        self.leKol.setValidator(four_digits_int)
        self.lePrice.setValidator(six_digits_int)
        self.cbProizv.clear()
        if type(list_valid_proizv) == str:  # Если передан 1 параметр в виде строки
            one_list = [list_valid_proizv]
            self.cbProizv.addItems(one_list)
        else:
            self.cbProizv.addItems(list_valid_proizv)

    def sql_insert_mother(self, new_bool, main_window, dict_proizv, dict_motherboard):
        conn = None
        cur = None
        try:
            conn = psycopg2.connect(database="confPc",
                                    user="postgres",
                                    password="2001",
                                    host="localhost",
                                    port="5432")
            cur = conn.cursor()
            id_pr = {i for i in dict_proizv
                     if dict_proizv[i] == self.cbProizv.currentText()}
            if new_bool:  # Если создаём новый заказ - вызываем 2 процедуры и заполняем их
                mark_labels(self.leFullName, self.lbFullName)
                mark_labels(self.leSocket, self.lbSocket)
                mark_labels(self.leChipset, self.lbChipset)
                mark_labels(self.leFreqMax, self.lbFreqMax)
                mark_labels(self.leRamMax, self.lbRamMax)
                mark_labels(self.lePrice, self.lbPrice)
                if self.leFullName.text() == "" or self.leChipset.text() == "" or self.leSocket.text() == "" or \
                        self.leFreqMax.text() == "" or self.leRamMax.text() == "" or self.lePrice.text() == "":
                    dialog = DialogOk("Ошибка", "Все поля должны быть заполнены")
                    dialog.show()
                else:
                    cur.callproc('insert_motherboard', [id_pr.pop(),
                                                        self.leFullName.text(),
                                                        self.cbGaming.currentText(),
                                                        self.leSocket.text(),
                                                        self.leChipset.text(),
                                                        self.cbFactor.currentText(),
                                                        self.cbPcie.currentText(),
                                                        self.cbRamType.currentText(),
                                                        self.cbRamSlots.currentText(),
                                                        self.leRamMax.text(),
                                                        self.leFreqMax.text(),
                                                        self.cbM2.currentText(),
                                                        self.cbSata.currentText(),
                                                        int(self.cbPinCool.currentText()),
                                                        int(self.cbPinCpu.currentText()),
                                                        int(self.cbPinCpuKol.currentText()),
                                                        int(self.lePrice.text())])
                    self.close()
            else:  # Если повторяем заказ - вызываем 1 процедуру и заполняем её
                mark_labels(self.leKol, self.lbKol)
                if self.leKol.text() == "" or int(self.leKol.text()) < 1:
                    dialog = DialogOk("Ошибка", "Заполните поле 'Количество' числом >= 1 ")
                    dialog.show()
                else:
                    id_izd = {i for i in dict_motherboard
                              if dict_motherboard[i] == self.leFullName.text()}
                    cur.callproc('insert_order_motherboard', [id_izd.pop(),
                                                              int(self.leKol.text()),
                                                              self.dateEdit.dateTime().toString("yyyy-MM-dd")])
                self.close()

        except (Exception, psycopg2.DatabaseError) as error:
            dialog = DialogOk("Ошибка", error)
            dialog.show()
        finally:
            if conn:
                conn.commit()
                cur.close()
                conn.close()
                main_window.reset_all_config()
                main_window.reset_radiobutton(main_window.tableSklad)
                main_window.load_sklad(2)  # Загрузка обновлённой таблицы Материнских плат из БД на склад
                main_window.load_conf(2)  # Загрузка обновлённой таблицы Материнских плат из БД в конфигуратор
                main_window.toolBoxNavigation.setCurrentIndex(2)
                main_window.create_sklad_filter()  # Пересоздание экземпляра класса фильтров для отображения новых
                # данных
                main_window.create_conf_filter()  # Пересоздание экземпляра класса фильтров для отображения новых данных


# Класс окна с добавлением\редактированием охлаждения
class AddChangeCoolWindow(QtWidgets.QWidget, addChCoolWidg.Ui_addChCoolWidg):
    def __init__(self, main_window, new_bool, list_valid_proizv, dict_proizv, dict_cool):
        super().__init__()
        self.setupUi(self)
        if new_bool:
            self.setWindowTitle("Добавление охлаждения процессора")
            self.dateEdit.setDisabled(True)
            self.dateEdit.setStyleSheet("QDateEdit{color:gray; border: 1px dotted rgb(120,120,120); padding-left: 5px;}"
                                        " QDateEdit::drop-down{border: 0px;}"
                                        '''QDateEdit::down-arrow {
                                        border-image: url("E:/pcconf/images/down-arrow-gray.png");
                                        width: 17px;
                                        height: 17px;
                                        margin-right: 5px;}''')
        else:
            self.setWindowTitle("Создание заказа")
        self.dateEdit.setDateTime(QDateTime.currentDateTime())
        #  временные рамки заказа?
        # Вызов метода проверки корректности заполнения полей
        self.btnSave.clicked.connect(
            lambda: self.sql_insert_cool(new_bool, main_window, dict_proizv, dict_cool))

        three_digits_int = QIntValidator()
        three_digits_int.setRange(0, 999)

        four_digits_int = QIntValidator()
        four_digits_int.setRange(0, 9999)
        six_digits_int = QIntValidator()
        six_digits_int.setRange(0, 999999)

        self.leHeight.setValidator(three_digits_int)
        self.leDisperse.setValidator(three_digits_int)
        self.leKol.setValidator(four_digits_int)
        self.lePrice.setValidator(six_digits_int)
        self.cbProizv.clear()
        if type(list_valid_proizv) == str:  # Если передан 1 параметр в виде строки
            one_list = [list_valid_proizv]
            self.cbProizv.addItems(one_list)
        else:
            self.cbProizv.addItems(list_valid_proizv)

    def sql_insert_cool(self, new_bool, main_window, dict_proizv, dict_cool):
        conn = None
        cur = None
        try:
            conn = psycopg2.connect(database="confPc",
                                    user="postgres",
                                    password="2001",
                                    host="localhost",
                                    port="5432")
            cur = conn.cursor()
            id_pr = {i for i in dict_proizv
                     if dict_proizv[i] == self.cbProizv.currentText()}
            if new_bool:  # Если создаём новый заказ - вызываем 2 процедуры и заполняем их
                mark_labels(self.leFullName, self.lbFullName)
                mark_labels(self.leSocket, self.lbSocket)
                mark_labels(self.leHeight, self.lbHeight)
                mark_labels(self.leDisperse, self.lbDisperse)
                mark_labels(self.lePrice, self.lbPrice)
                if self.leFullName.text() == "" or self.leHeight.text() == "" or self.leSocket.text() == "" or \
                        self.leDisperse.text() == "" or self.lePrice.text() == "":
                    dialog = DialogOk("Ошибка", "Все поля должны быть заполнены")
                    dialog.show()
                else:
                    cur.callproc('insert_cool', [id_pr.pop(),
                                                 self.leFullName.text(),
                                                 self.cbConstruction.currentText(),
                                                 self.cbType.currentText(),
                                                 self.leSocket.text(),
                                                 self.cbPipe.currentText(),
                                                 self.leHeight.text(),
                                                 self.leDisperse.text(),
                                                 self.leVoltage.text(),
                                                 self.cbConnect.currentText(),
                                                 int(self.lePrice.text())])
                    self.close()
            else:  # Если повторяем заказ - вызываем 1 процедуру и заполняем её
                mark_labels(self.leKol, self.lbKol)
                if self.leKol.text() == "" or int(self.leKol.text()) < 1:
                    dialog = DialogOk("Ошибка", "Заполните поле 'Количество' числом >= 1 ")
                    dialog.show()
                else:
                    id_izd = {i for i in dict_cool
                              if dict_cool[i] == self.leFullName.text()}
                    cur.callproc('insert_order_cool', [id_izd.pop(),
                                                       int(self.leKol.text()),
                                                       self.dateEdit.dateTime().toString("yyyy-MM-dd")])
                self.close()

        except (Exception, psycopg2.DatabaseError) as error:
            dialog = DialogOk("Ошибка", error)
            dialog.show()
        finally:
            if conn:
                conn.commit()
                cur.close()
                conn.close()
                main_window.reset_all_config()
                main_window.reset_radiobutton(main_window.tableSklad)
                main_window.load_sklad(3)  # Загрузка обновлённой таблицы Материнских плат из БД на склад
                main_window.load_conf(3)  # Загрузка обновлённой таблицы Материнских плат из БД в конфигуратор
                main_window.toolBoxNavigation.setCurrentIndex(3)
                main_window.create_sklad_filter()  # Пересоздание экземпляра класса фильтров для отображения новых данных
                main_window.create_conf_filter()  # Пересоздание экземпляра класса фильтров для отображения новых данных


# Класс окна с добавлением\редактированием ОЗУ
class AddChangeRamWindow(QtWidgets.QWidget, addChRamWidg.Ui_addChRamWidg):
    def __init__(self, main_window, new_bool, list_valid_proizv, dict_proizv, dict_ram):
        super().__init__()
        self.setupUi(self)
        if new_bool:
            self.setWindowTitle("Добавление оперативной памяти")
            self.dateEdit.setDisabled(True)
            self.dateEdit.setStyleSheet(
                "QDateEdit{color:gray; border: 1px dotted rgb(120,120,120); padding-left: 5px;}"
                " QDateEdit::drop-down{border: 0px;}"
                '''QDateEdit::down-arrow {
                                        border-image: url("E:/pcconf/images/down-arrow-gray.png");
                                        width: 17px;
                                        height: 17px;
                                        margin-right: 5px;}''')
        else:
            self.setWindowTitle("Создание заказа")
        self.dateEdit.setDateTime(QDateTime.currentDateTime())
        #  временные рамки заказа?
        # Вызов метода проверки корректности заполнения полей
        self.btnSave.clicked.connect(
            lambda: self.sql_insert_ram(new_bool, main_window, dict_proizv, dict_ram))
        # float_digits = QDoubleValidator()
        two_digits_int = QIntValidator()
        two_digits_int.setRange(0, 99)

        three_digits_int = QIntValidator()
        three_digits_int.setRange(0, 999)

        four_digits_int = QIntValidator()
        four_digits_int.setRange(0, 9999)
        six_digits_int = QIntValidator()
        six_digits_int.setRange(0, 999999)

        self.leFreq.setValidator(four_digits_int)
        self.leLatency.setValidator(two_digits_int)
        # self.leVoltage.setValidator(float_digits)
        self.leKol.setValidator(four_digits_int)
        self.lePrice.setValidator(six_digits_int)
        self.cbProizv.clear()
        if type(list_valid_proizv) == str:  # Если передан 1 параметр в виде строки
            one_list = [list_valid_proizv]
            self.cbProizv.addItems(one_list)
        else:
            self.cbProizv.addItems(list_valid_proizv)

    def sql_insert_ram(self, new_bool, main_window, dict_proizv, dict_ram):
        conn = None
        cur = None
        try:
            conn = psycopg2.connect(database="confPc",
                                    user="postgres",
                                    password="2001",
                                    host="localhost",
                                    port="5432")
            cur = conn.cursor()
            id_pr = {i for i in dict_proizv
                     if dict_proizv[i] == self.cbProizv.currentText()}
            if new_bool:  # Если создаём новый заказ - вызываем 2 процедуры и заполняем их
                mark_labels(self.leFullName, self.lbFullName)
                mark_labels(self.leFreq, self.lbFreq)
                mark_labels(self.leLatency, self.lbLatency)
                mark_labels(self.leVoltage, self.lbVoltage)
                mark_labels(self.lePrice, self.lbPrice)
                if self.leFullName.text() == "" or self.leFreq.text() == "" or \
                        self.leLatency.text() == "" or self.leVoltage.text() == "" or self.lePrice.text() == "":
                    dialog = DialogOk("Ошибка", "Все поля должны быть заполнены")
                    dialog.show()
                else:
                    cur.callproc('insert_ram', [id_pr.pop(),
                                                self.leFullName.text(),
                                                self.cbGaming.currentText(),
                                                self.cbRamType.currentText(),
                                                self.cbVolume.currentText(),
                                                self.leFreq.text(),
                                                self.cbModule.currentText(),
                                                self.leLatency.text(),
                                                float(self.leVoltage.text()),
                                                int(self.lePrice.text())])
                    self.close()
            else:  # Если повторяем заказ - вызываем 1 процедуру и заполняем её
                mark_labels(self.leKol, self.lbKol)
                if self.leKol.text() == "" or int(self.leKol.text()) < 1:
                    dialog = DialogOk("Ошибка", "Заполните поле 'Количество' числом >= 1 ")
                    dialog.show()
                else:
                    id_izd = {i for i in dict_ram
                              if dict_ram[i] == self.leFullName.text()}
                    cur.callproc('insert_order_ram', [id_izd.pop(),
                                                      int(self.leKol.text()),
                                                      self.dateEdit.dateTime().toString("yyyy-MM-dd")])
                self.close()

        except (Exception, psycopg2.DatabaseError) as error:
            dialog = DialogOk("Ошибка", error)
            dialog.show()
        finally:
            if conn:
                conn.commit()
                cur.close()
                conn.close()
                main_window.reset_all_config()
                main_window.reset_radiobutton(main_window.tableSklad)
                main_window.load_sklad(4)
                main_window.load_conf(4)
                main_window.toolBoxNavigation.setCurrentIndex(4)
                main_window.create_sklad_filter()
                main_window.create_conf_filter()


# Класс окна с добавлением\редактированием накопителя
class AddChangeDiskWindow(QtWidgets.QWidget, addChDiskWidg.Ui_addChDiskWidg):
    def __init__(self, main_window, new_bool, list_valid_proizv, dict_proizv, dict_disk):
        super().__init__()
        self.setupUi(self)
        if new_bool:
            self.setWindowTitle("Добавление накопителя")
            self.dateEdit.setDisabled(True)
            self.dateEdit.setStyleSheet(
                "QDateEdit{color:gray; border: 1px dotted rgb(120,120,120); padding-left: 5px;}"
                " QDateEdit::drop-down{border: 0px;}"
                '''QDateEdit::down-arrow {
                                        border-image: url("E:/pcconf/images/down-arrow-gray.png");
                                        width: 17px;
                                        height: 17px;
                                        margin-right: 5px;}''')
        else:
            self.setWindowTitle("Создание заказа")
        self.dateEdit.setDateTime(QDateTime.currentDateTime())
        #  временные рамки заказа?
        # Вызов метода проверки корректности заполнения полей
        self.btnSave.clicked.connect(
            lambda: self.sql_insert_disk(new_bool, main_window, dict_proizv, dict_disk))

        # float_digits = QDoubleValidator()
        # float_digits.setRange(0, 9)

        two_digits_int = QIntValidator()
        two_digits_int.setRange(0, 99)

        three_digits_int = QIntValidator()
        three_digits_int.setRange(0, 999)

        four_digits_int = QIntValidator()
        four_digits_int.setRange(0, 9999)
        six_digits_int = QIntValidator()
        six_digits_int.setRange(0, 999999)

        self.leWrite.setValidator(four_digits_int)
        self.leRead.setValidator(four_digits_int)
        self.leVolume.setValidator(four_digits_int)
        self.leKol.setValidator(four_digits_int)
        self.lePrice.setValidator(six_digits_int)
        self.cbProizv.clear()
        if type(list_valid_proizv) == str:  # Если передан 1 параметр в виде строки
            one_list = [list_valid_proizv]
            self.cbProizv.addItems(one_list)
        else:
            self.cbProizv.addItems(list_valid_proizv)

    def sql_insert_disk(self, new_bool, main_window, dict_proizv, dict_disk):
        conn = None
        cur = None
        try:
            conn = psycopg2.connect(database="confPc",
                                    user="postgres",
                                    password="2001",
                                    host="localhost",
                                    port="5432")
            cur = conn.cursor()
            id_pr = {i for i in dict_proizv
                     if dict_proizv[i] == self.cbProizv.currentText()}
            if new_bool:  # Если создаём новый заказ - вызываем 2 процедуры и заполняем их
                mark_labels(self.leFullName, self.lbFullName)
                mark_labels(self.leWrite, self.lbWrite)
                mark_labels(self.leRead, self.lbRead)
                mark_labels(self.leVolume, self.lbVolume)
                mark_labels(self.lePrice, self.lbPrice)
                if self.leFullName.text() == "" or self.leWrite.text() == "" or self.leVolume.text() == "" or \
                        self.leRead.text() == "" or self.lePrice.text() == "":
                    dialog = DialogOk("Ошибка", "Все поля должны быть заполнены")
                    dialog.show()
                else:
                    cur.callproc('insert_disk', [id_pr.pop(),
                                                 self.leFullName.text(),
                                                 self.cbType.currentText(),
                                                 self.leVolume.text(),
                                                 self.cbConnect.currentText(),
                                                 self.leRead.text(),
                                                 self.leWrite.text(),
                                                 self.cbRpm.currentText(),
                                                 int(self.lePrice.text())])
                    self.close()
            else:  # Если повторяем заказ - вызываем 1 процедуру и заполняем её
                mark_labels(self.leKol, self.lbKol)
                if self.leKol.text() == "" or int(self.leKol.text()) < 1:
                    dialog = DialogOk("Ошибка", "Заполните поле 'Количество' числом >= 1 ")
                    dialog.show()
                else:
                    id_izd = {i for i in dict_disk
                              if dict_disk[i] == self.leFullName.text()}
                    cur.callproc('insert_order_disk', [id_izd.pop(),
                                                       int(self.leKol.text()),
                                                       self.dateEdit.dateTime().toString("yyyy-MM-dd")])
                self.close()

        except (Exception, psycopg2.DatabaseError) as error:
            dialog = DialogOk("Ошибка", error)
            dialog.show()
        finally:
            if conn:
                conn.commit()
                cur.close()
                conn.close()
                main_window.reset_all_config()
                main_window.reset_radiobutton(main_window.tableSklad)
                main_window.load_sklad(5)
                main_window.load_conf(5)
                main_window.toolBoxNavigation.setCurrentIndex(5)
                main_window.create_sklad_filter()
                main_window.create_conf_filter()


# Класс окна с добавлением\редактированием БП
class AddChangePowerWindow(QtWidgets.QWidget, addChPowerWidg.Ui_addChPowerWidg):
    def __init__(self, main_window, new_bool, list_valid_proizv, dict_proizv, dict_power):
        super().__init__()
        self.setupUi(self)
        if new_bool:
            self.setWindowTitle("Добавление блока питания")
            self.dateEdit.setDisabled(True)
            self.dateEdit.setStyleSheet(
                "QDateEdit{color:gray; border: 1px dotted rgb(120,120,120); padding-left: 5px;}"
                " QDateEdit::drop-down{border: 0px;}"
                '''QDateEdit::down-arrow {
                                        border-image: url("E:/pcconf/images/down-arrow-gray.png");
                                        width: 17px;
                                        height: 17px;
                                        margin-right: 5px;}''')
        else:
            self.setWindowTitle("Создание заказа")
        self.dateEdit.setDateTime(QDateTime.currentDateTime())
        #  временные рамки заказа?
        # Вызов метода проверки корректности заполнения полей
        self.btnSave.clicked.connect(
            lambda: self.sql_insert_power(new_bool, main_window, dict_proizv, dict_power))

        two_digits_int = QIntValidator()
        two_digits_int.setRange(0, 99)

        three_digits_int = QIntValidator()
        three_digits_int.setRange(0, 999)

        four_digits_int = QIntValidator()
        four_digits_int.setRange(0, 9999)
        six_digits_int = QIntValidator()
        six_digits_int.setRange(0, 999999)

        self.leLenPower.setValidator(three_digits_int)
        self.lePower.setValidator(four_digits_int)
        self.lePinSata.setValidator(two_digits_int)
        self.leKol.setValidator(four_digits_int)
        self.lePrice.setValidator(six_digits_int)
        self.cbProizv.clear()
        if type(list_valid_proizv) == str:  # Если передан 1 параметр в виде строки
            one_list = [list_valid_proizv]
            self.cbProizv.addItems(one_list)
        else:
            self.cbProizv.addItems(list_valid_proizv)

    def sql_insert_power(self, new_bool, main_window, dict_proizv, dict_power):
        conn = None
        cur = None
        try:
            conn = psycopg2.connect(database="confPc",
                                    user="postgres",
                                    password="2001",
                                    host="localhost",
                                    port="5432")
            cur = conn.cursor()
            id_pr = {i for i in dict_proizv
                     if dict_proizv[i] == self.cbProizv.currentText()}
            if new_bool:  # Если создаём новый заказ - вызываем 2 процедуры и заполняем их
                mark_labels(self.leFullName, self.lbFullName)
                mark_labels(self.leLenPower, self.lbLenPower)
                mark_labels(self.lePower, self.lbPower)
                mark_labels(self.lePinSata, self.lbPinSata)
                mark_labels(self.lePrice, self.lbPrice)
                if self.leFullName.text() == "" or self.leLenPower.text() == "" or self.lePower.text() == "" or \
                        self.lePinSata.text() == "" or self.lePrice.text() == "":
                    dialog = DialogOk("Ошибка", "Все поля должны быть заполнены")
                    dialog.show()
                else:
                    cur.callproc('insert_power', [id_pr.pop(),
                                                  self.leFullName.text(),
                                                  self.cbFPower.currentText(),
                                                  self.leLenPower.text(),
                                                  self.lePower.text(),
                                                  self.cbCertificate.currentText(),
                                                  self.cbPinMain.currentText(),
                                                  self.cbPinCpu.currentText(),
                                                  self.cbPinVideo.currentText(),
                                                  int(self.lePinSata.text()),
                                                  self.cbPinCpuKol.currentText(),
                                                  self.cbPinVideoKol.currentText(),
                                                  int(self.lePrice.text())])
                    self.close()
            else:  # Если повторяем заказ - вызываем 1 процедуру и заполняем её
                mark_labels(self.leKol, self.lbKol)
                if self.leKol.text() == "" or int(self.leKol.text()) < 1:
                    dialog = DialogOk("Ошибка", "Заполните поле 'Количество' числом >= 1 ")
                    dialog.show()
                else:
                    id_izd = {i for i in dict_power
                              if dict_power[i] == self.leFullName.text()}
                    cur.callproc('insert_order_power', [id_izd.pop(),
                                                        int(self.leKol.text()),
                                                        self.dateEdit.dateTime().toString("yyyy-MM-dd")])
                self.close()

        except (Exception, psycopg2.DatabaseError) as error:
            dialog = DialogOk("Ошибка", error)
            dialog.show()
        finally:
            if conn:
                conn.commit()
                cur.close()
                conn.close()
                main_window.reset_all_config()
                main_window.reset_radiobutton(main_window.tableSklad)
                main_window.load_sklad(6)
                main_window.load_conf(6)
                main_window.toolBoxNavigation.setCurrentIndex(6)
                main_window.create_sklad_filter()
                main_window.create_conf_filter()


# Класс окна с добавлением\редактированием корпуса
class AddChangeBodyWindow(QtWidgets.QWidget, addChBodyWidg.Ui_addChBodyWidg):
    def __init__(self, main_window, new_bool, list_valid_proizv, dict_proizv, dict_body):
        super().__init__()
        self.setupUi(self)
        if new_bool:
            self.setWindowTitle("Добавление корпуса")
            self.dateEdit.setDisabled(True)
            self.dateEdit.setStyleSheet(
                "QDateEdit{color:gray; border: 1px dotted rgb(120,120,120); padding-left: 5px;}"
                " QDateEdit::drop-down{border: 0px;}"
                '''QDateEdit::down-arrow {
                                        border-image: url("E:/pcconf/images/down-arrow-gray.png");
                                        width: 17px;
                                        height: 17px;
                                        margin-right: 5px;}''')
        else:
            self.setWindowTitle("Создание заказа")
        self.dateEdit.setDateTime(QDateTime.currentDateTime())
        #  временные рамки заказа?
        # Вызов метода проверки корректности заполнения полей
        self.btnSave.clicked.connect(
            lambda: self.sql_insert_body(new_bool, main_window, dict_proizv, dict_body))

        two_digits_int = QIntValidator()
        two_digits_int.setRange(0, 99)

        two_digits_int.setRange(0, 99)

        three_digits_int = QIntValidator()
        three_digits_int.setRange(0, 999)

        four_digits_int = QIntValidator()
        four_digits_int.setRange(0, 9999)
        six_digits_int = QIntValidator()
        six_digits_int.setRange(0, 999999)

        self.leHeightCool.setValidator(three_digits_int)
        self.leLenVideo.setValidator(three_digits_int)
        self.leLenPower.setValidator(three_digits_int)
        self.leKol.setValidator(four_digits_int)
        self.lePrice.setValidator(six_digits_int)
        self.cbProizv.clear()
        if type(list_valid_proizv) == str:  # Если передан 1 параметр в виде строки
            one_list = [list_valid_proizv]
            self.cbProizv.addItems(one_list)
        else:
            self.cbProizv.addItems(list_valid_proizv)

    def sql_insert_body(self, new_bool, main_window, dict_proizv, dict_body):
        conn = None
        cur = None
        try:
            conn = psycopg2.connect(database="confPc",
                                    user="postgres",
                                    password="2001",
                                    host="localhost",
                                    port="5432")
            cur = conn.cursor()
            id_pr = {i for i in dict_proizv
                     if dict_proizv[i] == self.cbProizv.currentText()}
            if new_bool:  # Если создаём новый заказ - вызываем 2 процедуры и заполняем их
                mark_labels(self.leFullName, self.lbFullName)
                mark_labels(self.leWeight, self.lbWeight)
                mark_labels(self.leHeightCool, self.lbHeightCool)
                mark_labels(self.leFMother, self.lbFMother)
                mark_labels(self.leLenVideo, self.lbLenVideo)
                mark_labels(self.leLenPower, self.lbLenPower)
                mark_labels(self.leColor, self.lbColor)
                mark_labels(self.lePrice, self.lbPrice)
                if self.leFullName.text() == "" or self.leLenPower.text() == "" or self.leWeight.text() == "" or \
                        self.leLenVideo.text() == "" or self.leHeightCool.text() == "" or self.leColor.text() == "" \
                        or self.leFMother.text() == "" or self.lePrice.text() == "":
                    dialog = DialogOk("Ошибка", "Все поля должны быть заполнены")
                    dialog.show()
                else:
                    cur.callproc('insert_body', [id_pr.pop(),
                                                 self.leFullName.text(),
                                                 self.cbGaming.currentText(),
                                                 self.cbType.currentText(),
                                                 self.leFMother.text(),
                                                 self.cbFPower.currentText(),
                                                 self.leLenVideo.text(),
                                                 self.leHeightCool.text(),
                                                 self.leLenPower.text(),
                                                 float(self.leWeight.text()),
                                                 self.leColor.text(),
                                                 int(self.lePrice.text())])
                    self.close()
            else:  # Если повторяем заказ - вызываем 1 процедуру и заполняем её
                mark_labels(self.leKol, self.lbKol)
                if self.leKol.text() == "" or int(self.leKol.text()) < 1:
                    dialog = DialogOk("Ошибка", "Заполните поле 'Количество' числом >= 1 ")
                    dialog.show()
                else:
                    id_izd = {i for i in dict_body
                              if dict_body[i] == self.leFullName.text()}
                    cur.callproc('insert_order_body', [id_izd.pop(),
                                                       int(self.leKol.text()),
                                                       self.dateEdit.dateTime().toString("yyyy-MM-dd")])
                self.close()

        except (Exception, psycopg2.DatabaseError) as error:
            dialog = DialogOk("Ошибка", error)
            dialog.show()
        finally:
            if conn:
                conn.commit()
                cur.close()
                conn.close()
                main_window.reset_all_config()
                main_window.reset_radiobutton(main_window.tableSklad)
                main_window.load_sklad(7)
                main_window.load_conf(7)
                main_window.toolBoxNavigation.setCurrentIndex(7)
                main_window.create_sklad_filter()
                main_window.create_conf_filter()
