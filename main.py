import sys

from PyQt5 import QtWidgets

from ui import main_interface
from ui import untitled

class MainWindow(QtWidgets.QMainWindow, main_interface.Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        # self.ui = main_interface.Ui_MainWindow()
        self.setupUi(self)
        self.setWindowTitle('Конфигуратор ПК')
        self.pushButton.clicked.connect(lambda: print('работает'))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()