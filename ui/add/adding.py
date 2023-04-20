import sys
import psycopg2

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QDateTime
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QDialog, QTableWidgetItem
# ----------файлы интерфейса---------------
from ui import warningWin, acceptionWin
from ui.add import addChVidWidg


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
    def __init__(self, mainWindow, new_bool, list_valid_proizv, dict_proizv, dict_videocard):
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
        self.btnVidSave.clicked.connect(
            lambda: self.sql_insert_videocard(new_bool, mainWindow, dict_proizv, dict_videocard))

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

        self.leVolume.setValidator(five_digits_int)
        self.leBus.setValidator(four_digits_int)
        self.leFreq.setValidator(four_digits_int)
        self.leTdp.setValidator(three_digits_int)
        self.leLength.setValidator(two_digits_int)
        self.leKol.setValidator(four_digits_int)
        self.lePrice.setValidator(six_digits_int)
        self.cbProizv.clear()
        if type(list_valid_proizv) == str:  # Если передан 1 параметр в виде строки
            one_list = [list_valid_proizv]
            self.cbProizv.addItems(one_list)
        else:
            self.cbProizv.addItems(list_valid_proizv)

    # Проверяет и окрашивает название поле, если то заполнено неверно (не заполнено вовсе)
    def mark_labels(self, line_edit, label):
        if line_edit.text() != "":  # Если верно - перезадаём стиль (меняем цвет на белый)
            label.setStyleSheet("")
            if label.text()[-1] == "*":  # Если мы меняли эту строку - удаляем 2 символа
                label.setText(label.text()[:len(label.text()) - 2])
        else:  # Если заполнено неверно - добавление * и окрашивание надписи в красный
            if label.text()[-1] != "*":  # Если не меняли строку - не добавляем "*"
                label.setText(label.text() + ' *')
                label.setStyleSheet("color: rgb(240,0,0);")

    # Метод отправки запроса в БД на создание записи. выдаёт ошибку, если есть пустые поля
    # Окрашивает надписи к полям, которые не заполнены (cb заполнены всегда, поэтому их не красит)
    def sql_insert_videocard(self, new_bool, mainWindow, dict_proizv, dict_videocard):
        self.mark_labels(self.leFullName, self.lbFullName)
        self.mark_labels(self.leChipName, self.lbChipName)
        self.mark_labels(self.leVolume, self.lbVolume)
        self.mark_labels(self.leType, self.lbType)
        self.mark_labels(self.leBus, self.lbBus)
        self.mark_labels(self.leFreq, self.lbFreq)
        self.mark_labels(self.leTdp, self.lbTdp)
        self.mark_labels(self.leLength, self.lbLength)
        self.mark_labels(self.lePrice, self.lbPrice)
        if self.leFullName.text() == "" or self.leChipName.text() == "" or self.leVolume.text() == "" or \
                self.leType.text() == "" or self.leBus.text() == "" or self.leFreq.text() == "" or \
                self.leResolution.text() == "" or self.leLength.text() == "" \
                or self.leTdp.text() == "" or self.lePrice == "":
            self.dialog = DialogOk("Ошибка", "Все поля должны быть заполнены")
            self.dialog.show()
        else:  # Подтверждение создания заказа?
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
                    cur.callproc('insert_videocard', [id_pr.pop(),
                                                      self.leFullName.text(),
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
                                                      int(self.lePrice.text())])
                    """id_izd = {i for i in dict_videocard
                              if dict_videocard[i] == self.leFullName.text()}
                    cur.callproc('insert_order_videocard', [id_izd.pop(),
                                                            self.leKol.text(),
                                                            self.dateEdit.dateTime()])"""
                else:  # Если повторяем заказ - вызываем 1 процедуру и заполняем её
                    id_izd = {i for i in dict_videocard
                              if dict_videocard[i] == self.leFullName.text()}
                    cur.callproc('insert_order_videocard', [id_izd.pop(),
                                                            int(self.leKol.text()),
                                                            self.dateEdit.dateTime().toString("yyyy-MM-dd")])

            except (Exception, psycopg2.DatabaseError) as error:
                self.dialog = DialogOk("Ошибка", error)
                self.dialog.show()
            finally:
                if conn:
                    conn.commit()
                    cur.close()
                    conn.close()
                    mainWindow.load_all_sklad(0)  # Загрузка обновлённой таблицы из БД с 0 страницей (0 - видеокарты)
                    self.close()
