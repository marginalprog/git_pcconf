import sys

from PyQt5 import QtWidgets, QtCore, QtGui, Qt
from PyQt5.QtWidgets import QDialog, QTableWidgetItem
from PyQt5.QtGui import QIcon, QPixmap
from ui import main_interface, addChVidWidg, warningWin


# Класс диалогового окна с кнопкой
class DialogOk(QDialog, warningWin.Ui_warningDialog):
    def __init__(self, text):
        QDialog.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("Ошибка")
        self.lbErrDescription.setText(text)
        self.btnCancel.clicked.connect(lambda: self.close())


# Класс окна с добавлением\редактированием видеокарты
class AddChangeVideoWindow(QtWidgets.QWidget, addChVidWidg.Ui_addChVidWidg):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btnVidCancel.clicked.connect(lambda: self.close())


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

        self.treeWidget.itemClicked.connect(lambda: self.treeNavigation())

        #  self.toolBox_2.currentChanged.connect(lambda: self.toolBox_2.currentIndex())
        self.btnAdd.clicked.connect(lambda: self.tbChanged(
                                                         self.toolBox_2.currentIndex(),
                                                         True,
                                                         self.twSklad.currentRow())
                                    )
        self.btnChange.clicked.connect(lambda: self.tbChanged(
                                                             self.toolBox_2.currentIndex(),
                                                             False,
                                                             self.readSklad(
                                                                 self.twSklad.currentRow(),
                                                                 self.twSklad.columnCount()))
                                       )
        testPrice = "33500"
        item = QTableWidgetItem(testPrice)
        item.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)

        self.scrollArea.verticalScrollBar().value() # значение отловить

        self.twSklad.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
        self.twSklad.verticalHeader().setDefaultAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
        # предпросмотр закзаа
        self.table_config.setItem(0, 1, item)
        self.table_config.setColumnWidth(0, 170)
        self.table_config.setColumnWidth(1, 55)
        self.table_config.setColumnWidth(2, 15)
        #####
        self.tableConfVideo.setColumnWidth(0, 50)
        self.tableConfVideo.setColumnWidth(1, 40)
        self.tableConfVideo.setColumnWidth(2, 180)
        self.tableConfVideo.setColumnWidth(3, 180)
        self.tableConfVideo.cellClicked.connect(self.cell_row)
        self.row_selected = None
        self.insert_rb(self.tableConfVideo)
        ''' в дальнейшем existence будет из строк БД принимать true|false
         и вставлять соответствующее в таблицу состояние комплектующего
         Или if kol > 0 then....'''
        self.existence(self.tableConfVideo, True)

    def treeNavigation(self):
        index = self.treeWidget.currentIndex().row()
        match index:
            case 0:
                self.scrollArea.verticalScrollBar().setValue(500)
            case 1:
                self.scrollArea.verticalScrollBar().setValue(0)
            case 2:
                self.scrollArea.verticalScrollBar().setValue(0)
            case 3:
                self.scrollArea.verticalScrollBar().setValue(0)
            case 4:
                self.scrollArea.verticalScrollBar().setValue(0)
            case 5:
                self.scrollArea.verticalScrollBar().setValue(0)
            case 6:
                self.scrollArea.verticalScrollBar().setValue(0)
            case 7:
                self.scrollArea.verticalScrollBar().setValue(0)

    # чтение выбранной строки в таблце для редактирования
    def readSklad(self, cur_row, count_col):
        data_row = []
        if cur_row == -1:
            err = "Выберите строку для изменения"
            return err
        else:
            for i in range(2, count_col):
                data_row.append(self.twSklad.item(cur_row, i).text())
            return data_row

    def tbChanged(self, page, button, row):
        match page:
            case 0:  # 0-9 - вкладки ToolBox (меню навигации)
                if button:  # Если True - добавляем новую запись: открываем пустое окно
                    self.win_add_change = AddChangeVideoWindow(self)
                    self.win_add_change.show()
                else:  # Есил False - изменяем выбранную запись
                    if type(row) is str:  # Если пришел не список, а строка - вывод окна с ошибкой
                        self.dialog = DialogOk(row)
                        self.dialog.show()
                        if self.dialog.exec():
                            pass
                    else:  # Если пришел список - заполняем окно
                        self.win_add_change = AddChangeVideoWindow(self)
                        self.win_add_change.teVidName.setText(row[0])
                        self.win_add_change.teVidChip.setText(row[1])
                        self.win_add_change.teVidType.setText(row[2])
                        self.win_add_change.show()
            case 1:
                print("Процессоры")
            case 2:
                print("ццц")
            case 3:
                print("sss")

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

    # метод заполнения ячейки с состоянием
    def existence(self, table, bool_sklad):
        row_count = table.rowCount()
        for i in range(row_count):
            if bool_sklad:
                table.setCellWidget(i, 1, self.create_existence("E:/pcconf/images/have.png"))
            else:
                table.setCellWidget(i, 1, self.create_existence("E:/pcconf/images/unhave.png"))

    # Метод создания рб на виджете
    def create_radioButton(self):
        widget = QtWidgets.QWidget()
        rb = RadioButton()
        pLayout = QtWidgets.QHBoxLayout(widget)
        pLayout.addWidget(rb)
        pLayout.setAlignment(QtCore.Qt.AlignCenter)
        pLayout.setContentsMargins(0, 0, 0, 0)
        widget.setLayout(pLayout)
        return widget, rb

    def cell_row(self, row, column):
        # print(f'\n row={row}; column={column}')
        self.row_selected = row
        rb = self.button_group.button(row)
        rb.click()

    # метод вставки в таблицу рб-шек
    def insert_rb(self, table):
        row_count = table.rowCount()

        self.button_group = QtWidgets.QButtonGroup(self)
        self.button_group.setExclusive(True)

        for i in range(row_count):
            widget, radio = self.create_radioButton()
            radio.toggled.connect(lambda ch, row=i: self.currentPos(ch, row, table))
            table.setCellWidget(i, 0, widget)

            self.button_group.addButton(radio)
            self.button_group.setId(radio, i)

    def currentPos(self, ch, row, table):
        # print(f' row = {row} -- {ch}')
        if ch:
            self.row_selected = row
            table.selectRow(row)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
