import sys

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QDialog, QTableWidgetItem
from PyQt5.QtGui import QPixmap
from ui import main_interface, warningWin
from ui.add import adding  # импорт файла со всеми окнами добавления
from ui.help import helping  # импорт файла со всеми окнами помощи
from ui.filter import filters  # импорт файла со всеми фильтрами


# Класс диалогового окна с кнопкой
class DialogOk(QDialog, warningWin.Ui_warningDialog):
    def __init__(self, text):
        QDialog.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("Ошибка")
        self.lbErrDescription.setText(text)
        self.btnCancel.clicked.connect(lambda: self.close())


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
        #  self.toolBoxNavigation.currentChanged.connect(lambda: self.toolBoxNavigation.currentIndex())
        self.btnAdd.clicked.connect(lambda: self.tbChanged(
            self.toolBoxNavigation.currentIndex(),
            True,
            self.twSklad.currentRow())
                                    )
        self.btnChange.clicked.connect(lambda: self.tbChanged(
            self.toolBoxNavigation.currentIndex(),
            False,
            self.readSklad(
                self.twSklad.currentRow(),
                self.twSklad.columnCount()))
                                       )

        # ---------------------Кнопки с помощью---------------------------
        self.vHelp = helping.VideoHelp()
        self.btnVidHelp.clicked.connect(lambda: self.vHelp.show())

        # ----------------------------------------------------------------

        # ---------------------Кнопки с фильтрами---------------------------
        self.fVideo = filters.VideoFilter()
        self.btnVidFilter.clicked.connect(lambda: self.fVideo.show())

        # ----------------------------------------------------------------

        self.twSklad.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
        self.twSklad.verticalHeader().setDefaultAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
        # предпросмотр закзаа
        testName = "LambrGambr"
        testPrice = "33500"
        item1 = QTableWidgetItem(testName)
        item2 = QTableWidgetItem(testPrice)

        item2.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
        self.table_config.setItem(0, 1, item1)
        self.table_config.setItem(0, 2, item2)
        self.table_config.setColumnWidth(0, 0)
        self.table_config.setColumnWidth(1, 170)
        self.table_config.setColumnWidth(2, 55)
        self.table_config.setColumnWidth(3, 15)
        #####
        self.tableConfVideo.setColumnWidth(0, 50)
        self.tableConfVideo.setColumnWidth(1, 40)
        self.tableConfVideo.setColumnWidth(2, 180)
        self.tableConfVideo.setColumnWidth(3, 180)

        self.dict_button_group = {}
        self.tableConfVideo.cellClicked.connect(
            lambda row, column, table=self.tableConfVideo:
            self.cell_row(row, column, table))

        self.tableConfVideo.cellClicked.connect(lambda: self.fill_cart(0,
                                                                       self.tableConfVideo.item(
                                                                           self.tableConfVideo.currentRow(), 2).text(),
                                                                       self.tableConfVideo.item(
                                                                           self.tableConfVideo.currentRow(), 3).text())
                                                )

        self.tableConfProc.cellClicked.connect(
            lambda row, column, table=self.tableConfProc:
            self.cell_row(row, column, table))

        self.tableConfProc.cellClicked.connect(lambda: self.fill_cart(1,
                                                                      self.tableConfProc.item(
                                                                          self.tableConfProc.currentRow(), 2).text(),
                                                                      self.tableConfProc.item(
                                                                          self.tableConfProc.currentRow(), 3).text())
                                               )
        self.row_selected = None
        self.insert_rb(self.tableConfVideo)
        self.insert_rb(self.tableConfProc)

        ''' в дальнейшем existence будет из строк БД принимать true|false
         и вставлять соответствующее в таблицу состояние комплектующего
         Или if kol > 0 then....'''
        self.existence(self.tableConfVideo, True)
        self.existence(self.tableConfProc, True)

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
                    self.win_add_change = adding.AddChangeVideoWindow()
                    self.win_add_change.setWindowTitle("Создание заказа")
                    self.win_add_change.show()
                else:  # Есил False - изменяем выбранную запись
                    if type(row) is str:  # Если пришел не список, а строка(ошибка) - вывод окна с ошибкой
                        self.dialog = DialogOk(row)
                        self.dialog.show()
                        if self.dialog.exec():
                            pass
                        '''Убрал кнопку с изменением данных товара! теперь проверка неактуальна'''
                    '''else:  # Если пришел список - заполняем окно.
                        self.win_add_change = AddChangeVideoWindow()
                        self.win_add_change.setWindowTitle("Изменить запись")
                        self.win_add_change.teVidName.setText(row[0])
                        self.win_add_change.teVidChip.setText(row[1])
                        self.win_add_change.teVidType.setText(row[2])
                        self.win_add_change.show()'''
            case 1:
                if button:  # Если True - добавляем новую запись: открываем пустое окно
                    self.win_add_change = adding.AddChangeVideoWindow()
                    self.win_add_change.setWindowTitle("Создание заказа")
                    #self.win_add_change.radioButton = RadioButton()
                    self.win_add_change.show()
            case 2:
                if button:  # Если True - добавляем новую запись: открываем пустое окно
                    self.win_add_change = adding.AddChangeVideoWindow()
                    self.win_add_change.setWindowTitle("Создание заказа")
                    self.win_add_change.show()
            case 3:
                if button:  # Если True - добавляем новую запись: открываем пустое окно
                    self.win_add_change = adding.AddChangeVideoWindow()
                    self.win_add_change.setWindowTitle("Создание заказа")
                    self.win_add_change.show()
            case 4:
                if button:  # Если True - добавляем новую запись: открываем пустое окно
                    self.win_add_change = adding.AddChangeVideoWindow()
                    self.win_add_change.setWindowTitle("Создание заказа")
                    self.win_add_change.show()
            case 5:
                if button:  # Если True - добавляем новую запись: открываем пустое окно
                    self.win_add_change = adding.AddChangeVideoWindow()
                    self.win_add_change.setWindowTitle("Создание заказа")
                    self.win_add_change.show()
            case 6:
                if button:  # Если True - добавляем новую запись: открываем пустое окно
                    self.win_add_change = adding.AddChangeVideoWindow()
                    self.win_add_change.setWindowTitle("Создание заказа")
                    self.win_add_change.show()
            case 7:
                if button:  # Если True - добавляем новую запись: открываем пустое окно
                    self.win_add_change = adding.AddChangeVideoWindow()
                    self.win_add_change.setWindowTitle("Создание заказа")
                    self.win_add_change.show()

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
        for i in range(row_count):  # потом вызов построчно. (цикл уйдет)
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

    # Метод вставки в таблицу рб-шек
    def insert_rb(self, table):
        row_count = table.rowCount()

        button_group = QtWidgets.QButtonGroup(self)
        button_group.setExclusive(True)

        for i in range(row_count):
            widget, radio = self.create_radioButton()
            radio.toggled.connect(
                lambda ch, row=i: self.currentPos(ch, row, table))
            table.setCellWidget(i, 0, widget)

            button_group.addButton(radio)
            button_group.setId(radio, i)
        self.dict_button_group[table.objectName()] = button_group

    def cell_row(self, row, column, table):
        #print(f'\n row={row}; column={column}')
        button_group = self.dict_button_group[table.objectName()]
        rb = button_group.button(row)
        rb.click()

    def currentPos(self, ch, row, table):
        #print(f' row = {row} -- {ch}')
        if ch:
            table.selectRow(row)

    # Метод заполнения корзины выбранных комплектующих (принимает флаг, из какой таблицы был вызван, имя и цену)

    def fill_cart(self, id_table, name, price):
        row_count = self.table_config.rowCount()
        insert_row = self.check_cart(id_table)
        if insert_row == -1:  # если не найдена запись
            self.table_config.setRowCount(row_count + 1)
            self.table_config.setItem(row_count, 0, QTableWidgetItem(str(id_table)))
            self.table_config.setItem(row_count, 1, QTableWidgetItem(name))
            self.table_config.setItem(row_count, 2, QTableWidgetItem(price))
        else:
            # дублируется вставка ид таблицы для случая пустой корзины (вставить на 0 место)
            self.table_config.setItem(insert_row, 0, QTableWidgetItem(str(id_table)))
            self.table_config.setItem(insert_row, 1, QTableWidgetItem(name))
            self.table_config.setItem(insert_row, 2, QTableWidgetItem(price))

        # Метод проверки корзины на наличие выбранного типа комплектуюшего (вызывается из .fill_cart)
    def check_cart(self, id_table):
        if self.table_config.rowCount() == 0:  # если корзина пуста - вернуть -1
            return -1
        else:
            for i in range(self.table_config.rowCount()):
                s = self.table_config.item(i, 0).text()
                if self.table_config.item(i, 0).text() == str(id_table):
                    return i
            return -1  # если не найдено записей - вернуть -1


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
