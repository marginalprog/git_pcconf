import sys

from PyQt5 import QtWidgets
# ----------файлы интерфейса---------------
from ui.help import widgetVideoHelp, widgetProcHelp, widgetMotherHelp, widgetBodyHelp
from ui.help import widgetCoolHelp, widgetRamHelp, widgetDiskHelp, widgetPowerHelp


# -----------Классы окон с подсказкой-------------
class VideoHelp(QtWidgets.QWidget, widgetVideoHelp.Ui_widgetVideoHelp):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


class ProcHelp(QtWidgets.QWidget, widgetProcHelp.Ui_widgetProcHelp):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


class MotherHelp(QtWidgets.QWidget, widgetMotherHelp.Ui_widgetMotherHelp):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


class CoolHelp(QtWidgets.QWidget, widgetCoolHelp.Ui_widgetCoolHelp):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


class RamHelp(QtWidgets.QWidget, widgetRamHelp.Ui_widgetRamHelp):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


class DiskHelp(QtWidgets.QWidget, widgetDiskHelp.Ui_widgetDiskHelp):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


class PowerHelp(QtWidgets.QWidget, widgetPowerHelp.Ui_widgetPowerHelp):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


class BodyHelp(QtWidgets.QWidget, widgetBodyHelp.Ui_widgetBodyHelp):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
