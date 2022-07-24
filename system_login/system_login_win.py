from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QLineEdit

from .system_login import Ui_Dialog


class system_login_window(QtWidgets.QDialog, Ui_Dialog):
    enter_signal = pyqtSignal()

    def __init__(self):
        super(system_login_window, self).__init__()
        self.setupUi(self)
        self.slot_init()

        self.lineEdit_pw.setEchoMode(QLineEdit.Password)
        self.label_3.setAlignment(Qt.AlignCenter)

    def register_skip(self):
        if self.lineEdit_id.text() == 'dx' and self.lineEdit_pw.text() == '0925':
            self.label_3.setStyleSheet("color:blue")
            self.label_3.setText('登录成功!')
            self.lineEdit_pw.clear()
            self.close()
            self.label_3.clear()
            self.enter_signal.emit()
        else:
            self.label_3.setStyleSheet("color:red")
            self.label_3.setText('登录失败!')

    def slot_init(self):
        self.pushButton_register.clicked.connect(self.register_skip)
