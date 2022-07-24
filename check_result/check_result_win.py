from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from .check_result import Ui_Dialog
import glob as gb


class check_result_window(QtWidgets.QDialog, Ui_Dialog):
    back_check_signal = pyqtSignal()
    quit_system_signal = pyqtSignal()

    def __init__(self):
        super(check_result_window, self).__init__()
        self.setupUi(self)
        self.textBrowser.append("  姓名  " + "  班级  " + "    学号    " + "\n")
        self.textBrowser_2.append("  姓名  " + "  班级  " + "    学号    " + "\n")
        self.img_path = gb.glob(r'D:\MyCode\pythonProject\face_recognition_dx\face_images\*.jpg')
        self.picture_name = None
        self.known_face_names = []
        self.known_class_nos = []
        self.known_nos = []
        self.get_info()

    def slot_init(self):
        self.pushButton.clicked.connect(self.back_check)
        self.pushButton_2.clicked.connect(self.quit_system)

    def get_info(self):
        for i in self.img_path:
            self.picture_name = i.replace('D:\MyCode\pythonProject\face_recognition_dx\face_images\*.jpg', '')
            no = self.picture_name[-16:-4]
            class_no = self.picture_name[-23:-16]
            name = i[56:-23]
            self.known_face_names.append(name)
            self.known_class_nos.append(class_no)
            self.known_nos.append(no)

    def get_result(self, names):
        num1 = len(names)
        num2 = len(self.known_face_names) - num1
        self.label_2.setText(str(num1))
        self.label_4.setText(str(num2))
        for name, class_no, no in zip(self.known_face_names, self.known_class_nos, self.known_nos):
            if name in names:
                self.textBrowser.append(name + "  " + class_no + "  " + no + "  ")
            else:
                self.textBrowser_2.append(name + "  " + class_no + "  " + no + "  ")

    def back_check(self):
        self.textBrowser.clear()
        self.textBrowser_2.clear()
        self.back_check_signal.emit()

    def quit_system(self):
        self.textBrowser
        self.textBrowser_2.clear()
        self.quit_system_signal.emit()
