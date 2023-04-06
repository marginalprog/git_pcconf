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
class AddProizv(QtWidgets.QWidget, addProizvWidget.Ui_addProizvWidget):
    def __init__(self, text_complect):
        super().__init__()
        self.setupUi(self)
        self.labelComplect.setText(text_complect)
        self.btnProizvSave.clicked.connect(lambda: self.create_proizv_query(text_complect, self.leProzivName.text()))

        self.btnProizvSave.clicked.connect(lambda: self.close())

    def create_proizv_query(self, text_complect, proizv_name):
        match text_complect:
            case "Поставщик видеокарт":
                print(f"INSERT INTO Proizv_videocard (name) VALUES ({proizv_name});")


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
        self.btnAdd.clicked.connect(lambda: self.tb_new_komplekt(
            self.toolBoxNavigation.currentIndex(),
            True,
            self.twSklad.currentRow())
                                    )
        # Кнопка повтора заказа уже имеющегося (выбранного) комплектующего
        self.btnRepeat.clicked.connect(lambda: self.tb_new_komplekt(
            self.toolBoxNavigation.currentIndex(),
            False,
            self.read_sklad(
                self.twSklad.currentRow(),
                self.twSklad.columnCount()))
                                       )

        # По нажатии на кнопку запускается метод, который принимает выбранную вклдку ТБ и открывает нужное окно фильтра
        self.btnSkladFilter.clicked.connect(lambda: self.tb_sklad_filter(self.toolBoxNavigation.currentIndex()))
        # =================================Окна фильтрации комплектующих на складе=========================
        self.vidSkladFilter = filters.VideoFilter(0, self)  # Создаётся отдельный экземпляр для сохранения внесённых д-х
        # .......инициализация других окон фильтрации.......
        # =================================================================================================

        self.tableVideoProizv.setColumnWidth(0, 30)
        self.tableVideoProizv.setColumnWidth(1, 0)
        self.tableVideoProizv.setColumnWidth(2, 140)
        self.tableProcProizv.setColumnWidth(0, 30)
        self.tableProcProizv.setColumnWidth(1, 0)
        self.tableProcProizv.setColumnWidth(2, 140)
        self.tableMotherProizv.setColumnWidth(0, 30)
        self.tableMotherProizv.setColumnWidth(1, 0)
        self.tableMotherProizv.setColumnWidth(2, 140)
        self.tableCoolProizv.setColumnWidth(0, 30)
        self.tableCoolProizv.setColumnWidth(1, 0)
        self.tableCoolProizv.setColumnWidth(2, 140)
        self.tableRamProizv.setColumnWidth(0, 30)
        self.tableRamProizv.setColumnWidth(1, 0)
        self.tableRamProizv.setColumnWidth(2, 140)
        self.tableDiskProizv.setColumnWidth(0, 30)
        self.tableDiskProizv.setColumnWidth(1, 0)
        self.tableDiskProizv.setColumnWidth(2, 140)
        self.tablePowerProizv.setColumnWidth(0, 30)
        self.tablePowerProizv.setColumnWidth(1, 0)
        self.tablePowerProizv.setColumnWidth(2, 140)
        self.tableBodyProizv.setColumnWidth(0, 30)
        self.tableBodyProizv.setColumnWidth(1, 0)
        self.tableBodyProizv.setColumnWidth(2, 140)

        self.btnNewVideoProizv.clicked.connect(lambda: AddProizv("Поставщик видеокарт").show())  # x8

        self.btnCngVideoProizv.clicked.connect(lambda: self.change_proizv(self.tableVideoProizv.currentRow(), self.tableVideoProizv))

        self.insert_existence(self.tableVideoProizv)
        self.query_sklad = ""
        self.query_conf = ""
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
        self.vidConfFilter = filters.VideoFilter(1, self)  # Создаётся отдельный экземпляр для сохранения внесённых д-х
        self.btnVidFilter.clicked.connect(lambda: self.vidConfFilter.show())

        # ---------------------------------------------------------------------

        # -----------------------Кнопка сброса сборки--------------------------
        self.btnResetConfig.clicked.connect(self.reset_all)
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
        # self.paste_existence(self.tableVideoProizv, True, 1)

    # изменение состояния в таблице поставщика
    def change_proizv(self, cur_row, table):
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

    # Чтение выбранной строки в таблце для передачи в перезаказ
    def read_sklad(self, cur_row, count_col):
        data_row = []
        if cur_row == -1:
            err = "Выберите строку для изменения"
            return err
        else:
            for i in range(2, count_col):
                data_row.append(self.twSklad.item(cur_row, i).text())
            return data_row

    # Метод, заполняющий и блокирующий поле  ввода данных lineEdit
    def block_line_edit(self, field, parameter):
        field.setText(parameter)
        field.setDisabled(True)
        field.setStyleSheet("color:gray; border: 1px dotted rgb(120,120,120);")

    # # Метод, заполняющий и блокирующий поле  ввода данных comboBox
    def block_combo_box(self, field, parameter):
        field.setItemText(0, parameter)
        field.setDisabled(True)
        field.setStyleSheet("QComboBox{color:gray; border: 1px dotted rgb(120,120,120);}"
                            " QComboBox::drop-down{border: 0px;}"
                            '''QComboBox::down-arrow {
                                border-image: url("E:/pcconf/images/down-arrow-gray.png");
                                width: 17px;
                                height: 17px;
                                margin-right: 5px;}''')

    # Метод, завязанный на выбранном в toolbox комплектующем на складе (page).
    # При нажатии на кнопку добавить или изменить передается true\false (new_bool).
    # Если true - добавляем новое комплектующее. Если false - создаём заказ на существующее комплектующее
    def tb_new_komplekt(self, page, new_bool, row):
        match page:
            case 0:  # 0-9 - вкладки ToolBox (меню навигации)
                if new_bool:  # Если True - добавляем новую запись: открываем пустое окно
                    self.win_add_change = adding.AddChangeVideoWindow(new_bool)
                    self.win_add_change.show()
                else:  # Есил False - изменяем выбранную запись
                    if type(row) is str:  # Если пришел не список, а строка(ошибка) - вывод окна с ошибкой
                        self.dialog = DialogOk("Ошибка", row)
                        self.dialog.show()
                        if self.dialog.exec():
                            pass
                    else:  # Если пришел список - заполняем окно.
                        self.win_add_change = adding.AddChangeVideoWindow(new_bool)
                        self.block_line_edit(self.win_add_change.leVidName, row[0])
                        self.block_line_edit(self.win_add_change.leVidChipName, row[1])
                        self.block_line_edit(self.win_add_change.leVidType, row[2])
                        self.block_combo_box(self.win_add_change.comBoxVidChipCr, row[2])
                        self.win_add_change.show()
            case 1:
                if new_bool:  # Если True - добавляем новую запись: открываем пустое окно
                    self.win_add_change = adding.AddChangeVideoWindow()
                    #  self.win_add_change.radioButton = RadioButton()
                    self.win_add_change.show()
            case 2:
                if new_bool:  # Если True - добавляем новую запись: открываем пустое окно
                    self.win_add_change = adding.AddChangeVideoWindow()
                    self.win_add_change.show()
            case 3:
                if new_bool:  # Если True - добавляем новую запись: открываем пустое окно
                    self.win_add_change = adding.AddChangeVideoWindow()
                    self.win_add_change.show()
            case 4:
                if new_bool:  # Если True - добавляем новую запись: открываем пустое окно
                    self.win_add_change = adding.AddChangeVideoWindow()
                    self.win_add_change.show()
            case 5:
                if new_bool:  # Если True - добавляем новую запись: открываем пустое окно
                    self.win_add_change = adding.AddChangeVideoWindow()
                    self.win_add_change.show()
            case 6:
                if new_bool:  # Если True - добавляем новую запись: открываем пустое окно
                    self.win_add_change = adding.AddChangeVideoWindow()
                    self.win_add_change.show()
            case 7:
                if new_bool:  # Если True - добавляем новую запись: открываем пустое окно
                    self.win_add_change = adding.AddChangeVideoWindow()
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
        # row_count = table.rowCount()
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
    def reset_all(self):
        self.reset_radiobutton(self.tableConfVideo)
        self.reset_radiobutton(self.tableConfProc)
        self.reset_radiobutton(self.tableConfMother)
        self.reset_radiobutton(self.tableConfCool)
        self.reset_radiobutton(self.tableConfRam)
        self.reset_radiobutton(self.tableConfDisk)
        self.reset_radiobutton(self.tableConfPower)
        self.reset_radiobutton(self.tableConfBody)

    # Метод, обнуляющий RadioButton в таблице комплектующих, а также очищающий таблицу с предпросмотром
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
            widget, radio = self.create_radiobutton()
            radio.toggled.connect(
                lambda ch, row=i: self.current_pos(ch, row, table))
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
