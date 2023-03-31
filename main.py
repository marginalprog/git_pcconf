import sys

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QDialog, QTableWidgetItem
from PyQt5.QtGui import QPixmap
from ui import main_interface, warningWin, acceptionWin
from ui.add import adding  # импорт файла со всеми окнами добавления
from ui.help import helping  # импорт файла со всеми окнами помощи
from ui.filter import filters  # импорт файла со всеми фильтрами
from ui.post import addPostWidget  # импорт файла (виджета) добавления поставщика


# Класс окна с одной кнопкой
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


# Класс окна с добавлением поставщика
class AddPost(QtWidgets.QWidget, addPostWidget.Ui_addPostWidget):
    def __init__(self, text_complect):
        super().__init__()
        self.setupUi(self)
        self.labelComplect.setText(text_complect)
        self.btnPostSave.clicked.connect(lambda: self.createPostQuery(text_complect, self.lePostName.text()))
        self.btnPostSave.clicked.connect(lambda: self.close())

    def createPostQuery(self, text_complect, post_name):
        match text_complect:
            case "Поставщик видеокарт":
                print(f"INSERT INTO Post_videocard (exist, name) VALUES (True, {post_name});")


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
        # =============================== Надстройки вкладки "Склад"================================
        self.twSklad.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
        self.twSklad.verticalHeader().setDefaultAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
        #  self.toolBoxNavigation.currentChanged.connect(lambda: self.toolBoxNavigation.currentIndex())
        self.btnAdd.clicked.connect(lambda: self.tbChanged(
            self.toolBoxNavigation.currentIndex(),
            True,
            self.twSklad.currentRow())
                                    )
        # Кнопка будет удалена
        self.btnChange.clicked.connect(lambda: self.tbChanged(
            self.toolBoxNavigation.currentIndex(),
            False,
            self.readSklad(
                self.twSklad.currentRow(),
                self.twSklad.columnCount()))
                                       )
        # По нажатии на кнопку запускается метод, который принимает выбранную вклдку ТБ и открывает нужное окно фильтра
        self.btnSkladFilter.clicked.connect(lambda: self.tbClickFilter(self.toolBoxNavigation.currentIndex()))

        self.tableVideoPost.setColumnWidth(0, 30)
        self.tableVideoPost.setColumnWidth(1, 0)
        self.tableVideoPost.setColumnWidth(2, 140)
        self.tableProcPost.setColumnWidth(0, 30)
        self.tableProcPost.setColumnWidth(1, 0)
        self.tableProcPost.setColumnWidth(2, 140)
        self.tableMotherPost.setColumnWidth(0, 30)
        self.tableMotherPost.setColumnWidth(1, 0)
        self.tableMotherPost.setColumnWidth(2, 140)
        self.tableCoolPost.setColumnWidth(0, 30)
        self.tableCoolPost.setColumnWidth(1, 0)
        self.tableCoolPost.setColumnWidth(2, 140)
        self.tableRamPost.setColumnWidth(0, 30)
        self.tableRamPost.setColumnWidth(1, 0)
        self.tableRamPost.setColumnWidth(2, 140)
        self.tableDiskPost.setColumnWidth(0, 30)
        self.tableDiskPost.setColumnWidth(1, 0)
        self.tableDiskPost.setColumnWidth(2, 140)
        self.tablePowerPost.setColumnWidth(0, 30)
        self.tablePowerPost.setColumnWidth(1, 0)
        self.tablePowerPost.setColumnWidth(2, 140)
        self.tableBodyPost.setColumnWidth(0, 30)
        self.tableBodyPost.setColumnWidth(1, 0)
        self.tableBodyPost.setColumnWidth(2, 140)

        self.btnNewVideoPost.clicked.connect(lambda: AddPost("Поставщик видеокарт").show())  # x8

        self.btnCngVideoPost.clicked.connect(lambda: self.changePost(self.tableVideoPost.currentRow(), self.tableVideoPost))

        self.insert_existence(self.tableVideoPost)
        self.query = ""
        # ==========================================================================================

        # =========================== Надстройки вкладки "Конфигуратор"=============================
        self.treeWidget.itemClicked.connect(lambda: self.treeNavigation())
        # ----------------------Заполнение таблиц RB---------------------------
        self.dict_button_group = {}  # Словарь для хранения групп RB и таблиц, в которых они находятся
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
        self.btnVidFilter.clicked.connect(lambda: filters.VideoFilter(1, self).show())

        # ---------------------------------------------------------------------

        # -----------------------Кнопка сброса---------------------------------
        self.btnResetConfig.clicked.connect(self.resetAll)
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
        self. fill_tabs(self.video_tabs, self.tabWidgetVideo)
        self.fill_tabs(self.processor_tabs, self.tabWidgetProc)
        self.tabWidgetVideo.tabBarClicked.connect(lambda index: self.click_tab(index, self.tabWidgetVideo))
        self.tabWidgetProc.tabBarClicked.connect(lambda index: self.click_tab(index, self.tabWidgetProc))

        ''' в дальнейшем existence будет из строк БД принимать true|false
         и вставлять соответствующее в таблицу состояние комплектующего
         Или if kol > 0 then... '''
        for i in range(self.tableConfVideo.rowCount()):
            self.paste_existence(self.tableConfVideo, i, True, 2)
        # self.paste_existence(self.tableConfProc, True, 2)
        # self.paste_existence(self.tableVideoPost, True, 1)

    # изменение состояния в таблице поставщика
    def changePost(self, cur_row, table):
        if cur_row == -1:
            err = "Выберите поставщика для изменения"
            self.dialog = DialogOk("Ошибка", err)
            self.dialog.show()
        else:
            att = "Вы действительно хотите изменить договор поставок?"
            self.dialog = AcceptionWin("Подтвердите действие", att)
            self.dialog.show()
            if self.dialog.exec():
                if table.item(cur_row, 1).text() == "True":
                    self.paste_existence(table, cur_row, False, 1)
                    table.item(cur_row, 1).setText("False")  # Изменяем состояние в таблице
                    # здесь запрос в БД на изменение состояние поставщика (false->true)
                else:
                    self.paste_existence(table, cur_row, True, 1)
                    table.item(cur_row, 1).setText("True")
                    # здесь запрос в БД на изменение состояние поставщика (false->true)
                table.clearSelection()
            else:
                table.clearSelection()

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
                    self.win_add_change.show()
                else:  # Есил False - изменяем выбранную запись
                    if type(row) is str:  # Если пришел не список, а строка(ошибка) - вывод окна с ошибкой
                        self.dialog = DialogOk("Ошибка", row)
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
                    #  self.win_add_change.radioButton = RadioButton()
                    self.win_add_change.show()
            case 2:
                if button:  # Если True - добавляем новую запись: открываем пустое окно
                    self.win_add_change = adding.AddChangeVideoWindow()
                    self.win_add_change.show()
            case 3:
                if button:  # Если True - добавляем новую запись: открываем пустое окно
                    self.win_add_change = adding.AddChangeVideoWindow()
                    self.win_add_change.show()
            case 4:
                if button:  # Если True - добавляем новую запись: открываем пустое окно
                    self.win_add_change = adding.AddChangeVideoWindow()
                    self.win_add_change.show()
            case 5:
                if button:  # Если True - добавляем новую запись: открываем пустое окно
                    self.win_add_change = adding.AddChangeVideoWindow()
                    self.win_add_change.show()
            case 6:
                if button:  # Если True - добавляем новую запись: открываем пустое окно
                    self.win_add_change = adding.AddChangeVideoWindow()
                    self.win_add_change.show()
            case 7:
                if button:  # Если True - добавляем новую запись: открываем пустое окно
                    self.win_add_change = adding.AddChangeVideoWindow()
                    self.win_add_change.show()

    # Метод, отвечающий за открытие окна фильтрации на складе. Принимает id вкладки ToolBox
    def tbClickFilter(self, page):  # Отделить фильтрацию вызванную для склада и фильтрацию вызванную для конфигуратора
        match page:  # Передать в  конструктора класса параметры "склад" или "Конфигуратор"? Либо создать еще 8 окон...
            case 0:  # 0-9 - вкладки ToolBox (меню навигации)
                filters.VideoFilter(0, self).show()
            case 1:
                filters.VideoFilter(0, self).show()  # фильтр процессора и тп
            case 2:
                filters.VideoFilter(0, self).show()
            case 3:
                filters.VideoFilter(0, self).show()
            case 4:
                filters.VideoFilter(0, self).show()
            case 5:
                filters.VideoFilter(0, self).show()
            case 6:
                filters.VideoFilter(0, self).show()
            case 7:
                filters.VideoFilter(0, self).show()
            case 8:
                filters.VideoFilter(0, self).show()

    def send_sql_sklad(self):
        print(self.query)

    def send_sql_conf(self):
        print(self.query)

    # Метод для заполнения tabWidget-ов переданными
    def fill_tabs(self, list_names, tab_widget):
        count_tab = len(list_names)

        for i in range(1, count_tab + 1):  # первая вкладка должна остаться
            tab = QtWidgets.QWidget()
            tab_widget.addTab(tab, list_names[i - 1])

    def click_tab(self, tab_index, tab_widget):
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

    # метод заполнения ячейки наличием товара\поставщика
    def paste_existence(self, table, row, bool_, type_table):
        row_count = table.rowCount()
        match type_table:  # Если тип тиаблицы 1 (склад) - заполняем в 1 столбец. Если 2 (конфигуратор) - 2 столбец.
            case 1:
                if bool_:
                    table.setCellWidget(row, 0, self.create_existence("E:/pcconf/images/have.png"))
                else:
                    table.setCellWidget(row, 0, self.create_existence("E:/pcconf/images/nothave.png"))
            case 2:
                if bool_:
                    table.setCellWidget(row, 1, self.create_existence("E:/pcconf/images/have.png"))
                else:
                    table.setCellWidget(row, 1, self.create_existence("E:/pcconf/images/nothave.png"))

    def insert_existence(self, table):
        for i in range(table.rowCount()):  # заполнить столбец с бд и вызвать в цикле метод.
            if table.item(i, 1).text() == "True":
                self.paste_existence(table, i, True, 1)
            else:
                self.paste_existence(table, i, False, 1)

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

    # Метод, обнуляющий собранную конфигурацию
    def resetAll(self):
        self.resetRadioButton(self.tableConfVideo)
        self.resetRadioButton(self.tableConfProc)
        self.resetRadioButton(self.tableConfMother)
        self.resetRadioButton(self.tableConfCool)
        self.resetRadioButton(self.tableConfRam)
        self.resetRadioButton(self.tableConfDisk)
        self.resetRadioButton(self.tableConfPower)
        self.resetRadioButton(self.tableConfBody)

    # Метод, обнуляющий RadioButton в таблице комплектующих, а также очищающий таблицу с предпросмотром
    def resetRadioButton(self, table):
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

        for i in range(self.table_config.rowCount()):  # Проход по корзине и удаление строки по таблице
            if self.table_config.item(i, 0) is not None and self.table_config.item(i, 0).text() == str(table):
                self.table_config.removeRow(i)
        self.progressBar.setValue(self.table_config.rowCount())  # обновление прогрессбара

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
            self.fill_cart(table)

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
