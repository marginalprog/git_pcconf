import sys

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
        self.lbErrDescription.setText(error_text)
        self.btnCancel.clicked.connect(lambda: self.close())


# Класс окна с добавлением\редактированием видеокарты
class AddChangeVideoWindow(QtWidgets.QWidget, addChVidWidg.Ui_addChVidWidg):
    def __init__(self, new_bool, list_valid_proizv):
        super().__init__()
        self.setupUi(self)
        if new_bool:
            self.setWindowTitle("Создание заказа")
        else:
            self.setWindowTitle("Повторный заказ")
        self.dateEdit.setDateTime(QDateTime.currentDateTime())
        #  временные рамки заказа?
        # Вызов метода проверки корректности заполнения полей
        self.btnVidSave.clicked.connect(self.sql_insert_videocard)

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
    def sql_insert_videocard(self):
        self.mark_labels(self.leFullName, self.lbFullName)
        self.mark_labels(self.leChipName, self.lbChipName)
        self.mark_labels(self.leVolume, self.lbVolume)
        self.mark_labels(self.leType, self.lbType)
        self.mark_labels(self.leBus, self.lbBus)
        self.mark_labels(self.leFreq, self.lbFreq)
        self.mark_labels(self.leResolution, self.lbResolution)
        self.mark_labels(self.leLength, self.lbLength)
        self.mark_labels(self.leKol, self.lbKol)
        self.mark_labels(self.lePrice, self.lbPrice)
        if self.leFullName.text() == "" or self.leChipName.text() == "" or self.leVolume.text() == "" or \
                self.leType.text() == "" or self.leBus.text() == "" or self.leFreq.text() == "" or \
                self.leResolution.text() == "" or self.leLength.text() == "" or self.leKol.text() == "" \
                or self.lePrice == "":
            self.dialog = DialogOk("Ошибка", "Все поля должны быть заполнены")
            self.dialog.show()
        else:
            print(f"SELECT insert_videocard(2,'MSI AMD Radeon RX 6600', 'AMD', 'RX 6600',"
                  f" 8, 'GDDR6', 2044, 128, 'PCI-E 4.0', 4, '7680x4320', 132, 33, 26490);")
            self.close()
